# PROMPT FOR THE NEXT SESSION

*Paste the block below as the first message. Everything after it is for a human, not for the prompt.*

---

```
Read these before doing anything, in this order:

  diary/HANDOFF_2026-07-29.md   the last session, both halves: eleven instrument defects, what
                                every rod actually does, the dev/qa/prod ladder, the scout, and
                                what NVIDIA's 323 agent skills taught
  design/THE_LAWS.md            48 laws, each paid for by a real failure. They bind you.
  diary/DISCOVERIES.md          D18 governs this session
  diary/OPEN_LOOPS.md           every open item carries FINISH / LATER / KILL

Then run these, so you are looking at the live state rather than a description of it:

  python -m aea.tooling.selfcheck        7 invariants + an advisory house-style row
  python -m aea.tooling.xray             by role: live / tool / evidence / paused / unwired
  python -m aea.energy.rodprobe --show   every measured rod fact, one place

THE TWO RULES THAT GOVERN THIS SESSION, both measured rather than argued:

1 THE INSTRUMENT IS WRONG MORE OFTEN THAN THE MODEL. Fifteen instrument defects in one session
  against almost no model behaving unexpectedly. Before believing any finding, ask what would
  have to be true of the INSTRUMENT for it to be false, and test that first.

2 THE COMPONENT YOU WROTE FASTEST IS THE ONE YOU CHECKED LEAST (law M9). Attention follows
  effort, not risk. The worst defect of the last session was three lines - `[] and append()`
  short-circuiting - which made three complete runs report "0 results" while their author
  rebuilt the prompt, the panel and the batch size. Deliberately re-read the cheap part.

THE JOB: OUTBOUND CAPABILITIES. An entity that cannot reach the world cannot help anyone.
Luis set this order.

1 INTERNET. hands.web_fetch and json_get exist, are permission-gated at the call site, and are
  reachable from the wake through brief. Extend from two hardcoded fetches to real search.
  Law B3: a read tool IS an outbound channel the moment the model writes the address. Copy the
  protocol from NVIDIA's aiq-research: STATE THE EXACT URL before sending anything to it, and
  require explicit confirmation for any non-local destination.
2 VOICE. aea/organs/converse.py is 531 lines, verified running end to end: the mind answers in
  1.49s and VOICE synthesis is the bottleneck at 14.7s of a 16.2s turn. Unwired. Audio never
  leaves the machine; only transcript text does. KEEP_TURNS=12 is ~3000 tokens against a 1M
  window - stop truncating at 0.3% of what the rod can hold.
3 RAG. Retrieval over design/ (3.4 MB, 196 files), NOT over code where the AST is exact. Six
  hosted embedders measured; nemotron-3-embed-1b is best (2048 dims, margin 0.528, 0.6s). ZONES
  permits `local` only in the sensitive zone, so anything private needs a LOCAL embedder. torch
  is installed CPU-only; a CUDA build is a decision, not a default.

BEFORE ANY OF IT, four cheap things everything else rests on:
  - fix the discriminator's INPUTS before wiring kernel/fit.py (421 lines). The tool-calling
    census undercounts and 59 of 86 model cards are unread. Wiring fit on bad data makes bad
    selection authoritative.
  - re-read those 59 cards with aea/tooling/scout.py, which now exists for exactly this.
  - decide the outbound boundary deliberately. send_outbound and spend_money are FORBIDDEN with
    no implementation at all.
  - GIVE OUR OWN SKILLS A CALL BUDGET. NVIDIA's nemo-retriever declares "at most 2 Bash calls",
    bans Glob/Grep/Read/TodoWrite, and states why: tokens emitted between calls become input AND
    cached input for every later turn, so the cost is quadratic. Our skills have no budget.

THE TOOLS YOU INHERIT, and the limits measured on them:
  aea/energy/rodprobe.py   metered transport, per-rod published params, one store (state/rods.json)
                           timeout is rodprobe.IDLE = 300s INACTIVITY, never None
  aea/tooling/scout.py     scope an external repo with rods. Panel documented by HOW EACH ROD
                           FAILED. Every batch carries a planted positive AND a planted near-miss
                           negative; a rod that misses either has its batch VOIDED. Keep that.
  aea/kernel/shadow.py     dev -> qa -> prod, 5 gate checks incl. one REAL model call. No promote().
  Meter.ceiling('nvidia')  4 concurrent, MEASURED. The declared constant was 20 and caused every
                           429 of the last session. Re-calibrate with rodprobe.calibrate().

HOW TO WORK HERE.

Be a filter, not a mirror. Name failure points before validating strengths. Disagreement is
wanted and only counts with a measurement.

Verify, do not claim. "Done" means it RAN: the gate returned 5 green checks, the test printed.

Every recorded failure has FOUR parts (law W8): the rule, the failure that paid for it, HOW IT
SHOULD HAVE BEEN BUILT, and WHY the knowledge that would have prevented it was present and not
applied. The fourth is the only one that stops recurrence.

At the SECOND repetition, extract it. Never test a regex or a path through a shell heredoc - the
Bash tool eats backslashes and it made the same diagnosis wrong twice. Drop to the primitive when
a tool fails on a source: WebFetch times out on build.nvidia.com, a plain urllib GET with a
browser User-Agent returns 200 and the whole page.

No emoji anywhere. No em dashes, ever. No negative parallelism ("it's not X, it's Y").

Nothing is committed until Luis asks. Privacy-scan first; selfcheck now verifies that the private
stores are GITIGNORED as well as clean. state/journey_save.json is sacred. Known-good is 44525f3 -
roll back to that, never to "the last commit".
```

---

## HOW TO INTERPRET THE HANDOFF (for the human)

**Part One section 1 is the load-bearing table.** Fifteen instrument defects. If a session proposes
trusting a stored number, that table is the argument for re-measuring first.

**Part Two section 9 is the one to read if you only read one.** The scout took four runs, three of
the four failures were the author's, and the fourth was three lines of clever code that silently
made every result empty. It is the clearest example in the repo of M9, and of why the planted
control is not optional.

**The rod facts live in `state/rods.json`**, reachable via `rodprobe.facts(rod)`, and that store wins
over any prose in the handoff.

**What is deliberately NOT next:** the board's visual work (E12 sections 4 and 6), the remaining 30
unwired modules, and the 43 unmeasured models. All real, all deferred by Luis in favour of outbound
capability.

**The NVIDIA skills are a pattern source, never a dependency.** Every one needs an NVIDIA SDK, an NGC
entitlement or a GPU cluster. Six patterns transfer and are listed in Part Two section 10; one of
them (verify ignore coverage before writing secrets) is already shipped as selfcheck's seventh
invariant.
