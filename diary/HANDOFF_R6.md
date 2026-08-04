# HANDOFF — R5 IS PROVEN. What it cost, how it was done, and what R6 inherits.

*Written 2026-08-04, at tick 819+. Supersedes `HANDOFF_R5.md`.*

---

## 0 · READ THIS FIRST — the one sentence that matters

**R5 was not blocked by a missing capability. It was blocked eight separate times by a capability
that existed, was correct, was reachable, and could not be SELECTED.** Every one was found by
measuring the ACTION, never by reading the code, because the code was never what was wrong. Unit
tests passed throughout. If you take one thing into R6, take that.

---

## 1 · WHERE THE LADDER STANDS

    R0   THE LOOP SURVIVES              PROVEN   246.9 h unattended, 0 crashes in 278 boots
    R1   THE DECISION IS READ           PROVEN   (original gate was unsatisfiable; recorded, not rewritten)
    R1.5 THE DECISION IS PARSED         PROVEN   419 valid, 19 receipts, 0 swallowed
    R2   THE DECISION IS A TOOL CALL    PROVEN   245+ invocations, 7 tools, bound = proof over the language
    R3   THE OUTCOME IS REMEMBERED      PROVEN   633+ outcomes, 148 not-repeated
    R4a  PERCEPTION IS A CHOICE         PROVEN   56/8 chosen-with-reason, 20 distinct sources
    R4b  PERCEPTION REACHES THE WORLD   PROVEN   0 leaks/16 requests · 27.86 bits/day · 7 dispatches, 2 topics
    R5   RESEARCH                       PROVEN   16/5 runs with a death · 25 DIED · 0 honesty violations
    R6   REFLECTION                     FUTURE   blocked_on: "R5 (material worth linking)" — that material now exists

**Verify it yourself, do not trust this file:** `python -m aea.tooling.ladder`

---

## 2 · HOW R5 WAS ACTUALLY ARRIVED AT — six stages

**01. The rung would not close and the reason was ASSUMED.** We believed the entity could not
infer. Nobody had checked.

**02. Reading its own reasoning showed the assumption was wrong.** The rod's deliberation was being
discarded at the socket on every call — `reason_share` **0.82**, so 82% of what it produced was
deleted before anyone read it. Once kept, tick 794 said, unprompted: *"the hades=unverified block is
now confirmed permanent until it flips — ticks 788–793 all say the same thing."* That is inference
across its own history. **The faculty was present and pointed elsewhere.**

**03. Its refusals were valid arguments from a premise nobody had checked.** 41 of 56 ticks chose
NONE, each reasoned. Tick 744 enumerates every move, rejects each with a cause, and concludes: *"MOVE:
NONE is correct for entity upkeep. The real service to Luis happens through our dialogue, not
mechanical moves."* The inference was sound. **The premise was that its moves are chores.**

**04. Four explanations, three killed by numbers rather than argument.**

| explanation | test | result |
|---|---|---|
| it does not KNOW it can | capability surface, 3+3 sandboxed replicates | ELIMINATED — it got WORSE. NONE 16 vs 7; 5 distinct moves vs 7 |
| it must be TOLD | the nudge, removed and counted for 24 h | ELIMINATED — **5× backwards**: 0.88% with it, 4.2% without |
| it needs a CRITIC | HADES, 69 verdicts | ELIMINATED — disagrees 30 times; one grep hit uses the verdict: a print statement |
| it holds nothing UNRESOLVED | contradiction A/B, run 1 | ELIMINATED — it held one, named it 12×, still did not act |

**05. The answer was that the menu said not to.** `check_a_belief` rendered in the entity's own menu
as **"(no description — do not pick this)"**, because `decide.WHEN` had no entry for it and `_moves`
fails closed. One dictionary entry and one routing clause later, the same experiment: **0 → 25
selections across 72 ticks.**

**06. The entity closed the rung itself.** It ran 15+ investigations unprompted, choosing the subject
from its own record: *"check_a_belief nvidia/mistralai/mistral-small-4-119b-2603 has 120 successful
calls out of 128 attempts but energy_usage.json says it cooled after 8 consecutive failures and
cannot answer."*

---

## 3 · THE METHODOLOGY — what to repeat

**MEASURE THE ACTION, NOT THE CODE.** All eight blockers had passing tests. Ask "has this ever
actually been chosen?", not "is this correct?"

**ELIMINATE BY MEASUREMENT, NEVER BY ARGUMENT.** Three explanations died to numbers. The fourth
survives only because the others were killed properly.

**EVERY EXPERIMENT NEEDS A CONTROL AND A DELIVERY CHECK.** The first contradiction A/B was an
observation, not a test: one arm, two variables changed at once. And an *undelivered* treatment
reads exactly like a null result — so `armed.py` compares `prompt_chars` across arms and reports
**INVALID** rather than a finding when they do not differ.

**PRE-REGISTER, INCLUDING THE UNINFORMATIVE BRANCH.** Then report the signal your own escape hatch
would have buried. The awareness run came back "uninformative"; the treatment arm had *doubled*
NONE, which was the opposite of the theory and worth more than the null.

**RETRACT RATHER THAN BANK.** Two deaths were caused by our own broken reader. Re-settled UNSETTLED
with the reason. The gate would have read 5 on evidence known to be false — **a gate met that way is
not a gate.**

