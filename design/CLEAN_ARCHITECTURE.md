# CLEAN ARCHITECTURE — THE PROBE (the rebuild blueprint, 2026-07-22)

Companion to `design/FIELD_GUIDE.html` (the vision). This is the structure that builds the game the
guide describes. Supersedes the legacy `E1_CODE_ARCHITECTURE.md` where they conflict.

## Principle: THREE RINGS — truth flows outward only
1. **SUBSTRATE — `aea/` (PRESERVED, untouched).** The real always-on entity; the ONLY place a real token
   burns or a real number is measured. `grid` (meter/energy/paths), `energy`, `bench_core` (the ONE
   execution engine — never duplicated), `aea` (heartbeat/tick), `agent_tools` (HANDS), `autonomy` (the
   battery), `hades` (watcher), `trust`, `pulse`, `memory` + organs.
2. **SEAM — `aea/gameapi.py` (NEW).** The ONE curated read/act facade at `/game/*`. Where the honesty law +
   claim ceiling + allowlist + trust-gate live **structurally**: absent -> `null` -> a dash; refusal ->
   `{ok:false, refused:'<clause>'}`. Collapses the ~14 legacy routes to ~8 game endpoints.
3. **CLIENT — `web/probe.html` + `web/game/js/` (REBUILT clean).** Presentation + play only; owns ZERO
   truth; reads `window.GAME.state`, renders, sends acts back through the seam. Single global `window.GAME`
   (state + bus + onFrame); every module `init(GAME)`/`dispose()`; no build step; three.js r128.

## Endpoints (the contract)
- **READ** (GET, pure): `/game/state` (one folded snapshot) · `/game/events?since=` · `/game/catalogue`
  (the pokedex truth) · `/game/schema` (the fog map).
- **ACT** (POST, allowlisted + metered + trust-gated, receipts not exceptions): `/game/ignite {spec}` ->
  `run_id` · `/game/run?id=` (poll live trace) · `/game/fire {node,plant,zone}` · `/game/act {cmd}`
  (brief|consolidate|tick|play|stop) · `/game/talk` · `/game/save` (the sacred journey merge).

## Preserve / Rebuild / Delete
- **PRESERVE:** all of `aea/` + the curated read/act LOGIC (re-homed into `gameapi.py`, not rewritten);
  all of `state/` (esp. `journey_save.json` = sacred); the E1-compliant `web/game/js` modules
  (engine/bench/panels/seals/artifacts/boot) — extend, never rebuild; `aea_elements.js`;
  design/docs/diary/references; `archive/` (museum, routes cut).
- **REBUILD CLEAN:** `web/world.html` (HARVEST its live-wiring / mission-engine / OS / HUD / WebAudio into
  modules, THEN retire) · `web/missions.js` -> `data/missions.json` (script -> data) · `web/game/index.html`
  -> `web/probe.html` (THE one client entry) · `controlroom.py` routing (collapse the ~28-branch ladder ->
  a static server + the `gameapi` mount).
- **DELETE:** the already-broken legacy view routes (`/brain /city /plan /builder /mind /tree /poster
  /workspace /room`) — they serve `"<file>.html missing"` TODAY after the reorg; `web/game.html` + `/game`
  (legacy board); the duplicate `web/game/vendor/` (two-copy hazard); dev fixtures off the game path
  (lab/holo/samples/tracker -> `dev/`).

## Client modules (grouped by concern)
`core/api.js` (the ONLY server-talker) · `world/{engine,artifacts,seals}.js` · `compose/bench.js` (the
composer) · `catalogue/pokedex.js` (shadows + real stats) · `hud/{hud,os,panels}.js` · `missions/runner.js`
(replays `data/missions.json`; scaffolding that thins) · `audio/audio.js` (cues on real events only).

## Modes (R36) = client presets over the same seam
GUIDED (premade creatures) · BUILDER (compose from parts) · ARCHITECT (edit the code). ONE engine, a depth
dial — not three products. Orthogonal axis: **SANDBOX <-> LIVE** (the stakes/permission gate; LIVE = the
entity acts on the real internet, R26). Crystallization (R38) is the on-ramp BUILDER -> ARCHITECT.

## World (R37) = a living concentric instrument, data-driven
The map is the fog view of `/game/schema` (always true, grows with the entity). radius = privacy zone ·
altitude = DAG depth · fill = live capacity · edges = conduits. Openness is EARNED (metroidvania): districts
open as real organs are built; you fully roam what you've built; the fogged frontier is the pokedex-shadow
of territory. Your composed creatures populate it (emergent, R28). NOT open-world (can't honestly roam what
isn't real).

## FIRST LIGHT — the shortest slice (6 files; ship before any other module)
`boot.js` (done) + `world/engine.js` (void + flight, exists) + `core/api.js` (NEW ~40 lines: GET
`/game/state` render + POST `/game/ignite` + poll `/game/run` — this proves the honesty pipe is LIVE, which
v2 does NOT yet do) + `compose/bench.js` (exists; open with the 4 MVO slots BRAIN/SENSES/HANDS/HEARTBEAT) +
`hud/hud.js` (render the ignite result + one honesty tag) + `missions/runner.js` (replay M0.1 as the frame).
Path: pick a real BRAIN + SENSES + HANDS + HEARTBEAT -> POST `/game/ignite` -> `gameapi` wraps
`bench_core.start_run` (NO new execution engine) -> the dot wakes on its OWN tick, draws a real token, prints
its thought; OR it visibly fails (STARVED / refused) in diagnostic blue, and that failure is the teaching.
That one artifact IS first light. Everything else is strictly additive after it reads true on a screenshot.
