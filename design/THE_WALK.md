# THE WALK — the journey to a complete Autonomous Entity Architecture

*The first version of the game is a walk to complete the AEA. This is the path: every step, what it
closes, how we prove it, and what the companion gains. One step per turn. Nothing is marked done
until it RAN and was SEEN.*

**Started 2026-07-25. Source of truth for the destination: `A15_FULL_COVERAGE.md` (86 canonical
items · 30 embodied · 31 compressed · 22 missing · 3 out of scope).**

---

## 0 · THE PREMISE

Canon defines an architecture in 86 items. The running entity carries a fraction of them. **That gap
is the game.** The player closes it, step by step, and the final canonical gate (C-64) is literally
*"claim becomes receipt"* — the point at which the architecture stops being a document and becomes a
thing that demonstrably runs.

**Win condition:** the census closes. Not a score, not a boss — `86/86`.

**The binding rule (C-63, canon's own):** each layer of the construction stack requires every layer
below it. Remove one and everything above stops. That is the gate structure, and it was derived
rather than designed.

```
LAYER 0  THE QUESTION — "what must exist for indefinite growth?"
LAYER 1  the five axes            LAYER 6  the principles overlay
LAYER 2  the ten seeds            LAYER 7  the action layer
LAYER 3  the mechanics            LAYER 8  substrate intelligence
LAYER 4  transcendence ops        LAYER 9  infrastructure intelligence
LAYER 5  the innovation layer     LAYER 10 THE AEA — claim becomes receipt
```

---

## 1 · THE COMPANION — a construct that gains capabilities

Not an animal, not an anatomy. **A real construct spec that really runs**, whose identity is its
part-signature and whose name is EARNED (never given — A17). It evolves when it crosses a
**capability threshold**, and every stat on its card is a measurement, never a number we chose.

**Its capabilities — the honest list, each a yes/no we can test:**

| capability | the question it answers | how it is proven |
|---|---|---|
| **DRAWS** | can it get a real answer at all | a receipt returns |
| **CLOSES** | can its work be measured | a scorer records axes |
| **SHAPED** | does a scaffold make it beat its raw self | measured delta, same rod, with/without |
| **GROUNDED** | does recall change what it answers | measured delta vs the same run without memory |
| **PLANS** | does it choose its own next step | a multi-step trace it authored |
| **CONFERS** | do several differentiated roles synthesise | N real sub-runs, one synthesis |
| **WAITS** | does it run unattended on a schedule | it fired while nobody watched |
| **RECOVERS** | does it survive a dead rod | a fall-through receipt that still closed |
| **JUDGES** | can it refuse its own bad output | a real refusal on record |
| **REVISES** | can it change its own composition | a self-version entry in its lineage |
| **PROPOSES** | can it generate and commit a change to itself | a committed L5 action |

**Evolution thresholds** (form changes, name re-earned):

- **STAGE I — a spark.** DRAWS. One call, nothing else.
- **STAGE II — an instrument.** DRAWS + CLOSES + SHAPED. It is measurable and improvable.
- **STAGE III — a resident.** + GROUNDED + RECOVERS + WAITS. It persists and survives.
- **STAGE IV — an agent.** + PLANS + CONFERS + JUDGES. It acts and checks itself.
- **STAGE V — an entity.** + REVISES + PROPOSES. It changes itself. This is the AEA.

---

## 2 · THE PATH — sixteen steps

Each step names the canonical items it closes, the act, the test that proves it, and what the
companion gains. **A step is not complete until its test has run and been seen.**

### LAYER 1 — THE AXES · the coordinate system

**STEP 1 — THE POSITION RECORD (C-11)** — `DONE 2026-07-25`
Canon defines growth as movement through five axes (L0–L5). The substrate had `axis_levels` in zero
files: a coordinate system with no coordinates.
· **Did:** `aea/mind/axes.py` + `/game/axes`. A level raises ONLY on a receipt (OP1); a skipped rung
is refused; a re-claim is refused. Where canon never named a rung it returns `null`, never a guess.
· **Test (ran):** position reads `1/25`, the single raise on record cites run `r-25`.
· **Companion:** born. STAGE I, DRAWS.

**STEP 2 — THE PROMPTING LADDER (C-06/R)**
Canon's definition of the axis is itself the test: *"a scaffold makes a cheap node beat its raw
self."*
· **Do:** run one task on one cheap rod twice — bare, then framed — and measure.
· **Test:** a real delta on a comparable axis (pass, or chars/latency at equal pass). No delta, no
level. This is also the first honest chance to FAIL a step.
· **Companion:** gains **SHAPED** → STAGE II when CLOSES is also held.

**STEP 3 — THE ABSTRACTION LADDER (C-06/A)**
· **Do:** the same task with and without a real recalled memory injected; embed, retrieve, ground.
· **Test:** the grounded run measurably differs AND the retrieval was real (an embedding call with
real dimensions on record). Note: door 7 of the earlier walk proved storing and retrieving are
different operations — that failure is expected here and must be handled, not hidden.
· **Companion:** gains **GROUNDED**.

**STEP 4 — THE PATH LADDER (C-06/P)** — canon: L0 single call → L3 multi-step plan + critique
· **Do:** a construct that plans its own steps and critiques its own output before closing.
· **Test:** a trace with ≥2 authored steps where the critique changed the final answer.
· **Companion:** gains **PLANS**.

**STEP 5 — THE MULTIPLICITY LADDER (C-06/M)** — canon: L0 one path → L3 a council of N
· **Do:** N role-differentiated sub-runs, one synthesis. `mind/swarm.py` is the cited proof module.
· **Test:** N real receipts with distinct roles + one synthesis that references them.
· **Companion:** gains **CONFERS**.

**STEP 6 — THE ASYNC LADDER (C-06/S)** — canon: L0 synchronous → L2 prewarmer → L5 parallel
· **Do:** the companion fires on a schedule, unattended, and the run is waiting when we return.
· **Test:** a receipt timestamped while nobody was watching. (The entity already ticks 24/7 — this
step connects the companion to that clock.)
· **Companion:** gains **WAITS** → STAGE III with GROUNDED + RECOVERS.

### LAYER 2 — THE SEEDS

**STEP 7 — THE SIX FLOOR SEEDS (C-12..C-17)**
goal-presence · perception · coordination · coherence · substrate-variation · self-model. Canon: the
floor fires EVERY tick.
· **Test:** one real tick showing all six fired, or an honest list of which cannot yet.
· **Companion:** **RECOVERS** lands here (substrate-variation = surviving a rod swap).

**STEP 8 — THE FLOOR/STAIRCASE SPLIT + THE PULSE (C-18..C-22)**
The four conditional seeds, and C-22 — the split itself, carried nowhere.
· **Test:** a staircase seed fires on its precondition and NOT otherwise.

### LAYER 3 — THE MECHANICS

**STEP 9 — CRYSTALLIZE · FLEXIBILIZE · SELF-VERSION + CEILING-DETECT AS META (C-23..C-26)**
`flexibilize` is in zero files. Ceiling-detect's meta-status ("it triggers other mechanics by
recognising exhaustion") is the nuance nothing carries.
· **Test:** each mechanic fires on a real condition; ceiling-detect triggers another mechanic
rather than acting.
· **Companion:** gains **REVISES** (self-version writes a lineage entry).

### LAYER 4 — THE TRANSCENDENCE OPERATIONS

**STEP 10 — THE FOUR OPS (C-27..C-30)**
OP1 axis-extension (exercised at step 1) · OP2 corpus-swap · OP3 new-skill · OP4 bifurcation.
Canon's cleanest finding: **ops are things that HAPPEN TO the map, not nodes on it.**
· **Test:** each op observed as an event with a receipt — a notch lighting, a corpus replaced, a
skill minted, a branch forked.
· **Companion:** gains **JUDGES** → STAGE IV.

### LAYER 5 — THE INNOVATION LAYER · the deepest stratum, 28 items, absent

**STEP 11 — THE CYCLE (C-31)** TRIGGER → GENERATE → CASCADE → COMMIT.
**STEP 12 — THE EIGHT TRIGGER MODES (C-32..C-39)** saturation · failure_of_transcendence · anomaly ·
cross_pattern · anticipatory · decomposition · verification_debt · reflexive_steer.
**STEP 13 — THE FIVE CASCADE FILTERS (C-40..C-44)** all five must pass to commit.
**STEP 14 — THE SEVEN HYPOTHESIS TYPES + THE ACTION REGISTRY + THE SIX TOOLS (C-45..C-58)**
· **Test (the hard one):** the companion proposes a change to itself, the cascade filters it, and a
typed action commits it. Canon's own receipt warns 16.8% of emitted actions invent a tool name — the
validator must catch every one, and we must reproduce that catch.
· **Companion:** gains **PROPOSES** → STAGE V.

### LAYERS 6–9 — PRINCIPLES AND THE ENGINEERING LAYERS

**STEP 15 — THE OVERLAY AND THE INTELLIGENCES (C-59..C-75)**
The three principles (carried — verify, don't assume) · recovery v0.14a–d · the capability matrix and
`pick_for_role` (the seed choosing its own model from its own measurements) · resource monitor +
actuator.
· **Test:** the companion picks its own rod from its own measured matrix, and survives a real
resource event.

### LAYER 10 — THE RECEIPT

**STEP 16 — THE AEA (C-64)**
Sustained unattended operation certifying the whole stack.
· **Test:** the companion runs unattended across a real interval, every capability held, and the
census reads what it reads — honestly, whatever the number is.

---

## 3 · THE RULES OF THE WALK

1. **A step closes only on a receipt.** Ran and seen, or not done.
2. **A step may FAIL.** A capability we cannot prove is recorded as unproven. The walk is an
   experiment, not a script.
3. **Where canon is silent, show the gap.** Never invent a rung, a seed, or a stat.
4. **The companion's card is all measurement.** No chosen numbers.
5. **One step per turn**, so each gets its full test.
6. **The chronicle grows with the walk** — each step appends what actually happened, including what
   broke.

## 4 · PROGRESS

| step | closes | state |
|---|---|---|
| 1 · the position record | C-11 | **DONE** — `1/25`, raised by `r-25` |
| 2 · the prompting ladder | C-06/R | next |
| 3–16 | C-06..C-64 | pending |

**Census: 86 items. Verified-closed by this walk so far: 1.**

---

# THE CHRONICLE — what each step actually found

## STEP 2 · THE PROMPTING LADDER (C-06/R) — walked 2026-07-25 · **EARNED, conditionally**

**Assembly decision, and why:** I put PROMPTING first of the five axes because it needs no new
machinery, its canon definition is self-testing, and — the real reason — it de-risks every later
measurement. If a scaffold changes what a rod produces, every comparison after this must control for
it. Measure it first or everything downstream is contaminated.

**Rod:** `meta/llama-3.2-3b-instruct` (a genuinely cheap node). 5 tasks x 3 trials, bare vs framed.
Local rods were tried first and rejected as the instrument: 20-68s COLD START each, which is the
"physics not policy" limit made concrete.

**WHAT I FOUND — the generic scaffold LOST.**

```
TASK          BARE    FRAMED
WORD-COUNT    0/3     0/3
ARITHMETIC    3/3     3/3
STRICT-JSON   3/3     0/3     <- the scaffold DESTROYED a working capability
EXTRACT       3/3     3/3
HOLD          3/3     3/3
TOTAL        12/15    9/15    tokens: 969 -> 1848 (+91%)
```

Framed, asked for strict JSON, the rod answered **"I don't see a question."** The scaffold's own
instruction ("identify the FORM... emit ONLY that form") made it treat a directive as a non-question.
**A frame is not an upgrade. It can subtract.**

**THEN THE CONFOUND TEST (2b) — a FITTED scaffold won outright.**

```
CONDITION         PASS    TOKENS
bare              0/3     192     answers: 9, 11, 9
generic frame     0/3     327     answers: 9, 7, 9
targeted frame    3/3     471     answers: 13, 13, 13
```

The targeted scaffold said *how to count* (split on spaces, number the tokens, report the final
index). Impossible became certain, for 2.45x the tokens of bare.

**THE LAW, as measured (canon states the claim but not the condition):**
> A scaffold makes a cheap node beat its raw self **only when it is fitted to the specific failure.**
> A generic scaffold is pure cost, and can be negative.

**WHAT THE COMPANION CAN DO** (all measured, this rod):
- **DRAWS** — real answers return.
- **CLOSES** — the scorer records real axes.
- **SHAPED** — proven, *conditionally*: a fitted frame converted 0/3 to 3/3.
- Arithmetic (3/3), extraction (3/3), and holding a refusal rule (3/3) unaided.

**WHAT IT CANNOT DO:**
- **Count** unaided. 0/3, and consistently wrong the same way (9, 11, 9) — a stable capability
  ceiling, not noise.
- **Benefit from generic guidance.** Generic framing measurably harms it.
- **Keep strict format under a competing instruction.** 3/3 -> 0/3 is the sharpest fragility found.
- Everything above this rung: no memory, no plan, no council, no unattended run.

**WHAT THIS GIVES THE GAME (unplanned, and better than the plan):** THE FRAME becomes a real risk
rather than a free upgrade. Seating it can make a construct *worse*, and the player can only fit it by
first DIAGNOSING why the construct fails. That is a genuine mechanic no design document predicted -
it came out of the measurement.

**Axis moved:** PROMPTING L1 -> **L2**, proof `step2b/word-count 0-of-3 -> 3-of-3`. (Noting honestly
that the earlier L1 raise cited `r-25` loosely as a demonstration; this one is rigorous.)

**Order consequence:** doing R first was correct, and now it is load-bearing - every later step must
state whether its rod was framed, and the frame must be FITTED to be worth its rent.

## STEP 3 · THE ABSTRACTION LADDER (C-06/A) — walked 2026-07-25 · **EARNED, conditionally**

**What I found before testing anything — the machinery already existed.** `aea/memory/memory.py`
does embedding recall with LOCAL ollama (`mxbai-embed-large`) + cosine: free, unlimited, private. I had
been treating recall as fog. It is not. **And it was seeded with ten measured facts about this grid.**

**The finding that stopped the step cold.** Fact #2 in that store reads: *"NVIDIA's 40 requests/minute
limit is PER-MODEL with independent buckets - querying all 121 models at once produced zero 429
errors."* **The entity already knew.** I spent roughly a hundred API calls this session empirically
re-deriving a fact sitting in its own memory. Fact #5 states the crystallize doctrine - *a frontier
model encodes a behaviour into a scaffold a cheap model then runs* - which is EXACTLY what step 2
measured. And fact #10 warns: *"the biggest risk is that characterization keeps substituting for
building."* The store had already diagnosed the session it was not consulted for.

**FIRST TEST — FAILED, and the fault was mine.** I asked a question the rod could already answer:
```
bare       3/3  PER-MODEL   216 tok in
grounded   3/3  PER-MODEL   561 tok in   (+160%, +18.7s)
```
Zero gain for 160% more input tokens and an 18.7s cold recall. Bad test design: grounding cannot be
measured on a question the model already knows.

**SECOND TEST (3b) — isolated with a fact the rod CANNOT know (51 of the catalog serve):**
```
COND       PASS   TOK IN  TOK OUT  answers
bare       0/3    183     30       "I don't have acc..." x3
grounded   3/3    471      6       51 | 51 | 51
```
Impossible became certain. **Token flow: +288 prompt tokens (+157%), but OUTPUT FELL 30 -> 6** -
certainty is cheaper to say than an apology. The embedding itself cost **zero cloud tokens** (local),
and recall was **18.7s cold / 3.1s warm** - the local embedder has its own cold start.

**WHAT THE COMPANION CAN DO** (added this step):
- **GROUNDED** — a real local embedding retrieved the right fact at rank 1 and converted 0/3 to 3/3.
- **Refuses honestly when ignorant.** Bare, it said *"I don't have access"* three times out of three
  rather than inventing a number. That is a real, valuable capability found by accident.

**WHAT IT CANNOT DO:**
- **Know when grounding is worth it.** It cannot tell "I need memory" from "I already know" - that
  judgement is not in the construct, and stacking memory blindly is pure tax.
- **Recall quickly when cold.** 18.7s on the first call is a real latency cliff for any creature that
  wakes rarely.

**THE LAW ACROSS STEPS 2 AND 3 (the same shape twice — this is the walk's first real discovery):**
> **Every capability has a PRECONDITION for being worth its cost.**
> A scaffold pays only when FITTED to the failure. Memory pays only when the rod genuinely CANNOT know.
> Added without its precondition, a capability is pure tax — and sometimes actively harmful.

**Why that matters more than either step:** you cannot stack organs. A complete construct is not a
better construct. **Assembly order and assembly JUSTIFICATION are the game** — each organ must be
earned by a measured deficiency, which is exactly the "no right path" Luis named.

**Axis moved:** ABSTRACTION L0 -> **L1**. Position **3/25, 12% walked.**

## STEP 4 · THE PATH LADDER (C-06/P) — walked 2026-07-25 · **MECHANISM earned, PROFIT refused**

**Three conditions**, because "plan + critique" can mean two different things and the difference turned
out to be the finding: BARE (one call) · STRUCTURED (one call containing plan/execute/critique/final) ·
SEPARATED (three real calls - execute, critique, finalise). Tasks were cognitive traps (bat-and-ball,
machines-and-widgets, lily-pad) so a single call genuinely fails and a critique has something to catch.

```
TASK        BARE   STRUCTURED   SEPARATED
BAT-BALL    2/3    3/3          3/3
MACHINES    1/3    0/3          1/3
LILYPAD     2/3    2/3          2/3
TOTAL       5/9    5/9          6/9
bare         9 calls  1442 tok
structured   9 calls  2554 tok    critique: 0 found / 0 changed
separated   27 calls  6841 tok    critique: 9 found / 4 changed
```

**THE FINDING — SELF-CRITICISM REQUIRES SEPARATION.** The structured single call, explicitly instructed
to find the strongest error in its own answer, found **nothing in nine trials out of nine.** The same rod,
asked the same thing as a SEPARATE call, found something **nine times out of nine** and changed its answer
four times. **A model cannot criticise itself in the same breath it answers.** The boundary is not
stylistic - it is what makes self-examination occur at all.

**WHY THE LEVEL ONLY RISES TO L1, NOT L3:** separated critique cost **3x the calls and 4.7x the tokens
for +1/9** - inside noise at n=9. And of the four answers the critique changed, only one was a net
improvement: **changes were as likely to break as to fix.** So the mechanism is real and the profit is
not. Canon's L3 ("multi-step plan + critique") describes a capability the companion demonstrably HAS;
this walk cannot yet show it PAYS.

**WHAT THE COMPANION CAN DO:** **PLANS** - it authors steps, executes them, criticises its own output,
and revises. Proven, four real revisions.
**WHAT IT CANNOT DO:** criticise itself without a separate call · improve reliably when it does
criticise · and STRUCTURED made MACHINES worse (1/3 -> 0/3), the same shape as step 2's JSON breakage.

**MY OWN PREDICTION WAS WRONG.** P3 in the prompt library was designed as an instrument and its cheap
single-call form is inert. The library entry is now corrected: **P3 must be run SEPARATED or not at all.**

**Axis moved:** PATH L0 -> **L1**. Position **4/25, 16% walked.**
