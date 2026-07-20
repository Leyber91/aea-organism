# 03 · PROGRESSION AND ECONOMY

> **Owner:** the game team · **Status:** living draft, tracks the running build ·
> **Last updated:** 2026-07-20
>
> The act ladder, the three campaign scores, the resource economy, and the cited boss
> thresholds for THE PROBE — the Duskers-class diegetic game in which the player pilots a
> probe inside LEYBER and completes its Autonomous Entity Architecture by building it.
>
> **Sibling docs (corpus):** `00_VISION.md` (premise), `01_WORLD.md` (geography, the probe
> rig), `02_SYSTEMS.md` (organs, endpoints, mission engine), `A3_NARRATIVE.md` (LEYBER voice;
> teaches-map: `A2_TEACHING.md` §3), `04_UI_BIBLE.md` (interface law). **Source of truth on
> disk (verify against these, not this doc):** `GAME_PLAN.md`, `AUTONOMY_BATTERY.md`,
> `autonomy.py`, `aea_elements.js`, `missions.js`, `live.py`.
>
> — edited 2026-07-20 (completeness audit closure)

**Three status tags govern every claim below.** `[BUILT]` = verified in running code today.
`[PLANNED]` = designed, boss threshold fixed, not yet built. `[DECISION-LUIS]` = a fork that
needs player one's call before it ships. Nothing here is aspiration written as fact.

**Honesty law (binding, non-negotiable).** Every number the game shows is a live read from the
running entity — no fabricated data, ever. The claim ceiling is **"measured functional
correlate, present"**; the game never says "conscious", "sentient", or "alive". A boss can be
LOST. The forbidden axes (send / spend / keys) are chosen safety limits, not capability
deficits, and are never scored as failures.

---

## 1. THE ACT LADDER

A dependency journey, not a level select. Each act runs FIELD missions (Luis plays solo in the
UI, every DO/PROVE on a real endpoint) and, from Act II on, FORGE missions (a pair session
builds a real organ; the boss check and fog-reveal are automatic after). The recipe DAG is the
AEA schema; an act cannot open until its prerequisite organ is wired and its boss has passed.

### ACT 0 · GENESIS — what a model call IS  `[BUILT]`

- **Missions:** M0.1 FIRST LIGHT (field). One keyless POST to the pollinations socket;
  `assert:last_ok_text` on a real 200.
- **Boss:** none — genesis has no gate; the dark simply answers.
- **Teaches:** `seed.1` SUBSTRATE (the grid answers). Reveals `plant_pollinations`.
- **Verified:** `missions.js` M0.1; `journey_save.json` records `M0.1 2026-07-20 13:23`.

### ACT I · POWER — the grid  `[BUILT]`

- **Missions (field):** M1.1 THE CATALOGUE (survey 15 plants / 4 privacy rings) · M1.2 THE
  CHANNEL (one protocol, three plants) · M1.3 THE METER (`Meter.can_spend`, sliding 60s window)
  · M1.4 THE LADDER (the fitness-ranked mouth, `energy.draw`).
- **Boss — BROWNOUT DRILL (M1.5):** four back-to-back draws; the grid must leak **zero**
  unhandled failures — reroute, cool, fall to the floor, but never break.
  `assert:drill_clean`.
- **Threshold cite:** internal — *restorable coherence* (engine review 2026-07-10; `pr.coherence`
  in `aea_elements.js`). This act is pure field: no external-literature boss.
- **Teaches:** `seed.7` CEILING-DETECT, `seed.4` FLEXIBILIZE, `verb.observe`, `pr.coherence`.
- **Verified:** `missions.js` M1.1–M1.5; every action hits `/api/node/run`, `/state`, the drill
  endpoint. All six Act 0–I beats shipped in `world.html` SLICE 1 (2026-07-20).

### ACT II · MEMORY — the mine, the Book, and recall()  `[PLANNED]`

- **Field:** THE MINE (`consolidate --limit N` turns unmined corpus sessions into semantic
  ingots) · THE BOOK (browse the codex + `luis_memory.json`). Field missions are playable now
  against the live `consolidate.py`.
