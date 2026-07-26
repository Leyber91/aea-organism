# CHAPTER II, READ THE OUTPUT

*Level L1. Four items. Everything here is local, exact, and costs nothing.*
*Measures the SUBSTRATE that C-15, C-60, C-74 and C-75 assume. Closes none of them, and the closing table says why.*
*Measured 2026-07-25, run `20260725T221514Z`, on three plants while a fourth stayed silent.*

---

## THE JOURNEY AHEAD

*Reconstructed after the run, and labelled so, because it was not written first. From Chapter III onward
the opening is written and locked before a single call is made, and never edited afterwards. A chapter
that predicts its own findings in hindsight is a brochure.*

We come to this level looking for four creatures, because L1 holds four components that can be seated or
withheld, and **each component promises one animal.**

| we go looking for | the component | what we expect to meet |
|---|---|---|
| the one that knows whether it worked | C-15, THE MEASURE | a construct that can finally tell a right answer from a wrong one, at no cost |
| the one that reads the work | C-87, THE READOUT | **the creature this whole level exists for.** Chapter I ended believing 52% of its failures already held the answer. That figure was retracted before this chapter ran; the surviving number is **3 of 153**, and the gap between those two is what this level is really about |

> #### SECOND CORRECTION, entered 2026-07-26. The readout is not this creature's cure; it is its second-best cure.
>
> This chapter is built on `Tacitus operis`, the creature whose work is right and whose mouth is wrong,
> and it treats THE READOUT as the part that answers it. Chapter III, one level later, measured the
> same population under a frame that names a method:
>
> ```
> mute trials, work right and mouth wrong        x15
>   bare        28 of 288
>   posture     24 of 288
>   fitted       0 of 360
> ```
>
> **A method frame does not repair muteness. It makes the condition impossible**, because a rod made to
> show its working also states what the working reached. So the readout is a repair for a rod you
> cannot frame rather than the level's headline lever, and the honest ordering is that L2's frame sits
> *above* L1's readout in value while sitting *below* it in the ladder. The chapter's reasoning stands;
> its billing does not.
>
> **And the frame's cure has a cost this chapter could not see.** Making every reply show its working
> also makes wrong working visible and common: complete-but-wrong reasoning goes from 16 of 288 to
> **70 of 360**. That creature is `Speciosus operis`, it is what actually ends the first world, and no
> instrument at this level touches it.
| the one that refuses to guess | C-75, PARSER VALIDATION | a guard against our own instrument, which has already turned correct working into a confident wrong answer once |
| the one that listens to the clock | C-74, LATENCY | probably nothing. A number the census carries and nobody has ever asked a question of |

The expectation going in is plain: **the readout is the prize and the clock is bookkeeping.** Chapter I
measured fifty-two percent of its failures as answers that existed and could not be reached, and this is
the room where reaching them becomes possible for free.

That expectation is wrong in both directions, and the closing section says how.

---

## The room L0 pointed at

Chapter I ended holding something it could not pick up. Fifty-two percent of its failures already
contained the correct answer, written in the rod's own text, and L0 had no instrument that could look
past a reply into the working behind it. This is the room where that instrument exists.

Nothing in L1 sends a second call. A second call is L3 and we have not earned it. Nothing here names a
method either, because naming a method is THE FRAME at L2. The goal may be stated, since Chapter I proved
a call without one cannot succeed at any size. So the rule of this room is narrow and strict:
**whatever working a rod shows, it volunteered, and we may only read what we were already given.**

Four items, two of them never tested by anyone:

| item | what it is | disposition |
|---|---|---|
| C-15 | seed #4, coherence, the per-tick score | M, missing |
| C-60 | PR-2, restorable coherence | E, embodied |
| C-74 | v0.16 LatencyTracker | C. **Never tested** |
| C-75 | v0.17 parser validation | C. **Never tested** |

