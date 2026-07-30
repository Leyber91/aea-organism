# WHERE WE ACTUALLY ARE - measured, 2026-07-30

*Luis: "we need to make a recap of where we are. That's very important. And I don't feel that we
did it."*

*He is right that we did not, and a recap written from memory would be the thing he is objecting
to. Every number here is counted from the tree.*

---

## 1 - THE ONE NUMBER

```
130 modules      34,650 lines      12 packages
  17  reachable from something that runs on its own
 113  reachable only if a person types the command
```

**Every single thing built in this session is in the 113.**

```
aea.mind.council        ORPHAN     aea.io.mixer           ORPHAN
aea.mind.persona        ORPHAN     aea.lab.earbench       ORPHAN
aea.lab.party           ORPHAN     aea.io.blackbox        ORPHAN
aea.lab.social          ORPHAN     aea.organs.converse    ORPHAN
aea.tooling.transcripts ORPHAN
```

Luis's own diagnosis, in his words: *"we are actually doing what the autonomous entity
architecture should do. It's just that we're doing it in very separate pieces. It's not a full
organism. It's me talking to you to improve."*

That is not a feeling. It is 113 of 130.

---

## 2 - THE HANDS EXIST AND ALMOST NOTHING CAN REACH THEM

Nine real tools are built and gated: `calc`, `web_fetch`, `json_get`, `read_state`, `web_search`,
`self_map`, `list_tools`, `send_email`, `spend`.

**`hands.invoke` is called by exactly two files: `hands.py` itself, and `converse.py`.**

And `converse.py` is an orphan. So the chain is:

> the entity, running on its own, can call **nothing**.

The tool layer is not missing. The tool layer is unreachable, which is a different problem with a
different fix, and it is smaller.

---

## 3 - DEEP RESEARCH: THE HONEST STATUS

A probe I wrote claimed the repo had a research loop. **It was a false positive** - the pattern
matched the word *hypothesis* inside a comment in `speak.py`. Corrected before it reached this
document, and worth recording because it is the same instrument failure that has run through this
whole project.

What actually exists:

| | status |
|---|---|
| a `web_search` tool | **built**, gated to the public zone |
| a `web_fetch` tool | **built**, announces the URL before reaching it |
| a research PROCESS | **does not exist** |
| hypotheses tracked | **does not exist** |
| findings stored with sources | **does not exist** |

Luis is right. Two deep research passes happened this session - conversation theory, and prior art
on social agents, 116 agents between them - and **both were run by me, from the outside.** The
entity has never researched anything. Neither has the council: it argues from what four rods
already believe, which is exactly the failure it exists to prevent.

---

## 4 - WHAT WAS BUILT, AND WHAT IT IS WORTH

Honest ledger. "Works" means measured, not compiled.

| | state | evidence |
|---|---|---|
| the one-person voice loop | works | fabricated tool calls gone; dead air 4.1s -> 0.32s; a story 43 chars -> 1,076 |
| the ear | works, with limits | 0% WER median from 30 dB to 6 dB against his real room noise; 2 lexical failures survive |
| four voices, one sound card | works | 4 concurrent, realtime 1.0003, separation 0.93-0.97 |
| persistent selves | works | memory / impressions / commitments, separate stores, survives the process |
| the council | works | designed roster, enforced adversary, pairwise overlap 0.04-0.07 |
| transcripts | works | one file per run, a reader, a local page |
| **anything calling any of it** | **does not exist** | 113 orphans |

The lab has **60 modules**. The diary has **~78,000 words**. Discovery D7 recorded a 110:1
words-to-code ratio as the project's standing failure mode, and this session added roughly 25,000
words of diary against nine new modules. **The ratio did not improve.**

---

## 5 - THE PRINCIPLE LUIS NAMED, WRITTEN DOWN

In his words: *"you have a good idea, then you do the investigation, the deep research of all the
different sources, then summarize them, and you see if the hypothesis that you did at the beginning
are possible or not. And if you need to develop a new hypothesis that takes you to a new research,
then you will do another research. But it's not that you do infinite deep researches. You do until
you find a solution that might meet your purpose."*

That is a loop with a termination condition, and neither the entity nor I have it written down:

```
1  STATE THE HYPOTHESIS      falsifiable, in one sentence, before looking anything up
2  RESEARCH IT               many sources, and the sources are KEPT with what they said
3  SUMMARISE AGAINST IT      not "what did I learn" - "does the hypothesis survive"
4  THREE OUTCOMES, only three:
     SURVIVES   -> act on it, and say what would still falsify it
     DIES       -> record what killed it. A dead hypothesis is a result, not a failure.
     FORKS      -> the research produced a BETTER question. Restate it and go to 1.
5  STOP WHEN    the purpose is met, or the budget is spent, or two rounds produce no new fork.
                NOT when everything is known. That is the "not infinite" clause and it is the
                part that has to be a number, or it will be a feeling.
```

Two properties make this different from "search the web and summarise":

- **The hypothesis is written first.** Research without a prior hypothesis produces a summary of
  whatever was findable, and a summary cannot be wrong, which means it cannot be useful.
- **A dead hypothesis is an output.** This project has already paid for the opposite habit: three
  of four gains reported in this session were inside the noise floor, and the only reason that is
  known is that something was measured against a stated expectation.

**And it must feed the council, or the council is four rods arguing from priors.** The order is
research first, then argue about what was found. Not the reverse.

---

## 6 - THE PUSHBACK

Luis asked to be debated, so:

**Deep research is the right principle and the wrong next build.** Adding a research organ to this
tree makes it orphan number 114. The measured problem is not that the entity cannot research - it
is that the entity cannot START ANYTHING. A better brain wired to nothing is the same distance
from an organism as no brain at all, and this repo has now demonstrated that four separate times in
two days.

**The smallest thing that changes the number is one loop that calls one tool on a schedule and
writes what happened.** Not a good loop. One. Everything else already exists and is waiting behind
that.

**On money:** the council's own held seat already answered, and I agree with it over any plan I
would have written: *"The council of experts, cross-session memory, and tool-calling are all
distractions. With 20 hours total, you cannot build and validate a product - you can only test one
hypothesis... The tech is a trap; the only signal is someone handing over cash for a result."*
An app that makes money is a hypothesis. Under section 5, it gets researched before it gets built.

**One thing I do not know:** the comparison to "OpenGlow" - I do not recognise that name and will
not pretend to. If it is a real product whose success we should study, name it again and it becomes
research question one, which is exactly the loop working.

---

## 7 - WHERE WE ARE, IN ONE PARAGRAPH

The entity can hear a person, hold a conversation, remember them across sessions, tell the truth
about what it is, call nine real tools, run four distinct personalities that hold apart under
measurement, and convene a council that genuinely disagrees with itself. **None of that is wired to
anything that runs.** The voice work is finished enough to stop; the council is the useful organ and
it argues from priors because nothing researches; and the single measurement that describes the
whole project is 17 against 113.
