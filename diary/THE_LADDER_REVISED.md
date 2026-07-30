# THE LADDER, AFTER OPPOSITION AND EVIDENCE

*2026-07-30. Luis: "I see you are supporting the idea but I don't see you opposing the idea, and
then a third role that analyses the evidence and finds a way."*

*He was right. I wrote `THE_WIRING_LADDER.md` as an advocate, recommended it, and never ran an
adversary at it - while R7 of that same ladder says a plan should survive an adversary before it
executes. So the council was convened on my own plan, and then the claims on both sides were
measured. Transcript: `state/council/runs/20260730T045230.json`.*

---

## WHAT THE ADVERSARY GOT RIGHT

**1. There is a missing rung between R1 and R2.**

> *"R1 outputs a string; R2 expects a validated tool call. There is no rung for parse, validate,
> map string -> tool schema. That gap swallows the schedule."*

Correct, and it is my error. R1 delivers prose, R2 assumes structure, and the translation between
them is neither trivial nor scheduled. **New R1.5: the decision is PARSED into a candidate tool call
and validated, with invalid ones logged as receipts rather than swallowed** - and at first it may
validate and then do nothing, which is a rung you can ship and watch.

**2. Read-only tools produce observations, not outcomes.**

> *"R3 'store outcomes' assumes R2 produces outcomes - but read-only tools produce observations."*

This one is sharper than anything I wrote. R3's gate was *"a tick where it did not repeat something
it had recorded as failing"* - and a read-only tool call barely fails in a way that teaches
anything. **R3's gate is wrong as written.** Corrected: the outcome to store is *"did what came back
match what I predicted"* - which a read-only call absolutely can answer, because the prediction is
the thing being tested, not the tool.

**3. The timeline was optimistic.** I said ~3 weeks at 10h/week for R0-R7. The adversary said 10-20x
off. Both are guesses; mine was the more motivated one. R0-R3 is a fortnight and I will not put a
number on R5-R7 until R3 is running.

---

## WHAT THE EVIDENCE REFUTED

The adversary asserted risk without checking it, and the import graph settles both claims.

**"Touch the dispatcher and you will find imports reaching into the 113." FALSE.**

```
the two loops import 9 modules directly, and ZERO of them are dark
ZERO of the 113 import the loops - no hidden reverse dependency
76 of 116 are imported by NOTHING AT ALL - leaf scripts, not dependencies
60 of the 113 live in aea.lab - it is an experiment drawer, not dark matter
```

The dependency surface of the two loops is nine modules and it is clean. **This was the adversary's
central structural objection and it does not survive contact with the graph.**

**"The 9 gated tools are a mirage, none of it exercised." FALSE, and the truth is better.**

```
gather_public         level 1   62 runs    4 fails
reason_private_local  level 2   56 runs   36 fails
produce_brief         level 2   50 runs   34 fails
speak                 level 2    2 runs    0 fails
```

The path is exercised, recorded, and dated - including entries reading `ok tool:json_get`.

---

## WHAT NEITHER OF US FOUND, AND IT CHANGES THE PLAN

**The graduated autonomy mechanism I was designing gates for already exists**, in
`aea/kernel/trust.py`, populated and running:

```
0 FORBIDDEN  never
1 DRAFT      may produce the artifact; a human approves before anything leaves
2 WATCHED    may act autonomously; HADES verdict on EVERY run; failure -> demote to 1
3 TRUSTED    may act unattended; still logged; failure -> demote to 2

GRADUATION: level N -> N+1 after `promote_after` consecutive clean runs at N.
```

And the dangerous capabilities are already where I said they should be, without my help:

```
draft_outbound   1 DRAFT      0 runs
send_outbound    0 FORBIDDEN  0 runs
self_modify_code 0 FORBIDDEN  0 runs
spend_money      0 FORBIDDEN  0 runs
manage_keys      0 FORBIDDEN  0 runs
```

**And I nearly reported a disaster that is not one.** `reason_private_local` shows 36 fails in 56
runs, and I was one sentence from telling Luis the wake's reasoning step fails 64% of the time -
which would have killed R1 on false evidence. Reading the entries stopped it:

```
2026-07-21 18:30 FAIL -> DRAFT
2026-07-21 18:00 FAIL -> DRAFT hades=unverified sections_ok=False
```

`FAIL -> DRAFT` is **a demotion, not a crash.** Those 36 events are the containment mechanism firing
and correctly dropping a capability's privilege when HADES refused to verify its output. **The
failure count is the safety system's success count.** Fourth instrument error of the session, caught
one step before it became a decision.

---

## THE REVISED LADDER

The gates are no longer invented. **Each rung is a capability reaching a trust LEVEL**, using the
mechanism that is already there.

| rung | wire | gate - the existing ledger, not a new rule |
|---|---|---|
| **R0** | the wake becomes a tick inside `live`; one process, one heartbeat | 72h unattended, clean TERM |
| **R1** | `choose_action` reads the wake's decision; the if/elif ladder stays as the floor | one tick chosen differently, zero crashes |
| **R1.5** | *(new, from the adversary)* the decision is PARSED and validated against `hands.schema()`, and does nothing else | 50 ticks: valid parses logged, invalid logged as receipts, none swallowed |
| **R2** | the validated call EXECUTES, read-only five only | `gather_public` promotes 1 -> 2 on its own streak |
| **R3** | store `(predicted, called, returned, did it match)` | a tick where a prediction was wrong and the next one differed |
| **R4** | `sense()` may issue one search it chose | a week of non-duplicate queries |
| **R5** | research: hypothesis -> sources -> verdict, numeric stop | five runs, one hypothesis DIED |
| **R6** | reflection, stored with pointers to sources | a reflection retrieved and its sources walked |
| **R7** | the council on its own plans before acting | one action the council STOPPED |
| **R8** | the drive | **`send_outbound` reaching WATCHED honestly**, plus one recorded decline |
| **R9** | self-modification | `self_modify_code` is FORBIDDEN and stays there |

---

## THE HONEST VERDICT, REVISED

**Smaller than I said, and better founded.** The containment I called untested is built, populated
and demoting things correctly. The dependency risk the adversary called fatal does not exist in the
graph. What is genuinely missing is narrower: a parse step, an execute step, and a prediction stored
next to its result.

**And the method is the finding.** Advocate alone produced an optimistic plan with a hole in it.
Adversary alone produced two real hits and two confident falsehoods. **Only the evidence separated
them** - and it also produced the one thing neither role proposed, which was that most of the gating
was already built. A council without an evidence seat is two rhetoricians; an evidence seat without
a council has nothing to check.
