# CHAPTER II, WHAT STAYS

*The question: when the fuel changes, is it still the same entity?*
*Opens on the instrument's ceiling. Closes C-80, and demotes a rung nobody expected to demote.*
*Propositions locked 2026-07-25 before any experiment was designed. All three are now resolved.*

---

## 0 · The instrument ran out of range

Chapter I ended by building a measuring device and pointing it at eight rods, from a one-billion parameter
model to a five-hundred-and-fifty-billion one. Five tasks, eight trials each, no help of any kind. The
table it produced is the reason this chapter exists, and it is not the table I expected.

```
ROD                        wordcount  batball   lilypad   machines  strictjson
llama-3.2-1b               0/8 F      8/8 S     0/8 F     0/8 F     8/8 S
llama-3.2-3b               0/8 F      8/8 S     8/8 S     0/8 F     8/8 S
nemotron-nano-9b           8/8 S      2/8 W     8/8 S     6/8 W     8/8 S
gpt-oss-20b                8/8 S      8/8 S     8/8 S     8/8 S     8/8 S
llama-3.3-70b              0/8 F      8/8 S     8/8 S     8/8 S     8/8 S
mistral-small-119b         0/8 F      6/8 W     2/8 W     8/8 S     8/8 S
nemotron-3-super-120b      7/8 S      8/8 S     8/8 S     8/8 S     8/8 S
nemotron-3-ultra-550b      8/8 S      8/8 S     7/7 S     8/8 S     8/8 S
```

The bottom two rows are solid. **The 550b saturates every task in the bank. So does the 120b.** And every
organ chapter I measured, the frame, the critic, the ladder, the recall, is defined by what it does to a
failure. On a rod that does not fail, an organ can only add cost. Read literally, the table says the
architecture has nothing to offer the best fuel available, and if that is true this book has no subject.

It is worth sitting with that rather than hurrying past it, because it is the strongest argument against
the whole project and it arrived from our own instrument.

**But look at what the five tasks have in common.** Count the words in a sentence. Find the trick in the
bat and the ball. Halve the lily pads. Rate the machines. Emit one JSON object. Every one is a single
call, with no state, no second voice, no elapsed time, and an answer a regular expression can confirm in
one look. They are the tasks you can check cheaply, which is exactly why they were chosen, and cheap
checkability turned out to select with perfect precision for **the tasks that need no architecture at
all.**

A test on which the top three candidates all score full marks has not ranked them. It has run out of
range. The honest reading is **our instrument has no resolution above twenty billion parameters, and
every claim chapter I made lives below that line.**

So this chapter's first job was not to defend the architecture. It was to build a task the 550b cannot
pass alone, and to accept the verdict if no such task existed.

## 1 · The three claims, and what would have killed each

### Claim 1, the ceiling belongs to the instrument rather than to the architecture

*There exists a class of task on which the 550b, unaided, fails, and on which a construct built from small
fuel plus the right organs succeeds.*

**FALSIFIED IF** no such task can be built without smuggling. The smuggling has a precise name: hide
information from a model and then observe that the one with memory wins proves only that storage stores.
The task must be one where the big rod has everything it needs in its context and still loses.

### Claim 2, continuity is the axis the architecture lives on

*State written on one fuel can be read and continued on another, and the construct that results is
recognisably the same construct.*

This is C-80, recorded by the census as EMBODIED, found by `grep -rl checkpoint aea/` in zero files.
Thirty-five separate JSON files stand in its place, each written alone and read alone.

**FALSIFIED IF** a checkpoint written by one rod cannot be continued by another.

### Claim 3, a council can reach above its own fuel

*Several small rods under a protocol reach an answer that one small rod does not.*

**FALSIFIED IF** a council of small rods does no better than its best single member.

## 2 · The two laws this chapter inherits

**Law I, a capability pays only when its precondition holds.** Three of chapter I's four laws collapsed
because each was measured on rods that did not need the organ under test.

**Law IV, the architecture is not fuel-independent.** One composition produced four verdicts across five
rods. *The AEA is sixty percent complete* has the grammar of *the rod is four long*.

And a correction this chapter's data forces: **size is not the variable, family is also.** Later
measurement pushed that further than a correction. See section 4.

## 3 · Two methodological rules adopted before the first experiment

**Await, never a deadline.** A rod that thinks for ninety seconds before its first byte is slow rather
than broken, and a fixed timeout records it as a failure. Nothing in this chapter is to be cut short by
our own impatience.

