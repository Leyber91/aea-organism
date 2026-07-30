# A THEORY OF A SPEAKER - what two days of building four of them actually taught

*2026-07-30. Luis: "if you had to develop a theory out of this, a technique - how personalities
work, how someone keeps the idea of itself, how memory across the conversation is kept, how we
advance in the conversation and remember facts without losing the thread, and then we realise of
links and subsets."*

*Written as a theory, which means it has to be falsifiable. Every claim below carries the
measurement that supports it and the observation that would kill it. The last section is the part
we have NOT built, because a theory that only explains what you already made is a description.*

---

## 0 - THE CENTRAL CLAIM

> **A conversational identity is not in the model. It is a triple: a shared substrate, a private
> store, and a policy over what enters that store and what is retrieved from it.**
>
> Change the store and you change the person. Change the model and you change the accent.

This is counter-intuitive and it is the single most useful thing measured here. Four characters
running on largely one model held **vocabulary separation 0.93 to 0.97** and their convergence went
*negative* - they diverged as they talked. What separated them was not weights. It was that each
one knew different things and had said different things.

The corollary is the practical one: **a model is a capacity to produce text; a self is a constraint
on which text gets produced.** Everything below is about the constraints.

**What would falsify it:** four characters with identical stores and different models holding
separation as well as four with identical models and different stores. We have half of that
measurement and not the other half - the control is not run. Stated as an owed experiment, not a
result.

---

## 1 - PERSONALITY: THREE LAYERS, AND ONLY ONE OF THEM IS THE PROMPT

Ranked by how much work each does, which is nearly the reverse of how much attention each gets.

**Layer 3 - THE SEED (moderate, one afternoon, does not decay).** A personality written as
adjectives is the weakest possible version: one line of traits is literally the demographics-only
condition, measured at **74% of the human test-retest ceiling against 83%** for seeds built from
concrete first-person incidents. "Careful and precise" produces careful, precise nothing. *"In my
second year I signed off on a figure I had not personally checked and it went to a regulator"*
produces a person, because it gives them something to speak FROM rather than a way to speak.

Bias the atomic facts toward the concrete: measured contradiction reduction is **32.5% → 8.96% on
possessions and history** but only **8.0% → 5.7% on abstract attributes**. A character is held
together by what it has done.

**Layer 2 - THE SUBSTRATE (cheap, structural, unreachable by prompting).** Different models have
different priors, and some traits cannot be prompted away because they were trained in. Sycophancy
is the clearest: measured capitulation under a bare challenge runs **32% to 86%**, with false
admission of a mistake that never happened as high as **98%**, and it does not improve when
restricted to answers the model was 95% confident about. Four voices on one model share that.
Different rods are the cheapest real differentiation available, and prompt engineering cannot
substitute for it.

**Layer 1 - THE HISTORY (the strongest, and it is free).** What this speaker has already said, in
front of these people, that it is now answerable for. See §2 - this is where personality stops
being a costume.

**The measurable failure this predicts:** VOICE COLLAPSE - four prompts on one model drifting to a
single register while every individual line still reads fine. Invisible turn by turn, obvious across
a transcript. `social.distinctiveness()` reports it as `convergence`; positive means collapsing.

---

## 2 - THE SELF: A RECORD OF YOUR OWN COMMITMENTS THAT COSTS SOMETHING TO CONTRADICT

This is the operational definition, and it is deliberately behavioural.

Not "a concept of itself", not "self-awareness" - the claim ceiling forbids both and the evidence
would not support them anyway. What is measurable is **consistency with prior commitments across
sessions**. That is a receipt. GRAVE said *"solder joints don't care how careful you are"* and then,
pushed twice, *"the joint doesn't care about the person either"*. Holding under pressure is the
whole observable.

**Why it must be stored separately from memory.** A memory INFORMS - you draw on it, it decays, it
competes with other memories for attention. A commitment BINDS - it does not decay, it is not
optional, and contradicting it should cost. Putting them in one store makes the strong one behave
like the weak one, and a position you can quietly forget is not a position.

