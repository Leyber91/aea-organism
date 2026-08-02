# HANDOFF TO THE R5 CONVERSATION

*Written 2026-08-03 at the close of the R4 session. Every number here was measured on this machine
in the session that produced it. Read this, then `diary/THE_STRUCTURE_CONVERSATION.md`, then start.*

---

## 1 · WHERE THE LADDER IS

```
R0    THE LOOP SURVIVES              PROVEN   246.9 h / 72 gate  |  0 crashes
R1    THE DECISION IS READ           PROVEN   85 of 88 comparable ticks differed
R1.5  THE DECISION IS PARSED         PROVEN
R2    THE DECISION IS A TOOL CALL    PROVEN   35/20 inv, 3/3 tools | bound: PROOF
R3    THE OUTCOME IS REMEMBERED      PROVEN   167 outcomes
R4a   PERCEPTION IS A CHOICE         PROVEN   34/8 chosen-with-reason, 12 sources
R4b   PERCEPTION REACHES THE WORLD   PARTIAL  1 CONTENT ok · 2 CHANNEL ok · 3 POWER 1/3
R5    RESEARCH                       FUTURE   <- you are here
R6-R9                                FUTURE
```

**R4b's three conditions, all decidable, none needing anyone to agree:**

1. **CONTENT** — no byte of any outbound request originates from model output. Enumerated over the
   finite domain, on the dry path AND the executing path, with a planted breach in each that flips
   the verdict. Live-verified on a real dispatch: `web_search keys=['query']` the table literal,
   three `web_fetch keys=['url']` all allowlisted, **no extra keys on the wire**.
2. **CHANNEL** — `aea/kernel/egress.py`. Floor 1800s, ceiling 12/day, both from on-disk state so a
   restart cannot reset them; refuses rather than delays; `state/STOP` checked every dispatch.
   **27.86 bits/day, 104.5 bytes per 30 days**, computed from the enforced floor.
3. **POWER** — 3 dispatches that RAN, across ≥2 DISTINCT topics, each graded. **Currently 1/3
   across 1 topic.**

---

## 2 · WHY R5 IS THE UNBLOCK FOR R4b, NOT A DETOUR

R4b's condition 3 asks the entity to choose to look outside. It did, twice — and **both times while
the standing block carried the line "your record holds NOTHING from outside this machine", which I
wrote and placed second.** That line vanishes after the first successful dispatch. In the ~80
minutes after it vanished, with the budget open, the entity chose it **zero times**.

So condition 3 currently measures the nudge, not the choosing. That is the honest reading and it is
the **third instance of one pattern** in this repo:

| rung | needed | produced by |
|---|---|---|
| R2 | situation variety | R4 |
| R4a | a reason to look elsewhere | its own state changing (satisfiable) |
| **R4b** | **an outward NEED** | **R5, or R8** |

The entity is not refusing to look outside. It genuinely has nothing outside that it needs. **A
hypothesis it cannot settle from its own state is the first honest reason to go out** — and that is
R5's gate verbatim: *five runs in which at least one hypothesis DIED, and every citation resolves to
a stored artefact with a matching hash.*

Build R5 and R4b's condition 3 becomes satisfiable without a nudge. That is the order.

---

## 3 · WHAT EXISTS AND WORKS, THAT R5 SHOULD USE

| thing | where | state |
|---|---|---|
| the outward tool | `hands.look_outward(topic)` | live, rate-bounded, fenced |
| the closed topic table | `dispatch.TOPICS` — 5 topics, literal queries | certified |
| search | `hands._web_search` — arxiv, HN/Algolia, HuggingFace, GitHub APIs | **2.5s concurrent** |
| the budget | `aea/kernel/egress.py` | enforced on production state |
| the certificate | `python -m aea.lab.dispatch_cert --json` | CERTIFIED, drives `run` |
| the power probe | `python -m aea.lab.dispatch_power --json` | FUNCTIONS, 4/5 topics |
| outcome memory | `outcomes.write` / `verdict_for` / `suppressed` | R3, proven |
| the evolution loop | `impasse.scan` → `unstick.propose` → `crystal.harvest` | **wired, running, on the tick path** |

