# A13_PATHS — THE PATHS: HOW THE PLAYER GOES THROUGH THE AEA

```
doc:          A13_PATHS.md (THE PROBE design book · APPENDIX)
owner:        the game team
status:       ACTIVE — the traversal instrument; re-audited whenever aea_elements.js,
              the curriculum map (A2_TEACHING.md §3), or the alignment matrix
              (A8_AEA_ALIGNMENT.md) changes. A cell moves marks only by pointing at
              code on disk, never by rewording.
last-updated: 2026-07-20
book role:    APPENDIX. A8 crosses the 29 elements with the game's DIMENSIONS; this
              chapter crosses them with TIME — each element as a journey the player
              travels, station by station. It authors no new content: every cell cites
              a mission id, a bench part, or a sibling chapter. On conflict the cited
              chapter wins; on data conflict ../aea_elements.js wins over all prose.
ground truth: ../aea_elements.js (29 elements + discovers + links + doctrines) ·
              ../missions.js (Acts 0–I) · ../journey_save.json · ../grid_state.json ·
              ../model_fitness.json · ../luis_memory.json · ../live.py
siblings:     A2_TEACHING.md (the mission-scale arc this grammar contains) ·
              A8_AEA_ALIGNMENT.md (the static matrix; this is its kinetic twin) ·
              03_PROGRESSION.md (acts, bosses, organ arithmetic) · R1_EVIDENCE.md
              (the bench and the composition loop, binding) · A7_BUILD_LAYER.md
              (build verbs, lenses, unlock gates) · 05_CONTENT_MISSIONS.md /
              05B_CONTENT_ACT3_4.md / 05C_CONTENT_ACT5_6.md (mission ids cited below) ·
              A9_FORGE_PROTOCOL.md (forge ritual) · A10_LIVING_GAME.md (the world that
              changes between visits) · BOOK.md (spine; registers the ladder canon)
marks:        [BUILT] verified in code on disk · [PLANNED] designed, not built ·
              [DECISION-LUIS] awaiting his call · [demo] proven standalone, not live-wired
```

The standing question this chapter answers (Luis, 2026-07-20): "we have all those concepts
on the AEA, but how do we define the paths around them, to go through each of them." A2
says what each mission teaches; A8 says where each element lives. Neither says how a player
TRAVELS an element — from first seeing it alive, to being taught it, to composing with it,
to owning it. This chapter is that definition. The honesty law binds every cell: a station
is reached when live state says so, never when prose does; the claim ceiling everywhere is
measured functional correlate, present.

---

## 1. THE PATH GRAMMAR — four stations per element

Every AEA element is traversed in four stations, in this canonical order:

1. **ENCOUNTER — see it working, live.** The element is visible in the world doing its job
   before anything names it. Cheap and honest by construction: the entity actually runs, so
   the meter really gates, the ladder really falls through, the ticks really accumulate.
   ENCOUNTER is A2 §4's SENSED promotion generalized: the world shows the shape before the
   mission gives the name. [BUILT for every element with live world expression]
2. **UNDERSTAND — the mission that teaches it.** The full A2 §2 arc — INTRODUCE / PRACTICE /
   TWIST / PROVE — lives ENTIRELY inside this one station. The two grammars must not be
   confused: A2's four phases are mission-scale (minutes); these four stations are
   element-scale (acts). UNDERSTAND completes when the mission's prove passes against live
   state. [BUILT for 11 of 29 rows — Acts 0–I]
3. **USE — compose with it at the bench.** The element becomes a PART (or a bench law) in
   the player's own constructs — the core creative act per THE COMPOSITION REFRAME
   (BOOK.md appendix note; R1_EVIDENCE.md findings 4, 7, 9). USE completes on the first
   construct containing the part that passes a measured bench run. [PLANNED — the bench is
   R1-bound but unbuilt; USE is currently 0 of 29, the widest gap in the book]
