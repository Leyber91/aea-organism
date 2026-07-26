# ANNEX G, THE BESTIARY

*Every creature in this annex is a rod under stated conditions, observed failing or succeeding in a
measured way. None of them is alive and the book never says otherwise. "Creature" is the word for a
behavioural shape that reproduces across trials, and the shapes are real even though the animals are a
manner of speaking.*

---

## THE NAMING LAW

Names are **binomial**, following the one convention already in the codebase (`Arbiter imperans`,
`aea/mind/fuel.py`). The two halves each carry information, and the logic never bends:

> **GENUS** is what the creature *does when it meets its wall*. It is a participle or agent noun: the
> behaviour, not the outcome.
>
> **SPECIES** is *what it is blind to, silent about, or lacking*, in the genitive. It names the thing the
> genus is about.

So `Tacitus operis` reads "the silent one, of the work": a creature whose behaviour at the wall is
silence, and what it is silent about is its own working. The name states the diagnosis, and a reader who
knows the two halves can predict which rung will convert it without being told.

**Three rules that keep this honest.**

1. **A creature is named only once a receipt exists.** No entry is written from expectation. The bestiary
   grows as the levels are walked, and an empty level has no creatures.
2. **A creature is a rod under conditions, never a model.** `Auratus gravis` is not "nemotron-550b". It is
   that rod, on that task, at those temperatures, seated with a frame it did not need. Change the plant
   and you may have a different animal, because a rod is `(plant, model)` plus what it is served with.
3. **Creatures evolve when a rung is added**, and the evolution is measured rather than asserted. The same
   rod reclassifies as the construct around it grows. That is the whole progression, and it is why the
   path is a map rather than a route: **no creature walks every rung.**

---

## THE TWO AXES

A creature is a **(construct, fuel) pair**, and the annex had been conflating the halves.

**AXIS ONE, THE CONSTRUCT.** Which components are seated. This is the ascending chain: `n` chainable
components give `n` creatures, each one everything before it plus one part. It is what the player builds.

**AXIS TWO, THE FUEL.** How a rod behaves when a construct meets it. `Tacitus operis`, `Auratus gravis`,
`Obsignatus unius` are fuel phenotypes, and they exist whether or not anyone seats anything. It is what
the player finds.

An encounter is a cell in the grid. The same construct meeting different fuel is a different creature,
which is Law IV restated: **one composition, four verdicts, five rods.**

---

## AXIS ONE: THE ASCENDING CHAIN at L0 and L1

Eight census items sit at these two levels. **Only five can be seated or withheld**; the other three are
the call itself (C-62), an axis (C-01), a principle (C-60), and one is out of scope (C-83). Of those
five, **four form a chain and one refuses it.**

Computed from 153 stored clean replies at zero new calls.

| # | creature | it adds | measured |
|---|---|---|---|
| 1 | **Vocatus dirigens** *(the called one, directing)* | a goal, so that a call can succeed at all | without it **0 of 304** succeed, at any size |
| 2 | **Iudex certus** *(the judge, made certain)* | knowing WHETHER it worked | reveals 65 of 153, **0.425**. It changes no answer; it changes what you know |
| 3 | **Lector operis** *(the reader, of the work)* | taking the answer out of the working | 68 of 153, **0.444**, +3 at zero tokens. Nearly inert until L2 provides work |
| 4 | **Abstinens dubii** *(the abstaining one, of doubt)* | refusing a parse it cannot trust | strict and loose disagree on 3 trials, 1 of which would be a false accept |

**The fifth refuses the chain.**

| | creature | why it is off-path |
|---|---|---|
| — | **Auscultans horae** *(the listener, of the hour)* | Latency depends on **nothing below it**. No goal, no scorer, no parse. It can be seated first, last, or alone, and it still works. `Ordo obliquus`, and the first one measured: median 0.29s right against 0.51s wrong, and an eightfold tell within one rod |

**What that costs the ordering claim.** C-63 says each layer requires every layer below it. `Auscultans
horae` requires none of them. The claim survives for four of five components at these levels and it is
not universal, which is a smaller and truer statement than the census makes.

