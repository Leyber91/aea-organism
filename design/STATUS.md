DONE means it ran and was seen; nothing here is claimed.

---

# STATUS — THE PROBE

> a probe flies inside a real running entity and composes real AI parts into machines that actually fire. every value on this board is live truth or a dash. a row is DONE only when it RAN and was SEEN — a 200, a screenshot. everything else is PENDING or FOG. authored by the studio PRODUCTION dept at the 2026-07-24 standup; reconciled to verified reality by the builder. canonical state stays in `diary/SESSION_LOG.md`.

---

## 1 · VERIFIED-DONE (it ran, it was seen — do not rebuild)

the substrate is FROZEN. these already fire on real endpoints.

| row | proof | state |
|---|---|---|
| THE MERGE — fly, dock (F at core), seat parts, fire (Space) as ONE program | `web/game/` runs as a single loop | DONE |
| THE COMPOSER — real constructs, COMPOSED 0 to 1 | both plants seated + fired | DONE |
| free hearth (ollama) fires | run returns PASS, cost_u = 0 (FREE) | DONE |
| paid plant (nvidia) fires | run returns PASS, cost_u = 1u (real metered) | DONE |
| bench.js owns dock + compose + run | POST /game/ignite to run_id to poll GET /game/run, settles at finishPass() / haltAt() | DONE |
| boot.js births window.GAME | `{ state, bus:{on/off/emit}, onFrame/offFrame/frame }` — the bus is the only sanctioned cross-module channel | DONE |
| the real seam endpoints | POST /game/ignite, GET /game/run, /game/state, /game/schema, /game/events — honesty-firewalled | DONE |
| run:done emitted | bench.js finishPass() AND haltAt() — 7-field frozen payload | DONE |

**run:done payload — FROZEN, 7 fields, consume as-is:**
`{run_id:string|null, seq:int, pass:true|false|null, scored:bool, cost_u:number|null, total_ms:number|null, halted:bool}`
clean PASS => `{pass:true, halted:false}` · located fail => `{pass:false, halted:true}` · DRAW-only DONE => `{pass:null, scored:false, halted:false}`.

---

## 2 · STAGE 1 — THE MISSION ENGINE · VERIFIED DONE (it ran end-to-end, it was seen — 2026-07-24)

the vertical slice: THE PROBE is now a GUIDED GAME, not a bench that fires. cold-open to fly to dock to seat to fire to PROVE on a real receipt to reveal — driven by mission DATA, gated on real events. **proof of record: headless run `r-09` — brief to learn to DO armed to a real free-hearth draw (`pass:true, cost_u:0, total_ms:786.5ms`) to PROVE re-read `GET /game/run?id=r-09` (HTTP 200, `pass=True`, tap+scorer receipts truthy) to `MISSION COMPLETE`, localStorage `probe.mission.M0.1=done`, zero console errors, screenshot read (`scratchpad/mission.png`).**