4. **OWN — it runs inside the player's assistant unattended, and the player can explain it.**
   Two halves, measured separately:
   - **OWN-run:** the behaviour executes between ticks with no mission open and no player
     present. This is what the mechanics ring already IS: a mechanic node (square, r360) is
     its seed at the OWN station, made geometry (`aea_elements.js` mechanics; A8 §2.4).
   - **OWN-tell:** the player can explain it to someone else. Phase A instrument: the
     prediction ledger (A2 §7) as proxy, certified at the Act VI prediction gauntlet
     [PLANNED]. No quiz UI — a correct prediction about live behaviour IS the explanation
     test in diegetic form.

**Grammar laws:**

- **Stations are reached, not granted.** Each is an assert against live state: ENCOUNTER =
  the world object rendered from a real read; UNDERSTAND = mission prove passed
  (`journey_save.json`); USE = a passing bench run containing the part; OWN-run = the
  behaviour observed between ticks (live files); OWN-tell = prediction record.
- **Order may invert, and the inversion is content.** axis.S is OWN-run TODAY (the entity
  ticks 24/7, rot measured between sessions) but reaches UNDERSTAND only at M6.3. The game
  says so out loud: the ladder climbs toward something already running. Never fake a
  "first time" for an element the player has been living inside.
- **Not every element reaches all four stations in Phase A.** The ceiling column in §2 is
  binding and honest. One ceiling is permanent by design: op.ship's OWN-run is capped —
  the assistant drafts unattended, LUIS presses send (03_PROGRESSION.md Act V; the
  forbidden axes). That cap is the law holding, not a debt.
