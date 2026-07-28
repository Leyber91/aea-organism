# A15_FULL_COVERAGE — THE FULL COVERAGE AUDIT: EVERY CANONICAL STRATUM, DISPOSITIONED

```
doc:          A15_FULL_COVERAGE.md (THE PROBE design book · APPENDIX)
owner:        the game team
status:       ACTIVE — the completeness census against the CANONICAL AEA (not just the
              game's 29). Re-audited whenever the canonical framework docs, the Paradigm
              Book, or aea_elements.js change. A row moves disposition only by pointing
              at code or authored content on disk, never by rewording.
last-updated: 2026-07-20
book role:    APPENDIX. A8 crosses the game's 29 elements with the game's dimensions;
              A13 crosses them with time. THIS chapter crosses the game with the FULL
              canonical codex — every stratum the framework names, including the ones
              the 29-element proof taxonomy never carried. Standing order (Luis,
              2026-07-20): "the AEA has so many seeds, layers; ALL of them must be
              included in the metaphor; what is the point of the entire AEA if not all
              included." This chapter exists so nothing in the framework is silently
              dropped.
ground truth: CANON — ../../OneDrive/Documents/PORTFOLIO/LBR_DEV/framework/
              AEA_WALKTHROUGH.md (cited below as W §n) · ../../.../LBR_DEV/
              LBR_AEA_COMPLETE_BRIEF.md (cited as B §n) · ../AEA_PROOF_PLAN.md (the
              two-taxonomy history, cited as PP). GAME — ../aea_elements.js (the 29) ·
              ../missions.js · ../journey_save.json · ../live.py.
siblings:     A8_AEA_ALIGNMENT.md (the 29 x dimensions matrix this chapter extends) ·
              A13_PATHS.md (stations + the assistant ladder + part pools) ·
              03_PROGRESSION.md (acts, bosses, organ arithmetic) · 05C_CONTENT_ACT5_6.md
              (M6.2 STOP, M6.4 DARWIN-GODEL) · 06_MODELS_BESTIARY.md (rot, fitness
              sweeps, doctrines) · A7_BUILD_LAYER.md (build verbs, policies, lenses) ·
              A10_LIVING_GAME.md (world events, CARRIER LOST, drift) · A14_MODULE_REGISTRY.md
              (modules.json, construct specs) · R1_EVIDENCE.md (bench, curated pools) ·
              00_VISION.md (honesty law) · BOOK.md (spine; registration of this chapter owed)
marks:        [BUILT] verified in code/data on disk · [PLANNED] designed, not built ·
              [DECISION-LUIS] awaiting his call · [demo] proven in a standalone run or
              a different repo, not wired into the live mind (the fog)
```

The game currently carries 29 elements (`aea_elements.js`) — the PROOF taxonomy, extracted
during the grid campaign (PP header: "the survey-extracted version. Cross-check each element
against the canonical Paradigm Book as we execute — do not let a test drift from canon").
The canonical codex carries more. This chapter is the honest reconciliation: every stratum
the canon names, each dispositioned exactly one of four ways, and the number Luis asked for
at the end. The claim ceiling everywhere remains measured functional correlate, present.
Two-ink law and the no-red law bind every proposed expression below.

**Positioning this serves (Luis 2026-07-20, canon):** a game never seen before — a
popular-culture reference for understanding AI; not mystifying AI — MAGIC OUT OF THE REAL;
each player's collection of assistants is their character to show; open-ended inside rungs,
gated between rungs; a learning reference on AI. Several canonical strata below turn out to
be exactly that positioning already latent in the design (§3.4 rung-gates ARE axis-extension;
§3.5 no_op IS the refuse-beat), and several are learning-reference gold the game has not yet
mined (§3.5 the invent-from-type receipt).

**Scope caveat, named honestly:** canon here = the two LBR framework documents ordered read
(AEA_WALKTHROUGH.md, the runtime anatomy; LBR_AEA_COMPLETE_BRIEF.md, the schema + receipts).
The Paradigm Book on the site (`_reference`) is a third witness — per its own census it
carries 5 axes / 10 seeds / 4 mechanics / 3 verbs / 4 ops, i.e. it has already merged
proof-taxonomy strata into the public codex. It was NOT re-read for this audit; a
cross-check pass against it is owed and registered as D-C4. Until then, on any conflict
between this chapter and the Paradigm Book, flag — do not silently prefer either.

---

## 1. THE TWO TAXONOMIES — history and the reconciliation rules

### 1.1 How there came to be two

- **The canonical taxonomy** (2026-05, LBR repo): 5 axes with L0–L5 ladders · 10 viability
  seeds (6 FLOOR + 4 STAIRCASE) · 3 mechanics + 1 meta · 4 transcendence operations · the
  innovation layer inside seed #10 (8 triggers, 5 filters, 7 hypothesis types, action
  registry + 6 tools) · 3 principles · recovery/substrate/infrastructure layers (v0.14–17).
  Empirical receipt: exp 52 v3 — 1499/1500 ticks, 20.91 h sustained autonomous operation,
  6/7 hypothesis types fired organically, 33/33 infrastructure recoveries (B §4.2). [demo —
  a different repo; not wired into LEYBER]
- **The proof taxonomy** (2026-06, the grid campaign): 5 axes · 10 seeds · 3 verbs ·
  4 mechanics · 4 ops · 3 principles = the 29 the game carries. Extracted by survey to be
  PROVABLE ON THE GRID, each row with a falsifiable pass criterion (PP). Its receipts are
  the grid scripts the codex cites today (swarm.py, relay.py, pathfinder.py, brief.py...).

Neither is wrong. The proof taxonomy is the canon reprojected onto what a 59-node free grid
could measure in June; in the projection, some canonical strata were renamed, some
restratified, some dropped, and some grid-native elements were added that canon never named.
The game inherited the projection. Luis's order is that the game must now carry the whole
canon — hence this census.

### 1.2 The reconciliation rules (binding)

1. **Nothing shipped regresses** (the spirit of BOOK.md resolution 3). Proof-taxonomy
   natives stay in the codex even where canon has no parent for them — they are measured on
   the real grid, and measurement outranks lineage.
