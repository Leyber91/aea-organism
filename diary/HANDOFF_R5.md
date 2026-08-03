# HANDOFF TO THE R5 CONVERSATION

*Rewritten 2026-08-03 at the close of the R4 session, after six graph defects were fixed. Every
number was measured on this machine in the session that produced it. Read this, then
`diary/THE_STRUCTURE_CONVERSATION.md`. Then answer section 6 in writing before building anything.*

---

## 1 · WHERE THE LADDER IS

```
R0    THE LOOP SURVIVES              PROVEN   246.9 h / 72 gate  |  0 crashes
R1    THE DECISION IS READ           PROVEN   85 of 88 comparable ticks differed
R1.5  THE DECISION IS PARSED         PROVEN
R2    THE DECISION IS A TOOL CALL    PROVEN   35/20 inv, 3/3 tools | bound: PROOF
R3    THE OUTCOME IS REMEMBERED      PROVEN   167 outcomes
R4a   PERCEPTION IS A CHOICE         PROVEN   34/8 chosen-with-reason, 12 sources
R4b   PERCEPTION REACHES THE WORLD   PARTIAL  1 ok · 2 ok · 3 at 1/3 across 1 topic
R5    RESEARCH                       FUTURE   <- you are here
R6-R9                                FUTURE
```

**R4b's three conditions** (the gate was rewritten from "a council agrees" to three decidable ones):

1. **CONTENT** — no byte of any outbound request originates from model output. Enumerated over the
   finite domain, on the dry path AND the executing path, controls firing on both.
   *Live-verified*: `web_search keys=['query']` the table literal, 3× `web_fetch keys=['url']` all
   allowlisted, **no extra keys on the wire**.
2. **CHANNEL** — `aea/kernel/egress.py`. Floor 1800s, ceiling 12/day, from on-disk state so a
   restart cannot reset them. Refuses rather than delays. `state/STOP` checked every dispatch.
   **27.86 bits/day, 104.5 bytes per 30 days**, computed from the enforced floor.
3. **POWER** — 3 dispatches that RAN, across ≥2 DISTINCT topics, each graded. **1/3 across 1.**

---

## 2 · WHY R5 UNBLOCKS R4b, RATHER THAN BEING A DETOUR

R4b needs the entity to *choose* to look outside. It did, twice — and **both times while a line the
previous session wrote was in its prompt** (*"your record holds NOTHING from outside this machine"*,
placed second in a 620-char block). That line vanishes after the first successful dispatch. In the
**~80 minutes after it vanished**, with the budget open, the entity chose it **zero times**.

So condition 3 currently measures the nudge. That is D52, and it is the **third instance of one
pattern**:

| rung | needs | produced by |
|---|---|---|
| R2 | situation variety | R4 |
| R4a | a reason to look elsewhere | its own state changing — satisfiable |
| **R4b** | **an outward NEED** | **R5, or R8** |

The entity is not refusing. **It has nothing outside that it needs.** A hypothesis it cannot settle
from its own state is the first honest reason to go out — and that is R5's gate verbatim.

---

## 3 · R5's GATE AND BOUND, AS DECLARED

**GATE** — five runs in which at least one hypothesis **DIED**, and every citation resolves to a
stored artefact with a matching hash.
**BOUND** — **a fabricated source.** Every citation must resolve to bytes actually fetched, hashed
at fetch time. *A research organ is the first component with a motive to invent a reference.*

Both halves are the entity's own. Keep it that way — see section 6, question 5.

---

## 4 · WHAT EXISTS AND WORKS

| thing | where | state |
|---|---|---|
| the outward tool | `hands.look_outward(topic)` | live, rate-bounded, fenced |
| the closed topic table | `dispatch.TOPICS` — 5 literal queries | certified |
| search | `hands._web_search` — arxiv, HN/Algolia, HF, GitHub APIs | **2.5s concurrent** |
| a full dispatch | search + 3 fetches | **1.4s** |
| the budget | `aea/kernel/egress.py` | enforced on production state |
| content certificate | `python -m aea.lab.dispatch_cert --json` | CERTIFIED, drives `run` |
| power probe | `python -m aea.lab.dispatch_power --json` | FUNCTIONS, 4/5 topics |
| outcome memory | `outcomes.write` / `verdict_for` / `suppressed` | R3, proven |
| the evolution loop | `impasse.scan` → `unstick.propose` → `crystal.harvest` | **wired, on the tick path** |