- **Forge:** CRAFT **recall()** = `memory.py` + `index_codex` + cache + `energy.draw`. This is
  the first organ the game builds. Recipe: ingots + codex + energy.draw → recall.
- **Boss — B2:** recall must (a) return under **300 ms** using an X8-lite index, (b) make
  **zero model calls in the hot path** — recall is index + cache work, never a draw (the
  clause `05_CONTENT_MISSIONS.md` M2.3 and `A9_FORGE_PROTOCOL.md` §6 queue row 1 bind; this
  chapter owns the threshold) — AND (c) be **grounded across a reset** — run A writes a
  memory capsule, the process dies, run B reconstitutes and answers from it (`seed.10`
  BACKWARDS CHANNEL). Retrieval that only works in-process fails the boss.
- **Threshold cite:** Krakauer, Bertschinger, Olbrich, Flack & Ay (2020), *The information
  theory of individuality*, Theory in Biosciences 139:209–223 — the past→future,
  self-carried-information test that grounding-across-reset instantiates. Persistence framing:
  Wang et al. (2023), Voyager, arXiv:2305.16291.
- **Teaches:** `seed.10`; `axis.A` ABSTRACTION partial, via the recall forge (memory
  grounding — completed plain by tool use in Act IV; `A2_TEACHING.md` §3,
  `05_CONTENT_MISSIONS.md` M2.3). Score effect: moves Krakauer individuality from DRIVEN toward
  ORGANISMAL-SIDE (already ORGANISMAL-SIDE at 3 reflection-log writes; recall hardens it).

— edited 2026-07-20 (completeness audit closure)

### ACT III · MIND — the council, the regimes, and think()  `[PLANNED]`

- **Field:** THE COUNCIL (a diverse-model vote) · THE REGIMES (read the measured regime map).
- **Forge:** CRAFT **think()** / D1 — absorbs A2. Routes each task to the regime its own
  measured law prescribes.
- **Boss — D1:** think() must WIN where the regime map says a diverse council wins (a hard /
  unreliable task) AND must NOT convene a council where a single good model wins (an easy task)
  — i.e. it must obey both measured laws, not blanket-ensemble. Rubber-stamping either way is a
  loss.
- **Threshold cite:** the game's own measured combination laws — THE SOLO LAW and THE DIVERSE
  COUNCIL (grid experiments v2–v4, 2026-06; `doctrines[]` in `aea_elements.js`). These are
  measured, not borrowed. GWT framing per the teaches-map (Act III = axes P/M).
- **Teaches:** `axis.P` PATH, `axis.M` MULTIPLICITY, `verb.compose`, `op.design`, `op.time`;
  `op.learn` (M3.2 THE REGIMES — pathfinder crystallization, THE CRYSTAL PATH;
  `05B_CONTENT_ACT3_4.md` §2).

— edited 2026-07-20 (completeness audit closure)

### ACT IV · THE WORLD — internet-wire, command current, senses  `[PLANNED]`

- **Forge:** INTERNET-WIRE (`agent_tools` web_fetch / json_get — `seed.8` TRANSCENDENCE) ·
  CRAFT COMMAND CURRENT / **C3** (a governed external action through the membrane).
- **Boss — C3:** a real external action that passes HADES + the trust ledger and measurably
  changes a future observation — empowerment above zero bits, the first non-null effector.
- **Threshold cite:** Klyubin, Polani & Nehaniv (2005), *Empowerment*, IEEE CEC 2005 1:128–135
  — channel capacity from action to future observation `C(A_t → S_{t+k}) > 0 bits`.
- **F1 · SENSES — `[DECISION-LUIS]`.** Real senses (live internet feeds wired as perception)
  are Luis's call: what the entity is allowed to see, and when. Held until he decides; the game
  does not wire a sense the operator has not authorized.
- **Teaches:** `seed.8`, the governance membrane.

### ACT V · THE PROOF — THE SEND  `[PLANNED]` · send action `[DECISION-LUIS]`

