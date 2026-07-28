# THE SERPAC GRID - the six inside each of the six

*2026-07-27. A 6x6 grid: the claim under test is that the same six classes recur INSIDE each one, so
SEE has its own SPECIFY, its own SEE, its own REMEMBER and so on. Every real component should land at
a coordinate.*

**THIS IS A HYPOTHESIS UNDER TEST, NOT A RESULT.** Each author was required to mark a cell **WEAK**
where it read as a forced analogy rather than a real operation, and a separate reader attacked each
row hunting for cells that should have been marked weak and were not. **A grid honest about its empty
and forced cells is worth more than a complete one.**

**THE CLAIM CEILING WAS ENFORCED BY THE PROCESS.** This project forbids asserting the entity is
conscious, sentient or self-aware. The attackers caught and rewrote every phrase implying awareness,
attitude or inner life - distrust, confidence, deliberation, principle, self-questioning. Those
rewrites are listed per row. The grid describes OPERATIONS. Any richer reading is the reader's.

**ONE CONFIRMED PREDICTION.** x24 measured `checkpoint` completing 43 of 48 sixteen-step chains while
recalling 0 of 240 non-recomputable tokens, against `conversation` at 48/48 and 240/240 on the same
rod over the same sequences. Read through the recursion that is REMEMBER.REMEMBER present and
REMEMBER.ACT absent: carrying forward and reaching back are different operations. The grid named a
split the numbers had already made.

---

## ROW 1 - INSIDE SPECIFY

SPECIFY is saying what is wanted and how. Its interior is tested against the nine real components in
`aea/lab/organisms/catalogue.json`. Result of the test: **one cell occupied by two components, one
cell partially occupied by a recorded flag that gates nothing, four empty, and two of the six marked
WEAK.**

The row's first finding is a limit of the grid rather than a claim about the components. `goal`
(shape.1) and `frame` (shape.2) both land at SPECIFY.ACT, and none of the six sub-classes separates
them. The axis that does separate them is the outer class's own definition: `goal` states WHAT is
wanted, `frame` states HOW. That two-way split is written into the class name and has no coordinate
inside the recursion. Reported here as under-resolution of the grid at this coordinate, and nothing
more. The two components are separately seatable (`Organism(keys)` takes either), separately
configured, and separately manipulated in the experiment record: `aea/lab/x15_L2_the_frame.py` runs a
three-rung ladder whose BARE arm is the goal alone and whose FITTED arm adds the method, plus a cell
that withholds the goal under a frame. Any claim that the frame margin belongs to the cell rather than
to `frame` contradicts that design and is withdrawn.

