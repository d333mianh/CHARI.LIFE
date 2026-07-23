#!/usr/bin/env python3
"""Sync the tea catalogue (teas.md) into a Telegram channel as editable posts.

Zero dependencies — uses only the Python standard library.

First run posts one message per tea and records each message_id in
telegram_state.json. Subsequent runs edit changed posts in place, add posts for
new teas, and (with --prune) delete posts for teas you removed.

Setup (one time):
  1. Create a bot via @BotFather (/newbot) and copy its token.
  2. Make the bot an admin of your channel with "Post Messages",
     "Edit Messages of Others" off but "Edit Messages" + "Delete Messages" on.
  3. Create webtea/.env (gitignored):
       TELEGRAM_BOT_TOKEN=123456:ABC...
       TELEGRAM_CHAT_ID=@chariteas

Usage:
  python3 sync_telegram.py --dry-run     # show what would happen, verify access
  python3 sync_telegram.py               # post new + edit changed
  python3 sync_telegram.py --prune       # also delete posts for removed teas
"""

import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
from html.parser import HTMLParser
import urllib.error
import urllib.parse
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
TEAS_MD = os.path.join(HERE, "teas.md")
SETS_HTML = os.path.join(HERE, "sets.html")  # sets are sourced from the website
PHOTOS_DIR = os.path.join(HERE, "photos")
STATE_FILE = os.path.join(HERE, "telegram_state.json")
ENV_FILE = os.path.join(HERE, ".env")
LINKS_FILE = os.path.join(HERE, "links.json")
API = "https://api.telegram.org/bot{token}/{method}"
SLEEP = 0.5  # seconds between write operations (rate limit headroom)

# A "website" URL button is added to every post. Set to None to disable.
WEBSITE_URL = None  # temporarily removed; set back to "https://chari.life/" to restore
WEBSITE_LABEL = "website"

# A single "index" post is kept first in the channel: a grouped catalogue
# where each tea name links to its own post. PIN_INDEX pins it to the top.
INDEX_HEADER = "🍵 Roman&Julia teas — catalogue"
INDEX_FOOTER = "→ tap a tea to open its post"
PIN_INDEX = True

# "Contact to order" block shown at the bottom of the pinned index post, plus a
# tappable button per contact. Each entry is (display_name, telegram_username
# without @). Set to [] to remove the block entirely.
ORDER_HEADING = "📩 To order / Для замовлення"
ORDER_CONTACTS = [
    ("Julia", "Lina_yogastan"),
    ("Roman", "romankryzhan"),
]


# ---------- env ----------

def load_env():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        sys.exit("Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID. "
                 "Create webtea/.env (see the docstring at the top of this file).")
    return token, chat


# ---------- telegram api ----------

def _multipart(fields, file_field, filename, filedata, ctype="image/jpeg"):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for k, v in fields.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode()
        body += f"{v}\r\n".encode()
    body += f"--{boundary}\r\n".encode()
    body += (f'Content-Disposition: form-data; name="{file_field}"; '
             f'filename="{filename}"\r\n').encode()
    body += f"Content-Type: {ctype}\r\n\r\n".encode()
    body += filedata + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return boundary, bytes(body)


def api(token, method, params=None, photo_path=None):
    url = API.format(token=token, method=method)
    if photo_path:
        with open(photo_path, "rb") as fh:
            data = fh.read()
        boundary, body = _multipart(params or {}, "photo",
                                    os.path.basename(photo_path), data)
        req = urllib.request.Request(url, data=body)
        req.add_header("Content-Type",
                       f"multipart/form-data; boundary={boundary}")
    else:
        body = urllib.parse.urlencode(params or {}).encode()
        req = urllib.request.Request(url, data=body)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        try:
            return json.load(exc)
        except Exception:
            return {"ok": False, "description": f"HTTP {exc.code}"}


def must(resp, context):
    if not resp.get("ok"):
        sys.exit(f"Telegram API error ({context}): "
                 f"{resp.get('error_code')} {resp.get('description')}")
    return resp["result"]


# ---------- markdown table parsing ----------

