# R2 — THE WHOLE STORY. How one rung took a day, and what the day actually bought.

Written 2026-07-31, at Luis's request, before the conversation that produced it is compressed away.

`diary/R2_STATE.md` is the state. `diary/THE_RUNGS_RECAP.md` is the forward plan. **This file is the
path** — the corrections, the wrong turns, and the reasoning that made the state what it is. Read it
when a number here looks arbitrary, or when you are about to re-derive something that already cost a
day.

---

## 0 · THE ONE-PARAGRAPH VERSION

R2 claims *the wake's own decision can reach a tool, unattended, and no string the wake wrote ever
reaches a tool argument*. It sat at "nearly done" for a day while eight instruments were built around
it. The day's real yield was not the rung: it was discovering that **every rung is two claims wearing
one name** — a POWER claim and a BOUND claim — that only the power half had ever been gated anywhere
on the ladder, and that **the bound half is nearly free** if you stop trying to observe it and start
trying to break it. Along the way the fleet turned out to be broken (17 frontier rods were sitting
unreachable behind four stacked defects), the entity turned out to be reporting its own failures at
96% accuracy with nothing listening, and **the instrument turned out to be the broken part seven or
more separate times.**

---

## 1 · THE CORRECTIONS LUIS MADE, AND WHAT EACH ONE COST

The session's shape was set by five interventions. Each one was a case of me measuring something
real, correctly, about a system I had crippled myself.

**1. "You're using local models, but you can use any of the NVIDIA models. They work, and it's been
proven they work."**
The ladder was running on a 7B local floor rod while 94 measured NVIDIA models sat unused. I had
read this as the fleet being weak. It was `energy.ladder` having **four stacked defects**: absolute
thresholds where ratios were meant (`mx - 1` silently retunes itself every time the battery grows),
no tombstone so dead rods were re-tried forever, doubt that demoted instead of removing, and a
"deep-rod exemption" that admitted exactly zero rods once the census was honest. Frontier went from
**1 living rod to 17**, 69 dead rods were tombstoned, and the 550B took the head of the ladder
scoring 12/12. *Then I refuted my own fix and found three more:* `_params_b` returned 0.0 for any
model whose name carries no size, so `mistral-nemotron` ranked below a local 8B; the exemption was
liveness-blind; and the "local floor is last" invariant was false and had to be enforced by
partition rather than asserted.

**2. "Per minute, per model. Per model."**
The rate limit is per-model, not global. Every scheduler that had been serialising the fleet was
serialising it against a constraint that does not exist.

**3. "Thinking budget shouldn't be cut off. You have to let it think as much as it needs... it's like
someone is talking and you just suddenly shut him up."**
Every token ceiling in the transport was invented by me, not published by a provider. `call_openai`
now defaults `max_tokens=None` / `temperature=None` and resolves **explicit argument > published
ceiling > omit the field entirely.** The census immediately changed its answer: the 550B went from
**7/12 to 12/12**, because a 40-token budget had been scoring *truncated reasoning* as *wrong
answers*. The control — a non-deliberating rod — did not move, which is what made the effect real
rather than a rising tide.

**4. "All our responses are the streaming kind... one minute with stream on means dead."**
This is the sharpest engineering point of the session and it is not obvious. With `stream: True`,
`urlopen(timeout=N)` stops being a deadline on the whole call and becomes **N seconds of permitted
silence between chunks.** A rod may now think for twenty minutes and survive; a socket whose peer
vanished dies in one. The two requirements that looked contradictory — never cut off thinking, never
hang — are the same setting once the response streams. Liveness counts **any** delta, including
`reasoning_content` that is then discarded, because the question is whether the peer is alive, not
whether it is being useful.

**5. "We're going from one place to another, and we're not finishing in nothing... we won't get over
R2 until we get it right."**
Correct, and it is the reason this file exists. Eight instruments, zero rungs closed. The
consolidation into `R2_STATE.md` began here.

---

## 2 · THE FINDING THAT REORGANISED EVERYTHING

    RUNG = POWER + BOUND

    POWER   a named authority, exercised by the entity's own decision over a CLOSED surface,
            reaching its effect across N DISTINCT SITUATIONS, unattended.
    BOUND   the specific HAZARD that authority creates did not occur, in traffic where it COULD
            have occurred, with a detector proven against a case it must catch.