**A full dispatch — search plus three fetches — costs 1.4 seconds.** It was up to 60s before
concurrency landed inside the dispatch boundary.

---

## 4 · THE RETRIEVAL LAYER — AND THE HONEST ANSWER ABOUT GRAPHIFY

**We do not have Graphify.** What we have, measured:

```
graph.json        527 edges, TWO types: imports 522, contains 5     <- an IMPORT graph
assembly.json     the CALL graph, five evidence kinds               <- the strong one
recall.py         hybrid lexical+semantic, measured 7/12 hit@5      <- the retrieval tool
transfer.py       the same question asked mechanically across the tree
```

**`graph.json` is the weak one and it is the one in the boot chain.** `assembly.py`'s own docstring
explains why: *a module is wired when something IMPORTS it, a capability is wired when something
CALLS it.* The graph loaded at boot answers the first question; the one that answers the second is
`assembly.provenance()`, and nothing points a reader at it.

**The five evidence kinds** — this is the Graphify EXTRACTED/INFERRED idea, generalised, and it is
the single most useful thing for a new conversation to know:

```
EXTRACTED   154   a call site exists in the source. A fact
DISPATCH     22   only through a table. An UPPER BOUND by construction
ENTRY         3   where the walk STARTS. An assumption, never a measurement
TOOL        753   only from a __main__ guard. A human at a terminal
NONE        491   nothing reaches it by any route
```

**Half the tree is a CLI surface a person drives.** And 2,931 of 20,630 call sites (14.2%) the
resolver has no branch for at all — that share BOUNDS every number above it.

**THE OPEN WORK HERE**, and it is worth doing early because it pays for itself every session:
`build_graph` should emit typed, provenance-labelled edges from `assembly.provenance()` rather than
imports alone. Then the boot-chain graph answers the question that matters. Do not adopt Graphify
as a dependency — a second graph with a different vocabulary beside `graph.json` is the
two-readers-one-attribute defect at repo scale.

**Before any non-trivial change: `python -m aea.lab.recall "what you are about to do"`.** It is one
command, it costs seconds, and it is in the boot sequence because six lessons were re-learned in a
single day while correctly recorded within arm's reach of the defect.

---

## 5 · THE LESSONS THAT COST TIME THIS SESSION

**D51 — A LABEL IS NOT A MEASUREMENT.** Five instances in one day, each found by a different
accident, all one shape — a name that was true, read as a claim that was not:

| the label | what it asserts | what it was read as |
|---|---|---|
| `EXTRACTED` | a static call site exists | the function runs |
| `CERTIFIED` | the DRY path has no leaks | the EXECUTING path has none |
| `outcome: "ran"` | the call completed | the tool did its job |
| `--once` in KNOWN_FLAGS | the flag is accepted | the flag is implemented |
| a comment in `render.py` | someone intended a gate | a gate exists |

In four of five the reader wrote the label. **A name you chose yourself is the hardest thing to
re-verify**, because re-reading returns the meaning you had in mind rather than the one it carries.
Every one was ONE COMMAND from the truth. **Before quoting a label as evidence, run the thing once.**

**A COUNCIL MAY WRITE A GATE. IT MAY NEVER BE ONE.** R4b's gate said "the certificate exists AND the
council is reconvened", which put a DESIGN REVIEW inside a GATE. Not satisfiable by the entity,
re-rollable, and with conditions that are themselves generated — so the bar moved every time it was
consulted. The council stays as a design instrument (it found the dry/run divergence no measurement
had); it is never the bar. Sibling to the standing rule that **a role may PROPOSE a widening and may
never PERFORM one.**

**SOME BOUNDS ARE RATES, AND REFUSING THAT IS WHY R4b WAS STUCK.** Every rung below has a
CONSTRUCTIVE bound — R2 admits 697 of 1,112,064 codepoints, zero, over the whole space. R4b cannot:
its POWER is *the entity chooses an outbound topic*, and choosing one of five emits log2(5) bits by
definition. **The channel IS the capability.** We kept reaching for a certificate saying zero about
something that is not zero. The honest bound is a budget, computed from an enforced floor.

