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
       TELEGRAM_CHAT_ID=@hoiantea

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
import urllib.error
import urllib.parse
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
TEAS_MD = os.path.join(HERE, "teas.md")
PHOTOS_DIR = os.path.join(HERE, "photos")
STATE_FILE = os.path.join(HERE, "telegram_state.json")
ENV_FILE = os.path.join(HERE, ".env")
API = "https://api.telegram.org/bot{token}/{method}"
SLEEP = 0.5  # seconds between write operations (rate limit headroom)


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


# ---------- teas.md parsing ----------

def parse_teas():
    teas = []
    with open(TEAS_MD, encoding="utf-8") as fh:
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
            teas.append({
                "idx": idx,
                "name": name,
                "desc": desc,
                "tags": [t.strip() for t in tags.split("|") if t.strip()],
                "photo": photo or None,
                "price": [p.strip() for p in price.split("/") if p.strip()],
            })
    return teas


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def caption(tea):
    lines = [f"<b>{html.escape(tea['name'])}</b>"]
    if tea["tags"]:
        tagtxt = " · ".join(html.escape(t.lstrip("*").strip()) for t in tea["tags"])
        lines.append(f"<i>{tagtxt}</i>")
    if tea["desc"]:
        lines += ["", html.escape(tea["desc"])]
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
    args = ap.parse_args()

    token, chat = load_env()
    teas = parse_teas()
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
        print(f"parsed {len(teas)} teas from teas.md\n")
    else:
        must(chat_info, "getChat")

    for tea in teas:
        key = slug(tea["name"])
        seen.add(key)
        cap = caption(tea)
        digest = content_hash(tea, cap)
        photo_path = (os.path.join(PHOTOS_DIR, tea["photo"])
                      if tea["photo"] else None)
        if photo_path and not os.path.exists(photo_path):
            print(f"[{tea['idx']}] WARNING photo missing: {tea['photo']} — "
                  f"skipping")
            continue
        prev = items.get(key)

        if prev is None:
            action = "POST (new)"
        elif prev.get("hash") != digest:
            action = "EDIT (changed)"
        else:
            print(f"[{tea['idx']}] {tea['name']}: unchanged")
            continue

        if args.dry_run:
            print(f"[{tea['idx']}] {action}: {tea['name']}  "
                  f"photo={tea['photo']}")
            print("    " + cap.replace("\n", "\n    "))
            print()
            continue

        if prev is None:
            if photo_path:
                res = must(api(token, "sendPhoto",
                               {"chat_id": chat, "caption": cap,
                                "parse_mode": "HTML"}, photo_path), "sendPhoto")
            else:
                res = must(api(token, "sendMessage",
                               {"chat_id": chat, "text": cap,
                                "parse_mode": "HTML"}), "sendMessage")
            items[key] = {"message_id": res["message_id"], "hash": digest,
                          "has_photo": bool(photo_path), "name": tea["name"]}
            print(f"[{tea['idx']}] posted: {tea['name']} "
                  f"-> message_id={res['message_id']}")
        else:
            mid = prev["message_id"]
            had_photo = prev.get("has_photo", False)
            now_photo = bool(photo_path)
            if had_photo != now_photo:
                # media presence changed: delete + repost
                api(token, "deleteMessage", {"chat_id": chat, "message_id": mid})
                if now_photo:
                    res = must(api(token, "sendPhoto",
                                   {"chat_id": chat, "caption": cap,
                                    "parse_mode": "HTML"}, photo_path), "sendPhoto")
                else:
                    res = must(api(token, "sendMessage",
                                   {"chat_id": chat, "text": cap,
                                    "parse_mode": "HTML"}), "sendMessage")
                prev["message_id"] = res["message_id"]
                print(f"[{tea['idx']}] reposted (media changed): {tea['name']} "
                      f"-> message_id={res['message_id']}")
            elif now_photo:
                media = {"type": "photo", "media": "attach://photo",
                         "caption": cap, "parse_mode": "HTML"}
                must(api(token, "editMessageMedia",
                         {"chat_id": chat, "message_id": mid,
                          "media": json.dumps(media)}, photo_path),
                     "editMessageMedia")
                print(f"[{tea['idx']}] edited: {tea['name']} (msg {mid})")
            else:
                must(api(token, "editMessageText",
                         {"chat_id": chat, "message_id": mid, "text": cap,
                          "parse_mode": "HTML"}), "editMessageText")
                print(f"[{tea['idx']}] edited: {tea['name']} (msg {mid})")
            prev["hash"] = digest
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
            print(f"stale (not in teas.md, kept — rerun with --prune to delete): "
                  f"{entry.get('name', k)} (msg {entry['message_id']})")

    if not args.dry_run:
        save_state(state)
    print("\ndone." if not args.dry_run else "\ndry run complete.")


if __name__ == "__main__":
    main()
