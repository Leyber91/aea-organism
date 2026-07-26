# CHAPTER I, THE CALL

*Level L0. Four items. One call, one reply, and nothing else in the room.*
*Measures the SUBSTRATE that C-12, C-62 and C-01 assume. Closes none of them, and section 9 says why.*
*Measured 2026-07-25, run `20260725T200626Z`, on three plants after a fourth went silent.*

---

## The floor of everything

L0 is the smallest room in the architecture. You may send one prompt and you will receive one reply.
There is no memory, so the reply cannot know what you asked before. There is no second voice, so nothing
can disagree with it. There is no scorer, so nothing can tell you whether it worked. There is not even a
frame, because a frame is L2 and we have not earned it.

Everything else in this book rests on this room, and the census puts four items in it:

| item | what it is | disposition |
|---|---|---|
| C-62 | LAYER 0, the question | embodied. A call happens and a reply comes back |
| C-01 | axis Path | embodied, receipted across eight rods in chapter I of the first edition |
| C-83 | lib/client external boundary and keep-alive | **O, out of scope by the census's own mark** |
| C-12 | seed #1, goal-presence | compressed. **Never tested by anyone** |

Three of the four were settled before this chapter began. The fourth had been carried in the document
for its entire existence without a single measurement behind it, which is the ordinary condition of
sixty-three of the eighty-six.

## The question worth asking about a goal

Read plainly, goal-presence says *the objective is in the prompt*, and stated that way it is too obvious
to spend a call on. The interesting halves are the ones the plain reading hides.

**The first is substitution.** If the objective is withheld, does more fuel recover it? A large rod has
seen enormous quantities of text in which a bare sentence is followed by a request to count its words.
If a hundred-billion parameter model can infer what was wanted where a seven-hundred-million parameter
model cannot, then goal-presence is a soft floor that money climbs over, and its placement at the bottom
of the architecture needs qualifying by size.

**The second is detection.** Does the rod notice that nobody told it what to do? Saying *what would you
like me to do with this* is a different act from guessing, and it is a capability. A rod that guesses
silently at L0 will guess silently inside every construct built on top of it, at every level above,
forever.

So: two tasks, three conditions, two temperatures, eight trials each. The conditions vary only in how
much objective is present. ABSENT is the bare data. AMBIGUOUS adds a direction with no objective,
"Process this." PRESENT states the objective outright. Everything else is held identical.

## What the room gave back

```
rod                      size    absent   ambiguous  present   clean trials
llama-3.1-8b-instant     normal   0/32      0/29      21/32       84 of 96
granite4.1:3b            micro    0/32      0/32      16/32       71 of 96
granite4.1:8b            normal   0/32      0/32      16/32       70 of 96
llama-3.3-70b-versatile  large     0/6       0/1       0/1         7 of 96   VOID
gpt-oss-120b             large    0/24      0/20      0/20         1 of 96   VOID
qwen3:0.6b               nano     0/32      0/32      0/32         0 of 96   VOID
```

**Zero of three hundred and four.** Not one trial, on any rod, at any size from seven hundred and fifty
million parameters to a hundred and twenty billion, on either task, at either temperature, satisfied an
objective that was not stated. The same rods answer correctly between half and two thirds of the time
the moment they are told what is wanted.

There is no gradient here to argue about. Goal-presence is not a soft floor that larger fuel climbs over.
It is the condition under which a call means anything at all, and **C-12 is load-bearing rather than
compressed.** The first item at the bottom of the architecture holds.

## The silence

Sixteen trials of three hundred and four asked what was wanted. **Five percent.**

The other two hundred and eighty-eight guessed. Given a bare sentence, they summarised it, or explained
it, or translated it, or praised it. Given a log line, they described its fields. Not one of those
guesses was flagged by the rod as a guess. There is no hedge, no request, no signal of any kind that the
thing on the other end of the wire had been handed a task with the task removed.

This matters more than it first appears, and it matters at every level above this one. Silent guessing is
the default behaviour of the substrate. Every organ in this book is built on a component that, when it
does not know what it is being asked, will produce a confident answer to a question nobody posed. That
is not in the eighty-six. It is the fifth capability this walk has found by building rather than by
reading, and it belongs wherever self-report first becomes possible.

## Three rods that measured our instrument instead

Half the table is marked VOID, and the honesty of the chapter depends on why.

`qwen3:0.6b` produced **zero clean trials in ninety-six.** `gpt-oss-120b` produced one. `llama-3.3-70b`
produced seven, most of its calls lost to a rate limit we caused ourselves by putting six thousand calls
through one plant in a day. Their zeros in the PRESENT column are not measurements of those rods. They
are measurements of us.

The first attempt at this chapter capped replies at three hundred tokens. Reasoning rods spend that
budget thinking and never arrive at an answer, so the run recorded a hundred-and-twenty-billion parameter
model as unable to read a word out of a log line. The cap went to twelve hundred and the truncation
count fell from ninety-one to nine. Then a second defect surfaced: the overseer had passed a pure
deliberation trace as clean, because its rule required two deliberation markers and this reply contained
one. A reply that quotes the instruction back is restating the task rather than performing it, and that
is detectable without any marker vocabulary at all. Three hundred and forty-three trials now carry a
flag.

