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

| module | added | subtracted | receipt |
|---|---|---|---|
| `validation` | can_abstain | **all accuracy on a rod that was already right.** 7/7 to 0/7, three times | x17 |
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
end to end. The capacities are not:

```
v1 call          answ 1.00                     held 0.07  show 0.26              drift@2.0
v2 +goal         show 0.26 -> 0.57             held 0.08                         drift@2.0
v3 +frame        show 0.57 -> 0.38   COST      held 0.04                         drift@1.5
v4 +readout      reco 0.00 -> 0.54   show 0.54 held 0.12   <- THE PEAK           drift@1.5
v5 +validation   can_ 0.00 -> 0.61   COST reco -0.404      held 0.04             drift@1.5
v6 +critic       revi 0.00 -> 0.74   COST can_ -0.607      held 0.04             drift@1.5
v7 +carry        held 0.04 -> 0.00   COST show -0.327      revi 1.00             drift@1.0
v8 +measure      not delivered                                                   drift@1.0
```

### THE ARCHITECTURE IS NOT MONOTONIC

**v4 is the best organism on this task and it is four parts, not eight.** It carries the widest set of
live capacities — answered, on_task, shows_working, recoverable — and the **highest retention on the
whole ladder at 0.12**, above the bare call and above every assembly larger than it.

Everything above v4 trades one capacity for another, and above v6 it trades for nothing at all. The
drift point moves *earlier* as parts are added: step 2.0 at v1, step 1.0 at v8.

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
| `v4` +readout | the widest competence and the best retention. The peak |
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
