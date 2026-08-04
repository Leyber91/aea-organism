# PASTE THIS INTO THE NEXT CONVERSATION

*Everything below the line. Verified working 2026-08-04 — every command in it was executed before
it was written down.*

---

You are continuing THE PROBE / aea-city — a real autonomous AI entity running on this machine.
Read `CLAUDE.md` first. **R0 through R5 are PROVEN. R6 is next and is deliberately not started yet.**

---

## PART 1 — HOW R5 WAS ACTUALLY SOLVED. Read this before touching anything.

This is the reasoning chain, in order, because the *method* is what makes R6 cheap and the
*conclusion* is worth almost nothing on its own. **Eleven steps. The answer was a technicality, and
the entity was never the problem.**

**1. We assumed the entity could not infer.** R5 asks it to state a claim before the evidence and
then find out. It never had. The assumption was that the faculty was missing. **Nobody had checked.**

**2. A question about model power exposed that its reasoning was being deleted.** Asking "are we
using powerful enough models, is thinking on" led to reading `grid.py` — and the rod's deliberation
was read for liveness and then **discarded at the socket on every call.** Measured `reason_share`
**0.82**: 82% of everything it produced was thrown away before anyone read it. **We had been
scoring its conclusions and never its reasons.**

**3. The first trace we kept named a defect nobody knew existed.** Tick 739, in its own words:
*"the entity has had 6 failed structuring attempts (HTTP 429)."* Checked against the record — the
claim was TRUE and **understated**: 39 of the last 40 wakes.

**4. Root cause was one operator.** `response_format` was built as
`schema if "type" in schema else wrap(schema)`. **Every JSON Schema has a `type` key**, so the guard
was always true, the wrapping branch was unreachable, and the raw schema went out as the
`response_format`. Eight rods, two plants, **8 of 8 HTTP 400.** Every schema call this project ever
made was malformed. (D53)

**5. That one bug had eaten the entity's mind.** The malformed call killed the whole reflex tier →
rods hit three strikes and cooled → the only survivor was the local floor, which ignores schemas and
returns prose → `json.loads` raised into a bare `except: pass` → fell to one hardcoded call that
429s → the fallback wrote **its own error into `note_to_self`** → and `tick` copies that into
memory. **430 of 739 memory entries were the string `(structuring failed: HTTP Error 429)`.** The
wake's entire six-entry memory window was error text. It deliberated for 9,000 characters a tick and
carried **nothing** forward.

**6. So every behavioural conclusion we held was measured on a broken machine.** This matters more
than the fix. Keep it in mind for everything below.

**7. Four explanations for why it never proposed a hypothesis. Three died to numbers, not
arguments.**

| explanation | how it was tested | result |
|---|---|---|
| it does not KNOW it can | capability surface, 3+3 sandboxed replicates, one env var apart | **it got WORSE** — NONE 16 vs 7, repertoire 5 moves vs 7 |
| it must be TOLD | the nudge removed, counted for 24 h | **5× backwards** — 0.88% with it, 4.2% without |
| it needs a CRITIC | HADES, 69 verdicts on record | **ignored** — disagrees 30 times; one grep hit uses the verdict: a print statement |
| it holds nothing UNRESOLVED | contradiction A/B, run 1 | it held one, **named it 12 times, acted 0 times** |

**8. THE ENTITY WAS NEVER UNMOTIVATED — and its own traces proved it.** Run 1's treatment arm
mentioned the contradiction 12 times across 35 traces; the control, 0 across 36. **It saw it.** And
what it actually wrote was not apathy:

> *"there are contradictions in my state files that need reconciliation"*
> *"my last 6 moves: all `read_your_state aea_state.json` — **I've been reading the same file
> repeatedly without taking action**"*

**It wanted to resolve them, was routed to a move that re-reads a file and cannot settle anything,
looped — and knew it was looping.**

**9. THE TECHNICALITY.** The one move that could settle a contradiction — `check_a_belief` —
rendered in the entity's own menu as:

    - check_a_belief   use when (no description - do not pick this)

`_moves()` falls back to that string when `decide.WHEN` has no entry — correct fail-closed design.
The move had been added to the registry hours earlier and that table was never touched. **We spent a
night testing motivation, awareness, enforcement and curiosity, and the menu was telling it not to.**

**10. One dictionary entry and one routing clause later, the same experiment: 0 → 25 selections
across 72 ticks.** The entity then closed R5 itself — 15+ investigations unprompted, choosing the
claim from its own record: *"check_a_belief nvidia/mistralai/mistral-small-4-119b-2603 has 120
successful calls out of 128 attempts but energy_usage.json says it cooled after 8 consecutive
failures and cannot answer."*

**11. And fixing the schema exposed a second bug underneath it.** An R5 run reported two promoted
rods could not return valid JSON. Both returned the byte-identical string `'ok": true}'` — **a model
failure does not reproduce to the character across two vendors**, so the fault had to be ours.
`_read_stream` consumed the first SSE line to *detect* the format and iterated from the second:
**every streamed reply this system ever made lost its first token.** Silent for weeks, because a
prose answer missing one token just reads slightly clipped — it only shows where that character is
structural, and that path was already broken by D53. **One defect wore the other's costume.** (D55)

