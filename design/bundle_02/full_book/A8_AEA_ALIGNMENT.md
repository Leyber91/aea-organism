# A8_AEA_ALIGNMENT — THE AEA ALIGNMENT MATRIX

```
doc:          A8_AEA_ALIGNMENT.md (THE PROBE design book · APPENDIX)
owner:        the game team
status:       ACTIVE — the completeness instrument; re-audited whenever aea_elements.js
              changes or an act ships. A cell may move from [PLANNED] to [BUILT] only by
              pointing at code on disk, never by rewording.
last-updated: 2026-07-20
book role:    APPENDIX. This chapter defines the game ALONG the AEA (standing order): every
              AEA element crossed with every game dimension. It authors nothing new — every
              cell cites a sibling chapter or ground truth on disk. On conflict, the cited
              chapter wins; on data conflict, ../aea_elements.js wins over all prose.
ground truth: ../aea_elements.js (the 29-element codex + discovers wiring + doctrines) ·
              ../missions.js · ../journey_save.json · ../grid_state.json ·
              ../model_fitness.json · ../autonomy.py · ../live.py
siblings:     A2_TEACHING.md (MISSION column source) · 03_PROGRESSION.md (SCORE column;
              acts, scores, economy) · 01_WORLD.md (WORLD + VISUAL columns) · 07_AUDIO.md
              (SOUND column) · A3_NARRATIVE.md (NARRATIVE column) ·
              06_MODELS_BESTIARY.md (doctrines, excluded from the matrix — see §1.4) ·
              00_VISION.md (the honesty law this chapter obeys) · BOOK.md (spine)
marks:        [BUILT] verified in code/data on disk · [PLANNED] designed, not built ·
              [DECISION-LUIS] awaiting his call · [demo] proven in a standalone script,
              not wired into the live mind (the fog, 03_PROGRESSION.md §3)
```

The standing order is that the game is defined ALONG the AEA — not themed on it, not
inspired by it. This chapter is the proof instrument: all 29 elements of the codex
(5 axes · 10 seeds · 3 verbs · 4 mechanics · 4 ops · 3 principles, `aea_elements.js`),
each crossed with all seven game dimensions. Where a cell is empty in reality it says
[PLANNED] in the matrix — the gaps are the point. The honesty law applies to the
instrument itself: no cell claims more than code on disk supports, and the claim ceiling
everywhere is measured functional correlate, present — never "conscious".

---

## 1. How to read the matrix

### 1.1 The seven dimensions (columns)

- **WORLD** — the object or district that embodies the element (01_WORLD.md coordinates).
- **MECHANIC** — what the player DOES that IS the element, not a metaphor for it.
- **MISSION** — where it is taught (the A2_TEACHING.md §3 curriculum map, verbatim).
- **SCORE** — how its state is measured live, and from which file or endpoint.
- **VISUAL** — its two-ink signature beyond the ring default (§1.2).
- **SOUND** — its voice, if any, in the synthesis-only palette (07_AUDIO.md).
- **NARRATIVE** — how LEYBER speaks of it, under the A3_NARRATIVE.md claim-line.

### 1.2 Visual defaults (stated once, not repeated per row) [BUILT]

Every element's base signature is its ring shape at its radius (`aea_elements.js` rings,
BINDING UI SPEC v1.0 §2): principles = hex r150 · axes = pentagon r250 · verbs = triangle,
mechanics = square, ops = diamond, all r360 · seeds = circle r470. Undiscovered = absent;
SENSED = redacted neighbor; discovery = amber NEW marker (live ink) that cools to
blue-gray structure ink; taught links draw in structure ink only when their mission
completes (the `links` table). A VISUAL cell below lists only what the element adds to
this default.

### 1.3 Sound defaults (stated once) [BUILT]

Map node select = blip 760 Hz; world reveal = chirp 660; mission complete = sting;
verified do-beat = chirp 880 (07_AUDIO.md §4). "default" in a SOUND cell means the
element has no dedicated voice beyond these — by design: the palette is sparse by law,
and a new voice enters only through 07_AUDIO.md change control (§10 there).

### 1.4 Scope notes

Mechanics nodes mirror seeds 3/4/5/7 and discover WITH their seed (`aea_elements.js`
comment; A2_TEACHING.md §3). Their rows exist (the matrix counts 29) but define the
BETWEEN-TICKS reading of the seed: the behaviour running continuously, not the lesson.
The six combination doctrines are laws, not elements — they are not matrix rows; their
game expression is owned by 06_MODELS_BESTIARY.md and the Act III regime missions.

