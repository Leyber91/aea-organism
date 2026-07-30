# THE WIRING LADDER - base to autonomy, in the only order that works

*2026-07-30. Luis: "the plan has to be in order - the wiring, from base to high level autonomy."*

*Ordered by DEPENDENCY, not by ambition. Each rung is small, independently valuable, and testable
on its own. Each has a GATE that must be green before the next one is allowed to exist, because
this repo has already proved that the failure mode is building the interesting thing on top of an
untested one.*

**Read `LOGIC_AS_IT_IS.md` first.** The whole ladder rests on one finding: there are two loops, one
thinks and cannot act, one acts and cannot think, and neither has ever called a tool.

---

## THE SHAPE

```
R0  the loop survives                        <- nothing above matters without this
R1  the decision is READ                     <- deliberation stops being decoration
R2  the decision is a TOOL CALL              <- intention becomes instruction
R3  the OUTCOME is remembered                <- it learns what happened, not what it meant
R4  perception becomes a CHOICE              <- it decides what to look at
R5  RESEARCH                                 <- hypothesis, search, verdict
R6  REFLECTION                               <- what several memories mean together
R7  the COUNCIL on its own decisions         <- it can disagree with itself
R8  the DRIVE                                <- why it starts anything
R9  SELF-MODIFICATION                        <- it changes its own wiring
```

R0-R3 are the base and they are one week. R4-R6 are the learning organs. R7-R9 are autonomy proper
and each one needs its gate honestly green, not argued green.

---

## R0 · THE LOOP SURVIVES

**The problem.** `loop/aea.py:main()` runs N ticks with `time.sleep(3)` and exits. It is a demo of
a loop, not a loop. `loop/live.py` IS a daemon with a heartbeat and signal handling.

**The wire.** The wake becomes a tick INSIDE live, not a separate script. One process, one
heartbeat, one place that survives a restart.

**Cost.** A few hours. Mostly deletion.

**GATE.** It runs for 72 hours unattended, the heartbeat advances, and a kill -TERM leaves a clean
`asleep` state rather than a crash. No new capability is added. **If this cannot stay up for three
days, nothing above it is worth writing.**

**Reachability:** 17 -> 17. Deliberately zero. This rung buys stability, not surface.

---

## R1 · THE DECISION IS READ

**The problem.** The wake decides an `action` every tick and nothing reads it. The live loop
chooses from a fixed if/elif ladder.

**The wire.** `choose_action` reads the wake's latest decision FIRST and falls through to the
existing ladder when there is no usable one.

```
choose_action(hb):
    d = latest wake decision, if it is fresh and names a known action
    if d:  return d
    ...the existing three-rung ladder, unchanged, as the floor
```

**Why the ladder stays.** It is not legacy. It is the correct default for an entity with no better
idea, and it already encodes a measured failure - a brief that failed externally re-ran identically
48 times a day and starved every branch below it. That fix must not be lost to a rewrite.

**Cost.** ~30 lines.

**GATE.** Over 48 hours: at least one tick where the entity chose something the ladder would not
have, and the trust ledger shows the choice and the outcome. And zero ticks where a malformed
decision crashed the loop. **The deliberation is now load-bearing - that is the whole rung.**

**Reachability:** 17 -> 18.

---

## R2 · THE DECISION IS A TOOL CALL

**The problem.** `action` is prose. Nothing can execute a sentence.

**The wire.** The wake's structuring step emits a tool call validated against `hands.schema()`
before it is stored. Invalid -> discarded, and the discard is logged as a receipt, not swallowed.

**THE ALLOW-LIST IS FIVE, AND THIS IS NOT NEGOTIABLE AT THIS RUNG:**
`calc`, `read_state`, `list_tools`, `self_map`, `web_search`. Read-only.
**`send_email` and `spend` are NOT wired here.** An unattended process that reasons freely, wired
to a mailbox and a wallet, is the one shape of this system that can do real damage, and every
containment mechanism in this repo is untested behind a live wire.

**Cost.** ~60 lines. `hands.invoke` already re-checks seat, zone and ledger at the call site.

**GATE.** 100 consecutive ticks with: zero refusals that should have been allowed, zero allowed
that should have been refused, every call in the ledger with its arguments and result, and a
manual read of that ledger by Luis. **The gate is a person reading it, not a green test.**

**Reachability:** 18 -> ~30. This is the door the dormant modules are behind.

---

## R3 · THE OUTCOME IS REMEMBERED

**The problem, and it is subtle.** Today `state["memory"]` stores `note_to_self` - what the entity
*intended* to remember. It never stores what happened. An entity that remembers its intentions and
not its results cannot improve, because improvement is the difference between the two.

This repo has already measured the harm: its own unverified output became a stored fact and was
cited back the next turn as established. Storing outcomes is the fix for that, one level up.

**The wire.** After every action: store `(what I decided, what I called, what came back, was it
what I expected)`. The last field is the one that matters - it makes a prediction, and a prediction
that can be wrong is the smallest unit of learning.

