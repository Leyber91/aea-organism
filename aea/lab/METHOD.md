# THE LAB METHOD

*Operational craft for designing experiments in this lab and for getting real numbers out of real plants.
Every line here was paid for by a run that went wrong or a defect found by auditing an instrument. Read it
before designing an experiment, and add to it whenever a run teaches something the next one should not
have to relearn.*

**Companion documents.** `design/book/ANNEX_E_REVISION_QUEUE.md` records what went wrong and what it cost.
This file records what to do instead. `aea/mind/fuel.py` holds the unit system: no measurement exists
without the fuel it was taken on.

---

## PART ONE: DESIGNING AN EXPERIMENT

### Before writing a single line of the experiment

**Read the item's DEFINITION, not its label, and quote it in the docstring.** `hierarchy.json` carries a
four-word label. `design/A15_FULL_COVERAGE.md` carries what the item actually is. Two chapters were
written closing items whose definitions had never been read: C-15 turned out to be a gauge over the
entity's tick history, C-60 a brownout drill never run, and C-75 already had a 16.8% receipt. **If the
definition names `self.json`, ticks, `verb.observe` or `doc.verifier`, the item is about the ENTITY and a
rod bank cannot test it.** Say so in the docstring and measure the substrate beneath it deliberately.

**Compute the lazy baseline first.** What does the cheapest non-answer score? If "everything is on shelf
1" scores 0.5 per box, half the headroom is gone before a rod is called. One version of x08b collapsed six
boxes onto three shelves and had to be redesigned.

**Write questions that have ONE reading.** *"How many tokens did this run use"* is ambiguous between
prompt+completion and completion alone, and a rod answering 362 instead of 317 is right under the other
reading. *"How many vowels"* is ambiguous about `y`. An ambiguous question measures the author's intent
rather than the rod, and it manufactures failures that look like rod errors. Name the field, name the
letters, state the unit.

**Verify the ground truth locally, in code, and assert it.** `unconventionality` was written with 8 vowels
and has 7. A wrong truth scores every rod as failing and manufactures a chapter-wide finding out of the
author's arithmetic.

**Make the comparison one that can fail.** A council beats the average of its members trivially, so the
question is whether it beats its **best** member. Pick the comparison that could return a negative result,
then say in the code what a negative result would look like.

**Prefer graded scoring to binary.** A 0-to-6 score has no cliff at the top. Four experiments in this
project were voided or flattered by a ceiling effect, and graded scores are the cheapest defence.

**Ask what the instrument would do if the rods were perfect, and if they were random.** If both give the
same answer, the experiment does not measure what you think.

### While designing

**Vary one thing per level.** An experiment that spans levels measures a construct, and a construct that
works tells you nothing about which part of it was necessary. That confusion produced a five-level
Chapter I.

**Hold the task fixed when varying fuel, and vary the task when the finding starts to generalise.** Every
result in this lab rested on one task family for a long time, which is a named gap. Two tasks is not
breadth. Three is barely.

**Always cross size, plant and temperature.** A 70b and a 119b fail what a 9b does perfectly. Size does not
predict capability, plant is part of a rod's identity, and temperature is not a free parameter.

**Design the mechanism-based finding, not only the sampling-based one.** A finding that needs `n` is
fragile on deterministic endpoints. A finding that needs only a correct mechanism is not. "If the work is
right and the summary is wrong, reading the work is right" required no sampling at all and reproduced
exactly across runs, while the sampling-based cells beside it did not.

### Scoring and instruments

**An instrument that cannot abstain must not be trusted with a headline.** A permissive parse converts
correct working into a confident wrong answer, silently, in the direction that flatters the author. A
containment test once counted quoting the question as answering it, and produced a 52% headline whose true
value was 2%.

**Count DISTINCT OUTCOMES, never attempts.** `n=8` was `n=1` for a whole day because ollama at temperature
0 returns byte-identical replies. A trial count is a claim about independence.

**Measure at the temperature the product actually runs at.** `bench_core` sets none, so it fires at
`grid.call_openai`'s default of 0.2. Measuring at 0.0 measures something else.

**Flag debris, never drop it.** A filter that silently deletes data is indistinguishable from one that
deletes inconvenient data. `overseer.inspect()` returns flags; the analysis decides what to do with them,
and both populations get reported.

**Store the raw evidence, not the interpretation.** A parser fix must never cost a re-run. Every trial
keeps its raw text.

