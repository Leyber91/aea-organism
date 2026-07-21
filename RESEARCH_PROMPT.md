# DEEP RESEARCH BRIEF — agentic infrastructure on genuinely-free LLM inference

> A reusable prompt. Paste into Claude Research (or run via the deep-research workflow). It briefs
> the researcher with what we ALREADY know so it builds on it instead of re-deriving it, then points
> at the unmapped frontier: NVIDIA's agent schemas, real per-model quality, and dynamic-but-not-lost
> agent paths.

## What we already know (build ON this — do NOT re-research the free-source list)
- We run a free-AI "grid": ~59 independent parallel nodes, ~2,234 requests/min measured, 6 online
  genuinely-free (no-card) plants:
  - **NVIDIA NIM** — no-train, 40 req/min PER MODEL with INDEPENDENT buckets (verified: 0/121 hit 429
    when all queried at once), 51 of 121 catalog models actually serve, full organ set.
  - **Groq** — no-train, sub-0.3s, gpt-oss-20b at 246 tok/s.
  - **Cerebras** — no-train, 1M tokens/day, gpt-oss-120b at ~0.7s.
  - **Z.AI GLM-Flash** — free reasoning + vision (public-data only).
  - **Ollama** — local, unlimited, private, RTX 3500 Ada 12GB, qwen3:8b ~27 tok/s warm.
  - **Pollinations** — keyless.
- We ran a 4-task battery (math-trap / instruction / JSON / code): 36 of 59 models scored 4/4.
- We built: an orchestrator (plan -> fan across buckets -> synthesize); a recursive swarm (each agent
  TRIAGES answer-vs-decompose, ramifies by depth, deep models at root / fast at leaves) with a
  propagate-trace + silent-wrong-work flag; and a local memory layer (mxbai embeddings) that grounds it.
- Framework = the AEA. **An agent = a prompt + a preprompt that follows a path.** Axes: P=Path
  (control flow), M=Multiplicity (how many models), A=Abstraction (memory/tools/tool-generation),
  R=Prompting, S=Async. We want paths that are DYNAMIC and FLEXIBLE but do NOT get lost.

## Research questions (rank every finding by how actionable it is for a free agentic swarm)

### 1. NVIDIA NIM agentic structures, blueprints & schemas  (HIGHEST PRIORITY — the unmapped part)
- Map ALL NVIDIA **agent blueprints / reference architectures** (build.nvidia.com "Blueprints", ~33):
  what each does, which are free / self-hostable, which run on the free hosted NIM tier.
- The **agentic schemas**: NVIDIA's tool-calling / function-calling format, structured-output / JSON-
  schema support, the **NeMo Agent Toolkit** (and NeMo Guardrails), any planner / agent-graph schemas.
- Which free NIM models support **tool-calling / function-calling / structured output / reasoning-
  with-tools** — list them with sources (model cards / API docs). This is what agents need.
- The exact OpenAI-compatible tool-calling API shape on NIM, and the multi-step agent patterns NVIDIA documents.

### 2. Real model quality — published benchmarks per FREE model  (refine our 4-task tiering)
- For the genuinely-free models (NVIDIA's servable set incl. nemotron-3-ultra/super/nano, deepseek-v4,
  qwen3-235b / qwen3-next-80b, mistral-large-3-675b, llama-3.3-70b, gpt-oss-120b/20b; Groq's; Cerebras's;
  Z.AI GLM-5/5.1): published scores on **MMLU-Pro, GPQA, IFEval (instruction-following), BFCL (tool-
  calling), HumanEval / SWE-bench (coding), long-context, multilingual.**
- Rank the free models by **agent role**: best free PLANNER, REASONER, CODER, TOOL-CALLER, VISION,
  and FAST/cheap — each with the benchmark evidence.

### 3. Dynamic, flexible agent paths that don't get lost  (the AEA path question)
- How do production agent systems make control flow **dynamic + flexible** without drifting, looping,
  or losing the goal? Survey: ReAct, Plan-and-Execute, Reflexion / self-critique, Tree-of-Thoughts,
  state-machine / graph orchestration (LangGraph etc.), supervisor / router patterns, and Anthropic's /
  OpenAI's agent-loop guidance.
- **Anti-drift mechanisms**: what keeps a swarm on-goal — memory / checkpoints, a supervisor that
  re-grounds, depth / budget caps, verification gates, structured handoffs. What is the MINIMAL
  fast-reacting control loop that adapts to change without getting lost?
- Map these to **agent = prompt + preprompt + path**: where does flexibility live (the path / control
  flow) vs where does stability live (the preprompt / guardrails / memory)?

### 4. Function-calling & structured output on the free sources  (the Phase-3 enabler)
- Which of NVIDIA / Groq / Cerebras / Z.AI / Ollama support OpenAI-style **tool-calling** and **JSON-
  schema structured output**, with the exact API shape and any limits. (Agents need this for tool use.)

## Rules
- Verify against official docs / model cards; cite sources; flag uncertainty; reject marketing claims.
- Prioritize what is ACTIONABLE for building a free agentic swarm NOW. Output a ranked, cited synthesis.
