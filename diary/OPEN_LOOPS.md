# OPEN LOOPS - everything today opened, and what to do with it

*2026-07-28. Written because Luis named the pattern himself: strong at proposing, weak at carrying.
The point of this file is not to hold work. It is to CLOSE loops, including by killing them.*

**The rule that makes this file useful:** every entry has a verdict. `FINISH`, `LATER`, or `KILL`.
An entry with no verdict is the disease this file exists to treat. If a `LATER` is still `LATER` in a
month, it becomes a `KILL`.

---

## THE FLOW OF THE DAY, in order

World 3 art -> run x24 -> question the whole instrument -> **the pivot: stop the game, prove the
assistant** -> deep research on autonomy -> goals + crystallization -> the discriminator ->
seven-dimension code review -> the xray -> shadow/self-modification -> selfcheck + heal -> the
declared-operation research -> the living graph -> reflection on reflection itself.

Nine kernel modules written. **Zero connected.** That is the day in one line.

---

## FINISH - small, and everything else is blocked behind them

| # | what | why it is first | size |
|---|---|---|---|
| 1 | **Wire `impasse`/`unstick` into the wake, and stop a failing brief starving the loop** | `loop/live.py:93` re-dispatches the failing brief every tick, so consolidate and reflect have not run for the whole outage. This is the eighteen-day incident, still live. It also gives Luis the daily recap he asked for. | 2 lines + a counter |
| 2 | **Commit** | 34 modified, 79 untracked. `known_good.json` is empty because the tool correctly refuses a dirty tree. **There is no version to roll back to.** Everything built today exists in one working tree. | one privacy-scanned commit |
| 3 | **The brief's stale date** | It presents a month-old private file as "Today". A live honesty-law violation in the one artifact that gets read. Flagged three times today, never fixed. | small |
| 4 | **Crashed/timed-out wake records nothing** | `loop/live.py:69`. The consecutive-failure alarm can never fire for the failure mode most likely to kill it. | small |
| 5 | **Heartbeat write sits outside the never-die guard** | `loop/live.py:171`. One failed save kills the forever-loop. | one line |

---

## LATER - real, evidenced, and not now

- **HADES's outage recorded as the worker's failure** (`organs/brief.py:166`). The verifier being down
  is not the worker being wrong. Needs a third verdict, not a boolean.
- **`gather_public` graded on a substring of the model's prose** (`brief.py:168`).
- **`seats.dispatch` grades "non-empty text" as a clean run** and discards the tool trace. My own
  code, same class as the defect I fixed in `hands.invoke` this morning.
- **The shape index.** A closed vocabulary for failure kinds (fail-open, self-graded,
  proxy-for-property, deadlock-by-precondition, stale-measurement, criterion-contamination) so
  experience is queryable by KIND. Prerequisite for any cross-domain search. Half a day.
- **Retrieval over `design/`** - 3.4 MB across 196 markdown files, invisible to any AST. Local Ollama
  embeddings. NOT over code, where the AST is exact.
- **Preconditions and effects on the action registry.** Two fields on a registry that already exists
  in three places. Turns selection into a query and makes "no action matches" a specification.
- **`propose_ceiling`** - the auditable, never-self-applied ceiling raise.
- **The liveness canary**, running outside the loop it watches.
- **The graph's next design pass** - package clusters do not separate, edges are uniformly weighted,
  no depth. It is good, not JARVIS-grade, and I said so.
- **11 disagreeing constants** from `heal.py`. `TEMP` at 0.0 and 0.2 across 14 files, `MAXTOK` at
  1200/300/320 across 6. Real, cheap, unglamorous.

---

## KILL - and here is the reasoning, because a silent drop is just a deferral

- **Migrating the other five model selectors onto `fit`.** They disagree, which is true and was worth
  finding. But four of them are only reached from code paths that are themselves orphaned. **Fixing a
  selector nobody calls is motion, not progress.** Revisit only when a caller becomes reachable.
- **55 "god-module" and 52 "swallowed-error" candidates.** The detectors are correct and the volume
  is the point: at that count they are a background reading, not a work queue. Act on one only when it
  is implicated in a real failure.
- **The 18 emoji in design docs.** House-rule violation, zero function, and a mass edit across 196
  files risks more than it fixes.
- **20 reboot experiments.** Deprioritised days ago and nothing since has needed them.
- **W3 image prompts 1/2/3/5.** The game is explicitly paused. Killing this frees the largest block
  of latent obligation on the board.
- **RAG over the codebase.** Decided against with evidence: the AST is exact where embeddings are
  approximate, and the measured embedding benefit at 108 files is +0.3%.
- **Live per-line execution tracing.** Weeks of work, answers a question nobody asked.
- **A container or microVM for candidate isolation.** Firecracker and gVisor are Linux-only, and a
  candidate running inside a VM measures a different machine, which breaks the honesty law. The Job
  Object plus subprocess timeout already in `shadow.py` is the right boundary for our own code.
- **`git history` rewrite for the employer path.** Luis has an agreement covering that machine. The
  working tree is clean and paths are anchored. Rewriting published history costs more than it buys.

---

## THE HONEST TALLY

    FINISH   5 items, all small, all in loop/live.py or one commit away
    LATER   10 items, all evidenced
    KILL     9 items, ~2 weeks of latent obligation removed from the board

**Nine killed against five to finish.** That ratio is the point of the exercise. The board was not
too long because the work is large. It was too long because nothing was ever taken off it.