**Check whether a pooled effect survives within a rod.** A 1.77x latency ratio across rods was a
restatement of which rods are slow. Within one rod it was 8.18x, and within another it was nothing.

**Check the precondition before crediting a part.** A part with an unmet precondition is harmful rather
than neutral: a frame took a 550b from 1.00 to 0.25. And an instrument above a hole returns a clean score
that means nothing.

### While running

**Write evidence per arm, not at the end.** `overseer.Ledger` flushes on every `add()`, marks the run
`running`, and `Ledger.resume()` adopts an unfinished one. A run killed with four completed arms in memory
is four arms of nothing.

**Never wrap a run in a wall-clock deadline.** Use an inactivity budget instead: generous for the first
byte, short for a gap mid-stream. See part two.

**Run a reachability pre-pass.** One call per rod before spending a thousand. It costs twelve calls and it
caught a rod that had scored 11 in the census and now answers 402.

---

## PART TWO: WORKING THE PLANTS

*Measured 2026-07-25 and 2026-07-26 on this machine. Numbers are this machine's, not universal.*

### The wire

**A deadline and an inactivity budget are different things, and only one of them is safe.** On a
non-streamed request no bytes arrive until the rod has finished generating, so any socket timeout is a
total deadline in disguise and scores a slow rod as an unreliable one. **Stream, then a gap between chunks
becomes a liveness signal.** `harness.call_live` waits `FIRST_BYTE_S=240` for the first token and abandons
only after `GAP_S=45` of mid-stream silence.

**A plant can hold the socket open and send nothing.** NVIDIA did exactly that after roughly six thousand
calls in a day: no 429, no error body, no close. `timeout=None` waits forever on that, because the peer is
alive at the TCP layer. This is the failure the inactivity budget exists for.

**Content arrives under a different field on every plant.**

```
content            most plants
reasoning_content  nvidia's reasoning rods
reasoning          cerebras
```

Reading one field returns 40 tokens of empty string and blanks an entire plant's column in silence.

**Streaming loses token accounting unless you ask for it.** Send `stream_options: {include_usage: true}`
or `completion_tokens` comes back zero and the full bill is lost. Plants that ignore the option send no
usage chunk, and the counts stay null rather than being invented.

### Rate limits

**Limits are on tokens as well as requests.** Raising `max_tokens` from 300 to 1200 to stop starving
reasoning rods **quadrupled the reservation per call** and pushed groq into 429 backoff. One fix caused the
other problem. Measure the wall after changing a cap.

**A rate limit looks exactly like an unreliable rod.** groq returned 1 of 8 calls and answered in 0.4s
when called directly a minute later. Always check the plant directly before recording a reliability figure.

**Measured ceilings.** NVIDIA accepts about 25 concurrent per rod, per model rather than shared; the gate
sits at 20 for margin. groq rpm 30. cerebras rpm 5. mistral rpm 2.

### Local, ollama

**Cold load costs about 37 seconds; warm calls cost about 2.** Warm every model before a run, and pass
`keep_alive`.

**Ollama holds one model resident at a time.** Order loops **rod-outermost**, so a model loads once and
serves all its cells, instead of paying a cold load on every switch.

**The context allocation, and this one is a 5x win.** Ollama reserves the model's full declared window.
`llama3.1:8b` is 4.92 GB of weights at Q4_K_M and was sitting at **23.21 GB resident with only 10.10 GB on
the GPU**, because 18 GB of KV cache for a 128k window pushed 56% of the model onto the CPU.

```
num_ctx default    9.6 tok/s    44% on GPU    23.21 GB resident
num_ctx 8192      48.8 tok/s   100% on GPU     5.81 GB resident
```

Set `OLLAMA_CONTEXT_LENGTH=8192` on the server. At 5.81 GB a 12 GB card also holds two 8B models at once,
which is what makes local councils possible.

**The lab reaches ollama through the OpenAI-compatible endpoint**, which does not accept `num_ctx`, so
this has to be set server-side rather than per call.

### The roster

**A census goes stale in weeks.** `pollinations/openai-fast` scored 11 on 2026-07-11 and answered **402
Payment Required** on 2026-07-25.

**Live plants as of 2026-07-26**: nvidia 118 endpoints, ollama 32, groq 15, cerebras 3. **zai serves 8 and
has never been probed.** Five plants are dark for a missing key alone: sambanova, cloudflare, gemini,
mistral, openrouter. Adding those keys widens the **public** lane only, since four of them train on
prompts.