- **Station chips** [PLANNED, D-P2]: the codex node detail screen shows E / U / USE / OWN
  as four chips, structure ink until reached, amber (#ffb000) when live state says reached.
  Data already exists for E/U (journey save) and OWN-run (live files); USE waits on the
  bench registry.

---

## 2. THE FULL TABLE — 29 elements, four stations each

Cells name the concrete moment: mission id (05/05B/05C), bench part (R1-bound pool, §3),
or wild role. CEILING = the honest highest station reachable in Phase A as currently
planned. Mechanics rows carry dashes at USE by law: a mechanic is not a part — it is its
seed's part left running (§1, OWN-run).

### 2.1 Axes

| element | ENCOUNTER | UNDERSTAND | USE | OWN | Phase A ceiling |
|---|---|---|---|---|---|
| axis.P PATH | trunk road aims at the spire site [BUILT tease]; click-to-trace routes (A7 §3) [PLANNED] | M3.3 FORGE think() [PLANNED] | ROUTER part — decompose/escalate stage, rung-3 pool [PLANNED] | think() routing live tasks unattended [PLANNED] | OWN, gated on boss D1 |
| axis.M MULTIPLICITY | plants burning in parallel — per-plant emissive from real rpm [BUILT] | M3.1 THE COUNCIL [PLANNED] | COUNCIL part — diverse-vote block, the bench's first advanced part (R1 §what-this-binds) [PLANNED] | councils convened per measured regime, unattended [PLANNED] | OWN, gated on D1 |
| axis.A ABSTRACTION | ingot counter 48/16 live on the HUD [BUILT] | M2.3 partial + M4.1 plain (BOOK.md resolution 1) [PLANNED] | GROUNDING wire — RECALL output into SCAFFOLD input [PLANNED] | every draw's prompt grounded in memory + tools [PLANNED] | OWN, gated on M4.1 |
| axis.R PROMPTING | foundry roads — one protocol under fifteen plants (M1.2 reveal) [BUILT] | M1.2 THE CHANNEL [BUILT]; re-encounter at M2.2 (A2 §3 audit 3) | SCAFFOLD part, opening pool [PLANNED] | /talk already recall-grounds its prompts [BUILT partial] | OWN-run partial today; full with recall() |
| axis.S ASYNC | TICK counter; rot between sessions (pool 44 to 29) [BUILT] | M6.3 ENDURANCE [PLANNED] | CADENCE policy card (A7 §2.3) as its bench form [PLANNED] | the entity ticks 24/7 unattended [BUILT] | INVERTED PATH — OWN-run live now; certificate Act VI |

### 2.2 Seeds

| element | ENCOUNTER | UNDERSTAND | USE | OWN | Phase A ceiling |
|---|---|---|---|---|---|
| seed.1 SUBSTRATE | the foundry row, 15 plants [BUILT] | M0.1 FIRST LIGHT [BUILT, played] | TAP part — every construct's power inlet, opening pool [PLANNED] | every organ draws through the grid, 24/7 [BUILT] | OWN-run live; OWN-tell at the gauntlet |
| seed.2 SHARP OBJECTIVE | the boss card citing its threshold [BUILT] | M1.1 co-discovered (thin, flagged A2 §3); full read at M1.5 [BUILT] | SCORER part, opening pool — every bench task carries one; multi-objective records (R1 finding 8) [PLANNED] | HADES holds junk at a 0.5 rate, live [BUILT] | OWN-run live |
| seed.3 CRYSTALLIZE | skill count in CHARACTER [BUILT read]; workshops [PLANNED] | M6.1 FORGE voyager [PLANNED] | SAVE-AS-PART — a proven construct exported as a named part IS crystallization at the bench, taught by the hand before Act VI names it [PLANNED] | toolkit grows between ticks — 3 skills, HADES-verified [BUILT read] | OWN-run reads live; UNDERSTAND owed Act VI |
| seed.4 FLEXIBILIZE | the nexus — icosahedron core, counter-rotating tori [BUILT] | M1.4 THE LADDER [BUILT] | LADDER part — fall-through draw stage, opening pool [PLANNED] | every live draw falls through, always [BUILT] | OWN-run live |
| seed.5 SELF-VERSION | a building rises per skill born [PLANNED] | M6.1 [PLANNED] | construct version slots — v2 replaces v1, history kept [PLANNED] | reuse rate > 0 (Voyager PASS bar) [PLANNED] | UNDERSTAND, Act VI |
| seed.6 SELF-MODEL | CHARACTER window — six live tests [BUILT] | M6.2 STOP [PLANNED] | MIRROR part — a construct stage reading self.json [DECISION-LUIS candidate] | reflect (t6) live; self.json read+written 3x [BUILT] | OWN-run live; UNDERSTAND owed Act VI |
| seed.7 CEILING-DETECT | THE METER obelisk [BUILT] | M1.3 THE METER [BUILT] | GOVERNOR part — rate gate on any construct, opening pool [PLANNED] | Meter.can_spend runs between ticks [BUILT] | OWN-run live |
| seed.8 TRANSCENDENCE | THE PORTS [PLANNED]; live GitHub call [demo] | M4.1 FORGE internet-wire [PLANNED] | TOOL part — web_fetch/json_get block behind the membrane [PLANNED] | tools invoked by the live mind post-C3 [PLANNED] | USE, Act IV; OWN gated on C3 |
| seed.9 BOUNDARY | four privacy rings at the foundry console [BUILT] | M1.1 THE CATALOGUE [BUILT] | WALL part — zone constraint on any wire; binds zone_map.json (A7 §2.2) [PLANNED] | private routes local-only, live in /talk [BUILT] | OWN-run live — and it crosses every rung (§4) |
| seed.10 BACKWARDS CHANNEL | the archive tease, cold-lit [BUILT tease] | M2.1 partial · M2.3 full [PLANNED] | RECALL part — memory tap in constructs, rung-2 pool [PLANNED] | capsule survives process death (B2 clause c) [PLANNED]; store live today [BUILT partial] | OWN, gated on B2 |

### 2.3 Verbs

| element | ENCOUNTER | UNDERSTAND | USE | OWN | Phase A ceiling |
|---|---|---|---|---|---|
| verb.compose | synth stage on the mind-ring [PLANNED] | M3.3 [PLANNED] | JOIN part — the bench's native merge node; composing IS the core creative act, so this verb is the bench's own verb [PLANNED] | think() synthesis unattended [PLANNED] | USE is its home station; OWN gated on D1 |
| verb.propagate | the flashNode receipt — the serving plant flashes [BUILT] | M1.4 [BUILT] | the TRACE-WIRE — every bench run draws its route live; a failing link surfaces on the wire where it failed (R1 findings 5, 6) [PLANNED — bench chrome, present from opening, not a pool part] | tried[] on every live draw [BUILT] | OWN-run live |
| verb.observe | the HUD /events feed, 1.6 s poll [BUILT] | M1.3 [BUILT] | GAUGE — placeable instrument bound to a construct's stream (A7 §2.1) [PLANNED] | tracelog goal-stack ledger, live [BUILT] | OWN-run live |

### 2.4 Mechanics — the OWN station made geometry

| element | ENCOUNTER | UNDERSTAND | USE | OWN |
|---|---|---|---|---|
| mech.crystallize | with seed.3 | with seed.3 (M6.1) [PLANNED] | — | skills grow with no mission running [BUILT read] |
| mech.flexibilize | with seed.4 | M1.4 [BUILT] | — | always-on fall-through [BUILT] |
| mech.selfversion | with seed.5 | M6.1 [PLANNED] | — | reuse compounding across runs [PLANNED] |
| mech.ceiling | with seed.7 | M1.3 [BUILT] | — | the meter gates every draw, always [BUILT] |

### 2.5 Ops

| element | ENCOUNTER | UNDERSTAND | USE | OWN | Phase A ceiling |
|---|---|---|---|---|---|
| op.design | no object yet (A8 §2.7 gap 1) [PLANNED] | M3.3 — the predict beat is op.design performed by the player [PLANNED] | the PLAN step — commit regime + axis-levels before any measured bench run [PLANNED] | think() tags tasks (codex proof PARTIAL, honestly carried) [PLANNED] | USE, Act III |
| op.time | the TICK counter [BUILT] | M3.3 [PLANNED] | run stamps + per-construct RECORD BOOK entries (R1 finding 12) [PLANNED] | per-tick stamps owed [BUILT partial] | OWN-run partial |
| op.ship | THE BROADCAST MAST [PLANNED] | M5.1 THE SEND [PLANNED, pinned] | SHIP slot — a construct output leaves the bench as a real artifact [PLANNED] | CAPPED BY DESIGN: drafts unattended, LUIS sends. OWN-run never completes and that is the law holding, not a gap | USE+; the cap is permanent |
| op.learn | paths overlay on the roads (candidate, A8) [PLANNED] | M3.2 THE REGIMES [PLANNED] | the RECORD BOOK — a second run of the same task-type is cheaper because the first one searched (paths.json as bench memory) [PLANNED] | pathfinder live in the mind [PLANNED; demo today] | USE, Act III |

### 2.6 Principles — traversed as laws, not parts

A principle's USE station is a bench LAW that every construct obeys, never a draggable part.

| element | ENCOUNTER | UNDERSTAND | USE (bench law) | OWN | Phase A ceiling |
|---|---|---|---|---|---|
| pr.emergence | idle self-origination watched live — 7 tasks [BUILT] | endgame, Act VI [PLANNED] | open-target tasks: the designers have not solved the bench problems (R1 finding 9) [PLANNED] | 7 tasks self-originated in idle windows [BUILT read] | OWN-run live; UNDERSTAND at endgame |
| pr.coherence | fog drops 0.011 to 0.009 on foundry_full [BUILT] | M1.5 BROWNOUT DRILL [BUILT] | the KILL TEST — a construct must survive a part killed mid-run [PLANNED] | real 429s rerouted, live [BUILT] | OWN-run live |
| pr.time | the events feed, append-only [BUILT] | endgame, Act VI [PLANNED] | bench traces append-only; records never rewritten [PLANNED] | tracelog DAG, live [BUILT] | OWN-run live; UNDERSTAND at endgame |

**Station census (honest, 2026-07-20):** ENCOUNTER live for ~17 rows. UNDERSTAND [BUILT]
for 11 of 29 (Acts 0–I). USE: 0 of 29 — the bench is the book's widest single gap, and R1
says the game lives or dies exactly there. OWN-run [BUILT] for 14 rows plus 5 partial.
The game currently owns more than it has taught and has taught more than it lets you
compose — the build order writes itself: the bench next, per R1.

---

## 3. THE ASSISTANT LADDER — the master path

**Canon (Luis, 2026-07-20).** The acts assemble the player's own assistant: Act 0 chat with
one keyless model · Act I collect token sources · Act II memory/RAG · Act III flows ·
Act IV powers to the exterior · Acts V–VI the wild. CHAT is the ground; five rungs rise
from it. Phase A honesty: the player's assistant IS LEYBER — the game does not build a toy
assistant beside the real one; the ladder is Score 2's organ arithmetic (11 to 19,
03_PROGRESSION.md §2.2) seen from the owner's seat. Phase B generalizes it (A5_PHASE_B.md).