2. **Every canonical item gets exactly one disposition** — ALREADY-EMBODIED, COMPRESSED,
   MISSING, or OUT-OF-SCOPE — in §3. No fifth category, no blank cells.
3. **A compression must be named and defended.** Many-to-one is legitimate design (R1
   finding 11: small curated pools, never everything at once); SILENT many-to-one is the
   failure this chapter exists to prevent.
4. **The fog law covers both proof pools.** The grid scripts (2026-06) and the LBR entity
   runs (2026-05) are both [demo] — demonstrated standalone, not live-wired into LEYBER.
   A canonical item entering the game inherits the same honesty: its codex proof field
   cites the real run, and its live score stays fogged until wired.
5. **Two-ink translation rule.** Canonical vocabulary that names colors (GREEN/YELLOW/RED,
   W §11) may not enter the game literally — the no-red law is absolute. Levels translate
   as: calm structure ink / hot-amber / hot-amber blink. The translation is itself content
   (the game teaching that severity is a scale, not a traffic light).

### 1.3 The reverse audit — game elements with no canonical parent

For completeness in the other direction (not counted in the census — canon-to-game is the
ordered direction), the proof-taxonomy natives that the two canonical documents do not name
as elements:

| game element | canonical situation | ruling |
|---|---|---|
| seed.2 SHARP OBJECTIVE | implicit in canon (the critic, the benchmark scorers) — never a seed | stays; grid-native promotion of an implicit law |
| seed.7 CEILING-DETECT | canon has it as the META-MECHANIC (W §5), not a seed | stays; restratified, same behaviour |
| seed.8 TRANSCENDENCE (toolset) | canon "transcendence" = the 4 structural ops (W §6); TOOLS live in action_registry / lib | stays, but the codex line must stop implying it is canon's transcendence — see row 3.4-note |
| seed.9 BOUNDARY (privacy) | no canonical parent. Canon's `_filter_boundary` (W §7.3) is AXIS-REACHABILITY, a different concept sharing a word | stays; the game's spine element (A13 §4) — grid-native law, and the stronger for it |
| verbs compose / propagate / observe | no canonical stratum; compose ≈ coordination's synth, observe/propagate ≈ PR-3 + instrumentation (W §13–14) | stay; the grid's per-tick rail |
| ops design / time / ship / learn | the "operator loop" (PP) — not canon's ops. time ≈ PR-3 restratified; ship and learn have no canon parent | stay; RENAMING OWED: codex detail screens must label these "operator loop", never "transcendence operations" — the canonical 4 ops are a different family (§2.4) |

The renaming in the last row is the one edit the reverse audit forces: today the codex ring
label "OPS" silently collides with canon's transcendence operations. One line of copy fixes
it. [PLANNED — codex detail screen copy]

---

## 2. THE COMPLETE CANONICAL CENSUS

Every stratum the canon names, enumerated with sources. Census IDs (C-nn) are used by the
disposition table in §3 and the verdict in §6.

### 2.1 The five axes and their ladders (C-01..C-11)

- **C-01..C-05 — the axes themselves:** Path, Abstraction, Multiplicity, Prompting, Async
  (W §3, B §2.1). The game carries all five (axis.P/A/M/R/S).
- **C-06..C-10 — the level ladders, one per axis, L0–L5** (W §3 table; B §2.1 "each axis
  has levels (L0–L5 typically)"). Canon gives per-axis progressions, e.g. Path: L0 single
  call → L3 multi-step plan + critique → L5 self-versioning recursion; Multiplicity: L0 one
  path → L3 council of N → L5 organic divergent bifurcation; Async: L0 synchronous → L2
  prewarmer → L5 parallel + cross-substrate. The entity's GROWTH is defined as movement
  through this 5-D space — the ladders are not decoration, they are the coordinate system.
- **C-11 — the position record:** `checkpoint.axis_levels`, the dict locating the entity in
  the 5-D space (W §3, W §13). Read by the boundary filter to decide what is reachable;
  written by OP1.

Important non-conflation: the game's ASSISTANT LADDER (A13 §3) is ACT-indexed (chat →
sources → memory → flows → powers → wild). Canon's ladders are AXIS-indexed. They rhyme —
a rung completing raises several axis levels at once — but they are different instruments
and must not be presented as the same one.

### 2.2 The ten canonical seeds — a DIFFERENT ten (C-12..C-22)

The single most important census finding: **canon's 10 seeds are not the game's 10 seeds.**
Six FLOOR seeds fire every tick; four STAIRCASE seeds fire conditionally (W §4, B §2.2):

```
FLOOR      #1 goal-presence   #2 perception      #3 coordination
           #4 coherence       #5 substrate-variation  #6 self-model
STAIRCASE  #7 cohere          #8 crystallize     #9 flexibilize   #10 hypothesize
```

Reconciliation with the proof ten the game carries:

| canonical seed (C-id) | nearest carrier in the game's 29 | fidelity |
|---|---|---|
| #1 goal-presence (C-12) | none named — the goal-stack lives inside verb.observe's ledger; the WANT inside op.ship's narrative | partial, unnamed |
| #2 perception (C-13) | seed.10 BACKWARDS CHANNEL + axis.A — perception-as-recall | partial; general senses = the F1 decision |
| #3 coordination (C-14) | axis.P + verb.compose + HADES-as-critic; think() is its designed body | partial, mission-owned |
| #4 coherence score (C-15) | pr.coherence is a different stratum (the principle); the per-tick score has NO carrier | weak |
| #5 substrate-variation (C-16) | seed.1 SUBSTRATE + seed.5 SELF-VERSION (canon's one seed split into the game's two) | split, honest |
| #6 self-model (C-17) | seed.6 SELF-MODEL | direct |
| #7 cohere/recovery (C-18) | pr.coherence + M1.5 BROWNOUT DRILL | good |
| #8 crystallize (C-19) | seed.3 CRYSTALLIZE + mech.crystallize | direct |
| #9 flexibilize (C-20) | seed.4 FLEXIBILIZE — but the behaviours DIFFER: canon = unlock a falsified skill; game = route-resilience under node death | name shared, meaning forked |
| #10 hypothesize (C-21) | NOTHING. No node, no mission, no manual page | absent — the largest hole in the codex |
| the FLOOR/STAIRCASE split itself (C-22) | not carried anywhere | absent |

