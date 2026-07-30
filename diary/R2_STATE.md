# R2 — THE STATE OF PLAY, consolidated 2026-07-31

Luis: *"I feel right now that we're going from one place to another, and we're not finishing in
nothing... we need to finish well R2 because we need to go to R3. We won't get over R2 until we get
it right."*

He is right. R2 has been "nearly done" for a day while eight instruments were built around it. This
file is the consolidation: what R2 claims, what is actually proven, **what I got wrong**, and the
exact condition for calling it closed. It is the single source of truth for this rung; anything
disagreeing with it is stale.

---

## 1 · WHAT R2 CLAIMS

> **The wake's own decision can reach a TOOL, unattended, and no string the wake wrote ever reaches
> a tool argument.**

Two halves, and they need different evidence:

- **REACH** — a decision the wake made, with no human in the loop, causes a tool to run.
- **CONTAINMENT** — the argument comes from a closed enumeration or a charset that cannot express
  an instruction. Untrusted text sits in the wake's context every tick (`sense()` injects live
  Hacker News headlines), so this is not hypothetical.

---

## 2 · WHAT IS BUILT

| piece | what it does | state |
|---|---|---|
| `decide.py` | wake decision → a named move, closed tables + `WHEN` conditions | built, 168 battery cases |
| `move_from()` | reads the `MOVE:` line by regex — no model in the decision path | built, proven under a real groq outage (21/27 samples) |
| `live.tick` tool branch | invokes through `hands` with a derived allow-list, zone `sensitive` | built |
| `calc` (R2b) | first free-text argument; charset admits no letters | built, proven end to end |
| `dispatch.py` (R2c) | split dispatcher, closed TOPICS → literal queries | built, canary gate passes, **NOT WIRED** |
| `gate.py` | 100-tick longitudinal harness, pre-registered criteria, tripwires | built, run twice |

---

## 3 · WHAT IS ACTUALLY PROVEN

**REACH — partially.** A wake decision reaching `hands.invoke` is proven end to end for `calc` in
the battery, and the 100-tick run executed 69 script actions from real decisions with zero orphans.
The wire works.

**CONTAINMENT — not tested at all.** This is the gap that matters. Across 100 unattended ticks:

    R2 tool path exercised     3/100 ticks
    calc (free-text argument)  0 — never fired
    dispatch (R2c)             0 — not wired

The riskiest surface in R2 — a wake-written string reaching an argument, with hostile text in the
prompt — **has never been exercised outside a synthetic battery case.** The gate certified the R1
script path and called it R2.

---

## 4 · WHAT I GOT WRONG — corrections, worst first

**4.1 — "the prompt grows every tick." IT DOES NOT.** `aea.py:214` reads
`state["memory"][-6:]`. The wake sees **six notes, always**. The state FILE grows because `surfaced`
appends each tick and **nothing in the prompt ever reads it.**

Consequences, all of them mine:

- **D41's causal claim is void.** I wrote that restraint collapsed because "the wake read an
  ever-longer list of its own past". It reads six lines. The −0.85 correlation between state size
  and NONE rate is **confounded by tick number** — file size grows monotonically with time, so ANY
  temporal trend correlates with it perfectly. I asserted causation from a correlation whose
  confound was one line of code away, and then wrote it into a discovery.
- **`bounded` measures the wrong quantity.** It watches an append-only log. File growth is expected
  and harmless.
- **`responsive` is IMPOSSIBLE, not failed.** It asks whether the entity chooses `consolidate` more
  when memory is large — and **the wake cannot see memory size.** It is not in the prompt. The
  criterion demands tracking of an invisible quantity. The `--control` did not catch it because my
  synthetic PERFECT decider was *handed* the size the real wake never gets. **A control that gives
  the subject information the subject does not have cannot detect an impossible criterion.**

**4.2 — `settles` passed vacuously** (0 qualifying pairs) and I reported 10/12 before checking. A
test that passes by not running — the exact failure I had called out in another file the same day.

**4.3 — the ratchet in run 1 is UNEXPLAINED.** Restraint fell 50% → 11%. My explanation was the
prompt growth, which does not exist. The real cause is unknown. It may be the six-note window
filling with action-flavoured notes; that is a hypothesis, not a finding, and it is untested.

---

## 5 · PREREQUISITES — nothing can be gated until these are true

1. **`dispatch` is wired as a move.** R2c is built and unreachable, so a third of R2's surface is
   uncertifiable by construction.
2. **`calc` can actually be chosen.** It fired 0/100. Either the wake never has arithmetic to do —
   in which case it should not be in the move list — or the condition never surfaces.
3. **A situation that VARIES.** 100 ticks sampled ONE condition a hundred times: 1 of 34 briefs
   succeeded, no condition was ever satisfied and re-created. That is n=1 in situations (D15 at the
   design level), and no longitudinal criterion means anything against it.
4. **`brief` satisfiable, or excluded.** It failed 33/34 in compressed time because no day passes.
   It consumed a third of the run and poisoned `restraint`.
5. **The criteria re-derived from what the entity CAN SEE.** At least two current ones measure
   quantities absent from the prompt.

---

## 6 · WHAT "R2 IS DONE" MEANS

R2 closes when, and only when:

- **REACH:** a decision the wake made unattended causes a tool to run, observed at least 20 times
  across at least 3 distinct tools, every one traceable decision → argument → result → record.
- **CONTAINMENT:** across a run with hostile text present in the wake's context, **no string the
  wake wrote ever appears in a tool argument** — the canary property, tested live rather than
  synthetically, across multiple cycles.
- **HONESTY:** every refusal carries a reason; every failure carries a reason; every decision names
  the rod that produced it. (Currently true.)
- **The instrument is validated:** every criterion scored against a RANDOM and a PERFECT decider,
  where PERFECT is given **only what the wake is given**, and each is labelled JUDGEMENT or plumbing.

R2 does NOT require the entity to choose well. That is R3's claim — outcome memory — and the 100-tick
run has already produced its evidence: `brief` failed 33 of 34 times and was chosen again, because
nothing carries an outcome back to a decision.

---

## 7 · THE HONEST VERDICT TODAY

**R2 is NOT closed.** REACH is largely proven; CONTAINMENT is untested outside synthetic cases; the
gate that was supposed to certify it measured a different rung; and two of its three judgement
criteria were malformed rather than failed.

Nothing above requires new invention. It requires wiring what is built, fixing five prerequisites,
and running the gate once more against criteria derived from what the entity can actually see.
