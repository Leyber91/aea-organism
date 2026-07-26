# CHAPTER I — WHERE AM I

*The question: can the entity say where it stands?*
*Closes: C-11, and the first rungs on C-06 through C-10.*
*Walked 2026-07-25. Four steps. Three of them failed on the first attempt.*

---

---

## 0 - What this chapter puts under load

The architecture has 86 catalogued parts. A chapter that does not say which of them it is testing is a
travelogue, so this is the manifest, and it is deliberately narrow.

**Put under experimental load** - a real baseline, eight trials, five rods, two providers. These eight
are the only items in this chapter with receipts anyone else could re-run.

| item | what the census calls it | what it means, and why it was loaded |
|---|---|---|
| C-04 | axis Prompting | where a construct sits on the prompting ladder. THE FRAME is the part that moves it, and the most-used organ in the whole architecture |
| C-19 | #8 crystallize | a proven result becoming a reusable part. Without it nothing accumulates |
| C-23 | crystallize mechanic | the player-facing verb of C-19: the moment a proof becomes a thing you own |
| C-16 | #5 substrate-variation | the same construct behaving differently on different fuel. The chapter's deepest finding lives here |
| C-14 | #3 coordination (plan-act-critique) | the three-beat cycle the canon puts at the centre of thought |
| C-43 | filter: adversarial_probe | the policy that PERMITS a claim to be attacked. Falsification as law, not mood |
| C-50 | hyp type: adversarial_probe | the construct attacking its own answer. The whole basis of THE CRITIC |
| C-78 | falsify category | falsification as a first-class execution path with its own dispatch |

**Built and verified by construction, not by experiment.** C-11, the position record - the dict that
answers *where am I* - and C-01, the draw, which every arm above stands on and which needs no experiment
because a construct that cannot draw cannot do anything at all.

**Anchored but never loaded - eleven items.** C-02, C-13, C-15, C-18, C-26, C-29, C-47, C-52, C-60,
C-67, C-84. *Anchored* means each declares a precondition and a measured cost, so a composition
containing it can be checked. It does not mean tested. Naming that difference is the point: 20 items are
anchored, 8 were actually put under load, and the gap between those two numbers is the honest size of
this chapter.

So: **8 of 86 measured.** Not a survey. Four questions, asked properly.

## 1 · A coordinate system with no coordinates

The canon is emphatic about the five axes. It calls them PATH, ABSTRACTION, MULTIPLICITY, PROMPTING and
ASYNC, gives each one a six-rung ladder from L0 to L5, and then says the thing that makes them matter:
*"the ladders are not decoration, they are the coordinate system."* Growth in this architecture is
defined as movement through that five-dimensional space. Not a score. A position.

The census marks the position record — item C-11, the dict that says where the entity currently stands —
as **missing.** I checked the machine rather than the document. `axis_levels` appeared in zero files.

So the architecture had a coordinate system and no coordinates. It could describe growth precisely and
could not answer *"where am I?"* at all.

That is where the walk had to start, because everything above it depends on knowing the answer. One of
the five cascade filters deep in the innovation layer is called BOUNDARY, and its job is to ask whether
a proposed change is *reachable at the current axis levels* — a filter that cannot function until this
record exists. The dependency was real before I built anything.

## 2 · Step one: the record, and the one law it enforces

`aea/mind/axes.py`. A small file. The whole of it is five levels, thirty rung definitions, and one
refusal.

**A level is only raised by a receipt.** `raise_axis` will not move a number without a reference to
something that actually happened — a run id, a logged event, a test. It also refuses a skipped rung: a
rung is climbed, not jumped. And it refuses a re-claim, so the same proof cannot be spent twice.

That single constraint is what makes this a position rather than a score. In canon's own language, a
raise is an instance of **OP1 axis-extension** — *"a higher level on one of the five axes becomes
reachable"* — rather than a number a designer awarded. It is the difference between measuring an entity
and decorating one.

The first reading:

```
PATH           L0/5      ABSTRACTION    L0/5
MULTIPLICITY   L0/5      PROMPTING      L0/5
ASYNC          L0/5
                                   0 of 25 · 0% walked
```

Zero. Which is correct, and it is the first honest number the architecture had ever produced about
itself.

## 3 - Step two: the frame that subtracted

> **Correction, 2026-07-25.** The toxicity claim in this section was RETRACTED under re-measurement at
> n=8 on five rods. An unfitted frame is expensive, not destructive. See section 7.

The PROMPTING axis is unusual in that **the canon's definition of it is also the test**: *"a scaffold
makes a cheap node beat its raw self."* So the experiment writes itself — take a genuinely cheap model,
give it five checkable tasks, run each three times bare and three times framed, and count.