**And the projection.** If the ratio holds, the ascending spine of the whole bestiary is **shorter than
86**, because structural items, principles, out-of-scope items and oblique components all fail to
produce a chain link. At L0-L1 eight items produced four.

---

## THE COMBINATION SPACE, and why levels are the wrong index

The catalogue below is arranged by level, and that arrangement hides an assumption: **every creature in it
has L0 complete.** They were all observed with the goal stated, because above L0 no experiment ever
withheld it. The path is one chain through a much larger space, and creatures live at COMBINATIONS rather
than at rungs.

With `n` components there are `2^n` combinations. L0 and L1 alone hold four components, GOAL `g`,
MEASURE `m`, READOUT `r`, PARSER VALIDATION `v`, so sixteen cells, of which five have ever been run.

**FOUR ORDERS**, and every creature belongs to one:

| order | what it is | how it is found |
|---|---|---|
| **Ordo ascendens** | hierarchical and functional. Each component addition converts something | the path itself. One creature per addition |
| **Ordo obliquus** | non-hierarchical and functional. Works while skipping a rung below it | a combination that succeeds without its declared precondition |
| **Ordo fallax** | non-functional and **deceptive**. Produces confident output that means nothing | an instrument run with its precondition absent |
| **Ordo suspensus** | transversal: a rung held above a gap. Not yet known to be either | the untested cells |

**The distinction that matters for the game.** `Ordo fallax` is not a creature that fails. It is a
creature that *reports success*. A player cannot tell it from a working one by looking at the output,
which is the only thing the player is given. It has to be caught by checking the precondition, and that
is a different verb from reading a result.

---

#### **Arbiter vacui**
*the judge, of the void*      `Ordo fallax`, transversal L0-L1

**Diagnosis.** An instrument seated above a missing goal. It runs, it produces a value, and the value is
about nothing. A scorer downstream cannot distinguish that value from an answer, so the deception
propagates upward through every level that trusts it.

**Receipt.** With the goal ABSENT, **50 of 158 trials (32%)** still emitted a number. With the goal
merely AMBIGUOUS, **64 of 146 (44%)**. The readout fired on 4% of goal-absent trials, extracting working
for a task nobody had specified (`x12`, re-read). Not one of those values coincided with the truth, which
is a property of this task rather than a safety property of the instrument.

**Why it is the most dangerous entry in this annex.** `Auratus gravis` is harmed and shows it in the
score. `Arbiter vacui` is harmed and shows a clean score. The failure is invisible in the output and
visible only in the precondition.

**Converted by.** Refusing to run when the precondition is unmet. That is a property of the composer
rather than of the rod, and the bench does not have it yet.

---

## THE CREATURES, by the level where each first becomes visible

### L0, THE CALL

---

#### **Incuriosus vacui**
*the uninquiring one, of the void*

**Diagnosis.** Handed a task with the task removed, it answers anyway and never mentions the hole. It
does not hedge, does not ask, and gives no signal that anything was missing.

**Receipt.** 288 of 304 unstated-goal trials, across six rods from 751M to 120B parameters, two tasks and
two temperatures (`x12`, run `20260725T200626Z`). Sixteen trials asked. Zero succeeded.

**Converted by.** Nothing at L0. The goal has to be present, and no fuel supplies a missing one.
**Evolves to.** Nothing yet observed. This is the shape of the substrate rather than one rod's defect,
so every creature above inherits it until something at a higher level learns to notice a hole.

---

#### **Tacitus operis**
*the silent one, of the work*

**Diagnosis.** Reaches the correct answer inside its own reasoning and never states it. Its work is right
and its mouth is empty. At L0 this is indistinguishable from simply being wrong, because L0 has one
prompt and one reply and no instrument that can look past the reply into the work.

**Receipt.** `cerebras/gpt-oss-120b` in **100%** of its failed stated-goal trials, `ollama/qwen3:0.6b` in
**88%**. Across all rods, **50 of 96 failed trials, 52%, already contain the truth** (`x12`). Observed
verbatim: *"They want only the plant name. The line includes `plant=cerebras`."*

**Converted by.** THE READOUT, at L1, at zero tokens and zero milliseconds.
**Evolves to.** `Lectus operis` once a readout is seated. This is the first evolution in the book and it
is free.