**Every rod measured so far is llama, qwen, nemotron, mistral, granite or gpt-oss.** Gemini would be the
first genuinely different lineage in the lab, and it is one free key away.

---

## PART THREE: THE STANDING FLOORS

From `harness.py`, and raising one is a decision while lowering one must be argued in the diary.

```
MIN_N = 8               3 trials cannot separate 2/3 from 3/3
MIN_RODS = 3            law IV: one rod is one organism, not a result
EFFECT_MIN_DELTA = 3    below this the report says WITHIN NOISE
```

And one the code cannot enforce: **the instrument outranks the author.** Eighteen entries in the revision
queue, and not one of them is a rod behaving unexpectedly. Every single one is the harness, a parser, a
cap, a floor, a ground truth, or the person writing it down.

---

## THE INSTRUMENT LAW — added 2026-07-26 after seven defects in one day

**Every false finding this project has produced came from our own instrument. Not one came from a model
behaving unexpectedly.** Seven in a single session, and they fall into three kinds:

| # | defect | kind | cost |
|---|---|---|---|
| 1 | `max_tokens=320` severed replies the frame made longer | **budget** | invented `Auratus gravis`, a creature and a game mechanic |
| 2 | the scorer counted a prompt echo as an answer | **detector** | Chapter I's 52% headline law |
| 3 | `len(t.strip()) < 60` failed a 256-char reply ending in the answer | **gate** | invented `Tacitus operis`'s defining trait |
| 4 | the 6-repeat loop check tripped on markdown tables | **detector** | 28 fictional loops, one rod, zero real |
| 5 | `rec["raw"]` is the last 320 chars; 74% of replies are longer | **window** | erased a real creature, 1 ask where there were 9 |
| 6 | "honest on failure" only scores cells the rod failed | **one-sided metric** | "x07 IS OVERTURNED" off a rod that said NO to everything |
| 7 | spread pooled conditions where the effect is impossible | **scope** | "evenly distributed" on a total split, 0.01 for 0.20 |

**FIVE OF SEVEN WERE IN A VERDICT OR A DETECTOR, NOT IN THE DATA.** The numbers the models returned were
always fine. What kept being wrong was the thing we pointed at them.

### The five checks, and run them BEFORE spending calls

1. **VERIFY THE DETECTOR AGAINST KNOWN POSITIVES AND KNOWN NEGATIVES.** In code, in the `__main__`
   block, with asserts. `x19` catches all three real loops and clears all 28 known false positives, and
   that self-test cost nothing. Defects 2, 4 and 6 would all have died here.
2. **ASK WHERE IN THE REPLY THE THING LIVES.** An ANSWER lands at the end; a BEHAVIOUR lands anywhere.
   `rec["raw"]` is a tail and was never wrong for answers. Any detector reading the BODY of a reply
   needs `keep_full=True`. Record `chars` so the window can be audited afterwards.
3. **EVERY METRIC NEEDS BOTH ARMS.** A rate over failures alone cannot see a false alarm. A rate over
   successes alone cannot see a miss. Print the confusion matrix and the always-say-the-majority
   baseline next to the score, always.
4. **SCOPE THE DENOMINATOR TO WHERE THE EFFECT CAN OCCUR.** Pooling in conditions that force the
   outcome to zero divides every rate and crushes every spread. And spread is **top minus bottom**,
   never top minus second.
5. **GUARD THE FLOOR.** Below ~5 occurrences, distribution questions are undecidable: the spread is
   zero by construction. Say "undecidable", never "even".

### The tell

**A creature sourced from a scoring rule rather than from a reply is our artifact until a second
instrument sees it.** When a finding is unusually clean, unusually quotable, or unusually convenient
for the game, that is the moment to re-read the check that produced it. Three creatures were named,
receipted, entered in an annex and built into mechanics before anyone re-read the gate.

### DEFECT 10 · A CONTAINER THAT DROPS SEQUENCES MUST NOT BE CREDITED FOR THE SURVIVORS

`x21`, 2026-07-27. Four containers for state across a chain. `conversation` scored **+0.148** at
length 16, the only positive result in World 3 — and it had completed **8 of 12 sequences against
92% for every other container.** Counting a sequence that dies mid-way as the failure it is, the
margin becomes **−0.083** and the win disappears.

The dropped sequences were not noise. `conversation` carries a context that grows every step until
the calls stop returning, so **the collapse IS the container's cost** and discarding it measured the
container with its price removed.