I wrote what I believed was a good scaffold. Identify the exact form the answer must take; do the work
required to be correct; emit only that form, no preamble, no explanation.

```
TASK          BARE    FRAMED
WORD-COUNT    0/3     0/3
ARITHMETIC    3/3     3/3
STRICT-JSON   3/3     0/3
EXTRACT       3/3     3/3
HOLD          3/3     3/3
TOTAL        12/15    9/15      tokens 969 → 1848  (+91%)
```

The scaffold cost ninety-one percent more tokens and made the model **worse.** And the worst cell is the
third row: asked for strict JSON, a task it passed three times out of three unaided, the framed model
replied ***"I don't see a question."*** My own instruction — *identify the form the answer must take* —
had taught it to treat a directive as a non-question.

**A frame is not an upgrade. It can subtract.**

But my scaffold was generic, and the canon says *frontier-encoded*. So I isolated the one task the model
genuinely could not do, and tried a scaffold that named the **method** instead of demanding precision:
split the sentence on spaces, number each token, report the final index.

```
CONDITION         PASS    TOKENS
bare              0/3     192     answers: 9, 11, 9
generic frame     0/3     327     answers: 9,  7, 9
targeted frame    3/3     471     answers: 13, 13, 13
```

Impossible became certain, for two and a half times the tokens of bare. And the generic frame sits in
the middle of that table as the worst of the three options: more expensive than doing nothing, and no
better.

> **The law:** a scaffold makes a cheap node beat its raw self **only when it is fitted to the specific
> failure.** Generic guidance is pure cost, and can be negative.

The canon states the claim. It does not state the condition. The condition is the whole of the value.

## 4 · Step three: the memory that already knew

The ABSTRACTION axis is grounding — does a retrieved memory change what the entity says? I expected to
have to build the retrieval. I was wrong twice over.

**First, it already existed.** `aea/memory/memory.py` does embedding recall against a local model, with
cosine similarity, free and unlimited and private. I had been calling recall "fog" for the entire
session. It was thirty lines of working code.

**Second, and worse: it already knew.** The store was seeded with ten measured facts about this grid, and
the second one reads:

> *"NVIDIA's 40 requests/minute limit is PER-MODEL with independent buckets — querying all 121 models at
> once produced zero 429 errors, so there is no global cap."*

Earlier the same day I had spent roughly a hundred API calls establishing that empirically, by saturating
one model until it rejected me and then getting clean responses from three others in the same second. I
had measured, carefully and at cost, a fact sitting in the entity's own memory.

Two facts further down sits the crystallize doctrine — *a frontier model encodes a behaviour into a tight
scaffold that a cheap model then runs* — which is precisely what step two had just finished measuring.
And the tenth fact says: *"the biggest risk to the project is that characterization keeps substituting
for building."* The store had already diagnosed the session that never consulted it.

The first grounding test then failed, and the fault was mine again: I asked a question the model could
already answer, so grounding cost a hundred and sixty percent more input tokens for zero gain. **You
cannot measure grounding on something already known.** Isolated properly, against a fact the model could
not possibly hold:

```
COND       PASS   TOK IN  TOK OUT   answers
bare       0/3    183     30        "I don't have access" ×3
grounded   3/3    471      6        51 | 51 | 51
```

Impossible to certain again. Note the output column: it **fell** from thirty tokens to six. Certainty is
cheaper to say than an apology. And the retrieval itself cost nothing in cloud tokens, because the
embedder is local — though it took 18.7 seconds cold and 3.1 warm, which is a cliff for anything that
wakes rarely.

Note also what the model did when it was ignorant: it said *"I don't have access,"* three times out of
three, rather than inventing a number. That is a real capability, and I only found it by accident.

**The same shape as step two.** A scaffold pays only when fitted; memory pays only when the model
genuinely cannot know. Two axes, two independent experiments, one law:

> **Every capability has a precondition for being worth its cost. Added without it, a capability is pure
> tax — and sometimes actively harmful.**

That law later became executable. It is the load-bearing field in the contract that lets any assembly
order be checked without anyone deciding in advance which order is correct.

## 5 - Step four: it cannot criticise itself in one breath

> **Correction, 2026-07-25.** This section's title is REFUTED. One-breath self-critique names an error
> in 25 of 32 trials on the four rods that can do the task at all. Note that the table below never
> supported the title either - structured and separated tie on two of its three tasks. See section 7.

The PATH axis is control flow, and the canon's rung at L3 is *multi-step plan + critique*. That phrase
can mean two different things, and the difference turned out to be the finding.