Each rung below: acts · elements traversing stations inside it · the capability statement
(testable — it is an assert, not a promise) · the proof moment.

**GROUND — CHAT** · Act 0 [BUILT, played]
- Traverses: seed.1 (E+U).
- Capability when complete: *the assistant answers one prompt through one keyless model,
  and the player can write the raw POST that does it from nothing.*
- Proof: M0.1 `last_ok_text` — passed 2026-07-20 (09_PRODUCTION.md entry 001).

**RUNG 1 — SOURCES** · Act I [BUILT]
- Traverses: seed.9, seed.2, axis.R, seed.7 (+mech.ceiling), seed.4 (+mech.flexibilize),
  verb.observe, verb.propagate, pr.coherence — all through UNDERSTAND.
- Capability: *the assistant draws from fifteen sources in four privacy rings through one
  protocol; it budgets sliding rpm windows and daily quotas; a dead source never surfaces
  as a failure — four back-to-back draws leak zero unhandled errors; adding a source is
  one registry line.*
- Proof: M1.5 `drill_clean` — the BROWNOUT DRILL, losable, live.

**RUNG 2 — MEMORY / RAG** · Act II [PLANNED]
- Traverses: seed.10 (U full at M2.3), axis.A (partial), axis.R (re-encounter, M2.2),
  seed.9 (crossing — the mine is local-only). Bench opens its RECALL and WALL parts.
