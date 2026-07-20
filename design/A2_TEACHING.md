# A2_TEACHING — PART I · THE TEACHING DESIGN

```
doc:          A2_TEACHING.md (THE PROBE design book, top-of-book)
owner:        the game team (Portal-school master seat of the four-master fusion, 00_VISION.md §3)
status:       ACTIVE — pedagogy law; governs mission authoring in every act
last-updated: 2026-07-20
book role:    PART I, top-of-book. Lower chapters (01_WORLD.md, 09_PRODUCTION.md, the mission
              and UI chapters as they land) derive from this chapter and may not contradict it.
ground truth: ../aea_elements.js (codex + discovers wiring) · ../missions.js (Acts 0–I, beat
              kinds live) · ../GAME_PLAN.md (acts, teaches-map, tech tree) · ../journey_save.json
siblings:     00_VISION.md (root vision — this chapter is its §2.2 pillar expanded into law) ·
              01_WORLD.md (light-as-knowledge, the city as diagram) · 09_PRODUCTION.md
              (playtest evidence that the pedagogy ran)
marks:        [BUILT] verified in code on disk · [PLANNED] designed, not built ·
              [DECISION-LUIS] awaiting his call
```

The game IS a curriculum. This chapter is the pedagogy bible: what the player must be able to
DO afterward, the method every mission obeys, the full concept-to-mission map, how review
happens, how understanding is examined, and the one meta-lesson everything converges on. The
AEA honesty law applies to the teaching itself: nothing is taught with fake data, no claim
exceeds "measured functional correlate, present", and an exam that cannot be failed is not an
exam.

---

## 1. The thesis — learning outcomes as capabilities

`[BUILT as intent — 00_VISION.md §6.2; measured per act as acts land]`

After finishing THE PROBE, the player can build their own AEA assistant. Not "understands
agents" — CAN BUILD. Outcomes are stated as capabilities because knowledge that cannot act is
not the product. The player who completes the game can:

1. Make a raw model call with nothing but an HTTP POST — and knows that everything above that
   call is architecture, not magic. (Act 0)
2. Stand up a multi-provider grid behind ONE protocol function, where adding a plant is one
   registry line. (Act I)
3. Budget free-tier capacity — sliding rpm windows, daily quotas, shared file-locked state —
   so an unattended system never browns out. (Act I)
4. Build a fall-through ladder so that no component of the mind ever names a model. (Act I)
5. Wire persistent memory: one run writes a capsule, a later run reconstitutes it and thinks
   from it. (Act II)
6. Choose solo vs council FROM THE TASK, and justify the choice with measured regimes, not
   vibes. (Act III)
7. Gate outputs with a strict-schema verifier on a DIFFERENT model than the worker — and name
   why a lone verifier is a risk. (Act III, re-examined at Act V)
8. Give the mind real hands — external tools — inside a governance membrane, with a hard
   privacy boundary that never routes private data to a trains-zone plant. (Acts II/IV)
9. Ship a real external artifact through the system and know what "done" means when a gate,
   not a feeling, decides. (Act V)
10. Make the system improve itself: crystallize repeated behaviour into tools, version skills
    across runs, detect its own ceiling and escalate. (Act VI)
11. Classify what they built honestly: cited thresholds, measured functional correlates, never
    "conscious". The claim ceiling is itself a taught capability. (every act)

Phase A measures this thesis on player one: Luis finishing the game is the first demonstration
that the AEA can be learned from inside (00_VISION.md §4). Phase B generalizes it, after the
gate.

---

## 2. The Portal-school method — law

`[BUILT — the four-phase arc is live in the missions.js beat grammar; law for all acts]`

Every mission is INTRODUCE -> PRACTICE -> TWIST -> PROVE. The mapping to beat kinds is exact
and binding:

- **INTRODUCE — the machine demonstrates.** `brief` (why, three lines maximum) + `learn`
  (REAL code from the real file, typewriter reveal, one annotation line). Never pseudocode,
  never a diagram standing in for the thing — the code that runs is the code shown
  (M0.1 shows the entire protocol; M1.3 shows `Meter.can_spend` as it exists on disk).
- **PRACTICE — the player does.** `do`: a real endpoint action the player flies to and fires.
  M0.1's transmit is a live keyless call; M1.5's drill is four real draws through the mouth.
  Nothing is read that can be done (00_VISION.md §2.2).