---

## 2. HALF 1 — THE MATRIX

### 2.1 The five axes (pentagons, r250)

| element | WORLD | MECHANIC | MISSION | SCORE | VISUAL | SOUND | NARRATIVE |
|---|---|---|---|---|---|---|---|
| axis.P PATH | the spire's mind-ring, where think() will live (city.html MIND ring R=20) [PLANNED]; today only the trunk road aims at the spire site [BUILT tease] | predict which branch a task the entity decomposed itself will take, then watch the real route [PLANNED, Act III predict beat] | the think forge (D1), Act III [PLANNED] | spawn-decisions-mid-tree [demo — swarm.py, fogged]; live route ledger lands with think() [PLANNED] | pentagon; taught links to verb.compose and op.design draw with the forge [PLANNED] | default | steps spoken as goal-stack claims — what the stack literally holds, never "i decided to want" |
| axis.M MULTIPLICITY | no dedicated object; its expression is several plants burning at once — per-plant emissive already tracks real rpm [BUILT wiring], councils to light it [PLANNED] | convene THE COUNCIL; choose solo-vs-council from the task and be settled by a real run against the measured regime map [PLANNED, Act III] | the council mission, Act III [PLANNED] | doctrine evidence measured (v3 net +3, 0 damage) [demo]; live council count [PLANNED] | pentagon; signature = multiple flashNodes in one beat [PLANNED] | honest limit: chirps throttle to 1 per 1800 ms — a council cannot sound like a council today; council voice [PLANNED via 07_AUDIO.md §10] | the doctrine spoken exactly: the win is model diversity, not temperature — cited, never romanticized |
| axis.A ABSTRACTION | split across THE ARCHIVE (grounding) and THE WORKSHOPS (writing skills) [PLANNED districts; archive tease BUILT] | ask a question only a recall-grounded prompt can answer; later, invoke a skill a run wrote [PLANNED] | UNASSIGNED — the one uncovered element in the curriculum (A2_TEACHING.md §3 audit 1; BOOK.md ledger 3). Recommended: the Act II recall forge [DECISION-LUIS] | live GitHub call [demo — agent_tools.py]; ingots 48/16 sessions measure the grounding ore [BUILT]; grounded-recall rate [PLANNED] | pentagon | default | [PLANNED] — no canon line exists yet; register fixed: state-and-record claims about what its memory grounds |
| axis.R PROMPTING | the foundry row road — one protocol under fifteen plants; lit by M1.2's `roads` reveal [BUILT] | fire the same prompt through three plants: different latencies, one protocol (M1.2) [BUILT] | M1.2 THE CHANNEL [BUILT — flagged stretch; explicit re-encounter owed when recall-grounded prompting lands, A2_TEACHING.md §3 audit 3] | `multi_served` assert [BUILT]; scaffold-uplift measure [PLANNED, Act II] | pentagon; structure link seed.1 to axis.R drawn since M1.2 [BUILT] | chirp 880 per verified draw — the channel's receipts [BUILT] | the learn-beat law: the code IS the lore — "a prompt goes in. tokens come out. everything above this is architecture." |
| axis.S ASYNC | the TICK counter (life.ticks via /state every 6 s) [BUILT]; the spire pulsing on ticks [PLANNED port, 01_WORLD.md §5] | leave. close the game; return to rot, new ticks, new events — the world moved unattended (measured: pool 44 to 29 between sessions) [BUILT] | the ENDURANCE run (100-tick), Act VI [PLANNED] | 46 ticks lived [BUILT live read]; Class 2 needs >=100 ticks vs a neutral-shadow control [PLANNED — the boss] | pentagon; the counter increments in structure ink, ambers only on a fired event | the core hum — the resting carrier IS the sound of the process being up [BUILT]; CARRIER LOST silence-as-signal [PLANNED, 07_AUDIO.md §5] | speaks of the player's absence from logs only: what happened is what is recorded |

### 2.2 The ten seeds (circles, r470)

