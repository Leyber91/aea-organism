# THE AEA PROOF PLAN — prove every axis, seed, verb, mechanic & op on the live grid

**The point.** The AEA has always had ONE gap: no running demonstration (it scores 50 on its own
honesty decoder — "authored, not run"). This plan closes it. Every element of the framework gets a
**real-time test on the grid we built** (59 nodes, ~2,234 req/min), directed by the orchestrator,
each with a falsifiable pass criterion and an evidence artifact. When the scoreboard is green, the
AEA is a running system, not a document — and that running system IS the portfolio centerpiece.

> Grounding caveat: the AEA structure below is the survey-extracted version. Cross-check each
> element against the canonical Paradigm Book (site `_reference`) as we execute — do not let a test
> drift from canon.

## The machinery every test runs on
- **Orchestrator** (`orchestrator.py`) directs traffic: plan → fan across buckets → synthesize.
- **Propagate trace** = the swarm reporting each agent's task → node → output as a live causal log.
  This is the `propagate` verb itself AND the evidence layer for every other proof. (Phase 1.)
- **Tool use** powers the A-axis: agents calling web/search/calc/code-exec/the skill library.
- **Meter** = ceiling-detect · **anonymize-guard** = boundary preservation · **memory** = backwards channel.

---

## The proof matrix (element → real-time test → traffic → PASS → status)

### 5 AXES (locate the system at a level, then prove the level runs)
| Axis | Test on the grid | Traffic | PASS when | Status |
|---|---|---|---|---|
| **P · Path** (control flow) | orchestrator where the NEXT step depends on a prior result (dynamic re-plan, not a fixed DAG) | deep node re-plans mid-run | a run branches on an intermediate result | L3 proven · L4 to-build |
| **M · Multiplicity** | N role-differentiated nodes + synthesizer on one task | fan across distinct buckets + synth | merged output beats the best single node (measured) | L3 proven · L4 to-prove |
| **A · Abstraction** | agent that retrieves memory (L2), calls a tool (L3), writes+uses a new skill (L4) | tool-using node | completes a task impossible without the tool/memory | to-build (Ph 2–3) |
| **R · pRompting** | a frontier-encoded scaffold makes a cheap node beat its raw self | deep encodes → cheap runs | cheap+scaffold score > cheap raw on a task | to-build (Ph 4) |
| **S · aSync** (time) | scheduled unattended run + parallel pipeline | cron → orchestrator, no human | a run completes + logs overnight | L2 proven · L4 to-build (Ph 5) |

### 10 SEEDS (the organs — prove each is present & firing)
| # | Seed | Real-time test | PASS | Status |
|---|---|---|---|---|
| 1 | substrate | grid dashboard + capacity probe | 59 nodes answer | **PROVEN** |
| 2 | sharp objective | every test carries a falsifiable scorer (an eval) | output graded 0/1 | PROVEN (battery scorers) |
| 3 | crystallize | freeze a repeated behavior into a reusable scaffold/skill | re-run cheap node w/ scaffold, score up | forge proved offline; prove in-loop (Ph 4) |
| 4 | flexibilize | kill a node mid-run → router falls back | task still completes | to-build (Ph 6) |
| 5 | self-version | a run writes a NEW skill to the library + uses it next run | next run invokes it | to-build (Ph 4) |
| 6 | self-model | orchestrator answers "what am I made of?" from its own registry | correct self-report | grid/city = this; make queryable (Ph 1) |
| 7 | ceiling-detect | meter flags a plant at rate-limit AND a quality gate flags a low score → escalate to deeper node | escalation fires | rate=proven; quality-ceiling to-build (Ph 4) |
| 8 | transcendence toolset | agent invokes ≥3 distinct tools | all 3 succeed | to-build (Ph 3) |
| 9 | boundary preservation | a `private` task NEVER routes to a trains-zone node; anonymize-guard catches a leak | 0 leaks, guard fires | zone-filter partial; prove enforcement (Ph 6) |
| 10 | persistent backwards channel | run A writes a memory capsule; fresh run B reconstitutes + continues | B uses A's context | to-build (Ph 2) |

### 3 VERBS (the per-tick rail)
| Verb | Test | PASS | Status |
|---|---|---|---|
| **compose** | assemble subtask results into a whole | coherent synthesis | **PROVEN** (synth step) |
| **propagate** (honesty node) | live trace: each subtask input→node→output, + a "silent-wrong-work" flag when a node returns but fails its eval | trace renders, bad work flagged | to-build (Ph 1) |
| **observe** | meter telemetry + city render + the trace | state is visible | meter/city proven; +trace |

### 4 MECHANICS (between-tick growth) = seeds 3/4/5/7 — proven via those rows.

### 4 OPS (the operator loop)
| Op | Test | PASS | Status |
|---|---|---|---|
| **design** | orchestrator tags a task with the axis-levels it needs before running | tags present | to-build (Ph 1) |
| **time** | every tick timestamped + observable | timeline renders | to-build (Ph 1) |
| **ship** (unskippable) | a run produces a REAL external artifact (file/draft/posted) | artifact exists | partial (text); prove a deliverable (Ph 5) |
| **learn** | a run's result improves the next (memory/crystallize) | measurable lift | to-build (Ph 4) |

### 3 PRINCIPLES (emergent properties, proven by the above)
- **emergence over imposition** → P-L4 (entity defines its own steps) · **restorable coherence** → flexibilize + boundary (Ph 6) · **operator-observable time** → the trace + city (Ph 1).

---

## Phases (each ships proofs + evidence, smallest-first, reusing what exists)

- **Phase 0 — already proven (the grid run).** substrate · M-L3 · compose · observe(partial). Evidence: `test_capacity.py`, `test_battery.py`, `orchestrator.py` run.
- **Phase 1 — Propagate / observability.** Build the live trace: every agent reports task→node→output→eval, timestamped, with a silent-wrong-work flag. *Proves:* propagate, observe, self-model, ops design+time, operator-observable-time. **This is the swarm-awareness layer you asked for.**
- **Phase 2 — Memory (backwards channel).** Local mxbai/nomic embeddings → a store the orchestrator reads and INJECTS into every subtask. *Proves:* A-L2, R-L3, seed-10. (The orchestrator run proved this is non-negotiable — without it the swarm hallucinates.)
- **Phase 3 — Tool use.** Give agents tools (web/search/calc/code-exec/skills). *Proves:* A-L3, seed-8 transcendence toolset. ("tool use there is a lot.")
- **Phase 4 — Growth.** crystallize a scaffold → cheap node beats raw; quality-ceiling escalation; self-version writes a new skill. *Proves:* R-L4/5, seeds 3/5/7, mechanics, op-learn.
- **Phase 5 — Async + ship.** Scheduled unattended run that produces a REAL artifact. *Proves:* S-L4, op-ship, op-time.
- **Phase 6 — Safety / robustness.** Boundary enforcement (private never leaves its zone, anonymize-guard) + flexibilize fallback. *Proves:* seeds 9/4, restorable coherence.

---

## The scoreboard (the AEA's own honesty decoder for "is it running")
A live table of all ~26 elements × {PLANNED · IN-PROGRESS · PROVEN} + evidence link, regenerated as
each test passes. Render it INTO the city (each proven element lights a building gold). When it's
all gold, the AEA is demonstrably alive — and we screenshot that for the portfolio.

**Recommended start:** Phase 1 (the trace — your swarm-awareness) + Phase 2 (memory — the grounding
the last run proved we need). Those two turn the orchestrator from a powerful-but-blind machine into
an observable, truthful one — and they light up the most AEA elements per unit of work.
