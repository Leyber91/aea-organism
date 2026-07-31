# THE QUALITIES A STEP MUST HAVE. The standard a whole-entity test is measured against.

Named 2026-07-31, after `vital.py` was built asking only two questions - *did the function run* and
*did something change* - and Luis stopped it: *"we think about the test, but we don't think the level
that the test has to go through, the qualities they have to measure in order for it to pass and to
function. To make a test means to measure the quality in all the possible angles."*

He is right, and the gap was live in the file. A step that RUNS and CHANGES SOMETHING can still be
wrong, dishonest, unbounded, unattributable, irreversible, and fatal to the process that hosts it.
Presence is one angle out of ten.

**A STEP OF THE LADDER IS NOT DONE WHEN IT WORKS. IT IS DONE WHEN IT HAS EVERY QUALITY BELOW THAT
APPLIES TO IT, AND EACH ONE IS PROBED SEPARATELY.** A quality with no probe is an opinion.

---

## THE TEN ANGLES

| # | quality | the question | what it catches |
|---|---|---|---|
| 1 | **RUNS** | did this function execute, in this organism, just now? | dead code that static reachability calls live |
| 2 | **EFFECT** | did the world change, measured before and after? | `_apply_knob` returning False for hours |
| 3 | **CORRECT** | is the thing that changed the RIGHT thing, to the right value? | a stamp landing on an object nobody reads |
| 4 | **HONEST** | does the record of what happened match what happened? | "EXHAUSTED: every move has been tried" when none was |
| 5 | **BOUNDED** | does it terminate, and does nothing grow without limit? | the livelock: a move proposable but never appliable |
| 6 | **STABLE** | do N runs give the same answer; does it drift? | a test that passes alone and fails in a sweep |
| 7 | **ISOLATED** | is production untouched by running the test? | `test_knobs` persisting 32000 into the live store |
| 8 | **ATTRIBUTED** | does every record name who made it? | 4,925 synthetic rows indistinguishable from history |
| 9 | **REVERSIBLE** | can the change be undone, and is the undo exercised? | a knob that could be raised and never cleared |
| 10 | **DEGRADES** | does a failure here leave the organism alive? | a bookkeeping error killing the tick |

Every one of those ten "what it catches" columns is a defect that actually occurred in this repo, and
eight of them occurred on the single day this file was written. None was caught by asking *did it
run*.

---

## THE RULES

**A QUALITY WITHOUT A PROBE IS AN OPINION.** Each quality a step claims must name the specific check
that measures it, and that check must be able to FAIL. `verify_detectors`' law applies here too: a
probe never shown a case it must catch has not been tested, only run.

**PRESENCE IS THE WEAKEST ANGLE, AND IT IS THE ONE EVERYONE BUILDS.** RUNS and EFFECT are cheap and
they were the whole of the first `vital.py`. They are necessary and they are the floor.

**CORRECT AND HONEST ARE DIFFERENT QUESTIONS.** A system can do the right thing and record it wrongly
(the census stamp), or do the wrong thing and record it accurately (the entity reporting its own 429s
for 101 ticks). Both are failures and neither implies the other.

**BOUNDED IS NOT OPTIONAL FOR AN AUTONOMOUS LOOP.** Anything that runs unattended forever must be
shown to terminate or to be capped. The livelock this file was written after would have proposed the
same inapplicable move on every tick, for weeks, while every other angle stayed green.

**NOT EVERY QUALITY APPLIES TO EVERY STEP, AND THE OMISSIONS ARE DECLARED.** A step that claims eight
of ten names the two it does not claim and why. Silence about an angle is how an unexamined risk
becomes a green tick.

---

## HOW A STEP DECLARES ITSELF

In `aea/lab/vital.py`, each step of the ladder carries its functions, its effects, and the qualities
it claims - and the run reports per-quality rather than per-assertion, so a step that is merely
present is visibly distinguishable from a step that is finished.

    step: R3.5 the entity changes its own configuration
      RUNS        _apply_knob, knobs.set, knobs.get executed
      EFFECT      a knob VALUE differs before and after
      CORRECT     the value equals what the move asked for, clamped to declared bounds
      HONEST      the knobs history row says what actually happened, including refusals
      BOUNDED     a move that cannot be applied is not offered again forever
      STABLE      two identical stuck ticks do not produce divergent proposals
      ISOLATED    production knobs.json is byte-identical after the run
      ATTRIBUTED  the history row carries by="wake", never "unattributed"
      REVERSIBLE  set(knob, None) returns it to the declared default
      DEGRADES    a refused or failed knob write does not raise into the tick

That is the level a test has to go through.
