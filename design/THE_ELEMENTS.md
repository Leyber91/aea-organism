# THE ELEMENTS - everything the assistant needs, in dependency order

*2026-07-28, written the night `produce_brief` earned WATCHED after eighteen days pinned at DRAFT.
This is not a wish list. Every item is either BUILT and tested, or named because its absence has a
measured consequence. Ordered by what is impossible without what.*

---

## THE ONE-LINE STATE

It wakes itself, reads real repos, calendar and inbox, keeps private data on this machine, produces a
brief, grades its own permission to do so, and as of tonight can tell when it is stuck and say what
to change. It cannot yet act on that, learn from it, or be given a second job.

---

## TIER 0 - THE LOOP THAT GETS UNSTUCK

*Five steps. Four built tonight. Nothing above this tier matters until they close, because a system
that cannot leave an impasse cannot be left alone.*

| # | element | what it is | status |
|---|---|---|---|
| 1 | **NOTICE** | consecutive-failure counter, alarm at 3, durable to `state/trust_alarms.json` | **BUILT** |
| 2 | **DIAGNOSE** | stuck (one repeated cause) vs unreliable (many causes) | **BUILT**, verified on the real 18 days |
| 3 | **VARY** | one bounded move from a declared set, chosen by measured evidence | **BUILT**, proposes only |
| 4 | **RECORD** | impasse signature + move + outcome, indexed by what it resolved | **BUILT**, empty |
| 5 | **CRYSTALLIZE** | a resolution that holds becomes a reusable part | **MISSING** |

**The gap between 3 and 4 is the whole safety argument.** A system that varies without recording is
not adaptive, it is thrashing. That is why 4 was built before 3 was allowed to execute.

**What still blocks the loop closing:** step 3 proposes and nothing applies. Wiring `unstick.propose`
into the wake is small; it was deliberately left undone until the record existed.

---

## TIER 1 - THE THINGS WITHOUT WHICH IT IS STILL A SCRIPT

### GOALS - the largest missing element, and it is not close

It has exactly one job, hardcoded: produce the brief. There is no slot for a second. Everything in
Tier 0 is machinery for getting unstuck on a task it was **given**, and it has only ever been given
one.

What a goal needs to be, minimally: a statement of what is wanted, a way to tell whether it is done,
a capability it maps to (so the trust ledger can grade it), and a zone (so the privacy boundary
knows where it may run). Without the last two a goal cannot be graded or bounded, which makes it a
wish rather than a goal.

### MEMORY OVER EXPERIENCE - the floor under tools

It has tools available and no record of which tool worked. `A2` on the ABSTRACTION ladder. The
experience record built tonight is this element's storage; it has the shape and no history. **You
cannot crystallize a tool the system has never used, and it cannot know which tool worked without a
record of using them.**

### HONEST ESCALATION - more valuable than never getting stuck

`unstick` ends with `EXHAUSTED: every declared move has been tried against this impasse. Ask for
help.` That line matters more than any move above it. An assistant that escalates well beats one
that never gets stuck, because the second does not exist.

**Missing:** the escalation has nowhere to go. `notify.call()` rings a phone and is deliberately
unarmed. The open alarms are not in the brief, which is the one artifact actually read.

### HANDS - **BUILT** 2026-07-28, `kernel/hands.py` + `kernel/seats.py`

`io/agent_tools.py` had working tools since Phase 3 and the lab never touched them. What was missing
was not tools - it was **permission enforced where the call happens**.

- `hands.invoke()` is the only path a tool ever runs through. Four gates: seat allowlist, zone,
  charter capability, implementation exists. Verified: a rod was advertised `json_get`, told to use
  it, and refused twice in the sensitive zone. **Zero bytes moved.**
- `seats.py` = custom subagents. A seat is `capability + zone + MEASURED rod`. Drop one and it is a
  persona: a persona cannot be graded, bounded, or compared across a model swap.
- **Tool-calling is now measured** - the sixth suite, and the first one that grades a side effect
  rather than text. 16 rods probed, 8 pass. Live proof: `scout` returned llama.cpp's open-issue
  count from the real API through the gate.

**The line worth keeping:** *a read tool is an outbound channel if the model writes the address.*
`web_fetch` looks read-only; the URL is composed from context, so the request carries the data out.
Network tools are therefore PUBLIC-ONLY, structurally.

**Declared and permanently refused:** `send_email` (`send_outbound`, ceiling 0) and `spend`
(`spend_money`, ceiling 0), with **no implementation behind the gate**. The assistant demos in
circulation are built almost entirely out of those two. A system that merely lacks them looks
identical to one that refuses them; this one refuses them out loud, with the reason.

#### Two defects the build found in an hour, both fixed

- **The answer key was wrong.** The tool-call probe carried the expected product as a literal and the
  literal was wrong by six hundred. Every rod that answered *correctly* would have been recorded as a
  failure and the fuel table would have said tool-calling was impossible. Ground truth is now
  computed by the same deterministic function the tool uses. *An answer key written by the hand that
  wrote the question is not a key.*
- **The privacy boundary was testing a proxy.** Zones permitted plant `ollama` for private work
  because ollama is the local daemon. Ollama now proxies **hosted** models through that same daemon,
  marked only by a name suffix - and `gpt-oss:120b-cloud` was the fastest passing rod, so the
  selector seated a 120b **cloud** model on the zone that reads this machine's private state. A 120b
  model is not running on a laptop. `unstick.is_local()` now tests the rod, fails closed, and the
  seat refuses to exist. *Same shape as the invariant that tested for the word "zone": a boundary
  asserted about a proxy instead of the property.*