**A council waits for every voice.** A three-voice debate that proceeds with two voices had a quieter
debate, and every conclusion drawn from it silently inherits a missing participant.

*Both rules were broken during the chapter. Section 7 records how, because a rule stated and then violated
by its own author is worth more as a receipt than as an intention.*

---

## 4 · CLAIM 1, RESOLVED: failed in general, confirmed narrowly, then confirmed again from a new direction

**The general form failed.** `gpt-oss-20b` holds a fifty-step arithmetic chain in a single call and
answers 8/8, and it holds two hundred steps. There is no length at which a small construct beats it on
this task, because it does not fail. The claim as written, that there exists a task where the best fuel
fails and small fuel plus organs wins, was not demonstrated.

**The narrow form was confirmed, and it is the one that matters.** On a rod that *does* drift, carried
state repairs it:

```
nemotron-nano-9b, fifty-step chain
  one breath      9/16
  carried state   11/11          Fisher exact p = 0.0216
  cost            50x calls, 4.5x wall clock
```

That is the architecture doing precisely what it claims, on stated fuel, with the price named. It is not
a claim about all fuel and it was never going to be.

**Then a second experiment confirmed it from a direction nobody planned.** Sweeping eleven rods across
four temperatures and three plants on one task produced this:

```
groq/llama-3.3-70b      bare 0.00 at ALL FOUR temperatures
mistral-small-119b      bare 0.00 at three of four
nemotron-nano-9b        bare 1.00
gpt-oss-20b             bare 1.00
```

**A seventy-billion and a hundred-and-nineteen-billion parameter rod fail what a nine-billion rod does
perfectly.** The correction in section 2 said family matters as well as size. This says something
stronger: **capability on a given task is not ordered by size at all.** Reaching for a bigger rod is not
a strategy, it is a guess. The ceiling is per task and per rod, and the only way to know it is to measure
from outside.

Which closes a placement that was previously a judgement call. Asked "will you get this right?" before
the attempt, five rods across five tasks were honest on the cells they failed **zero times out of
twelve**. A rod cannot see its own ceiling, and now we know you cannot infer it from its size either. The
calibration table is load-bearing.

## 5 · CLAIM 2, RESOLVED: state crosses fuel, and the form decides what state can be

The first test handed a checkpoint from one rod to another halfway through a fifty-step chain, in both
directions, four arms, sixteen hundred calls. Every arm scored 100%, and the fuel trail on each artefact
records two rods. State crossed fuel with no measurable loss.

**And the result was almost worthless, because the checkpoint held an integer.** Any rod that can read
`-3` can double it. There is no interpretation step to fail. The question had been answered in the one
form where it could not have come out any other way.

So it was asked again with the state holding **working notes in the rod's own phrasing**: six boxes,
thirty events, two thirds of them referential so the state is load-bearing at every step, graded zero to
six per box, roughly two thousand calls.

```
                       per-box  final-note chars (min/med/max)  cap hits  crossing
canonical, 4 arms       1.00         81 / 81 / 81                  0-1     6.0 -> 6.0
free-form, 4 arms    0.52-0.71     117 / 1020 / 4801              32-53    5.12 -> 5.25
```

The canonical note is **eighty-one characters, identical in every trial**, bounded by construction. The
free note reaches **four thousand eight hundred and one characters**, and reading it shows what it
actually contains:

> *"We need to produce final notes. We need to decide rule for conflict when moving a box to an occupied
> shelf... But we don't know if shelf 1 was occupied. We need to decide rule... Wait, the earlier event."*

The rod's working notes became a transcript of its own uncertainty, including a shelf-conflict rule the
task never posed. Given a free form it wrote down its reasoning *about* the state instead of the state,
invented a problem, and ran out of budget. **Every free trial hit the token cap at least once. Almost no
canonical trial did.**

**So the answer to the chapter's title question is: whatever the form forces to be written.** A declared
shape admits state and nothing else, and survives a fuel change intact. A free shape admits deliberation,
which grows without bound and then truncates. That is the property C-80 has to hold. Persistence is not
enough and legibility is not enough. The vessel has to constrain what can be poured into it.