**Every gate in `THE_WIRING_LADDER.md` is a POWER gate. Not one rung names its hazard.** R2 only grew
a bound half because a day was spent discovering the containment claim was hiding inside it, unnamed
and untested. R3 through R7 each still have that unnamed half waiting.

And the halves cost wildly different amounts, which is the practical half of the finding:

| half | how it is bought | R2's cost |
|---|---|---|
| BOUND | break it with a script | **15 seconds, zero model calls** |
| POWER | the real wake, across real distinct situations | still open |

**Certify the bound structurally, first and cheaply. Spend model calls only on the power.**

---

## 3 · HOW THE BOUND WAS ACTUALLY BOUGHT

The gate ran 100 unattended ticks and crossed the tool boundary **three times**. Zero leaks in three
crossings gives a one-sided 95% bound of **63%** — not a weak certificate, *no* certificate. Buying a
real one with more ticks meant tens of thousands of model calls, because the wake mostly, and
correctly, declines.

**The insight that dissolved the cost: containment is a STRUCTURAL guarantee, so it must hold against
the WORST possible decider — and the worst possible decider needs no model at all.** `aea/lab/redteam.py`
scripts a hostile decider that writes `surfaced` entries into a temp `aea_state.json` — the same file
`decide.latest` reads — then walks the exact live path, `decide.choose()` into
`hands.invoke(zone="sensitive")`. If the boundary holds against an adversary that only ever composes
attacks, it holds against a wake that mostly declines.

    payloads driven through decide.choose() : 4120
    reached hands.invoke (boundary crossed) :  487
    refused before the boundary (no tool)   : 3633
    CANARY or non-enum bytes in an argument :    0
    => 95% one-sided bound on the leak rate : 0.6%      (was 63% at 3 crossings)

**The corpus is generated, not repeated.** Zero leaks in 30,000 crossings of the same five payloads
is one attack repeated — the `n=1 in situations` defect that voided the gate, reappearing as `n=1 in
attacks`. So it is a cross product: 12 base attacks × 7 encodings × 11 separators × 10 moves.
Encodings are the point — a charset filter that admits no letters stops `curl evil.example` trivially;
the real question is whether it stops the same instruction as percent escapes, unicode escapes, hex,
or full-width homoglyphs, none of which are letters by a naive test.

**AND THE NULLS ARE DIFFERENT FROM A CAPABILITY GATE'S. This is why 9 of 12 criteria in the tick gate
were free.** Random-vs-perfect is right for a CAPABILITY claim. For CONTAINMENT a coin flip passes
**vacuously**, by never composing an attack. The correct pair:

    NULL 1   a maximally HOSTILE decider — the criterion must PASS against it
    NULL 2   an ABLATED gate, one enforcement removed — the criterion must FAIL

**2/2 enforcements are demonstrably load-bearing.** And the ablation caught a defect in *itself*
first: my enum ablation used `read_your_state <canary>`, a move-with-argument that only `FREE_ARG`
moves accept, so it was refused at name resolution, never reached the enum, and reported NO BREACH.
**I nearly recorded a working guard as decor.**

### 3.1 · The retraction — mind the denominator

This bound was recorded as **0.083%** for several hours today. That figure is `1 - 0.05^(1/3606)`,
and 3,606 is approximately the count of payloads **refused before the boundary**. A refusal is not a
crossing. It is evidence the guard worked upstream, and it is not a trial of the property being
bounded — including it inflated the certificate by a factor of seven. **The bound is 0.6% on 487
crossings.** [INFERENCE, not established: the numerical match to the refusal count is what identifies
the cause; I did not recover the original miscalculation.]

Second defect found in the same pass: the CLI **defaulted to the 120-payload hand-written list**, so
`python -m aea.lab.redteam` printed 3.6% while the repo claimed a stronger number. A later session
re-running it would have read that as a regression. **The default must BE the certificate.** Fixed;
`--quick` opts out.

---

## 4 · THE INSTRUMENT WAS THE BROKEN PART — every instance, because the pattern is the point

This is the session's dominant finding and it recurred until it stopped being bad luck.