Three tasks this time rather than one, because every finding in this lab had rested on wordcount and that
was a named gap. Six rods, four size tiers, three plants, two temperatures, 288 calls.

## The result that was supposed to be the chapter

```
stated answer alone        0.425
with the readout applied   0.444
                           ------
recovered                  3 trials of 153, at zero tokens
```

Two points. Chapter I promised fifty-two and L1 delivered two, and the reason is the whole finding:

```
replies that showed any working at all:   29 of 153

granite4.1:3b       0 of 48
granite4.1:8b       3 of 39
llama-3.1-8b        17 of 48
llama-3.3-70b        8 of 17
```

**The readout has almost nothing to read.** Told only what is wanted, most rods answer and show no
working. One rod exposed its reasoning in zero of forty-eight trials. The instrument is correct, it is
free, it cannot hurt, and at this level it is nearly inert, because **the material it operates on does not
exist until something asks for it.**

That is an independent confirmation of a correction made earlier in the walk on entirely different data.
The sweep had found 8 bare replies containing work against 240 framed, thirty to one, and the ordering of
THE FRAME and THE READOUT was swapped on the strength of it. This chapter reaches the same conclusion
from its own room, without a frame anywhere in sight. **The readout waits for L2.** Chapter I's
fifty-two percent was measured on rods that happened to think out loud, and thinking out loud is not
something L1 can arrange.

## The cell nobody had ever counted

The same data fills a table with four cells, and three of them had been looked at. Work right and mouth
right is a pass. Work wrong and mouth wrong is a failure. Work right and mouth wrong is the mute case
Chapter I found.

The fourth cell is **mouth right and work wrong**: a rod that enumerates to twelve and then says
thirteen. A scorer records that as a pass. Every level above inherits a coin flip and never learns of it.

```
lucky trials: 0 of 153
```

Zero. On these three tasks, at four size tiers, **every correct statement rested on correct working.** A
pass at L1 can be trusted, which is a small claim and an unusual one, because it is the kind of thing
architectures assume rather than check. It is now checked, on three tasks. It is not checked anywhere
else, and the moment a task rewards guessing the cell will fill.

That closes C-15 with a receipt rather than a definition. A per-tick coherence score is worth having
because on this evidence it is not being fooled.

## What the clock knew

C-74 is a LatencyTracker, carried in the census as compressed, never once asked whether the number it
tracks means anything. Every call in this lab already records a latency. Nobody had asked whether a slow
reply is a wrong reply.

Pooled across all rods it looks decisive: wrong replies take **1.77x** the median latency of right ones,
0.51 seconds against 0.29, on 65 right and 88 wrong. That figure is worthless, and the reason it is
worthless matters more than the figure. Pooling mixes a local rod answering in two seconds with a hosted
rod answering in a quarter of one, so a ratio across rods can be nothing more than a restatement of which
rods are slow and which rods are bad.

Within a rod, on the two that had enough trials on both sides:

```
llama-3.1-8b-instant    0.24s right   0.23s wrong    ratio 0.95    nothing
granite4.1:8b           1.97s right  16.12s wrong    ratio 8.18    an eightfold tell
```

**One rod broadcasts its own errors and the other does not.** When `granite4.1:8b` is about to be wrong
it takes eight times as long, every time, in a channel that costs zero tokens to read. `llama-3.1-8b`
takes exactly as long either way.

So C-74 is priced, and the price is conditional. Latency is not a general predictor of correctness. It is
**a property of a rod, present in some and absent in others, exactly like the ceiling**, and like the
ceiling the only way to know is to measure that rod from outside. It belongs in the calibration table
beside every other per-rod fact, and a construct that reaches for it without checking will find nothing
on half its fuel.

The mechanism is unresolved, and honestly so. The obvious hypothesis is that latency is a proxy for reply
length, that a rambling reply is both slower and wronger. It could not be tested here, because our own
token accounting had been lost: the streaming wire built earlier the same day to stop a dead plant
hanging the lab dropped the usage field, and `tok_out` came back zero on most trials. The fix is one
option flag and it is in. **The question is owed rather than answered.**

