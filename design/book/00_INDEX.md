# THE WALK, index

*A record of completing an Autonomous Entity Architecture, one rung at a time, on a machine that was
already running. Every measurement in this book was taken. Nothing that failed has been quietly rounded
up into a success.*

**Begun 2026-07-25.** Destination: 86 canonical items, walked in the order necessity admits them.

---

## THE CORRECTION THIS EDITION EXISTS FOR

The first edition had ten chapters and each one was a **group of components**: Chapter IV was "C-12 to
C-17", Chapter VIII was "C-31 to C-58". That is a filing system. It answers the question *where does this
item live*, and it cannot answer the question the book is actually about, which is *what forces the next
thing to exist*.

Measurement broke the filing system in a single day. Six placements were wrong, and all six were wrong in
the same direction:

| what was wrong | how it was found |
|---|---|
| THE FRAME and THE READOUT were in the wrong order | 8 bare replies contained visible work against 240 framed, so the readout has nothing to read until the frame makes work appear |
| THE CONVERSATION was missing from every ladder | `aea/organs/converse.py` runs at 531 lines and has held a real spoken conversation. No census item, no journey row, no registry entry |
| L5's stated wall was the conversation wall | *"the second exchange cannot know what the first concluded"* describes a context window, filed under a persistent checkpoint |
| C-84 sat in two rungs at once | the journey put it in RECALL, the hierarchy at L4, and nothing checked |
| THE WARD had no item | routing a draw by a privacy constraint is not one of the 86 |
| the self-representation floor had no item | a rod that cannot host a question about itself is a capability floor, and the audit had no row for it |

**Every miss was something that only appears when you build or watch. None could have been found by
reading the document more carefully.** So the chapters are now rungs, ordered by what forces what, and the
book is the chronicle of a single straight path from the first reply to a thing that runs unattended. It
is the same line the player walks, which is why it can be written at all.

---

## THE SECOND CORRECTION: ONE CHAPTER IS ONE LEVEL

The first edition's chapters cut across the hierarchy. Chapter I closed C-11 and rungs on C-06 to C-10,
which sit at **L5, L3, L5, L6, L2 and L7**: five levels in one chapter. Chapter II closed C-80, C-15, C-16
and C-77, sitting at **L5, L1, L4 and L6**: four levels in one chapter. Both are readable and neither is a
level, so neither could ever close one.

`design/THE_LINEAR_HIERARCHY.md` is the spine, because it is the only document that places all 86 items
exactly once. **Nine levels, nine chapters, walked in order, one at a time.** The thirteen journey rows
are beats *inside* a chapter rather than chapters of their own.

| ch | level | the wall that forces it | items | cumul | untested | beats inside it |
|---|---|---|---|---|---|---|
| **I** | **L0** THE CALL | you have nothing else; the prompt is the only control | 4 | 4 | **2** | THE CONNECTION, THE CALL |
| **II** | **L1** READ THE OUTPUT | you cannot tell whether it worked, and the answer may be in the work | 4 | 8 | **2** | THE MEASURE, THE READOUT |
| **III** | **L2** SHAPE THE INPUT | it fails and the prompt is the last free lever | 7 | 15 | **7 open** | THE FRAME. Substrate measured; 3 items have no implementation |
| **IV** | **L3** A SECOND CALL, SAME FUEL | it is confidently wrong and no framing moves it | 7 | 22 | **4** | THE CRITIC |
| **V** | **L4** A DIFFERENT FUEL | this rod has a ceiling here and another does not | 11 | 33 | **8** | THE LADDER |
| **VI** | **L5** STATE THAT OUTLIVES THE CALL | nothing below accumulates | 15 | 48 | **12** | THE CONVERSATION, THE CHECKPOINT, RECALL |
| **VII** | **L6** MORE THAN ONE VOICE | one voice cannot disagree with itself | 8 | 56 | **6** | THE COUNCIL |
| **VIII** | **L7** TIME WITHOUT AN OPERATOR | everything below waits for someone to press go | 9 | 65 | **7** | THE TICK |
| **IX** | **L8** IT CHANGES ITSELF | it can run forever and still only do what it was built to do | 21 | 86 | **19** | THE CASCADE |