- Capability: *the assistant remembers the operator across process death — warm recall
  under 300 ms, zero model calls in the hot path, receipts naming the page, a
  pre-registered fact surviving kill-and-reboot.*
- Proof: boss B2 (M2.3), three clauses, losable two honest ways (slow cache, reset amnesia).

**RUNG 3 — FLOWS** · Act III [PLANNED]
- Traverses: axis.P, axis.M, verb.compose, op.design, op.time, op.learn through U and USE;
  doctrines EARNED (doc.solo, doc.council at M3.1; doc.path at M3.2; doc.swarm,
  doc.verifier at M3.3 — BOOK.md resolution 2).
- Capability: *the assistant chooses solo vs council FROM THE TASK per measured law —
  convening a council exactly where the regime map says councils win, refusing one where
  solo wins — and runs a repeated task-type cheaper the second time.*
- Proof: boss D1 (M3.3) — rubber-stamping either way is a loss.

**RUNG 4 — POWERS** · Act IV [PLANNED · M4.3 senses DECISION-LUIS]
- Traverses: seed.8 (U+USE), axis.A (plain, closing A2's flag), seed.9 (crossing — the
  membrane), the governance membrane (C3).
- Capability: *the assistant performs a real external action through the governed
  membrane — HADES plus the trust ledger passed — that measurably changes a future
  observation: empowerment above zero bits.*