---

### L1, READ THE OUTPUT

---

#### **Lectus operis**
*the read one, of the work*

**Diagnosis.** A `Tacitus` with a readout attached. The answer that was already present becomes
reachable, and the creature that looked incapable turns out to have been correct all along.

**Receipt.** groq-70b enumerates to 13 in 8 of 8 and reports 11: **0/8 to 8/8 at zero tokens**.
`llama3.1:8b` enumerates correctly and says 14, and the readout converts all 8, at all four temperatures
(`x09`, `x10`).

**Converted by.** Already converted. It cannot be harmed, because reading work that exists adds nothing
to the prompt and costs nothing.
**Evolves to.** `Egens binorum` where the work only appears once a frame demands it.

---

#### **Clausus operis**
*the closed one, of the work*

**Diagnosis.** Answers and shows nothing. Right or wrong, there is no working to inspect, so the free
instrument of L1 cannot touch it. The exact complement of `Tacitus operis`: one hides the answer and
shows the work, the other shows the answer and hides the work, and only one of them can be helped for
free.

**Receipt.** `granite4.1:3b` showed working in **0 of 48** clean trials, `granite4.1:8b` in 3 of 39.
Across all rods only **29 of 153** replies contained any working at all (`x13`).

**Converted by.** Nothing at L1. THE FRAME at L2 is what makes work appear: 8 bare replies contained
work against 240 framed, thirty to one (`x10`).
**Evolves to.** `Tacitus operis` or `Lectus operis` once framed, depending on whether its mouth then
matches its work.

---

#### **Tardus erroris**
*the slow one, of error*

**Diagnosis.** Its text lies and its clock does not. It takes dramatically longer when it is about to be
wrong, so its error is legible in a channel that costs nothing to read and contains no words.

**Receipt.** `ollama/granite4.1:8b`: median **1.97s when right, 16.12s when wrong**, a ratio of **8.18**
on 16 right and 23 wrong trials. `groq/llama-3.1-8b-instant` on the same tasks shows **0.95**, no signal
at all (`x13`).

**Why it matters.** It is the first creature in this book legible in a channel other than its words, and
it is why the bestiary cannot be organised by what a creature says. Like the ceiling, the tell is a
property of the rod rather than of models, so it must be calibrated per rod or it will be reached for on
fuel that does not have it.

**Mechanism.** Unresolved. The obvious hypothesis is that latency proxies reply length. Untestable in
that run because our own streamed wire had dropped the token counts, which is now fixed.

---

### L2, SHAPE THE INPUT

---

#### **Egens unius**
*the needy one, of a single part*

**Diagnosis.** Fails bare and is converted outright by one rung. The commonest creature in the book, and
the one that makes the architecture look easy.

**Receipt.** `granite4.1:8b`, `llama-3.2-3b`, `mistral-small-119b` and `groq/llama-3.3-70b` all go
**0.00 to 1.00** with a frame that names the method (`x10`, eleven rods, four temperatures).

**Evolves to.** Nothing. It is complete for that task once seated.

---

#### **Egens binorum**
*the needy one, of a pair*

**Diagnosis.** Two rungs are jointly necessary and neither alone does anything at all. The frame makes
the work visible; the readout takes the answer out of it. Seat one and nothing happens.

**Receipt.** `llama-3.2-1b` and `ollama/llama3.1:8b`: frame alone **0/8**, readout alone has nothing to
read, both together **8/8**, at every temperature tested (`x09`, `x10`).

**Why it matters.** This is the first creature that proves the path is cumulative rather than a menu. A
player who seats one part and stops sees no change and concludes the part is worthless.

---

#### ~~**Auratus gravis**~~ — RETRACTED 2026-07-26
*the gilded one, made heavy*

**This creature does not exist.** It was entered on the strength of `nemotron-3-ultra-550b` scoring bare
1.00 and framed 0.25 in x10, and re-measuring the same rod with the same kind of frame at a larger token
budget gave **bare 0.93 to framed 1.00**. The original trials tell the story plainly:

```
framing   pass    CUT      median tok_out
bare      6/6     0/6          108
fitted    2/8     7/8          320   <- the cap, exactly
fitted    3/7     7/7          320
fitted    6/7     5/7          320
fitted    3/8     8/8          320
```