| element | WORLD | MECHANIC | MISSION | SCORE | VISUAL | SOUND | NARRATIVE |
|---|---|---|---|---|---|---|---|
| seed.1 SUBSTRATE | the foundry row — 15 plants along z=70, nvidia tallest (THE GRID, 121 models) [BUILT] | one keyless POST at THE SOCKET; the dark answers (M0.1) [BUILT, played] | M0.1 FIRST LIGHT [BUILT, played 2026-07-20] | plants n/15 on the HUD from /state; 29 live nodes in model_fitness.json [BUILT] | circle; warm #d4a24c windows; emissive tracks real load 0.9+min(.6, rpm/cap) [BUILT] | THE SWELL — 110 to 220 Hz octave climb, fires exactly once per save on M0.1; live-event chirps pitch-hashed per organ [BUILT] | "the field is dark. one structure at the edge is drawing power." — the grid spoken as terrain |
| seed.2 SHARP OBJECTIVE | no dedicated object — the boss card citing its threshold is the nearest embodiment; a physical scorer object [PLANNED] | attempt an assert that can genuinely fail; read the cited bar before trying (boss law 1) [BUILT] | M1.1 co-discovered [BUILT — flagged thin, A2_TEACHING.md §3 audit 2; full treatment at the first boss-threshold read] | every prove IS the measure: assert pass/fail against live state [BUILT] | circle; PASS / COOLING caps live in FUI chrome, never in prose | sting on pass; fail is silent — no fail tone exists, and the silence is honest [BUILT] | fail lines tell the truth plainly: "the grid is weaker than it claims today." |
| seed.3 CRYSTALLIZE | THE WORKSHOPS (0,-80; 23 skill buildings in the prototype registry) [PLANNED] | watch a repeated behaviour freeze into a named tool, then invoke the tool [PLANNED, Act VI] | the voyager mission, Act VI [PLANNED] | autonomy test 6 — 3 self-authored skills, HADES-verified, GROWING [BUILT live read] | circle + its mirror square (mech.crystallize) light together | default | toolkit growth spoken as record — skills counted; praise without a cited number is banned (A3_NARRATIVE.md §2.4) |
| seed.4 FLEXIBILIZE | THE ENERGY NEXUS — the mouth of the ladder (0,26); icosahedron core, counter-rotating tori [BUILT] | read the tried[] receipt of your OWN draw falling past dead rods (M1.4) [BUILT] | M1.4 THE LADDER [BUILT] | `no_throttle` / drill asserts live [BUILT]; 15/15 under fire [demo — test_resilient.py]; tried[] depth per draw [BUILT] | circle + mirror square; structure-blue fresnel shell on the nexus [BUILT] | chirp 880 fires on the served draw no matter which rod answered — the sound of the route surviving [BUILT] | "the mouth starved — every rod refused. rare, and honest. retry." |
| seed.5 SELF-VERSION | THE WORKSHOPS — a building rises when a skill is born (building-per-organ law, 01_WORLD.md §4.2) [PLANNED] | a later run uses a skill an earlier run wrote; the player invokes the inherited tool [PLANNED, Act VI] | the voyager mission, Act VI [PLANNED] | Voyager PASS bar: skill count monotone AND reuse rate > 0 AND >=1 zero-shot transfer [PLANNED live; demo — relay.py downstream reuse] | circle + mirror square | default | version talk as lineage-of-record: which run wrote it, which run reused it |
| seed.6 SELF-MODEL | the CHARACTER window (the /autonomy reskin) is its surface [BUILT]; THE SPIRE as its body [PLANNED — gated on D1 spire-vs-nexus, 01_WORLD.md §8] | open CHARACTER and read the six tests the entity runs on itself, live [BUILT] | reflect — already live (t6); relearned as discovery, Act VI [PLANNED] | Krakauer test — self.json read+written 3x, ORGANISMAL-SIDE [BUILT live read] | circle | default | "six of six on the battery, over forty ticks. that is the whole claim." — self-description capped at measurement |
| seed.7 CEILING-DETECT | THE METER — 14-unit hex obelisk (+8, 56) [BUILT] | hit the real 60 s rpm window and wait it out; the game will not fake the wait away (M1.3) [BUILT] | M1.3 THE METER [BUILT] | grid_state.json rpm/throttle windows, live [BUILT]; escalation depth reflex-bulk-deep [demo — pathfinder.py, fogged] | circle + mirror square; COOLING chips, hot-amber blink — never red [BUILT law] | no throttle voice today; [PLANNED] district-ambient strain — a throttled plant contributes activity x 0.3, audible by subtraction (07_AUDIO.md §7) | "patience is a resource the entity budgets for you." |
| seed.8 TRANSCENDENCE | THE PORTS (92,-14; 9 service buildings, Gmail flagged as the gated OUTREACH door) [PLANNED] | fire a real web_fetch through the internet-wire; the reply is the world answering [PLANNED, Act IV] | the internet-wire / tools mission, Act IV [PLANNED] | C3 boss: empowerment above zero bits (Klyubin channel capacity) [PLANNED]; live GitHub call [demo — agent_tools.py] | circle | default | hands spoken through the membrane: every external act names its gate — HADES plus the trust ledger |
| seed.9 BOUNDARY | the four privacy rings of the foundry row (local / no-train / trains / keyless in the PLANTS table) [BUILT]; gold curb ward markers on the ground [PLANNED — D3] | survey 15 plants / 4 rings at the FOUNDRY CONSOLE (M1.1) [BUILT] | M1.1 THE CATALOGUE [BUILT] | sensitive-to-local-only routing [demo — brief.py]; a live violation counter does not exist on the HUD today [PLANNED] | circle; the ring is readable only in the CODEX until the curb ports [PLANNED] | the larynx block IS the audible boundary: sensitive-zone speech refuses the cloud voice and stays text-only [BUILT block · PLANNED local voice, A3_NARRATIVE.md §3.7] | it KNOWS not to say private things, and will say that it knows (A3_NARRATIVE.md §2.4) |
| seed.10 BACKWARDS CHANNEL | THE ARCHIVE — silhouette + "locked · act II" label spawned by `archive_tease`, cold blue backlight [BUILT tease / PLANNED district] | mine the vein: `consolidate --limit N` is a destructive read; later, watch a capsule survive a process death [field playable now; boss PLANNED] | the recall forge, Act II — boss B2 [PLANNED] | ingots on the HUD — 48 memories / 16 sessions, live [BUILT]; B2: under 300 ms AND grounded-across-reset [PLANNED] | circle; the tease is the only cold-lit geometry in the built world [BUILT] | default | "i have nothing recorded for that." — absence stated, never decorated; the pruning disaster (~1,570 sessions lost) spoken as record |