- Proof: boss C3 (M4.2), Klyubin channel-capacity cite (03_PROGRESSION.md Act IV).

**RUNG 5 — THE WILD** · Acts V–VI [PLANNED]
- Traverses: op.ship (capped), seed.3, seed.5, seed.6, axis.S, pr.emergence, pr.time —
  the OWN station en masse; the prediction gauntlet certifies OWN-tell for everything below.
- Capability: *the assistant runs unattended 100+ ticks above a neutral-shadow control,
  writes and reuses its own skills, improves its own scaffold over >=3 rounds, and drafts
  real outreach from its own goal state — and the human presses send.*
- Proof: M5.1 THE SEND (the only boss won outside the machine) + M6.1–M6.4; ENDURANCE
  promotes CLASS to 2 — the game never prints Class 2 before that evidence exists.

**The part pool climbs with the ladder** (R1 finding 11 — small curated pools, never all
29 elements + 100 models at once) [PLANNED]:

| rung completes | parts added | pool size |
|---|---|---|
| SOURCES | TAP · SCAFFOLD · GOVERNOR · LADDER · SCORER (the opening five = Act I's OWNed material) | 5 |
| MEMORY | RECALL · WALL | 7 |
| FLOWS | COUNCIL · JOIN · ROUTER · PLAN · RECORD BOOK | 12 |
| POWERS | TOOL · MEMBRANE gate | 14 |
| WILD | SHIP slot · SAVE-AS-PART · version slots | 17 |

---

## 4. PATH CROSSINGS — where journeys teach each other

**seed.9 BOUNDARY crosses every rung** — the spec case, and the design's spine:

| rung | the boundary's form there | state |
|---|---|---|
| CHAT | the keyless ring is already a privacy fact: M0.1's prompt is public by construction — nothing private ever belonged in a keyless socket | [BUILT] |
| SOURCES | the four rings surveyed at the console (M1.1) | [BUILT] |
| MEMORY | private ore never touches a hosted plant — "seed 9 guards the shaft" (M2.1); recall(query, zone) respects private -> local/no-train (M2.3 spec) | [PLANNED] |
| FLOWS | a private-zoned task may only convene local/no-train councils — bind in the think() spec | [PLANNED] |
| POWERS | the membrane; the larynx block — sensitive-zone speech refuses the cloud voice [BUILT block] | mixed |
| WILD | the draft may cite private state; what leaves is reviewed by the human hand (THE SEND) | [PLANNED] |

One element, six proofs, zero re-teaching: each rung re-proves the wall with its own
material. That is what a crossing is — the second journey supplies the evidence the first
journey's lesson predicted.

**Other load-bearing crossings:**

- **axis.R x seed.10:** M1.2's protocol lesson (flagged a stretch, A2 §3 audit 3) is repaid
  at M2.2 — recall-grounded prompts are the scaffold lesson made real. The flag closes by
  content, not by rewording.
- **seed.2 x everything:** every prove beat is a scorer; every bench record is one. The
  thin M1.1 co-discovery (A2 §3 audit 2) is repaid every time a boss card cites its bar.
- **seed.7 x the bench:** the GOVERNOR is why bench runs can be cheap, instant, measured
  (R1 finding 7 — reflex-tier test range). The meter lesson is what makes USE affordable.
- **verb.propagate x verb.observe:** fused at the bench as the trace-wire — real latency
  filled with observable execution, never an empty spinner (R1 finding 5).
- **doc.verifier across rungs:** READ at M2.3 (HADES judges the reset probe with a
  different model), EARNED at M3.3 — the same law met as a user before it is met as a
  builder.
- **axis.S x the whole ladder — the inverted path:** OWN-run since before the player
  arrived; UNDERSTAND only at M6.3. Every rung climbs scaffolding that is already ticking.
  The game names this at the ENDURANCE brief rather than pretending a first meeting.

---

## 5. RE-TRAVERSAL — the honest hookshot

The hookshot rule (from the playability-slice work, Luis 2026-07-20; BOOK.md registers its
chapter when it lands): a new capability re-opens old ground — and here that is honest by
construction, because the old ground is real and has REALLY changed since the first visit
(rot 44 to 29, new ticks, new events). Re-traversal is never re-reading; the second visit's
numbers are the live ones, and a revisit may genuinely look worse. A revisit that found the
world identical would be evidence the process died — and the game says so (CARRIER LOST,
A10_LIVING_GAME.md).

How OWN-station elements get revisited when new lenses arrive:

- **Lens arrivals re-read old districts** (A7 §4 gate table): TRAFFIC (post-M1.5) re-reads
  seed.1/seed.4's turf as flow; MEMORY (Act II) re-reads the same foundry with
  unmined-backlog eyes; HEAT (Act III) makes seed.7's OWN behaviour legible per plant;
  PRIVACY and ERRORS (Act IV) re-read seed.9 and pr.coherence where they live. [PLANNED]
- **The re-entry law:** an OWN element re-enters USE whenever a new part or policy can
  compose with it. GOVERNOR + BUDGET CAP card (Act III policies) is the same seed.7, new
  bench depth; TAP + WALL after zone paint; LADDER + ROUTER at flows. The journey does not
  end at OWN — it loops through USE again at higher altitude. [PLANNED]
- **Retroactive listeners** (A7 §4): free play that genuinely produces a mission's state
  ticks it complete — re-traversal counts, the curriculum watches without gating. [PLANNED]
- **Micro-re-traversal is already live:** NEW markers and recall-on-open (A2 §4) pull the
  eye back one session later; bestiary rot alerts are unscheduled review of the
  fuel-decays lesson. [BUILT / partially PLANNED]
- **The final re-traversal is the exam:** the Act VI prediction gauntlet — no new content,
  only old elements behaving and the player calling it in advance. Passing it is OWN-tell
  certified for the whole table. [PLANNED]

---

## 6. Governance and open decisions

Binding: this chapter yields to A2_TEACHING.md (pedagogy law) and 03_PROGRESSION.md
(thresholds); its tables yield to `aea_elements.js` on disk. A new element entering the
codex must receive a path row here before its mission is authored; a mission that cannot
name its station in §2 does not ship. The ladder canon is recorded here and in BOOK.md.

| # | decision | recommendation |
|---|---|---|
| D-P1 | when the bench opens | immediately after M1.5 with a two-part trivial construct (TAP + SCORER, one click, one visible run — R1 finding 10), amending A7 §4's gate table; the alternative (Act II, with CONSTRUCT) delays the core creative act one full act |
| D-P2 | station chips on the codex detail screen | ship with the bench — E/U data already exists; four chips, two inks, no new screen |
| D-P3 | OWN-tell instrument | prediction ledger as the Phase A proxy, certificate at the gauntlet; a separate TELL beat risks quiz UI against A2 §4's diegetic law |

---

## Changelog

- 2026-07-20 — v1. Authored from `../aea_elements.js` (29 rows), A2_TEACHING.md §3,
  A8_AEA_ALIGNMENT.md, 03_PROGRESSION.md, R1_EVIDENCE.md, A7_BUILD_LAYER.md, and mission
  ids from 05/05B/05C. Four-station grammar defined; full 29 x 4 table with Phase A
  ceilings (census: U built 11/29, USE 0/29, OWN-run 14 full + 5 partial); the assistant
  ladder recorded as canon (ground + five rungs, capability statements, proof moments,
  part-pool climb); seed.9 crossing table; the honest hookshot and the re-entry law;
  D-P1..D-P3 opened.
