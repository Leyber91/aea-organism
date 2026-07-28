# THE ADDITION LAW — how a module joins the ecosystem

*Written 2026-07-27. This is the whole purpose of the lab stated in one page: add a capability to the*
*system, find the right way to attach it, and prove it took nothing away.*

---

## THE LAW

> **A component must not subtract functionality when it is added.**

That is the test. Not "does it help" — *what does it add, and what does it cost?* Every measurement in
this project should produce a two-sided ledger per module, and a module that gains one capacity while
silently destroying another has failed even if its own number went up.

---

## THE LAW IS CURRENTLY BROKEN, FOUR TIMES OVER

Every one of these is measured, and every one is a component subtracting on addition.

**ROW 1 REATTRIBUTED 2026-07-27. The subtraction is real; the cause was not the guard.**

Reproduced with no network at all, on a mute reply where the working is right and the mouth says 9:

```
call                      -> 9     stated             the mouth, wrong
call+readout              -> 4     work:enumerated    RECOVERED
call+readout+validation   -> None  declined           the recovery is destroyed
```

`Readout` is `read.order 1` and `Validation` is `read.order 2`, so **Readout runs first**, recovers
correctly, and Validation then re-reads the raw text from scratch and overwrites the shared answer
slot. It never checks whether a lever has already acted. Four parts write that one slot — `Call`,
`Readout`, `Validation`, `Critic` — and the last one to run wins.

