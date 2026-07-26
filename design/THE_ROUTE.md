# THE ROUTE — the path through all 86, how they connect, and what each costs in tokens

*Companion to `THE_WALK.md` (the chronicle) and `A15_FULL_COVERAGE.md` (the census). This is the
ENGINEERING plan: the dependency order, the token budget, and the exact prompts each test needs.
Written 2026-07-25 after steps 1–3.*

---

## 0 · WHY THE CENSUS ORDER IS THE WRONG ORDER

C-01..C-86 is a catalogue, not a route. Walking it numerically would test the floor seeds before the
tick cycle they fire on, and the action registry before the tools it dispatches. **The route follows
the dependency graph.** Canon gives the coarse rule (C-63: each layer requires every layer below);
the fine edges are derived below and each one is stated so it can be argued with.

### The derived dependency edges

```
C-01..C-05 (axes exist)        -> C-06..C-10 (ladders can have rungs)
C-11 (position record)         -> C-06..C-10   [canon: axis_levels is "written by OP1"]
C-11                           -> C-27 (OP1 axis-extension writes it)
C-80 (the Checkpoint)          -> C-76 (the tick passes it by reference)
C-76 (the tick cycle)          -> C-12..C-17 (the FLOOR fires EVERY tick - no tick, no floor)
C-15 (coherence score)         -> C-18 (cohere/recovery acts on the score)
C-12..C-17 (floor)             -> C-18..C-21 (staircase fires conditionally ON floor state)
C-53..C-58 (the six tools)     -> C-52 (a registry with nothing to dispatch is empty)
C-32..C-39 (triggers) +
C-40..C-44 (filters) +
C-45..C-51 (hypothesis types) +
C-52 (registry)                -> C-31 (the cycle IS their composition)
C-31                           -> C-21 (hypothesize IS the L5 cycle)
C-52                           -> C-75 (validation guards the registry's dispatch)
everything                     -> C-64 (the receipt certifies the stack)
```

### THE CRITICAL PATH — and its root is the one nobody built

```
C-80 CHECKPOINT -> C-76 TICK -> C-12..17 FLOOR -> C-18..22 STAIRCASE
   -> C-53..58 TOOLS -> C-52 REGISTRY -> C-31 CYCLE -> C-21 HYPOTHESIZE -> C-64 RECEIPT
```

**Everything of consequence hangs off C-80**, which canon calls *embodied* and which appears in **zero
substrate files**. The entity does have shared state — but as MANY atomic JSON files read through
`grid.load_json`, not ONE mutable object passed by reference. That is either an honest compression
(same function, different shape) or the deepest gap in the architecture, and **settling it is the
single highest-leverage question on the route.** It gates 40+ items.

---

## 1 · THE ROUTE — nine phases in dependency order

Axis ladders (C-06..C-10) are not a phase; they are climbed THROUGH the phases, since each phase
produces the receipt that earns a rung.

| phase | closes | gate question | token budget* |
|---|---|---|---|
| **0 · THE INSTRUMENTS** *(done)* | C-11, + rungs on C-07/C-09 | can the entity say where it stands? | ~4k spent |
| **1 · THE SELF-MEASURE** | C-15, and SETTLE C-80 | can it score its own coherence per tick? | ~3k |
| **2 · THE CLOCK** | C-76 | does the ten-step tick exist, in order? | ~1k (mostly reading) |
| **3 · THE FLOOR** | C-12..C-17 | do all six fire on every real tick? | ~12k |
| **4 · THE STAIRCASE** | C-18..C-22 | do the four fire ONLY on their precondition? | ~10k |
| **5 · THE MECHANICS** | C-23..C-26 | does ceiling-detect TRIGGER rather than act? | ~6k |
| **6 · THE OPS AS EVENTS** | C-27..C-30 | can each op be witnessed as a receipt? | ~8k |
| **7 · THE INNOVATION LAYER** | C-31..C-58 (28) | can it propose a change to itself and commit it? | ~60k |
| **8 · THE ENGINEERING** | C-65..C-75 | does a seed pick its own rod from its own matrix? | ~15k |
| **9 · THE RECEIPT** | C-64 | does the whole stack hold unattended? | ~5k + wall time |