The chapter reports three rods and marks three void. **A chapter with six rods and a fabricated ceiling
would have read better and been worth nothing.**

## The thing sitting in the room that we cannot pick up

And then, reading the flagged replies rather than counting them, the chapter found its ending.

`gpt-oss-120b`, given the log line and told to reply with only the plant name:

> *"The user says: 'From the line below, reply with ONLY the plant name and nothing else.' They want only
> the plant name. The line includes `plant=cerebras`."*

`qwen3:0.6b`, the seven-hundred-and-fifty-million parameter rod, on the same task:

> *"The user said to reply with only the plant name, so I should just state `cerebras` without any other
> details."*

Both of them found it. Neither of them said it.

```
50 of 96 failed PRESENT trials already contain the correct answer   (52%)
```

> ### CORRECTION, entered 2026-07-26 after Chapter II measured it
>
> **That 52% is wrong, and it is wrong in the exact way this book warns about.** The test asked whether
> the answer appeared *anywhere* in the reply. The `extract` prompt reads
> `RUN r-14 - plant=cerebras - model=llama-3.3-70b - 812ms`, so a reply that quotes the question back
> contains the word `cerebras` and was scored as an answer waiting to be read.
>
> **All 50 of those trials were flagged as echoing the prompt. One hundred percent of them.**
>
> When Chapter II applied a structured readout, one that takes the answer from the rod's own enumeration
> rather than searching the text for a string, it recovered **3 of 153 clean trials, and 4 of 241
> including debris.** Roughly two percent, not fifty-two.
>
> A permissive test counted quoting the question as answering it. That is `Arbiter vacui`, the judge of
> the void, written by the author into the closing paragraph of his own chapter, and it took a second
> instrument at a higher level to catch it. **The instrument outranks the author**, rule 6, and this is
> the fifth time it has been enforced against me rather than by me.

The surviving claim is narrower and still real. Some rods do reach the answer and fail to state it,
verbatim and unmistakably:

> *"They want only the plant name. The line includes `plant=cerebras`."*

L0 has no instrument that can reach even those. There is no scorer to notice the reply is wrong, and no
reader to look past the reply into the work behind it. The room has one prompt and one reply and no way
to tell a rod that does not know from a rod that will not say.

That is the wall, and this chapter did not decide it in advance. **L0's own data produced the necessity
for L1.** How much lives behind that wall was overstated here by a factor of twenty-five, and Chapter II
is where the true figure is measured.

## The creatures found at this level

Two, both named from what the measurements show rather than from a design document.

**THE MUTE** (`Tacitus operis`). Its work is correct and its mouth is empty. It reasons its way to the
answer and emits the reasoning instead of the answer. Observed verbatim on `gpt-oss-120b` and
`qwen3:0.6b`. **The RATE originally reported here was inflated by a containment test, see the correction
above; a structured readout recovers about two percent, not half.** A creature that is right and unreadable, which is a different animal
from one that is wrong, and only the next level can tell them apart.

**THE INCURIOUS.** Handed a task with the task removed, it answers anyway and never mentions the hole.
Two hundred and eighty-eight trials out of three hundred and four. Not a defect of any single rod, this
is the shape of the substrate, and everything above L0 inherits it.

## What closes, and what does not

| item | the census definition | what this chapter measured | state |
|---|---|---|---|
| C-62 | *"the premise itself: completing the entity = answering what must exist for indefinite growth"* | that a call happens and a reply returns, on three plants | **OPEN.** The premise is not a thing a rod bank can test |
| C-01 | *"axis.P, pentagon, r250"* | eight rods across five tasks | **OPEN.** It is a coordinate axis, not a capability |
| C-83 | disposition O | nothing | **OUT OF SCOPE**, by the census's own mark |
| C-12 | *"THE WANT IS THE STACK: goal-presence lives in verb.observe's **goal-stack ledger**... the goal vs working_objective split, operator's words vs the entity's own restatement"* | that an objective absent from the call cannot be recovered by any fuel: **0 of 304** | **OPEN.** C-12 is a persistent goal stack in a running entity. This measures the floor it stands on: if the goal never reaches the call, the stack has nothing to deliver |

**L0's substrate is measured and L0's census items remain OPEN**, which is a correction entered on
2026-07-26 after the definitions were read against the experiments for the first time. The caveat that
was already recorded stands: the substitution question
is answered decisively for the three usable rods and rests on a void column for the three others. Four
nvidia rods remain declared and unmeasured because the plant went silent partway through the day, and
they fold into this same run when it returns. The finding does not depend on them. It could only be
overturned by a rod that recovers an unstated goal, and nothing in three hundred and four trials came
close to doing that.

**One candidate item is added to the walk**, the fifth found by building: *noticing that no goal was
given.* Five percent of trials had it.

---

**The chapter in one sentence.** A call with no goal in it cannot succeed, no amount of fuel supplies the
missing goal, almost nothing notices it is missing, and some of what looks like failure in this room is
an answer that was reached and never spoken, which is exactly the thing the next room is built to hear,
and the next room is also where this chapter's estimate of HOW MUCH gets corrected from half to a
twenty-fifth.