- **TWIST — it breaks honestly.** The break is never scripted. The game ARRANGES a real
  encounter with a real limit: M1.3 loads the actual 60s rpm window and makes the player wait
  it out ("patience is a resource the entity budgets for you"); M1.4's ladder can genuinely
  starve; every `prove` has a real fail branch with plain language ("a plant is cooling from
  a real 429"). A rod dies because rods really die (measured pool decay, GAME_PLAN.md §1),
  not because a timer fired.
- **PROVE — a real assert passes.** `prove`: an assertion against live state
  (`last_ok_text`, `plants_online`, `no_throttle`, `drill_clean`). The pass line carries the
  takeaway in one sentence. The fail line tells the truth and offers the retry.

**The twist-honesty corollary.** Because faking a failure is forbidden, TWIST availability
depends on live conditions. When the world refuses to break (all rods healthy, windows clear),
the mission passes clean and the twist is deferred to the act boss — which stresses the system
hard enough to surface real failure. `[PLANNED]` Opportunistic twists: when `model_fitness.json`
shows a genuinely degrading rod, a mission may deliberately route a draw through it so the
player watches a real fall-through. Real, opportunistic, never fabricated.

**Audit (honest):** Act 0–I twists are induced-limit (the meter) and possible-starvation (the
ladder). No mission yet guarantees a rod death on cue, and none ever will — that is the law
holding, not a gap to fix with simulation.

---

## 3. One concept per mission — and the curriculum map

`[BUILT for Acts 0–I · PLANNED for Acts II–VI]`

**The law.** Each mission teaches exactly ONE concept. A mission may REVEAL more than one codex
node (the map's SENSED promotion shows redacted neighbors by design), but its brief, learn, do,
and prove all serve a single teachable idea. If a mission needs two learn-beats about two
different organs, it is two missions.

**The curriculum map.** The AEA is the curriculum; the city is the syllabus. Source of truth:
`aea_elements.js` `discovers` (Acts 0–I wired) plus its Act II+ comment and GAME_PLAN.md §4.
Mechanics nodes (CRYSTALLIZE / FLEXIBILIZE / SELF-VERSION / CEILING-DETECT) discover with
their seed and are not separate rows.

| AEA element | name | mission | act | state |
|---|---|---|---|---|
| seed.1 | SUBSTRATE | M0.1 FIRST LIGHT | 0 | [BUILT, played] |
| seed.9 | BOUNDARY | M1.1 THE CATALOGUE | I | [BUILT] |
| seed.2 | SHARP OBJECTIVE | M1.1 THE CATALOGUE (co-discovered) | I | [BUILT — see audit] |
| axis.R | PROMPTING | M1.2 THE CHANNEL | I | [BUILT — see audit] |
| seed.7 (+mech.ceiling) | CEILING-DETECT | M1.3 THE METER | I | [BUILT] |
| verb.observe | OBSERVE | M1.3 THE METER | I | [BUILT] |
| seed.4 (+mech.flexibilize) | FLEXIBILIZE | M1.4 THE LADDER | I | [BUILT] |
| verb.propagate | PROPAGATE | M1.4 THE LADDER | I | [BUILT] |
| pr.coherence | RESTORABLE COHERENCE | M1.5 BOSS · BROWNOUT DRILL | I | [BUILT] |
| seed.10 | BACKWARDS CHANNEL | the recall forge (mine -> Book -> recall/B2, GWT-3 cite) | II | [PLANNED] |
| axis.A | ABSTRACTION | UNASSIGNED — see coverage audit | II (recommended) | [DECISION-LUIS] |
| axis.P | PATH | the think forge (D1) | III | [PLANNED] |
| axis.M | MULTIPLICITY | the council mission | III | [PLANNED] |
| verb.compose | COMPOSE | the think forge | III | [PLANNED] |
| op.design | DESIGN | the think forge (proof PARTIAL — lands with think) | III | [PLANNED] |
| op.time | TIME | the think forge (per-tick stamps owed) | III | [PLANNED] |
| op.learn | LEARN | the pathfinder mission (THE CRYSTAL PATH doctrine) | III | [PLANNED] |
| doctrines (solo / council / verifier) | the regime map | the regimes missions | III | [PLANNED] |
| seed.8 | TRANSCENDENCE | the internet-wire / tools mission | IV | [PLANNED] |
| — | governance membrane (C3) | the command-current forge | IV | [PLANNED] |
| — | F1 senses | — | IV | [DECISION-LUIS] |
| op.ship | SHIP | THE SEND (convergence boss) | V | [PLANNED, pinned] |
| seed.3 (+mech.crystallize) | CRYSTALLIZE | the voyager mission | VI | [PLANNED] |
| seed.5 (+mech.selfversion) | SELF-VERSION | the voyager mission | VI | [PLANNED] |
| seed.6 | SELF-MODEL | reflect — already live; relearned as discovery | VI | [PLANNED] |
| axis.S | ASYNC | the ENDURANCE run (100-tick, temporal independence) | VI | [PLANNED] |
| pr.emergence | EMERGENCE OVER IMPOSITION | endgame | VI | [PLANNED] |
| pr.time | OPERATOR-OBSERVABLE TIME | endgame | VI | [PLANNED] |

**Coverage audit (filter-first, run against the 29-element codex):**

1. **axis.A has no mission.** ABSTRACTION ("memory grounding, tool use, writing new skills")
   appears in neither `discovers` nor the Act II+ comment. Recommendation, with the reason:
   wire it to the Act II recall forge — memory grounding is the first clause of its own line,
   and recall() is where grounding becomes real; seed.8 (tools) then re-encounters it in
   Act IV. One wiring line in `aea_elements.js`. `[DECISION-LUIS]`
2. **M1.1 discovers two seeds.** The taught concept is the registry and its privacy rings
   (seed.9). seed.2's teaching moment (falsifiable scorers) is thin in M1.1 — the concept gets
   its full treatment when the first boss threshold is read as a scorer. Acceptable as a
   reveal, flagged so no future mission repeats the pattern of discovering what it did not
   teach. `[BUILT, flagged]`
3. **M1.2 -> axis.R is a stretch.** THE CHANNEL teaches protocol-unity; axis.R's line is the
   prompting scaffold. The wiring stands (ground truth), but the scaffold lesson deserves an
   explicit re-encounter when recall-grounded prompting lands in Act II. `[BUILT, flagged]`

---

## 4. Spaced re-encounter — the review system

`[BUILT — map, codex, bestiary, doctrines live in PROBE OS; recall prompts partially planned]`

A concept met once is a concept lost. The review system is diegetic — the player reviews by
inhabiting, never by rereading:

- **The concentric map (M)** is the primary review surface. Discovery state derives from
  `journey_save.json`; a newly discovered element carries a NEW marker (amber — the live ink)
  that functions as a recall prompt: the marker draws the eye back to the concept one session
  after it was earned. Taught links draw only once their mission completes — the map slowly
  becomes the relational diagram of everything learned, in blue-gray structure ink. [BUILT]
- **SENSED promotion** shows redacted neighbors of the discovered — pre-exposure priming. The
  player has seen the shape of seed.10 long before Act II names it. [BUILT]
- **The bestiary (B)** re-encounters models incidentally: a model enters only via a real
  `tried[]` log, and its true fitness stats change between visits. Rot alerts are unscheduled
  review of the fuel-decays lesson. [BUILT]
- **The codex (K) and doctrines** are the consolidation layer: the six combination doctrines
  (`aea_elements.js`) unlock as their evidence is earned and are re-read as review of measured
  results, each carrying its evidence line. [BUILT — 2 unlocked, 4 locked]
- **The city itself** is the memory palace: light = knowledge earned (01_WORLD.md §1). Flying
  past the foundry IS reviewing Act I; the geography does the spacing for free. [BUILT]
- `[PLANNED]` **Recall-on-open:** opening the map onto a NEW marker shows the element's glyph
  first, its name a beat later — a one-second retrieval attempt before the answer, every time.
  Cheap, diegetic, no quiz UI.

---

## 5. Bosses as honest exams

`[BUILT for M1.5 · PLANNED thresholds cited per act]`

A boss is an exam, and an exam that cannot be failed teaches nothing. Boss law:

1. **The threshold is cited on the card before the attempt.** Every boss names its source:
   drill_clean (Act I, live) · recall/B2 with the GWT-3 citation (Act II) · think/D1 with
   GWT-2/4 (Act III) · THE SEND, HADES-fit + Luis sends (Act V) · STOP at >=3 rounds,
   ENDURANCE 100-tick to Bedau Class 2, the Darwin-Godel archive (Act VI).
2. **Failure is real and stated plainly.** M1.5's fail line: "the grid is weaker than it
   claims today." HADES holds junk at a 0.5 rate today (GAME_PLAN.md §1) — bosses can
   genuinely be lost, because the gate genuinely rejects.
3. **Retakes are free; thresholds never lower.** No rubber-banding, no pity-pass, no second
   phrasing of the assert that passes easier. The player retries against the same cited bar.
4. **THE SEND has an external examiner.** The Act V boss is a convergence exam: the entity
   drafts real outreach, HADES fits it, LUIS sends it. The game cannot grade this one alone —
   by design (00_VISION.md §7.1, pinned).
5. **The claim ceiling binds exam language.** A passed boss certifies a measured functional
   correlate, present. No pass screen ever says more than the measurement supports.

---

## 6. The no-text-walls law

`[BUILT — Act 0–I complies; lint planned]`

If a paragraph is needed, the level is misdesigned. The fix is never better prose — it is a
better DO. Binding budgets, verified against missions.js:

- `brief` — three lines maximum. Every shipped brief complies.
- `learn` — real code plus ONE annotation line. The code teaches; the annotation aims the eye.
- `prove` — one pass line, one fail line. The pass line is the only place a takeaway may be
  stated in full.
- All mission text is terminal-voice: lowercase, terse, no lore dumps. Depth on demand goes
  through ASK LEYBER (`/talk`) — the entity explains from live state when ASKED, never as a
  forced scroll. The relief valve is why the budgets can be hard.
- `[PLANNED]` Mission lint: a script over `missions.js` failing any brief over three lines,
  any learn with more than one annotation, any beat text over budget. Authoring law becomes
  mechanical before Act II content lands.

---

## 7. How understanding is measured

`[BUILT: bosses + real asserts · PLANNED: prediction beats, later acts]`

Completion measures compliance; prediction measures understanding. From Act III on, missions
gain a `predict` beat: before the do-beat fires, the player commits to a prediction that live
truth will settle. Prediction beats work here because every answer is checkable against real
state — no answer key is authored, the system IS the key:

- "which plant will answer this draw?" — settled by the real `tried[]` routing history.
- "will the meter block a third draw inside the window?" — settled by `grid_state.json`.
- "solo or council for this task — and why?" — settled by a real run against the measured
  regime map (THE SOLO LAW vs THE DIVERSE COUNCIL, evidence lines in `aea_elements.js`).
- "why did the council beat the solo?" — the one that matters: the player must name model
  diversity, not temperature, or the doctrine was memorized, not understood.
- "will HADES hold this draft?" — Act V, the highest-stakes prediction in the game.

Wrong predictions cost nothing and are recorded in `journey_save.json` as a private learning
ledger — the record exists so re-encounter can target what the player actually got wrong.
`[PLANNED]` The Act VI endgame includes a prediction gauntlet: no new content, only the system
behaving and the player calling it in advance. Passing it is the measured form of outcome
capability — the player can predict the machine because the player could now build the machine.

---

## 8. The meta-lesson — models are fuel, the structure is the mind

`[BUILT as demonstration in Acts 0–I · the arc completes in Act VI]`

The model-agnostic law is the one lesson every act converges on, and it is DEMONSTRATED, never
preached. The demonstration ladder:

- **Act I, felt:** M1.2 fires the same prompt through three plants — different latencies, one
  protocol. M1.4's mouth never names a model; the tried-list is the real routing history of
  the player's own draw falling past dead rods.
- **The bestiary, ongoing:** fuel decays — measured pool 44 -> 29, perfect 7 -> 2
  (GAME_PLAN.md §1) — while the ladder that outlives every rotted rod keeps answering. The
  player watches the structure survive its fuel, repeatedly, on real data.
- **Act III, measured:** the regimes show structure decisions beating fuel decisions — a
  diverse council rescues what a bigger model does not (doc.council evidence: v3 net +3,
  0 damage; same-model ensembles did not rescue).
- **Act III, economized:** pathfinder searches once for the winning fuel per task-type, then
  the structure runs cheap forever (op.learn, THE CRYSTAL PATH).
- **Act VI, closed:** pr.emergence — the entity defines its own steps; no central controller,
  and no model anywhere in the mind's own text.

**The naming rule.** A principle may be named only in the beat that demonstrates it, never
before, and never as standalone lore. M1.1 is the template: the registry code shows model
names living in ONE data file, and only then does the annotation say "the mind never names a
model — that is what model-agnostic means." Statement is allowed as the caption of a
demonstration, never as its substitute.

---

## 9. Governance — what lower chapters derive from here

Binding on the rest of the book:

- The mission chapter authors every Act II–VI mission against §2 (the four-phase arc), §3
  (one concept, the map above), and §6 (text budgets). A mission that cannot state its one
  concept and its curriculum-map row does not get authored.
- The world chapter (01_WORLD.md) owes the review system its surfaces: reveals, fog, and
  emissives are pedagogy (spacing and recall), not decoration.
- The UI chapter renders NEW markers in amber (live ink) and taught links in blue-gray
  (structure ink) — the two-ink law carries the recall/structure distinction itself.
- 09_PRODUCTION.md records boss outcomes as playtest evidence, including losses. A production
  log with no failed boss attempts is evidence the exams are too soft, and triggers a
  threshold audit — not a celebration.
- Conflicts resolve upward: this chapter yields only to 00_VISION.md, and its §3 curriculum
  map yields only to `aea_elements.js` on disk (data outranks prose; a divergence is a bug in
  one of them, named and fixed, never left standing).

---

## Changelog

- 2026-07-20 — v1. Authored from `../aea_elements.js`, `../missions.js`, `../GAME_PLAN.md`
  ground truth. Curriculum map wired from `discovers` + the Act II+ comment; coverage audit
  found axis.A unassigned (flagged [DECISION-LUIS]) and two thin discovery wirings (flagged,
  kept). Prediction beats and mission lint entered as [PLANNED].