\* *budgets derived from MEASURED unit costs (below), not estimated.*

### Measured unit costs — the basis of every budget

| unit | prompt tok | completion tok | measured where |
|---|---|---|---|
| bare draw | 77 | 64 | the Hall, door 1 |
| chat-template floor | ~15 | — | a 6-token prompt billed 21 |
| + system frame | +34 | — | door 3 |
| + grounded recall | +288 | −24 | step 3b (output FELL) |
| + tools attached, unused | +75 | — | door 6 vs door 1 |
| tool round-trip | 2 calls, 297 in | 98 | door 6 |
| guard on output | 2 calls | — | door 4 (×2.14 wall clock) |
| local embedding | 0 cloud | 0 | free, 18.7s cold / 3.1s warm |

**The two laws that constrain every budget** (earned in steps 2–3):
1. **A capability is only worth its tokens when its precondition holds.** A frame pays only when
   FITTED to the failure; memory pays only when the rod genuinely CANNOT know.
2. **Local work is free.** Scoring, routing, parsing, deciding all measured 0–1ms against 600–6000ms
   network. Think hard, speak rarely.

---

## 2 · THE PROMPT LIBRARY — the exact instruments

Every test needs a prompt designed for it. These are the reusable ones; each is written to be
*checkable*, because a test whose result needs interpretation is not a test.

### P1 · THE FITTED SCAFFOLD (from step 2's law)
Generic framing measurably HARMS (12/15 → 9/15, and it broke strict JSON 3/3 → 0/3). A frame must name
the *method* for the specific failure:
```
To <do the failing thing>: <the explicit procedure, step by step>.
Show the working, then put <the answer form> alone on the last line.
```
*Proven: word-count 0/3 → 3/3.* **Never ship a frame that only says "be precise."**

### P2 · THE PRECONDITION PROBE (before spending on memory)
```
Answer only if you already know. If you do not know, reply exactly: NEED-GROUND.
<the question>
```
Cheap (one small call) and it decides whether the +288-token grounding is worth spending. This turns
law #1 into a runtime test instead of a designer's guess.

### P3 · PLAN + CRITIQUE (C-06/P, step 4)
```
STEP 1 - PLAN: list the minimum steps needed. Number them. Do not solve yet.
STEP 2 - EXECUTE: carry out your own plan.
STEP 3 - CRITIQUE: find the strongest error in your own answer. If none, write NONE.
STEP 4 - FINAL: the corrected answer alone, on the last line.
```
*Test: the level rises ONLY if step 3 changed step 4.* An unchanged critique is a critique that did
nothing — and that must be recorded as a failure, not rounded up.

### P4 · COUNCIL ROLES (C-06/M + C-77 peer_debate, step 5)
Three differentiated roles, each one call, then one synthesis:
```
PROPOSER  : give the strongest answer. One paragraph.
FALSIFIER : find the fatal flaw in the proposal. If none, write SOUND.
ARBITER   : given the proposal and the objection, give the final answer. One line.
```
*Test: the arbiter's answer must differ from the proposer's when the falsifier found something.*
Roles that always agree are theatre, not a council.

### P5 · THE COHERENCE SCORE (C-15 — the seed with no carrier)
Canon needs a per-tick score. It must be measurable, not vibes:
```
Rate ONLY these, each 0 or 1, then output the four digits with no other text:
G  did the output serve the stated goal
H  is every claim in it supported by given material
F  is the required output form exactly respected
S  is it free of invented specifics
```
Four binary axes → a 0–4 integer. Cheap, checkable, and it composes with the existing scorer.