def parse_table(path, key_prefix=""):
    """Parse a teas.md-style pipe table. Each record's state key is
    key_prefix + slug(name) so sources (teas, sets) never collide while teas
    keep their original plain-slug keys for backward compatibility."""
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.startswith("|"):
                continue
            protected = line.replace("\\|", "\x00")
            cells = [c.strip().replace("\x00", "|")
                     for c in protected.strip().strip("|").split("|")]
            if len(cells) < 6:
                continue
            idx, name, desc, tags, photo, price = cells[:6]
            if not re.match(r"^\d+$", idx):  # skip header + separator rows
                continue
            rows.append({
                "idx": idx,
                "name": name,
                "desc": desc,
                "tags": [t.strip() for t in tags.split("|") if t.strip()],
                "photo": photo or None,
                "price": [p.strip() for p in price.split("/") if p.strip()],
                "key": key_prefix + slug(name),
            })
    return rows


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


class _CardParser(HTMLParser):
    """Extracts `.tea` cards from a site page (sets.html / index.html) so the
    website itself is the source of truth — no separate markdown to drift from.
    Reads each card's name, description, tags, price segments, and photo."""

    def __init__(self):
        super().__init__()
        self.cards = []
        self.cur = None          # card being built, or None when outside a card
        self.field = None        # which field text is flowing into right now
        self.buf = []

    def _flush(self):
        return "".join(self.buf).strip()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = a.get("class", "").split()
        if tag == "div" and "tea" in classes:
            self.cur = {"name": "", "desc": "", "tags": [],
                        "price_parts": [], "photo": None}
            self.cards.append(self.cur)
            return
        if self.cur is None:
            return
        if tag == "img" and "tea-photo" in classes:
            src = a.get("src", "")
            if src.startswith("photos/"):
                self.cur["photo"] = src[len("photos/"):]
        elif tag == "h3" and "tea-name" in classes:
            self.field, self.buf = "name", []
        elif tag == "p" and "tea-sub" in classes:
            self.field, self.buf = "desc", []
        elif tag == "span" and "tea-tag" in classes:
            self.field, self.buf = "tag", []
        elif tag == "div" and "tea-price" in classes:
            self.field, self.buf = "price", []
        elif tag == "br" and self.field == "price":
            seg = self._flush()
            if seg:
                self.cur["price_parts"].append(seg)
            self.buf = []

    def handle_data(self, data):
        if self.field:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if self.cur is None or self.field is None:
            return
        if self.field == "name" and tag == "h3":
            self.cur["name"] = self._flush()
            self.field = None
        elif self.field == "desc" and tag == "p":
            self.cur["desc"] = self._flush()
            self.field = None
        elif self.field == "tag" and tag == "span":
            t = self._flush()
            if t:
                self.cur["tags"].append(t)
            self.field = None
        elif self.field == "price" and tag == "div":
            seg = self._flush()
            if seg:
                self.cur["price_parts"].append(seg)
            self.field = None


def parse_cards_html(path, key_prefix=""):
    """Parse `.tea` cards out of a site page. Same record shape as
    parse_table(), so downstream code (caption, hash, posting) is identical."""
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        p = _CardParser()
        p.feed(fh.read())
    for i, c in enumerate(p.cards, 1):
        if not c["name"]:
            continue
        rows.append({
            "idx": f"{i:02d}",
            "name": html.unescape(c["name"]),
            "desc": html.unescape(c["desc"]),
            "tags": [html.unescape(t) for t in c["tags"]],
            "photo": c["photo"],
            "price": [html.unescape(p_) for p_ in c["price_parts"]],
            "key": key_prefix + slug(html.unescape(c["name"])),
        })
    return rows


def caption(tea):
    lines = [f"<b>{html.escape(tea['name'])}</b>"]
    if tea["tags"]:
        tagtxt = " · ".join(html.escape(t.lstrip("*").strip()) for t in tea["tags"])
        lines.append(f"<i>{tagtxt}</i>")
    if tea["desc"]:
        desc_lines = [part.strip() for part in tea["desc"].split(" // ")
                      if part.strip()]
        lines += [""] + [html.escape(part) for part in desc_lines]
    if tea["price"]:
        lines.append("")
        lines += [html.escape(p) for p in tea["price"]]
    return "\n".join(lines)


def content_hash(tea, cap):
    h = hashlib.sha256()
    h.update(cap.encode())
    if tea["photo"]:
        path = os.path.join(PHOTOS_DIR, tea["photo"])
        h.update(b"photo:")
        if os.path.exists(path):
            with open(path, "rb") as fh:
                h.update(fh.read())
    else:
        h.update(b"nophoto")
    return h.hexdigest()


