# THROUGHPUT — what the fleet will actually serve, and how to spend it

*2026-07-27. Harvested from four prior repositories and then measured against the live plants. Every
number here was read off a response header or a stored run, never from documentation and never from
memory. Read this before writing an experiment that costs more than a hundred calls.*

`METHOD.md` is about not measuring the wrong thing. This file is about not waiting six hours to
measure the right one — and about the specific way a slow plant turns into a false finding.

---

## 1 · THE BUDGET IS PER MODEL, NOT PER PLANT, NOT PER ACCOUNT

Measured, two models on one groq key:

```
llama-3.1-8b-instant      reset-requests  31m       14400 / day    6000 tokens/min
llama-3.3-70b-versatile   reset-requests  6h51m      1000 / day   12000 tokens/min
```

Different reset windows means **independent buckets**. `_rod_gate` keyed on the PLANT, so every rod
on groq queued behind one semaphore of two, and running two rods concurrently was strictly slower
than the provider allows, for nothing. It is now keyed on `(plant, model)`.

**The consequence for experiment design is larger than the fix.** N rods running at once is N calls
against N separate buckets. So a run goes **WIDE, NOT DEEP**: parallelise across rods, never pile
concurrency onto one. x24 ran its rods sequentially and left five of six buckets idle at every
moment.

**A production content service exploits this by ROTATING models** — a ranked list, round-robin, with
a minimum gap per model. That move is **forbidden here** and the reason is Law IV: the same seat on
different fuel is a different organism, so swapping the model mid-run destroys the thing being
measured. What transfers is not the rotation. It is the fact underneath it, and that fact is free.

## 2 · THE PLANTS PUBLISH THEIR REMAINING BUDGET ON EVERY RESPONSE

```
groq        x-ratelimit-limit-tokens 6000       x-ratelimit-remaining-requests 14056
cerebras    x-ratelimit-limit-requests-minute 5     150/hour    2400/day
nvidia      publishes no rate-limit headers at all
```

We paced with a hand-typed semaphore plus exponential backoff on 429 — blind in both directions,
too slow on a plant with capacity and too fast on one without, unable to tell which. `pace.py` reads
the headers and paces before the refusal instead of after. **A 429 we caused ourselves is currently
recorded against the ROD's reliability.**

Unknown is reported as unknown. nvidia publishes nothing, and that is a gap, not permission.

## 3 · REFUSE AN IMPOSSIBLE PLAN BEFORE SPENDING ANYTHING

The harness already refuses an experiment with no baseline, or with n below the floor. **An
experiment that needs more calls than the plant will serve in a working day is equally unrunnable**,
and `pace.plan()` prices it in the first second:

```
cerebras   3072 calls -> REFUSED - 10.2 h against a ceiling of 6 h, bound by requests
groq       6144 calls -> REFUSED -  9.4 h, bound by tokens
```

**AND THIS IS NOT AN EFFICIENCY POINT. IT IS A VALIDITY POINT.** A run that hits the wall does not
fail cleanly. `call_gated` burns its retries, returns not-ok, the sequence is recorded incomplete,
and **exhaustion is written into the archive as a capability result.** It happened, live:

```
conversation  ollama/granite4.1:3b          correct 37/48   token 144/144
conversation  groq/llama-3.3-70b-versatile  correct  0/48   token   0/6     <- 1000/day cap
conversation  cerebras/gpt-oss-120b         correct  0/48   token   5/23    <- 5/min
```

Same container, same task. Without the header reading, those two rows would have been written up as
"these rods cannot retrieve." **A per-minute limit announces itself as slowness. A daily cap
announces itself as a rod that suddenly cannot do the task, which is indistinguishable from a
finding.** That is defect 19 and it is the most dangerous one in the file.

## 4 · CHOOSE RODS BY MEASUREMENT, NOT BY NAME

`fleet.py` tests every rod with the suite its modality allows, and the spread is not what name
recognition predicts:

```
nvidia/nemotron-3-super-120b-a12b    2.16s    45.8 tok/s   passes every suite
meta/llama-3.3-70b-instruct         47.48s     0.9 tok/s   passes every suite
```

A 120B model, fifty times faster than the 70B we had seated, free, and unused for weeks.

