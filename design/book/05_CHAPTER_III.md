# CHAPTER III, SHAPE THE INPUT

*Level L2. Seven census items. The last free lever on the whole path.*
*Measures the SUBSTRATE that C-04, C-09, C-19 and C-23 assume. Closes none of them.*
*Measured 2026-07-26, run `20260726T001805Z`. Nine rods, four plants, four size tiers, 1008 calls.*

**The opening of this chapter was sealed before a single call was made**, at
`04_CHAPTER_III_OPENING_LOCKED.md`, sha256 `f1ed053c`. It carried five falsifiable predictions.
**Three of the four testable ones lost.** Nothing in the opening has been edited, including the parts that
turned out wrong, especially those.

---

## What was asked

Three rungs on a prompting ladder, on the same task, with only the framing varying:

```
BARE      the goal, nothing else
POSTURE   the goal plus a MANNER, quoted verbatim from bench_core.SCAFFOLDS["bench"]
FITTED    the goal plus the METHOD, step by step
```

Plus two goal-less cells, and the second exists because of a conflation caught before the run. *"To count
words: split the sentence on spaces..."* **states its objective.** A method for counting words tells the
rod a word count is wanted, so method and goal are not separable for a specific task, and a cell built
that way measures something else entirely. The cell that actually tests the prediction names a procedure
over **"units"**, never says what a unit is, and never says why the number is wanted.

## What came back

```
frame       showed work    stated    with readout
bare              0.41      0.415           0.435
posture           0.20      0.135           0.216
fitted            1.00      0.639           0.639
```

### PREDICTION 1 HOLDS, and it is the largest effect in this book

Working appears in **41% of bare replies and 100% of fitted ones.** Predicted above 60%. Every single
fitted reply, across nine rods, four plants and two temperatures, showed its working. A frame that names a
method does not merely help a rod, it changes what the rod emits.

That closes the question L1 could not answer. `Lector operis` sat idle at L1 with nothing to read, and
this is the machinery that supplies it.

### PREDICTION 2 FAILS, and the chain was wrong

Under a fitted frame the readout adds **0.0 points**, stated 0.639 against readout 0.639. Predicted above
ten.

The reason overturns a structure this book built two chapters ago. **When the frame makes a rod show its
work, the rod also states the answer correctly.** The mute condition, work right and mouth wrong, was
caused by the absence of a frame rather than repaired by a readout. So `Lector operis` is not *enabled* by
`Monstrans operis`, it is **made redundant** by it, and the chain that has FRAME handing material to
READOUT is backwards.

The readout keeps its value exactly where it was measured: on **unframed** replies, where it recovers
0.415 to 0.435. It is a repair for a rod you cannot frame, not a stage above framing.

### PREDICTION 3 FAILS, and a creature is retracted

Predicted: at least one rod loses more than ten points to a fitted frame. **Not one did.**

```
llama-3.2-3b      -0.010          granite4.1:8b   +0.500
nemotron-550b     +0.067          granite4.1:3b   +0.531
groq-70b          +0.083          groq-8b         +0.239
```

`nemotron-3-ultra-550b` is the rod this prediction was written for. In x10 it scored bare 1.00 and framed
0.25, and that single row put **`Auratus gravis`** in the bestiary as the most dangerous creature in the
book. Here the same rod, the same kind of frame, goes **0.93 to 1.00.**

The difference between the runs is `max_tokens`: 320 then, 1200 now. The x10 trials say the rest:

```
framing   pass    CUT      median tok_out
bare      6/6     0/6          108
fitted    2/8     7/8          320   <- the cap, exactly
fitted    3/7     7/7          320
fitted    6/7     5/7          320
fitted    3/8     8/8          320
```

**Twenty-seven of thirty fitted trials were truncated. Not one bare trial was.** The frame told the rod to
write out a numbered list and then state the count on the last line, and our cap severed the reply before
the last line arrived. The rod obeyed precisely and we recorded it as damaged.

`Auratus gravis` is withdrawn, and so is everything built on it: *a part is a fit rather than a bonus*,
*up to fifty-seven points*, *the player who collects parts loses*. **The harm was ours**, and it is the
second false finding produced by the same starving cap.

**What survives of that idea is weaker and still real.** The rods that gain from a frame are the ones that
fail without it, granite 3b and 8b both at 0.00 bare. The rods that already pass gain almost nothing:
+0.067 and +0.083. So a part with an unmet precondition **buys nothing**, rather than costing something.
That is a design constraint, and a much quieter one than the book had yesterday.

### PREDICTION 5 FAILS, and Chapter I earns a second correction

A prompt that names a procedure over "units", with no goal, no task named and no mention of words:

```
25 of 33 clean trials succeeded
```

Seventy-six percent, against L0's **0 of 304**.

Chapter I concluded that goal-presence is a hard floor no fuel can climb over. That conclusion was drawn
from calls where **both** the goal and any procedure were withheld. Supply one without the other and it
works. So the floor is real and it was misnamed:

> **A call must specify WHAT TO COMPUTE. A goal and a procedure are two ways of doing that, and either
> one suffices.**

