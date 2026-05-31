# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-page static site for **Roman&Julia teas** (brand "Roman&Julia teas", Telegram-only ordering, no buy flow) plus a tool that mirrors the same catalogue into the Telegram channel **@chariteas**. No build step, no framework — plain HTML/CSS and one zero-dependency Python script.

The repo is also the **GitHub Pages source**: pushing to `main` republishes the live site at https://chari.life/ (remote `d333mianh/hoiantea`). Treat the repo as **public** — secrets live only in `.env` (gitignored).

Pushing to `main` also **auto-syncs the Telegram channel**: `.github/workflows/telegram-sync.yml` runs `sync_telegram.py` whenever `teas.md`, `sets.md`, `links.json`, `photos/`, or the script change (uses repo secrets `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`). So in practice "apply teas.md" = edit `index.html` + `teas.md`, commit, push — the channel updates itself. Running the script locally is now optional (useful for `--dry-run`, `--prune`, or `--reset`, which the Action never does).

## The central idea: `teas.md` is the single source of truth

`teas.md` is a Markdown table the owner hand-edits. It feeds **two** outputs that must be kept in sync with it:

1. **`index.html`** — synced *manually* (there is no HTML generator). When `teas.md` changes, regenerate the `.tea` rows in `index.html` by hand to match. Each row maps directly to a table column (see below).
2. **The Telegram channel** — synced *programmatically* by `sync_telegram.py`, which parses `teas.md` at runtime.

So a typical "apply teas.md" request means: edit `index.html`'s tea rows to match, then (if asked) run the Telegram sync.

**Drink sets** work the same way via a parallel source, `sets.md` (same column format). It feeds `sets.html` (manual mirror) and the Telegram channel — `sync_telegram.py` calls `parse_table()` on both files and posts sets with `set-`-prefixed state keys (so they never collide with teas), grouped under a "DRINK SETS" heading in the index. There's also a static `ceremony.html` page (no markdown source). The three site pages are linked from the upper-left nav (`index.html` = Catalogue, `sets.html` = Drink Set, `ceremony.html` = Ceremony).

### `teas.md` column → output mapping

| Column | `index.html` | Telegram caption |
|--------|-------------|------------------|
| № | `<div class="tea-idx">№ NN</div>` (sequential, in physical row order) | order only |
| Name | `<h3 class="tea-name">` | `<b>` line |
| Description | `<p class="tea-sub">` | body line |
| Tags | `<span class="tea-tag">` (prefix `*` → `tea-tag-accent`, the clay-red pill) | `<i>` line, ` · `-joined |
| Photo | `<img class="tea-photo" src="photos/X">`; **blank → kanji placeholder** `<div class="tea-photo">KANJI<span class="tea-photo-label">photo</span></div>` | uploaded photo |
| Price | `100g · Yk ₫` segments split on ` / `, joined with `<br>` | same, newline-joined |

Gotchas:
- The **№ column is display position only** — when rows are reordered in `teas.md`, renumber them 01..N in their new physical order ("normalize").
- Every `Photo` filename must exist in `photos/`. After bulk edits, verify: `grep -o 'photos/[^"]*\.jpeg' index.html | sed 's|photos/||' | while read f; do [ -f "photos/$f" ] || echo "MISSING $f"; done`
- The page is fixed-width desktop: `<meta name="viewport" content="width=1280">`, `#root { width: 1280px }`. Photos are 260×260 circular (`border-radius: 50%`, `object-fit: cover`). Colors are `oklch()`. Fonts: Shippori Mincho (serif), Inter (sans), JetBrains Mono (mono) via Google Fonts.

## Common commands