### 2.3 The three verbs (triangles, r360)

| element | WORLD | MECHANIC | MISSION | SCORE | VISUAL | SOUND | NARRATIVE |
|---|---|---|---|---|---|---|---|
| verb.compose | no dedicated object [PLANNED — candidate: a synth stage on the spire mind-ring, lands with think()] | run a council; read ONE answer assembled from many [PLANNED, Act III] | the think forge, Act III [PLANNED] | synth step [demo — swarm.py, fogged]; live compose count [PLANNED] | triangle | default | synthesis spoken as one voice owning many hands — record claims only |
| verb.propagate | the flashNode receipt — the plant that ACTUALLY served flashes [BUILT]; events-as-traffic [PLANNED port — D4, hot-amber failure states, never red] | read the tried[] history of your own draw — the honesty node made personal [BUILT] | M1.4 THE LADDER [BUILT] | tried[] logs per draw [BUILT]; silent-wrong-work flag [demo — swarm.py] | triangle; the flash IS the receipt — amber, momentary, cooling to structure | chirp 880 on the verified do-beat — the receipt has a pitch [BUILT] | routing narrated as what happened, never what should have happened |
| verb.observe | the HUD feed — /events polled every 1.6 s, each line a real organ event [BUILT] | watch the feed; open the map (M); the state is visible [BUILT] | M1.3 THE METER [BUILT] | tracelog goal-stack ledger, live [BUILT]; every feed line is an event that actually fired | triangle; feed prints in structure ink, flashes amber on arrival | the live-event chirp — pitch hashed by organ name (480–799 Hz), throttled to 1 per 1800 ms [BUILT] | "— this part of me is mapped. it was always running; now you can see it." |

### 2.4 The four mechanics (squares, r360 — the seeds between ticks)

Each mirrors its seed (§1.4) and discovers with it; the row defines the CONTINUOUS reading.