**Law IV is now enforced rather than quoted:** a rod change under a capability resets the promotion
streak and holds the level (`trust.reset_streak`). Consecutive only means something if the runs are
comparable, and Law IV says they are not.

### THE BUDGET CENTRE AND THE DISCRIMINATOR - the next element, and it is not missing, it is triplicated

There is no single authority on *what may be called, how often, and which rod fits this task*. There
are at least three partial ones - `lab/pace.py` (live `x-ratelimit-*` headers, day budget, feasibility),
`grid.Meter.can_spend` (used by `orchestrator`/`swarm`), and `energy/capacity.py` - and
`seats.pick_rod`, written today, consults **none of them**: it sorts by measured latency and stops.

The discriminator is now buildable because the measurements finally exist: fleet grades
`reach/format/arith/carry/code`, hands grades `tools`, unstick owns the zone, pace owns the budget. A
task states what it needs; the discriminator intersects those and returns a rod **or refuses**.
Selecting on speed alone is exactly how the fastest rod in the table - which cannot call a tool at
all, it emits a JSON blob as prose - would have been seated.

---

## TIER 2 - SELF-RECOGNITION

*Three questions the entity cannot currently answer about itself.*

**WHAT AM I MADE OF RIGHT NOW.** Not the design document - the live seat. Which parts are loaded, on
which fuel, with which read precedence. Measured over 18,338 stored replies, that precedence changes
the final answer on 0.233 of them and on half against the naive read; a running organism has no way
to know its own.

**WHAT DID I DO LAST TIME THIS HAPPENED.** Tier 1's experience record. Without it every impasse is
the first one.

**WHAT CHANGED UNDER ME.** No stored run records the code revision that produced it. `design_id`
fingerprints the declared design, not the code. So the entity cannot separate *the world changed*
from *I changed*, which is the difference between learning and drifting.

---

## TIER 3 - CRYSTALLIZATION, AND THE PART EVERYONE GETS WRONG

The field calls this **library learning / skill induction**: SOAR chunking 1986, Voyager 2023,
SkillWeaver 2025. The 2026 consensus is unambiguous and it is not what people expect:

> **Creating the part is easy. ADMITTING it is hard.**

There is measured evidence that growing skill libraries make agents *worse* - skill shadowing. So the
element needed is not a skill writer. It is an **admission gate**, and this project already owns one:
the trust ledger, applied to parts instead of capabilities. A part is DRAFT on admission, promoted by
clean reuse, demoted on failure, retired when shadowed.

**And SOAR named the trigger in 1986:** do not crystallize on success. Crystallize on **resolved
impasse**. The signal that a result deserves to become permanent is that the system was stuck and got
unstuck. Which is why Tier 0 is the floor: the impasse loop is not a prerequisite for crystallization,
it is its *source of material*.

**The verified gap:** no system combines self-written skills with a competence gate on whether the new
skill may run unsupervised. Hermes writes skills and does not grade them; the trust-ledger frameworks
grade capabilities and nobody implements them. **That intersection is empty.**

---

## TIER 4 - THE CEILING, AND WHY IT DOES NOT MOVE BY ITSELF

The charter caps each capability regardless of earned streak: `send_outbound` 0, `spend_money` 0,
`self_modify_code` 1 as a reviewable diff. **The ceiling is not a cage. It is what makes the rest safe
to leave running.**

The rule that keeps the unstick loop honest, enforced in code and checked twice:

> **It may vary anything about HOW it does the task.**
> **It may never vary WHAT IT IS PERMITTED TO DO.**

**Two defects found in that enforcement within an hour of writing it**, both now fixed and both worth
keeping on the record:

- The check tested for the WORD `zone` in a move. The first replay duly proposed sending the PRIVATE
  calendar section to a hosted endpoint because that rod was faster, and passed the check, because the
  move never said "zone" - it just breached one. *An invariant that tests for a word instead of a
  property is not an invariant.*
- The boundary failed OPEN. An unlisted zone returned "no restriction". A mistyped or new zone name got
  full access to every hosted rod. It now fails closed.

### `propose_ceiling` - MISSING, and the answer to "not everything is set in stone"

A capability that has exhausted every move inside its ceiling should be able to **make the case** for a
higher one: what it is blocked on, what it has already tried, what it would do with the raise, and what
the worst outcome would be. Written to a proposals file. **Never self-applied.**

This is the entrustment model from medical training, which the research surfaced: autonomy is
*granted*, never taken. It preserves the flexibility - the ceiling genuinely is not set in stone - and
keeps the decision somewhere it can be checked, which self-assessment is not.

---

## TIER 5 - WHAT IS DELIBERATELY DEFERRED

**It improving its own purpose.** A system that cannot reliably do the one job it has should not be
redesigning the job.

**The liveness canary.** A heartbeat cannot certify its own heartbeat; the check must run outside the
loop it watches. Silent death is the dominant real-world failure of unattended agents - the process is
up, the log looks busy, and nothing works.

---

## THE ORDER, AND IT IS FORCED

```
close Tier 0        wire propose into the wake            small                     STILL OPEN
GOALS               it can be given a second job          largest missing element   BUILT
HANDS               one real tool call                    A0 -> A3, biggest jump    BUILT + measured
SEATS               subagents that can be graded/bounded  the roster                BUILT
DISCRIMINATOR       one authority on budget + fit         three exist, none used    NEXT
EXPERIENCE fills    accumulates by running, not building
CRYSTALLIZE         with the trust ledger as admission gate                         BUILT, empty
propose_ceiling     the flexibility, made auditable
```

Not preference - dependency. You cannot crystallize without experience, cannot accumulate experience
without tools that get used, cannot direct tools without goals, and cannot trust any of it without the
loop that notices when it is stuck.
