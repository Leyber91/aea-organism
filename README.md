# THE PROBE · AEA_GAME

A browser game where you fly a probe **inside a real autonomous AI entity** running on this
machine. Every number is live system truth — real model latencies, real rate-limit windows, real
API calls. You compose real AI parts into small machines and **run them for real**.

> **The thesis (one line):** *Wire living proofs of a mind, each more complete than the last, until
> you hold the whole one — and it keeps running after you close the tab.*

---

## START HERE

1. **`SESSION_LOG.md`** — the current state and the exact next task. Read the latest entry first;
   it's how each work session hands off to the next.
2. **`GAME_PLAN.md`** — the canonical game plan.
3. This README — the map of every part (below).

---

## THE GAME (`/game`, `/world`)

| path | what it is | status |
|---|---|---|
| `world.html` | the mission build: fly, dock, run mission beats that fire real API calls | LIVE, playable (Acts 0–I) |
| `game/` | the bench build: compose AI parts into a machine and run it (`game/js/bench.js`) | LIVE, works |
| `missions.js` | the 6 authored missions (data) | LIVE |
| `tracker.html` | progress tracker over `tickets.json` | LIVE |

> **Known state: the two builds are forked** — `world.html` has the missions and no bench; `game/`
> has the bench and no missions. Merging them is the next build step (see `SESSION_LOG.md`).

## RUN IT

```
python controlroom.py         # serves the game + the entity's live endpoints on :7799
```

## THE AEA RUNTIME (the living entity the game reads)

- **`controlroom.py`** — the server. Serves the game and the JSON endpoints; imports
  `grid, consolidate, trust, pulse, talk, speak, energy, bench_core`.
- **`bench_core.py`** — THE BENCH: validates a composed machine, fires it on real models, scores it.
- **`grid.py`** — the metered model grid (rate-limit windows, daily quota) — the game's real energy.
- **`aea.py`** — the entity's **heartbeat**: the seeded, looping, self-watched tick.
- **`agent_tools.py`** — the entity's **hands**: real tool-calling (a model chooses a tool, it runs).
- **`brief.py`, `hades.py`, `autonomy.py`, `energy.py`, `talk.py`, `speak.py`, `trust.py`** — organs.

## THE DESIGN (`design/`)

- **`design/`** — the design book (~40 chapters). Entry: `design/INDEX.md`, `design/BOOK.md`.
- **`design/concepts/`** — 47 concept sheets (the visual canon). `SHEET_DEFECTS.md` logs known flaws.
- **`design/E7_VISUAL_COVERAGE.md`** — the image census (42/86 canon drawn).
- **`design/E8_FIDELITY_LAW.md`** — how sheets translate to the engine; the honesty law.
- **`design/bundle_03/`** — the upload set used to generate sheets B10–B16. (`bundle_01/02/20` are
  earlier sets — reference only.)

## SUPPORTING

- **`docs/`** — older AEA research/planning notes (pre-game).
- **`archive/`** — dead prototype HTML views, scratch experiment/test scripts, orphaned data. Kept,
  not deleted, in case anything is needed.
- **`voice/`** — local TTS/STT tooling. Model weights are gitignored (too large; downloaded, not source).
- **`*.json` / `*.jsonl`** at root — live runtime state (grid, saves, fitness, trust). Private ones
  are gitignored and never committed.

---

## SOURCE OF TRUTH (on conflict, higher wins)

`SESSION_LOG.md` (current state) > `GAME_PLAN.md` + `design/` (the design) > `tickets.json` (tickets).

## NEXT REORG (staged — not yet done, because it touches the running server)

The safe declutter is done (dead prototypes + experiments archived, notes moved to `docs/`). The
deeper move — grouping the runtime `.py` into an `entity/` package, relocating state `.json` into a
`state/` dir, vendoring the three.js libs, trimming dead server routes — changes imports and paths
and **must be done with a server-start + game-load test after each step**, not blind. It's the next
housekeeping task; it is not urgent, and it must never block the merge.