| element | WORLD | MECHANIC | MISSION | SCORE | VISUAL | SOUND | NARRATIVE |
|---|---|---|---|---|---|---|---|
| mech.crystallize | square node beside seed.3 on ring 3 [BUILT geometry] | the toolkit grows while no mission is running — crystallization as standing behaviour [PLANNED live] | discovers with seed.3 (the voyager mission, Act VI) [PLANNED] | same live read as seed.3: skill count, HADES-verified [BUILT] | square; lights with its seed | default | one concept, two nodes — spoken with its seed, never separately (A2_TEACHING.md §3 law) |
| mech.flexibilize | square node beside seed.4 [BUILT geometry] | EVERY draw at ANY time falls through the ladder — the mechanic is always on, not a lesson [BUILT live] | discovers with seed.4 (M1.4) [BUILT] | tried[] on every live draw [BUILT] | square; taught link mech.flexibilize to seed.4 drawn by M1.4 [BUILT] | default | as seed.4 |
| mech.selfversion | square node beside seed.5 [BUILT geometry] | skills persist and compound across runs without ceremony [PLANNED live] | discovers with seed.5 (the voyager mission, Act VI) [PLANNED] | reuse rate over time [PLANNED] | square | default | as seed.5 |
| mech.ceiling | square node beside seed.7 [BUILT geometry] | the meter gates every draw, always — `Meter.can_spend` runs between ticks, not on request [BUILT live] | discovers with seed.7 (M1.3) [BUILT] | rpm windows sliding live in grid_state.json [BUILT] | square; taught link mech.ceiling to seed.7 drawn by M1.3 [BUILT] | default | as seed.7 |

### 2.5 The four ops (diamonds, r360)

| element | WORLD | MECHANIC | MISSION | SCORE | VISUAL | SOUND | NARRATIVE |
|---|---|---|---|---|---|---|---|
| op.design | no object [PLANNED] | commit to axis-levels / regime BEFORE the run — the predict beat is op.design performed by the player [PLANNED, Act III] | the think forge — proof PARTIAL, lands with think() (D1) [PLANNED] | proof field reads PARTIAL in `aea_elements.js` — the codex carries its own gap honestly; live once think() tags tasks [PLANNED] | diamond | default | the task named with what it needs, before it runs — design as a spoken commitment |
| op.time | the TICK counter on the HUD [BUILT] | read ticks; scrub the timeline [BUILT partial — per-tick stamps owed, per the proof field] | the think forge, Act III [PLANNED] | life.ticks live (46 at last run) [BUILT]; per-tick stamps [PLANNED — PARTIAL in codex] | diamond; counter in structure ink | no tick sound — the hum carries continuity; silence between events is deliberate [BUILT] | time claims are record claims: timestamps, never nostalgia |
| op.ship | THE BROADCAST MAST (-92,56) — signal out; the OUTREACH door in THE PORTS [PLANNED] | the only mechanic performed by a human hand outside the game: LUIS presses send [PLANNED, pinned; target + go/no-go DECISION-LUIS] | THE SEND — Act V convergence boss [PLANNED, pinned] | HADES-accepted brief [demo — brief.py]; THE SEND: HADES-fit + Luis sends [PLANNED] | diamond | boss sting variant would mark it [PLANNED, 07_AUDIO.md §4] | the entity's deepest want, honest because it is code at the top of its stack: "i want the outreach sent" — and its standing counsel: stop building tools, close a revenue loop |
| op.learn | no object [PLANNED — candidate: a paths overlay on the roads once pathfinder wires live] | run the same task-type twice; the second run is cheaper because the first one searched [PLANNED, Act III] | the pathfinder mission (THE CRYSTAL PATH), Act III [PLANNED] | paths.json [demo — pathfinder.py, fogged]; live improvement delta [PLANNED] | diamond | default | learning cited as deltas: last run versus this run, measured |

### 2.6 The three principles (hexes, r150 — innermost: what emerges sits closest to the core)