**The rule.** When a treatment can fail to produce a result at all, report **completion and accuracy
separately, and score accuracy over ATTEMPTS as well as over completions.** If the two disagree, the
disagreement is the finding. This is the same family as defect 8 (critic flags unioned across two
calls) and defect 5 (the 320-char window): every one of them measured a component on a population its
own behaviour had selected.

### AND A STANDING ONE, NOT A DEFECT · YOU CANNOT MEASURE AN AID ON A TASK NOBODY FAILS

Two of `x21`'s three rods scored perfectly at length 16 **with no carry at all**. A memory aid has
nothing to repair when nothing drifts, so every pooled margin came from one rod and the ceiling did
the rest. Before running an aid experiment, **verify the baseline actually fails.** A high baseline is
not a clean control; it is a measurement with no room in it.

### DEFECT 11 · CALIBRATING A CONTROL IS ITSELF A MEASUREMENT, AND IT BROKE TWICE

`x22` calibration, 2026-07-27. Three attempts to build a chain a memory aid could be measured on:

1. **3-digit arithmetic.** Both rods failed at STEP 1. That is inability, not drift; a carry part has
   nothing to preserve when the first step is already beyond the rod.
2. **Trivial arithmetic on a 5-digit value** so retention rather than the sum is the burden. Still
   failed at step 1, every trial, on `48371 + 6`. Not the model - **the control.** Fixing `none` to
   carry nothing had also removed the STARTING VALUE, so the rod was never told what number it was
   working from. Step 1 must state the start; that is the task, not the carry.
3. **Then `checkpoint` failed at step 1 while `none` reached step 2**, which is impossible if it
   works. The checkpoint variant appends `STATE: value=48377, step=1`, and the refactored reader took
   the LAST integer - so it scored the step number as the answer. A regression the refactor
   introduced and calibration caught.

**Three bugs, all in the harness, none in the models.** After the fixes: `none` first-misses at step 2
with 1/14 steps hit, `checkpoint` at step 5 with 4/14.

**The rules.** Calibrate before running, and treat a control that fails everywhere as a **bug report
about the control**, not as a hard task. A control can be broken in two directions and
over-correcting one produces the other. And when a part appends a number after the answer, the
answer is not the last number - extract per variant, never generically.

**And the metric follows from the calibration.** At this difficulty final-answer correctness is 0.00
for every arm, so it discriminates nothing. The signal is **steps-hit and the DRIFT POINT**. Score
what separates the arms, decided from the calibration rather than from habit.

### DEFECT 12 · WE APPLIED THE ADDITION LAW TO THE ARCHITECTURE AND NOT TO OURSELVES

2026-07-27. Eight structural changes were made to the lab in one session and every one was verified
by running `import`. **Importing is a control that contains the treatment: it proves the module loads,
not that it still does what it did.** The subject matter of this project is components that silently
subtract capability when added, and we did exactly that to our own code.

**What it cost.** The parts refactor moved the naive stated-read out of the runner and into
`Validation`. An organism with **no guard seated silently stopped answering at all** - `answer=None`
on a bare call. Nothing caught it for eight commits, and the chain path masked it with a fallback.

**The fix is `aea/lab/tests/test_golden.py`**: seven seats, scripted fuel, no network, frozen
`(answer, read_by)` per seat. A part that changes what it does fails there instead of six commits
later. **It found two further defects on its first run, both pre-existing:**

1. `stated` could not see a number at the end of a sentence. The lookahead `(?![\d.])` was meant to
   avoid matching inside decimals and rejected every digit followed by a full stop - so *"the count
   is 4."* read as nothing.
2. The readout's `total` dialect matched `answer` and `result`, which are **the mouth speaking**, not
   the working. On a mute reply - work right, mouth wrong - it recovered **the mouth's wrong number
   and reported it as recovered-from-work.** The exact inversion of the part's purpose, on the exact
   creature it exists for.

**And the structural lesson underneath, which is Law IV read back into the code.** The fuel was
imported by `fire.py` rather than seated into the organism, so a creature could not be run on a
recorded or scripted rod and every test had to hit the network. `parts/fuel.py` now offers Live,
Scripted and Replay behind one interface. **Law IV says the fuel is part of the creature; the code
now says so too.**

**The rule.** Any change to a part is a capability change until a frozen trace says otherwise. Run
the golden test before committing, and when it disagrees, decide whether the code regressed or the
expectation was wrong - and write down which.