> #### REFINEMENT, entered 2026-07-26 after the organisms were assembled
>
> *"Either one suffices"* is true and it hides the size of the difference. Run as assembled organisms on
> pinned fuel, with nothing else seated:
>
> ```
> call + goal     0.38
> call + frame    0.65        27 points, well outside the 0.10 noise band
> ```
>
> Both beat the 0.00 that a call with neither produces, so both satisfy the law. **They are not
> interchangeable.** A procedure is worth twenty-seven points more than an objective, and adding the
> objective to a procedure moves the number by 0.01, inside the band.
>
> So they are alternatives at one rung rather than two rungs, and **the stronger one currently sits three
> positions higher in the spine than the weaker.** Whether that makes `goal` a rung at all is what the
> ordering lattice is measuring.

Which is a better law, because it explains the L0 result rather than merely restating it. And the
companion cell measures the other direction: the task's own method, with the goal sentence removed,
succeeded **33 of 34**. A method carries its objective almost perfectly.

## The real toxic creature, and it is one we ship

The posture rung is not a null result. Against bare, on the four rods with any headroom at all:

```
groq/llama-3.3-70b       0.67 -> 0.00     -0.67
llama-3.2-3b             0.69 -> 0.09     -0.59
nemotron-550b            0.93 -> 0.50     -0.43
groq/llama-3.1-8b        0.50 -> 0.25     -0.25
```

**Four of four.** The three rods showing no change sit at a ceiling (gpt-oss-20b, 1.00) or a floor (both
granites, 0.00) and had nothing to lose. Mean across seven rods: **0.54 to 0.26**.

The instruction is `bench_core.SCAFFOLDS["bench"]`, which is the only frame the product can currently
seat: *"You are on the bench. Answer exactly and only what is asked."* It names no method, carries no
information about the task, costs input tokens, and takes a seventy-billion parameter rod from
two-thirds correct to **zero**.

So the law of this level is sharper than "framing helps":

> **A frame that names a METHOD is free or better. A frame that names only a MANNER is actively harmful.**
> The difference is whether the words tell the rod what to do or only how to seem.

**`Obtemperans habitui`**, *the one obeying, of manner*, replaces the creature this chapter retracted, and
it is worse news, because `Auratus gravis` was our own instrument and this one is in the shipped code.

## What closes, and what does not

| item | the census definition | what this chapter measured | state |
|---|---|---|---|
| C-04 | *"axis.R"* | framing effects across nine rods | **OPEN.** It is a coordinate axis |
| C-09 | *"as C-06"*, the Path ladder L0 to L5 | a three-rung prompting ladder | **OPEN.** The census ladder has six levels and names them; this measured three of our own |
| C-19, C-23 | crystallize, and its mechanic | nothing | **OPEN.** Never approached |
| C-53, C-54, C-55 | `working_objective.set` / `.append` / `.consolidate` | nothing | **OPEN, and they do not exist.** `grep -rn working_objective aea/` returns one hit, in this experiment's own docstring. They are absent rather than compressed |

**L2's substrate is measured. All seven items remain open**, and three of them have no implementation to
test. Prediction 4 in the sealed opening concerned `append` without `consolidate`, and it could not be
run for that reason.

---

## WHAT THE JOURNEY BROUGHT

We came for a lever and found two, pointing opposite ways.

**The frame that names a method is the strongest thing in this book.** It takes working from 41% to 100%,
converts rods that fail outright, and costs a rod that does not need it almost nothing. **The frame that
names a manner is the most harmful thing in this book**, and it is the one already in the repository.

**Three of four sealed predictions lost**, and the losses were worth more than the win. The one that
held confirmed something already suspected. The three that failed retracted a creature, reversed a link
in the chain, and corrected the previous chapter's headline law. **A chapter that had gone four for four
would have taught nothing**, and the only reason any of it surfaced is that the predictions were written
down before the run and could not be quietly adjusted afterwards.

**The retraction is the lesson to carry.** `Auratus gravis` was measured, receipted, named, entered in an
annex, and built into a game mechanic. It took a second experiment at a larger token budget to discover
that the danger was our own cap. **Everything in this book is one better-instrumented run away from that,
and the only defence is to keep running them.**

## THE QUESTION FOR CHAPTER IV

L2 was the last free lever. From here every gain costs a call, and L3 is the first place where you pay:
a second call on the same fuel, looking at the first one's answer.

> **When a rod is confidently wrong and no framing moves it, can a second look on the same fuel repair it,
> and what does it cost when there was nothing to repair?**

The prior evidence is narrow and unflattering: a critic took a 9b from 0/8 to 5/8 on a trap question, at
**6.4x the tokens**, and on four of five rods there was nothing to repair at all. That is the shape this
chapter should expect, and the sealed opening for Chapter IV will say so before the calls are made.

**And one thing changes about how the walk proceeds.** This book has been measuring fuel, which is the
ground the architecture stands on rather than the architecture. The entity itself is standing, dormant,
with a goal stack in `self.json`, a tick loop, a memory that survives restart and a watcher on every tick.
It has never once been run on **stated fuel**. Until it is, its own history records several different
organisms wearing one name, and the census items cannot be closed by any amount of work on a bench.