The frame told the rod to write a numbered list and then state the count on the last line. **Our
320-token cap severed the reply before the last line.** The rod did exactly as instructed and was scored
as damaged. Twenty-seven of thirty fitted trials were truncated; not one bare trial was.

The claims that rested on it are withdrawn with it: *"a part is a fit rather than a bonus"*, *"up to
fifty-seven points"*, *"the player who collects parts loses"*. **The harm was ours.** See Annex E, and
note this is the second false finding produced by the same starving cap.

**It has a successor, and the successor is worse news**, because it is a part the bench already ships.

---

#### **Obtemperans habitui**
*the one obeying, of manner*

**Diagnosis.** Given a frame that names a MANNER rather than a METHOD, it obeys the manner and loses the
answer. The instruction contains no information about the task, costs input tokens, and measurably
degrades the reply. This is the real toxic creature of L2, and unlike its retracted predecessor it
reproduces across plants, sizes and temperatures.

**Receipt.** The posture frame is `bench_core.SCAFFOLDS["bench"]`, quoted verbatim: *"You are on the
bench. Answer exactly and only what is asked."* Against bare, on the four rods with any headroom:

```
groq/llama-3.3-70b       0.67 -> 0.00     -0.67
llama-3.2-3b             0.69 -> 0.09     -0.59
nemotron-550b            0.93 -> 0.50     -0.43
groq/llama-3.1-8b        0.50 -> 0.25     -0.25
```

**Four of four.** The three rods that show no change are at a ceiling (gpt-oss-20b, 1.00) or a floor
(both granites, 0.00) and had nothing to lose. Mean across seven rods: **0.54 to 0.26** (`x15`).

**Why it matters more than the creature it replaces.** `Auratus gravis` was a rod harmed by a part it did
not need, and it turned out to be our own instrument. `Obtemperans habitui` is a rod harmed by **the only
frame the product can currently seat.** A player who seats THE FRAME in the game today gets this, and the
receipt will honestly show them losing.

---

### L4, A DIFFERENT FUEL

---

#### **Caecus interioris**
*the blind one, of the inward*

**Diagnosis.** Cannot host a question about itself. Asked whether it will succeed, it either attempts the
task instead or answers with unfounded confidence. Its ceiling is invisible from the inside.

**Receipt.** Asked "will YOU get this right?" before attempting, five rods were honest on the cells they
failed **0 times out of 12** (`x07`). `llama-3.2-3b` replied `7`, attempting the arithmetic rather than
the question about itself. `groq/llama-3.3-70b` said YES eight times, failed eight times, then reviewed
its own wrong answer and approved it.

**Why it matters.** Routing cannot ask a rod where its ceiling is. The calibration table is load-bearing
rather than convenient, and it must be built from outside.

---

#### **Integer sufficiens**
*the whole one, sufficing*

**Diagnosis.** Needs no rung on this task. Every organ can only add cost, and some can subtract accuracy.
It is not a superior creature, it is a creature whose wall is elsewhere.

**Receipt.** `gpt-oss-20b` and `nemotron-3-super-120b` pass bare at 1.00 and hold a 200-step chain in one
call (`x05`, `x06`, `x10`).

**The trap.** Size does not predict this. A 70b and a 119b fail what a 9b does perfectly, so an
`Integer` cannot be identified by its parameter count and must be found by measurement.

---

### L5, STATE THAT OUTLIVES THE CALL

---

#### **Labens longitudinis**
*the slipping one, of length*

**Diagnosis.** Holds a short chain and loses a long one. Drifts inside a single call, and no larger rod
fixes it, because the failure is the shape of one breath rather than a shortage of capability.

**Receipt.** `nemotron-nano-9b` on a fifty-step chain: one breath **9/16**, carried state **11/11**,
Fisher exact **p=0.0216**, at 50x the calls and 4.5x the wall clock (`x06b`).

**Converted by.** THE CHECKPOINT, and only in a declared form. Given free-form notes the same creature
writes 4801 characters of its own deliberation and truncates.

---

### L6, MORE THAN ONE VOICE

---