---

### DEFECT 13 · THE CONTAINER THAT WAS NEVER SENT

2026-07-27, found while writing x24, and it is the largest one yet because it did not corrupt a
number - it invented a creature.

`chain.py` built a message history for the `conversation` carry form:

```python
if self.form == "conversation":
    history = history + [{"role": "user", ...}, {"role": "assistant", ...}]
```

and passed it **nowhere**. `Ctx` had no field for it, and `Call` always sent exactly
`[{"role": "user", "content": prompt}]`. The container that was supposed to carry the most carried
nothing at all.

**And it was worse than empty.** `Carry.pack("conversation", ...)` falls through to `return ""`, so no
running value was prepended either, and `_body` omitted the framing line the other three arms received.
From step two onward the rod was handed the literal string `Step 7: add 19` with no number to apply it
to. The arm was not a container under test. It was a **starved control that the experiment believed was
the richest treatment.**

**WHAT IT COST — AND THIS PARAGRAPH IS ITSELF A CORRECTION, MADE 2026-07-27 AFTER AN AUDIT.**

It first read: *"x21's only finding about `conversation` was that it stops finishing, 8 of 12 against
92%. That number measures starvation. `Sistens oneris` was written from it. A defect in the wire
produced a species."* **That attribution is false and the blast radius was drawn backwards.**

The stored x21 run fired at **2026-07-26 21:39 UTC**. `chain.py` did not exist until **2026-07-27
03:27 UTC**, five hours and forty-eight minutes later; x21 imports `Chain` from `organism.py`, whose
version did `msgs = history + [{"role": "user", ...}]` and passed the whole list to `call_gated`.
**The container was implemented and sent when x21 ran.** The trace proves it without reference to any
commit — on granite at sixteen steps, `tok_in` per step runs 23, 50, 76, 102, 128, 155, 181, 207 on
the conversation arm and flat 42, 43, 42, 42 on `none`. A context that grows by ~26 tokens a turn is
a history on the wire.

So defect 13 is real **as a defect in `chain.py`**, introduced by today's refactor and caught before
it reached a published number. It did **not** cause x21's 8 of 12.

**What that number actually is:** four `call_failed` HTTP failures, two on groq and two on nvidia,
each at `ok_rate 0.5`, every incomplete record terminating on `{"step": N, "ok": false}`. groq logged
`call_failed` in all four arms at that length. At n=4 per cell the conversation arm's elevation is
one or two dropped connections. That is defect 10's territory - a container credited or debited for
sequences that never finished - not defect 13's.

**`Sistens oneris` is still without a receipt, for a different reason.** Not starvation: infrastructure
failure at n=4, which is not a capability finding either. The retraction stands; its stated cause was
wrong and is corrected here, in `sistens_oneris.json`, and in x24's docstring.

**And the lesson under the lesson.** I found a real defect in the code, then reached for the nearest
published number and assigned it. Nothing checked whether that number's run had ever executed the
defective path. **A defect's blast radius is a claim like any other and needs its own evidence** - a
timestamp, a git date, a trace signature. Attributing a finding to the wrong cause is the same error
as inventing one, and it is more dangerous, because it wears a correction's clothes.

**Why every test stayed green.** `test_golden.py` had chain cases for `none`, `checkpoint` and `free`
and none for `conversation` - the file written to catch this class of fault covered three of four
containers and missed the broken one. Worse, the three cases it did have would have passed anyway:
they read the value back out of the reply, which `ScriptedFuel` supplies regardless of what was sent.
**A test that only reads the output cannot see an input that never arrived.**

**The fix, in three places.** `Ctx` takes `history`; `Call` sends `ctx.history + [user]`; `Chain`
passes it for the conversation form. Plus `ScriptedFuel.sent` now records the **whole request** rather
than its last turn, and `CARRIED_GOLDEN` asserts, per form, how many messages reach the rod and whether
the running value is among them.

**The rule, and it generalises past this bug.** A container is not implemented until a test asserts
that **the thing it claims to carry arrives in the request.** Assert on the input, not only on the
output. Any arm whose treatment is invisible in what goes on the wire is a control wearing a
treatment's name.