**Two details that the integer version could never have shown.** First, the cost is not at the crossing:
handing prose notes from the 9b to the 20b went 5.12 to 5.25 out of six, so the incoming rod read another
rod's phrasing and did not degrade it. The loss is continuous across all thirty steps. Second, the
crossing is **directional**: handing down to weaker fuel went 5.5 to 4.5 while handing up cost nothing. An
integer handoff is symmetric because a number carries no interpretive burden.

## 6 · CLAIM 3, RESOLVED: a council selects, it cannot generate

Four arms on the fifty-step chain, and the comparison chosen so it could fail. A council beats the average
of its members trivially, so the discriminating test is whether it beats its **best** member, and whether
that is worth N times the calls.

```
A  SOLO                 best member gpt-oss-20b at 1.00
B  SELF-CONSISTENCY     9b  1/8 -> 4/8   (one rod, five samples, majority)
C  CROSS-ROD COUNCIL    8/8, tying the best member, at 5x the calls
D  PEER DEBATE          6/8 -> 8/8, nine minds changed
E  WEAK COUNCIL         0/8, three rods that ALL fail solo
```

Arm C is the headline and it is negative. A mixed council ties its best member and costs five times as
much, which means it solved a rod-selection problem. Ceiling-detect against a calibration table already
solves that for one cheap call.

Arm E is the one that explains why. Three rods that never solve the chain voted eight times:

```
vote 0  [4, 428515, 49]        vote 4  [3, 142, 49]
vote 1  [-15, 8, 49]           vote 5  [4, 13, 49]
vote 2  [50, 8, 49]            vote 6  [5, 10, 49]
vote 3  [-5, 7, 49]            vote 7  [7, 8, 49]

twenty-four values across twenty-four calls. The truth, -17, appeared ZERO times.
```

No majority ever formed. **A council cannot create a signal no member produced.** It can only select one
that already exists, which is exactly why self-consistency worked: the 9b does sometimes reach the answer,
and voting over five samples surfaces it. Voting over three rods that never reach it surfaces nothing.

That demotes the rung. THE COUNCIL is a selection instrument sitting in a position the path implied was a
capability gain. The cheapest form of it, one rod voting with itself, is also the only form that improved
anything, and it costs five calls rather than five rods.

Note the third column of every ballot. The one-billion rod returns **49 every single time**, deterministic
and wrong. No amount of voting rescues a rod that is confidently identical.

## 7 · What the chapter cost, including the rules it broke

Rule 6 of the walk is that the instrument outranks the author. Here is where it did.

**Both methodological rules in section 3 were violated by the author who wrote them.** *Await, never a
deadline* was stated before the first experiment. The council run was then launched under a wall-clock cap
that exceeded the harness maximum, and it was killed at ten minutes with **four completed arms held in
memory and never written to disk**. The remedy was not a larger cap. Evidence is now written the moment
each arm completes, so a killed run resumes rather than restarts. *A council waits for every voice* was
violated in the same run: one member returned one call in eight under a rate limit we caused by hammering
the plant, and its silence was nearly recorded as the rod being bad.

**Four defects were found in our own instruments, none in the rods.** A yes/no parser read "YES and NO" as
YES, biasing rods toward looking dishonest in the exact direction that flattered the placement under
test. A token cap cut free-form notes in a third of all step calls and the loss was charged to the
representation. `n=8` turned out to be `n=1`, because a deterministic endpoint returned byte-identical
replies in eleven of twelve cells, and the floor that was supposed to guarantee power guaranteed nothing.
And the lab was measuring at temperature 0.0 while the product fires at 0.2, so it was not measuring the
product.

That last pair killed a claim that had already been written down: a posture frame appeared to convert one
rod at 8/8, and at the temperature the product actually uses it is 5/8 against 3/8 bare, inside noise by
the harness's own threshold. One lucky deterministic sample had been promoted to a measured conversion.

**The pattern is worth more than any individual fix.** Every defect was found by auditing an instrument
rather than by a rod failing, and each one had already produced a written conclusion. A `grep -c
temperature`, a distinct-reply count, and a token-cap check are one line each.

---

## 8 · The chapter in one sentence

Chapter I measured what the architecture does to a model that fails and found the best fuel never failed
at anything we knew how to ask. Chapter II built tasks it does fail at, and found three things: **the
ceiling is real but it is not ordered by size**, **state crosses fuel intact only in a form that
constrains what can be written into it**, and **a council amplifies a signal rather than creating one.**
The entity that survives a change of fuel is the one whose memory has a shape.