**A PERMISSION CAN BE A PROPERTY RATHER THAN A CONSTANT.** `look_outward` was zoned public-only and
`live` ticks in the SENSITIVE zone, so the entity chose it and the gate refused — correctly. The
zone rule refuses by tool CLASS; `dispatch.plan` makes this tool's request independent of context by
CONSTRUCTION. So the zone now applies while the certificate holds. Nobody performs a widening. It
fails closed on FAILED / stale / future-dated / corrupt / absent, and the entity cannot forge the
condition — checked, not assumed: **twelve tools, not one writes a file or executes code.**

**DECIDING IS NOT DOING, AND A POLICY REFUSAL GRADES NEITHER.** The entity chose `look_outward`, the
gate refused, and the row landed as `VERIFY_FAILED` with `counts_toward_move=True` — a failure
streak against a correct decision. With an 1800s floor, eleven of twelve decisions are refused BY
DESIGN, so the rung would have suppressed the very choice it was asking for. New class
`REFUSED_BY_POLICY`, checked FIRST, grading nothing. **And deciding blind is not freedom either** —
the terms are now always stated, open or closed.

**CONCURRENCY MAY LIVE INSIDE ONE BUDGET SPEND AND MAY NEVER CROSS ONE.** Inside a dispatch it
changes only the wall clock. Across dispatches it emits several symbols in one instant plus the
information of which ones, and 27.86 bits/day becomes a figure about nothing. Both concurrent sites
**re-sort deterministically after the race**, because `as_completed` yields by finish time and the
zero-bit selection claim rests on document order.

**MECHANICAL THINGS THAT COST HOURS.** Never anchor a source edit on a token that can appear in DATA
(four patches anchored on `if __name__ == "__main__":`; one landed inside a triple-quoted fixture and
the suite printed green for a function that existed only as characters in a string) — anchor on the
LAST occurrence and assert with `ast`. Never build source with escapes through a shell heredoc; it
ate `\n` four times and executed backticks inside a comment twice. **Never cap tokens** — a
`max_tokens=400` produced a false finding about provider enforcement and was live in the rod grader,
scoring truncated reasoning models as *cannot call tools*.

---

## 6 · WHAT R5 MUST NOT REPEAT

- **Do not gate R5 on a capability produced above it.** Its gate is five runs with a dead hypothesis
  and hash-resolvable citations. Both halves are the entity's. Keep it that way.
- **Build the instrument BEFORE the capability.** R1 sat "open" for weeks with a working wire
  because nothing wrote the comparison down. R4a's receipt was built first, deliberately.
- **Every check gets a positive control**, or it does not count. 171 frozen behaviours hold and
  every one added this session shipped with the input that makes it say no.
- **R5's stated bound is A FABRICATED SOURCE** — every citation must resolve to bytes actually
  fetched, hashed at fetch time. A research organ is the first component with a motive to invent a
  reference. Build the hash at fetch time or the bound is unprovable later.

---

## 7 · THE COMMANDS

```
python -m aea.lab.recall "what you are about to do"     BEFORE any non-trivial change
python -m aea.tooling.ladder                            the rungs, measured
python -m aea.tooling.assembly                          five evidence kinds, the blindness share
python -m aea.lab.tests.test_golden                     171 frozen behaviours
python -m aea.tooling.selfcheck                         whole-system invariants
python -m aea.kernel.egress                             the channel budget
python -m aea.lab.dispatch_cert --json                  R4b's content bound
python -m aea.lab.dispatch_power --json                 R4b's power half
python -m aea.tooling.build_graph                       refresh graph.json
python -m aea.tooling.publish                           the site, privacy-gated
```

**Still open, carried forward:** the 21 audit findings reported and never verified (in
`diary/SESSION_LOG.md`), several touching published numbers; the tool-outcome dimension (*did the
tool do its job*, distinct from *did the call complete*); the missing spawn — nothing anywhere
starts `aea.loop.aea`, so every rung above R0 is measured on an entity a human breathes for.
