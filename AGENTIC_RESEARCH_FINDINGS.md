# Agentic infrastructure on free inference — CORRECTED canonical findings (2026-06-27 v2)

> Supersedes the workflow-recovered v1. Source: Luis's Claude Research run of RESEARCH_PROMPT.md
> (richer, live-console numbers) + our own grid verifications. Where the two disagree, our measured
> grid data wins (noted inline).

## Corrections that change the build (read these first)
- **Cerebras free tier downgraded:** report says **5 RPM / 30K TPM / 8,192-token context cap** on
  gpt-oss-120b + GLM-4.7 only (was 30 RPM / 1M-tok-day in our grid). VERIFYING live (test_cerebras.py);
  if confirmed, Cerebras = BATCH/LEAF only, not interactive. grid.py updated accordingly.
- **Nemotron-3-Super-120B free availability was "disputed" in the report — RESOLVED by our data:** it
  serves on our free NVIDIA NIM key and scored 4/4 at 59 tok/s in our battery. It IS free-hosted for us.
- **Z.AI API content is NOT used for training** (opt-in only, per Z.AI Terms of Use) — only consumer-chat
  + public web feed foundation training. So Z.AI's *API* tier is effectively no-train; promotable from
  "public-only" to private-safe after a ToS re-confirm. (Keep conservative until confirmed.)
- **Blueprint count is 44** (32 "Launchable", 12 Enterprise, 1 Dev), ~32 NVIDIA-AI — not ~33/37.
- **Throughput:** gpt-oss-20b on **Groq ~939 tok/s** (not 246; 246 was gpt-oss-20b on NVIDIA NIM);
  gpt-oss-120b on **Cerebras ~2,042 tok/s**. Plant matters.

## 1. NVIDIA agentic stack (free + open)
- **NeMo Agent Toolkit (NAT v1.8)** — Apache-2.0, `pip install nvidia-nat`, framework-agnostic
  (LangChain/LlamaIndex/CrewAI/Semantic-Kernel/ADK). YAML config: `llms: {_type: nim, model_name: ...}`
  + `workflow: {_type: react_agent, tool_names, llm_name, parse_agent_response_max_retries: 3}`. Full
  **MCP (client+server) + A2A**, Phoenix tracing, eval harnesses, parallel/speculative "Agent
  Performance Primitives". Runs free on NIM with NVIDIA_API_KEY; runs in Colab.
- **AI-Q blueprint** = LangGraph state machine: orchestration node (classify meta-vs-research, set
  shallow/deep depth in ONE step) + bounded shallow researcher + deep researcher + clarifier. **This is
  a reference implementation of our orchestrator + triage-swarm.** Built on LangChain DeepAgents + NAT.
- **NeMo Guardrails** — Colang rails (input/dialog/retrieval/execution/output); **dialog rails** =
  native topical on-path enforcement (anti-drift), model-agnostic.
- 44 blueprints incl. Safety-for-Agentic-AI, Retail Assistant (LangGraph), Enterprise RAG (MCP server,
  query decomposition, RAGAS eval), Data Flywheel (continuous agent optimization).
- CAVEAT: blueprints' heavy multimodal/3D parts assume local GPUs; the LLM-driven parts run free by
  pointing the OpenAI client at https://integrate.api.nvidia.com/v1.

## 2. Function-calling & structured output (the Phase-3 message bus)
| Plant | Tool-calling | Structured output | Hard limits |
|---|---|---|---|
| **NVIDIA NIM** | OpenAI `tools`/`tool_choice`/`parallel_tool_calls` | `nvext.guided_json` (NVIDIA-recommended) + guided_regex/choice/grammar; newer NIMs accept `response_format:json_schema` | SGLang containers support response_format but NOT nvext guided_*; verify per model card |
| **Groq** | OpenAI `tools` + parallel | `response_format:{json_schema, strict:true}` = constrained decoding, 100% adherence | **streaming + structured-output CANNOT combine**; strict only on gpt-oss-20b/120b |
| **Cerebras** | OpenAI `tools` | `response_format:{json_schema, strict:true}` (subset; required arrays need additionalProperties:false) | **`tools` and `response_format` CANNOT be in the same request**; 5 RPM/30K TPM/8K ctx |
| **Z.AI (GLM)** | native OpenAI `tools` | `response_format:json_object` (glm-5/4.7/4.5/4.6); GLM-4.7 adds JSON-schema | GLM-4.6V-Flash = free vision + native function-call, 128K |
| **Ollama (local)** | OpenAI `/v1` tool-calling (qwen3 etc.) | `format:json` / json-schema | unlimited/private; ~27 tok/s warm |
| **Pollinations** | best-effort, not schema-guaranteed | no | keyless fan-out only |