Worse, `Readout`'s own deference line, `if ctx.declined or ctx.read_by not in (None, "stated"):
return`, is **unreachable**: the abstention it defers to has not happened yet. And the note recorded
elsewhere in this repo has the direction backwards — it says validation "handed control down to
readout", when readout ran first and was clobbered.

**So the row below states a true measurement and the wrong cause.** This is the document's own
protocol point 5 — *"wrong placement subtracts without the module being wrong; the module was fine,
the seam was not"* — and the headline table contradicts it. Both rows now frozen in
`tests/test_golden.py`, so a wiring change breaks the test instead of silently moving the finding.

| module | added | subtracted | receipt |
|---|---|---|---|
| ~~`validation`~~ **WITHDRAWN** | can_abstain | ~~all accuracy on a rod that was already right~~ **the treatment was never independently manipulated - see above** | x17, void |
| `critic` | revised | **up to −0.55**, and every large loss lands on a high baseline | x20 |
| `carry:free` | held (nominally) | **−0.636 at sixteen steps.** Nine of eleven sequences destroyed | x21 |
| `frame:manner` | nothing | **8/12 to 0/6** on one rod, 69% to 9% on another | x15 |

And a fifth, in the harness rather than the architecture: `x22`'s first `STEP_GOAL` read *"Reply with
ONLY the resulting number"* — a manner instruction in the goal slot — and it took `shows_working` from
0.29 to 0.00, making three of eight capacities unmeasurable.

---

## THE RESOLUTION, AND IT IS NOT TO WEAKEN THE LAW

Look at the first three rows. `validation` and `critic` both subtract **on a rod that passes bare**.
`carry:free` subtracts because an unstructured history injects noise rather than losing it. The
pattern is not that these modules are bad. It is that **each has a precondition, and it subtracts
exactly when the precondition is unmet.**

So the law sharpens:

> **A component must not subtract when its PRECONDITION IS MET.**
> **What it subtracts when the precondition is UNMET is its toxic profile, and that must be declared.**

A precondition is part of the module, not a note about it. `catalogue.json` already carries
`requires` for module-to-module edges and `conflicts` for module-to-fuel edges — `validation` and
`critic` both declare `conflicts: fuel:passes_bare`, which is the same statement read from the other
side.

---

## THE TEST PROTOCOL — five questions, in this order

Every new module answers all five before it is seated anywhere.

**1 · WHAT CAPACITY DOES IT CLAIM?** Named, and measurable independently of accuracy. `can_abstain`
is not `accuracy`. `shows_working` is not `accuracy`. A module scored on the wrong axis will read as
inert no matter what it does — this project did that to five components across two worlds.

**2 · WHAT IS ITS PRECONDITION?** Which modules must be beneath it, and what must be true of the fuel.
Both are hypotheses until an assembly convicts them: `x16` ran `call+frame` with its declared
precondition absent and scored 0.65 against 0.66 for the seat that satisfied it.

**3 · WITH THE PRECONDITION MET: DOES IT ADD ITS CAPACITY, AND SUBTRACT NOTHING?** The full capacity
vector before and after. **Any drop outside the band is a failure, whatever happened to its own
number.** This is the law.

**4 · WITH THE PRECONDITION UNMET: WHAT EXACTLY DOES IT COST?** That is the toxic profile, it is a
creature, and it is the most valuable thing the module produces for the game. `Integer sufficiens`
exists only because someone seated a guard on a rod that needed nothing.

**5 · WHERE DOES IT ATTACH?** Stage and order within stage. Wrong placement subtracts without the
module being wrong: `x16` lost 18 points because `validation` abstained at `read.order 2` and handed
control to `readout` instead of ending the read. The module was fine; the seam was not.

---

## THE BEST TEST SITUATIONS

A situation is only useful if it can show both directions at once.

**The baseline must fail, and fail by drift rather than by inability.** A module cannot demonstrate a
capacity on a task nobody fails, and it cannot demonstrate retention on a task where step 1 is already
beyond the rod. `x22`'s chain was calibrated to exactly this: trivial arithmetic on a five-digit value,
so holding the number is the work.

**Both fuels must be present: one that needs the module and one that does not.** The second is where
subtraction shows. Every large loss this project has measured landed on a rod that was already right,
and a battery of only-failing rods would have found none of them.

**The measurement must be a vector, not a scalar.** `x22` scores eight capacities per rung. A flat
accuracy row beside a collapsing capacity column is a signature you can read at a glance, and it is
invisible to any single number.

**And the null must be interpretable.** Every truth in this project is a single integer, so on
output-side modules there is almost no surface to act on and a null result cannot be distinguished
from a task too small to show one. That gap is recorded in `tasks.json` under `answer_shapes` and it
is the next thing to close.

---

## WHAT THIS MAKES THE GAME

The player's loop is this protocol. They meet a creature, read what it is missing, seat a part, and
watch the capacity vector move — including the column that goes **down**. The lesson World 1 already
teaches is the law stated as play: **the part that promises repair is the one that takes your correct
answer away.**

---

## MEASURED — x22, 2026-07-27. The ladder is not a ladder.

Eight rungs, two rods, the calibrated retention chain. Accuracy flat across all eight, inside the band
end to end. The capacities are not. THE `held` COLUMN IS A DASH ON EVERY RUNG: six had no state
channel and the other two were misread. An absent measurement is a dash, never a number.

```
v1 call          answ 1.00                     held  --   show 0.26              drift@2.0
v2 +goal         show 0.26 -> 0.57             held  --                          drift@2.0
v3 +frame        show 0.57 -> 0.38   COST      held  --                          drift@1.5
v4 +readout      reco 0.00 -> 0.54   show 0.54 held  --                          drift@1.5
v5 +validation   can_ 0.00 -> 0.61   COST reco -0.404      held  --              drift@1.5
v6 +critic       revi 0.00 -> 0.74   COST can_ -0.607      held  --              drift@1.5
v7 +carry        held  --            read returned the step index; text unstored drift@1.0
v8 +measure      not delivered                                                   drift@1.0
```

### THE ARCHITECTURE IS NOT MONOTONIC — AND THE PEAK WAS AN ARTIFACT

**CORRECTED 2026-07-27.** This section read: *"v4 is the best organism on this task and it is four
parts, not eight ... the highest retention on the whole ladder at 0.12, above the bare call and above
every assembly larger than it."* **The peak does not exist.**

x22 selected its scored chains with `done = [r for r in recs if r["completed"]]` — a truthiness test,
not `== steps` — and then took an unweighted mean of per-chain rates. So a chain that died after one
step weighed exactly as much as a chain of fourteen. v4's 0.119 is **one chain**:

```
v4   llama-3.1-8b   completed 2 of 14   hits 1   held 0.500   flags: call_failed
```

A connection that dropped after two steps, whose single hit was **step 1 — the opener, where the task
itself states the starting value** — averaged against a full fourteen-step sequence. That is the whole
peak. It is a dead socket, not an organism.

**WITHDRAWN A SECOND TIME, SAME DAY, AND THE SECOND WITHDRAWAL MATTERS MORE THAN THE FIRST.**

The correction above re-derived the ladder over completed sequences and concluded: *"the bare call
retains best at 0.071, and nothing added to it ever retains better."* **That is also wrong, and it is
wrong in a worse way, because it was computed from a run that could not have shown retention at all.**

```
v1 - v6    form = "none"        THERE IS NO STATE CHANNEL
v7 - v8    form = "checkpoint"

