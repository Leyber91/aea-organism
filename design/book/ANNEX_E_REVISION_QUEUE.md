# ANNEX E, THE REVISION QUEUE

*Every case where measurement disagreed with the author, what was claimed, what was measured, and what
changed. Rule 6 of the walk states that the instrument outranks the author. This annex is the receipt for
that rule, and it exists so the count is visible rather than remembered selectively.*

**Twenty entries as of 2026-07-26, all from the first two levels.** Fifteen were caught before they
reached a conclusion. **Five had already produced a written claim**, and those are the ones that matter. A5 invalidated two
chapters' worth of closures at once and is the largest single correction in the walk.

---

## CLASS A: a claim was written down and later overturned

These are the failures of the walk, and each one survived until a second instrument caught it.

| # | the claim | what measurement said | how it was caught |
|---|---|---|---|
| **A1** | *"52% of L0's failures already contain the answer"* (Chapter I's closing image) | **2%.** The test asked whether the answer appeared anywhere in the reply; the `extract` prompt contains the word `cerebras`, so quoting the question counted as answering it. **All 50 trials were flagged as echoing the prompt** | Chapter II applied a structured readout to the same population and got 3 of 153 |
| **A2** | *"the posture frame converts llama3.1:8b, 8/8"* | **5/8 against 3/8 bare**, inside noise by the harness's own threshold. One lucky deterministic sample promoted to a measured conversion | the determinism check, which found the endpoint returning byte-identical replies |
| **A3** | *"THE READOUT sits below THE FRAME"* (ordered by cost, free before +34 tokens) | **8 bare replies contained working against 240 framed, 30:1.** The readout is inert until something makes the rod show work | building the chain table and asking what each rung hands the next |
| **A5** | *"Chapter I closes C-12. Chapter II closes C-15, C-60 and C-75"* | **none of them.** Every experiment quoted the item's four-word LABEL from `hierarchy.json` and never its DEFINITION in `A15_FULL_COVERAGE.md`. C-15 is a gauge over `self.json` tick history; C-60 is a brownout drill that was never run; C-75 validates parsed ACTIONS and **already had a 16.8% receipt nobody read**; C-12 is a persistent goal stack | reading A15_FULL_COVERAGE.md for the first time, prompted by the question "are the tests up to what each component states" |
| **A4** | *"a 120B rod cannot read a word out of a log line"* | it never reached an answer because `max_tokens=300` starved it. At 1200 the truncation count fell from 91 to 9 | the overseer flagging 42 of 48 of its trials as debris |

**A5 is different in kind from the rest, and worth stating separately.** A1 through A4 are instruments
that measured the wrong thing. A5 is an instrument that measured a **real** thing and filed it under a
name that meant something else. The measurements survive; the closures do not. The defence is a single
habit that was missing from the start: **quote the item's definition in the experiment's docstring**, so
that a mismatch is visible while the experiment is being written rather than three chapters later.

**The pattern in Class A.** Three of the first four came from **our own instrument guessing**: a containment
test that accepted an echo, a sampling floor that measured determinism, a token cap that measured itself.
Not one came from a rod behaving unexpectedly.

---

## CLASS B: caught before it became a claim

| # | what would have gone wrong | caught by |
|---|---|---|
| B1 | a yes/no parser read `"YES and NO"` as YES, biasing rods toward looking dishonest in the exact direction that flattered the placement under test | reading the parser before trusting its output |
| B2 | a loose parse read *"b5 moved 2 shelves ahead from shelf 4 to shelf 6"* and returned **2**, converting correct working into a confident wrong answer | testing the parser against realistic reply shapes first |
| B3 | a saturation guard that passed trivially, so four arms at 100% read as a clean confirmation | asking whether the comparison had any headroom |
| B4 | free-form notes hit the token cap 32 to 53 times per arm while canonical notes hit it 0 to 1, and the loss was about to be charged to representation | recording cap-hits per arm |
| B5 | the lab measured at temperature 0.0 while `bench_core` fires at 0.2, so the lab was not measuring the product | `grep -c temperature aea/bench/bench_core.py` returning 0 |
| B6 | a run killed at a wall-clock cap with **four completed arms held in memory and never written** | the evidence directory being empty after an exit code of 0 |
| B7 | the streaming wire dropped usage, so `tok_out` came back zero and the latency mechanism could not be tested | trying to test the mechanism and finding no data |
| B8 | the overseer passed a pure deliberation trace as clean, because its rule needed two markers and the reply had one | reading the raw replies rather than the flag counts |
| B9 | `cerebras` streams content under `reasoning`, where others use `content` or `reasoning_content`. Reading one field returned 40 tokens of empty string and would have blanked a whole plant's column | checking a plant that returned tokens and no text |
| B10 | ground truth for `unconventionality` written as 8 vowels. It is **7**, and every rod would have been scored as failing | verifying the truth locally before the run |
| B11 | a pooled latency ratio of 1.77x that was confounded by rod identity, mixing a local rod at 2s with a hosted rod at 0.24s | asking whether the effect survived within a single rod |
| B12 | the `follow` op collapsed six boxes onto three shelves, so "everything is on shelf 1" would score 0.5 per box | computing the lazy baseline before running |
| B13 | describing the L0-L1 space as 16 cells when there are **5 seatable components, so 32** | counting the census items instead of remembering |
| B14 | a rate limit we caused ourselves recorded as a rod returning 1 of 8 calls | checking the plant directly, where it answered in 0.4s |
| B15 | the C-75 task asked *"how many tokens did this run use"* with truth set to `completion_tokens=317`. A run using 45 prompt and 317 completion **uses 362**, so the four "fabrications" were a defensible reading of an ambiguous question | reading the four raw replies instead of trusting the counter |

---

## THE LESSONS, in order of how much they cost

**1. Our instruments fail more often than the rods do.** Nineteen entries, and **not one** is a case of a
rod behaving in an unexpected way. Every single one is the harness, the parser, the cap, the floor, the
ground truth, or the author. The rods have been consistent throughout; the measurement of them has not.

**2. A permissive instrument is worse than no instrument.** A1 and B2 are the same failure: a test that
commits rather than abstains converts correct working into a confident wrong answer, and it does so
silently, in the direction that flatters whoever wrote it. The rule that follows: **an instrument that
cannot abstain must not be trusted with a headline.**

**3. Trial counts are claims about independence, not about effort.** `n=8` was `n=1` for an entire day
because nothing counted distinct outcomes. A floor that counts attempts guarantees nothing.

**4. Fixing one thing breaks another, and the fix must be measured too.** Raising the token cap to stop
starving reasoning rods quadrupled the token reservation and triggered rate limits on a plant with a
per-minute token budget. Switching to a streaming wire to stop a dead plant hanging the lab dropped the
usage accounting.

**5. Write the evidence as you go.** B6 cost four completed arms. Everything since writes per arm.

**6. The author is the least reliable component in the system**, and the only defence that has worked is
a second instrument at a different level looking back down. A1 was caught by Chapter II auditing Chapter
I. Nothing internal to Chapter I would ever have found it.

---

## WHAT THIS MEANS FOR THE ARCHITECTURE

Four amendments are owed to the census, and one of them contradicts a named item. **None is being applied
yet**, because each rests on a single level's evidence and the discipline of this book is that one
counterexample is a note while a pattern is a law.

| # | the census says | L0 and L1 measured | status |
|---|---|---|---|
| **1** | **C-63**, each layer requires every layer below it, and removing one stops everything above | `Auscultans horae` (latency) requires **nothing** below it. No goal, no scorer, no parse. It can be seated alone | **counterexample, n=1.** Held pending L2 and L3. If more off-chain components appear, C-63 needs qualifying |
| **2** | an item sits at the lowest rung where it is POSSIBLE and NECESSARY | THE READOUT is possible and necessary at L1 and **not supplied until L2**. Three conditions, and the third points upward | **amendment proposed.** The placement rule is incomplete |
| **3** | every item is the same kind of thing | four kinds appeared at L1 alone: **reveal** (the scorer changes no answer and enables everything), **recover**, **guard**, **predict** | **addition proposed.** The census has no type field |
| **4** | nothing | **preconditions are never checked.** `Arbiter vacui` runs with its precondition missing and returns a clean score in 32% of trials | **missing capability.** Not in the 86. The composer cannot refuse to seat a part whose precondition is unmet |

**And the census undercounts in a nameable direction.** Five capabilities have now been found outside the
86, all five by building or watching rather than by auditing: THE READOUT, THE WARD, the
self-representation floor, noticing an absent goal, and precondition checking. **Every one of them is
something that only appears when you run the thing.**

---

## DOES L0 AND L1 PROVE THE AEA?

**At the bottom, yes.** C-12 is a hard floor at every size from 751M to 120B, 0 of 304. C-15 is not
fooled, 0 of 153. The two items the architecture puts at the base of everything hold under measurement,
and they had never been tested before this walk.

**And the shape needs work.** The ordering claim has a counterexample, the placement rule is missing a
condition, the items need types, and the largest hazard found so far is a capability the census does not
contain. That is four amendments from two levels, which is a rate worth watching rather than panicking
about: seven levels remain, and if the rate holds the census will need a revision pass rather than a
patch.