**The mechanism that makes it work at four members:** one seat that does not move. A same-model
population converges to a shared convention on its own, and the committed minority needed to prevent
that starts around **2%** of the population. At N=4 you cannot express 2%, so the holdout is
hard-coded. Without it, a council or a conversation slides to agreement and calls it consensus.

**What would falsify it:** a character with commitments stored and enforced contradicting itself as
often as one without. Not yet measured across sessions - `persona.contradictions()` exists and
nothing has yet run long enough to test it. Owed.

---

## 3 - MEMORY: THREE REGISTERS THAT BIND DIFFERENTLY

The single most transferable structural result.

| register | what it is | how it behaves | how it is used |
|---|---|---|---|
| **MEMORY** | what happened | decays, competes, retrieved by score | informs the turn |
| **IMPRESSION** | who each other person is, to me | rebuilt from evidence, correctable | shapes how I address them |
| **COMMITMENT** | what I have claimed | does not decay, never pruned | binds what I can now say |

Three registers because they have three different failure modes. Merging memory and impression
gives you a speaker who recites events instead of knowing people. Merging impression and commitment
means being wrong about someone binds you to it. Merging memory and commitment means the thing you
said becomes just another thing you might recall.

**Impressions are REBUILT, not appended.** A first impression that turned out wrong has to be
correctable the way a real one is - so it is regenerated from the evidence rather than accumulated.
Observed working: PIP corrected GRAVE for misremembering what PIP had said, and the impression moved.

---

## 4 - ASYMMETRY IS WHAT MAKES FOUR PEOPLE INSTEAD OF ONE

**One line, four different memories.** The speaker records it as something it SAID and is bound by.
The other three record it as something they HEARD FROM someone, tagged with who.

This sounds like bookkeeping and it is the whole architecture. **A shared conversation log is one
mind with four voices**, because every participant would know exactly the same things and differ
only in style. What makes four people is that GRAVE remembers being contradicted and MIRA remembers
who moved the goalposts, and neither has access to the other's reading of it.

**Asymmetric knowledge is not an implementation detail of multi-agent systems. It is the definition
of one.**

---

## 5 - RETRIEVAL: SCORED, NEVER WINDOWED

The last-N-turns window is recency and nothing else, and it is why most agents cannot remember
anything that matters. Scoring three components lets a turn reach much further:

```
score = 1.0 * recency      exponential decay, half-life 20h
      + 1.2 * importance   scored at write time, cheaply and deterministically
      + 1.6 * relevance    overlap with what is being discussed right now
```

Relevance outweighs recency deliberately - the entire point of scoring is to beat "the last few
turns", which recency alone reduces to.

**Measured:** at 26 turns, **16 of 26 turns reached back more than two, the deepest by 12 turns,
mean depth 7.7.** That is remembering rather than reacting, and it is the difference a listener
hears as "they were listening".

**The honest limit, stated rather than hidden:** relevance here is LEXICAL overlap, not embedding
similarity, because there is no embedder wired in. A memory about "lying" will not surface for a
turn about "dishonesty". `_relevance` is the one function to replace when an embedder lands, and
until then this system remembers words rather than meanings.

**Importance is scored at write time, not read time**, and cheaply: a position, a disagreement, a
generalisation, a personal disclosure. Asking a model to rate each memory would cost one call per
remembered line per listener - four speakers hearing every turn - which is more than the
conversation itself.

---

## 6 - ADVANCING: A GUIDE NAMES WHERE TO GET TO, NEVER WHAT TO SAY

A script produces speakers who talk past each other in the right order - four monologues
interleaved. The fix is not better lines; it is that **the destination is specified and the route
is not.**

Three parts:

1. **The guide** is a list of places the conversation should reach. It advances when the group
   actually gets there, and nobody is ever handed a sentence.
2. **A mechanical stall detector**, not a model asking whether things have stalled - the documented
   failure is that agents RECOGNISE the loop and still cannot leave it. A detector that has to be
   talked into firing is the same organ that is stuck.
3. **Intent**, which is the part we barely have. The single unambiguous prior success in this whole
   literature (CICERO, 40 anonymous games, 82 human players, no message indicating suspicion) worked
   because **an intent was chosen OUTSIDE the model and every utterance had to serve it** -
   intent-grounding alone moved plan-consistency 76.19 → 92.86. Our speakers have a topic to drift
   toward and, briefly, a person they wanted to meet. That is the smallest version of it.