### P6 · TRIGGER DETECTION (C-32..C-39, the eight weathers)
One classifier call over recent state, forced to a single token:
```
Given the last N outcomes, which condition holds? Reply with ONE label only:
SATURATION | TRANSCEND-FAIL | ANOMALY | CROSS-PATTERN | ANTICIPATORY |
DECOMPOSITION | VERIFICATION-DEBT | REFLEXIVE-STEER | NONE
```
*Canon's empirical prior to check against: saturation fired 162×, verification_debt 96×,
reflexive_steer 16×, the other five never (preconditions unmet). If our distribution differs wildly,
one of us is wrong — and that is worth knowing.*

### P7 · THE CASCADE FILTERS (C-40..C-44 — all five must pass)
Five independent single-token gates, cheapest first so the common rejection is cheap:
```
TRIGGER-FIT : does the proposal address the trigger that fired?      PASS|FAIL
SCOPE       : is it inside the entity's declared objective?          PASS|FAIL
BIFURCATION : does it require a branch it cannot afford?             PASS|FAIL
ADVERSARIAL : state the strongest reason to reject it, then PASS|FAIL
BOUNDARY    : is it reachable at the current axis levels?            PASS|FAIL
```
BOUNDARY reads C-11 — **the position record we built at step 1 is what makes this filter possible.**
That is the route's first proof that the dependency graph is real.

### P8 · HYPOTHESIS GENERATION (C-45..C-51, forced to a typed action)
```
Propose ONE change to yourself. Emit ONLY this JSON:
{"type":"<objective_refine|axis_extension|new_skill|corpus_swap|bifurcation|adversarial_probe|no_op>",
 "tool":"<exact tool name from the registry>", "args":{...}, "why":"<one line>"}
```
*Canon's own receipt: 25 of 149 emitted actions (16.8%) invented a tool name; the validator caught
every one. **We must reproduce that catch rate** — if our validator catches nothing, it is not
working, it is just absent.*

---

## 3 · THE CREATURE SPACE IS COUNTABLE — and completion is the content engine

Computed from the real machinery (5 fireable parts, 177 connected rods, 3 zones, 8 tasks):

```
part-signatures (head x ordered mid x tail)        32
SPECIES        signature x rod                  5,664
LAWFUL         x zone                          16,992
TRIALS         x task                         135,936
ACTUALLY EXIST fired, on record                    62
```

And the reason completing the census matters more than authoring content:

```
+3 organs (recall, hand, ward)     3,914 signatures ->    692,778 species    x122
+5 organs (all missing)          219,202 signatures -> 38,798,754 species  x6,850
```

**You do not author creatures. You close canonical items, and the species space expands
combinatorially.** Each mid-slot organ multiplies the arrangements, because order matters — a
scaffold before a ladder is a different animal from a ladder before a scaffold, and both are
measurable. This is why the walk IS the content: 62 creatures exist, 5,664 are possible today, and
finishing the architecture puts 38 million in reach.

---

## 4 · THE RULES THE ROUTE INHERITS

1. **A step closes only on a receipt.** Ran and seen.
2. **A step may fail** — and steps 2 and 3 both did on first attempt, which is how the laws were found.
3. **Token flow is a column on every step**, never an afterthought.
4. **Where canon is silent, the gap shows.**
5. **Settle conflicts, do not paper over them.** Four are open: C-80 checkpoint, C-24 flexibilize,
   C-29 new-skill, C-79 branches.
6. **The prompts above are instruments** — if a test needs interpretation to score, redesign the
   prompt until it does not.

**NEXT: step 4 (P3, plan+critique) completes phase 0's ladder work; then PHASE 1 settles C-80, which
gates forty items.**

---

## 5 · THE CHAPTERS — the story is the dependency order

The route was derived from engineering constraints. Read it back and it is already an arc: a thing
that does not know where it is, becoming a thing that does not need you. **Nothing here is imposed on
the architecture — each chapter is the honest question its phase answers.**