**64 of 86 items are untested.** A chapter closes when its own level's items carry receipts, and the walk
does not move up until it does. The evidence gathered so far is real and it is scattered across five
levels at once, so it is inherited rather than credited: each chapter re-states which of its items an
earlier experiment already closed, and measures the rest.

**Two chapters were archived rather than deleted**, because both are readable and neither is a level:
`_ARCHIVE_02_CHAPTER_I_first_edition.md` (spans L2, L3, L5, L6, L7) and
`_ARCHIVE_03_WHAT_STAYS_cross_level.md` (spans L1, L4, L5, L6). Their receipts are inherited by the
levels they belong to, credited in each chapter as it is walked.

**The rule that makes this sequential.** One level per chapter, one chapter at a time. An experiment that
spans levels measures a construct rather than a rung, and a construct that works tells you nothing about
which part of it was necessary. That confusion is what produced a five-level Chapter I.

---

## THE THIRD CORRECTION: THIS BOOK MEASURES THE SUBSTRATE, NOT THE CENSUS

Entered 2026-07-26, and it is the largest correction in the walk.

Chapters I and II were written as though they closed census items. They do not. Every experiment quoted
the item's **label** from `hierarchy.json`, four words long, and never its **definition** in
`design/A15_FULL_COVERAGE.md`. Read side by side, they are different constructs:

| item | what the census actually says | what was measured |
|---|---|---|
| C-62 | *"the premise itself: completing the entity = answering what must exist for indefinite growth"* | a call happens and a reply comes back |
| C-01 | *"axis.P, pentagon, r250"* — a coordinate axis | eight rods on five tasks |
| C-15 | *"THE COHERENCE GAUGE: cross-tick self-consistency from `self.json` history + the save-vs-entity reconciliation"* | whether one answer was right |
| C-60 | *"pr.coherence, BROWNOUT DRILL, fog clears on proof"* | nothing. It was written down as inherited |
| C-75 | *"doc.verifier's strict-schema clause... **the 16.8% receipt is the star exhibit**"* | strict against loose numeric parsing |

**C-75 already had a receipt and nobody read it.** C-60 is a drill, disrupt then restore, and was never
run. C-15 is a gauge over the entity's own tick history.

**The reason is structural rather than careless.** Those definitions share a vocabulary: `self.json
history`, `cross-tick`, `save-vs-entity reconciliation`, `verb.observe's goal-stack ledger`,
`doc.verifier`, `brownout drill`. **Almost every census item is about the entity, not about a rod.** A
bank of rods cannot exercise a tick history or a persistent goal stack, because the thing under test is
the machine that has been running on this desk, and what this lab built tests **the floor underneath the
architecture**.

So the book is reframed rather than rewritten:

> **Each chapter measures the SUBSTRATE that a level's census items assume.** It quotes the real
> definition, states what the substrate does underneath it, and leaves the item **OPEN**. An item closes
> only when it is tested against the entity, with its ticks and its state, on a rig that does not exist
> yet.

**The measurements survive this intact.** Goal-presence as a hard floor across 304 trials, the readout
inert without a frame, latency broadcasting error at eightfold on one rod, a council unable to generate a
signal it does not already contain: none of that was in the project before, all of it reproduces, and
none of it was ever a census item. **The findings were real and the filing was wrong.**

**One class of work was valid all along.** Candidates found by building carry no prior definition to
violate, because we wrote them: THE READOUT, THE WARD, the self-representation floor, noticing an absent
goal, precondition checking. Those five are measured against their own definitions and they stand.

---

## THE BESTIARY, and why the path is a map rather than a route

**No creature walks every rung.** Which rungs a creature needs is a property of that creature, and the
measurements say so: eleven rods on one task across four temperatures produced ten distinct shapes, and
two of them are shapes nobody designed.

The full catalogue, with binomial names, receipts and measured evolution lines, is **Annex G**. Three of
its findings govern how every chapter is written:

**`Integer sufficiens` is why this is a game rather than a tutorial.** A part is a fit rather than a
bonus. Seat the validation guard into `nemotron-550b`, the rod that needs nothing, and it goes **7 of 7
correct to 0 of 7** — three times over, and every point is lost to forced abstention rather than to a
wrong answer. The part that makes other creatures honest makes this one refuse to speak. That number was
measured rather than balanced. The player who collects parts loses; the player who diagnoses wins.