---

## 7 - THE FLOOR: THE LINE BETWEEN ORCHESTRATION AND COORDINATION

A scheduler picks who speaks. Bidding lets each one decide whether it wants to.

The difference is testable: **remove a participant from a scheduler and the others behave
identically; remove one from a coordinating group and the others fill the space.**

**An entity that cannot decline to speak is not autonomous.** With bids, GRAVE asks for the floor at
0 for six turns and then at 10 when someone is wrong about it - which is the character, expressed
as behaviour rather than as prose.

**One correction, measured:** being named must be a strong BIAS and not an override. Current-speaker-
selects-next is the strongest rule in real turn-taking, so the first version let it win outright -
and two speakers named each other into a loop that took 84% of the floor and left a third with
**zero speech acts**. A rule that is merely strong in humans becomes absolute in code unless
something else can outweigh it.

---

## 8 - LINKS AND SUBSETS: THE PART WE HAVE NOT BUILT

This is what Luis was pointing at, and the honest answer is that it is missing.

Everything above is **storage and retrieval**. Nothing yet performs the operation of noticing that
several memories MEAN something together that none of them means alone. In the prior art that
operation is called reflection, and its ablation is the strongest result in the paper it comes
from: removing it hurt believability more than removing planning did.

**The shape it should take here:**

```
periodically (every N turns, or when accumulated importance crosses a threshold):
    take the highest-scoring recent memories
    ask ONE question of them: "what do these together suggest that none says alone?"
    store the ANSWER as a new memory, tagged as derived, with pointers to its sources
```

Three properties make it worth building rather than decorative:

- **The answer is itself retrievable.** A conclusion competes for attention alongside the raw
  memories that produced it, so later turns can reach for the insight instead of re-deriving it.
- **It is a SUBSET operation.** It runs over a scored selection, not the whole store - which is what
  makes it a synthesis instead of a summary.
- **It keeps its sources.** A derived memory that cannot name what it came from is exactly the
  fabricated-provenance failure this project spent two days removing from the voice path. A
  reflection is a claim, and a claim with no receipt is the thing the honesty law forbids.

**And it is where the cost argument finally pays.** This looks expensive and is not: an utterance is
ten to fifteen seconds of speech, so every call except the current speaker's runs in the SHADOW of
the previous utterance playing. Only ONE generation is ever on the critical path per turn.
Reflection, impressions, bids and probes are all free if the loop is a producer/consumer around the
audio queue.

---

## 9 - THE METHOD, WHICH IS THE PART THAT GENERALISES FURTHEST

Four rules earned by getting them wrong, and they are not about conversation at all.

1. **The instrument is more likely wrong than the subject.** Session one: nine of eleven wrong
   beliefs came from an instrument. Session two: six of eight. Ask what would have to be true of the
   INSTRUMENT for the finding to be false, and test that first.
2. **One run is an anecdote with a decimal point.** Three of four gains reported here were inside
   the run-to-run spread of the metric measuring them. A comparison means nothing until the noise
   floor is known.
3. **Test the wiring, not the function.** Three separate capabilities in this repo were measured,
   documented, tested, and called by nothing. Each passed its own test every time.
4. **Bound the quantity you care about, never a proxy.** Sentences for seconds, characters for half
   a minute, tokens for speech, and a threshold derived from the very thing it was supposed to check.

---

## 10 - THE AUDIT BEHIND THIS DOCUMENT

Counted, not estimated:

```
72 lessons recorded    19 crystals, 7 voice defects, 18 discoveries, 28 research rungs
14 of 25 mechanisms BUILT, 11 not
13 of 13 defects carry their evidence in the code that fixed them
```

Not built, in the order they are worth building: **reflection (links and subsets)**, the echo gate,
the probe harness and drift curve, intent per speaker, the FTO ledger, barge-in, the filler ladder.

And one defect in the record itself, found by counting it: three crystals from this session were
numbered C-V9 to C-V11 and collided with three of the same numbers from the earlier one. The
register of lessons had a lesson-shaped hole in it, and only an audit that counted instead of
trusting would find that.