| ch | phase | the question it asks | the turn |
|---|---|---|---|
| **I** | 0 · the instruments | *Where am I?* | The entity had five axes and no coordinates. Giving it a position is the first act — and the first two rungs revealed that a capability added without its precondition is pure tax. |
| **II** | 1 · the self-measure | *Is there one of me, or many?* | C-80 says every layer communicates through ONE mutable object. The substrate has MANY files. **This chapter settles whether the entity has a self or a filing cabinet.** |
| **III** | 2 · the clock | *Does my time have an order?* | Ten steps, fixed sequence. A heartbeat is not a loop; it is a loop with an order that cannot be rearranged. |
| **IV** | 3 · the floor | *What happens whether or not anyone asks?* | Six seeds fire every tick. This is the chapter of involuntary function — the entity discovering it has processes it does not choose. |
| **V** | 4 · the staircase | *When should I NOT act?* | Four conditional seeds. Restraint as a capability: the test is that they fire on their precondition and **not otherwise**. |
| **VI** | 5 · the mechanics | *Do I know when I am stuck?* | Ceiling-detect never acts — it recognises exhaustion and triggers others. The capability to notice your own ceiling is the quietest and most important in the architecture. |
| **VII** | 6 · the ops | *What can happen TO me?* | The four transcendence operations are not things the entity owns; they are transformations it undergoes. A notch lights. A corpus is replaced. A branch forks. |
| **VIII** | 7 · the innovation layer | *Can I propose a change to myself — and commit it?* | 28 items, the deepest stratum, entirely absent. This is where the proposer becomes an ACTOR rather than a describer (C-52, canon's headline claim). The chapter the whole architecture exists to reach. |
| **IX** | 8 · the engineering | *Can I choose my own body?* | `pick_for_role`: the seed selecting its own model from its own measurements. Self-determination, measured. |
| **X** | 9 · the receipt | *Do you still need me?* | Sustained unattended operation. The ending is a subtraction: the entity keeps its heartbeat while nobody watches, and the claim becomes a receipt. |

### THE PATHS — where the route genuinely forks

These are real choices, not flavour. Each changes what gets learned and in what order.

1. **C-80: build or prove.** Either implement one Checkpoint object (canon's shape) or demonstrate the
   file-set is functionally equivalent (compression). **Building teaches the architecture; proving
   teaches the substrate.** Both are legitimate; they lead to different games.
2. **Which axis first.** I chose PROMPTING because it de-risks every later measurement. Choosing
   MULTIPLICITY first would have front-loaded the council and taught coordination before discipline —
   a different creature at the same coordinate.
3. **The innovation layer: minimal or faithful.** A small honest L5 cycle reachable in one phase, or
   canon's full eight-trigger / five-filter / seven-type machine. The first ships; the second is the
   real thing.
4. **Order inside the mid-slot.** A scaffold before a ladder is a different animal from a ladder
   before a scaffold, and both are measurable. **This is the fork the PLAYER owns** — the one the
   game exists to offer.

**The story and the engineering are the same object.** That is only true because the architecture was
derived from a question rather than assembled from features — and it is the reason this walk can be a
game instead of a tutorial.

---

## 6 · THE ANCHOR CONTRACT — how any path composes, and why that is not No Man's Sky

**The honest starting state:** 33 modules exist. Exactly ONE declared a combination contract
(`bench_core`, 5 parts with slots). The rest were a library of functions — working code with no way to
compose. `aea/mind/anchor.py` is the contract, and eight modules are anchored to it.

**An ANCHOR declares six things** — five obvious, one load-bearing:

```
closes     which canonical items it embodies        -> a path can be scored against the census
slot       head | mid | tail                        -> the ONLY hard ordering law
consumes   what must already exist in the chain     -> an impossible order is refused, not run
produces   what it adds for later parts             -> the edge that makes ORDER matter
cost       MEASURED tokens, calls, wall-clock       -> provenance recorded; never estimated
requires   THE PRECONDITION - when it earns its cost
```

**The precondition is the whole design.** Steps 2 and 3 measured the same law twice: a capability added
without its precondition is pure tax, sometimes harmful. Declaring it is what makes **arbitrary order
safe** — the composition can say which organs earn their keep on ANY path, with no designer's blessing.

### Four paths, checked (all real output)

| path | order | legal | cost | closes | waste |
|---|---|---|---|---|---|
| **A · seat everything** | all 8 organs | yes | 6 calls · 549 in · 11.3s | **19/19** | **86%** |
| **B · justified** | tap→frame→recall→score | yes | 3 calls · 399 in · 3.8s | 9 | **0%** |
| **C · measure early** | tap→score→recall | **NO** | — | — | — |
| **D · a different animal** | tap→**ladder→frame**→score | yes | 2 calls · 111 in · 6.2s | 8 | **0%** |

### The finding that settles the No Man's Sky question

**COMPLETENESS IS 86% WASTE.** Path A closes every canonical item the anchored set can reach — and
wastes 86% of its tokens, because five of its eight organs have no precondition met. Path B closes half
as much for none of the waste. **Coverage and efficiency are in genuine tension**, which means there is
a real decision at every assembly and no dominant strategy.

That is the opposite of procedural emptiness. Infinite paths, but **every path gets an honest score on
two axes** — how much of the architecture it embodies, and how much of its cost it justifies.
Exploration is bounded by measurement rather than by walls.

**And the guide is not a tutorial — it is the precondition message.** When Path A wastes 86%, the
checker names each unjustified organ and why: *"pays ONLY when the rod genuinely cannot know."* The
player is taught by the diagnosis of their own build.

**Path D is the DNA point made concrete:** reach-before-frame is a *different animal* from
frame-before-reach — 2 calls instead of 3, slower, closing a different set — and it is equally
justified. Same contract, different organism. Nobody has to declare which is correct because the
measurement does not require a winner.

### What is NOT done (honest)

- **8 of 33 modules anchored.** 25 modules still have no contract — including everything in the
  innovation layer, which is where the remaining canonical coverage lives.
- **The `verify` field is null on all eight.** The contract declares tests; it does not yet run them.
- Anchored coverage is **19 of 86** canonical items. Anchoring the rest IS the route's engineering work.

---

## 7 · THE MUTATION CHANNEL — how the contract learns it was wrong

**The hole Luis found:** `requires` above reads like a law. It is a HYPOTHESIS. If my preconditions are
the only judge, then any form I failed to imagine is scored as waste and never gets to prove otherwise —
which is exactly the failure mode of designing an ecology instead of measuring one.

**So nothing gates execution.** `compose()` only PREDICTS; `observe()` records what actually happened;
a composition predicted wasteful that nevertheless PASSES is a **SURPRISE**, and surprises are the
revision queue. Variation (any order runs) · measurement (the receipt) · selection (what performed) ·
heredity (a losing precondition gets revised and the revision persists). **None of that is design.**

### The channel's first two catches were both mine

**1 · My prompt design (step 4).** I built P3 and predicted its cheap single-call form would work. It
found **zero** errors in nine trials out of nine. The library entry is corrected: P3 runs SEPARATED or
not at all.

**2 · My own waste metric.** Using the checker on its own output exposed that waste was denominated in
TOKENS only:

```
PATH D   waste  tok=0.0%   calls=50.0%   ms=89.4%   -> WORST 89%
```

The unjustified LADDER costs **5.5 seconds and a whole network call for zero tokens** — so a part whose
price is TIME was invisible to a token metric, and the checker called a 6-second detour "0% waste."
Fixed: waste is now the **worst of three dimensions**, never the convenient one.

### And then the real thing happened

With the metric fixed, PATH D reads **89% waste — and it PASSED.** Recorded:

> *"worked at 89% predicted waste — a precondition is too strict"*

Either the ladder's precondition is wrong, or the reach helps in a way I did not predict. **I do not
know which, and that is the point.** This is the first entry in the revision queue: a form nobody
designed, working anyway.

**This is where "other creatures, maybe better than ours" actually enters the system** — not as a
generous design allowance, but as a measured contradiction that the architecture is obliged to explain.
Corrupted mutations, partial versions and unintended interactions all arrive through the same door: they
run, they are measured, and if they win the contract changes.