def load_links():
    """Per-tea extra URL buttons, keyed by tea slug:
       { "gaba-ruby": [{"text": "огляд gabaruby", "url": "https://..."}] }
    """
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def build_markup(tea, links):
    """Inline keyboard: a global website button + any per-tea links,
    laid out two buttons per row. Returns None if there are no buttons."""
    btns = []
    if WEBSITE_URL:
        btns.append({"text": WEBSITE_LABEL, "url": WEBSITE_URL})
    for b in links.get(slug(tea["name"]), []):
        btns.append({"text": b["text"], "url": b["url"]})
    if not btns:
        return None
    rows = [btns[i:i + 2] for i in range(0, len(btns), 2)]
    return {"inline_keyboard": rows}


def markup_key(markup):
    """Stable string for change-detection."""
    return json.dumps(markup, sort_keys=True, ensure_ascii=False) if markup else ""


# ---------- index post ----------

def channel_username(chat):
    """Public @username (without @) if chat_id is a username, else None.
    Needed to build t.me/<username>/<message_id> deep links."""
    if isinstance(chat, str) and chat.startswith("@"):
        return chat[1:]
    return None


def index_markup():
    """The index post carries an order button per contact (top row), then the
    global website button (if set)."""
    rows = []
    if ORDER_CONTACTS:
        rows.append([{"text": f"✍️ {name}",
                      "url": f"https://t.me/{uname}"}
                     for name, uname in ORDER_CONTACTS])
    if WEBSITE_URL:
        rows.append([{"text": WEBSITE_LABEL, "url": WEBSITE_URL}])
    return {"inline_keyboard": rows} if rows else None


def build_index_text(teas, items, username):
    """Grouped catalogue: teas under their category heading (first tag), each
    name an HTML link to its own post. Category order follows first appearance
    in teas.md. Links are emitted only when we know the post's message_id."""
    groups = []           # [(category, [tea, ...]), ...]
    pos = {}              # category -> index in groups
    for tea in teas:
        cat = tea["tags"][0].lstrip("*").strip() if tea["tags"] else "OTHER"
        if cat not in pos:
            pos[cat] = len(groups)
            groups.append((cat, []))
        groups[pos[cat]][1].append(tea)

    lines = [f"<b>{html.escape(INDEX_HEADER)}</b>", ""]
    for cat, ts in groups:
        lines.append(f"<b>{html.escape(cat)}</b>")
        for tea in ts:
            name = html.escape(tea["name"])
            entry = items.get(tea["key"])
            mid = entry.get("message_id") if entry else None
            if username and mid:
                lines.append(f'• <a href="https://t.me/{username}/{mid}">{name}</a>')
            else:
                lines.append(f"• {name}")
        lines.append("")
    lines.append(html.escape(INDEX_FOOTER))
    if ORDER_CONTACTS:
        lines.append("")
        lines.append(f"<b>{html.escape(ORDER_HEADING)}</b>")
        for name, uname in ORDER_CONTACTS:
            lines.append(f'{html.escape(name)} → '
                         f'<a href="https://t.me/{uname}">@{uname}</a>')
    return "\n".join(lines)


