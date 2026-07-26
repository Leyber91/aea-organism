# WORLD 3 — x21 THE CARRY BATTERY. Scoring the sealed opening.

*Run `20260726T213959Z`. 960 calls, 4 containers x 2 lengths x 3 rods, n=4 sequences per cell.*
*Scored against `W3_SEALED_OPENING.md`, sha256 `86d0cd4bd36f2c31`, written before the CARRY stage*
*existed. **Nothing in the sealed opening has been edited, including the parts that lost.***

---

## THE NUMBERS, HONESTLY ACCOUNTED

A sequence that dies mid-way is a **failure of the container**, not a sample to be discarded. Both
accountings are shown because the difference is the finding.

```
                 completed        credited    honest
LENGTH 4
  none            12/12  100%       0.917      0.917
  checkpoint      12/12  100%       1.000      1.000
  conversation    12/12  100%       1.000      1.000
  free            12/12  100%       0.750      0.750

LENGTH 16
  none            11/12   92%       0.727      0.667
  checkpoint      11/12   92%       0.636      0.583
  conversation     8/12   67%       0.875  ->  0.583
  free            11/12   92%       0.091      0.083
```

**`conversation` completed two thirds of its sequences where everything else completed 92%.** Its
apparent +0.148 win is survivorship: it was credited only for the sequences that survived a context
growing every step until calls stopped returning. That collapse IS the container's cost.

---

## THE PREDICTIONS, SCORED. 3 of 4 held, and the one that lost was the headline.

### PREDICTION 1 — `CHECKPOINT` is the second real lever. **LOST.**

Claimed **>= +0.20** at length. Measured **−0.091 credited, −0.083 honest**. It made things slightly
worse. The only p-value in the project does not reproduce as a lever on a different task.

### PREDICTION 2 — `CONVERSATION` disappoints on short tasks. **HELD.**

+0.083 at length 4, inside the band. But held for the wrong reason: I argued it would never pay
because short tasks have no history. It also does not pay at length once the accounting is honest.

### PREDICTION 3 — free form is ACTIVELY HARMFUL. **HELD, and it is the largest effect ever measured here.**

**−0.167 at length 4 and −0.636 at length 16.** Nine of eleven sequences destroyed. It gets worse with
length, which is the signature of a container that compounds.

### PREDICTION 5 — a creature nothing carries. **HELD on honest accounting.**

`nemotron-3-ultra-550b` at length 16, all four containers, n=4 each: none **1/4**, checkpoint **0/4**,
conversation **1/4**, free **1/4**. It fails without help and no container reaches it.

*(The script scored this LOST because it credited conversation's survivorship 1/2. The honest
accounting reverses it. Recorded here rather than silently corrected in the script's output.)*

---

## WHAT THIS ACTUALLY FOUND

**NOT ONE CONTAINER IMPROVES A SEQUENCE, AND ONE DESTROYS IT.** At honest accounting, length 16:
none 0.667, checkpoint 0.583, conversation 0.583, free 0.083.

**The retention gradient does not explain it, and that is the interesting part.** Order the containers
by how much they retain — none keeps one number, checkpoint keeps a number and a step count,
conversation keeps everything — and the results do not follow. But **free form is far worse than
keeping nothing at all.** So a self-authored summary does not merely lose information, it **injects
noise**: the rod's note to itself is actively worse than no note. That is World 3's toxic creature and
it is the strongest thing this run produced.

**THE SEALED OPENING PREDICTED THIS SITUATION BY NAME.** Section 5, written before any call:

> *If `CHECKPOINT` comes back inert at power, then the only p-value in the project was one task on one
> chain length, World 3 has nothing that carries just as World 2 has nothing that repairs, and two
> consecutive worlds are named for faculties their components do not deliver. That would stop being a
> run of bad luck and start being a finding about the architecture itself.*

That is now the standing hypothesis. It is not yet established — see below.

---

## WHY THIS IS NOT YET A FINDING. Three limits, all real.

**1 · THE BASELINE IS TOO HIGH.** `granite4.1:3b` scored 4/4 and `llama-3.1-8b` 3/3 at length 16 with
**no carry at all**. Two of three rods never drift, so there is nothing for a memory aid to repair and
every pooled margin is driven by one rod. **You cannot measure a memory aid on a task the rods can
already hold in their heads.**

**2 · SIXTEEN STEPS IS NOT FIFTY.** C-80's receipt is a 50-step chain. This ran 16 because 50 steps x
4 containers x 3 rods x n=4 is 2,400 calls. The length where drift begins may simply be past where
this run stopped.

**3 · n=4 SEQUENCES PER CELL.** Twelve per container per length. The direction is clear; the size is
not.

---

## WHAT x22 MUST DO DIFFERENTLY

**Raise the difficulty until the baseline fails.** A memory experiment on a task nobody forgets
measures nothing. Either longer chains, or larger numbers, or operations that cannot be held in one
token of state.

**Price `conversation` by completion, not by accuracy.** Its real behaviour here was not "it helps" but
"it stops finishing." That is a creature — one that carries everything and collapses under the weight
of it — and it needs a receipt at proper n.

**Keep both accountings in the script.** The credited/honest split is the whole reason this run's one
apparent win did not survive, and it is now the tenth instrument defect of the project: a container
that drops sequences must not be credited for the ones that survive.
