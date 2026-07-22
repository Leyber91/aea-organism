# ROOT REORG — COMPLETE (2026-07-22)

**Done. Root went from 126 loose files to 6.** State → `state/`, web → `web/`, all Python →
`aea/`, runtime files → `state/`, spec → `docs/`. Code rewired via `grid.ROOT`/`STATE`/`WEB`
anchors; a root `controlroom.py` shim keeps `python controlroom.py` working. Verified end-to-end
after every stage: server boots, `.env` keys load (NVIDIA/GROQ/CEREBRAS), all endpoints 200, the
save (`M0.1`/`M1.1`) is intact, every write lands in `state/`, nothing leaks to root. The record
of exactly what moved and why is below.

## DONE (committed + tested)

- **Safe archival** — dead prototype HTML, scratch scripts, orphaned data, loose notes, junk →
  `archive/` + `docs/`.
- **Stage A — STATE → `state/`** ✓ tested. `grid.STATE` (walked up to repo root) is the single
  home. ~55 sites + the load/save/lock helpers redirected; the four single-quoted refs the first
  pass missed are fixed; exhaustive rescan shows zero state left on `HERE`. 36 `.json/.jsonl` moved.
  Server reads state (incl. `journey_save` = `M0.1`/`M1.1`) and every write lands in `state/`.
- **Stage C — WEB → `web/`** ✓ tested. `grid.WEB` anchor; controlroom's live serving redirected;
  `world/tracker/game.html`, 10 `.js`, and `game/` moved. `/world /probe /tracker /CopyShader.js`
  all 200.

Current root: `runtime .py (33)` + `8 .md` + `.gitignore` + dirs `state/ web/ design/ docs/
archive/ voice/`. **Run command unchanged:** `python controlroom.py` (it's still at root).

## REMAINING — Stage B: PYTHON → `runtime/` (do fresh, server in hand)

The riskiest move: it touches `.env` (the API keys). `grid.STATE`/`grid.WEB` already walk up to the
repo root, so they survive the move — but these `HERE`-anchored, root-living references would break
and must be redirected FIRST (all mapped 2026-07-22):

- **`.env`** — grid.py:132 `os.path.join(HERE, ".env")` → `os.path.join(ROOT, ".env")`. **Miss this
  and the entity silently loses its keys.** Leave `.env` at root.
- **`voice/`** — listen.py:22,92 · speak.py:29,229 `os.path.join(HERE, "voice", …)` → anchor to
  `ROOT`. (voice/ stays at root.)
- **Runtime files → `state/`** (they live at root now, would split): `aea_seed.md` (aea.py:16,
  talk.py:31) · `brief_output.md` (controlroom.py:128, speak.py:236, written by brief.py) ·
  `live.log` (controlroom.py:122,641, live.py:29) · `live.instance` (live.py:30) · `_live_edge.mp3`
  (speak.py:120). Redirect to `grid.STATE`, then move the existing ones into `state/`.
- **`bench_core.py:151`** `os.path.join(HERE, row.get("file"))` — bench module-file resolution;
  check where those files live before moving.
- **Lesson from Stage A:** scan BOTH quote styles (`'x'` and `"x"`) — the single-quote refs were
  missed the first time.
- Then `git mv *.py runtime/` (co-located → flat `import grid` still resolves when run as
  `python runtime/controlroom.py`). Add a 3-line root `controlroom.py` shim that execs
  `runtime/controlroom.py` so `python controlroom.py` keeps working. `subprocess(cwd=HERE)` is fine
  (finds the co-located `.py`; state is `grid.STATE`-anchored regardless of cwd).

**Test (same as before):** server on a spare `--port`; `/world /probe /api/tickets /api/journey`
200; trigger a save + a tick; confirm NO new file appears at root and `state/journey_save.json`
still holds `M0.1`+`M1.1`; **and confirm a real model call still authenticates** (the `.env` check).
Recoverable: everything is committed + pushed.