**A RUN IS AN INVESTIGATION, NOT A CLAIM.** Twelve concurrent probes collided onto one run id. The
collision was a bug whose RESULT was correct: one question asked of twelve rods is one run. Fixing
it toward uniqueness would have met a five-run gate by widening a batch.

**THE CHEAP CHECK IS THE ONE NOTHING RE-READS.** D53, D54 and D55 share one shape: the expensive
reasoning was sound and the six-word line underneath it was never re-read. Attention follows effort,
not risk. Deliberately re-read the cheap part.

---

## 4 · THE TOOLS — what exists now and how to run it

    python -m aea.tooling.ladder              every rung, measured from disk
    python -m aea.lab.research_cert           R5's bound, certified independently
    python -m aea.lab.blockers                THE DEFECT HUNTER — 7 checks for unselectable capability
    python -m aea.lab.tests.test_r5           17 checks against the LIVE store
    python -m aea.lab.tests.test_wiring       15 checks, R0..R5 reachable
    python -m aea.kernel.hypotheses           20 checks, 10 controls, write-ahead enforced
    python -m aea.kernel.contradictions       what the record says that cannot both be true
    python -m aea.lab.armed --arm contradiction   the A/B harness, sandboxed + concurrent
    python -m aea.tooling.dossier --write     every number the pages show, computed once
    python -m aea.tooling.page.rungsite       19-route dossier under web/ladder/
    python -m aea.lab.recall "<what you are about to do>"   MEASURED 7/12 hit@5 — run it

**New modules:** `kernel/hypotheses.py` · `kernel/contradictions.py` · `lab/blockers.py` ·
`lab/armed.py` · `lab/fleet_check.py` · `tooling/dossier.py` · `tooling/page/{rung,rungsite,chapters}.py`
· `lab/tests/{test_r5,test_wiring}.py`. All in `graph.json._index.code` (229 nodes).

---

## 5 · THE DEFECT CLASS — eight instances, one shape

| # | where | what was wrong |
|---|---|---|
| 1 | R1's original gate | asked for an action the wake's surface could not express |
| 2 | `look_outward` | built, wired, budgeted, certified — and no MOVE named it |
| 3 | `response_format` | `"type" in schema` where a VALUE test belonged — **every schema call ever made was malformed** |
| 4 | `note_to_self` | the formatter's error written into memory — **430 of 739 entries were one string** |
| 5 | `check_a_belief` | in the tool registry; no move could name it |
| 6 | the standing block | a line appended past a cap already exactly full — silently truncated |
| 7 | `decide.WHEN` | rendered "(no description — do not pick this)" for five hours |
| 8 | `_read_stream` | first SSE line consumed for detection — **every streamed reply lost its first token** |

`aea/lab/blockers.py` now hunts this class on demand. **Run it before believing any negative result.**

---

## 6 · WHAT IS LEFT — in priority order

**1. DO NOT START R6 YET. Re-measure first.** Every behavioural conclusion in this document was
measured on a broken machine: memory was 58% error string, reasoning was discarded, every schema
call was malformed, every streamed reply lost a token. The NONE rate, the move distribution, the
"3.5% attention on rods", the "its moves are upkeep" premise — **all of it.** Let the loop run one
clean day and re-measure those findings before building on them.

**2. The entity still cannot see its own claims.** `kernel.hypotheses:state` is read by the console
and by nothing the organism runs. It is the single entry on `test_wiring`'s `KNOWN_UNWIRED` list,
with its reason. Fixing it is the natural first move toward R6.

**3. Two thirds of every tick is unmeasured.** Only `core()` is instrumented. `structure` and
`hades` have no timing record at all, and HADES keeps a verdict with **no prompt** — so the judge
that disagrees 43% of the time cannot be audited on what it was shown.

**4. The record is thin where R6 needs it thickest.** Memory is 819 entries and the wake sees **6**
(0.8%). There is **no salience field**, so nothing in this system can matter more than the last six
ticks — a formative memory is structurally impossible. R6 is about linking memories; it needs both.

**5. 51 lessons the entity cannot read.** `DISCOVERIES.md` holds principles welded to the failures
that paid for them. `recall.py` retrieves them at 7/12 hit@5 — and is wired to the ASSISTANT reading
the repo, never to the entity living in it.

---

## 7 · WHAT R6 SPECIFICALLY INHERITS

R6: *"Derive a memory from several memories, store it competing with its own sources, and retrieve
it later in a real decision."* Bound: **untraceable provenance.**

**Now available that was not:** 68 claims with hashed, cited, walkable evidence · a memory that is
no longer 58% error string · `hypotheses.settle()`'s write-ahead rule, which is exactly the
provenance discipline R6's bound demands, already built and controlled.

**The law that carries up:**

> **A rung above R4 fails at the PREMISE, not the mechanism.** Build the mechanism and it will sit
> unused behind a correct argument. Find out what the entity believes its job is FIRST — and check
> the cheap thing nothing re-reads: *can it name this move at all?*

---

## 8 · SECURITY — done 2026-08-04, do not redo

A full sweep of the tree and all 250 commits. **CRITICAL: zero — no key, token or private key has
ever been committed.** 307 HIGH hits in history purged via `git filter-repo`; both remotes
force-pushed. `thinking.jsonl` is permanently gitignored — it reasons about private circumstances
every tick and cannot be redacted without destroying its purpose. A verified 281 MB pre-rewrite
bundle exists in the session scratchpad. **Every SHA changed: re-clone, do not pull.**
