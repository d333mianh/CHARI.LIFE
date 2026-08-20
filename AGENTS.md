# AGENTS.md

See `CLAUDE.md` for the full project overview (source-of-truth model, `teas.md` → `index.html`/Telegram mapping, and the `sync_telegram.py` design). This file only adds Cloud-specific notes.

## Cursor Cloud specific instructions

- This repo is a **zero-build static site** plus one **stdlib-only** Python script (`sync_telegram.py`). There are no package manifests (`package.json`, `requirements.txt`, etc.) and nothing to install — Python 3 is the only requirement and is preinstalled. The startup update script is a no-op by design.
- **Serve the site (dev):** `python3 -m http.server 8000` from the repo root, then open `http://localhost:8000/index.html`. Pages: `index.html` (Catalogue), `sets.html` (Drink Set), `ceremony.html` (Ceremony), and `tea-research.html` (internal research tool). There is no framework, bundler, or hot-reload — just re-serve/refresh the browser after edits.
- **No test suite and no configured linter exist.** For a quick sanity check of the one code file, use `python3 -m py_compile sync_telegram.py`. Its offline parsers can be exercised without secrets, e.g. `python3 -c "import sync_telegram as s; print(len(s.parse_table(s.TEAS_MD)))"`.
- **`sync_telegram.py` is an OPTIONAL owner tool, not needed to develop the site.** Even `--dry-run` calls the live Telegram API (`getChat`) and therefore requires real `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (see `.env.example`) plus network access. Without those secrets it exits immediately with a "Missing TELEGRAM_..." message — this is expected, not a broken environment. Do not run a real (non-dry-run) sync against the live `@chariteas` channel unless explicitly asked.
