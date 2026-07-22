# THE PROBE — SESSION LOG

One entry per work session. **Read the latest entry before starting.** The next session builds
from the `NEXT` block — it does not re-decide what is under `LOCKED`.

---

## 2026-07-22 — vision locked, repo backed up

**DID:** strategic audit (five research passes) → measured verdict: *not a game yet*, but the one
real idea is worth finishing. Vision cohered and locked. Full working tree committed locally
(branch `wip/checkpoint-2026-07-22`, commit `bc825ce`). Clean **game-only** export pushed to
private `github.com/Leyber91/AEA_GAME` (`aeagame_main` → `main`). Career/portfolio data
(`data.js`, `index_codex.py`) excluded by design.

**LOCKED — do not re-litigate:**
- **THESIS (no-AND):** *Wire living proofs of a mind, each more complete than the last, until you
  hold the whole one — and it keeps running after you close the tab.*
- **UNIT = the Minimal Viable Organism:** `BRAIN` (a model) + `SENSES` (an observe tool) + `HANDS`
  (typed action tools — already exist in `agent_tools.py`) + `HEARTBEAT` (the loop — already exists
  in `aea.py`). Wire the four, it comes alive. Legibility = LEGO-Fortnite: each part's form tells
  its job. Claim ceiling holds — the player supplies "it's alive", the game never asserts it.
- **PROGRESSION = increasingly complete AEA combinations; the MASTER = THE AEA.** Each creature is
  a *proof of a combination* (proof = a receipt, it runs; not a claim). Progression-as-understanding.
- **ENDGAME = Phase B:** the finished entity reaches the real internet and acts for you, gated on
  prompt quality. Still deferred until Phase A is actually played.
- **FORM:** the probe stays (it's the vehicle). The city becomes a concentric **instrument**:
  radius = privacy zone · altitude = dependency-DAG depth · node fill = live capacity · edges =
  first-class conduits. NOT open world (short of verbs, not world). NOT landscape.
- **WHY IT'S NOT A GAME YET (measured):** no integration, no variable outcome, no stake the player
  can spend badly, flat verb set (fly / dock / press one button, Act 0 through Act VI).

**STATE:** forked. `world.html` = 6 missions, no bench. `game/` = a working bench, no missions,
empty `data/`. Not merged. Played ~20 min, once (`M0.1`, `M1.1` in `journey_save.json`).

**NEXT — build, ~5 evenings, every step wires what already exists on disk:**
0. **MERGE (step 0, do first).** Port the mission engine from `world.html` into `game/` (keep
   `game/index.html`'s module contract). Delete the dead fork. Then **FIRST LIGHT** = a Minimal
   Viable NPC: a dot with a brain + one sense + one move + a heartbeat that wakes on its own tick,
   moves toward the lit node on real tokens, thoughts printed. That single artifact *is* the thesis.
1. **Energy = stake.** Snapshot the daily quota at boot; charge each call; make `bench_core` emit
   `cost_u = 1` (client already reads it, always renders a dash today).
2. **One decision per DO beat.** Pick a rod — cheap may starve, strong may throttle.
3. **Integration.** Unspent budget carries forward; every call heats the next 60s window.
4. **Losable outcome.** `PASSED / PASSED-DEGRADED / STARVED`, written to `journey_save.json`.
5. **Predict beat.** `A2_TEACHING.md §7`, already specified, unbuilt — commit an answer the live
   system settles before each DO. Cheapest, most load-bearing item; makes the theme mechanically true.
   Then play all six missions twice. Run 2 differs from run 1 → it's a game.

**STOP:** no new design chapters, no new acts, no more concept sheets until an act ships. The
corpus is 12× the game by volume; that ratio is the recorded failure mode, not thoroughness.
