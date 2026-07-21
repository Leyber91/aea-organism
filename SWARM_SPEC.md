# THE SWARM SPEC — qualities, coordination, model policy (grounded in the Constellation Laws + measured data)

## 1. Qualities the swarm MUST have

| Quality | Why (law / evidence) | How we realize it |
|---|---|---|
| **Heterogeneity** | LAW 2: N clones share blind spots, amplify the same error, cost N×. Mix sizes/vendors/roles. | cross-vendor, cross-size node pool; council = solver + skeptic + synthesizer (under test now) |
| **Scale by composition** | LAW 1: capability lives in topology, not parameters. | plan→fan→synthesize; recursive ramification (pico→large by depth) |
| **Routing is cognition** | LAW 5: picking the right model IS the intelligence. | the crystallized router (pathfinder), tier ladder, role-assignment |
| **Every layer watched** | LAW 3 (SEDAH Law): autonomy without observation = unaccountable automation. | HADES watcher (does no work; judges vs goal; logs); silent-wrong-work flag |
| **Fit the hardware you own** | LAW 4. | free/local only; respect exact per-plant limits |
| **Resilient** | autonomy must survive its own limits. | per-bucket 429 cooldown + reroute; 50-concurrent → 9 reroutes, 0 lost (measured) |
| **Continuity / memory** | the backwards channel; "we can't talk forever." | genetic-memory capsule (relay); local mxbai grounding |
| **Crystallizing / self-improving** | search once, run cheap forever. | pathfinder learns type→model; relay crystallizes tools |
| **Bounded / non-drifting** | LLMs loop and drift. | depth/turn caps; goal re-injection (Focused ReAct, 18–530% gains on small models); explicit exit conditions |

## 2. How the swarm coordinates (the mechanisms, built + proven)

- **Plan → fan → synthesize** (orchestrator): a deep node decomposes, sub-tasks fan across INDEPENDENT
  buckets in parallel, a deep node merges. = ReWOO / orchestrator-workers (Anthropic: +90.2% vs single).
- **Recursive spawn (triage)**: each agent decides answer vs decompose vs escalate; ramifies by depth.
- **Genetic-memory relay**: predecessor → successor handoff via a state capsule {goal, crystallized
  tools, done}. Different models compose a result with no shared context (S-axis L5).
- **Crystallized routing**: learned type→model table; direct after the first search.
- **Council (vote / verify)** — MEASURED (v2/v3): heterogeneous models propose, then majority vote.
  RULE: easy task → ONE good model (a council only adds risk, v2); hard/unreliable task → DIVERSE VOTE
  of 3-5 distinct lineages (v3: rescued every hard question single failed, net +3, 0 damage; the win is
  model-diversity, not temperature — clones-vote ≈ single). A single VERIFIER/adjudicator is risky —
  it helped on easy tasks but on hard ones reasoned itself out of the crowd's correct answer; use it
  ONLY when the vote is split, never to override a clear diverse majority.
- **HADES oversight**: a heterogeneous watcher re-grounds or reroutes on drift; logs every verdict.
- **Resilient reroute (meter)**: a 429/at-limit on one bucket reroutes to a free one; never blocks others.

## 3. Model policy — which we USE, which we DON'T (from the measured battery + role research)

**USE — by role (all scored 4/4 on the battery / verified benchmarks):**
- Deep reasoning / planner: `gpt-oss-120b` (Groq/Cerebras/NVIDIA), `nemotron-3-super-120b`, GLM-5,
  `mistral-large-3-675b`, `nemotron-super-49b`.
- Tool-caller / instruction: **`llama-3.3-70b`** (IFEval 92.1, BFCL 77.3 — the safe default), Qwen3-235b.
- Fast / reflex (routing, classification, the watcher): **`groq/gpt-oss-20b`** (~939 tok/s), `gpt-oss-120b` on Groq.
- Vision: `nemotron-nano-12b-vl`, Z.AI `glm-4.6v-flash`.
- Local private base: Ollama `qwen3:8b` + `nomic-embed`.
- Deterministic offload: tools (`calc`, `json_get`) > asking a model to compute/parse.

**DON'T USE (measured failures / mismatches):**
- **Catalog-listed but not served** — e.g. `nemotron-ultra-253b` (404 "Function not found"). Census first.
- **Special-purpose models for general work** — `nemotron-content-safety`, vision-only, embed, guard,
  OCR, rerank models scored 4/4 on simple text so the router kept *picking them for reasoning* — wrong
  tool. POLICY: tag every node by TRUE purpose; the general-reasoning pool EXCLUDES safety/vision/embed/guard/ocr.
- **Slow reasoners for easy tasks** — crystallizing a 49B reasoner onto arithmetic made 50 tasks take 74s.
  POLICY: crystallize for COST — record the *fastest*-correct model per type, not the first that works.
- **`< 4/4` on the battery** — don't trust for unsupervised work.
- **Cerebras for interactive** — VERIFIED 5 RPM / 8K ctx → BATCH/LEAF only, never the hot loop.
- **Z.AI for parallel bursts** — ~1 concurrent → serialize it; public-data only.
- **Pollinations for anything critical** — keyless best-effort, no schema guarantee.
- **`enum` in Groq strict-mode schemas** — 400s; state options in the prompt instead.

## 4. The hardcore tests (what proves the qualities)
- **Heterogeneity vs clones** (`experiment_v2.py` easy / `experiment_v3.py` hard): single vs clones-vote vs
  hetero-vote vs hetero+verify on known-answer questions, objective grading, clones as the temperature control.
  RESULT: LAW 2 is REGIME-DEPENDENT — false on easy tasks (council hurts), CONFIRMED on hard ones (diverse
  vote rescues, net +3, 0 damage; clones-control proves it's diversity not sampling). See regime map in memory.
- **Resilience under load** (`test_resilient.py`, `stress_test.py`): 50-concurrent → reroutes, 0 lost. PASSED.
- **Genetic handoff** (`relay.py`): 5 distinct models build one toolkit via the capsule. PASSED.
- **Accountability** (`hades.py`): heterogeneous watcher gives a reliable strict-JSON verdict. PASSED.
- **Crystallization** (`pathfinder.py`, `stress_test.py`): learns type→model; payoff scales with search cost.
- TODO hardcore: adversarial drift (does HADES catch a deliberately wrong worker?), tool-failure recovery,
  privacy-boundary (does a `private` task ever reach a trains-zone node? must be 0), cold-restart resume.