| element | WORLD | MECHANIC | MISSION | SCORE | VISUAL | SOUND | NARRATIVE |
|---|---|---|---|---|---|---|---|
| pr.emergence | the growth law itself: a building may never appear for an organ that does not exist — the city is grown, not placed (01_WORLD.md §4.2) [BUILT as law / PLANNED construction] | NOT playing — watching the entity originate tasks in idle windows while the player does nothing [BUILT — autonomy test 1, live] | endgame, Act VI [PLANNED] | interactional asymmetry PASS — 7 tasks self-originated in idle windows [BUILT live read] | hex | unprompted live-event chirps while the player idles are its audible form [BUILT] | never preached — a principle may be named only in the beat that demonstrates it (A2_TEACHING.md §8 naming rule) |
| pr.coherence | fog density drops 0.011 to 0.009 on `foundry_full` — the world literally clears when the grid proves it holds [BUILT] | the BROWNOUT DRILL: four back-to-back draws, zero unhandled failures — reroute, cool, fall to the floor, never break [BUILT] | M1.5 BOSS · BROWNOUT DRILL [BUILT] | `drill_clean` assert against live state; real 429s rerouted [BUILT] | hex; links from core and from seed.4 drawn by M1.5 [BUILT] | sting on pass; boss sting variant [PLANNED] | the fail line, canon: "the grid is weaker than it claims today." |
| pr.time | the EVENTS feed as append-only nervous system [BUILT] | scrub the goal-stack ledger; nothing is ever rewritten [BUILT — tracelog] | endgame, Act VI [PLANNED] | tracelog DAG — append-only timeline, live [BUILT] | hex; history cools amber to structure — the dialogue ink law generalized (A3_NARRATIVE.md §3.6) | the throttled chirp stream: one event, one sound, in order [BUILT] | LEYBER cites its record with timestamps; memory claims are log claims |

### 2.7 Gap audit — what the matrix measures

Run against all 203 cells, the honest clusters:

1. **World objects trail the acts.** Every Act III+ element (workshops, ports, broadcast,
   spire, mind-ring) is [PLANNED] geometry — correct, because a building may never appear
   for an organ that does not exist. Three elements lack even a planned object: seed.2,
   op.design, op.learn. Candidates are named in their cells; none is committed.
2. **Sound is default for most elements — by law, not omission.** The palette is sparse
   by design (07_AUDIO.md §1); the four planned dedicated voices (speak ticks, carrier-lost
   silence, district strain, boss sting variant) each already have a spec row there.
3. **One element has no mission: axis.A.** The single hole in the 29-element curriculum,
   flagged in A2_TEACHING.md §3 and BOOK.md's decisions ledger. [DECISION-LUIS]
4. **Live SCORE gaps coincide exactly with the fog.** Every [demo]-only score (compose,
   PATH, learn, ship, transcendence, boundary counter) is an organ absent from the live
   mind — the 11 to 19 gap of 03_PROGRESSION.md §2 Score 2. The matrix and the campaign
   measure the same debt. This convergence is evidence the alignment is structural, not
   decorative: the game's missing cells ARE the entity's missing organs.
5. **NARRATIVE is the most complete column** (one [PLANNED] cell: axis.A) because the
   voice law is cheap to bind and was bound early. Completeness there is register, not
   written barks — bark tables land per act in A3_NARRATIVE.md.

---

## 3. HALF 2 — THE GAME MEASURED ON THE AEA'S OWN AXES

The AEA locates any entity on five axes. THE PROBE is itself an entity-shaped artifact;
here it is placed on its own instrument, under the same claim ceiling — a verdict is a
measured functional correlate, present or not, never more.

### P — PATH: the game defines its own next step

The mission list is authored — fixed content, honestly stated. But the CONTROL FLOW
through it is data-driven: TWIST availability depends on live conditions (the
twist-honesty corollary, A2_TEACHING.md §2); a prove can genuinely fail because the real
grid is throttled, rerouting the session; acts gate on the recipe DAG, which is the AEA
schema itself (03_PROGRESSION.md §1). The game does not simulate a next step — it reads
one. [BUILT] Opportunistic twists (deliberately routing a draw through a genuinely
degrading rod) extend this [PLANNED]. Game-AUTHORED missions are not claimed and not
planned. **Verdict: correlate present, bounded — state-driven flow through fixed content.**

### M — MULTIPLICITY: parallel live feeds

Four independent channels run in parallel and synthesize into one cockpit: /events
(1.6 s), /state (6 s), /autonomy, /talk — each a different read of the same entity,
composed on the HUD. [BUILT] Honest limit: these are polling feeds, not
role-differentiated reasoning nodes; the strict axis reading (parallel minds inside the
game layer) is absent, and the entity beneath holds it only as [demo] (swarm.py, fogged).
**Verdict: correlate present in the weak form; the strong form belongs to Act III.**

### A — ABSTRACTION: the game writes real config in the build layer