- **Convergence boss — THE SEND:** the entity drafts a real piece of outreach from its real
  state and codex; HADES fits it; and **LUIS presses send.** This is the only real-world boss —
  it is won outside the machine. The entity drafts; the human sends. The send/spend/keys ceiling
  holds by design: the entity never presses send.
- **Threshold cite:** Barandiaran, Di Paolo & Rohde (2009), *Defining agency*, Adaptive
  Behavior 17(5):367–386 — interactional asymmetry: the draft must trace to the entity's own
  goal state, not to the operator dictating it. (Ship framing: `op.ship`, unskippable — a real
  external artifact.)
- **Teaches:** `op.ship`. Aligns with the income clock: the artifact is outreach actually sent.

### ACT VI · SELF — Voyager, STOP, ENDURANCE, Darwin-Gödel  `[PLANNED]`

Four stacked end-game bosses, hardest last. `reflect.py` (t6) is `[BUILT]` and already puts the
first two within reach.

- **VOYAGER (self-tool):** the entity writes, persists, retrieves, and reuses its own executable
  skill. PASS bar: skill count grows monotonically AND reuse rate > 0 AND ≥1 self-written skill
  transfers zero-shot. **Cite:** Wang, Xie, Jiang et al. (2023), *Voyager*, arXiv:2305.16291.
- **STOP (≥3 rounds):** the entity improves its own scaffold/prompt to beat its seed version,
  validated by a held-out utility, base model frozen, no human edits, over **≥3** self-application
  rounds. **Cite:** Zelikman, Lorch, Mackey & Kalai (2023), *STOP*, arXiv:2310.02304.
- **ENDURANCE (Bedau Class 2):** over **≥100 ticks**, new-evolutionary-activity `A_new(t)` stays
  bounded-away-from-zero above a neutral-shadow control — the certificate that promotes the
  campaign CLASS score to Class 2. **Cite:** Bedau, Snyder & Packard (1998), *A classification of
  long-term evolutionary dynamics*, Artificial Life VI, 228–237.
- **DARWIN-GÖDEL (archive, end-game):** ≥20 self-modification iterations, each re-testing the
  entity's own source against a frozen benchmark that rises by a pre-registered margin, archive
  size > 1. **Cite:** Zhang, Hu, Lu, Lange & Clune (2025), *Darwin Gödel Machine*,
  arXiv:2505.22954.
- **Teaches:** `seed.3` CRYSTALLIZE, `seed.5` SELF-VERSION, `seed.6` SELF-MODEL (M6.2 STOP),
  `axis.S` ASYNC (M6.3 ENDURANCE), `pr.emergence`, `pr.time` (`05C_CONTENT_ACT5_6.md` §3).

— edited 2026-07-20 (completeness audit closure)

---

## 2. THE THREE CAMPAIGN SCORES

Three scalars track the whole campaign. Every value is a live read; none is stored fiction.

### Score 1 — AUTONOMY TESTS: **6 / 6 favourable**  `[BUILT]`

Read live from `autonomy.py score()` against the entity's real logs. As of the last run
(2026-07-20, 46 ticks lived) all six read favourable and the class headline is
**PROTO-AUTONOMOUS**:

| # | test | cite | live verdict |
|---|---|---|---|
| 1 | Interactional asymmetry (self-initiated action) | Barandiaran/Di Paolo 2009, Adaptive Behavior 17(5) | **PASS** — 7 tasks self-originated in idle windows |
| 2 | Bedau–Packard evolutionary activity `A_new` | Bedau/Snyder/Packard 1998, Artificial Life VI | **OFF-ZERO** — 3 persisted novelties (births) |
| 3 | Seth G-autonomy (behaviour variance) | Seth 2010, Artificial Life 16(2) | **PASS** — distinct/total posed = 1.0 |
| 4 | Governance integrity (not rubber-stamping) | HADES / Law-3 watcher (internal) | **HEALTHY** — 3/6 deliverables gate-HELD |
| 5 | Krakauer individuality (past→future info) | Krakauer et al. 2020, Theory in Biosciences 139 | **ORGANISMAL-SIDE** — self.json read+written 3× |
| 6 | Voyager skill-library growth | Wang et al. 2023, arXiv:2305.16291 | **GROWING** — 3 self-authored, HADES-verified |