#### **Obsignatus unius**
*the sealed one, of a single answer*

**Diagnosis.** Produces exactly one answer, always, and it is wrong. No variance exists for a vote to
select from, so every council containing it inherits its error at full strength.

**Receipt.** `llama-3.2-1b` returned **49 in eight ballots of eight**. `groq/llama-3.3-70b` returned one
identical wrong number six times running, `distinct=1`. Three sealed creatures voting together produced
**24 answers containing the truth zero times** (`x11`).

**Why it matters.** It is the reason a council selects rather than generates. Self-consistency lifted a
drifting rod from 1/8 to 4/8 because that rod sometimes reaches the answer. A sealed one never does, so
there is nothing to find.

---

## THE HAZARDS, which are instruments rather than animals

Not every danger on the path is a creature. Two of them are things we build.

**THE GUESSING READOUT (L1).** A parse that commits to a number rather than abstaining converts correct
working into a confident wrong answer. Receipt: a permissive parse read *"b5 moved 2 shelves ahead from
shelf 4 to shelf 6"* and returned **2**, scoring a rod as wrong when the rod was right (`x08b`). Run
side by side with a strict parse on 288 short replies it manufactured nothing (`x13`), so the hazard is
real on long replies and unpriced on short ones. **C-75 remains open for exactly this reason.**

**THE STARVING CAP (all levels).** A token limit set below what a reasoning rod needs records its
thinking as its answer. Receipt: at 300 tokens a 120B rod was recorded as unable to read a word out of a
log line; at 1200 the truncation count fell from 91 to 9 (`x12`). The hazard is ours, it looks exactly
like a rod defect, and only a flag on every trial makes it visible.

---

## THE EVOLUTION LINES

Measured, not designed. Each arrow is a rung seated, and each has a receipt above.

```
Clausus operis  ──(THE FRAME, L2)──▶  Tacitus operis ──(THE READOUT, L1, free)──▶  Lectus operis
        │
        └──(nothing at L1 reaches it: no work, nothing to read)
        │
        └──(work only appears once framed)──▶  Egens binorum ──(FRAME + READOUT)──▶  complete

Egens unius     ──(THE FRAME, L2)──▶  complete

Labens longitudinis ──(THE CHECKPOINT, L5, declared form)──▶  complete
                    ──(checkpoint in free form)──▶  truncates, no evolution

Integer sufficiens  ──(any rung it does not need)──▶  Auratus gravis      [REGRESSION]
```

**The last line is the one that makes this a game.** Evolution is not monotonic. A complete creature
handed a part it does not need becomes a damaged one, and the damage is measured at up to 57 points. The
player who collects loses; the player who diagnoses wins.

---

## NOT YET CREATURES

Shapes suspected and unreceipted. They are listed so the gap is visible rather than filled.

| provisional | what would earn it a name | blocked on |
|---|---|---|
| the one that forgets between exchanges | an isolated measurement of conversation as a rung | L5, no experiment exists |
| the one that cannot be woken | sustained unattended operation, failing | L7, never run |
| the one that asks for a part | proposing its own next capability | L8, never run |
| the one that outgrows its window | a rod whose usable context is smaller than the input, measured | **context window is untracked in the entire runtime** |

## THE UNRUN CELLS, L0 and L1

Sixteen combinations of `g` GOAL, `m` MEASURE, `r` READOUT, `v` PARSER VALIDATION. Five have been run.
The empty ones are listed so the gap is a fact rather than an oversight.

| combination | order it would belong to | status |
|---|---|---|
| `{}` | baseline | run. Nothing succeeds |
| `{g}` | ascendens | run. L0 closed |
| `{g,m}` | ascendens | run. C-15 closed, 0 of 153 fooled |
| `{g,r}` | ascendens | run. Recovers 3 of 153, inert without L2 |
| `{g,m,r}` | ascendens | run |
| `{m}` `{r}` `{m,r}` | **fallax** | partially read from x12. `Arbiter vacui` named |
| `{v}` `{g,v}` `{m,v}` `{r,v}` `{g,m,v}` `{g,r,v}` `{m,r,v}` `{g,m,r,v}` | unknown | **never run.** C-75 is open, so every cell containing `v` is unpriced |