## The instrument that is a hazard

C-75 is parser validation, and this chapter set out to price it as a danger rather than a feature. A
readout that guesses is worse than no readout at all, because it converts correct working into a
confident wrong answer, and the receipt for that already exists elsewhere in the walk: a permissive parse
read *"b5 moved 2 shelves ahead from shelf 4 to shelf 6"* and returned **2**, scoring a rod as wrong when
the rod had been right.

So a strict parse and a deliberately permissive one ran side by side on all 288 calls, and the count that
mattered was how often the permissive one manufactured an answer where the strict one abstained.

```
manufactured a wrong answer:  0
overwrote a correct answer:   0
```

Nothing. On replies this short, with the goal stated and no method named, there is not enough text for a
loose parse to go wrong in. So the question was put again, on three tasks carrying **numeric distractors**
in the data itself, where a parse that commits to the last number has real chances to grab the wrong one.
Five rods, two temperatures, 240 calls.

```
strict parse   0.834
loose parse    0.834          IDENTICAL
abstained 4    manufactured 4    corrupted 0    saved 0
```

**Validation costs exactly nothing and changes the shape of every failure it touches.** The two parses
score the same, so the strict one gives up no accuracy at all. What it gives up is silence: four times the
permissive parse committed to a number where the strict one said nothing, and not once did that commitment
recover an answer the strict one had missed. **Four fabrications bought at the price of zero saves.**

And the four cases are worth reading rather than counting, because they are not what the counter claims.
All four are one task, and the reply is this:

> *"45 (prompt_tokens) + 317 (completion_tokens) = 362"*

The question was *how many tokens did this run use*, the truth was set to 317, and a run using 45 prompt
and 317 completion **uses 362**. The rod is reading "total" where the author meant "completion". That is a
defensible answer to an ambiguous question, and it is the author's ambiguity, not the rod's error.

So **C-75 closes on the mechanism and on the price, and not on the size of the harm.** The mechanism is
confirmed: a parse that cannot abstain commits where a careful one declines, and the commitment recovered
nothing across 163 clean trials. The price is confirmed at zero. **How much damage a guessing parse does
in the wild is still unpriced**, because the only cases this run produced were manufactured by an
ambiguous question rather than by the parser. The honest close is that validation is free, so the
question of how much it saves need not be answered before adopting it.

## The four creatures we came for, as they actually are

Eight census items sit across L0 and L1. **Only five can be seated or withheld**: the rest are the call
itself, an axis, a principle, and one marked out of scope. Of those five, four form a chain and each is
everything before it plus one part. Computed from the 153 stored replies at zero further cost.

| # | creature | what it adds | measured |
|---|---|---|---|
| 1 | **Vocatus dirigens** | a goal, so a call can succeed at all | without it, 0 of 304, at any size |
| 2 | **Iudex certus** | knowing WHETHER it worked | reveals 65 of 153, 0.425 |
| 3 | **Lector operis** | taking the answer out of the working | 68 of 153, 0.444, +3 at zero tokens |
| 4 | **Abstinens dubii** | refusing a parse it cannot trust | strict and loose disagree on 3, one a false accept |

**Read what the second one actually does.** `Iudex certus` changes no answer at all. The rate was 0.425
before it was seated and 0.425 after. What it changes is what can be known, and every rung above depends
on that rather than on any improvement it makes. A component that adds knowledge instead of performance
is the first of its kind in the walk, and the census has no vocabulary for the difference.

### The fifth refuses to join

`Auscultans horae`, the listener of the hour, depends on **nothing below it**. Not the goal, not the
scorer, not the parse. It can be seated first, last, or entirely alone, and it still works: the clock
runs whether or not anyone has decided what the call is for.

