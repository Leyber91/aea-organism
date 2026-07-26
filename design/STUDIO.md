# THE PROBE — THE STUDIO (operating model + staged plan)

*Founded from real post-mortems (studio-founding panel wf wytihe88r). This is a REFERENCE. The critic's
verdict is the law: "a 7-department studio around a core that has never run one mission is the 110:1 pattern
relabeled as agents — delete everything except stage 1 and execute it." So: the operating model + guardrails
below stand; the staged plan runs ONE stage at a time, gated by "it played."*

## THE OPERATING MODEL

Tiny studio: **Luis** (creative director + sole go/no-go pilot) · **Claude** (studio head) · **AI agents**
(extra hands that author DATA, never decisions). Cadence: **one focused push → one real artifact → verified
before the next starts.** No parallel departments until the slice plays. **Definition of done is single and
hard: it RAN** — a headless-Chrome screenshot READ and/or a real endpoint 200 — then Luis pilots it and the
boring test gates shipping. A description of an artifact is not an artifact; compiles-in-my-head is not done.

## THE GUARDRAILS (the failures, as hard rules — obey them)

1. **No new design corpus before the slice PLAYS** (110:1 is the recorded failure; writing more IS the
   avoidance). The 12 refs are locked — build-to-match, never a new forge batch.
2. **No parallel agent departments before the slice plays** (38 Studios: org-before-product). Agent-hours are
   burn rate too.
3. **Freeze the working substrate** (Duke Nukem law): no composer rewrite, no render-stack swap, no
   "refactor the seam first." New capability = the mission engine, never a better foundation.
4. **Every new system must be justified by the slice** (Star Citizen). If it doesn't help one mission run
   start-to-receipt, defer it.
5. **Loop fires before it's pretty** (Vampire Survivors): string the beats into a playable loop BEFORE
   refining the bench to REF-10. Polishing the plate first is avoidance — name what it costs.
6. **Honesty is architecture, not a coat** (Aliens:CM fake-demo): DO calls real `/game/ignite`; PROVE asserts
   a real `/game/run` receipt. A scripted beat is the deepest betrayal.
7. **Depth before breadth** (Mighty No. 9): one mission to reference quality, not eight at placeholder.
   Agents make breadth cheap — cheap breadth is the trap.
8. **Authoring a mission must never touch engine code** (Slay the Spire / Zachtronics). If it does, fix the
   schema, not the mission.
9. **Never build the deferred fog** (BUILDER/ARCHITECT, the antagonist ecology, rungs 3-7) before the center
   fires.
10. **Done means it RAN and was SEEN**; never claim conscious/alive; a dash never a 0/guess; a proof is a
    receipt. Never ship what a stranger would call a dashboard.

## THE DEPARTMENTS (as agent-runnable stages — each MAKES a real artifact)

`SYSTEMS/LOGIC` (the mission engine + the mission JSON schema) · `MISSION DESIGN` (missions as authored DATA) ·
`NARRATIVE` (LEYBER lines as data in the mission JSON) · `UX/MENUS` (views over data — bench + mission HUD) ·
`ART/TEXTURES` (build-to-match the refs, no new assets) · `QA/VERIFY` (honesty-lint + the screenshot/receipt
proof) · `PRODUCTION` (fix the milestone, cut the scope, the diary handoff). None fan out until the slice plays.

## THE STAGED PLAN (run in order; gate each on "it played")

- **STAGE 1 · THE VERTICAL SLICE (NOW):** `web/game/js/mission.js` (port the working `runBeat()` state machine
  from `world.html` — do NOT rebuild a general framework) + `web/game/data/missions/m01_first_light.json`
  (beats · beacon · gate · empty `leyber[]`), wired into `boot.js`. Beats: `brief · learn · do · observe ·
  prove · ask`. DO gates on `POST /game/ignite → run_id`; PROVE gates on `GET /game/run → receipt`. Strings
  cold-open → fly → dock → seat → ignite → read → prove → first reveal. **Done = it plays end-to-end, a real
  run_id + receipt returned, screenshot READ showing PROVE firing on a real draw, then Luis pilots.**
- **STAGE 2 (deferred):** honesty-lint — fix `tokens=0→dash`, `len>0` MEMORY, the `alive` field (only the one
  the slice surfaces).
- **STAGE 3 (deferred):** LEYBER lines authored over the running loop.
- **STAGE 4 (deferred):** bench build-to-match REF-10 (polish AFTER it plays).
- **STAGE 5 (deferred):** the mission HUD (view over data).
- **STAGE 6 (deferred):** production scale-out — missions 02…N as DATA against the frozen schema, agents in
  parallel, only after m01 plays.

**The one move now: STAGE 1.** Everything else is a checklist item that waits for "it played."