## 3. Anti-drift: dynamic paths that don't get lost (rank-ordered, actionable)
1. **Explicit state machine + checkpoints (LangGraph)** — >60% of production agent incidents are state
   management (LangChain 2026 report). Typed shared state, conditional edges bound loops, checkpointer
   makes runs resumable.
2. **Focused ReAct (goal-reiteration every step + early-stop on repeated action)** — **18-530% accuracy
   gains, -34% runtime** on SMALL models (Gemma-2-2B, Phi-3.5-mini, Llama-3.1-8B). HUGE for our cheap
   swarm. (Li et al., arXiv 2410.10779.) ← cheapest highest-leverage win.
3. **Supervisor / lead re-grounding (orchestrator-worker)** — beat single-agent by 90.2% (Anthropic).
   Each subtask gets objective + output format + tool guidance + clear boundaries. Evaluate FINAL state.
4. **Verification gates / evaluator-optimizer** with explicit halt conditions.
5. **Hard depth/iteration/token caps** — guard the documented "broke tool, called it 400× in 5 min".
6. **NeMo Guardrails dialog rails** for topical enforcement.
- MINIMAL loop: bounded ReAct wrapped in a graph with (a) goal re-injected each step, (b) hard cap,
  (c) early-stop on repeat, (d) checkpoint per node, (e) one evaluator gate before finish.
- AEA MAP: **flexibility = Path (edges, dynamic decomposition, next-action choice); stability =
  preprompt + guardrails + checkpointed memory.** Flexible interior, hard boundary.

## 4. Best free models by role (published benchmarks)
- **Planner/Reasoner:** GLM-5 (GPQA 86.0, SWE 77.8, τ²-bench 89.7) or gpt-oss-120b (MMLU 90, GPQA 80.9
  w/tools) — gpt-oss-120b is free+fast on Cerebras/Groq; Nemotron-3-Super-120B for NVIDIA-native.
- **Coder:** GLM-4.7/GLM-5 (SWE 73.8/77.8) or Qwen3-Coder-480B; gpt-oss-120b (SWE 62.4) = fast option.
- **Tool-caller:** GLM-4.5 (BFCL v3 77.8), Qwen3.5-122B (BFCL-v4 72.2, IFEval 93.4); **Llama-3.3-70B
  (BFCL v2 77.3, IFEval 92.1) = safest OpenAI-format default.**
- **Vision:** GLM-4.6V-Flash (free) or Nemotron-3-Nano-Omni.
- **Fast:** gpt-oss-20b on Groq (~939 tok/s) / Cerebras; Nemotron-3-Nano.

## Build order (from the report, adapted)
1. **Wire Phase-3 tool-calling as the swarm's message bus** — standardize handoffs on OpenAI `tools`;
   enforce JSON with Groq strict (leaf planners), NIM nvext.guided_json (NIM nodes). Respect the XOR
   limits (Groq no-stream+structured; Cerebras no tools+response_format). Threshold: 0 parse fails / 200 calls.
2. **Install the anti-drift envelope** — goal-reiteration each step (Focused ReAct), hard caps,
   early-stop-on-repeat, checkpoint per node, one evaluator gate. (We have depth-cap + capsule already.)
3. **Role-assign by benchmark** (table above), not vibes; re-confirm free availability per console.
4. Study (don't necessarily adopt) AI-Q + NeMo Agent Toolkit for the LangGraph state-machine + hard-caps pattern.

## Watch-outs
- Rate limits are not SLAs (NIM ~40 RPM model/traffic-dependent; Cerebras now 5 RPM). Add exponential
  backoff + Retry-After; fall back NVIDIA->Groq->Cerebras->Ollama.
- Keep sensitive data on Ollama-local; hosted endpoints log prompts (Z.AI API excepted per ToS).
- Specs move fast — the live build.nvidia.com console + model cards + provider rate-limit docs are ground truth.