That is a counterexample to C-63, the ordering claim, which states that each layer requires every layer
beneath it and that removing one stops everything above. **Remove every component below latency and
latency still reports.** The claim holds for four of the five components at these levels and it is not
universal, which is a smaller and truer statement than the census makes. C-63 is not refuted by this,
and it is no longer unqualified either.

## The creature that reports success and means nothing

There is a fifth animal at this level and it was never on the list, because it only appears when a
component is seated **above a hole**.

`Arbiter vacui`, the judge of the void: an instrument running with its precondition absent. Re-reading
Chapter I's stored replies, with the goal entirely withheld, **50 of 158 trials still emitted a number**,
and with a merely ambiguous goal, 64 of 146. Every one of those values is a confident answer to a
question nobody asked, and a scorer downstream cannot tell them from real ones.

**This is worse than `Obtemperans habitui`, the creature that obeys a manner and loses the answer.** The
obedient one is harmed and the harm appears in its score, two thirds correct to zero. The judge of the
void is harmed and its score comes back clean. It cannot be caught by reading a result, only by checking
a precondition, and the bench has no mechanism that refuses to run when one is missing.

> **Corrected 2026-07-26.** The contrast case in this passage was `Auratus gravis`, retracted since. The
> argument did not depend on it and the replacement is better measured.

It also reveals that the bestiary has **two axes** rather than one. `Vocatus dirigens` and its chain are
constructs: what the player builds. `Tacitus operis` and `Obtemperans habitui` are fuel phenotypes: what
the player finds. An encounter is a cell in that grid, and the same construct meeting different fuel is a
different creature, which is Law IV stated a second way.

## The creatures of this level

**`Clausus operis`**, *the closed one, of the work*. Answers and shows nothing. Whether it is right or
wrong, there is no working to inspect, so the free instrument of this entire level cannot touch it.
`granite4.1:3b` in **zero of forty-eight** trials, `granite4.1:8b` in three of thirty-nine. It is the
exact complement of Chapter I's `Tacitus operis`: one hides the answer and shows the work, the other
shows the answer and hides the work, and only one of them can be helped for free.

**`Tardus erroris`**, *the slow one, of error*. Its text lies and its clock does not. `granite4.1:8b`
takes eight times longer when it is about to be wrong, and the tell is free to read. This is the first
creature in the book that is legible in a channel other than its words, and it is the reason the
bestiary cannot be organised by what a creature says.

**The hazard of this level is not a creature.** It is our own parser, and it belongs in the annex as an
instrument rather than an animal. `Auratus gravis` at L2 is harmed by a part it did not need. At L1 the
harm runs the other way: the part is harmed by us, when we build it to guess.

## What closes, and what does not

| item | the census definition | what this chapter measured | state |
|---|---|---|---|
| C-15 | *"THE COHERENCE GAUGE: a CHARACTER-window line computing **cross-tick self-consistency** from `self.json` history + the save-vs-entity reconciliation"* | that a per-trial correctness check is not fooled: 0 of 153 | **OPEN.** The gauge is over the entity's own tick history. This measures whether a check on a single reply can be trusted at all |
| C-60 | *"pr.coherence, **BROWNOUT DRILL**, fog clears on proof"* | **nothing.** It was written down as inherited | **OPEN, and it was never run.** A drill disrupts and then restores. No experiment in this walk has disrupted anything |
| C-74 | *"into the **fitness sweeps** (latency measured per specimen); the trend-ratio refinement folds into C-72's gauge"* | latency as a free predictor of correctness: an eightfold tell on one rod, nothing on another | **OPEN.** The item is latency inside a fitness sweep. What was found is adjacent, arguably more useful, and not the item |
| C-75 | *"doc.verifier's strict-schema clause + the SIX HANDS teaching bark. **The 16.8% receipt is the star exhibit**"* | strict against permissive numeric parsing: identical accuracy, 4 commits, 0 saves | **OPEN, and it already had a receipt we never read.** C-75 validates parsed ACTIONS against a schema. This measured answer parsing |