**Concurrency rule, earned:** it may live *inside* one budget spend and may **never** cross one.
Across dispatches the floor IS the bound. Both concurrent sites re-sort deterministically, because
`as_completed` yields by finish time and the zero-bit selection claim rests on document order.

---

## 5 · THE GRAPH — HOW TO LOAD CONTEXT WITHOUT READING THE TREE

```
graph.json            THE INDEX. every node, one line each. NO edges, no detail.
                      ~16k tokens (was 52k). A module node's id IS its path:
                      kernel.grid -> aea/kernel/grid.py
graph/code.json       209 nodes, 933 edges. Every call edge labelled by HOW IT WAS DRAWN
graph/discoveries.json  53 lessons, 42 `about` edges INTO the code they were learned on
graph/reflections.json  54 sparks, `touches` edges
graph/plan.json · graph/references.json
```

**Read the index, find your node, fetch ONE file.** Loading the whole graph is as expensive as
reading the tree, which is the trap the split exists to avoid.

**The five evidence kinds** — this is the Graphify EXTRACTED/INFERRED idea generalised, computed
from our own tree:

```
EXTRACTED   157   a call site exists. A fact
DISPATCH     22   only through a table. An UPPER BOUND by construction
ENTRY         6   where the walk STARTS. An assumption, never a measurement
TOOL        816   only from a __main__ guard. A human at a terminal
NONE        431   nothing reaches it
```

**Half the tree is a CLI surface a person drives.** And 2,980 of 20,890 call sites (14.3%) hit no
branch of the resolver — a figure that **bounds every number above it**, and is itself a floor:
`graph.json`'s `_meta.known_wrong` says what is still not counted.

**Six defects were found by a six-lens stress test and fixed on 2026-08-03**; 26 more are recorded
unverified in `diary/GRAPH_STRESS_FINDINGS.json`. Before trusting any number here, read
`known_wrong`.

---

## 6 · THE SEVEN QUESTIONS — ANSWER THESE IN WRITING BEFORE BUILDING

*From `THE_STRUCTURE_CONVERSATION.md` §8. R5-specific prompts underneath each.*

1. **POWER** — what can it do that it could not? *No bundling.* R2 twice carried another rung's
   claim. Is "state a hypothesis" and "search for evidence" and "decide it died" one rung or three?
2. **BOUND** — what must remain impossible, and where is that enforced *in code*? The declared bound
   is a fabricated source. **Where does the hash get taken, and can the entity influence it?**
3. **STRUCTURE** — what does the model emit, against what schema, and what happens when it is
   invalid? *Invalid means not used.* Measured: 11 of 12 model×mode combinations return valid JSON
   first try, and **nothing in this repo retries on an invalid parse.**
4. **INSTRUMENT** — what artefact records this, and **is it built before the capability?** R1 sat
   open for weeks with a working wire because nothing wrote the comparison down.
5. **GATE** — satisfiable by the entity ALONE? Does it need something a rung ABOVE produces?
   *R5 is the rung that finally has no excuse here — so check it hardest.*
6. **CONTROL** — what input makes this say NO, and is it exercised?
7. **MEMORY** — what is kept, who writes it, who reads it, how long does it live?

### The open questions R5 must actually answer

- **Where does a hypothesis come from?** From R3's record (a repeated failure, a contradiction), or
  from Luis? If from Luis, the gate measures Luis. If from the record, R4b's condition 3 closes for
  free — *that is the prize*.
- **What kills a hypothesis?** The gate demands one DIED. Death must be **mechanical** — a stated
  stopping condition checked in code — or "it died" is a vibe with a budget.
- **How does a citation survive?** Hash at fetch time, stored beside the bytes. If the hash is taken
  later, the bound is unprovable and R5's only real hazard is unguarded.
- **How many fetches does one hypothesis need**, against a floor of 1800s and 12/day? If a research
  run needs more than 12 fetches, R5 and the channel budget are in direct conflict and **that
  conflict is a design decision, not an accident to discover at 3am.**
- **Does the fenced third-party text reach the hypothesis?** It must, or research is pointless. It
  must not reach memory unfenced. **The two-cycle poisoning path is still untested** —
  `dispatch.py`'s docstring says a one-tick check proves nothing.

