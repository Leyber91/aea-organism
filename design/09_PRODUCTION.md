# 09_PRODUCTION — shipped slices, playtest log, queue, guards, risks

```
doc:          09_PRODUCTION.md (THE PROBE design corpus)
owner:        the game team
status:       LIVE — updated after every shipped slice and every playtest
last-updated: 2026-07-20
siblings:     GAME_PLAN.md (governing plan, root) · 04_UI_BIBLE.md (binding UI spec)
              missions.js (mission data, root) · world.html (the game, root)
              aea_elements.js (codex + map data, root)
ground truth: journey_save.json · grid_state.json · model_fitness.json (live files, root)
```

This document is the production ledger: what actually shipped (with evidence), what the
player actually did (with timestamps from the save file), what gets built next, and the
standing laws that keep the project from eating itself. Every section carries one of three
marks — **[BUILT]** (verified in code on disk), **[PLANNED]** (designed, not built),
**[DECISION-LUIS]** (awaiting his call). Nothing in this file is aspiration wearing a
status tag. The AEA honesty law applies to the doc itself.

---

## 1. Shipped slices [BUILT]

### Slice 1 — GENESIS + Act I playable (shipped 2026-07-20, morning)

`world.html` at `/world`. The locked form (GAME_PLAN.md §8): PILOT THE ENTITY, opening at
ACT 0 GENESIS.

- Genesis dark world on the city.html district geography; probe flight rig (WASD + Q/E,
  drag look, chase cam); beacon + off-screen arrow; dock terminal.
- Mission engine replaying `missions.js` (Acts 0–I: FIRST LIGHT, CATALOGUE, CHANNEL,
  METER, LADDER, BROWNOUT boss). Every DO/PROVE beat fires a REAL endpoint — M0.1's
  transmit is a live keyless call, M1.5's drill is four real draws through the mouth.
