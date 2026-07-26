# THE DERIVATION — the ladder, built from the bottom, each level forced by the one below

**Luis, 2026-07-25:** *"a call to a model with a prompt and the output we get, the prompt is the only
way we control the output, no memory. this is the base level. I feel that we are not going from the
bottom up but selected a bunch of elements and grouped them into chapters, a hierarchy I don't feel it."*

He is right, and the diagnosis is structural rather than editorial.

**What went wrong.** The 86-item census is an *audit of a document*. Its eleven layers group items by
where they appear in the canon's own description of itself, not by what depends on what. The chapters
inherited that grouping, so nothing forced chapter I to contain the five things it contained. A reader
cannot feel a hierarchy that is not load-bearing, and this one was a filing system wearing a ladder's
clothes.

**What a derivation is instead.** A level exists only because of something the level below **cannot do,
by construction rather than by weakness.** You do not get to add an organ until the layer beneath it has
been shown insufficient. Every rung is then falsifiable in the same way: *show that the level below can
already do this, and the rung collapses.* That is a spine. What follows is that spine, and every
measurement already taken re-files into it without waste.

---

## L0 · THE CALL

One prompt in, one output out. No memory, no second call, no state. **The prompt is the entire control
surface.** This is the floor, and it is not a poor floor: measured, nemotron-550b passes all five tasks
in the bank at 8/8 bare, and even llama-3.2-1b passes two of them.

Everything above exists because of five things L0 cannot do — and each is an absence by construction,
not a deficiency to be fixed with a better model:

| L0 cannot | because | forces |
|---|---|---|
| know anything absent from the prompt | there is no other input | L5 |
| tell whether it succeeded | the output is the only artifact | L1 |
| be corrected | there is no second look | L3 |
| exceed one context, or hold a long chain without drift | one call is one breath | L5 |
| disagree with itself usefully | there is one voice | L6 |
| run without someone pressing go | there is no clock | L7 |

## L1 · LOCAL WORK ON THE OUTPUT — free, no call

*Forced by:* at L0 you cannot distinguish a pass from a failure, and the answer is sometimes in the work
rather than in the model's summary of the work.

Contains **THE MEASURE** (C-15, C-60) and **THE READOUT** (candidate C-87). Both are pure local
computation over text already paid for: measured cost 0 tokens, 0ms.

**This level is free, which is why it comes first.** Nothing else in the architecture is free. Measured:
THE READOUT alone takes llama-3.3-70b from 0/8 to 8/8 on wordcount, because that rod enumerated to 13
correctly in 8 of 8 trials and then reported 11. No call, no tokens, no time — the answer was already
bought and simply not read.

*Collapses if* a rod's self-report is always as reliable as its work. Measured false.

## L2 · LOCAL WORK ON THE INPUT — free, no call

*Forced by:* the prompt is the only control surface at L0, so constructing it is the only remaining free
lever. Once L2 is exhausted, every further gain costs a call.

Contains **THE FRAME** (C-04, C-19, C-23). Measured: a frame that names the method takes llama-3.2-3b
from 0/8 to 8/8. A frame that names only a posture costs +38 to +107% input tokens and changes nothing.

*Collapses if* framing never changes an outcome. Measured false — but note it holds only inside a
failure window: on gpt-oss-20b the same frame is void because that rod never failed.

**L0 + L1 + L2 is the whole of "one call".** Everything to here is one prompt and one output, and it is
where chapter I actually lived. That is the honest scope of chapter I, and it should have been said that
way: *what can be done with one call, and how far can the prompt alone carry it.*

## L3 · A SECOND CALL, SAME FUEL

*Forced by:* a single call cannot review itself — **and this is the rung whose justification just got
weaker.** Chapter I claimed one-breath self-critique finds zero errors in nine trials; re-measured, it
names an error in 25 of 32 trials on the four rods that can do the task at all. So L3 is not forced by
detection. What survives: on a rod that genuinely gets an answer wrong, a separate critic repairs it
0/8 → 5/8, at 6.4x the input tokens.

Contains **THE CRITIC**, **THE WARD** (C-43, C-50, C-78, C-18). Cost: doubles or triples the call count.

*Collapses if* one-breath critique repairs as well as a separate call. **Currently unresolved** — the
only two calibration-valid tasks have not yet been used to settle it.

## L4 · A DIFFERENT FUEL

*Forced by:* this fuel has a ceiling, and it is not the same ceiling for every task. Measured: one
composition, four verdicts, five rods. Also measured: mistral-119b is in the measurable window where
nemotron-120b is saturated, so family matters as much as size.

Contains **THE LADDER**, the fall-through (C-16, C-67).

*Collapses if* one rod is always at least as good as any other for a given task. Measured false.

## L5 · STATE THAT OUTLIVES A CALL

*Forced by:* nothing at L0–L4 accumulates. Each level so far improves a single exchange; none of them
lets the second exchange know what the first concluded.

Contains **RECALL** (C-02, C-13, C-84) and **THE CHECKPOINT** (C-80) — the single mutable object every
layer reads and writes, which the census records as EMBODIED and which greps to zero files. Thirty-five
separate JSON files stand in its place, each written alone and read alone.

**This is the first rung a bigger model cannot climb for you**, and it is the reason chapter II opens
where it does. A 550b saturates every one-call task in the bank; it still cannot remember what it
concluded a minute ago. That is the shape of L0, and no quantity of parameters alters it.

*Collapses if* a long chain in one breath matches a stepped chain with a checkpoint. **This is x06.**

## L6 · MANY VOICES THAT MUST AGREE

*Forced by:* one voice cannot disagree with itself. Measured hint: asked whether a system storing state
in thirty-five files is one self or many, three rods answered simultaneously and split — the 550b said
one self with fragmented memory, deepseek said one self, the 3b said many.

Contains peer debate (C-77), the council. Requires the all-or-incomplete barrier: a three-voice debate
that proceeds with two voices had a quieter debate and every conclusion inherits a missing participant.

MULTIPLICITY stands at L0 of 5 on the axis record — entirely unwalked.

*Collapses if* a council never beats its best single member.

## L7 · TIME WITHOUT AN OPERATOR

*Forced by:* everything above needs someone to press go.

Contains the tick cycle (C-76), autonomy, and the final gate C-64 — sustained unattended operation, on a
stated fuel.

---

## What this reorganisation costs, and what it does not

**It costs nothing already measured.** Every experiment re-files: x01 and x02 are L2 proofs, x03 and x04
are L3, the calibration is the L0 survey, x06 is L0-versus-L5. The retractions become sharper in this
frame rather than embarrassing — *L3's justification is weaker than claimed* is a statement about a rung,
and it is exactly the kind of statement a ladder is supposed to make possible.

**The chapters get renamed by what they prove, not by which census rows they contain.** Chapter I was
never "where am I" — it was **"how far does one call go, and what can the prompt alone do?"** The axis
record was built there because it was needed, not because it belonged to a group.

**The one thing not to do now.** Do not re-file all 86 items into these eight levels before the ladder
has earned it. That is the shape of infrastructure-as-avoidance, and the census will still be there. The
ladder proves itself by hosting the next experiment cleanly, and the next experiment is x06 — the L0
claim that one big breath is enough, against the L5 claim that only carried state can hold a long chain.