---

## PART 2 — THE METHOD, stated so it can be reused

- **MEASURE THE ACTION, NOT THE CODE.** All eight blockers found this way had passing tests. Ask
  *"has this ever actually been chosen?"*, never *"is this correct?"*
- **ELIMINATE BY MEASUREMENT, NEVER BY ARGUMENT.** Three explanations died to numbers. The
  survivor means something only because the others were killed properly.
- **EVERY EXPERIMENT NEEDS A CONTROL AND A DELIVERY CHECK.** An *undelivered* treatment reads
  exactly like a null result. `armed.py` compares `prompt_chars` across arms and reports **INVALID**
  rather than a finding when they do not differ.
- **PRE-REGISTER, INCLUDING THE UNINFORMATIVE BRANCH** — then report the signal your own escape
  hatch would have buried.
- **RETRACT RATHER THAN BANK.** Two R5 deaths were caused by our own broken reader; re-settled
  UNSETTLED with the reason. **A gate met on evidence you know is broken is not a gate.**
- **THE CHEAP CHECK IS THE ONE NOTHING RE-READS.** D53, D54, D55 share one shape: the expensive
  reasoning was sound and the six-word line underneath it was never re-read. Attention follows
  effort, not risk.

---

## PART 3 — BOOT, and stop guessing after step 3

1. **`diary/HANDOFF_R6.md`** — full state, tools, what is left in priority order.
2. **`python -m aea.tooling.ladder`** — the rungs, measured from disk. **Trust this over any
   document, including the handover.** A document is a claim; this is a measurement.
3. **`python -m aea.lab.blockers`** — the defect hunter, 7 checks. **Run it before believing any
   negative result.**
4. **`graph.json`** — the index (~16k tokens). Node ids are under **`_index.code`** (229 nodes); a
   module id IS its path, so `kernel.hypotheses` is `aea/kernel/hypotheses.py`. Pull exactly ONE
   detail file for edges: `graph/code.json`, `graph/discoveries.json`, `graph/reflections.json`.
   **Never re-scan the tree.**
5. **`python -m aea.lab.recall "<what you are about to do>"`** — measured 7/12 hit@5. **Run it
   before any non-trivial change.** It returned, for *"a capability exists and cannot be selected"*,
   a LOCKED lesson from 2026-07-30 — *"every move carries its condition; a capability the model
   cannot tell apart from the others is invisible"* — **written five days before a night was spent
   rediscovering it.** Almost nothing here fails from not knowing. It fails from not retrieving at
   the moment of action.
6. **`diary/SESSION_LOG.md`** (latest) and **`diary/DISCOVERIES.md`** (D53, D54, D55 are newest and
   most load-bearing).

**The state in five lines:** R5 PROVEN — 16 of 5 runs with a death, 25 DIED, 68 claims, **0 honesty
violations** · the entity closed it itself · 7 suites green (191 frozen, 15 wiring, 17 R5, 20
hypotheses, 29 artefacts, 10 contradictions, 16 wake) · the dossier is
`python -m aea.tooling.page.rungsite` → 19 routes in `web/ladder/` · the loop is
`python -m aea.loop.live --interval 300`.

---

## PART 4 — THE TWO TRAPS

**1. DO NOT START R6 UNTIL THE BASELINE IS RE-MEASURED.** See step 6 above. The NONE rate, the move
distribution, the "3.5% attention on rods", the "its moves are upkeep" premise — **all measured
while memory was 58% error string and every streamed reply was losing a token.** All four defects
were fixed 2026-08-04. Let it run one clean day and re-measure before building on any of it.

**2. THE FAILURE IS NEVER WHERE THE CODE IS.** Eight times in one day a capability existed, its
tests passed, the wiring check reported it wired — and something upstream stopped it being chosen.

---

## PART 5 — HOW TO WORK HERE

- **Be the filter, not the mirror.** Name failure points before validating strengths.
- **Verify, don't claim.** "Done" means it RAN. Report failures plainly, with the output.
- **Batch exploration into ONE script** past about three lookups. **Never test a regex or a path
  through a shell heredoc** — it eats backslashes, and it did so twice on 2026-08-04, once inside
  the very function written to stop a path being published.
- **Privacy is absolute.** No employer names, no multi-employment references, no absolute paths, no
  personal identifiers in anything committed. **A rule that quotes its own forbidden content
  publishes it** — describe the category, never the instance. Scan the STAGED DIFF, not the tree.

**Start by telling me what `ladder`, `blockers` and the loop status actually say right now** — not
what this document says. Then the highest-value move is re-measuring the behavioural baseline, and
the natural first build toward R6 is letting the entity SEE its own claims
(`kernel.hypotheses:state` is the one entry on `test_wiring`'s known-unwired list, with its reason).