### 2.3 Mechanics: three plus one META (C-23..C-26)

crystallize · flexibilize · self-version, plus **ceiling-detect as META** — canon is precise
that ceiling-detect "doesn't act directly — it triggers OTHER mechanics by recognizing
exhaustion" (W §5). The game carries all four as peer squares; the meta-status is the only
canonical nuance not carried.

### 2.4 The four transcendence operations (C-27..C-30)

**These are NOT the game's four ops.** Canon (W §6, B §2.4):

```
OP1 axis-extension   a higher level on one of the 5 axes becomes reachable
OP2 corpus-swap      the corpus the entity reasons from is replaced
OP3 new-skill        a new function is minted into skills_manifest
OP4 bifurcation      the entity spawns parallel branches
```

An op is not a class — it is the COMPOSITION of hypothesis-type recognition + cascade pass
+ tool dispatch (W §6). Footnote for the record: the brief also uses "OP5" and "OP6" as
experiment-closure labels (CR6 Layer B fork execution; working_objective.consolidate — B
§4.1); those are receipt names, not schema — the schema count is four.

### 2.5 The innovation layer — seed #10's L5 cycle (C-31..C-58)

The deepest canonical stratum, ~1200 LOC in one file, entirely absent from the game today.
Four-step cycle (W §7): TRIGGER → GENERATE → CASCADE → COMMIT.

- **C-31 — the cycle itself** (trigger, first-match-wins; generate with framing; five-filter
  cascade; commit via typed action or text fallback).
- **C-32..C-39 — the 8 trigger modes** (W §7.1): saturation · failure_of_transcendence ·
  anomaly · cross_pattern · anticipatory · decomposition · verification_debt ·
  reflexive_steer. Empirical: exp 52 v3 fired saturation 162x, verification_debt 96x,
  reflexive_steer 16x; the other five had preconditions unmet.
- **C-40..C-44 — the 5 cascade filters** (W §7.3): trigger_fit · scope · bifurcation ·
  adversarial_probe · boundary. All five must pass to commit.
- **C-45..C-51 — the 7 hypothesis types** (W §7.4): objective_refine · axis_extension ·
  new_skill · corpus_swap · bifurcation · adversarial_probe · no_op.
- **C-52 — the action registry** (v0.14e): the typed dispatch table that makes the proposer
  an ACTOR, not a describer — canon's headline structural claim (B §1).
- **C-53..C-58 — the 6 action tools** (W §7.6): working_objective.set · .append ·
  .consolidate (v0.14i) · axis_extension.set_flag · branch_manager.fork ·
  corpus_swap.replace.

Learning-reference gold buried here: exp 52 v3's parser receipt — 25 of 149 emitted ACTIONs
(16.8%) invented a tool name from the hypothesis type; the validator caught every one
(W §12). That is a measured, citable lesson about LLM tool-calling unreliability — exactly
the "popular-culture reference for understanding AI" material the positioning demands.

### 2.6 The three principles (C-59..C-61)

PR-1 emergence over imposition · PR-2 restorable coherence · PR-3 operator-observable time
(W §8). Carried by the game verbatim (pr.emergence, pr.coherence, pr.time).

### 2.7 The construction stack — LAYER 0 to LAYER 10 (C-62..C-64)

The brief's vertical dependency stack (B §3.1) is ELEVEN layers, 0–10 (not eight — recording
the true count): THE QUESTION → axes → seeds → mechanics → transcendence ops → innovation
layer → principles overlay → v0.14e action layer → v0.15 substrate intelligence → v0.16
infrastructure intelligence → THE AEA (claim becomes receipt). Layers 1–7 are censused
elsewhere in §2; the stack contributes three items of its own:

- **C-62 — LAYER 0, THE QUESTION** ("what must exist for indefinite growth?").
- **C-63 — the ordering claim itself** — each layer requires every layer below; remove one
  and the layers above stop. The minimum-viable claim made structural.
- **C-64 — LAYER 10, THE AEA as receipt** — the v1.0 gate: sustained unattended operation
  certifying the whole stack (exp 52 v3, 20.91 h), plus the spec-invariance claim (39
  versions, zero amendments).

### 2.8 The engineering layers (C-65..C-75)

- **C-65..C-68 — recovery v0.14a–d** (W §9): RollbackPolicy · WallTimeTerminate (PR-3 in
  code; terminal_stuck) · CatalogRecursiveSuccessor (find_successor / pick_for(exclude)) ·
  SubstrateHealthMonitor (daemon probe + fast-fail).