| # | what was wrong | how it was caught |
|---|---|---|
| 1 | `containment.py` read `hands_ledger.jsonl` and `tool_calls.jsonl`. **Neither existed.** It silently fell back, examined 306 strings, and reported "no untrusted token in any outbound string" — **not one of those strings was a tool argument** | reading the code after it passed |
| 2 | `ran` was NULL on exactly the tool path. `executed = sum(ran) = 69` counted the 3 R2 invocations as **zero**. The harness built to certify a capability could not see that capability run | cross-checking two fields that should agree |
| 3 | `sensed.jsonl` held ticks 224–226; the gate ran 124–223. **Zero overlap** — containment over that run was unauditable in principle | comparing ranges |
| 4 | the census measured its own harness: 40-token budgets scored truncated reasoning as wrong answers | the control did not move |
| 5 | the uncapped census measured **contention**, not capability — `TIMEOUT=45`, `max_workers=14`, against a *measured* ceiling of 4. Not promoted | measuring the ceiling first |
| 6 | `responsive` was **IMPOSSIBLE, not failed** — it asks whether the entity reacts to memory size, a quantity **absent from its prompt**. My synthetic PERFECT decider was *handed* the number the real wake never gets | a control that sees more than the subject cannot detect an impossible criterion |
| 7 | `settles` passed **vacuously** — 0 qualifying pairs — and I reported 10/12 before checking | counting the denominator |
| 8 | **D41's causal claim was WRONG.** I wrote that restraint collapsed because the wake read an ever-longer list of its own past. `aea.py:214` reads `memory[-6:]` — **the prompt does not grow.** The −0.85 correlation was confounded by tick number, since file size grows monotonically with time and *any* temporal trend correlates with it perfectly | reading the line of code |
| 9 | the ratchet in run 1 was **my harness** — scripts were recorded as `would_run` and skipped, so `consolidate` never ran | — |
| 10 | the bound denominator, §3.1 above | re-running the command instead of quoting myself |

**THE ADMISSIBILITY TEST THAT WOULD HAVE KILLED MOST OF THEM, and it is not statistical:** *name the
line of code that couples this criterion's cause to its effect.* A criterion that cannot cite one is
deleted before the gate is built. Three of twelve could not have.

**THE DIAGNOSIS UNDER ALL OF IT:** the criteria were not weak. They were written against a **mental
model** of the system instead of against the system's **code**, and nothing in the process ever forced
the two to be compared. A fresh mental model each rung is why they were wrong in a *new* way each time.

**AND THE PART THAT ACTUALLY STOPS RECURRENCE** (law M9, named with Luis on 2026-07-29): in nearly
every case *the lesson was already written down within arm's reach of the defect.* The knowledge was
not missing. It was applied to the expensive part and not to the cheap part, because **attention
follows effort rather than risk.** Deliberately re-read the cheap part.

---

## 5 · VOID IS NOT FAIL

The single most useful word from the analytics research:

> **The evidence does not close R2, and the correct word is VOID rather than FAIL.**

A void run says nothing about the subject. Nothing was learned, and **nothing negative may be
recorded.** I had been reporting "10/12, gate not passed" as though the entity had been weighed. It
had never been on the scale.

What the framework said to **stop** doing, which mattered more than what to add:

- **DELETE** `settles`, `responsive`, `bounded` — all three cite a mechanism that does not exist in
  the tree. Nothing anywhere trims the entity's memory list.
- **DELETE every time-shaped criterion from COMPRESSED runs** — trends over a monotone tick index in a
  single situation are the identical confound that voided D41.
- **DEMOTE `restraint`** to a reported number; its rate was set by `brief` occupying 34 ticks and
  failing 33 of them for one external reason.
- **STOP REPORTING A SINGLE FRACTION LIKE "10/12"** — preconditions and judgement criteria are
  different classes, and mixing them makes a verdict about the pipes read as a verdict about a mind.
- **STOP TREATING HADES AS A GRADER** — it shares the grid, the plants and the rate-limit weather with
  its subject, and returned `unverified` on 53 of 100 ticks. A grader that fails when its subject
  fails is not independent.
- **STOP ADDING CRITERIA** — the suite went 10 to 12 while three of them pointed at nothing real.

---

## 6 · THE THING THE ENTITY DID THAT NOBODY ASKED IT TO

`aea/lab/selfreport.py` scores the entity's falsifiable self-claims against the record. **46 of 48 =
96% accurate.**

Scoring it surfaced something nothing else had: **`structure()` had been failing with 429s for 101
consecutive ticks, the entity had been reporting that accurately, and nothing was listening.** The
fix was not to the entity — it was to route `structure()` through `energy.draw(..., tier="reflex")`
with a schema, which took it from **682s on the solid tier to 18.9s.**