- WebAudio synth, HUD tracks (class / tests / plants / ingots read from live state),
  `/api/journey` server-side save (merge + reset, atomic, `.lock` file discipline —
  same durability rules as the entity's own state).
- Verified at ship: genesis + revealed screenshots, M0.1's real 200 ("FIRST LIGHT"),
  save roundtrip.

### Slice 1, iteration 2 — PROBE OS (shipped 2026-07-20, afternoon)

Built to the BINDING UI SPEC (04_UI_BIBLE.md) after a 100-source FUI research pass.
All verified in `world.html` on disk:

- **PROBE OS** (TAB): full-screen diegetic OS shell, v0.9; flight HUD dims to 0.22
  underneath it; presence chip stays at full opacity — LEYBER is always with you.
- **Concentric AEA map** (M): the codex rendered as the spec's ring geometry
  (`aea_elements.js` — viewBox 1000: core r70, rings 150/250/360/470; 29 elements:
  10 seeds, 5 axes, 3 verbs, 4 mechanics, 4 ops, 3 principles). Discovery state derives
  from `journey_save.json` mission completions; taught links draw only once their
  mission completes; SENSED promotion shows redacted neighbors of the discovered.
- **MODELS bestiary** (B): item cards from real encounters — a model enters the bestiary
  only via a real `tried[]` log, with true stats from `model_fitness.json`.
- **CODEX** (K): schematic projection of the AEA taxonomy, discovery-gated.
- **COMMS** (C): right dock into `/talk` — the entity comments from its real state.
  Quick-comms one-liner input (ENTER sends, ESC closes).
- **Presence**: the LEYBER presence chip, persistent across all views.
- **3D pass**: UnrealBloom composer (0.65 / 0.4 / 0.5); Film/Vignette/Gamma passes absent
  on disk so CSS carries the texture — a NAMED deviation, recorded in the source at
  `world.html` (composer block, ~line 375).
- **Discoverability law** (post-playtest, same day — see §2): persistent clickable key
  hints strip (`#hints`, world.html ~line 81), law text added to 04_UI_BIBLE.md.

Two-ink FUI throughout: amber (#ffb000 hot / #d4a24c warm) = live only; blue-gray =
structure. No third ink anywhere in the shipped build.

---

## 2. Live playtest log

The log records what the player DID, from `journey_save.json` and the session — not what
we hoped. One entry per playtest. Findings are triaged the session they land.

### Entry 001 — 2026-07-20 · player: Luis (player one) · build: slice 1 iteration 2

| time | event | evidence |
|---|---|---|
| 13:23 | **M0.1 FIRST LIGHT — WON, live.** One keyless prompt into the dark; the socket answered. The first real first-light of the game by its player. | `journey_save.json` done["M0.1"] = "2026-07-20 13:23"; reveal `plant_pollinations`; bestiary gained `pollinations/openai-fast` |
| 14:03 | **M1.1 THE CATALOGUE — completed.** Survey fired, plants revealed. Session ended here, before M1.2. | `journey_save.json` done["M1.1"] = "2026-07-20 14:03"; reveal `foundry_all` |

**Findings (triaged same session):**

1. **CRITICAL — the menu/map was undiscoverable.** Key bindings (TAB os, M map, C comms,
   F interface) were shown only on the title screen; once flying, Luis had no way to
   learn or recall them. He could not open the map at all. Forty minutes of shipped OS
   were invisible to the one player. **Resolution: DISCOVERABILITY LAW** added to
   04_UI_BIBLE.md and implemented same day — a persistent, clickable key-hints strip
   (`#hints`), breathing "loud" state until each key is first used, hidden only while
   the OS is open (world.html ~lines 81–91, 212, 244). Law text: no interaction exists
   until it is discoverable from the state the player is actually in.
2. **VISUAL — probe renders too hot on real GPU.** On Luis's hardware the probe core
   (world.html ~line 514: `emissive:HOT, emissiveIntensity:1.0`) blooms into a white
   blob under UnrealBloom 0.65. All ship-verification screenshots were swiftshader,
   which renders bloom dimmer — the two pipelines disagree and we verified on the wrong
   one. **Ticket: EMISSIVE-TUNE** (queued in §3, slice 2). Root cause is a process gap,
   not a code bug — logged as risk R2 (§5).

Verdict on the build from the player: playable, real, wanted more — blocked only by the
two findings above. Slice 1 gate ("Luis pilots slice 1 and calls go") — see §6.

---

## 3. Next-build queue

Ordered. Nothing enters ahead of the queue without displacing something by name.

### Slice 2 — Act II MEMORY [PLANNED]

The first forge act (GAME_PLAN.md §2, §4). Contents, in build order:

1. **EMISSIVE-TUNE ticket** — probe brightness on real GPU: drop core emissiveIntensity
   and/or bloom strength, verify on BOTH pipelines (see risk R2 protocol). Small, first,
   because the player sees it every second.
2. **Coach-marks** — first-run guidance layer applying the discoverability law beyond
   keys: first dock, first OS open, first map view each get a one-time diegetic mark.
   Spec lands in 04_UI_BIBLE.md before code.
3. **Act II field missions** — THE MINE (corpus sessions -> `consolidate --limit N` ->
   memory ingots in `luis_memory.json`; destructive-read of a finite real vein) and
   THE BOOK (the codex index as the map of what is already known). Mission JSON only —
   the engine replays it (GAME_PLAN.md §5).
4. **FORGE recall() / B2** — the first forge mission: the game frames the recipe
   (memory.py + index_codex + cache + energy.draw), the build is a pair session (Claude
   writes, Luis judges), the boss check and fog-reveal are automatic after. The game
   never pretends the UI wrote the code.
5. **Revealed-state art pass** — carried from the slice 2 definition in GAME_PLAN.md §8.

### Slice 3 — Act III MIND [PLANNED]

The council -> the regimes -> FORGE think() (D1, absorbs A2). Enters planning only after
slice 2 ships and is played. No design work on it before then beyond what GAME_PLAN.md
already holds.

---

## 4. Standing guards [BUILT — as process law]

These are not preferences; they are the walls. Each exists because its absence already
cost something once.

- **THE SEND stays pinned at Act V.** The convergence boss — draft real outreach,
  HADES-fit, LUIS sends — is the income clock made playable. No act reshuffle moves it
  later; no polish ships that delays the act path toward it. When scope competes with
  the clock, the trade is named in this file before it is taken.
- **Phase B is gated on Phase A played.** Audience now = Luis, player one. The
  anyone-builds-their-own-AEA phase (Phase B) gets zero build hours until Luis has
  played through the acts that exist. A tutorial for others written before player one
  finishes is fiction.
- **Re-planning only against new evidence.** A shipped artifact, playtest data, or a
  Luis decision. Re-reading GAME_PLAN.md and producing GAME_PLAN_2.md is the recorded
  failure mode of this whole workspace. The playtest log (§2) is what "new evidence"
  looks like: two findings, both triaged into build items, zero plan rewrites.
- **The boring test gates every slice.** Ships only if the acted-on systems are real
  (GAME_PLAN.md §8 guards: forge missions ARE the real AEA engineering; polish that
  does not serve the current act is refused).
- **The honesty law.** Every game number is live system truth. No fake data, ever —
  not in a bar, not in a bestiary card, not in a screenshot for this doc. Claim ceiling
  everywhere: "measured functional correlate, present" — never "conscious", never
  "sentient" (GAME_PLAN.md §1 honesty clause).
- **Two-ink law.** Amber #ffb000/#d4a24c = live/fired only; blue-gray = structure.
  Violations are bugs, filed as bugs. NO emoji, anywhere, ever.

---

## 5. Risks

| id | risk | evidence it is real | mitigation |
|---|---|---|---|
| R1 | **Scope inflation.** The OS invites infinite screens; "one more tab" is the local failure mode. Iteration 2 already grew from "map" to five views in one day. | This workspace's recorded history: a full prior conversation of brilliant strategy, zero artifacts. | The queue (§3) is the only door. New scope displaces a named item or waits. Park ideas in GAME_PLAN.md, not in code. |
| R2 | **Swiftshader-vs-GPU verification gap.** Headless swiftshader renders bloom/emissive dimmer than real hardware; we shipped a probe that verified clean and played blown-out. | Playtest finding 2 (§2): every pre-ship screenshot passed; player one's first minute did not. | Protocol change: any change touching emissive, bloom, or tone mapping verifies on BOTH pipelines — swiftshader screenshot AND a real-GPU eyeball (or a Luis screenshot) before "done". Recorded here so it survives sessions. |
| R3 | **Model rot changes Act I balance.** Missions assert against a live grid; the grid decays. The 2026-07-19 fitness sweep took the pool 44 -> 29 models, perfect 7 -> 2. A plant dying can turn M1.2 (three plants) or M1.5 (drill) from a lesson into a wall. | `model_fitness.json` deltas; the rot mechanic is itself a design pillar (GAME_PLAN.md §1). | Missions already fail HONESTLY (fail text names the real cause). Standing check before each playtest: run the survey, confirm >= 3 plants online; if the field has rotted under a mission, rebalance the mission data, never fake the state. |
| R4 | **Luis's session budget.** Two parallel deep sessions per night is the measured ceiling; quality decays past it. The game competes with the income track and the AEA engine itself for the same hours. | Standing rule in his operating doc; the income clock is real. | Slices sized to one session. Forge missions double-count (game progress IS AEA engineering — the same hour serves both). THE SEND placement (§4) keeps the game pointed at the clock instead of away from it. |

---

## 6. Open decisions [DECISION-LUIS]

| decision | context | default if unmade |
|---|---|---|
| Slice 2 go | Gate per GAME_PLAN.md §8: Luis pilots slice 1 and calls go. Playtest 001 completed M0.1 + M1.1; Acts 0–I not yet finished (M1.2–M1.5 remain). Go now, or after the BROWNOUT boss? | No slice 2 build beyond the EMISSIVE-TUNE ticket until called. |
| F1 senses (Act IV) | Flagged Luis-decision in GAME_PLAN.md §4 since inception. | Stays out of scope; Act IV plans without it. |
| Phase B timing | Gated on Phase A played (§4). Needs an explicit call, not drift. | Zero Phase B hours. |

---

*Change discipline: this file updates in the same commit as the thing it records. A slice
that shipped without a §1 entry did not ship; a playtest without a §2 entry did not happen.*