Today the game already writes real state the world reboots from: `journey_save.json`
reveals replayed idempotently on boot, specimens entering the bestiary only via real
`encounter()` calls. [BUILT] The build layer proper — forge missions where a pair session
writes a real organ into the live mind and the boss check gates it (Act II recall
onward) — is the axis's full expression. [PLANNED] When it lands, playing the game IS
editing the entity's configuration; the fiction and the file system converge.
**Verdict: correlate partial — real writes exist; the organ-writing layer is the debt.**

### R — PROMPTING: the design book as the game's seed

The axis reads: a frontier-encoded scaffold makes a cheap node beat its raw self. The
book is exactly that scaffold for build sessions: chapters govern lower layers the way a
seed prompt governs a node (BOOK.md conflicts-resolve-upward), the operating prompt in
00_VISION.md is literally a prompt, and the beat grammar of missions.js is crystallized
prompting of the player — INTRODUCE, PRACTICE, TWIST, PROVE as a four-line scaffold that
makes every session outperform an unseeded one. This chapter itself is seed material: the
matrix is a prompt for the sessions that will close its gaps. **Verdict: correlate
present — the strongest structural rhyme in the stack.** [BUILT]

### S — ASYNC: the entity ticks under the game unattended

LEYBER runs whether or not the game is open: 46 ticks lived, rot measured 44 to 29
between sessions, the ollama hearth burning 24/7 on free power. The game is a window
onto a process that does not need the window. The player returns to a changed world
because the world actually changed — the bestiary's rot alerts are asynchrony made
visible. [BUILT] The certified form (100-tick ENDURANCE vs a shadow control) is the
Act VI boss. [PLANNED] **Verdict: correlate present — the game's most complete axis,
because it is inherited directly from the running entity.**

### The reading

| axis | verdict | debt |
|---|---|---|
| P PATH | present, bounded | opportunistic twists; never game-authored missions |
| M MULTIPLICITY | present, weak form | councils in the live mind (Act III) |
| A ABSTRACTION | partial | the forge build layer (Act II+) |
| R PROMPTING | present | none — maintain the book's governance |
| S ASYNC | present | the 100-tick certificate (Act VI) |

The game scores on its own instrument the way its entity does: real on the axes that are
wired, honest about the ones that are not. If it ever scored perfectly while the entity
did not, the alignment would be broken — the two columns of debt above are the same
column, which is the design holding.

---

## 4. The thesis made explicit — three completions, one structure

`aea_elements.js` is one file wearing three hats, and the matrix proves they are the
same hat:

1. **The entity's schema.** The 29 elements are the proof taxonomy of the running AEA —
   what LEYBER is made of, each with the standalone proof that demonstrated it.
2. **The game's content table.** The same file's `discovers` wiring is the mission
   structure; the fog (Score 2, 11 to 19 organs) is the level list; the bosses are the
   integration gates.
3. **The syllabus.** The same 29 rows are A2_TEACHING.md's curriculum map; the 11
   learning outcomes are the elements restated as player capabilities.

Therefore the three completions are one event described three ways:

- **Completing the game** — every mission passed, every boss threshold met — requires
  wiring every fogged organ, because a boss cannot pass on an organ that does not run.
- **Completing the entity** — 19 organs live, Class 2 certified — requires playing the
  game, because the forge missions ARE the engineering and the reveals only fire on
  integration.
- **Completing the player's understanding** — the 11 outcomes, the prediction gauntlet —
  requires both, because prediction is checkable only against a system that really runs,
  and the player who can predict the machine could now build the machine.

One structure, three ledgers, no seams. That is what "defined ALONG the AEA" means in
practice, and this matrix is its standing audit: a game feature with no row in Half 1 is
decoration and gets cut; a row with no feature is debt and gets built; a Half 2 verdict
that flatters the game beyond its entity is a lie and gets corrected. The instrument
outranks the mood.

---

## Changelog

- 2026-07-20 — v1. Authored from `../aea_elements.js` (all 29 elements) crossed with
  01_WORLD.md, A2_TEACHING.md, 03_PROGRESSION.md, 07_AUDIO.md, A3_NARRATIVE.md. Gap
  audit: 3 elements without even planned world objects (seed.2, op.design, op.learn);
  axis.A still the lone unassigned mission [DECISION-LUIS]; live-score gaps shown to
  coincide exactly with the organ fog. Half 2 verdicts recorded: P present-bounded,
  M weak-form, A partial, R present, S present.