# ---------- state ----------

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"items": {}}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------- sync ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print actions and verify channel access; change nothing")
    ap.add_argument("--prune", action="store_true",
                    help="delete posts for teas no longer in teas.md")
    ap.add_argument("--reset", action="store_true",
                    help="delete ALL posts this tool made (index + every tea) "
                         "and clear state, then rebuild from scratch with the "
                         "index post first")
    args = ap.parse_args()

    token, chat = load_env()
    teas = parse_table(TEAS_MD)
    sets = parse_cards_html(SETS_HTML, key_prefix="set-")
    catalogue = teas + sets
    links = load_links()
    state = load_state()
    items = state.setdefault("items", {})
    seen = set()

    chat_info = api(token, "getChat", {"chat_id": chat})
    if args.dry_run:
        if chat_info.get("ok"):
            r = chat_info["result"]
            print(f"channel OK: {r.get('title')} ({r.get('type')})  id={r.get('id')}")
        else:
            print(f"channel access FAILED: {chat_info.get('description')}")
        print(f"parsed {len(teas)} teas from teas.md, "
              f"{len(sets)} sets from sets.html\n")
    else:
        must(chat_info, "getChat")

    username = channel_username(chat)
    if not username:
        print("note: chat_id is not a public @username — index post will list "
              "tea names without links.")

    # --reset: delete everything this tool created, then rebuild below.
    if args.reset:
        targets = [(v["message_id"], v.get("name", k)) for k, v in items.items()]
        if state.get("index"):
            targets.append((state["index"]["message_id"], "INDEX"))
        if args.dry_run:
            print(f"--reset would delete {len(targets)} messages, then rebuild:")
            for mid, name in targets:
                print(f"  delete msg {mid}  ({name})")
            print()
        else:
            for mid, name in targets:
                r = api(token, "deleteMessage",
                        {"chat_id": chat, "message_id": mid})
                ok = "deleted" if r.get("ok") else f"skip ({r.get('description')})"
                print(f"  {ok}: msg {mid} ({name})")
                time.sleep(SLEEP)
            state = {"items": {}}
            items = state["items"]
            save_state(state)
            print("state cleared; rebuilding.\n")

    # Index post is created first so it is the oldest (top) post in the channel.
    # On a fresh channel it goes up as a placeholder, then gets filled with
    # per-tea links once every tea has a message_id (after the loop below).
    if state.get("index") is None and not args.dry_run:
        placeholder = f"<b>{html.escape(INDEX_HEADER)}</b>\n\n…"
        params = {"chat_id": chat, "text": placeholder, "parse_mode": "HTML",
                  "disable_web_page_preview": "true"}
        imk = index_markup()
        if imk:
            params["reply_markup"] = json.dumps(imk)
        res = must(api(token, "sendMessage", params), "sendMessage(index)")
        mid = res["message_id"]
        state["index"] = {"message_id": mid, "hash": "", "pinned": False,
                          "markup": markup_key(imk)}
        if PIN_INDEX:
            pin = api(token, "pinChatMessage",
                      {"chat_id": chat, "message_id": mid,
                       "disable_notification": "true"})
            state["index"]["pinned"] = bool(pin.get("ok"))
            if not pin.get("ok"):
                print(f"  (could not pin index: {pin.get('description')} — "
                      f"grant the bot 'Pin Messages' and rerun)")
        save_state(state)
        print(f"index posted -> message_id={mid}"
              + ("  [pinned]" if state["index"]["pinned"] else ""))
        time.sleep(SLEEP)

    for tea in catalogue:
        key = tea["key"]
        seen.add(key)
        cap = caption(tea)
        digest = content_hash(tea, cap)
        markup = build_markup(tea, links)
        mkey = markup_key(markup)
        photo_path = (os.path.join(PHOTOS_DIR, tea["photo"])
                      if tea["photo"] else None)
        if photo_path and not os.path.exists(photo_path):
            print(f"[{tea['idx']}] WARNING photo missing: {tea['photo']} — "
                  f"skipping")
            continue
        prev = items.get(key)
        n_btns = sum(len(r) for r in markup["inline_keyboard"]) if markup else 0

        if prev is None:
            action = "POST (new)"
        elif prev.get("hash") != digest:
            action = "EDIT content"
        elif prev.get("markup", "") != mkey:
            action = "EDIT buttons"
        else:
            print(f"[{tea['idx']}] {tea['name']}: unchanged")
            continue

        if args.dry_run:
            print(f"[{tea['idx']}] {action}: {tea['name']}  "
                  f"photo={tea['photo']}  buttons={n_btns}")
            print("    " + cap.replace("\n", "\n    "))
            if markup:
                labels = [b["text"] for r in markup["inline_keyboard"] for b in r]
                print("    [buttons] " + " | ".join(labels))
            print()
            continue

        reply_markup = json.dumps(markup) if markup else None

        if prev is None:
            params = {"chat_id": chat, "parse_mode": "HTML"}
            if reply_markup:
                params["reply_markup"] = reply_markup
            if photo_path:
                params["caption"] = cap
                res = must(api(token, "sendPhoto", params, photo_path),
                           "sendPhoto")
            else:
                params["text"] = cap
                res = must(api(token, "sendMessage", params), "sendMessage")
            items[key] = {"message_id": res["message_id"], "hash": digest,
                          "markup": mkey, "has_photo": bool(photo_path),
                          "name": tea["name"]}
            print(f"[{tea['idx']}] posted: {tea['name']} "
                  f"-> message_id={res['message_id']} ({n_btns} buttons)")
        else:
            mid = prev["message_id"]
            had_photo = prev.get("has_photo", False)
            now_photo = bool(photo_path)
            content_changed = prev.get("hash") != digest
            if had_photo != now_photo:
                # media presence changed: delete + repost
                api(token, "deleteMessage", {"chat_id": chat, "message_id": mid})
                params = {"chat_id": chat, "parse_mode": "HTML"}
                if reply_markup:
                    params["reply_markup"] = reply_markup
                if now_photo:
                    params["caption"] = cap
                    res = must(api(token, "sendPhoto", params, photo_path),
                               "sendPhoto")
                else:
                    params["text"] = cap
                    res = must(api(token, "sendMessage", params), "sendMessage")
                prev["message_id"] = res["message_id"]
                print(f"[{tea['idx']}] reposted (media changed): {tea['name']} "
                      f"-> message_id={res['message_id']}")
            elif content_changed and now_photo:
                media = {"type": "photo", "media": "attach://photo",
                         "caption": cap, "parse_mode": "HTML"}
                params = {"chat_id": chat, "message_id": mid,
                          "media": json.dumps(media)}
                if reply_markup:
                    params["reply_markup"] = reply_markup
                must(api(token, "editMessageMedia", params, photo_path),
                     "editMessageMedia")
                print(f"[{tea['idx']}] edited content+buttons: {tea['name']} "
                      f"(msg {mid})")
            elif content_changed:
                params = {"chat_id": chat, "message_id": mid, "text": cap,
                          "parse_mode": "HTML"}
                if reply_markup:
                    params["reply_markup"] = reply_markup
                must(api(token, "editMessageText", params), "editMessageText")
                print(f"[{tea['idx']}] edited content+buttons: {tea['name']} "
                      f"(msg {mid})")
            else:
                # only buttons changed
                params = {"chat_id": chat, "message_id": mid}
                params["reply_markup"] = reply_markup or json.dumps(
                    {"inline_keyboard": []})
                must(api(token, "editMessageReplyMarkup", params),
                     "editMessageReplyMarkup")
                print(f"[{tea['idx']}] edited buttons ({n_btns}): "
                      f"{tea['name']} (msg {mid})")
            prev["hash"] = digest
            prev["markup"] = mkey
            prev["name"] = tea["name"]

        save_state(state)
        time.sleep(SLEEP)

    # stale entries (teas removed/renamed)
    stale = [k for k in items if k not in seen]
    for k in stale:
        entry = items[k]
        if args.prune:
            if not args.dry_run:
                api(token, "deleteMessage",
                    {"chat_id": chat, "message_id": entry["message_id"]})
                del items[k]
                save_state(state)
                time.sleep(SLEEP)
            print(f"pruned: {entry.get('name', k)} "
                  f"(msg {entry['message_id']})")
        else:
            print(f"stale (not in teas.md/sets.html, kept — rerun with --prune "
                  f"to delete): {entry.get('name', k)} (msg {entry['message_id']})")

    # rebuild the index post body now that every tea has a message_id
    idx_text = build_index_text(catalogue, items, username)
    if args.dry_run:
        print("\nINDEX post preview:")
        print("    " + idx_text.replace("\n", "\n    "))
    elif state.get("index"):
        idx_hash = hashlib.sha256(idx_text.encode()).hexdigest()
        imk = index_markup()
        imk_key = markup_key(imk)
        text_changed = state["index"].get("hash") != idx_hash
        markup_changed = state["index"].get("markup", "") != imk_key
        if text_changed:
            params = {"chat_id": chat, "message_id": state["index"]["message_id"],
                      "text": idx_text, "parse_mode": "HTML",
                      "disable_web_page_preview": "true"}
            if imk:
                params["reply_markup"] = json.dumps(imk)
            must(api(token, "editMessageText", params), "editMessageText(index)")
            state["index"]["hash"] = idx_hash
            state["index"]["markup"] = imk_key
            print("index updated.")
        elif markup_changed:
            params = {"chat_id": chat,
                      "message_id": state["index"]["message_id"]}
            if imk:
                params["reply_markup"] = json.dumps(imk)
            must(api(token, "editMessageReplyMarkup", params),
                 "editMessageReplyMarkup(index)")
            state["index"]["markup"] = imk_key
            print("index buttons updated.")
        else:
            print("index unchanged.")

    if not args.dry_run:
        save_state(state)
    print("\ndone." if not args.dry_run else "\ndry run complete.")


if __name__ == "__main__":
    main()