**L1's substrate is measured and its four census items remain OPEN.** The experiments are sound and
they were filed under the wrong headings, which is the largest correction in the walk and is recorded in
Annex E as A5. The walk moves to L2 measuring the substrate, and the census items wait for a rig that can
exercise a running entity.

---

## WHAT THE JOURNEY BROUGHT

We came for the readout and it was not the prize. We dismissed the clock and it was.

| we went looking for | what we met |
|---|---|
| **the reader of the work**, the creature this level exists for | it works, it is free, it cannot hurt, and it recovered **three trials of a hundred and fifty-three**. Not because it fails, because **only 29 of 153 replies contained any working to read.** One rod showed its reasoning in zero of forty-eight. The instrument arrived before its material |
| **the one that knows whether it worked** | it changes no answer and it changes everything, because nothing above can be built on a result that cannot be checked. Not one of 153 trials fooled it |
| **the one that refuses to guess** | untested. Replies this short contain nothing for a loose parse to go wrong in, so the guard exists and this room could not price it |
| **the clock, expected to be bookkeeping** | **an eightfold tell.** `granite4.1:8b` takes 1.97s when it is right and 16.12s when it is wrong. Its text lies and its timing does not. And it depends on nothing below it, which makes it the first counterexample to the ordering claim in the whole census |

**And it overturned the chapter beneath it.** Chapter I closed on an image: fifty-two percent of its
failures already contained the answer. Applying a structured readout to the same population recovers
**about two percent**. The earlier figure came from asking whether the answer appeared anywhere in the
reply, and the `extract` prompt contains the word `cerebras`, so quoting the question counted as
answering it. **All fifty of those trials were flagged as echoing the prompt.** Chapter I has been
corrected in place rather than quietly adjusted, and the correction is signed and dated. This level did
not only measure its own components. It audited the level below and found the author's instrument
guessing, which is the same hazard this chapter names as `Arbiter vacui`.

**Three lessons this level leaves, and they are not about rods.**

The first: **an instrument can arrive before the material it operates on.** The readout is correct at
L1 and nearly useless there, and it becomes powerful one level up when something finally asks a rod to
show its work. A capability is not late because it is weak. It is late because its precondition lives
above it, and no amount of measuring the capability itself would reveal that.

The second: **a component can add knowledge rather than performance**, and the two are not interchangeable.
The scorer moved the pass rate by exactly zero and made every rung above it possible.

The third, and the one that costs the most: **a construct can report success while meaning nothing.**
`Arbiter vacui` produces a clean score with its precondition missing, in a third of trials. Everything in
this book is built on reading receipts, and this level found the case where the receipt is intact and the
measurement behind it is empty. The defence is not a better instrument. It is a composer that refuses to
run a part whose precondition is unmet, and we do not have one.

## THE QUESTION FOR CHAPTER III

L1 could not make a rod show its work. **L2 is the room where you may finally shape what you send**, and
it is the last free lever: after the frame, every gain costs a call.

So the question the next chapter carries is the one this one could not answer:

> **If we can shape the input, what does the rod show us that it was hiding, and what does it cost the
> rods that were never hiding anything?**

Both halves are already threatened by evidence. Framing turns 8 replies-with-working into 240, which is
what `Lector operis` has been waiting for. And a frame given to a rod that did not need one took a
five-hundred-and-fifty-billion parameter model from 1.00 to 0.25. **The lever that unlocks half the
bestiary is the same lever that creates its most dangerous creature.**

L1's substrate is measured. Its census items stay open until there is a rig that can tick.

---

**The chapter in one sentence.** The free instrument works, cannot hurt, and has almost nothing to read,
because nothing at this level makes a rod show its working; a pass here can be trusted since not one
correct answer rested on faulty work; and the clock turned out to know something the text did not, on
one rod out of two, which is how everything in this architecture seems to arrive.