One scope note, and two cells below turn on it. Prompt text is data IN THE LAB (`catalogue.json`: "A
variant is a data change, never a code change"). It is not data in the entity: `produce_brief`, the
capability this row prices at SPECIFY.CHANGE, builds its prompts in Python inside `aea/organs/`.
Carrying the lab's data rule across that boundary changes what the charter permits, so the boundary is
held explicitly below.

### SPECIFY.SPECIFY - the rule that separates an objective from a procedure   **WEAK**

The operation would be: state what makes a specification well formed, before any specification is
written. The rule exists in this codebase and is exact. A goal states an OBJECTIVE, a frame states a
PROCEDURE, and a frame that states a MANNER is poison. `catalogue.json` encodes it structurally: the
`frame` component carries two variants, `method` (default) and `manner` (`"class": "toxic"`).

**Occupant: none of the nine.** The rule is a static label on a data file plus a comment block in
`aea/lab/chain.py:30-38`. `aea/lab/parts/dna.py:edges()` emits a firing conflict edge when a config
names a toxic variant, which is the only executable trace of the rule anywhere, and it is a derivation
over the wiring graph rather than a seated part.

**And that single trace does not fire on the one creature it was written for.** `dna.py:34` reads
`config[key]["variant"]`. `organisms/creatures/obtemperans_habitui.json` declares
`"seat_config": {"frame": {"names": "manner"}}`. `Frame.run` honours both keys
(`ctx.cfg("frame","variant") or ctx.cfg("frame","names")`, `aea/lab/parts/shape.py`), so the toxic
frame runs, while `edges()` sees no variant and `classify_seat` returns healthy. The run path and the
classification path disagree on a dict key. This is a live defect and it is reported as such, not as a
grid finding.

**Buys:** nothing at run time. It cannot lower a failure rate it never inspects, and as wired it does
not reliably label the case it names.

**Marked WEAK, for a specific reason.** Inside this outer class, "what defines a good spec" and "what
judges whether a spec was good" do not separate into two operations. The same static variant label is
both the criterion and the entire judgment. A cell that collapses into its neighbour is a forced
coordinate. It may separate in a system that authors a new frame variant and needs a standard to author
it against; the row does not get to claim that yet.

### SPECIFY.SEE - the presence flag that gates nothing

The operation, genuinely distinct from SEE inside SEE: judge the INPUT before the call rather than the
output after it. Is an objective present, is it unambiguous, does the method text describe a procedure
that could produce the answer shape the task expects. This is the only cell in the row whose verdict
would be available before any tokens are bought.

**Occupant: `measure` (gauge, judge.1, `can_know`), partially, and after the fact.** `Measure.run`
records `verdict_is_empty = not (ctx.has("goal") or ctx.has("frame"))` (`aea/lab/parts/judge.py`).
That is an input-side read: it tests whether a specification was seated at all. Three limits, and they
are what keep the cell mostly empty. It reads the SEAT, never the spec text, so an ambiguous goal and a
good goal are identical to it. It runs at the judge stage, after the tokens are spent. Nothing consumes
it: `ctx.verdict`, `ok` and the answer are unaffected, and no code path declines a seat
(`aea/lab/organism.py:73` records `precondition_unmet` and proceeds; `aea/lab/parts/base.py:191`
computes unmet requires-edges between COMPONENTS and has no verb for a precondition living in the task
dict). `validation` (guard, read.2, `false_commitment_rate`) reads `ctx.text` only and contributes
nothing here.

The recorded receipt for `arbiter_vacui` (`organisms/creatures/arbiter_vacui.json`) is the mechanism in
one seat: `measure` and `readout` above an ABSENT goal return a clean value. Its recorded figure, 50 of
158 clean goal-absent trials still emitted a number, is flagged PROVISIONAL in the file itself, so the
mechanism is what is cited, not the count. Note the correction that file forces on the usual telling:
the record does carry `verdict_is_empty=true` for that seat. What is missing is anything that reads it.

**Buys, if seated properly: a gauge, and it is the missing one.** Every gauge this project owns
measures the output side. Without a content-level input gauge the `ok` flag is honest about the answer
and silent about whether the question was legitimate. In trust-grade terms that is a promotion earned
on runs whose specification was never read, which is a gauge failure and not a guard failure: the `ok`
flags are individually true and the promotion they compound into is not warranted. The guard axis is
untouched here, because nothing false was committed to.

**What breaks without it, specific to this cell:** every null result on a lever becomes
uninterpretable. "The readout does not help" and "the readout had no goal above it to read against"
produce identical rows, and the one flag that could separate them is a boolean about seat presence that
no report consumes. An empty SPECIFY.SEE costs the ability to attribute an accuracy result rather than
costing accuracy.

### SPECIFY.REMEMBER - the objective across steps of one sequence   **WEAK**

The operation would be: carry the specification, not the value, from step 1 to step n, so that step 7 is
still doing the task set at step 1. Distinct on paper from REMEMBER inside REMEMBER (which carries a
running value) and from SPECIFY.PERSIST (which survives a process death rather than a step boundary).

**Occupant: EMPTY, and the operation is discharged by brute re-transmission.**
`aea/lab/chain.py:71-73` rebuilds the task dict every step and re-emits `STEP_GOAL` and `STEP_METHOD`
verbatim. The spec is re-paid for at every step in input tokens.

**Correction to a claim this cell previously carried.** `carry`'s `conversation` form does NOT
accumulate the prior spec. `chain.py` appends `task["data"]` to `history`; `Goal.run` and `Frame.run`
write `ctx.prompt`, and `Call.run` sends `ctx.history + [current prompt]` (`aea/lab/parts/fire.py`).
Prior turns therefore hold the body without the spec. The x24 tokens live in `self.notes`, which go
into `task["data"]`, so the token is inside the conversation container and the spec never is.

**Marked WEAK.** With the spec re-emitted verbatim in every arm, there is no carrier to ablate, so the
cell cannot be manipulated and cannot be measured. That is the WEAK criterion exactly. It becomes a
real cell the moment an arm exists that states the spec once and stops re-sending it; until that arm is
built, SPECIFY.REMEMBER is SPECIFY.ACT run n times.

**What the cell would cost if it were real:** objective drift, where the value survives and the task
changes underneath it. The closest instrument the lab has is `on_task` in the chain trace (did the step
apply the operation, or hand back what it was given), which detects one symptom and names no cause.
**Prediction, and it is a stated experiment rather than an extension of x24:** build a `spec_once` arm
that emits goal and method at step 1 only, then compare it against the current re-transmitting arm at
sixteen steps. The x24 container split (conversation token recall 144/144, checkpoint 0/144) does not
predict that result, because the spec does not travel in the container those numbers measured. Untested.

### SPECIFY.PERSIST - the spec that outlives the process

Keep a specification identical across restart, so that a streak measured last week is a claim about the
same capability this week. 17 days unattended, 109 ticks, 6 boots: this cell has been crossed six times.

**Occupant: none of the nine, and there is no code path either.** `organisms/tasks.json` holds goal and
method per task. `catalogue.json` holds the frame variants and their templates. `creatures/*.json` holds
`seat_config`, which pins which variant a named creature runs. The `CHARTER` dict in
`aea/kernel/trust.py` holds the entity-side specification of each capability as a one-line `desc`.
Persistence here is discharged by the specs being files, which is storage rather than an operation. What
makes the cell worth a coordinate is what the files do not do, below.

**Buys: the precondition for any gauge being worth anything.** `gather_public` at TRUSTED, streak 39,
runs 44, fails 0, is a claim that survives reboot only because what it was asked to do survived reboot
in the same form.

**What breaks without it, specific to this cell:** the streak silently outlives its own referent.
`CHARTER` is source, `state/` is state, and nothing binds a ledger entry to a version of the spec that
produced it. **Prediction:** edit a `desc` or a frame template and the streak does not reset, because
`trust.record` (`aea/kernel/trust.py:82`) takes only a capability name and a boolean and never reads the
spec; the 39 would then certify a capability that no longer exists. The promotion rule is slow-up,
fast-down on OUTCOMES and has no reaction to the spec moving underneath it. Cheapest fix in the row: a
spec hash on the ledger entry.

### SPECIFY.ACT - the two components that put the spec on the wire

The only fully occupied cell. Make a specification take effect, meaning get it into the request that
leaves the process. `Goal.run` prepends `task["goal"]` to `ctx.prompt`. `Frame.run` wraps the result in
the selected variant template. `call` (enabling, fire.1) then transmits it. `call` is not claimed for
this coordinate: it is the enabling difference between FORBIDDEN and anything at all for every class and
it belongs to the ACT row.

**Occupants: `goal` (lever, shape.1, accuracy) and `frame` (lever, shape.2, accuracy).**

**Buys: two levers, both shortening the path to promotion by lowering the failure rate.** The recorded
receipts, quoted from `catalogue.json` rather than measured here: for `goal`, "x12: 0 of 158 clean
trials succeed with no objective, 0 of 146 more with a vague one", which is an enabling-shaped result
from a component the catalogue types as a lever. For `frame`, "x15: working 41% -> 100%, four rods 0.00
-> 1.00. A METHOD frame only". Both are attributable to their own component: x15's BARE arm is the goal
alone, so the frame margin is measured with the goal held constant.

**What the grid actually says about this coordinate.** Two components, one cell, and the six sub-classes
provide nothing that distinguishes stating an objective from stating a procedure. That distinction is
real, load-bearing and measured (the `manner` variant, recorded receipt in `catalogue.json`, "8/12 ->
0/6 on one rod, 69% -> 9% on another"), and the recursion cannot see it. The honest reading is that the
grid is under-resolved here, and that the outer class name carries a split the inner six do not.

**And the cell has no runtime gate.** The `manner` variant is in the shipped code. A wrong spec takes
effect through this cell as reliably as a right one: `dna.edges()` computes a label over the wiring
graph, no code path refuses to run a toxic seat, and by the key mismatch recorded at SPECIFY.SPECIFY the
label does not even fire for the creature that names the variant. That defect and the thin SPECIFY.SEE
above it are the same hole seen from two sides.

### SPECIFY.CHANGE - the spec no failure rewrites

Rewrite a goal or a method in response to what happened when the last one ran. Distinct from CHANGE
inside SEE (rewriting a criterion) and from `critic`, which rewrites an ANSWER at repair.1 and never
touches the spec that produced it.

**Occupant: EMPTY. The most expensive empty cell in the row, and the live ledger prices it.**
`produce_brief` sits at DRAFT, streak 0, runs 40, fails 34. All 30 wakes report
`AWAKE:brief FAIL :: trust ledger : produce_brief -> level 1`. Forty runs, thirty-four failures, one
unchanged specification. Same shape at `reason_private_local`, DRAFT 0/42/35.

**Buys, if seated: nothing on the lever axis, everything on the loop.** A lever lowers a failure rate
once. This cell is what closes a specification loop, which is the difference between 34 failures and 34
inputs to a revision.

**What breaks without it, and the charter reading has to be split in two.** For the LAB, prompt text is
data, so rewriting a frame variant would not be `self_modify_code`, and no capability named
`modify_own_specification` exists: the operation is neither permitted nor forbidden, which is a state the
ladder has no level for. For the ENTITY, which is where the 34 failures are, the spec is Python.
Rewriting what `produce_brief` asks for means changing source, and that IS `self_modify_code`, which the
charter holds at FORBIDDEN with ceiling 1, reviewable diff only. The cell is closed twice over by two
different mechanisms, and only one of them is a naming gap. **Prediction:** the 34 failures recur until a
human edits the organ, because the only permitted output of a self-modification attempt is a diff that
waits for review. Second prediction, and the one to fund first: content-level reads at SPECIFY.SEE are a
precondition for this cell, since a rewrite with no read of the spec it replaces is a random walk with a
demotion attached.

---

**Row verdict.** One occupied cell holding two components the grid cannot separate. One cell holding a
single boolean that nothing consumes. Two cells marked WEAK, one because criterion and judgment collapse
into each other, one because the operation cannot be ablated and therefore cannot be measured. Two empty
cells, SPECIFY.PERSIST and SPECIFY.CHANGE, that name absent operations with concrete costs: an
unversioned streak, and a failure count that cannot reach the spec that produced it. The recursion earns
four of six coordinates in this row and is told to stop at the other two.

*(File paths in this row are repo-relative by the project's privacy guard.)*

---

## ROW: THE INTERIOR OF **SEE**

SEE is the class that judges whether what came back is right. Its interior splits into six operations and the split is uneven, but not along the line the first draft of this row drew. Two cells are fully occupied by the nine, one is occupied by half of a component, and three hold nothing the seat can reach. The finding is that the organism can produce a verdict on a run and has no operation that evaluates a verdict, carries one forward, or survives with one. The occupied cells cluster at the moment of the reply. Everything before the reply and everything after the process exit is either exogenous by design or absent.

CONVENTION FOR THIS ROW. Statements about code are read from `aea/lab/parts/base.py`, `parts/read.py`, `parts/repair.py`, `parts/judge.py`, `aea/lab/grader.py`, `aea/lab/rescore.py`, `aea/lab/stats.py` and `aea/kernel/trust.py`. Constants quoted from those files are source facts. The only figures stated as measured are the ones supplied to this document: the trust ledger state at 2026-07-27 and the x24 token-recall result. The lab's component receipts carry their own numbers in `organisms/catalogue.json`; they are referred to by direction here and not recited, because they are outside this document's sanctioned measurement set.

### SEE.SPECIFY - the criterion the reply is held to

**Operation.** Declare what counts as right, and in what vocabulary the verdict is issued, before any reply exists. Genuinely distinct from SPECIFY.SPECIFY: that one states the task, this one states the passing condition and names the failure modes. A task can be fully specified and still carry no criterion, which is the condition `measure` records as `verdict_is_empty`.

**Occupant, and only half of it. PARTIAL.** `measure` (gauge, judge.1, metric `can_know`) implements the comparison and owns the verdict vocabulary: `pass` when the answer equals truth, `abstain` when the answer is None, `fail` otherwise. It does not author the criterion. It indexes `ctx.task["truth"]`, so the standard arrives from the task bank, and in the x24 line of work from `grader.py`, which is handed no `Ctx`, no seat and no part output by construction. So the applying half of this cell is occupied by one of the nine and the authoring half is EMPTY of the nine and deliberately exogenous. Listing this cell as simply occupied overstates it, which is the correction this paragraph makes.

**Buys.** The gauge kind, exactly: no gauge, no legitimate promotion. A trust level means something only if the ok flag that fed it came from a criterion the component could not write. This is the cell that makes a streak a claim rather than a count of runs that did not crash.

**Breaks without it.** Criterion contamination, which this lab already committed in its terminal form. `grader.py` records it: `recoverable` was defined as the field `Readout.run` writes and `can_abstain` as the field `Validation` writes, so seating the component satisfied the metric by construction. Without the authoring half held outside the seat, every component passes its own test and the ladder in `trust.py` becomes a random walk with a ratchet. `measure` also records the weaker failure: a verdict issued when neither `goal` nor `frame` was seated is well formed and is about a question that was never posed.

### SEE.SEE - the second read of the same reply

**Operation, corrected.** The first draft of this cell bundled two operations that are not the same, and only one of them exists in code.

(a) OBSERVE AGAIN. Derive a value from the same reply by a route independent of the first read. The first read already happened: `call` claims `stated(ctx.text)`, the last integer in the reply, at the fire stage.

(b) ADJUDICATE. Compare two or more observations of one reply and issue a verdict on the earlier one. This is the operation that would make the cell a true second-order SEE, and it is the operation the cell was named for.

**Occupant of (a).** `readout` (lever, read.1). It reads the WORK rather than the MOUTH in three declared dialects: a solved variable, a labelled total, an enumeration index. The comment in `parts/read.py` is the cell's thesis in one line, WORK LABELS ONLY, because including `answer` and `result` made the readout recover the mouth's wrong answer and report it as recovered-from-work, which is the exact inversion of what the part exists for.

**Occupant of (b): EMPTY.** There is no adjudicator. `ctx.claim` raises when one key is claimed twice, which catches a coding bug, and says nothing when two different keys claim different values for the same reply. Four writers can now hold conflicting values in `ctx.reads` and the only thing that happens is that `READ_PRECEDENCE` silently picks one. A component reading `len({r["value"] for r in ctx.reads.values()}) > 1` and raising it as a signal is a few lines and does not exist. PREDICTION: it would fire on a large fraction of the mute-reply population, since that is precisely the population where the mouth and the work differ.

**`latency` at this coordinate: WEAK.** `latency` (channel, judge.2, metric `separability`) is a second observation of the same event through a non-textual signal, and the catalogue carries its separability receipt. It is not a second read of the reply and it is not an adjudication: nothing in the seat consumes it, and no read is revised because the two signals diverged. It was placed here by exclusion rather than by fit. Marking it WEAK is more useful than defending the placement, and the right conclusion is that `latency` is a channel whose home coordinate this row has not established.

**Buys.** Lever, in trust-grade terms: it shortens the path to promotion by lowering the failure rate on replies that were already right in the working. The catalogue records the ceiling as low, a recovery on a small minority of mute replies at no extra tokens, and the second battery scores it inert overall. Its own warning states that the condition it repairs is eliminated by a method frame, which makes it a lever whose value is contingent on a component in another class being absent.

**Breaks without it.** Without (a), the organism commits to the last integer in the reply. On a task whose working ends in an intermediate quantity, the mouth is unhedged and wrong and no mechanism records it, because `call`'s naive read is the only read and it is unopposed. Without (b), which is the current state, two reads can hold different values for one reply and the divergence is resolved by a config key rather than recorded as a signal.

### SEE.REMEMBER - the verdict carried to the next step - WEAK

**Operation as stated.** Carry a judgment forward inside a single run, so that step 5 is evaluated in the light of what was decided about step 3.

**Why this is weak and not merely empty.** In the modal SEE organism there is one call, one reply, one verdict, so the cell has no substrate. It becomes distinguishable from SEE.PERSIST only when the run has more than one step, and in the multi-step case the grading is applied per step from outside by `grader.py`, which is exogenous by construction and therefore cannot carry anything. The boundary between the verdict reaching the next step and the verdict outliving the run collapses for every object that actually exists. Forced analogy, marked WEAK rather than filled.

**The one thing actually at this coordinate.** A coded policy of discarding. `critic` sets `ctx.flags = list(seen["flags"])` rather than unioning, and the comment records why: unioning both calls' flags discarded most critic trials and removed exactly the messy first answers a critic exists for. That is a rule about verdict memory inside a run, written into a component whose home cell is elsewhere.

**What would occupy it, if anything.** PREDICTION: the analogue of the x24 result. Measured there, `checkpoint` got 43 of 48 sequences right while recalling 0 of 144 tokens, which is state reaching forward without being addressable. A verdict channel would show the same signature, a chain carrying its running value forward while carrying nothing about whether the earlier steps were graded right, so a chain that went wrong at step 4 is still graded as if step 5 were fresh. `stats.py` already establishes that those outcomes are not independent and handles the correlation at analysis time by resampling whole sequences. The running organism has no equivalent.

### SEE.PERSIST - the verdict that outlives the run

**Operation.** A judgment survives process exit and is available to the next one. Distinct from PERSIST.PERSIST, which is the entity's state surviving a boot in general. This is specifically the verdict surviving, so that the prior failure is a readable record rather than a lost one.

**Occupant, and it is not one of the nine.** `state/trust_ledger.json` via `aea/kernel/trust.py`: level, streak, runs, fails and a truncated history per capability, written under a file lock with quarantine-on-corrupt. Measured, 2026-07-27, after 17 days unattended, 109 ticks and 6 boots: `gather_public` TRUSTED, streak 39, 44 runs, 0 fails. `produce_brief` DRAFT, streak 0, 40 runs, 34 fails. `reason_private_local` DRAFT, 0 / 42 / 35. `speak` WATCHED, 2 / 2 / 0. Among the nine, this cell is EMPTY. `measure` writes a verdict onto a `Ctx` that is discarded at process exit. Persistence of lab verdicts is done by the run archive `rescore.py` reads, which is infrastructure and not a seated component.

**Buys.** It is what makes the gauge and the guard accumulate. Persistence does not make a verdict honest, which is the gauge's job, and it does not prevent a demotion, which is the guard's. It makes both survive the boot. Slow up, fast down is meaningless if the streak resets: without it, every restart would return each capability to charter defaults and the ceiling would be the only remaining constraint. `trust.py` names this as an already-fixed defect, a torn ledger that used to silently reset every capability and erase the accountability history the module exists for.

**Breaks without it, and what is broken with it.** What persists is a scalar. `e["history"] = e["history"][-20:]` caps the record at the last twenty entries while `produce_brief` has accumulated 34 fails, so the level survives and most of the reasons do not. The entity can state that `produce_brief` sits at level 1 and cannot state which 34 failures put it there. All 30 wakes emit the same line, `AWAKE:brief FAIL :: trust ledger : produce_brief -> level 1`, which is the persisted verdict repeating without accumulating diagnosis. PREDICTION: persisting a failure fingerprint alongside the counter, rather than a prose line in a twenty-slot ring, is the smallest change that converts this cell from a counter into evidence.

### SEE.ACT - the judgment reaching the answer slot

**Operation.** A read becomes a consequence. Inside SEE this means the verdict changes what the organism commits to, by withholding it or by replacing it. Distinct from ACT.ACT, which reaches outside the entity: this reaches only as far as the answer slot.

**Occupants.** `validation` (guard, read.2, metric `false_commitment_rate`) withholds. `critic` (lever, repair.1) replaces. Both are real and both carry receipts in the catalogue: the guard converting clean passes into forced abstentions on a rod that needs nothing, which is the job and not the failure, and the critic showing bounded upside with larger losses on high baselines at a cost multiple above one. This is the only cell in the row that is unambiguously occupied by two of the nine.

**The first seam.** On a mute reply where the working is right and the mouth is wrong, `call+readout` recovers the right answer and `call+readout+validation` returns nothing. Read through the recursion, that is SEE.ACT destroying SEE.SEE. `READ_PRECEDENCE` is `("critic", "validation", "readout", "call")` and `_winner` returns the first key present, so the guard's abstention outranks the lever's recovery. The lever read the work and produced a value, and the cell next door discarded it. Before the refactor the same outcome arrived by accident, four parts assigning one slot and the last writer winning; declaring the precedence reproduced that behaviour against the frozen trace and made it a variable instead of an accident. The interaction is not a defect in either component. It is two occupied cells of one interior wired in series with no adjudication between them, which is the same missing operation SEE.SEE records as empty.

**The second seam, read from the code and not yet measured.** `critic` outranks `validation` in the same precedence list, and `Critic.run` claims unconditionally once its call returns ok, including when its own parse yields None. So whenever the critic is seated the guard's abstention is unreachable, because the critic's read always wins. A critic that fails to parse produces `answer = None`, which `measure` scores as `abstain`, so a parse failure at the repair stage is indistinguishable in the verdict from a rule-driven abstention by the guard. PREDICTION: seat `call+validation+critic` on the rod family where the guard's forced abstentions were recorded and the abstention count attributable to the guard goes to zero without the guard being removed.

**Buys.** Guard: prevents demotion, which is worth a whole streak, since any failure demotes instantly. Lever: shortens the path to promotion. The two are in direct conflict here and the conflict is resolved by a config key rather than by anything that evaluates which one is right on this reply.

**Breaks without it.** Nothing stops a silently wrong answer from being committed and recorded as a clean run. That is the worst outcome the ledger can absorb: promotion needs N consecutive clean runs, so a wrong run scored clean is the one input that can raise a capability to a level it has not earned.

**The entity-scale occupant.** `trust.record` is the same operation one layer out: the verdict changes the level and `trust.check` gates the next act on it. It has a floor, read from the code: `if e["level"] > min(1, c["ceiling"])`, so a capability never drops below DRAFT unless its charter ceiling is 0. Derived, not measured: `produce_brief` has `promote_after` 7 in the charter and 40 runs against 34 fails, leaving six clean runs in total, so seven consecutive clean runs never occurred and re-promotion was never possible. One demotion therefore accounts for the current level and the remaining fails changed nothing. Consequence in this cell saturates and is not proportional to evidence.

### SEE.CHANGE - the reader rewriting its own rule

**Operation.** The judging faculty modifies its own structure: a dialect is added, a regex is narrowed, a precedence is reordered, a criterion is retired. Distinct from CHANGE.CHANGE, which is the entity altering its own source in general. This is specifically the instrument correcting the instrument.

**Occupant.** None of the nine. Empty, and empty twice over.

Empty in the lab: every change to the reading rule in this project was made by a human editing code. `parts/read.py` records three of them, the `_TOTAL` label set narrowed after the readout recovered the mouth's answer, the `_NUM` decimal rejection fixed after it rejected "the count is 4.", and the dead gate in `Readout.run` deleted after it was found unreachable given the stage order. `rescore.py` exists because instrument defects in the READ were repeatedly discovered after the calls were spent, and its rule is that a score set is appended and never overwritten, so a corrected reader can be applied to an immutable archive. That is the right shape for this cell and it is operated by a person from a command line.

Empty by charter: `self_modify_code` is FORBIDDEN with ceiling 1, reviewable diff only. Measured. So this cell is not an oversight to be filled. It is a policy, and the policy is that the entity may emit a proposed change to its own reading rule and may not apply one.

**Buys.** Attribution, which is what the channel kind buys in this document's vocabulary: it converts a run of failures into an attributable cause. Flagged, because the catalogue defines channel more narrowly as making a state legible in a non-textual signal, scored on separability, and a self-correcting reader is not that. The claim here is the looser one and should be read as such rather than as a kind assignment.

**Breaks without it.** A measurement defect persists until a human notices. `produce_brief` sits at DRAFT with 34 fails and 30 identical wake lines, nothing in the system distinguishes a bad brief from a bad check on the brief, and nothing in the system is allowed to change the check. `rescore.py` states the cost plainly: the diff between two score sets over one archive is the size of the measurement bug, and that is a number the lab had never been able to see.

---

## ROW SUMMARY

Fully occupied by the nine: SEE.ACT (`validation`, `critic`).

Half occupied: SEE.SPECIFY, where `measure` applies a criterion it does not author, and SEE.SEE, where `readout` observes again and no component adjudicates.

Empty of the nine: SEE.REMEMBER, SEE.PERSIST, SEE.CHANGE. SEE.PERSIST and the consequence half of SEE.ACT are occupied one layer out by the trust ledger, which is the strongest support in this row for the recursion being real rather than decorative: the same operation appears at organism scale and at entity scale with different implementations and different failure modes.

Marked WEAK: SEE.REMEMBER, which has no substrate in a single-step run and collapses into SEE.PERSIST in a multi-step one, and the placement of `latency` in SEE.SEE, which was conceded as a misfit in the first draft and is now labelled as one.

The row's sharpest result is not a component. SEE.SEE and SEE.ACT are wired in series and cancel each other on the mute reply, and the code shows a second case where a seated critic makes the guard unreachable. Both collisions have the same cause, which the grid names as a coordinate rather than a bug: the adjudicating half of SEE.SEE is empty, so the only arbitration between two occupied cells of one interior is a precedence tuple in a config file.

---

## ROW: THE SIX OPERATIONS INSIDE **REMEMBER**

REMEMBER holds one component of the nine: `carry` (catalogued THE CHECKPOINT, C-80, lever, stage `carry.1`, metric `accuracy_over_sequence`, four forms `none / checkpoint / conversation / free`). Three of the six interior cells are empty. That is the row's main result.

**Two corrections to the supplied numbers before the cells, because the honesty law outranks the brief.**

First, "checkpoint got 43 of 48 sequences RIGHT while recalling 0 of 144 tokens" merges two rods, and x24 forbids that (`fix_11_never_pooled`: four providers, a pooled rate is a Simpson's-paradox generator). 43/48 is `gpt-oss-20b` at 240 probes; 0/144 is `granite4.1:3b`. No cell holds both.

Second, the dissociation is stronger than the merged version and it does not need two hand-picked rods. Read off `state/lab/runs/x24_the_store_and_the_door/20260727T123912Z.json`, per rod, all six, with the per-cell call reliability beside it, because several cells failed at the transport and a zero from a starved container is not a finding:

| rod | L | container | ok_rate | sequences | token retrieval |
|---|---|---|---|---|---|
| gpt-oss-20b | 16 | none / checkpoint / conversation / free | 0.979 / 1.000 / 1.000 / 1.000 | 0 / 43 / 48 / 44 of 48 | 0/235 / 0/240 / 240/240 / 32/240 |
| granite4.1:3b | 3 | none / checkpoint / conversation / free | 1.000 / 1.000 / 1.000 / 1.000 | 0 / 8 / 42 / 27 of 48 | 0/144 / 0/144 / 144/144 / 7/144 |
| nano-30b-a3b | 3 | none / checkpoint / conversation / free | 1.000 / 1.000 / 0.812 / 0.958 | 0 / 32 / 35 / 16 of 48 | 0/144 / 0/144 / 101/129 / 18/140 |
| omni-30b-reasoning | 7 | none / checkpoint / conversation / free | 0.958 / 1.000 / 0.188 / 0.521 | 0 / 47 / 9 / 24 of 48 | 0/187 / 0/192 / 93/106 / 33/148 |
| super-120b-a12b | 3 | none / checkpoint / conversation / free | 1.000 / 0.354 / 0.000 / 0.000 | 0 / 11 / 0 / 0 of 48 | 0/144 / 0/56 / 0/0 / 0/0 |
| laguna-xs-2.1 | 16 | none / checkpoint / conversation / free | 0.292 / 0.292 / 0.062 / 0.021 | 0 / 3 / 0 / 1 of 48 | 0/127 / 0/153 / 45/63 / 2/18 |

What survives every objection about rod choice and every objection about pooling is one column: **checkpoint token retrieval is 0 on all six rods, per rod, 0/144, 0/240, 0/56, 0/144, 0/153, 0/192**, including `omni` where checkpoint takes 47 of 48 sequences and `gpt-oss-20b` where it takes 43 of 48 with Wilson [0.778, 0.955]. What does NOT generalise is the sequence comparison: on `omni` checkpoint 47/48 beats conversation 9/48, on `laguna` checkpoint 3/48 beats conversation 0/48, and both of those conversation cells are starved (ok_rate 0.188 and 0.062), so they are unusable rather than evidence either way. `super-120b` conversation and free are void, 48 of 48 calls failed, which is the same starved-container defect x24 was built to correct in x21 and it is not fully corrected.

Everything below distinguishes **carrying forward** (state at step n is present at step n+1) from **reaching back** (an item at step k is produced on demand at step n). The measurement says a form can have one and none of the other.

---

### REMEMBER.SPECIFY - the state schema, declared once and never varied

**The operation.** Say what the store shall contain and in what shape, before anything is put in it. Different from SPECIFY.SPECIFY, whose object is the task objective: here the object is a wire format for state, and the reader is a regex rather than a model.

**Occupant.** `carry`, partially. Real code: `INSTRUCTION` in `aea/lab/parts/carry.py` and `variants[form].instruction` in the catalogue. `checkpoint` mandates exactly `STATE: value=<n>, step=<n>` and `_STATE` is the regex that reads it. `free` declares no schema, its instruction text being to write anything worth passing to the next step. `conversation` and `none` declare nothing, both instruction strings being empty, because their stores are structural rather than textual.

**What it buys.** Nearer enabling than lever, despite `carry` being catalogued a lever. A declared schema is what makes the store machine-readable rather than model-readable only. Without it `Carry.extract` falls back to "last integer in the text", and two files record what that cost: `carry.py` says the fallback "made every checkpoint trial miss at step 1 during calibration", and `chain.py` lines 93 to 94 say the same regression "scored three whole rods at 0.00 solo in x23b and read as the task is too hard for this fleet". Note the repo disagrees with itself on the count: `aea/lab/tests/test_golden.py` says five rods. Either way the failure is a read error scored as a capability failure. In trust terms, and this follows from the mechanism in `aea/kernel/trust.py` rather than from analogy: `record(cap, ok=False)` zeroes the streak and demotes one level, never below DRAFT unless the charter ceiling is 0. So a capability metered on `accuracy_over_sequence` with an unreliable schema does not oscillate around its old level, it sits at DRAFT, which is exactly where `produce_brief` sits at 40 runs and 34 fails.

**What breaks without it.** Rods written up as incapable of a task they could do. That is a false demotion produced by the store's own format, and it also zeroes a streak that takes 3 to 7 clean runs to rebuild depending on the capability (`speak` 3, `gather_public` and `reason_private_local` 5, `produce_brief` 7, and 99 for the five human-gated ones, which is to say never by streak).

**The unmeasured part, and it is this cell exactly.** x24 states its own scope limit at `fix_09`: "the container's OWN instruction text is not paraphrased, so every container result is conditional on that one wording". Task framing is paraphrased three ways; the schema declaration is n=1. So this cell is occupied in code and its effect size is unknown. Prediction, unmeasured: varying only the schema wording moves the checkpoint numbers by a regime rather than an increment, on the grounds that one wording change already flipped whole rods from 0.00.

---

### REMEMBER.SEE - nothing grades the state at the handoff

**The operation.** Judge whether what is about to be carried is intact, before the next step consumes it. Different from SEE.SEE, which grades an answer against a task: this grades a state against its own continuity, and it must run between steps, where no answer exists yet.

**Occupant.** EMPTY. `Carry.extract` parses and `Carry.pack` formats; neither judges. There is no continuity check (does `value_n` differ from `value_{n-1}` by the step's operand), no plausibility bound, no refusal path. The two components of the nine that could be mistaken for occupants are `validation` (guard, read.2, `false_commitment_rate`) and `measure` (gauge, judge.1, `can_know`), and both are excluded for the same reason: they read an answer, not a state at a handoff. Neither was seated in x24, whose seat is `call, goal, frame, readout` plus the carry form. The only judge in the loop is `truth_fn`, an oracle held by the experiment, absent from the live entity.

**What it buys if built.** Channel first, then guard. Channel: `accuracy_over_sequence` currently cannot attribute a failed sequence between "carried a wrong value faithfully" and "carried the right value and computed wrong". x24 prices the stakes at line 29, "miss step 4 and 5..16 are wrong by construction", so at length 16 one corrupted handoff prices as twelve failures. Guard: converting a corrupt carry into a visible abstention is what stops one bad handoff from consuming a whole streak. Gauge only in the derived sense that the metric stops mixing two failure sources. Against `promote_after` of 3 to 7, slow up and fast down, this is the most expensive missing cell in the row.

**What breaks without it.** A note that asserts something false is carried forward with the same authority as a correct one, because nothing between steps reads it. The catalogue classes `free` toxic on x21's receipt, "-0.167 at four steps, -0.636 at sixteen. It injects noise, it does not merely lose information", and degradation that scales with length is the signature of an uncaught error compounding rather than of information being lost.

**Caveat against my own reading.** x24 does not reproduce a `free` collapse on `gpt-oss-20b` (44/48 sequences against checkpoint's 43/48), and on `granite` free beats checkpoint outright (27/48 against 8/48) while on `omni` it loses badly (24/48 against 47/48). The toxic label rests on x21, whose control was void for `none` and whose conversation arm the experiment records as never sent. The cell is empty either way; the size of what it would catch is unsettled.

---

### REMEMBER.REMEMBER - the hop, state present at the next step

**The operation.** State produced at step n is in front of the model at step n+1. The narrowest possible reading of the outer class, deliberately: it excludes schema, grading, reach-back and restructuring, which are the other five cells.

**Diagonal risk, named.** Every X.X cell is at risk of restating its outer class. What rescues this one is a measurement rather than an argument: `checkpoint` scores 43/48 and 47/48 on the hop on two rods while returning 0 tokens on all six. Carrying forward is measurably not the whole of REMEMBER, so naming the hop separately partitions rather than repeats.

**Occupant.** `carry`, in three of its four forms. `checkpoint` packs "The running value is X." `conversation` appends the exchange to `history`. `free` packs the value plus a model-written note. `none` is not an occupant, it is the constructed absence of the hop: it packs the empty string, and the comment in `carry.py` explains why that is load-bearing, "a control that hands the running value forward IS a checkpoint, and that is the bug this method exists to prevent."

**What it buys.** Catalogued as lever on `accuracy_over_sequence`, on x06b's receipt of 11/11 against 9/16, p=0.0216, at one task and one chain length, with the entry flagged UNMEASURED as of 2026-07-27 because x21's control contained the treatment.

**The kind cannot be settled by the `none` arm.** `none` scores 0/48 on every rod, which looks like enabling. It is not evidence of that: under `none` the rod is handed "Step 5: add 209" with no running value and no history, so an all-correct sequence at length 3 or more is close to arithmetically unavailable, and the zero is the design's null rather than a capability finding. Note that the weaker gloss "it can only ever be right at step 1" is false and I am not going to use it: per-step accuracy under `none` measures 0.484, 0.533 and 0.527 on the three length-3 rods, well above the 0.333 that gloss implies. The informative comparison is checkpoint against conversation against free, all of which make the hop and differ in what else they do.

**What breaks without it.** Nothing sequential runs. Not degraded: 0/48 on six of six rods.

---

### REMEMBER.PERSIST - the store does not survive a restart

**The operation.** Carried state survives the death of the process holding it, so a sequence can resume rather than restart. Different from PERSIST.PERSIST, whose object is the entity's own continuity across boots, and different from the hop, which is state crossing a step boundary inside one live process.

**Not marked weak, and this reverses my first reading of it.** The temptation is to say a restart cannot occur inside a single sequence and therefore the sub-class has no defining event here. That smuggles in a scope, "inside a single sequence", that the class definition never imposed, and the reading it blocks is direct rather than analogical. The entity already runs a working exemplar of exactly this operation in a different class: `grid.atomic_save_json` and the sacred `state/journey_save.json`. So the cell is well defined, it is EMPTY, and it names a specification.

**Occupant.** None of the nine. Nothing in `carry.py` touches `grid.STATE`. `chain.py` ends `Chain.run` with `self.history, self.carried = history, carried`, an attribute on a live Python object, which outlives the loop only long enough for `Chain.ask()` to fork probes off it, and that attribute is the entire reason ARM B of x24 exists. The persisted trace records `carried_chars`, a count, not the carried text. The store dies with the process.

**The one near neighbour, and it belongs in the next cell.** x23's `inherited` capacity, sealed in the catalogue as "a value crossed from one organism to another and the receiver continued from it", is state surviving the organism that made it. It reads as reach-back with a different addressee, so it lands in REMEMBER.ACT.

**What it buys if built.** Enabling for any sequence longer than a process lifetime, and a guard on the streak: a boot mid-chain currently registers as a failed sequence, which under `record(cap, ok=False)` is indistinguishable at the ledger from a capability failure and demotes on infrastructure noise.

**What breaks without it, stated as prediction.** The live entity shows 6 boots in 17 days across 109 ticks. Any chain interrupted mid-sequence restarts at step one. Whether that is implicated in `produce_brief` at 34 fails of 40 is UNMEASURED and I will not imply it: no carry component is seated in the live loop at all. The nine live in the lab.

---

### REMEMBER.ACT - reaching into the store and pulling one item out

**The operation.** Address an item by position and emit it, on demand, at a time not adjacent to when it was stored. Different from ACT.ACT, whose object is the world outside the process. Here the effect crosses the store's own boundary: an addressed item leaves the store and enters the running computation. The store is the actor, not the object.

**Occupant.** `carry`, the `conversation` form only. Each probed step carries a random token of the form `XX-0000` generated fresh at run time, so reproducing it is retrieval and can be nothing else (`fix_07_nonrecomputable`). Value probes run beside it because a value can always be recomputed.

**The result, at depth, because the depth structure is the finding.** On `gpt-oss-20b`, length 16, probes at depths 1, 4, 8, 12, 16, 48 sequences each:

| container | token retrieval by depth | own-value by depth | totals |
|---|---|---|---|
| conversation | 48 / 48 / 48 / 48 / 48 | 48 / 48 / 48 / 48 / 48 | token 240/240, own 240/240 |
| checkpoint | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 47 | token 0/240, own 47/240 |
| free | 0 / 0 / 1 / 10 / 21 | 0 / 0 / 0 / 0 / 42 | token 32/240, own 42/240 |

The structure replicates on `granite4.1:3b` at length 3: checkpoint own is 0, 0, 12 at depths 1, 2, 3, conversation token is 48, 48, 48, free token is 0, 3, 4.

Read it column by column. `checkpoint` is not a store with a poor retrieval rate. Every own-value hit it scores is at the final depth, which is the number sitting verbatim in "The running value is X." At every earlier depth it is 0 of 48. That is a store which is exactly one item deep and cannot be addressed at all. `free` shows a recency gradient, 0 at depth 1 rising to 21 at depth 16, which fits a note rewritten each step that loses distant content, not an arbitrary per-item choice. `conversation` is flat at 48 across every depth including depth 1, which is what makes this a dissociation rather than a difference of degree.

**What it buys.** Enabling, for any operation whose input is an earlier item rather than the last one: citation, correction of a specific prior step, auditing a chain, answering "what was at step 4". Those do not degrade without this cell, they are unavailable. In trust terms, and stated narrowly because the mechanism does not stretch further: `accuracy_over_sequence` can still promote on a checkpoint store, since `record(cap, ok)` writes the streak to the ledger in `state`, not to the model's context. What cannot promote is any capability whose ok flag depends on the run producing evidence about its own earlier steps, because on a checkpoint store the run cannot produce it and the flag can only be set by an external oracle. I am not extending this to `self_modify_code`: it sits at level 0 with ceiling 1 and `promote_after` 99, gated by a human authorisation ceiling, and no carry component is seated in the live loop.

**What breaks without it.** The store becomes strictly one-directional and only the most recent item is queryable. On the numbers above that costs nothing on the sequence score (43 against 48) and everything on accountability (0 against 240 tokens, and 0 at every earlier depth).

**Price, stated as scope-limited.** `conversation` wins the retrieval number on every rod where the cell produced probes at all, and its cost is INPUT tokens growing with the sequence (context_max 5738 against checkpoint's 27 on `gpt-oss-20b`). x24 refuses to generalise this: "NOT A LONG-CONTEXT RESULT. A dozen short steps is a few thousand tokens." That the price becomes a problem is a prediction, not a measurement. Note also that conversation is the container that failed hardest at the transport, ok_rate 0.000, 0.062 and 0.188 on three rods, which is a reliability cost the sequence scores hide.

---

### REMEMBER.CHANGE - the store cannot restructure itself

**The operation.** The store alters its own shape while running: compacting, evicting, summarising, promoting an item to a more durable tier, or switching form mid-sequence. Different from CHANGE.CHANGE, which alters the entity's code: here the object is the container's structure and the trigger is the store's own size or age.

**Occupant.** EMPTY, no partial credit. `form` is read once at construction, `ctx.cfg("carry", "form", "checkpoint")`, and never read again. `Carry.pack` truncates the free note at 1200 characters and `chain.py` truncates stored assistant text at 2000, which is a fixed clamp, not eviction: nothing selects what to keep. `free` is the nearest neighbour and is not this cell. Note contents are model-generated under a fixed schema; the schema, the tier and the container do not move.

**What it buys if built.** Lever on cost rather than on accuracy, which no metric in the catalogue currently expresses. It is the only way to hold conversation's 240/240 retrieval while paying less than the full history, and the only mechanism by which a sequence can outlast its budget.

**What breaks without it.** The two working containers sit at fixed opposite corners and nothing moves between them. `checkpoint` is one item deep and unaddressable, 0/240 tokens and 0 own-value at every depth but the last. `conversation` is fully addressable and priced at the whole history. There is no intermediate and no way to construct one at run time, so the choice is made once, before the run, by a human editing a config. Prediction, labelled as one: at the length where conversation stops being affordable, the system has no fallback retaining reach-back, and it degrades to checkpoint, which measures zero on the capability that mattered.

---

## SHOULD REMEMBER BE TWO CLASSES

One recommendation and its trade-off.

**No. Keep it one class.** The dissociation is real, it is the cleanest result in the lab, and it replicates across rods in the direction that matters: checkpoint holds sequences where the rod is capable (43/48, 47/48, 32/48) and returns 0 tokens on six of six rods. A single component whose forms separate two capabilities that cleanly is the textbook case for a split. But the split already has two addresses in the grid, REMEMBER.REMEMBER and REMEMBER.ACT. Promoting it to a class boundary would break the six-fold symmetry to encode one dissociation and would buy no address that does not already exist.

**What that costs, named.** The row is 2 occupied, 1 partially occupied, 3 empty, and the one occupant is a single component wearing four hats. A reader can fairly say REMEMBER is thin for a top-level class. The thinness is the measurement: state between steps is where this system is least built, and a row that admits it is worth more than a row that inflates.

**Where the recursion earns its keep.** The interior of REMEMBER named a split before the split was reported as one, and it named it at the right resolution. x24 filed retrieval against recomputation. Through the grid it reads as one cell occupied and the adjacent one empty: the hop is seated, the reach-back is not, and the depth data says the checkpoint store is exactly one item deep rather than merely unreliable. The number was in the ledger without a name. That is one confirmed prediction, on one row, from one experiment. It is not six confirmations and it is not a general result.

**Where the recursion is at risk.** REMEMBER.PERSIST is empty and its specification is clear, so the recursion holds there. The place to watch is the reverse cell, PERSIST.REMEMBER. If that one can only be filled by describing carried state surviving a boot, the two classes are touching and the grid has a boundary defect rather than a recursion. That is a test for the PERSIST row, not a claim from this one.

---

## Row: inside PERSIST

PERSIST holds **zero of the nine components**. The test applied: no component's metric is evaluated across a process boundary. `carry.1` comes closest, and its metric is `accuracy_over_sequence` inside one chain; every other component is scored inside a single fire-to-judge pass. So this entire row is a specification rather than an inventory.

What occupies it instead is **kernel infrastructure**, and that distinction is load-bearing. Infrastructure is code that runs underneath every part without being a part: it is never seated, never scored, never promoted, and it has no metric. `state/heartbeat.json` (6 boots, 109 ticks; its `alive_since` field reads 2026-07-10, consistent with 17 days unattended) and `state/trust_ledger.json` (gather_public at TRUSTED, streak 39, 44 runs, 0 fails) are the evidence that something in this row already works. The row's job is to say which cells that infrastructure actually fills, and which cells are empty in a way that has already cost something measurable.

Three primitives do all the current work, all in `aea/kernel/grid.py`: `atomic_save_json` (line 64, temp file plus `os.replace`), `load_json` (line 73, quarantine on unparseable), `file_lock` (line 94, msvcrt advisory lock that degrades to unlocked on a 5s timeout rather than deadlocking).

**The distinctness rule this row applies, stated before the cells so it cannot be applied selectively.** A cell is only real if it has a *failure mode* that the same sub-class inside another outer class cannot produce. Pointing the same operation at a different object is not enough, and neither is running the same operation over a different interval. Both are substitutions, both are free, and a grid that accepts either can never be falsified. Each cell below carries an explicit verdict against that rule. One cell fails it and is marked WEAK; one passes it only on a contested argument and is marked CONTESTED.

---

### PERSIST.SPECIFY - the durability contract

**The operation.** Declare, before anything is written, which records must outlive the process, what shape a valid restored record has, and how long each is retained.

**Distinctness verdict: passes.** Not because the object differs (that alone would be substitution) but because this is the only SPECIFY cell in the grid whose declaration includes a *lifetime*. SEE.SPECIFY declares what counts as a right answer, and that declaration has no clock in it. A durability contract can fail in a way no other SPECIFY cell can: the contract is satisfied at write time and violated at read time, by retention, with no code change in between. That is a failure mode the sub-class does not have elsewhere.

**Occupant.** None of the nine. Infrastructure fills it partially and in the worst possible arrangement: the contract exists once per call site and nowhere as a declaration. `aea/loop/live.py:48` carries the heartbeat's default shape as a literal inside the loader. `trust.CHARTER` carries each capability's starting level, ceiling and `promote_after` as a Python dict, and `trust._entry()` (line 59) materialises a default entry from it on any read where the key is missing. No runtime state file carries a version or schema field: `heartbeat.json`, `trust_ledger.json` and `journey_save.json` were each read and none has such a key. `aea/lab/organisms/catalogue.json` does declare `"schema": "aea.organism.catalogue/1"`, which shows the project already knows how to do this. It has done it for lab data and not for the state that survives boots.

**What it buys.** Not enabling, and the row's own evidence forbids that claim: 109 ticks and 6 boots have run without a declared contract, so its absence is plainly not the difference between FORBIDDEN and anything at all. What it buys is upstream of a kind rather than a kind of its own. It is the precondition for the gauge one cell over. A gauge needs something to measure against; an integrity check with no declared shape can only check syntax, which is exactly the state PERSIST.SEE is in. In trust-grade terms: without this cell, no promotion computed after a restart has an auditable evidence chain, because the outcome variable of the whole system is stored in an undeclared format.

**What breaks without it.** A restored default is indistinguishable from a restored record. `trust._entry()` re-creates a missing capability at charter level with streak 0 and an empty history, and returns it as a normal entry. `gather_public` at TRUSTED with a 39-run streak, and a `gather_public` key silently lost from the file, both come back as valid dicts that `check()` reads without complaint. This is not hypothetical: the comment on `trust._load()` records it as an already-paid cost, "a torn ledger used to silently reset every capability to charter defaults - erasing the accountability history this module exists for."

---

### PERSIST.SEE - the integrity check on what came back from disk

**The operation.** Judge whether the state read at boot is the state that was written before the process ended. Two failure classes need different machinery. Syntactic corruption (the bytes do not parse) is cheap to detect. Semantic corruption (it parses, and the contents are stale, partial, or written by a different version of the code) is the expensive one and the one that matters.

**Distinctness verdict: passes.** Semantic staleness is a failure mode SEE proper cannot produce. SEE proper judges an answer produced moments ago by a component in the same chain; there is no interval across which the object of judgment can have been replaced, truncated or written by different code. Here the interval is the whole point and it generates a failure the sub-class has nowhere else: an object that is well-formed, plausible, and not the one that was left.

**Occupant.** None of the nine. Infrastructure fills exactly the cheap half. `grid.load_json` quarantines an unparseable file to `<name>.corrupt.<epoch>` and returns the default rather than letting the next save cement the loss. It has fired at least once in real operation: `state/bench_runs.json.corrupt.1784898655` is on disk. There is no semantic check of any kind, and the syntactic one is not universal. Three read sites bypass it with a bare `json.load(open(...))` and therefore get no quarantine and no default discipline: `aea/organs/autonomy.py:37`, `aea/loop/aea.py:78`, `aea/mind/pathfinder.py:25`.

**What it buys.** Gauge, and it is the only gauge in this row. Its whole job is to make a restored `ok` legitimate. It decides whether "6 boots, 109 ticks" is a measurement or a number that has merely never been contradicted; those are different statuses and only a gauge separates them. No gauge, no legitimate promotion: a promotion computed on an unverified restore has a hole in its evidence chain exactly at the restart.

**What breaks without it.** A boot on silently wrong state runs an entire wake against the wrong ledger and stamps that wake's outcomes into it. `trust.record()` demotes on any failure, unconditionally, and resets the streak to 0, so a single bad restore can erase gather_public's 39-run clean streak, and the resulting history line is indistinguishable from a genuine fetch failure. Note what that streak is: `promote_after` for gather_public is 5 and its ceiling is 3, which it has reached, so the promotion branch no longer fires and the streak is pure accumulated evidence. It is the longest evidence chain in the ledger and it is the thing most exposed by a missing restore check. Prediction: the first hard evidence of this cell's absence will present as an unexplained demotion of gather_public, with nothing in the file that attributes it to the restore rather than to the fetch.

---

### PERSIST.REMEMBER - the live copy between two writes

**WEAK. Marked down rather than dressed up.**

**The operation as best it can be stated.** Hold the durable record in a process variable across the steps of one wake, so that writing to disk is a flush of an authoritative in-memory copy rather than the medium of every update.

**Distinctness verdict: fails the rule.** It is the same operation as REMEMBER proper, carrying state between steps, pointed at a different object. Object substitution is the cheapest way to make a recursion look real; accepting it here forces accepting it everywhere, at which point the grid stops being falsifiable. There is one candidate rescue and it does not hold: the failure mode here (two processes each holding a stale copy) is genuinely unavailable to REMEMBER proper, which runs single-process inside a chain. But that difference comes from how this system happens to be deployed, not from the sub-class, and a rule that lets deployment accidents certify cells is not a rule. The honest reading stands: PERSIST.REMEMBER and REMEMBER.REMEMBER may be one cell counted twice.

**Occupant.** None of the nine. Infrastructure: `aea/loop/live.py` loads the heartbeat once at boot (line 48), mutates it across the whole wake (`total_ticks`, `history`), and writes per tick. That is a real read-modify-write cycle held in memory, which is why the cell is not empty even though it is not distinct.

**What it buys, if it is real.** Lever. Fewer writes, fewer chances to tear a record, so a lower failure rate on the path to promotion.

**What breaks without it.** Last writer wins; two processes each holding a stale copy overwrite each other's ticks. The codebase already knows this: `live.py:146` carries a single-instance guard whose comment names the incident, "two lives racing the same heartbeat/brief was silent double-work." That guard is a process-level workaround for a missing record-level merge. Prediction: `total_ticks` is a floor rather than a count, and no field in the file distinguishes a lost tick from a tick that never happened.

---

### PERSIST.PERSIST - the write that cannot be half-done

**CONTESTED. It is the diagonal, and a self-similar grid can always make a diagonal sound profound by restating the outer class.**

**The operation.** Make the transition from the old record to the new one atomic and ordered, so that an interruption at any instant leaves one of exactly two valid states and never a third.

**Distinctness verdict: passes, but only on one argument, and the obvious argument is rejected first.** "Different interval, different mechanism" is not sufficient. Interval substitution is the same free move as the object substitution rejected at PERSIST.REMEMBER three cells up, and if it is allowed here it has to be allowed there, which would un-mark that cell. The argument that does hold is the failure class. Outer PERSIST fails by *absence or staleness*: the record is gone, or old, and it always parses. PERSIST.PERSIST fails by *tearing*: the record is a fragment that belongs to neither the before nor the after state, and it is not a valid instance of anything. Nothing else in the row can produce a torn object, and detecting a torn object needs different code from detecting a missing one. That is a real difference, and it is the only one carrying this cell.

**Occupant.** None of the nine. This is the one cell in the row that infrastructure genuinely closes. `grid.atomic_save_json` writes to `path + ".tmp"` and calls `os.replace`, so an interruption mid-write cannot truncate the live file. `grid.file_lock` serialises read-modify-write across processes, and `trust.record()` holds it around the whole load-mutate-save sequence specifically so a concurrent run can never lose a demotion.

**What it buys.** Enabling, in the strict sense the kind vocabulary means: the difference between FORBIDDEN and anything at all. The chain is direct. Promotion is computed from a counter stored in the ledger; if the ledger can be half-written it is not a ledger; if it is not a ledger no capability can hold a defensible grade above FORBIDDEN. Every other cell in this row is meaningless if a write can truncate.

**What breaks without it, and what is still broken.** The guarantee is per call site rather than per system, and two live sites still bypass it with a truncating `json.dump(s, open(path, "w"))`: `aea/loop/aea.py:83` and `aea/mind/pathfinder.py:26`. An interruption during either write leaves a truncated file, which then meets the incomplete PERSIST.SEE above and is quarantined into a default. Second open edge: `file_lock` yields False on a 5s timeout and proceeds unlocked, deliberately, so the system degrades rather than deadlocks. That trade means the serialisation silently downgrades under contention rather than failing loudly. It is the right default and it is unmeasured; nothing counts how often the timeout path is taken.

---

### PERSIST.ACT - the reach back into the store

**The operation.** Address a stored record by query and pull a specific part of it into a running step, so that a prior run conditions the next one rather than only sitting on disk.

**Distinctness verdict: passes.** The failure mode is unique to this cell: a fact is present in the store, and is unreachable because no field anticipated the question, and the retention window destroys it before the question is asked. ACT proper fails by an external effect not landing. REMEMBER.ACT, in-chain, has no retention dimension at all. Only here can a retrieval fail against data that demonstrably exists.

**Occupant.** Empty, and this is the most useful empty cell in the row. State the emptiness precisely, because the loose version is wrong: readout exists. `trust.board()` prints level, streak, runs, fails and ceiling for all 9 charter capabilities, and `live.py --status` prints the heartbeat summary plus the last 6 history lines. What does not exist is *addressable* retrieval. Both of those are fixed reports whose questions were chosen at code-write time; every consumer otherwise calls `load_json` on a named file and receives the whole dict. Nothing can select on a predicate: which capability failed most recently, what the last successful brief contained, when a streak began. The machinery for this exists in the repo and points elsewhere: `aea/memory/consolidate.py` holds `embed`, `_cos` and `recall(query, k)` over a store at `state/luis_memory.json`, which indexes the ingested corpus rather than the entity's operating state. The retrieval capability is built. It has never been aimed at the record of the system's own runs.

**What it buys.** Channel first: a query interface is what makes a failure attributable rather than merely visible. The ledger already makes produce_brief's failure visible (40 runs, 34 fails, DRAFT, streak 0). Nothing makes it attributable, because attribution needs a question asked against history rather than a counter read off the top. Lever second: a step that can condition on the prior outcome fails less often, which shortens the path to promotion. In trust-grade terms this cell is the difference between a capability that is stuck and a capability whose stuckness has a locatable cause.

**The x24 evidence, and what it licenses.** In x24, checkpoint recalled 0 of 144 tokens while getting 43 of 48 sequences right. Read through the recursion, that is a component with REMEMBER-inside-REMEMBER (state reaches the next step) and without ACT-inside-REMEMBER (the store cannot be addressed and reached back into). PERSIST currently shows the same signature one class over: state arrives across a boot, and no predicate can be run against it. **Prediction, labelled as prediction and not carried by the x24 number:** PERSIST will fail the way carry=checkpoint failed, for the same structural reason rather than a coincidental one. What x24 measured is one class; the claim that the shape repeats here is exactly the hypothesis under test, and this row is not evidence for it.

**What breaks without it.** No fact about a prior run can be retrieved unless a field anticipated the question at write time, and the retention policy destroys the record before anyone asks. produce_brief's history array holds the last 20 entries (`trust.record()` slices `[-20:]`) and the heartbeat holds the last 30 (`live.py:122` slices `[-30:]`). All 30 surviving wake lines read `AWAKE:brief FAIL :: trust ledger : produce_brief -> level 1`. The first failure, the one that would show what changed, is gone. The highest-value query this system could run against its own record, when produce_brief started failing and what was different at that boot, returns nothing, and the reason is that this cell is empty.

---

### PERSIST.CHANGE - the revision of the store's own shape

**The operation.** Change what is stored and how it is stored, without losing what is already stored. Migration, versioning, declared compaction.

**Distinctness verdict: passes.** It carries a constraint the outer class does not, and the constraint generates its own failure mode. CHANGE proper may break the future: a modified structure produces worse runs from now on, and the damage is bounded by how fast it is detected. CHANGE inside PERSIST may break the past: a bad migration invalidates records already written, and no amount of subsequent detection recovers them. Irreversibility with respect to already-collected evidence exists in no other CHANGE cell.

**Occupant.** Empty, and not merely component-empty. Infrastructure-empty. No runtime state file carries a version. What sits in this cell's place is unversioned truncation applied by hardcoded constants: the `[-20:]` and `[-30:]` slices above, and `aea/kernel/pulse.py` rotating `events.jsonl` at `MAX_BYTES = 1_000_000` while keeping `KEEP_TAIL = 1200` lines. That is a retention policy nobody declared and nothing can revise except by editing source, which is precisely the point. The store's shape changes only by human code edit, so the capability does not exist in the running system at all.

**What it buys.** Enabling, with a channel component, and not guard. Enabling because the capability is currently absent rather than degraded: without migration the store's format cannot change at all under the system's own operation. Channel because a version field is what makes a post-migration failure attributable; without one, a format mismatch presents as a behaviour change with no marker to point at. The guard belongs to the *governance* of this cell rather than to the cell itself, and it does not exist either. A store that rewrites its own format is a self-modification with the same risk profile as `self_modify_code`, which the charter pins at level 0 with ceiling 1, reviewable diff only. The trust mechanism has the right model for governing this and nothing to point it at. Note the asymmetry that makes a guard necessary before this is ever built: the demotion rule recovers from one false commit at the cost of a streak, and it cannot recover from a migration that destroyed the history the streak was recorded in.

**What breaks without it.** The ledger cannot be extended. `trust._entry()` creates a whole missing capability from CHARTER and never a missing field inside an existing entry (line 59: the check is `if cap not in state`), so adding any field to a trust entry leaves all 9 charter capabilities carrying the old shape. Prediction: the first field added to `trust_ledger.json` produces either a `KeyError` at the read site or a silent default that reads as a real value, and the entry that breaks worst is the one with the most to lose, gather_public at 44 runs, because it has the longest history to be wrong about. Second prediction: with no version field the failure presents as a behaviour change with no diff to point at, which is the hardest class of failure this system can produce.

---

## Row verdict

Six cells, zero of the nine components. One cell honestly closed by infrastructure (PERSIST.PERSIST, and contested as the diagonal). One half closed (PERSIST.SEE, syntactic only and not universal). One weak (PERSIST.REMEMBER, likely the same operation as REMEMBER.REMEMBER pointed at a different object). Three genuinely empty (SPECIFY, ACT, CHANGE), of which ACT is empty of addressable retrieval rather than of readout.

The row's strongest result is that PERSIST.ACT is empty and the emptiness has a measured analogue one class over: checkpoint recalled 0 of 144 tokens while getting 43 of 48 sequences right, which is REMEMBER present and ACT absent inside REMEMBER. PERSIST shows the matching profile, 109 ticks and 6 boots of state arriving intact with no predicate runnable against it. The grid did not discover that. It named a shape x24 had already put a number on, and predicted the same shape here. The prediction is unverified and stays labelled as one. What the row can claim without prediction is narrower and still useful: five of six cells survive an explicitly stated distinctness rule, one does not and is marked, and the rule was written down before the cells so it could not be bent to fit them.

---

## Row: the six cells inside ACT

ACT is the class where the live run fails. All 30 wakes end `AWAKE:brief FAIL :: trust ledger : produce_brief -> level 1`. The row below tests whether that failure has interior structure, and it does, but not the structure the ledger's own docstring claims.

**The row's finding, stated once and then evidenced cell by cell: the ledger gates one channel and grades the rest.** `trust.check()` is called at exactly three sites in the repo. `aea/bench/bench_core.py:318` sits inside `trust_gate` (296-340), which is game-bench code and inert for everything shipped ("P0's parts bind no charter row -> fire"). `aea/organs/talk.py:137` and `aea/server/controlroom.py:605` are the same gate on the same channel: both test `trust.check("speak")["allowed"]` before text-to-speech fires, and `talk.py:139` records the result after. That is a real call-time gate on a real reach, and it is the only one. Every other reach in the live entity performs first. `aea/organs/brief.py` writes `brief_output.md` at line 111 and calls `trust.record()` at lines 130-132, in that order: the artifact is released, then scored. So for `produce_brief`, the boundary the 30 wakes fail at is not a boundary. It is a post-hoc grade on text quality written into a permission ledger.

None of the nine components lands anywhere in this row. All nine operate inside a single model call: they shape a prompt, read a reply, or judge one. Not one can name a reach target, hold a produced artifact across a human decision, or observe whether a byte left the process. `carry` is the only component whose job is state between steps and its state lives inside one chain. `measure` and `latency` are the two whose kinds (gauge, channel) match what this row needs, and neither can observe anything outside the process. The ACT row is empty of the inventory, and that emptiness is the row's content.

### ACT.SPECIFY - the declaration of reach

**What the operation is.** Recording, before anything is performed, what will be touched outside the process, which charter capability that draw belongs to, and what would count as having released it. This is not SPECIFY.SPECIFY, which shapes a task for a model. It fixes a target and attaches a permission claim to it. A prompt fixes what gets produced; a reach declaration fixes what gets *reached*, and it is the only thing a gate can be a gate over.

**Occupant.** Empty from the nine. `goal` and `frame` are the closest-shaped components and neither applies: both shape the content of a call, and a reach declaration is about a destination, not a content. In code the absence is literal. `brief.py:111` is a bare `open("brief_output.md", "w")` at the working directory, which also routes around `grid.STATE`. No record of the form "capability=produce_brief, target=file, digest=..." is emitted anywhere before a reach.

**What it buys.** Enabling, in the strict sense the kinds table allows: with no declared target there is no argument to pass `check()`, so there is no subject a guard could refuse. This cell is the difference between a permission system and a scoreboard. In trust-grade terms it is the precondition for WATCHED and TRUSTED meaning anything, since both are defined as licences to perform an act that must first be nameable.

**What breaks without it.** Exactly what is in the ledger. The grade can only be applied after the fact, so every retained `produce_brief` FAIL entry reads `hades=unverified sections_ok=False`: judgments about text, not about a release. Across 40 runs the ledger holds data about how good the briefs were and none about what was released.

**What would have to be built.** A declaration record emitted before the reach: capability row, target class (file, network, audio, phone), payload digest, and the trust level read at that instant. **Estimate, not a measurement:** a few dozen lines. **Prediction:** this is the cheapest cell in the row to build and four of the other five depend on the record it emits.

### ACT.SEE - the confirmation that it landed

**What the operation is.** Judging whether the act took effect outside the process, which is a different question from whether the artifact was any good. HADES reads the brief and rules on its content. Nothing reads the world afterward. This is distinct from SEE.SEE (judging a judgment) and from SEE.ACT (a verdict reaching out): here the thing judged is a delivery, and the evidence has to originate outside the entity.

**Occupant.** Empty from the nine. `measure` is the right kind, a gauge that changes what can be known rather than what is answered, and it is structurally unable to occupy this cell: it sits at judge.1 inside a model call. `latency` is the inventory's channel-kind component and fails for the same reason, one level out: it separates timing within a judged call, never delivery beyond the process. Two degenerate stand-ins exist in code and are worth naming precisely because they show the shape of what is missing. `notify.py:23` decides an outbound call succeeded by substring-matching a vendor's response body against `("apikey is correct", "queued", "calling", "success", "will call", "your balance")`. `telegram_bridge.py:30-31` returns `ok: True` if `urlopen` did not raise. Both measure transport, neither measures receipt.

**What it buys.** Gauge, and the phrasing from the kinds table is exact: no gauge, no legitimate promotion. Take the one gated channel as the worked case. `speak` sits at WATCHED with streak 2 and 2 runs, and the value fed to `trust.record` is `speak.speak()`'s boolean. That boolean is evidence that a file was rendered (`speak.py:133` checks the mp3 exists and is at least 400 bytes) and that a player subprocess exited 0. It is not evidence that audio left the device or reached anyone. So the promotion mechanism is being fed a transport signal, and consecutive clean runs accumulate against something the gate cannot see.

**What breaks without it.** Silent non-delivery reads as success. A brief that HADES accepts and that never reaches Luis increments a streak toward TRUSTED. The failure mode is specific and it is the worst-shaped one available: the error direction of the promotion rule points toward *more* autonomy on unobserved acts.

**What would have to be built.** A per-channel landing check that rests on external evidence rather than a return code: file exists at the declared path with the declared digest, Telegram message id echoed back, a nonzero-length wav on disk with a nonzero playback duration. Cheap per channel, and it must be written per channel rather than generically, because "it landed" has a different witness for each.

### ACT.REMEMBER - the held artifact between production and release

**What the operation is.** Holding a produced-but-unreleased artifact somewhere addressable, across a wait, until a decision arrives. This is the operation that makes DRAFT a real state. `trust.py:11` defines level 1 as "may produce the artifact; a human must approve before anything leaves", and that sentence is a specification for a store: something must hold the artifact while the human is not there. It differs from REMEMBER.REMEMBER (state reaching the next step within a run) because the wait is unbounded and the reader is not the process.

**Occupant.** Empty from the nine, and this is the most consequential empty cell in the row. `carry` is the only component whose job is state between steps and it does not fit: it carries a running value inside one chain, and the artifact here outlives the process. Verified by search over `aea/`: no approval queue, no pending store, no outbox. The DRAFT semantics are implemented in exactly one place in the repo, `bench_core.trust_gate` (296-340), which is the game bench and which fires straight through for everything shipped.

**What it buys.** Guard. The kinds table defines a guard as what prevents demotion under slow-up-fast-down, where one false commit costs a whole streak, and a hold-before-release store is exactly the interposition that stops a bad artifact from becoming a committed act. Without it, level 1 and level 3 produce byte-identical behavior for `produce_brief` and the ledger's four levels are functionally two.

**What breaks without it.** Visible in the live state. `produce_brief` has been at DRAFT through 34 failures and wrote `brief_output.md` on every run. Demotion changed nothing about what left the process. The demotion rule at `trust.py:102` floors at DRAFT for any capability whose ceiling is above zero, so a failing capability can never fall to FORBIDDEN, and DRAFT has no teeth. A capability can fail indefinitely and keep releasing.

**Reading it through the recursion.** The x24 measurement found that `checkpoint` got 43 of 48 sequences right while recalling 0 of 144 tokens: state reached the next step and could not be addressed and reached back into. The ACT row has the same shape one class up. Artifacts are produced correctly and none is addressable by an approver. I judge the parallel real rather than decorative because the missing operation is the same in both cases, a store that can be reached into rather than only written through. It is an analogy and not a second measurement: x24 measured the REMEMBER row, not this one. **Prediction:** an addressable pending store will separate produce-rate from release-rate the way conversation separated from checkpoint, and the two numbers will stop tracking.

**What would have to be built.** `state/pending_acts.json` through `grid.atomic_save_json`, one record per held act carrying the ACT.SPECIFY declaration plus the payload, an endpoint to list and to approve or reject, and one line in `brief.py` routing the write through it when `check()` returns `draft_only`. **Prediction:** this is the highest-leverage build in the row, because it is the one that turns 30 identical wake failures into a queue that can be inspected.

### ACT.PERSIST - the release record that outlives the process

**What the operation is.** Keeping, across restart, what was actually released: when, through which channel, under which level, with what payload, and whether it can be revoked. Distinct from ACT.REMEMBER, which holds what has not gone out; this holds the trail of what has.

**Occupant.** Empty from the nine. A partial code stand-in exists, `trust_ledger.json`, and its partiality is the finding: it persists the grade, never the act. Two concrete losses. `trust.py:105` truncates history to the last 20 entries, so of 34 `produce_brief` failures only the most recent survive and 14 are gone. And `brief.py:111` overwrites `brief_output.md` on every run, so the released artifact has no version trail either. After 109 ticks and 6 boots across 17 unattended days, no state in the repo can be queried for what was released on tick 40, which is the question `trust.py:7` claims is always answerable ("The entity can always answer: 'why am I allowed to do this?'").

**What it buys.** Channel, in the kinds sense: it makes a failure attributable rather than merely visible. It does not prevent a demotion and it does not shorten a path to promotion. It is what makes the demotion side of slow-up-fast-down diagnosable after the fact, which is a different purchase from preventing the commit in the first place.

**What breaks without it.** No revocation and no audit. If `send_outbound` were ever raised off zero, nothing would record what went out, so the first bad send would be undiagnosable and unrecallable. The absence is currently masked by `send_outbound` sitting at FORBIDDEN, which defers this cell's cost rather than avoiding it.

**What would have to be built.** An append-only `state/acts.jsonl`, never truncated, one line per completed release joining the ACT.SPECIFY declaration to the ACT.SEE landing result. The 20-entry truncation at `trust.py:105` should stay for grade history and must not be inherited by this log.

### ACT.ACT - the release itself **[WEAK]**

**What the operation is.** The crossing: a byte leaves the process and cannot be recalled.

**Why I am marking this cell weak.** The description above is the definition of the outer class, not of a sub-operation inside it. The diagonal cell (X,X) restates its own row, so it tests nothing about the recursion; at best it is bookkeeping for where the other five attach. My best distinction is that inner ACT is the crossing instant while the other five are pre-crossing or post-crossing operations around it, and that distinction is doing work the words barely support. It is the same failure shape the ACT.CHANGE cell below flags, one square over. **Prediction, structural:** all six diagonal cells in the 36-cell grid will read this way, and if they do, the honest grid is 30 cells plus a diagonal of six labels.

**Occupant.** None of the nine, and this is not an absence in the way the other cells are absent: the operation runs, it just runs mostly ungated. Reach sites in the live entity: `notify.py:21` places a telephone call, `telegram_bridge.py:30` sends a message, `agent_tools.py:15,32,64` performs HTTP requests, `brief.py:111` writes a file. None of those four consults the ledger. `speak` is the fifth and the only one that does, at `talk.py:137` and `controlroom.py:605`. The exemption for one of the four is explicit rather than accidental: `notify.py:2` states that a self-notify to the owner is "not a trust-FORBIDDEN outbound". That may well be right on the merits. It is a policy decision written into a comment instead of into the charter, and a policy that lives in a comment cannot be read by a gate.

**What it buys.** Enabling, in the strictest sense the kinds table allows: the difference between FORBIDDEN and anything at all. It is also where the honesty of the board is decided. `send_outbound` reads 0/FORBIDDEN while three working outbound channels never consult the ledger. The board is not wrong, because those channels were never registered as `send_outbound`. But an unregistered channel and a forbidden one are indistinguishable on the board, and the board is what `trust.py:112` calls "the entity's answer to 'why are you allowed to do what you do?'".

**What breaks without a gate here.** The separation between capability and permission does not exist in the live system for four of five channels. It exists in the charter as data and in `bench_core.trust_gate` as inert bench code. Between those two, for those four channels, there is nothing.

**What would have to be built.** One choke point. Every reach in `aea/organs/` and `aea/io/` routed through a single `release()` that takes the ACT.SPECIFY declaration, calls `trust.check()`, and either performs, hands to the ACT.REMEMBER store, or refuses and names the level. Counting the sites named above, that is seven conversions, not four: three in `agent_tools`, plus `notify.call`, `telegram_bridge.send`, the `brief.py` file write, and `speak`, which already checks and would move its check into the same place.

### ACT.CHANGE - the act path modifying its own surface **[WEAK]**

**What the operation is.** Modifying which channels exist, what the release predicate is, or what the permission surface looks like. In charter terms this is `self_modify_code`, at FORBIDDEN with ceiling 1, reviewable diff only.

**Occupant.** Empty. No diff producer, no patch path, no proposal mechanism exists in code. The charter row is a declared dial with no enforcement path behind it, which the repo's own vocabulary calls a fake lever (`bench_core.trust_gate` docstring; `design/E4_UX_P0.md:614`).

**Why I am marking this cell weak rather than filling it.** I cannot cleanly distinguish ACT.CHANGE from CHANGE.ACT. Both come out as "a modification to its own structure is emitted", and if cell (X,Y) and cell (Y,X) collapse into one operation, that is a problem for the recursion hypothesis and belongs on the record as a problem. My best attempt: ACT.CHANGE modifies the release surface specifically, the channel roster and the gate predicate, whereas CHANGE.ACT modifies anything at all and emits the modification. The distinction is thin and I do not trust it. **The cell stays weak until the CHANGE row is written and the two can be compared directly.** Whoever writes that row should treat this as an open collision to resolve, not as settled.

**What it buys, provisionally.** Lever, and correctly the last cell in the row to build. **Prediction:** building ACT.CHANGE before ACT.REMEMBER and ACT.PERSIST exist yields a system that can rewrite its release rules with no store of held acts and no audit trail of past releases, which is strictly worse than the current state. Build order for this row: SPECIFY, REMEMBER, ACT, SEE, PERSIST, and CHANGE last or never.

**What breaks without it.** Currently nothing, and saying so is the honest answer. The release predicate changes only when Luis edits Python. Given the state of the other five cells, that is the right arrangement, and this empty cell should stay empty.

---

**Row summary.** Six cells, zero occupied by any of the nine components. One (ACT.ACT) is live in code through five reach sites of which one consults the ledger, and it is marked weak because the diagonal restates its own class. One (ACT.PERSIST) has a partial code stand-in that persists the wrong noun. One (ACT.CHANGE) is marked weak on a collision the CHANGE row must resolve. The 30 identical wake failures are not a permission boundary holding for `produce_brief`. They are the absence of one, recorded 30 times, in a repo that has proven it can gate a channel because it already gates speech.

---

## ROW C: THE SIX CELLS INSIDE CHANGE

*CHANGE modifies the system's own structure. Its interior is the most dangerous row in the grid and
the reason is structural rather than rhetorical: in every other row the object of the operation is a
task, an output, a value or an external effect, and the blast radius of a mistake is bounded by that
object. In this row the object is the instrument, so a mistake is inherited by every operation the
instrument performs afterwards, including the ones that would have caught it.*

**Occupancy, stated first because it is the row's main result: none of the nine components lands in
any CHANGE cell.** All nine are pipeline parts inside an organism. They shape a prompt, fire a call,
read a reply, repair an answer, carry a value, gauge a judgement and time it. Not one of them writes
to the structure that runs them. `catalogue.json` makes this explicit for the closest candidate:
prompt text is DATA and "a variant is a data change, never a code change". The charter agrees:
`self_modify_code` sits at level 0, ceiling 1, `promote_after` 99, described as a reviewable diff
only. **The grid and the ledger independently say the same thing, which is the first non-trivial
agreement between them.**

**Second result, and it costs the row a cell: the six do not all survive the test here.** Four cells
name operations that are real and empty. One, CHANGE.REMEMBER, does not survive and is marked WEAK
below. One, the diagonal, degenerates into CHANGE.ACT and is marked WEAK. The row is four
specifications, one deletion and one fixed point.

**Three rejected occupants, named so the emptiness is a finding rather than an oversight.** `critic`
(lever, repair.1) rewrites the answer, not the pipeline, and calling that self-modification is the
exact forced analogy this document exists to catch. `frame` (lever, shape.2) changes what the call
receives, which is configuration. `carry:free` lets a component write an unconstrained note into its
own next input, an unconstrained self-addressed write with no fixed container, and it is still data
rather than structure. None of the three occupies a cell here.

---

### CHANGE.SPECIFY - the charter that names the editable surface

**The operation.** Declaring what may be edited, what an edit is toward, what counts as one legal
edit unit, and which invariants must survive it. It is not the same operation as SPECIFY.SPECIFY,
which sets the shape of a task, nor ACT.SPECIFY, which names one effect and its preconditions. The
difference is quantification. An act specification constrains one effect. An edit specification
constrains the class of all future effects, because the edited component performs every later act. A
specification that is adequate for an act is underspecified for an edit by exactly that gap.

**Occupant: empty.** No component. The nearest real artefact is `CHARTER` in `aea/kernel/trust.py`,
which names `self_modify_code` and its three locks, and it was written by a human from outside the
process. That is the correct place for it and it is worth saying why: **the charter is a dict in a
`.py` file, and `.py` files are the surface CHANGE acts on.** A CHANGE.SPECIFY that lives on the
editable surface is a suggestion, not a specification. What makes it hold today is not its location,
it is that nothing in the system is permitted to reach it.

**What it buys.** Enabling, in the strict sense of the kind: the difference between FORBIDDEN and
anything at all. Grade terms, code-checked, and the earlier draft of this cell got this wrong so the
correction is stated plainly. The charter line already exists, so the missing thing is not the line.
The missing thing is that **no code path anywhere calls `trust.record("self_modify_code", ...)`**.
The only `record` call sites in the repo are `aea/organs/brief.py` lines 130-132 (`gather_public`,
`reason_private_local`, `produce_brief`) and `aea/organs/talk.py` line 139 (`speak`). `promote_after`
99 is therefore nominal: 99 clean runs cannot accrue when zero runs can be recorded. What
CHANGE.SPECIFY would produce is the first thing that could be recorded as a run at all, because a run
needs a unit and a clean-or-not criterion before it needs a grader. Note also what the level means
today: at level 0, `check` returns `allowed` False and `draft_only` False. Ceiling 1 is a cap on
where a clean streak could take it, not a permission already granted.

**What breaks without it.** Modification toward nothing in particular, driven by whatever the current
session happens to contain. The cheapest available evidence for this is one level down and it is
measured: the `carry:free` form gives a component an unconstrained write over its own next input and
recalls 7 of 144 tokens, against 144 of 144 for the specified `conversation` container. That is data,
not structure, so it does not occupy this cell. **Prediction: the same ordering holds when the write
target is structure rather than input, and the gap widens, because a structural write is read back by
more consumers than a note is.**

---

### CHANGE.SEE - the judge that outlives the thing it grades

**The critical cell of the row.** The operation is comparing the system after an edit against the
system before it, on a criterion the edit could not have moved. It is genuinely unlike SEE.SEE, which
grades one output against the ground truth of one item. An edit has no single output to grade. Its
unit is a distribution of outputs over a population of items, and the pre-edit distribution stops
existing the moment the edit lands unless it was archived first. **SEE.SEE needs a correct answer.
CHANGE.SEE needs a preserved population and a re-run.** Two consequences follow directly, and both
already have the right shape somewhere else in this repo: `rescore.py` separates generation from
scoring over an archive it appends to and never overwrites, so a corrected reader can be applied to
spent runs, and `calibrate.py` establishes that a benefit is only measurable inside the failure
window of the fuel. Applied here: an edit graded on items the system already passes measures the
edit's cost and nothing else. Both mechanisms exist for experiment evidence. Neither exists for
structural change.

**Occupant: empty, and the emptiness is precise.** `measure` (gauge, judge.1, `can_know`) is the only
gauge in the inventory and it is the right KIND for this cell. It grades an answer. There is no gauge
over a structural change anywhere in the nine.

**The structural hazard, and its shape is already frozen in the repo one level down.** A component
that can rewrite the pipeline can rewrite the judge that grades it. The instinct is to read that as a
motivated act. The repo shows it is not: `readout` is read.order 1 and `validation` is read.order 2,
they share one output field, and the later one wins. On a mute reply `call+readout` recovers 4 and
`call+readout+validation` returns None, frozen as golden rows in `aea/lab/tests/test_golden.py`, with
no network involved. Readout's own guard-deference line is unreachable, because the abstention it
defers to has not happened yet. **That is not a guard being destroyed by a lever. It is two parts
sharing one slot and ordering deciding the winner.** CHANGE.SEE is the same shape with a larger slot:
if the judge and the edit target sit in one namespace, the last writer wins, and the edit target is
by construction able to be a writer. The hazard needs no intent and no adversary. It needs a shared
slot and an order.

**A second hazard, code-true, in the grading mechanism itself.** `trust.record` demotes with
`if e["level"] > min(1, c["ceiling"])`. For `self_modify_code`, ceiling is 1, so the floor is 1: 99
consecutive clean runs are required to reach DRAFT, and once at DRAFT no failure can demote it. State
the scope honestly, because the earlier draft claimed uniqueness it does not have. This is a general
consequence of ceiling <= 1 and it holds identically for `draft_outbound` (level 1, ceiling 1) and
trivially for every ceiling-0 capability. **Slow up, fast down holds only for capabilities with
ceiling >= 2, which is every capability except the four whose failures are least reversible.** Stated
as a code fact; the operational implication is a prediction, since the branch has never executed for
this capability.

**What it buys.** Gauge. No gauge, no legitimate promotion, and here that is not a slogan.
`produce_brief` has a verdict source at `brief.py:132` and therefore carries 34 fails in 40 runs and
sits pinned at DRAFT: visible, honest, useful failure. `self_modify_code` has no verdict source and
no call site, so a run of it would record zero fails if one were ever recorded at all. **Zero fails
from competence and zero fails from having nothing that could register one are the same row in the
ledger.** `gather_public` reads TRUSTED, streak 39, 44 runs, 0 fails, and that record is worth
something exactly because something was grading it.

**What breaks without it.** Edits become a random walk executed by the system performing every other
operation, with a clean log the whole way, because a log written without a judge records that a step
ran and never that it was right. Cell-specific rather than generic: the degradation is invisible
precisely in proportion to how much of the judging apparatus the edit touched, so the worst edits are
the quietest.

---

### CHANGE.REMEMBER - the pre-edit copy that makes a diff possible   [WEAK]

**Marked weak, and the reason is that the cell fails its own necessity test.** The intended operation
is holding the prior structure inside the session so the change can be expressed as a difference
rather than a replacement. Test whether that is load-bearing here. REMEMBER exists as a class because
what is carried is otherwise lost between steps: a model call retains nothing, so the running value
must be handed forward, which is exactly why `carry` exists and why `carry:none` is a real control.
The structural surface has the opposite property. It is a file. It is durable by default, readable at
any point in any process, and a diff against it is a read rather than a carry. **Nothing has to be
held for the diff to exist.** The cell is REMEMBER-shaped because the grid has a REMEMBER column, not
because the operation is doing work.

**Correcting two claims an earlier draft of this cell made, both wrong.** First: "no retained pre-edit
state, no diff, therefore no legal artefact" is false while the prior version is on disk. Second, and
this is a repo fact rather than a judgement: that draft argued the in-session hold cannot serve
CHANGE.SEE because "routes load at import and the running PID must be killed before an edit is live".
That is a property of the controlroom server, not of this process class. `aea/loop/live.py` line 94
spawns each wake as a fresh subprocess under `sys.executable` with `["-m", "aea.organs.brief"]`, so
an edited module is imported by the next wake with nothing restarted. **The boundary a structural
edit crosses here is a wake, not a boot**, and in the live state wakes outnumber boots 30 to 6. The
substrate CHANGE.SEE needs, a re-run in a fresh process against a preserved population, already
exists at wake granularity. Nothing about it routes through this cell.

**The residue that is real, kept small rather than inflated.** A multi-file edit must hold the state
of the edit itself across its own steps so it is not applied half. That is REMEMBER.REMEMBER applied
to an edit-shaped task, not a distinct operation of CHANGE, and saying otherwise is the forced
analogy.

**Occupant: empty, and the emptiness carries no specification.** `carry` (lever, carry.1,
`accuracy_over_sequence`) carries a task value; the catalogue's `held` capacity reads "state survived
into the next step" against a value hit. It has never carried a structure and nothing in its forms
could. But unlike the other empty cells in this row, this one does not name a thing to build.

**What it buys.** Nothing that CHANGE.PERSIST plus a file read does not already buy. **Prediction for
whoever writes the other five rows: a REMEMBER cell collapses wherever the object of the outer class
is already durable. Check REMEMBER inside PERSIST for the same collapse.**

**What breaks without it.** For a single-file edit, nothing. For a multi-file edit, partial
application, which is a transaction problem rather than a memory problem and belongs to CHANGE.ACT.

---

### CHANGE.PERSIST - the lineage, not the current version

**The operation.** Making both the modification and its provenance survive restart. Two things, and
conflating them is the failure mode of the cell. PERSIST.PERSIST is an atomic write of current state
and a single current-state file is a correct implementation of it. Here that same implementation
destroys the cell's purpose, because what must survive is a LINEAGE: which version produced which
measurement, in order, recoverable. A file that holds only what is true now cannot answer whether the
last edit helped. This cell also absorbs the work the REMEMBER cell above failed to justify: the
pre-edit state is available because it was persisted, not because it was held.

**Occupant: empty of the nine, and the correct shape exists elsewhere in the repo for other reasons.**
The experiment harness refuses to overwrite an archive (`refusing to overwrite existing evidence`,
`harness.py:856`, `calibrate.py:152`), and `rescore.py` appends a new score set beside the old with
its own id and reports the diff between them, on the stated rule that a score is a hypothesis about a
run rather than a fact about it. That is exactly the persistence discipline an edit history needs. It
is applied to evidence, not to structure.

**One constraint in the grading substrate, code-true.** `trust.record` truncates with
`e["history"] = e["history"][-20:]`. The live ledger covers 109 ticks across 6 boots over 17 days,
and all 30 recorded wakes read the same `produce_brief -> level 1` line. **Prediction: any CHANGE
whose provenance is kept in the trust ledger inherits a 20-entry audit horizon per capability and
will be unable to attribute a regression to the edit that caused it once 21 records have accrued.**
The prediction is conditional on that storage choice; a lineage kept in the archive discipline above
does not inherit the cap.

**What it buys.** It converts a modification into an accumulation. In grade terms it is what makes a
streak a streak at all, and the same property is what makes a streak forgeable across boots: a system
that persists can grind toward `promote_after` during the very boots in which it is degrading, since
without CHANGE.SEE the runs it records are clean by default.

**What breaks without it.** The modification reverts at the next restart while the evidence that
motivated it regenerates, so the same change is produced again every boot with no record that
distinguishes the second occurrence from the first. Cell-specific second effect: an edit whose
provenance is gone cannot be rolled back, only re-edited, which means recovery is another edit
performed by the component that produced the fault.

---

### CHANGE.ACT - the diff that leaves the process

**The operation.** Emitting the modification as an artefact a reviewer outside the process can
receive, and the reciprocal half, applying an approved edit to the live surface. Distinct from
ACT.ACT in target and in direction. ACT.ACT is outbound and terminal, and its blast radius is one
effect. CHANGE.ACT is outbound then inbound, with a mandatory human between the halves, and the
inbound half is the dangerous one because it lands on the instrument. The charter's wording is a
specification of this cell: a DRAFT diff for review means the artefact is produced and a human
approves before anything moves. Note what the level says today: `self_modify_code` is at 0, so this
is a cap on what the capability could earn, not a standing authorisation.

**Occupant: empty.** `latency` (channel, judge.2, `separability`) is the only channel in the nine.
Resist the neat fit: the catalogue defines a channel as making a state legible in a NON-TEXTUAL
signal, and `latency` is that literally, separating right from wrong by time. A diff is text, so the
diff is not a channel in the vocabulary's sense. What it shares with one is attributability, and that
is the only part of the analogy worth keeping.

**What it buys.** Enabling, plus attributability. FORBIDDEN to DRAFT is gated on this cell rather
than on competence: with no presentable diff there is no artefact for the ceiling to cap. And the
attributability property is what would make a bad edit traceable to the edit rather than showing up
later as diffuse degradation.

**What breaks without it.** The edit is either applied silently or not at all, and the silent case is
the failure specific to this cell: a change to the instrument that no reviewer received is
indistinguishable, from outside, from the instrument having always behaved that way. Note the
delivery constraint honestly: `send_outbound` is level 0, ceiling 0, so there is no charted outbound
path. Review here depends on a human opening a file the entity wrote. That is a human polling, not a
delivery, and it is a real gap between the charter's "for review" and any mechanism that ensures a
review happens.

---

### CHANGE.CHANGE - the edit to the edit rule   [WEAK]

**Marked weak, and the reason is a finding rather than a shrug.** The intended operation is
modifying the mechanism by which modifications are made and permitted: editing the charter, the
ceiling, the promotion rule. Test whether that is a distinct operation from the other five cells. It
is not. The charter is source; source is structure; structure is what CHANGE.ACT writes to.
**CHANGE.CHANGE is CHANGE.ACT with the object of CHANGE.SPECIFY as its target.** No new operation,
just a target selection. Inside this outer class specifically, the diagonal degenerates, because
CHANGE is the one class whose object domain contains its own specification. Writing a distinct
operation into this cell would mean inventing content, which is the thing this document is supposed to
refuse. **Prediction for whoever writes the other five rows: check the diagonal cell in each. If it
also collapses into that row's ACT, the diagonal is a structural artefact of the recursion rather
than six real cells, and the grid is 30 cells plus 6 fixed points.**

**Occupant: empty, and here alone the emptiness is a requirement rather than a gap.** In the four
live cells of this row an empty cell is a specification of something to build. This one is a
specification of something not to build. The hazard it names is real even though the operation is not
distinct: a system that can select the charter as its edit target can raise its own ceiling, and the
ceiling is the only thing in the mechanism that a clean streak cannot move. The promotion rule can be
satisfied. A ceiling is a human decision that a diff gets read.

**What it buys.** Nothing that should be bought. If it were built its kind would be enabling, and
enabling is the kind that decides between FORBIDDEN and anything at all, which is the one decision
that must sit outside the process.

**What breaks without it.** Nothing. What breaks with it is the whole row: the only constraint that
survives a component able to edit its own permissions is a constraint enforced outside the process it
can edit. **Prediction, and it follows from the mechanism rather than from alarm: any optimisation
whose objective is computed from values reachable inside the process scores at least as high with the
ceilings relaxed, because a ceiling only ever subtracts from the reachable set. Relaxing it therefore
registers as an improvement under every criterion computable from inside.** The current
implementation happens to hold, because `self_modify_code` is 0, nothing calls `record` for it, and
every path to the charter runs through a human. It holds by those three facts and not by any property
of the code.

---

## WHAT THIS ROW ARGUES

The recursion survives this row and it survives non-trivially, but it survives with a cell deleted,
which is the point of testing it: **CHANGE is not one forbidden capability, it is four missing
operations, one cell that does not earn its place, and one that must stay missing.** The charter says
FORBIDDEN, which reads as a policy choice reversible by a decision. The row says the capability is
currently ungradeable for mechanical reasons a decision would not fix: no specification of what one
legal edit is, so no criterion; no gauge over structure, so no verdict; no call site anywhere calling
`trust.record` for it, so `promote_after` 99 counts runs that cannot occur; a 20-entry audit horizon
if provenance is kept in the ledger; and a demotion floor at DRAFT that applies to every capability
with ceiling <= 1.

The deleted cell is worth as much as the kept ones. CHANGE.REMEMBER fails because the object of this
outer class is already durable, and that failure is a prediction about the rest of the grid rather
than a local embarrassment.

The strongest evidence that the recursion is doing work rather than decorating is that CHANGE.SEE's
hazard was already frozen in the repo under a different name, one level down, with no network and no
adversary: `readout` and `validation` share an output slot, order decides, and the deference check is
unreachable code. **The grid did not discover that. It named the general form of it, and predicts the
same form recurs wherever a judge and its target share a namespace.** Order and a shared slot are
sufficient. That is the whole hazard, and it is why CHANGE.SEE is the cell to build first and the one
that cannot be built by the thing it grades.