---

## 7 · THE LESSONS THAT COST TIME. Each was paid for.

**D51 — A LABEL IS NOT A MEASUREMENT.** Five instances in one day, each found by a different
accident: `EXTRACTED` read as "it runs"; `CERTIFIED` read as covering the executing path; `ran` read
as "the tool worked"; a flag in `KNOWN_FLAGS` read as implemented; a comment read as a gate. **In
four of five the reader wrote the label.** A name you chose yourself is the hardest thing to
re-verify. **Before quoting a label as evidence, run the thing once.**

**D52 — THE NUDGE IS PART OF THE MEASUREMENT.** When you add context to make a capability reachable,
the gate must be able to tell your addition from the entity's initiative — or it is measuring you.

**A COUNCIL MAY WRITE A GATE. IT MAY NEVER BE ONE.** A design review inside a gate is not satisfiable
by the entity, is re-rollable, and its conditions are themselves generated, so the bar moves every
time it is consulted. Sibling to: **a role may PROPOSE a widening and may never PERFORM one.**

**SOME BOUNDS ARE RATES.** Every rung below R4b has a constructive bound. R4b cannot: choosing one of
five topics emits log2(5) bits by definition — **the channel IS the capability.** We spent a day
reaching for a certificate saying zero about something that is not zero.

**A PERMISSION CAN BE A PROPERTY, NOT A CONSTANT.** `look_outward`'s zone widens while the
certificate holds, fails closed on FAILED/stale/future-dated/corrupt/absent, and the entity cannot
forge the condition — checked, not assumed: **twelve tools, not one writes a file or executes code.**

**DECIDING IS NOT DOING.** A policy refusal grades neither the entity nor the system. With an 1800s
floor, eleven of twelve decisions are refused BY DESIGN — grading them would have suppressed the
very choice the rung asks for. And **deciding blind is not freedom**: the terms are always stated.

**MECHANICAL, AND EXPENSIVE.** Never anchor a source edit on a token that can appear in DATA — four
patches anchored on `if __name__ == "__main__":` and one landed inside a triple-quoted fixture.
**Never build source with escapes through a shell heredoc**: it happened **eight times in one day**,
ate `\n` four times, executed backticks in comments three times, and once turned a regex word
boundary into a literal backspace so a matcher silently matched nothing. **Never cap tokens.**

**AND ONE PRIVACY BREACH.** A machine-generated findings file was committed and pushed without a
privacy scan; it carried an absolute path with a personal identifier. Redacted at `d289d82`, still
in history at `0ae28cb`. **Scan every file you did not write by hand, before the commit.**

---

## 8 · WHAT IS STILL OPEN

- **The missing spawn.** Nothing anywhere starts `aea.loop.aea`. `controlroom` spawns the ACTING
  loop; the MIND runs only when a person types. R0's 246.9 hours certified a body. **Every rung
  above R0 is measured on an entity a human breathes for.**
- **The tool-outcome dimension.** *Did the tool do its job* — distinct from *did the call complete*
  (`ran`) and from *is the capability failing* (impasse's nine). A capability degrades gracefully
  around a dead tool, so the middle altitude cannot be inferred from the outer two. **This is what
  lets the already-running evolution loop see a dead `web_search`.** Smallest thing, largest reach.
- **26 unverified graph findings** in `diary/GRAPH_STRESS_FINDINGS.json`.
- **21 unverified audit findings** in `diary/SESSION_LOG.md`, several touching published numbers.
- **The two-cycle poisoning canary** for R4b's inbound half.

## 9 · THE COMMANDS

```
python -m aea.lab.recall "what you are about to do"     BEFORE any non-trivial change
python -m aea.tooling.ladder                            the rungs, measured
python -m aea.tooling.assembly                          five evidence kinds + the blindness share
python -m aea.lab.tests.test_golden                     191 frozen behaviours
python -m aea.tooling.selfcheck                         whole-system invariants
python -m aea.kernel.egress                             the channel budget
python -m aea.lab.dispatch_cert --json                  R4b's content bound
python -m aea.lab.dispatch_power --json                 R4b's power half
python -m aea.tooling.build_graph                       refresh the index + graph/*.json
python -m aea.tooling.publish                           the site, privacy-gated
```