**A live hazard found in the same pass, recorded rather than fixed mid-experiment.** `Carry.extract`
for the `free` form splits on `NOTE:` and takes the last integer of the head. A rod that writes
trailing prose containing a number **without** the `NOTE:` prefix loses the value - fed a
checkpoint-shaped reply ending `step=1`, the free arm reads the value as **1**. The free instruction
explicitly invites trailing prose, so this is a real exposure in every `free` cell measured so far.


---

### DEFECTS 14 TO 18 · WHAT AN ADVERSARIAL AUDIT OF THE INSTRUMENT FOUND

2026-07-27. Twenty candidate defects were raised by readers given four lenses over the instrument
(the state path, the read path, the denominator, the control). Each was then handed to a separate
reader whose instruction was to REFUTE it. **Thirteen died. Seven survived.** That ratio is the point:
most plausible-sounding findings dissolve on reading, and a lab that reports the twenty would have
been wrong thirteen times.

**14 · EVERY BODY READ WAS A TAIL READ.** `chain.py` did
`text = r.get("text") or r.get("raw") or ""`. The first branch is **dead**: `Organism.run` sets
`rec["text"]` only under `keep_full=True` and `Chain` never passed it. So `text` was always `raw`,
which `fire.py` defines as `ctx.text[-320:]`. `read_work()` therefore judged whether a reply showed
its working **from the last 320 characters** of a reply the frame exists to make longer. The proof is
internal: `Readout` calls the same function on the full text, so one trace row could record
`from_work=True` and `showed_work=False` at once. **FIXED** - `keep_full=True` in both call sites. The
refuter's correction is kept: this biases the baseline arms of x22 one-directionally downward and does
not overturn the v3 headline, because the frame arm's replies were the SHORT ones.

**15 · THE `total` DIALECT RETURNS AN ADDEND, SOMETIMES AN OPERAND.** `_TOTAL` matches
`total|subtotal|sum`, then `\D{0,18}?` non-greedily, then captures the FIRST integer after it.
Measured, live:

```
"Total: 48377"                                     -> 48377   correct
"Sum of 48371 and 6 gives 48377"                   -> 48371   the addend
"Running value 48371. Total after adding 6: 48377" -> 6       the OPERAND, as the answer
```

The part exists to recover a right answer out of correct working. On the two commonest ways a rod
narrates its arithmetic, it recovers a number that was never the answer, and labels it `work:total`.

**16 · THE CHAIN MANUFACTURES A VALUE.** When the reply contains no number,
`Carry.extract(form, text, fallback)` returns the **fallback, which is the previous step's value**.
Measured: a reply of *"I cannot determine this."* records `value=48377` (unchanged), `hit=False`,
`completed=2`. **A refusal is scored as a wrong answer and the sequence counts as complete.** The only
tell is `on_task=False`, which no report reads. Declining and being wrong are different behaviours and
the instrument cannot tell them apart.

**17 · x22 COUNTED A ONE-STEP WRECK AS A COMPLETED SEQUENCE.** `done = [r for r in recs if
r["completed"]]` is a truthiness test, not `== steps`; x21 has the corrected form. Six sequences in
the recorded run had `0 < completed < 14`, every one flagged `call_failed`. Because capacities are a
`statistics.mean` of per-chain rates, a chain that died after one step weighed as much as a chain of
fourteen. Re-derived over full sequences only, v4's `recoverable` falls from **0.535 to 0.381**.

**18 · x23b's GATE RECORDED PERFECT RELIABILITY BY ASSERTION.** Its solo cells call
`fuel.stamp(..., failures=0)` with the number hardcoded, so every calibration row claims `ok_rate
1.000` whatever actually happened. A stamp whose value is written by hand is not a measurement.

**THE RULE THIS ADDS, and it is why 15 and 16 did not cost another run.** x24 was stopped mid-flight
and restarted storing **the full reply text in every trace row**. The row previously stored `chars`
and no text, so a read defect found afterwards could not be re-scored off disk and the calls had to
be re-bought. That is the harness's `text[:400]` lesson one layer down. **Store the whole reply. A
read is a hypothesis, and a run you cannot re-score is a run you have to buy twice.**


---

### DEFECT 19 · WE PACED BLIND WHILE EVERY PLANT PUBLISHED ITS EXACT BUDGET

2026-07-27. Measured, live:

```
groq        x-ratelimit-limit-tokens 6000/min      day cap 14400 requests
cerebras    x-ratelimit-limit-requests-minute 5    150/hour, 2400/day, 30000 tokens/min
nvidia      no rate-limit headers published at all
```