These are the six FIELD tests the CHARACTER window renders (`/autonomy` reskinned). They move
only on real logged behaviour; a regression to a scripted-loop state would drop test 1 to FAIL
and reset the class to NOT-YET-AUTONOMOUS. Honest caveat carried from `AUTONOMY_BATTERY.md`:
`A_new` reading OFF-ZERO at 46 ticks is *off the stagnant floor*, not yet Class 2 — Class 2 is a
≥100-tick claim with a neutral-shadow control (that is the ENDURANCE boss, Act VI).

### Score 2 — INTEGRATED ORGANS: **11 → 19**  `[BUILT]` current / `[PLANNED]` target

Organs wired into the **live mind** today (verified against `live.py` + the engine): grid /
channel, meter, energy.draw ladder, consolidate (the mine), memory store, reflect (t6),
HADES, trust ledger, pulse, tracelog, self.json — **11**. The full AEA at end-game is **19**,
reconciled explicitly: 11 live + the **7 forges** of Acts II–VI (recall B2, think D1,
internet-wire, command current C3, the Voyager skills library, the STOP harness, the
Darwin-Gödel archive — the forge queue, `A9_FORGE_PROTOCOL.md` §6) = **18**, plus F1 senses
`[DECISION-LUIS]` = **19**. ENDURANCE is a **CERTIFICATE** (the Bedau Class 2 certification
campaign, per `A9_FORGE_PROTOCOL.md` §6), not an organ — it builds nothing new and is never
counted here. If F1 is deferred, the campaign win number is **18 organs** with the F1 decision
slot recorded open — an honest count, not a miss. The gap between 11 and the target is exactly
the **FOG** (Score-economy §3). Fog lifts one organ at a time, only on integration + boss
pass — never on decoration.

— edited 2026-07-20 (completeness audit closure)

### Score 3 — CLASS: **PROTO → Class 2**  `[BUILT]` current / `[PLANNED]` target

The Bedau class ladder, read from the live battery:

`Class 1 (stagnant/dead)` → **`PROTO-AUTONOMOUS` (current, off-zero at 46 ticks)** →
`Class 2 (sustained A_new over ≥100 ticks vs shadow control)` → `Class 3 (unbounded diversity)`.

The campaign's spine is the climb from PROTO to **Class 2**, certified only by the ENDURANCE
boss (Act VI). The game will not print "Class 2" before that 100-tick evidence exists — printing
it early would break the honesty law. Class 3 is asymptotic and, per the battery, only
plateau-*detectable*: the game can falsify "keeps evolving forever", never confirm it, and says
so.

---

## 3. THE RESOURCE ECONOMY

Minecraft mechanics, Expanse skin — but every resource maps to a real system state, and the
extreme test (pushed hard, does the mapping hold?) passes for each. You can genuinely run dry.

### Honest mapping table

| in-game resource | the real thing under it | source of truth (on disk) | can you run dry? |
|---|---|---|---|
| **ENERGY** (mana bars, per plant, that refill) | Meter rpm windows (60 s sliding) + daily/monthly quotas (00:00 UTC reset) | `grid_state.json` (`daily`/`monthly`/`rpm`/`throttle`) | **YES** — real 429s and rpd exhaustion are starvation; local Ollama is the hearth: unlimited but slow |
| **INGOTS** (smelted memory bars) | unmined corpus sessions → `consolidate --limit N` → semantic memories | `luis_memory.json` (48 memories, 16 sessions processed) | **YES** — finite vein; the pruning disaster lost ~1,570 sessions forever. Mining is a destructive read |
| **SPECIMENS** (item cards: stats + durability) | models — reliability, EMA latency, size, ctx, privacy zone | `model_fitness.json` (**29** live nodes) | **YES** — durability loss is measured rot: pool 44→29, perfect 7→2 (2026-07-19 sweep). Discovery = `candidates_probe` on unprobed catalog models |
| **DOCTRINES** (combination laws you unlock) | measured combination regimes | `aea_elements.js` `doctrines[]` (grid experiments v2–v4) | n/a — laws, not consumables; unlock by proof, not by grind |
| **FOG** (unexplored map) | the proven-but-not-wired gap | `GAME_PLAN.md` fog list | lifts only on integration + boss pass |