**Classify before testing.** The first fleet pass sent an arithmetic question to all 103 nvidia
models and recorded 60 as `not-served`. They are served — embedding models, protein folders and
speech endpoints were being asked to add two numbers at `/chat/completions`. Recording that 404 as a
property of the model is the oldest void class in this lab committed at fleet scale. A rod whose
modality has no suite is **UNTESTED-BY-DESIGN**, never failing.

**Test wide.** 96 rods across 5 suites finished in minutes, because one call each to 96 models is one
call against 96 buckets.

## 5 · A NESTED CONDITION IS A PREFIX, NOT A SECOND PURCHASE

From a repository that answers 5/15/30/60-minute queries with ONE call at the largest window and
slices the rest locally. Its stated motivation was not cost — separate calls with per-call result
caps produced a **30-minute window reporting fewer events than the 15-minute one.**

Here: `x21` declares `LENGTHS = (4, 16)` and `x06` declares `(10, 25, 50)`, and both buy the short
conditions outright. Nothing length-dependent reaches the wire — `Chain._body` emits only the head,
the step and the container instruction — so **a 4-step chain is byte-for-byte the first four steps of
a 16-step run.**

The call saving is about 3% of a large queue. **The real gain is the pairing**: x21's claim is "holds
at four, drifts at sixteen", tested today between two independent runs at temperature 0.2. Sliced
from one trajectory it becomes within-trajectory, which is `stats.mcnemar` instead of the unpaired
`stats.boot_diff`. The caveat is real and must be honoured: the length factor then stops supplying
independent samples and must not be double-counted.

## 6 · SPEND THE METERED ROD ON THE ONE STEP THAT NEEDS IT

From a repository whose generation pipeline descends in model size as the task becomes mechanical:
an 8b writes the plan, a mini-class model extracts structure at temperature 0.18, a 1.7b converts to
JSON at 0.05, and the mini repairs schema at 0.01. The expensive model is spent only on the single
creative step.

**Here the boundary is sharp and it is Law IV.** Moving the CRITIC to a cheap local rod changes the
organism and manufactures exactly the false-finding class this lab keeps catching. Moving the
READERS does not — extraction sits outside the measurement.

- `parts/read.py` is all regex, and several read defects are ones a small model would not have made.
- `rescore.py` re-reads an immutable archive at zero metered cost and has only regex readers.
- ollama is local, free and uncapped, so work moved there leaves the metered plants entirely.
- `judge_rod` already exists as a harness parameter and is **`None` at every call site**. The
  separate-judge capability is built and has never been used.

## 7 · A TRANSPORT FAILURE MUST NEVER ENTER THE DATA PATH

Found in a harvested repo and worth stating as a law, because it is our defect family in someone
else's code: their client returns `{content: "service unavailable", error: true}` rather than
raising, and the retry loop assigns that sentence to the output and grinds six attempts against a
fixed error string, never checking `error`.

Ours is the same shape one layer down (defect 16): when a reply has no number, `Carry.extract`
returns the PREVIOUS value, so a refusal is scored as a wrong answer and the sequence counts as
complete. **Declining, failing and being wrong are three different events and an instrument that
cannot separate them will eventually report one as another.**

## 8 · THE TWO STREAMS ARE NOT ONE STREAM

`harness.py` read `content or reasoning_content or reasoning`. An `or` chain **concatenates**: on any
chunk where content is empty, the model's chain of thought was appended to the reply. Measured across
96 nvidia rods, **8 of the 12 fastest return a separate reasoning field**, and every gpt-oss reply in
this archive opens *"The user says..."*. The answer was being read out of the thinking.

Fixed, with an explicit `reasoning_only` flag for rods that genuinely answer only in the reasoning
channel. **Every stored gpt-oss result predates the fix.**

---

## THE CHECKLIST, BEFORE A RUN THAT COSTS ANYTHING

1. `pace.plan({plant: calls})` — will it finish today? If not, cut it or move the arm.
2. `pace.afford(plant, calls)` — is there budget left today, not just per minute?
3. Are the rods chosen from `fuels.json` by measured capability, or from memory?
4. Is the parallelism across rods, or piled onto one?
5. Is any condition a prefix of another? Slice it, and then pair the comparison.
6. Is any mechanical work seated on a metered rod that a local one could do?
7. If a cell comes back near zero beside a healthy cell on the same arm, **check the budget before
   believing it.**