| task | scope | proof | state |
|---|---|---|---|
| bench: `run:refused` emit at the no-run_id branches | ignite ok:false + ignite HTTP-error + carrierLost() emit `run:refused {reason}` — distinct event, no run minted. the only bench edit stage 1 required. | in `web/game/js/bench.js`; DO card resolves, never hangs | DONE |
| `web/game/js/mission.js` — the data-driven runner | the ONE new file under web/game/js. four handlers (brief/learn/do/prove). no framework. reads ONLY GAME.bus + /game/*. | ported; drives m01 end-to-end | DONE |
| M01 "FIRST LIGHT" — the DATA | `web/game/data/missions/m01_first_light.json`: brief to learn to do to prove + reveal. LEYBER lines live ONLY as data; the engine authors no strings. | renders the real protocol; reveal ceiling-clean | DONE |
| the content layer serves | `.json` added to the static allowlist (`controlroom.py _CTYPES`) so `game/data/*` missions serve (was soft-404). | `/game/data/missions/m01_first_light.json` → 200 real body | DONE |
| boot wiring — DO arm + hands-off card | mission.js loaded after BENCH; `MISSION.init(GAME)`. DO subscribes run:done + run:refused, arm-gated, stores rid, acts. | wired in `index.html`; card closes, keys reach the bench | DONE |
| CDP headless verify — SEEN, not claimed | the real run_id legible in the reveal; tap+scorer receipts; first amber on the real draw; the literal glyphs FREE. | `scratchpad/mission.png` read; `/game/run?id=r-09` 200 | DONE |

**the STAGE-1 spine (locked, held through the build):**
- the DO beat does NOT fire a canned ignite — it OBSERVES the player's REAL bench fire. the player composes for real.
- **two-tier DO gate (VERIFIED):** (a) the DO WAIT resolves on ANY terminal event for this arm — run:done pass true/false/null OR run:refused — so the card always gives feedback and never hangs. (b) the mission ADVANCES to PROVE ONLY on `run:done pass===true`. located fail, unscored, and refusal keep the objective card up with a re-seat/re-fire nudge — they never advance, never fabricate a PASS.
- **PROVE is HTTP-truth, not event-truth (VERIFIED):** re-reads `GET /game/run?id=<stored rid>` and asserts the LIVE body. PASS = 200 AND body.ok AND pass (top-level `r.pass` / `r.run_ok` / scorer `receipt.pass`; the real body carries NO `verdict` object) AND links non-empty AND `part==='tap'` receipt truthy AND `part==='scorer'` receipt truthy AND state settled. receipt is an OBJECT — asserted PRESENT+truthy, never "a non-empty string".
- **part ids FROZEN:** THE DRAW = `tap` (head), THE MEASURE = `scorer` (tail). `carrier` is a halt label, not a seated part.
- **cost_u TRI-STATE LAW (VERIFIED):** 0 renders FREE, positive renders Nu, null renders a dash. M01 fires the FREE hearth — PROVE + reveal render `FREE`, never `0`.
- **keyboard single-owner (VERIFIED):** brief/learn/prove = terminal MODAL (mission owns input); do = terminal collapses (`display:none`, `pointer-events:none`), flight + bench own Space/F.
- **temporal-honesty:** prove.pass/fail + reveal.tag are TEMPLATES against the real re-read; absent fields render a dash; no event-claim line renders before its receipt exists.
- **claim-ceiling on every line (VERIFIED):** the reveal reads "something answered. it was listening the whole time. the socket is real." — never conscious/sentient/alive; the player supplies the conclusion.
- **first-amber wow is the BENCH's:** the real draw fires the core amber; the overlay paints amber ONLY on the earned PASS chip + the `mission complete` tag — void + grey everywhere else.

**PROVE FAIL rewinds to DO** (world.html behavior kept, VERIFIED on the first run where the assert read the wrong field): an honest real fail loops the player back to re-seat and re-fire. the mission never fabricates a PASS.

---

## 3 · THE TALKING TEAM (standup held 2026-07-24, wf_9d73037c)

the departments that argued STAGE 1 into a locked contract, then authored the DATA + the honesty-lint + this board. the standup is recorded (transcript in the workflow output); the seams below were resolved in the room, not left open. the team's read that the merge was "unbuilt" was stale — SUBSTRATE corrected it live: run:done already shipped.

| department | held the line on |
|---|---|
| SUBSTRATE / STUDIO HEAD | run:done already emits at both terminal branches — consume it, do not rebuild. the 7-field shape (incl. `halted`) is frozen. |
| SYSTEMS / LOGIC | mission.js is a data-driven runner, not a framework; one new file; one-way dependency on GAME.bus + /game/*. |
| UX / MENUS | the two-tier DO gate — feedback on any terminal event, advance only on real pass. keyboard single-owner during DO. |
| MISSION DESIGN | the exact beat list; PROVE gates on tap+scorer part ids; the located re-fire nudges (earned/reseat/halted). |
| NARRATIVE | temporal-honesty + claim-ceiling: LEYBER lines are DATA only; no line asserts an event before its receipt; the reveal never states the conclusion. |
| QA / VERIFY | the headless proof must SEE the real run_id, both receipt lines, first amber on the draw, the literal FREE — a green check does not satisfy it. caught the weak runAssert. |

**resolved seams:** haltAt-must-emit (already met) · run:refused for the two silent branches (built) · pass-vs-scored-vs-advance (two-tier gate) · receipt-is-dict-not-string (assert truthy) · pass-lives-top-level-not-in-a-verdict-object (caught in verify) · cost tri-state (FREE / Nu / dash).

**QA sign-off gate — all CONFIRMED on the live run `r-09`:**
- reveal carries the real run_id the endpoint answered 200 for; the PROVE line reads `run r-09 - 787ms - cost FREE`. CONFIRMED.
- out-of-band `GET /game/run?id=r-09` → 200, `ok=True`, `pass=True`, links non-empty, tap receipt truthy, scorer `receipt.pass=True`. CONFIRMED.
- first amber ignites on the real draw (the core burns); the overlay is void+grey except the earned PASS chip + `mission complete`. CONFIRMED (screenshot).
- the literal glyphs `FREE` render for cost (bench log `COST FREE`, PROVE line `cost FREE`). CONFIRMED.
- DO → PROVE advanced only after the fire, only on `pass===true`; no advance on null/false/refused. CONFIRMED.
- completeMission: `#mhud .m-tag` = "mission complete", reveal "first light - the socket answers", localStorage `probe.mission.M0.1=done`, bus `mission:done`. CONFIRMED.
- hands-off card: terminal not `.open` during DO, keys reached the bench (seat + fire took effect). CONFIRMED.
- SUBSTRATE UNTOUCHED: only new web/game/js file is mission.js; bench.js changed only by the emits; no console errors, no painted `#err`. CONFIRMED.

---

## 4 · FOG — deferred behind the sequencing gate (not started, not scoped)

do not pull these into the present. the income clock and completion-over-planning both say: the slice ships first, then each next layer is earned.

| behind the gate | why it waits |
|---|---|
| RUNG 2 · RECALL forge + the earned-title ceremony (REF-09) | the next guided rung; a real Claude+Luis dev session, only after the first loop is felt in Luis's hands. |
| the journey/evolution map + the codex (Phase C) | built FROM the reveal ledger + the sacred save, NOT new reference generations. |
| BUILDER / ARCHITECT progression roles · rungs 3-7 | STAGE 1 fires ONLY THE DRAW + THE MEASURE; the middle three parts + the role ladder open in later missions. |
| antagonist ecology (starvation · runaway · the wall) | no antagonist until the honest core loop is proven; a threat with nothing to threaten is forbidden. |
| the server-side sacred save + reveal ledger | M01 persists completion to localStorage only; the `journey_save.json` write + fog-lift is a later stage (named, not built). |
| paid-plant mission content | the paid nvidia plant fires (verified), but M01 stays on the FREE hearth; cost-bearing missions are FOG. |
| second + third REVEALS | each reveal is a completeMission reward; only `plant_local` (first light) is in STAGE 1. |

---

_the next real move lives in `diary/SESSION_LOG.md` NEXT. this board reflects it; it does not replace it._