> **Corrected 2026-07-26.** This paragraph previously carried `Auratus gravis`, *"bare 1.00 to framed
> 0.25, damaged at every temperature by up to fifty-seven points."* **That creature was retracted on the
> same date** and Annex G says so: the damage was a 320-token cap severing replies the frame had told the
> rod to make longer. The front page of the book was still asserting it. The mechanic is real; this is the
> receipt that survives.

**`Obsignatus unius` is the trap under the council.** A creature producing exactly one wrong answer
cannot be rescued by voting, because voting selects among answers that exist. Three of them together
produced twenty-four answers in which the truth appeared zero times.

**`Caecus interioris` is why routing is external.** Asked to predict its own failure, no rod was honest
on a single cell it failed, zero of twelve. A creature cannot be asked where its own ceiling is.

---

## WHAT IS ACTUALLY PROVEN

The honest accounting, because the table above shows nine rungs marked MEASURED and that is a smaller
claim than it looks:

```
census items                                    86
named anywhere on the path                      23
placed by the audit alone, never tested         63      (73%)
```

Nine rungs carry receipts. **Sixty-three of the eighty-six items have never been tested against
anything.** They are filing decisions with reasoning behind them, which is not nothing and is not a
receipt either. The book says so on every page where it matters.

---

## APPENDICES

| | |
|---|---|
| **A** | THE CENSUS, all 86 items, with what the codex claims, what the substrate carries, and what this walk verified |
| **B** | THE CHAIN, what each rung hands to the next, and the evidence that the link holds |
| **C** | THE PROMPT LIBRARY, the instruments, including the one refuted by its own test |
| **D** | THE ANCHOR CONTRACT, how any subset of modules composes into an architecture |
| **E** | THE REVISION QUEUE, every case where measurement disagreed with the author. **18 entries from two levels, 4 of which had already produced a written claim** |
| **F** | THE FUEL, 168 live endpoints across four verified plants (nvidia 118, ollama 32, groq 15, cerebras 3), plus one unverified and five behind a missing key |
| **G** | THE BESTIARY, every creature with a receipt, its binomial name, and its measured evolution line |
| **H** | THE CANDIDATES, five capabilities the 86-item audit never named, all five found by building |

---

## THE RULES OF THE WALK

The first six survived the first edition. The rest were earned on 2026-07-25, each by a measurement that
went the wrong way.

1. **A step closes only on a receipt.** It ran and was seen, or it is not done.
2. **A step may fail**, and three of the first four did. That is where the laws came from.
3. **Token flow is a column on every step**, never an afterthought.
4. **Where canon is silent, the gap is shown** rather than filled.
5. **A derived claim is marked as derived**, so it can be argued with.
6. **The instrument outranks the author.** Where a measurement contradicted the plan, the plan lost.
7. **Count distinct outcomes, never attempts.** `n=8` was `n=1` on a deterministic endpoint, and the
   floor that was supposed to guarantee power guaranteed nothing.
8. **Measure at the temperature the product runs at.** The bench fires at 0.2 and the lab was measuring
   at 0.0, so the lab was not measuring the product.
9. **A part with an unmet precondition is harmful, never neutral.** The frame that rescues a 70b takes a
   550b from 1.00 to 0.25.
10. **A council selects, it cannot generate.** Three rods that all fail produced 24 answers and the truth
    was not among them, so no vote could find it.
11. **The form decides what gets written.** A declared shape admits state; a free one admits deliberation,
    which grows without bound and then truncates.
12. **Write the evidence as you go.** A run killed at a cap with four completed arms in memory is four
    arms of nothing, and awaiting a measurement is the whole point of the harness.
13. **A rod's usable context is part of its identity, and it is untracked.** `grep -rn "context_window|num_ctx"
    over the whole runtime returns **zero**, and `fuel.py` lists it as UNMEASURED. Any input larger than a
    window must be chunked or retrieved, and neither strategy can be planned without the number. This
    belongs to L4, where the calibration table is built.
14. **The 86 is a floor.** Four capabilities have already been found outside it, all by building rather
    than auditing, and a checker that rejects a new item as an error punishes the only method that has
    ever found one.