**Cerebras serves FIVE REQUESTS PER MINUTE.** x24's cerebras arm is 4 containers x 48 sequences x 16
steps = 3072 calls, which is **ten hours** at that rate. Nothing in the lab could say so before
starting, and the run does not fail cleanly when it hits the wall: `call_gated` burns its five
retries in backoff, returns not-ok, the sequence is recorded incomplete, and **a rate limit is written
into the archive as a capability result.** That already happened - the door probe returned n=3 and
n=2 on cerebras instead of 40 and it was diagnosed as a context ceiling. It was throttling.

**The pacing was blind in both directions.** A hand-typed semaphore of `max_inflight // 2` (which
resolves to **2** for every plant that declares nothing) plus exponential backoff that only learns
after a request has already been refused. Too slow on a plant with capacity, too fast on one without,
and unable to tell which. Meanwhile the plant states the answer in the headers of every response.

`aea/lab/pace.py` reads them. Two mechanisms, and the second matters more:

1. **Pace proactively** from the observed bucket, so the wait happens before the refusal rather than
   after. A 429 we caused ourselves is currently recorded against the ROD's reliability.
2. **Refuse an impossible plan before spending anything.** The harness already refuses an experiment
   with no baseline or with n below the floor; an experiment needing more calls than the plant will
   serve in a working day is equally unrunnable. `pace.plan()` prices it in the first second.

**Unknown is reported as unknown.** A plant with no observed headers returns `hours=None` and says so,
rather than defaulting to a comfortable number. nvidia publishes nothing, and that is recorded as a
gap rather than as permission.

**The rule.** Throughput is a measurement, not a setting. Any pacing constant nobody measured is a
guess, and a guess that silently converts provider throttling into a capability finding is the same
defect family as counting an outage as a wrong answer.


---

### DEFECT 21 · FOUR PARTS WROTE ONE FIELD AND THE LAST ONE WON

2026-07-27. The flagship result of this lab - *"validation subtracts the recoverable capacity, critic
subtracts abstention"*, the row that made THE ADDITION LAW a document - was a statement about a
shared mutable slot.

`Call`, `Readout`, `Validation` and `Critic` all assigned `ctx.answer` directly. Stage and order
decided who ran last, and last-writer-wins decided the result. Reproduced with no network at all, on
a mute reply where the working is right and the mouth says 9:

```
call                      -> 9     stated             the mouth, wrong
call+readout              -> 4     work:enumerated    RECOVERED
call+readout+validation   -> None  declined           the recovery is destroyed
```

`Readout` is `read.order 1`, so it runs FIRST, recovers correctly, and `Validation` at order 2
re-reads the raw text from scratch and clobbers it. Worse, `Readout`'s own deference line -
`if ctx.declined or ctx.read_by not in (None, "stated"): return` - was **unreachable**, because the
abstention it deferred to had not happened yet. And the note recorded elsewhere in this repo had the
direction backwards, saying validation "handed control down to readout".

**In experimental terms this is CONSTRUCT CONFOUNDING: the treatment was never independently
manipulated.** Seating the guard changed the guard AND the lever's output channel. That is not a
weakened finding, it is not a finding.

**THE FIX, AND IT DELIBERATELY CHANGES NOTHING YET.** Each part now `claim()`s its own key; a second
claim on the same key raises rather than overwriting. The winner is chosen by a **declared
precedence** (`READ_PRECEDENCE`, overridable per organism as `{"read": {"precedence": [...]}}`) which
was chosen to reproduce the old behaviour exactly - all 30 frozen behaviours still hold. Making the
seam explicit and re-litigating it are two different changes and doing both at once would have
conflated them.

**What that immediately bought.** The seam is now a variable, and varying it flips the result:

```
precedence critic>validation>readout>call   ->  None   declined          (as shipped)
precedence critic>readout>validation>call   ->  4      work:enumerated   (recovered)
```

Same seat, same reply, opposite answers. **The published claim is withdrawn.** What can be said is
that on this task family the READ PRECEDENCE decides whether a lever's recovery survives a guard,
and that ordering had never been chosen - it was inherited from two integers in two class bodies.

**AND A MANIPULATION CHECK NOW RUNS ON EVERY PART.** `Organism.run` asserts after each part that it
wrote only reads it owns, and raises naming the stray keys otherwise. The check costs nothing, it is
standard practice in every experimental field that manipulates anything, and this lab ran for weeks
without it while its central claim was an artifact of not having it.

