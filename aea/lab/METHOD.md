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