Three conditions, on cognitive-trap problems where the intuitive answer is wrong so a single call
genuinely fails: **bare** (one call), **structured** (one call containing plan, execute, critique and
final as labelled sections), and **separated** (three real calls — answer, then criticise the answer,
then finalise).

```
TASK        BARE   STRUCTURED   SEPARATED
BAT-BALL    2/3    3/3          3/3
MACHINES    1/3    0/3          1/3
LILYPAD     2/3    2/3          2/3
TOTAL       5/9    5/9          6/9

bare         9 calls  1442 tok
structured   9 calls  2554 tok   critique: 0 found / 0 changed
separated   27 calls  6841 tok   critique: 9 found / 4 changed
```

Read the critique column. The structured model, explicitly instructed to find the strongest error in its
own answer, found **nothing in nine trials out of nine.** The same model, asked the same thing as a
**separate call**, found something **nine times out of nine** and changed its answer four times.

> **Self-criticism requires separation.** A model cannot criticise itself in the same breath it answers.
> The boundary is not stylistic; it is what makes self-examination occur at all.

And the level rose only to L1, not to canon's L3, for an honest reason: separated critique cost three
times the calls and nearly five times the tokens **for one additional correct answer out of nine** —
inside noise. Of the four answers the critique changed, only one was a net improvement. Changes were as
likely to break as to fix. The mechanism is real; the profit is not proven.

## 6 · Where the chapter closes

```
PATH           L1/5   ██▁▁▁▁      a fixed sequence it executes in order
ABSTRACTION    L1/5   ██▁▁▁▁      grounded in a retrieved memory
MULTIPLICITY   L0/5   ▁▁▁▁▁▁      one path
PROMPTING      L2/5   ███▁▁▁      a fitted frame converts failure into success
ASYNC          L0/5   ▁▁▁▁▁▁      synchronous

                            4 of 25 · 16% walked
        30 rungs · 10 stated by canon · 20 derived · 4 climbed
```

**What the companion can do**, all measured: it draws real answers · its work is scored · a *fitted*
scaffold makes it beat its raw self · a retrieved memory changes what it says · it plans, criticises its
own output and revises · and it refuses honestly when it does not know.

**What it cannot do:** count unaided, and wrong the same way every time — 9, 11, 9 — which is a
capability ceiling rather than noise. Benefit from generic guidance. Hold a strict output format under a
competing instruction. Criticise itself without a separate call. Improve *reliably* when it does
criticise. And judge for itself whether a capability is worth its cost, which is the very thing the
chapter's law says matters most.

**And what the chapter cost me.** Two of my four steps failed on their first attempt because of my test
design, not the machine's behaviour. A prompt I had written as an instrument turned out to be inert. The
plate that illustrates this chapter went out with a number in its footer I had never computed, and with
the L0 rungs lit amber — which would have opened the entire progression with a flattering lie, every
player starting at seven of thirty having done nothing.

Four corrections, all mine. **The instrument is more honest than the author, and that is the only reason
the next eighty-two items are worth attempting.**

---

*Chapter II asks whether there is one of this entity, or forty. The canon says every layer communicates
through a single mutable object passed by reference. The machine has many files. Settling which is true
gates more than forty of the remaining items, and it is the most interesting question on the route.*


---

## 7 - The apologia: what the final creature actually showed

The chapter's last creature seats five modules in the order necessity demanded them - the draw, the
frame, the recall, the critic, the measure. It was meant to be the chapter's proof. What it turned out
to be is an instrument for discovering how little the chapter knew, and that is a better result, though
it is not the one I set out to report.

**It is not one creature. It is five.** The same five modules, the same task, the same minutes, on five
rods, produce four different verdicts. On llama-3.2-3b the frame converts total failure into total
success, 0 of 8 to 8 of 8. On gpt-oss-20b the same frame is void, because that rod never failed and a
frame cannot rescue a capability that was not missing. On llama-3.2-1b nothing helps at all. On
llama-3.3-70b the frame works perfectly and the rod then misreports its own answer. This is C-16, and it
is the finding itself, and everything else in the chapter rests on it. A sentence of the form *the AEA is 60 percent
complete* has the same grammar as *the rod is four long*. Completion is only ever completion on a stated
fuel, and a number in this book without its fuel stamp cannot be read at all.

**Three of its four laws did not survive being measured properly.**