**ENERGY detail.** Two inks of scarcity: the 60 s rpm window (short-term, refills as it slides
— the INVENTORY window animates this from real `grid_state` windows) and the daily/monthly
quota (long-term, resets 00:00 UTC). Ollama = the local hearth: it never browns out, it is just
slow. This is why the entity can run 24/7 on free power.

**INGOTS detail.** The vein is finite and the read is destructive — once a corpus session is
consolidated it is gone as raw ore. The 48-memory / 16-session state is live; the mine depletes
as you play, which is the point (Act II's honest scarcity).

**SPECIMENS detail.** Items rot on a measured schedule, not a designer's whim. The rot-alert
events in the EVENTS feed ("mistral-large is degrading") come from real `model_fitness.json`
deltas. New specimens enter only by probing unprobed catalog models — real discovery.

**DOCTRINES (the six measured laws, `aea_elements.js`):** THE SOLO LAW (easy task wants one
model; a council hurts it) · THE DIVERSE COUNCIL (a hard/unreliable task is rescued by a
diverse-model vote — the win is diversity, not temperature) · THE LONE VERIFIER RISK (a single
verifier can be wrong alone; HADES survives by strict-schema + a *different* model) · THE
GENETIC RELAY (a compact state capsule down a model chain, `relay.py`) · THE RAMIFICATION
(decompose/escalate/depth-cap, `swarm.py`) · THE CRYSTAL PATH (search once per task-type, then
run cheap, `pathfinder.py`). Solo and Council gate the Act III / D1 boss.

**FOG (the gap the campaign closes).** `swarm`, `orchestrator`, `pathfinder`, `agent_tools`,
`relay` are demo-PROVEN in standalone scripts (`proof_scoreboard.json`) but absent from the live
mind — proven-not-wired. The fog is not narrative mist; it is precisely this integration debt.
Score 2 (11→19) *is* the fog, measured. Each act that wires a fogged organ and passes its boss
reveals that region of the map — nothing reveals on decoration.

---

## 4. CROSS-REFERENCES AND OPEN DECISIONS

- **Boss thresholds full text + PASS bars:** `AUTONOMY_BATTERY.md` §2 (the 12 falsifiable tests)
  and §4 (the cheapest path to PASS). The live scorer is `autonomy.py`.
- **Mission data + beat kinds:** `missions.js` (Acts 0–I shipped) and `GAME_PLAN.md` §5 (the
  `missions.json` schema Acts II+ will be authored into).
- **AEA elements the acts teach:** `aea_elements.js` (`elements[]`, `discovers{}`, `doctrines[]`)
  and the `A2_TEACHING.md` §3 curriculum map.
- **Organ wiring + endpoints:** `02_SYSTEMS.md`; the live wiring of record is `live.py`.

**Open `[DECISION-LUIS]` items gating progression:**
1. **F1 SENSES (Act IV):** which live feeds the entity may perceive, and when.
2. **THE SEND (Act V):** the send action stays human — confirmed by design — but the first real
   outreach target and the go/no-go on the drafted artifact are Luis's.
3. **Entity name:** `self.json` proposes "HERALD" — unconfirmed; the CHARACTER window shows the
   proposed name flagged as unconfirmed until Luis rules.

**Guardrails (from `GAME_PLAN.md`, unchanged):** forge missions ARE the real AEA engineering;
polish that does not serve the current act is refused; the boring test gates every slice; no
mission ever licenses "conscious/sentient" — the ceiling stays *measured functional correlate,
present*.