max hits any chain ever achieved:   1        across all 48 chains of 14 steps
first_miss across the whole ladder: {1, 2}   and nothing else, ever
1/14 = 0.0714                                v1 scored 0.071
```

`Chain._body` emits the starting value at step 1 only. For `form="none"` every later step is
*"Step N: subtract 13"* with **no running value, no carried string and no history** - `Carry.pack`
returns empty for that form and `chain.py` passes history only for `conversation`. So on six of the
eight rungs the rod was asked to continue a calculation it was never given.

The traces say it out loud. v1's step 2 records `value=13` against truth 48364 - **the operand,
echoed back**, because nothing else was in the prompt. On the repaired instrument the replies are
stored and they are not drift at all: *"To proceed with the calculation, please provide the number
you would like to subtract 13 from."* That is a refusal.

**So `held` is arithmetically the indicator "was step 1 right", divided by fourteen.** A fourteen-step
chain delivered one step of dynamic range, and `0.071` is the ceiling of a zero-channel arm rather
than a property of the bare call. v7 and v8 are the only rungs with a channel and their `0.000` is a
read artifact - their traces record the STEP COUNTER as the value (1, 2, 3, 4 against truths 48377,
48364, 48385) - and no reply text was stored, so they can never be re-scored.

**THE RETENTION COLUMN OF THIS TABLE MEASURES NOTHING. Not in either direction.** There is no ladder,
no peak, and no null result. There is an empty axis. The claim is withdrawn rather than replaced.

The document's own criterion, thirty lines above, forbade exactly this: *"The baseline must fail, and
fail by DRIFT rather than by INABILITY."* The baseline first-misses at step 2 of 14 by asking for the
number back.

### AND THE LESSON IS ABOUT THE CORRECTION, NOT THE ORIGINAL

The first withdrawal found a real defect and recomputed the number from the same run. **Recomputing a
number from a run that could not have produced evidence is not a correction - it is the same error
with better arithmetic.** Before re-deriving anything, ask what range the measurement could have
taken. If the answer is "two values, one of which the prompt gives away," there was never anything
there to re-derive.

**What survives, and it is not nothing.** The non-retention columns on v1-v6 have real dynamic range
- `shows_working` 0.26 to 0.57, `recoverable` 0.00 to 0.54, `can_abstain` 0.61, `revised` 0.74 - and
those rungs share the same absent channel, so the ADDITION-LAW SUBTRACTIONS between v3 and v6 are
untouched by this. The law itself is unharmed. Only the retention reading dies, and v7/v8's entire
capacity row goes with it.

The document already knew this and contradicted itself. Line 149 states *"the bare call — the highest
hit rate on the ladder, 7.1%, and it holds better than six of the seven assemblies above it."* That
sentence was true and this section denied it. The correction resolves the contradiction in favour of
the evidence.

**What survives unchanged.** v4 does carry the widest set of LIVE CAPACITIES — `recoverable` is 0.000
at v1 through v3 under either aggregation, so it genuinely first appears at v4. Capacity and retention
are different claims and only the retention one dies. Everything above v4 still trades one capacity
for another, above v6 it trades for nothing, and the drift point still moves *earlier* as parts are
added: step 2.0 at v1, step 1.0 at v8.

**Two qualifications, neither rescuing the peak.** The corrected v4 groq row rests on a single
surviving chain, so 0.036 is defect-17-clean but not well-powered. And the hit reads themselves came
through the `total` dialect, which returns an addend — v1's trace shows value 13 against truth 48364 —
so every rung carries defect 15 uniformly. Neither moves v4 back above v1.

**So completeness is a TOOLKIT, not a configuration.** The full architecture is the set of capacities
made available. It is not the assembly you should be running. A player who seats everything has not
built the strongest creature, they have built one that abstains, overrides its own abstention, and
carries the override forward.

### AND PARTIAL ASSEMBLIES ARE NOT DEGRADED FULL ONES

They are different organisms with different competences, and the numbers say so:

| assembly | what it is best at |
|---|---|
| `v1` bare call | the highest hit rate on the ladder, 7.1%, and it holds better than six of the seven assemblies above it |
| `v2` +goal | the most working elicited, 0.57 — more than the frame produces |
| `v4` +readout | the widest competence. NOT the best retention - see the correction above |
| `v5` +validation | the only assembly that can refuse, 0.61 |
| `v6` +critic | the only assembly that re-decides, 0.74 |

None of those is a worse version of another. **`v5` is the only thing on the ladder that can abstain;
that capacity exists nowhere else and is destroyed the moment you add the rung above it.**

### THE TWO SUBTRACTIONS THAT ARE WIRING, NOT MODULES

Both are fixable without touching either component, which is the whole value of declaring the wiring.

**`validation` costs `recoverable` −0.404.** It sits at `read.order 2`, its abstention ends the read,
and the readout never fires. This is x16's eighteen-point seam seen as the capacity loss it always was.

**`critic` costs `can_abstain` −0.607, all of it.** `repair` runs after `read`, makes its own call and
overwrites the answer, so **the critic un-does the guard.** Seat both and you get neither. Nothing
declared that, and no accuracy measurement could have surfaced it.

**And `carry` compounds the second.** At v7 the critic revises every step, so what `carry` carries is
the critic's rewrite rather than the working value: `held` 0.04 to 0.00. Three parts that each deliver
their own capacity combine into a system that holds nothing.

### CAVEATS, BEFORE ANY OF THIS IS QUOTED

n=3 on two rods. Every assembly fails the task, so "accuracy is flat" means uniformly bad rather than
equally good. And `v3`'s `shows_working` drop is suspect: the goal elicited more working than the
frame, which is backwards, and the `on_task` proxy is a length threshold that fights `shows_working`
by construction. That orthogonality hole was flagged before the run and it landed where it was
expected to.