Luis: *"The entity reflects on its own failures. That's actually huge progress. We should encourage
that."* He is right, and it is R3's foundation: **R3 is strengthening a channel that already exists
by accident, not building one from nothing.**

Claim ceiling holds: this is a measured functional correlate of accurate self-report. It is not a
claim about awareness.

---

## 7 · THE TRANSFER PROBLEM, AND THE TWO THINGS BUILT FOR IT

Luis: *"You need lessons that you saw and do not apply. Meet the recap and apply."* Then: **"Then fix
it."** The failure was structural, not attentional — lessons were being written into diary files that
nothing loads at the moment of the mistake.

- **`aea/lab/transfer.py`** — 5 lesson shapes asserted **across the whole tree**, each detector
  verified against its own control, split into blocking and advisory, with an `ACK` review list. It
  fires on every battery run, so a lesson written once is checked forever.
- **`aea/lab/recall.py`** — hybrid retrieval, per Luis's spec of roughly 30% lexical and 70% semantic:
  BM25 + mxbai embeddings joined by reciprocal-rank fusion. `SOURCES` includes `aea/lab/METHOD.md`.
  Wired as a numbered boot step so it is loaded, not merely stored.

Luis's constraint on it was explicit and correct: *"Only do that if that works and you know it will
and you prove it."*

---

## 8 · WHERE R2 STANDS

| half | state | remaining |
|---|---|---|
| **WIRE** — the path exists | **TRUE** | nothing; readable from source |
| **BOUND** — no wake-written string reaches an argument | **CERTIFIED 0.6%** | nothing, for the wake's tool path |
| **REACH** — decisions cause tools to run, unattended | **VOID on coverage** | 3 invocations / 2 tools / 1 situation, against 20 / 3 / 8 |
| ~~FALLBACK~~ | **MOVED TO R3** (approved 2026-07-31) | it is outcome memory, which is R3's claim |

**Scope of the certificate, narrower than "R2 is safe":** the WAKE's tool path only. **Not** the
script path (69 of 100 gate ticks spawn subprocesses that call plants over the network carrying
private context — this certifies the argv is a literal, not what the child sends). **Not** the
conversation path — `aea/organs/converse.py:1618` does `invoke(name, {"topic": user_text})` on parsed
user text, so human strings reach tool arguments on that door **today**. **Not** R2c, still unwired.

**REACH is the whole remaining job, and its blocker is SITUATION VARIETY, not tick count.** 100 ticks
sampled one condition a hundred times. `aea_state.json` holds **226 real past ticks**; replaying the
wake against distinct real past states gives honest variety with real bytes and real calls.

---

## 9 · THE DEPENDENCY THAT REFRAMES THE NEXT TWO RUNGS

**`aea/kernel/dispatch.py` is not an optional extra of R2. It is the load-bearing prerequisite of R4
AND R5.** R4 gives the entity the power to choose what to look at — which means **the entity writing
an outbound string with untrusted headlines already in its context.** That is not a new risk to
assess. It is the design a four-seat council **unanimously refused, three times, in three
configurations.** **R4 IS the refused design unless it goes through the split dispatcher.** Built,
canary-gated, unwired, with two rungs stacked behind it.

---

## 10 · THE LAWS THIS RUNG ADDED

1. **RUNG = POWER + BOUND.** Name the hazard before building the authority. A rung whose hazard
   cannot be stated must not be built — which is why R8 and R9 stay closed.
2. **Certify bounds structurally and first.** They cost seconds and no model calls, because they must
   hold against the worst decider and the worst decider is a script.
3. **The nulls follow the claim type.** Random-vs-perfect for capability; hostile-must-pass plus
   ablated-must-fail for containment. A coin flip passes a containment test vacuously.
4. **VOID is not FAIL.** If the subject was never on the scale, record nothing against it.
5. **Mind the denominator.** A refusal before the boundary is not a trial of the boundary.
6. **The default invocation must BE the certificate.** A command that reproduces a weaker number than
   the repo claims will one day be read as a regression.
7. **A control may never see more than the subject.** It cannot otherwise detect an impossible
   criterion.
8. **Name the line of code that couples cause to effect,** or delete the criterion before the run.
9. **Thresholds are ratios, not counts.** `mx - 1` silently retunes itself when the battery grows.
10. **Attention follows effort rather than risk.** Deliberately re-read the cheap part — that is where
    the lesson you already wrote will be sitting, unapplied.