| the chapter claimed | measured at n=8 on five rods | status |
|---|---|---|
| I - a capability pays only when its precondition holds | demonstrated three separate times, and it explains most of the wreckage below | **HOLDS** |
| IV - the architecture is not fuel-independent | one composition, four verdicts, five rods | **HOLDS** |
| a generic frame DESTROYS strict JSON, 3/3 to 0/3 | delta zero on every rod that reached the floor. Expensive, not toxic: +38 to +107 percent input tokens, up to 4.7x latency | **RETRACTED** |
| III - a judge must OVERRULE, not advise | on the one rod whose precondition genuinely held, advise repaired +5 and overrule repaired +5. Identical | **RETRACTED** |
| II - self-criticism requires SEPARATION; one breath finds 0 errors in 9 | one-breath critique names an error in 25 of 32 trials across the four rods that can do the task at all | **REFUTED** |

What survives of THE CRITIC is smaller and real: on a rod that genuinely gets the answer wrong, a
separate critic repairs it, 0 of 8 to 5 of 8, at 6.4 times the input tokens and about five times the
wall clock. That is a receipt for C-43, C-50 and C-78. It is not the receipt the chapter first wrote.

**The reason they failed is one mistake made five times.** Every retracted claim was measured on rods
that did not need the organ under test. The judge matrix read *the critic did not help* off models that
had already answered correctly, where there was no wrong answer to repair, so the only thing measured was
the critic's price. A capability's benefit can only be measured inside the failure window of the fuel,
and that window must be **measured before the experiment is designed, not assumed while writing it.**
Law I was in front of me the whole time and I kept testing capabilities outside their own preconditions.

**It carries an organ the architecture never named.** On the word-count task with a fitted frame,
llama-3.3-70b produced the correct enumeration in 8 of 8 trials - *1. the ... 13. wire* - and then stated
the total as 11. Every single time. The answer was in its own output. Reading it off the work instead of
off the last line takes that rod from 0 of 8 to 8 of 8 at zero tokens and no measurable time, because it
is a local regex over text already paid for. The general form is not small: **when a frame names a
method, the answer is in the work, and the model's summary of its own work is an unreliable narrator of
it.** Every architecture that says *show your steps, then give the answer* is trusting the least reliable
line of the output. No item in the 86 covers this. The census was built by auditing what the architecture
already described; this was found by watching a rod work - which suggests the census undercounts, and
that the missing items are not only the ones we noticed were missing.

**What it cost to find this out, listed plainly.** Six errors, all mine, all caught - several by the
instrument built to catch them, which is the only reason they appear in a table instead of in the book as
findings.

- A strict-output check silently lost half its condition, so a toxic creature reported itself healthy.
  Checks are now declared objects with fingerprints; weakening one changes its id and makes the rows
  incomparable by construction.
- Preconditions were asserted per task instead of measured per rod, voiding most of two experiments.
- Trial text was stored truncated, so re-analysis off disk disagreed with the live result.
- Experiment records were written in place, and re-running destroyed earlier evidence that cannot be
  recovered. Runs are append-only now, and an existing path is an error.
- Two numbers were written into reference images without deriving either: a file count that is 35, and a
  code claim that greps to zero.
- A pass was typed into an observation record instead of measured.

Nothing here was caught by being careful. It was caught by refusing to let a number exist without the
command that produced it.

## 8 - What the journey will try to clarify

Four questions, in the order the evidence forces them.

**Does anything survive a change of fuel?** If a construct on a 70b and the same construct on a 9b are
different organisms - and they are - then the only thing that could make them one entity is the state
they share. That is C-80, the single mutable object every layer reads and writes, which the architecture
lists as present and the code does not contain. Thirty-five separate files hold that information today,
each written alone and read alone. One self, or thirty-five. Chapter II settles it, and roughly forty
further items wait behind the answer.

**Can the precondition set predict, rather than explain?** Right now it is a good story told after the
fact. A law that cannot say *this organ will pay on this rod and not that one* before the run is
bookkeeping. The test is a calibration table: measure each task's failure window per rod first, then
predict, then run.

**How badly does the census undercount?** THE READOUT was found in an afternoon by reading output rather
than documents. If auditing the architecture missed an organ that cheap and that consequential, the 22
items marked missing are a floor and not a count.

**Is completeness even the goal?** Eighty-six items, twenty anchored, eight measured, and the repeated
lesson is that most parts are tax most of the time. A creature with every organ seated measured 76 to 94
percent waste. The end state the canon describes is not a construct containing everything; it is C-64,
sustained unattended operation on a stated fuel, and it may well be reached by a creature that declines
most of its own catalogue.

The chapter does not close with a working mind. It closes with something more useful at this stage: an
instrument that can tell whether a claim about a mind is real, and a scoreboard where two laws stand,
three fell, and one organ arrived that nobody had named. Four of twenty-five rungs. Sixteen percent
walked - and the sixteen percent is measured now, not asserted.