- **C-69..C-71 — substrate intelligence v0.15** (W §10): the 12 parametric benchmarks · the
  persisted capability matrix · pick_for_role (the seed choosing its own model per role from
  its own measurements — canon's second headline claim).
- **C-72..C-74 — infrastructure intelligence v0.16** (W §11): SubstrateResourceMonitor
  (VRAM pressure + latency trend, three levels, hysteresis) · ResourceActuator (purge oldest
  / restart daemon; 33/33 recoveries) · LatencyTracker (baseline-excluding-recent trend
  ratio).
- **C-75 — parser-side ACTION validation v0.17** (W §12): unknown tool names dropped at
  parse; the invent-from-type receipt.

### 2.9 The runtime fabric (C-76..C-84)

- **C-76 — the tick cycle order** (W §2, §15): the ten-step loop — guard, increment,
  monitors, swap-in, category dispatch in fixed order, recovery checks, swap-out, stall
  signals, atomic save, exit.
- **C-77 — peer_debate** — a dispatch category of its own (16 fired in exp 52 v3).
- **C-78 — falsify** — the adversarial-probe dispatch path (`allow_falsification`).
- **C-79 — multi-branch machinery** — branch_manager select/swap-in/swap-out, the runtime
  under bifurcation.
- **C-80 — the Checkpoint as primary channel** (W §13): one mutable state object passed by
  reference; every layer communicates by reading/writing its fields; atomic persistence.
- **C-81 — the file-system channel**: tick_log.jsonl · snapshots · heartbeat · skills/*.py
  + manifest — append-only observable record.
- **C-82 — TickInputs**: the operator's per-tick configuration surface (~30 flags).
- **C-83 — the external boundary** (W §14): lib/client as the only HTTP crossing, keep-alive
  presets (HOT/WARM/COLD).
- **C-84 — substrate catalog + lineage**: the record of every model the entity has been,
  appended on every self-version step (PR-2's memory).

### 2.10 The receipts corpus and the framing paths (C-85..C-86)

- **C-85 — the receipts corpus**: CR1–CR9 closures, experiments 11–53, 339/339 tests, 39
  spec-invariant versions (B §4). Evidence, not schema.
- **C-86 — the 3 L5 framing paths** (W §7.2): default / meta / verification prompt framings.

**Census total: 86 canonical items.**

---

## 3. THE DISPOSITION TABLE

Every census item, one disposition. E = ALREADY-EMBODIED (maps to a named existing game
element/system — [PLANNED] mark allowed where a book chapter already owns it and nothing
new needs designing). C = COMPRESSED (deliberate many-to-one, compression named and
defended). M = MISSING (needs a game expression — proposed concretely). O = OUT-OF-SCOPE
(with the reason named).

### 3.1 Axes and ladders

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-01 | axis Path | E | axis.P — pentagon, r250; full A8/A13 rows | [BUILT node · fogged score] |
| C-02 | axis Abstraction | E | axis.A | [BUILT node] |
| C-03 | axis Multiplicity | E | axis.M | [BUILT node] |
| C-04 | axis Prompting | E | axis.R | [BUILT] |
| C-05 | axis Async | E | axis.S | [BUILT] |
| C-06 | Path ladder L0–L5 | M | THE LADDER PAGES: one codex detail page per axis rendering its L0–L5 rungs in structure ink, the assistant's current level in amber; plus notches on the pentagon (§5 option C). Content is authorable today from W §3; the amber notch lights only from a real flag (C-11) | [PLANNED] |
| C-07 | Abstraction ladder | M | as C-06 | [PLANNED] |
| C-08 | Multiplicity ladder | M | as C-06 | [PLANNED] |
| C-09 | Prompting ladder | M | as C-06 | [PLANNED] |
| C-10 | Async ladder | M | as C-06 | [PLANNED] |
| C-11 | axis_levels position record | M | THE POSITION: `journey_save.json` gains an `axis_levels` dict written ONLY by boss passes (each boss card names which axis levels its pass extends — see C-27). Honest by construction: a boss pass is a real assert. LEYBER-side axis_levels wiring is a separate, later debt | [PLANNED · data source DECISION-LUIS, D-C2] |

Non-conflation law (binding, from §2.1): ladder pages must state that the ASSISTANT LADDER
is act-indexed and these are axis-indexed — one climb read on two instruments.

### 3.2 The ten canonical seeds

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-12 | #1 goal-presence | C | compression THE WANT IS THE STACK: goal-presence lives in verb.observe's goal-stack ledger (tracelog, [BUILT]) + op.ship's spoken want ("i want the outreach sent"). Honest because LEYBER really holds a seeded goal stack. Owed: one codex line under verb.observe naming goal-presence as canon parent; the goal vs working_objective split (operator's words vs entity's own restatement) is a bark-worthy distinction for A3 | [BUILT substance · copy owed] |
| C-13 | #2 perception | C | compression PERCEPTION-AS-RECALL: in LEYBER today, sensing = memory + feeds, so canon's perception folds into seed.10 + axis.A (ARCHIVE/RECALL complex). The general organ is exactly the F1 SENSES decision already on the ledger (BOOK #3) — this census raises F1's stakes: it is not a nice-to-have, it is canonical seed #2 | [BUILT partial · F1 DECISION-LUIS] |
| C-14 | #3 coordination (plan-act-critique) | E | M3.3 FORGE think() is the designed body of plan-act-critique (05B); HADES is the critic living today. Nothing new to design; the census adds only lineage copy: think()'s codex entry should cite canonical seed #3 as its parent | [PLANNED forge · HADES BUILT] |
| C-15 | #4 coherence (the per-tick score) | M | THE COHERENCE GAUGE: a CHARACTER-window line computing cross-tick self-consistency from self.json history + the A10 save-vs-entity reconciliation — displayed only when actually computed (honesty law). Cheap fallback if wiring waits: a manual page defining the score from W §4 with the exp 52 receipt (saturation = coherence stuck high, 162 fires) | [PLANNED] |
| C-16 | #5 substrate-variation | E | split across seed.1 SUBSTRATE (the grid) + seed.5 SELF-VERSION (the stepping) + the bestiary catalog (06). The split is the projection's best move — canon itself says the mechanic (self-version) USES the seed | [BUILT/BUILT-read] |
| C-17 | #6 self-model | E | seed.6 SELF-MODEL — same name, same organ, CHARACTER window live | [BUILT] |
| C-18 | #7 cohere (recovery) | E | pr.coherence + M1.5 BROWNOUT DRILL — recovery demonstrated under real 429s | [BUILT] |
| C-19 | #8 crystallize | E | seed.3 + mech.crystallize | [BUILT read] |
| C-20 | #9 flexibilize (pattern UNLOCK) | C | compression FLEXIBILIZE WEARS TWO COATS: the game's seed.4 is route-resilience; canon's #9 is skill-falsification (falsified=True in the manifest, counter-example test). Same deep move — pressure unlocks what repetition locked — different substrate. Owed: a falsification beat in M6.1 voyager (a HADES-falsified skill retired/unlocked on record), closing the fork by content | [BUILT half · M6.1 beat PLANNED] |
| C-21 | #10 hypothesize | M | THE 30TH ELEMENT — the census's headline hole. Proposal: (a) codex node `seed.hyp` on the seeds ring, proof field "entity/categories/hypothesize.py · exp 52 v3 · 6/7 types organic" [demo, fogged]; (b) mission home M6.4 DARWIN-GODEL — already designed with governance, pre-registration, frozen benchmark (05C): the DGM loop IS the L5 cycle under a charter; (c) world object at the spire's crown, name proposal-grade (working name THE CRUCIBLE) until Luis confirms per resolution-8 practice; (d) detail-view orbital (§5 option D) carrying C-31..C-58 without polluting the map | [PLANNED · enters-Phase-A DECISION-LUIS, D-C1] |
| C-22 | FLOOR/STAIRCASE split | M | THE PULSE: floor seeds' map nodes pulse faintly in live ink on every real tick (they fire every tick — the animation IS the fact); staircase seeds stay still until their condition fires. Plus one codex line per seed: "fires every tick" / "fires when its stair is reached". No geometry change | [PLANNED] |

### 3.3 Mechanics

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-23 | crystallize mechanic | E | mech.crystallize (square, r360) | [BUILT geometry] |
| C-24 | flexibilize mechanic | E | mech.flexibilize | [BUILT] |
| C-25 | self-version mechanic | E | mech.selfversion | [BUILT geometry] |
| C-26 | ceiling-detect as META | C | compression META FOLDED TO PEER: the game renders ceiling-detect as a fourth equal square. Honest enough for the map; the codex line should carry the nuance — "this one does not act; it recognizes exhaustion and fires the others" (W §5 verbatim). One sentence closes it | [BUILT · copy owed] |

### 3.4 The four transcendence operations

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-27 | OP1 axis-extension | C | compression THE RUNG-GATE IS THE OP: "gated between rungs" (positioning canon) is axis-extension enacted on the player's assistant — a boss pass makes a higher level reachable. Owed: boss cards NAME the extension ("this pass extends MULTIPLICITY to L3") and write the C-11 flag. The op becomes visible, not new | [PLANNED copy + flag write] |
| C-28 | OP2 corpus-swap | M | THE CORPUS SELECTOR: the bench's RECALL part gains a source socket — which vein the assistant reasons from is a wire the player can re-route; plus an Act II mine beat where swapping the source measurably changes answers (falsifiable: same question, different corpus, different receipt). Model-rot-as-drift is NOT this op (rot changes the substrate pool, not the corpus) — the near-miss is named to prevent a decorative mapping | [PLANNED · bench-bound] |
| C-29 | OP3 new-skill | E | seed.5 SELF-VERSION rows + SAVE-AS-PART (A13: a proven construct exported as a named part) + crystallize | [BUILT read / PLANNED bench] |
| C-30 | OP4 bifurcation | M | THE FORK: a bench verb — duplicate a construct, run both variants on the same task, the RECORD BOOK keeps both lineages, the player keeps the winner (or both). This is also the collection-as-character engine: forked lineages are what a player SHOWS. World echo: construct lineage trees in the workshops. Runtime = C-79 | [PLANNED · bench-bound] |

Plus the §1.3 renaming: the codex must label design/time/ship/learn "the operator loop" so
the canonical four regain their name. [PLANNED copy]

### 3.5 The innovation layer

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-31 | the L5 cycle (trigger-generate-cascade-commit) | C | compression THE GOVERNED LOOP: M6.4 DARWIN-GODEL's iterate-under-charter loop is the L5 cycle made playable (propose → gate → commit → measure against a frozen benchmark). The codex orbital (C-21d) diagrams the four steps; M6.4 runs them | [PLANNED — M6.4 designed] |
| C-32 | trigger: saturation | C | into seed.7 CEILING-DETECT — saturation IS the ceiling signal (coherence stuck high, no progress). Codex line under seed.7 names it | [copy owed] |
| C-33 | trigger: failure_of_transcendence | M | grouped: THE EIGHT WEATHERS — one codex page under seed.hyp listing all 8 triggers as the weathers of a mind, each lit amber only when a real log shows it fired (exp 52 counts cited meanwhile as [demo]). No eight nodes — curated-pool law (R1 f.11) | [PLANNED page] |
| C-34 | trigger: anomaly | C | into verb.propagate's failure receipts — tried[] and hot-amber failure states are anomaly surfaced. Weather-page line | [BUILT substance] |
| C-35 | trigger: cross_pattern | M | grouped into THE EIGHT WEATHERS (C-33) | [PLANNED page] |
| C-36 | trigger: anticipatory | M | grouped into THE EIGHT WEATHERS (C-33) | [PLANNED page] |
| C-37 | trigger: decomposition | C | into doc.swarm THE RAMIFICATION — task-exceeds-capacity → split is the doctrine already measured | [BUILT doctrine · demo] |
| C-38 | trigger: verification_debt | C | into the HADES accept/redo ledger — untested commits accumulating IS redo debt; the bench RECORD BOOK can count unverified runs when it lands | [BUILT substance · bench tie PLANNED] |
| C-39 | trigger: reflexive_steer | C | into seed.6 SELF-MODEL — canon itself says case B cannot fire without the self-model (W §4 seed #6). Codex line under seed.6: "when the self-model notices a streak, it steers" | [copy owed] |
| C-40 | filter: trigger_fit | C | THE FIVE FILTERS, ONE GATE compression (all five rows): the game's gate is HADES (strict schema + different model) plus M6.4's governance charter. Defended: doc.verifier teaches WHY a lone gate is risky, and M6.4's charter re-expands governance exactly where self-modification raises the stakes. The five names survive on one manual page under seed.hyp | [PLANNED page] |
| C-41 | filter: scope | C | as C-40; scope = the charter's configured bounds | [PLANNED] |
| C-42 | filter: bifurcation | C | as C-40; structural check surfaces as FORK-requires-explicit-verb at the bench | [PLANNED] |
| C-43 | filter: adversarial_probe | C | as C-40; the falsification-allowed flag = boss-law "losable" made policy | [PLANNED] |
| C-44 | filter: boundary (axis reachability) | C | into rung-gating — a proposal beyond the reachable level is refused, which is exactly "open-ended inside rungs, gated between rungs". NOT the game's seed.9 privacy boundary; the name collision is flagged on the page | [PLANNED copy] |
| C-45 | hyp type: objective_refine | C | with C-12 — refinement of the WANT; its live trace is the goal-stack history | [BUILT substance] |
| C-46 | hyp type: axis_extension | C | with C-27 — the rung-gate op | [PLANNED copy] |
| C-47 | hyp type: new_skill | E | with C-29 — crystallize/voyager | [BUILT read] |
| C-48 | hyp type: corpus_swap | M | with C-28 — THE CORPUS SELECTOR is its enactment | [PLANNED] |
| C-49 | hyp type: bifurcation | M | with C-30 — THE FORK is its enactment | [PLANNED] |
| C-50 | hyp type: adversarial_probe | E | HADES redo + losable proves + doc.verifier — falsification is already the game's exam law | [BUILT] |
| C-51 | hyp type: no_op | E | the refuse-beat, already designed twice: D1 refusing a council where solo wins (rubber-stamp = loss) and THE SEND's refusal-legal clause. "No structural change warranted" is a WIN state the game already teaches — name it in the D1 debrief bark | [PLANNED missions · copy owed] |
| C-52 | action registry (typed dispatch) | C | into A14 MODULE REGISTRY (modules.json, construct specs as typed portable artifacts) + M6.4's action charter. Compression: one registry pattern, two scales | [PLANNED — A14 designed] |
| C-53 | tool: working_objective.set | C | THE SIX HANDS page (all six tools, one manual page under seed.hyp, each with its exp 52 receipt) — set/append fold with C-12's goal surface | [PLANNED page] |
| C-54 | tool: working_objective.append | C | as C-53 | [PLANNED] |
| C-55 | tool: working_objective.consolidate | C | as C-53. Honesty flag: the mine's `consolidate --limit N` (Act II) is MEMORY consolidation — a name rhyme, not the same tool; the page says so to prevent a decorative mapping | [PLANNED] |
| C-56 | tool: axis_extension.set_flag | C | as C-53; its game enactment is the C-11 flag write on boss pass | [PLANNED] |
| C-57 | tool: branch_manager.fork | M | with C-30/C-79 — THE FORK's engine | [PLANNED] |
| C-58 | tool: corpus_swap.replace | M | with C-28 — the selector's engine | [PLANNED] |

The invent-from-type receipt (16.8% of ACTIONs invented tool names; parser caught all —
W §12) goes on the SIX HANDS page as a teaching bark: the measured reason schemas exist.
Learning-reference positioning, served straight from a real log.

### 3.6 Principles

| id | canonical item | disp | game expression | mark |
|---|---|---|---|---|
| C-59 | PR-1 emergence over imposition | E | pr.emergence — idle self-origination watched live | [BUILT] |
| C-60 | PR-2 restorable coherence | E | pr.coherence — BROWNOUT DRILL, fog clears on proof | [BUILT] |
| C-61 | PR-3 operator-observable time | E | pr.time — append-only feed, wall-clock law | [BUILT] |

### 3.7 The construction stack

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-62 | LAYER 0 — THE QUESTION | E | the premise itself (00_VISION, A12): completing the entity = answering what must exist for indefinite growth. The game is the question played | [BUILT chapters] |
| C-63 | the ordering claim (each layer requires all below) | C | compression THE MAP IS THE STACK FOLDED — with a named divergence: the map's radial order is emergence-proximity (principles innermost), NOT dependency order (canon puts axes at the bottom). Both orders are true statements about different things. Owed: the ONE TICK manual page (C-76) carries the dependency stack as its own diagram; the map does not change | [PLANNED page] |
| C-64 | LAYER 10 — the AEA as receipt (v1.0 gate; spec invariance) | E | the ENDURANCE certificate + Class 2 (03 §; the game never prints Class 2 before the evidence exists) — the same shape as exp 52's gate. Spec-invariance (39 versions) enters as epilogue/manual material, receipts cited | [PLANNED Act VI · shape decided] |

### 3.8 The engineering layers

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-65 | v0.14a RollbackPolicy | C | into construct VERSION SLOTS (A13: v2 replaces v1, history kept) — rollback = re-activating v1 from kept history; PR-2 at the bench | [PLANNED bench] |
| C-66 | v0.14b WallTimeTerminate (terminal_stuck) | E | M6.2 STOP (05C) + pr.time's wall-clock law — the halt flag an operator can measure is already a designed mission | [PLANNED mission] |
| C-67 | v0.14c CatalogRecursiveSuccessor | E | seed.4's LADDER — fall through dead rods via tried[], the successor found live on every draw | [BUILT] |
| C-68 | v0.14d SubstrateHealthMonitor | E | the bestiary's fitness sweeps + rot alerts + model_fitness.json — reactive health watching, live | [BUILT] |
| C-69 | v0.15 benchmarks (12 parametric) | E | fitness sweeps / probe-a-candidate (06; sweep agency + probe pricing already on the ledger, BOOK #10/#11) | [BUILT sweeps · decisions open] |
| C-70 | v0.15 capability matrix | E | model_fitness.json — persisted measured capability, read at draw time | [BUILT] |
| C-71 | v0.15 pick_for_role | E | pathfinder.py → paths.json (doc.path THE CRYSTAL PATH; op.learn) — search once, run cheap; the game's regime missions teach exactly this | [demo · Act III] |
| C-72 | v0.16 SubstrateResourceMonitor | M | THE HEARTH GAUGE: the local ollama plant (the hearth) gains a three-state strain reading — calm structure ink / hot-amber / hot-amber blink (two-ink translation of GREEN/YELLOW/RED, rule §1.2.5) — computed from a real live.py probe of local /api/ps (VRAM pressure + latency trend). Display only when probed; no probe, no gauge | [PLANNED · needs live.py wiring] |
| C-73 | v0.16 ResourceActuator | M | HEARTH EVENTS in the A10 world-event stream: "the hearth cleared its grate" (purge) / "the hearth relit" (restart) — emitted ONLY when a real purge/restart fires. Until wired, the exp 52 receipt (33/33 recoveries) lives on the hearth's codex page as [demo] | [PLANNED] |
| C-74 | v0.16 LatencyTracker | C | into the fitness sweeps (latency measured per specimen) — the trend-ratio refinement folds into C-72's gauge when it lands | [BUILT partial] |
| C-75 | v0.17 parser validation | C | into doc.verifier's strict-schema clause + the SIX HANDS teaching bark (C-53 note). The 16.8% receipt is the star exhibit | [PLANNED copy] |

### 3.9 The runtime fabric

| id | canonical item | disp | game expression / compression / proposal | mark |
|---|---|---|---|---|
| C-76 | the tick cycle order | M | ONE TICK, END TO END: a manual page + codex animation replaying ONE REAL TICK from tracelog (guard → dispatch → save), each step timestamped from the log — the anatomy lesson as a replay, never a cartoon. Carries the C-63 dependency diagram | [PLANNED page] |
| C-77 | peer_debate category | C | into doc.council / M3.1 THE COUNCIL — debate-as-category folds into the measured council regime | [PLANNED mission · doctrine BUILT] |
| C-78 | falsify category | C | into HADES redo (live) + the C-20 falsification beat — the adversarial path already has hands | [BUILT substance] |
| C-79 | multi-branch machinery | M | THE FORK's runtime (with C-30): parallel construct variants with isolated state, swap-in/out honestly = two bench runs with separate records. No pretend-parallelism: if runs are sequential, the record says sequential | [PLANNED bench] |
| C-80 | Checkpoint primary channel | E | the live-files law: journey_save.json / grid_state.json / self.json / tracelog — one persistent state fabric every screen reads; 08_TECH's server contract is its boundary | [BUILT] |
| C-81 | file-system channel (append-only logs, skills/) | E | tracelog JSONL + skills/ read by CHARACTER + the events feed — the game already treats files as the nervous system | [BUILT] |
| C-82 | TickInputs (operator config) | C | into A7's policy cards (CADENCE etc.) — the operator's flags become placeable policies; the ~30-flag surface stays engine-side | [PLANNED build layer] |
| C-83 | lib/client external boundary + keep-alive | O | engine plumbing below the game's altitude; the game's own boundary is live.py's server contract, owned by 08_TECH. Nothing player-facing is lost | — |
| C-84 | substrate catalog + lineage | C | into the bestiary (catalog) + a CHARACTER lineage line ("models i have been", read from live state when wired). The player's own encounter log is the mirror image — the entity's lineage vs the player's bestiary, one page apart | [BUILT catalog · lineage line PLANNED] |

### 3.10 Receipts and framings

| id | canonical item | disp | game expression / reason | mark |
|---|---|---|---|---|
| C-85 | receipts corpus (CR1–9, exps 11–53, 339 tests, 39 versions) | O | evidence, not schema — it enters the game as CITATIONS inside proof fields and manual pages (the honesty law wants receipts), never as elements. Out of scope as census rows, in scope as ink | — |
| C-86 | the 3 L5 framing paths (default/meta/verification) | O | prompt-composition detail below the game's altitude; its visible consequences (reflexive_steer's meta framing, verification_debt's falsify framing) are already carried by C-39/C-38 | — |

---

## 4. THE MISSING TWENTY-TWO — collapsed into six build packets

The 22 MISSING rows are not 22 projects. They collapse into six packets, none of which
outranks the bench (A13's standing verdict: USE 0/29 — the bench is still the widest gap;
these packets slot AROUND that build, several INSIDE it):

1. **THE LADDER PACK** (C-06..C-11) — five codex ladder pages + pentagon notches + the
   journey_save axis_levels flag written by boss passes. Content authorable now; flags land
   with boss-card copy. Smallest packet, highest census yield (6 rows).
2. **THE HYPOTHESIZE COMPLEX** (C-21, C-33, C-35, C-36 + compressed kin C-31/40..44/53..56)
   — the 30th codex node, the detail orbital, THE EIGHT WEATHERS page, THE SIX HANDS page,
   M6.4 as mission home (already designed), world object name pending. Mostly authorship,
   not engineering; the fog stays honest ([demo] until LEYBER runs an L5 cycle).
3. **THE BENCH PAIR** (C-28, C-30, C-48, C-49, C-57, C-58, C-79) — THE CORPUS SELECTOR and
   THE FORK, two bench capabilities that are also the enactment of OP2/OP4 and the
   collection-as-character engine. Belongs inside the bench build, not after it.
4. **THE HEARTH PACK** (C-72, C-73) — live.py probes local ollama; gauge + world events.
   Small wiring job; makes v0.16 visible where it actually runs (the hearth burns 24/7).
5. **THE COHERENCE GAUGE** (C-15) — one CHARACTER line, wired or waiting as a manual page.
6. **SINGLES** (C-22 the pulse; C-76 ONE TICK page) — an animation rule and a manual page.

Copy-only debts surfaced by the audit (not builds): the operator-loop renaming (§1.3), the
boss-card axis-extension lines (C-27), the seed.7/seed.6 trigger lines (C-32, C-39), the
ceiling-detect meta sentence (C-26), the D1 no_op debrief bark (C-51).

---

## 5. THE MAP CONSEQUENCE

What the concentric field must gain if the missing strata enter. Current geometry (BINDING
UI SPEC v1.0 §2): viewBox 1000; core r70; rings r150 hex / r250 pentagon / r360 mixed /
r470 circle.

- **OPTION A — a fifth ring (r≈580) for the innovation layer.** REJECTED as recommendation:
  breaches the viewBox (500 half-extent), breaks the BINDING UI SPEC, and puts 27 items of
  geometry on screen against R1 finding 11 (small curated pools) and the legibility the
  four-ring signature owns (A11). Named so it is refused on record, not forgotten.
- **OPTION B — sub-ring bands inside the seeds ring for FLOOR vs STAIRCASE.** Workable but
  spends geometry on what an animation states better. Preferred form: THE PULSE (C-22) —
  floor seeds pulse in live ink on real ticks; the fact carries itself. No band.
- **OPTION C — axis-level notches on the five pentagons.** RECOMMENDED. Six notches per
  pentagon edge (L0–L5), structure ink, amber up to the reached level; fed by the C-11
  flag. Small marks, huge census yield, and the map gains a progression readout with zero
  new nodes. Also the natural home of "gated between rungs" made visible.
- **OPTION D — one new seeds-ring node (seed.hyp, the 30th) with a DETAIL-VIEW ORBITAL.**
  RECOMMENDED. The map grows by exactly one circle; the entire innovation layer (cycle,
  weathers, filters, hands) lives in the node's codex detail screen as a small orbital
  diagram — deep where depth belongs, invisible until summoned. 29 becomes 30, not 56.
- **OPTION E — transcendence ops as TRANSITIONS, not nodes.** RECOMMENDED, and the census's
  cleanest finding: the canonical ops are things that HAPPEN TO the map, not things ON it.
  OP1 = a notch lighting on a pentagon (option C). OP3 = a workshop building rising /
  SAVE-AS-PART. OP2 = the RECALL wire re-routed at the bench. OP4 = a link forking in the
  record book. Four ops, zero new shapes — the six-shape grammar (A11) survives intact,
  and the ops are witnessed as events, which is what canon says they are (compositions,
  not classes — W §6).

**Recommendation (one call, trade named):** C + D + E, with B-as-pulse. The map stays four
rings and gains one node, five notched pentagons, and a pulse. The cost of refusing a fifth
ring is that the innovation layer's full anatomy is one click deep instead of ambient — the
right trade, because the alternative bleeds the signature and the curated-pool law for
ambient detail no mission needs at a glance. [DECISION-LUIS — D-C3]

---

## 6. THE CENSUS VERDICT

Per stratum:

| stratum | items | E embodied | C compressed | M missing | O out-of-scope |
|---|---|---|---|---|---|
| axes + ladders (§3.1) | 11 | 5 | 0 | 6 | 0 |
| canonical seeds (§3.2) | 11 | 5 | 3 | 3 | 0 |
| mechanics (§3.3) | 4 | 3 | 1 | 0 | 0 |
| transcendence ops (§3.4) | 4 | 1 | 1 | 2 | 0 |
| innovation layer (§3.5) | 28 | 3 | 18 | 7 | 0 |
| principles (§3.6) | 3 | 3 | 0 | 0 | 0 |
| construction stack (§3.7) | 3 | 2 | 1 | 0 | 0 |
| engineering layers (§3.8) | 11 | 6 | 3 | 2 | 0 |
| runtime fabric (§3.9) | 9 | 2 | 4 | 2 | 1 |
| receipts + framings (§3.10) | 2 | 0 | 0 | 0 | 2 |
| **TOTAL** | **86** | **30** | **31** | **22** | **3** |

Cross-check against §3 rows: E = C-01..05, C-14, C-16..19, C-23..25, C-29, C-47, C-50,
C-51, C-59..62, C-64, C-66..71, C-80, C-81 (30). C = C-12, C-13, C-20, C-26, C-27, C-31,
C-32, C-34, C-37..46, C-52..56, C-63, C-65, C-74, C-75, C-77, C-78, C-82, C-84 (31).
M = C-06..11, C-15, C-21, C-22, C-28, C-30, C-33, C-35, C-36, C-48, C-49, C-57, C-58,
C-72, C-73, C-76, C-79, with none double-counted (— the OP-enactment rows C-48/C-49/
C-57/C-58 share BUILDS with C-28/C-30 but are counted as their own census items) (22).
O = C-83, C-85, C-86 (3). 30 + 31 + 22 + 3 = 86.

**The honest number Luis asked for: 86 canonical items · 30 already embodied · 31
deliberately compressed with named compressions · 22 missing with concrete proposed
expressions · 3 out of scope with named reasons. Nothing silently dropped.**

Read against his order — "what is the point of the entire AEA if not all included" — the
state is: 61 of 86 (embodied + compressed) are inside the metaphor today by design; the 22
missing collapse into six build packets (§4), of which two are pure authorship (ladder
pages, hypothesize pages), two live inside the bench build already owed as the book's #1
debt, and two are small wiring jobs. Full coverage is reachable without a single new
system that the book has not already committed to — the census found holes, not
architecture.

### Open decisions raised by this chapter

| # | decision | recommendation |
|---|---|---|
| D-C1 | does seed.hyp (the 30th element) enter the Phase A codex now, or land with M6.4? | enter now as a SENSED/fogged node — the fog is the antagonist and this is its largest organ; hiding it until Act VI would be the one dishonest silence left |
| D-C2 | axis_levels data source: journey_save flags from boss passes (player's assistant) vs LEYBER-side wiring | journey_save first — boss passes are real asserts today; entity-side wiring is a later forge |
| D-C3 | map consequence bundle C+D+E (no fifth ring; ops as transitions; the pulse) | approve as recommended in §5 |
| D-C4 | the Paradigm Book cross-check pass (third canon witness, §scope caveat) | schedule as a bounded audit session; until run, conflicts flag rather than resolve |

(F1 SENSES is already ledger #3 and is not duplicated here; this census only raises its
stakes — it is canonical seed #2's full body.)

### Governance

This chapter yields to A8 (element-by-dimension truth) and A13 (stations) for the 29+ that
exist in the codex; it OWNS the canon-to-game disposition. A new canonical document, a
Paradigm Book divergence, or a codex change reopens the census; a row changes disposition
only by pointing at code or authored content on disk. BOOK.md registration of this chapter
and its four decisions is owed with the next spine edit.

---

## Changelog

- 2026-07-20 — v1. Authored from AEA_WALKTHROUGH.md + LBR_AEA_COMPLETE_BRIEF.md (canon)
  crossed with aea_elements.js, A8, A13, 03, 05B/05C, 06, A7, A10, A14, R1. Findings of
  record: canon's 10 seeds are a different ten from the game's (reconciliation table §2.2);
  seed #10 hypothesize + the entire innovation layer absent from the codex (largest hole);
  the game's "ops" are the operator loop, not canon's transcendence ops (renaming owed);
  rung-gating identified as OP1 enacted and D1's refuse-beat as no_op embodied. Verdict:
  86 items — 30 embodied / 31 compressed / 22 missing / 3 out-of-scope; missing collapses
  into six build packets; map recommendation C+D+E, no fifth ring. D-C1..D-C4 opened.