```sh
# Preview the site — no build, just open the file
open index.html

# Compress a photo before committing (originals are multi-MB; keep ~250KB)
sips -Z 800 -s formatOptions 80 photos/NAME.jpeg

# Publish: GitHub Pages rebuilds (~1 min) on push to main; the Telegram-sync
# Action also fires if teas.md/links.json/photos/sync_telegram.py changed
git add -A && git commit -m "..." && git push

# Telegram: preview every action + verify the bot can see the channel
python3 sync_telegram.py --dry-run
# Telegram: post new teas / edit changed ones / add buttons in place
python3 sync_telegram.py
# Telegram: also delete posts for teas removed from teas.md
python3 sync_telegram.py --prune
# Telegram: nuke ALL posts (index + teas) and rebuild from scratch, index first
python3 sync_telegram.py --reset --dry-run   # preview the deletions first
python3 sync_telegram.py --reset
```

Always run `--dry-run` before a real Telegram sync.

## `sync_telegram.py` — how the channel mirror works

Zero dependencies (stdlib `urllib`/`json`/`hashlib` only). Posts via the Telegram **Bot API**; the bot is a channel admin acting as a silent posting key (not a chatbot). Requires `.env` with `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (see `.env.example`).

- **State**: `telegram_state.json` (gitignored, machine-local) maps each tea's **slug** (`slug(name)` = lowercased, non-alphanumerics → `-`) to its `message_id`, a content `hash`, and a `markup` key, plus a top-level `index` entry for the index post (`message_id`, `hash`, `pinned`). This map is what lets reruns *edit existing posts* instead of re-posting.
- **Per-tea decision** each run: new tea → `sendPhoto`; content hash changed → `editMessageMedia`/`editMessageText`; only buttons changed → `editMessageReplyMarkup`; unchanged → skip. Teas in state but absent from `teas.md` are reported, and deleted only with `--prune`.
- **Buttons** (inline URL keyboard, 2-per-row): a global **website** button (`WEBSITE_URL` constant at top of the script) is added to every post, plus optional per-tea buttons from `links.json`, keyed by slug: `{ "gaba-ruby": [{"text": "огляд", "url": "https://..."}] }`.
- **Index post**: a single catalogue post kept **first** in the channel (and pinned, `PIN_INDEX`). Teas are grouped under their category heading (first tag, in `teas.md` order); each name is an HTML deep-link `https://t.me/<username>/<message_id>` to that tea's own post (requires a public `@username` chat_id). On a fresh channel it is posted *before* the teas as a placeholder, then edited to fill in the links once every tea has a `message_id`; later runs re-edit it whenever the catalogue or any linked id changes. Header/footer text: `INDEX_HEADER` / `INDEX_FOOTER`.
- **`--reset`**: deletes every message this tool made (index + all teas) and clears state, then rebuilds from scratch so the index lands first. The *only* way to reorder existing posts or move the index to the top (see constraint below). Always `--dry-run` it first.

### Telegram constraints that shape the design (don't fight these)
- A bot can only edit/delete **its own** messages. Posts made by other bots (e.g. @ControllerBot) are untouchable here.
- **Channel post order is fixed at post time.** Reordering teas in `teas.md` does *not* reorder existing channel posts; new teas append at the bottom.
- **Renaming a tea changes its slug** → treated as a new post (old one becomes a `--prune` candidate). Editing description/price/photo of a same-named tea edits in place.

## Files

- `index.html` (Catalogue) / `sets.html` (Drink Set) / `ceremony.html` (Ceremony) / `styles.css` — the site pages + external stylesheet, linked from the upper-left nav.
- `teas.md` — source-of-truth tea catalogue table (also the owner's editing surface).
- `sets.md` — source-of-truth drink-sets table (same format); feeds `sets.html` + Telegram.
- `sync_telegram.py` — Telegram channel sync (teas + sets); `.env.example` documents required vars.
- `links.json` — per-tea Telegram button links (keyed by slug).
- `photos/` — compressed catalogue images referenced by `teas.md`/`index.html`.
- `.github/workflows/telegram-sync.yml` — CI that auto-runs the Telegram sync on push to `main` and commits the updated state back.
- `telegram_state.json` — Telegram sync state (slug→message_id/hash + index post). **Tracked** (not gitignored) so CI keeps state across runs; holds no secrets.
- Gitignored: `.env` (secrets) only.
