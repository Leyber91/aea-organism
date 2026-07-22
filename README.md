# THE PROBE · AEA_GAME

A browser game where you fly a probe **inside a real autonomous AI entity** running on this
machine. Every number is live system truth — real model latencies, real rate-limit windows, real
API calls. You compose real AI parts into small machines and **run them for real**.

> **The thesis (one line):** *Wire living proofs of a mind, each more complete than the last, until
> you hold the whole one — and it keeps running after you close the tab.*

---

## START HERE — this repo is built to be handed off

Any conversation can take over development from the repo itself. Read in this order (cheap → deep):

1. **`graph.json`** — the deterministic knowledge-graph (modules, imports, endpoints, design,
   state, web). Query the node you need + its edges instead of re-scanning the tree. Refresh:
   `python aea/build_graph.py`.
2. **`diary/SESSION_LOG.md`** — the latest entry: current state, what's locked, the exact next
   task. Full handoff protocol in `diary/README.md`.
3. **`GAME_PLAN.md`** + `design/` — the design, read on demand.

## RUN IT

```
python controlroom.py          # serves the game + the entity's live endpoints on :7799
```
(That's a thin shim; the server itself lives in `aea/controlroom.py`.)

## REPO LAYOUT (reorganized 2026-07-22, root 126 files → 6)

```
controlroom.py         run shim -> aea/controlroom.py
graph.json             deterministic repo knowledge-graph (read this first; refresh via aea/build_graph.py)
README.md / GAME_PLAN.md
install_autostart.ps1  optional autostart setup

diary/   the dev journal + handoff protocol (SESSION_LOG, REORG_PLAN). How a new conversation takes over.
references/ external reference material a takeover agent needs (AEA + portfolio sources; privacy-guarded).
aea/     ALL the runtime Python — the server + the living entity (one package, flat imports):
           controlroom.py (server), grid.py (metered model grid = the game's energy),
           bench_core.py (THE BENCH: compose real models into a machine and run it),
           aea.py (the entity's heartbeat/tick), agent_tools.py (its hands = real tool-calling),
           brief / hades / autonomy / energy / talk / speak / trust / pulse / ... (organs)
state/   ALL runtime state (grid_state, journey_save, self, heartbeat, memory, ...). Resolved by
           `grid.STATE` (walked up to repo root). Private stores are gitignored, never committed.
web/     the front-end: world.html, tracker.html, game.html, three.js libs, game/. Served via
           `grid.WEB`.
design/  the design book (~40 chapters) + design/concepts/ (47 sheets). Entry: design/INDEX.md.
docs/    AEA research/planning notes + specs (pre-game).
archive/ dead prototype views, scratch scripts, orphaned data — kept, not deleted.
voice/   local TTS/STT tooling (model weights gitignored — downloaded, not source).
```

**How the paths hold together:** `grid.py` defines `ROOT` (found by walking up to `design/`/`.git`),
then `STATE = ROOT/state` and `WEB = ROOT/web`, and `.env` (keys) loads from `ROOT`. So the code
runs correctly from `aea/` while state, web, and keys resolve to the repo root. Verified: server
boots, reads state (incl. the save), writes only into `state/`, and `.env` keys load.

## SOURCE OF TRUTH (on conflict, higher wins)

`SESSION_LOG.md` (current state) > `GAME_PLAN.md` + `design/` (the design) > `state/tickets.json`.

## NEXT

The reorg is done. The real next move is the **merge** — the game currently has the mission loop
(`web/world.html`) and the composition bench (`aea/bench_core.py` + `web/game/`) in two halves;
uniting them, then lighting the first Minimal Viable NPC, is step 0. See `SESSION_LOG.md`.