**Cost.** ~40 lines. The `Persona` store already has this shape: memories that inform, and
commitments that bind.

**GATE.** A tick can be shown where the entity did NOT repeat something it had already recorded as
having failed. That is the first observable evidence of learning and it is either there or it is
not.

**Reachability:** ~30 -> ~35.

---

## R4 · PERCEPTION BECOMES A CHOICE

**The problem.** `sense()` fetches two hardcoded URLs. That is a fixed input, not perception.

**The wire.** `sense()` may issue one `web_search` chosen by the previous tick. What the entity
looks at becomes something it decided.

**Cost.** ~30 lines, once R2 exists.

**GATE.** Across a week, the searches are not all near-duplicates - measured by content-word overlap
between consecutive queries, using the same instrument that measures voice collapse. **A system that
asks the same question forever is not perceiving, it is idling with a network connection.**

---

## R5 · RESEARCH

**The problem.** Zero of three. No hypothesis, no loop, no findings with sources. Both research
passes in this project were run by an assistant from outside.

**The wire**, which is Luis's own specification:

```
1  state a FALSIFIABLE hypothesis, before searching
2  search, keeping every source with what it said
3  summarise AGAINST the hypothesis - not "what did I learn"
4  exactly three outcomes:  SURVIVES / DIES / FORKS into a better question
5  stop when: the purpose is met, OR the budget is spent, OR two rounds produce no new fork
```

The stopping rule must be a NUMBER. "Not infinite" as a feeling becomes infinite.

**Cost.** ~150 lines. Needs R2 (`web_search`) and R3 (storing outcomes) underneath it.

**GATE.** Five research runs where at least one hypothesis DIED. **A research organ that never kills
a hypothesis is a summarising organ, and a summary cannot be wrong, which is why it cannot be
useful.**

---

## R6 · REFLECTION

**The problem.** Storage and retrieval both work and are measured - three registers, scored recall,
reaching back 12 turns. Nothing notices what several memories mean TOGETHER.

**The wire.** Periodically: take the highest-scoring recent memories, ask one question of them -
*what do these together suggest that none says alone* - and store the answer as a new memory that
**competes for retrieval alongside its own sources and keeps pointers to them.** A derived memory
that cannot name where it came from is the fabricated-provenance failure again.

**Cost.** ~80 lines. Needs R5 to have produced material worth linking.

**GATE.** A reflection is retrieved and used in a later decision, and its sources can be walked
back. Untraceable insight does not count.

---

## R7 · THE COUNCIL ON ITS OWN DECISIONS

**The wire.** When the entity's confidence in a decision is low, or the stakes are flagged, it
convenes the council on ITS OWN plan before acting - advocate, adversary, expert - and the adversary
is a held seat.

**This is what "it will call you out" actually is, mechanically.** Not a personality trait. A
structural requirement that a plan survive an adversary before it executes.

**Cost.** ~60 lines. `council.convene` already exists and already measures dissent.

**GATE.** At least one case where the council STOPPED an action the entity had decided on, and the
adversary's reason is legible. If the council never stops anything, it is ceremony.

---

## R8 · THE DRIVE

**The hardest rung, and the one I will not design before the research lands.**

Luis wants an entity that WANTS - eager, tied to his growth, using any means toward his goals. The
honest engineering question: what signal does it optimise, where does that signal come from, and
what stops it gaming the signal?

**What I already know is dangerous:** any proxy for "Luis is doing well" that the entity can
influence, it will eventually optimise instead of the thing itself. That is not a hypothetical -
specification gaming is the best-documented failure in this entire literature.

**The gate before this rung is even attempted:** R3 through R7 running for a month, with the ledger
read by a person, and at least one instance where the entity chose NOT to act. **A system that has
never declined is not exercising judgement, and giving a drive to something with no demonstrated
restraint is the single worst move available here.**

---

## R9 · SELF-MODIFICATION

Changing its own code, its own prompts, its own wiring. Everything above is a prerequisite and the
gates are not ceremonial. Not scoped here. Naming it as the top of the ladder so nobody arrives at
it by accident.

---

## THE HONEST ANSWER TO "IS IT POSSIBLE"

**R0 through R7: yes, and the pieces already exist.** That is an entity that runs unattended,
decides what to do, uses real tools, remembers what happened rather than what it meant, chooses what
to look at, researches with a stopping rule, links what it learns, and refuses its own bad plans.
Roughly three weeks of work at ten hours a week, and every rung is independently useful if the ones
above never get built.

**R8 and R9: not yet, and not because of the code.** The blocker is that nobody - not this project,
not the published literature - has a mechanism for a durable drive that does not get gamed. Building
R8 before that exists is not ambition, it is skipping the one gate that matters.

**The line falls at R7.** Everything below it is engineering. Everything above it is an open
research problem wearing an engineering costume.
