# THE GRID — the AEA entity's energy catalogue

The city's electricity. Every model the entity can run, classified by the only two axes that
matter for an always-on **personal** entity: **is it really free** (no card, recurring) and
**does it train on your data** (privacy zone). Machine-readable registry: `energy.json`.
Live engine: `grid.py`. Inspector: `probe.py`. Generated from a verified 11-provider sweep
(each claim checked against the provider's own pricing page) + live probes, 2026-06-24.

---

## THE VERDICT — which plants are GENUINELY free (you asked: many aren't)

### Tier A — genuinely free, NO credit card, recurring. Worth a key.
| Plant | Zone (privacy) | Free ceiling | For the entity |
|---|---|---|---|
| **Ollama** (have) | residential · local | unlimited, private, offline | the 24/7 base load — embeddings, routing, cheap reasoning |
| **NVIDIA NIM** (have) | residential · no-train | 40 rpm/model × 121 models | the full organ set on one key — VERIFIED live |
| **Groq** (have) | residential · no-train | 30–60 rpm | fast — VERIFIED live (0.28s, 50/50 burst, 0 throttle); WAF blocks VPN IPs |
| **Cloudflare Workers AI** | residential · no-train | 10,000 neurons/day (hard-stop, no bill) | edge + embed/rerank/ASR; no-train ★ |
| **SambaNova** | residential · no-train | 20 rpd/model × 6 ≈ 120/day | fast reasoning; no-train ★ |
| **Cerebras** | residential · no-train | 1,000,000 tokens/day | fastest inference; no-train ★ |
| **OVHcloud (EU)** | residential · no-train | keyless 2 rpm / 400 rpm with a free token | EU, GDPR, no-train; full stack ★ |
| **Pollinations** | outskirts · no guarantee | 1 req / 15s, keyless | zero-setup fallback — VERIFIED live, no signup |
| **Gemini (AI Studio)** | industrial · TRAINS | ~1,500 rpd/model | huge/fast — **PUBLIC data only** |
| **Mistral (EU)** | industrial · TRAINS | ~1 billion tokens/month, 2 rpm | omni, big budget — **PUBLIC only** (opt-out exists) |
| **OpenRouter** | industrial · TRAINS | 50 rpd free (1,000 after a one-time $10) | 22 SOTA :free models — **PUBLIC only** (must enable logging) |

### Tier B — free but a killer caveat. Limited use only.
| Plant | The catch |
|---|---|
| **Cohere** | 1,000 calls / **MONTH**, and the trial is **NON-COMMERCIAL + "not for personal/household use."** Best reranker on the planet, but the license is wrong for a personal/paid entity. Rerank-only, sparingly. |
| **GitHub Models** | **Closed to new customers (2026-06-16) and officially RETIRING.** Only usable if your account already had access. Never build the spine on it. |
| **Hugging Face** | Only **$0.10/month** of credit. A routing/failover + embeddings dabble, not a workload engine. |

### Tier C — NOT really free. Checked and EXCLUDED. Don't waste time.
| Plant | Why it's out |
|---|---|
| **Together AI** | the `-Free` lane is unstable/rotating + inconsistent; embeddings/rerank are paid. |
| **Fireworks** | one-time **$1** credit, no recurring free tier. |
| **Nebius** | $1 / 30-day trial, **credit card MANDATORY at signup**. |
| **Hyperbolic** | $1 phone-verify promo (not even GPU-usable); $5 deposit to actually use. |
| **Scaleway** | one-time 1M-token trial, **payment method required on file** even to spend it. |
| **Chutes** | **no free tier remains** — pay-as-you-go / paid subscriptions only. |

**Bottom line:** besides Groq + NVIDIA, **8 more are genuinely free with no card** (Cloudflare,
SambaNova, Cerebras, OVHcloud, Pollinations, Gemini, Mistral, OpenRouter). 3 are caveated
(Cohere, GitHub, HF). 6 are fake-free (Tier C) — already excluded from `.env`.

---

## The two axes the city is zoned by

**Privacy (zoning).** Residential = no-train, safe for your private day. Industrial = trains on
free-tier prompts, public data only. You don't put a data-harvesting plant in a residential zone.
- **No-train (private-safe):** Ollama (local), NVIDIA, Groq, Cloudflare, SambaNova, Cerebras, OVHcloud.
- **Trains-by-default (public-only unless opted out):** Gemini, Mistral, OpenRouter, GitHub, Cohere.
- **No guarantee:** Pollinations, HuggingFace (per-partner).

**Throughput (the real wall).** Almost none of these sustain a heavy real-time loop alone —
they're scheduled/batch brains. The entity's true capacity = the **union, load-balanced** across
plants, with Ollama (unlimited, local) carrying the heartbeat. That's why we mapped all of them.

---

## The runtime stack — 4 rings (the crystallize doctrine, as a city)

- **Ring 0 — local base (Ollama):** unlimited, private. The 24/7 heartbeat: embeddings (mxbai),
  routing, classification, cheap reasoning. Never rate-limited, never leaks.
- **Ring 1 — private-safe hosted (no-train):** quality/speed bursts on PRIVATE data —
  Cloudflare, SambaNova, Cerebras, NVIDIA, OVHcloud.
- **Ring 2 — public hosted (trains):** high-throughput scanning of PUBLIC data only —
  Gemini, Mistral, OpenRouter, Groq.
- **Ring 3 — specialist/fallback:** Cohere rerank (high-value only), Pollinations (keyless), HF (failover).

**Routing rule (enforced by `grid.py`):** private data → ring 0/1 only. public data → ring 2 ok.
heartbeat → ring 0. escalate → ring 1. Ignition (Opus) only encodes; the cheap rings run it.

**Density → ramification:** depth 0 = large, 1 = normal, 2 = micro, 3 = nano, 4+ = pico. Deep
sub-sub-sub-agents draw the smallest models, so the swarm never drains a plant.

---

## Live benchmark evidence (2026-06-24, `probe.py`)

- **NVIDIA verified live:** `nano-8b` 0.96s avg / **63 tok/s**, `deepseek-v4-flash` 1.7s,
  `super-49b` 4.9s, `deepseek-v4-pro` 6.2s — all pass. `nemotron-ultra-253b` is catalog-listed
  but **404s (not served)** — a real gap between "121 listed" and "models that fire."
- **The 40-rpm wall is REAL but burst-throttled:** firing 40–50 concurrent tiny requests at one
  model hit a hard **429 after ~19–21**, not 40. So 40 rpm is a per-minute ceiling, but **bursts
  are throttled harder than 40-at-once** — the meter must *pace*, not just count per minute.
- **Pollinations:** keyless, `200 → ONLINE`, genuinely free, no signup.
- **Groq verified live:** `qwen3-32b` 0.38s, `llama-3.3-70b` **0.28s** (fastest plant), 50/50
  burst with zero 429 (burst-tolerant, unlike NVIDIA). Note: Groq's WAF blocks VPN IPs
  (`Access denied`) — run with the VPN off.

---

## Using the grid
```
python grid.py                 # the city dashboard: plants, zones, capacity, what's keyed
python probe.py                # battery on every online plant
python probe.py nvidia --rpm 50  # find the real 429 wall on a plant
```
`grid.complete(prompt, capability="reasoning", zone="private", depth=0)` → routes to the cheapest
powered plant in the allowed zone at the right model size, meters the draw, returns the text.
Keys live in `.env` (gitignored) or your OS env. State persists in `grid_state.json`.

---

## Round 2 — exhaustive source hunt + corrected local options (2026-06-25, 28 agents)

**New keeper — WIRED into the grid:** Z.AI / Zhipu **GLM-Flash** — genuinely recurring-free, no
card, OpenAI-compatible. `glm-4.5-flash` (reasoning + thinking mode), `glm-4.7-flash` (text),
`glm-4.6v-flash` (vision, 128K, function-calling). Use the international `api.z.ai` (Singapore-hosted;
DPA says API content is not stored — better privacy than feared). Caveat: ~1 concurrent (serialize),
rate limits unpublished, residual training ambiguity → a sanitized **public** worker, not the trusted
core. This adds a free reasoning+vision lane. Grab a key at z.ai.

**Minor:** Requesty (200 req/day, no-card overflow router). Modal ($30/mo *recurring* free
serverless-GPU — event-driven bursts only, never always-on).

**Rejected (NOT recurring-free):** Jina (one-time 10M tokens), Nomic hosted (paid), Voyage (one-time),
Alibaba Qwen/DashScope (90-day trial). **But their embedding/rerank *weights* self-host free locally** —
use Ollama `nomic-embed-text` / `bge-m3`. The memory layer doesn't need a paid API.

**Free GPU clouds — verified, none give a free always-on GPU endpoint:** Colab/Kaggle ToS *ban*
serving + 12h session caps (experiments only); Lightning free = CPU-only studio + 15 throwaway
credits/mo; HF ZeroGPU = 5 min/day burst, Gradio-only. Modal $30/mo is the one recurring option, but
event-driven only.

### Local options — corrected verdict (RTX 3500 Ada, 12GB, Win11, no WSL/Docker)
- **vLLM** — no native Windows (community fork only); its edge is concurrent *batch* throughput, moot
  for a single user. Skip — Ollama matches it solo.
- **NVIDIA TensorRT-LLM + NIM** — Windows-native is DEAD (TRT-LLM dropped it at v0.18; NIM is
  Linux-only). Needs WSL2 + Docker (you have neither). The standard 8B NIM needs **24GB VRAM** (you
  have 12), and the WSL2-NIM path only lists RTX 40/50 GeForce — not your RTX 3500 Ada. Decisively out.
- **NVIDIA ChatRTX** — DEPRECATED + archived (2026-01-21), local API removed in v0.4, only legacy 7B
  fits your GPU. Dead end. (Correcting my suggestion from last turn — it is not a live option.)
- **LM Studio + llama.cpp** — both native Windows, free, OpenAI-compatible headless server
  (`lms server start` / `llama-server`), GBNF grammar-constrained JSON for structured behaviors.
  Arguably a *better* entity backbone than Ollama. The real local upgrade path.

**Concrete 12GB always-on stack:** Qwen3 8B (5.2GB) resident reasoner + `nomic-embed-text` for memory
(**raise num_ctx to 8K — it defaults to 2K!**) + Qwen2.5-VL 7B (6GB) on-demand vision + Qwen3-30B-A3B
MoE via `llama.cpp --n-cpu-moe` (~20-35 tps) for heavier async reasoning. Avoid `mxbai-embed-large`
(512-token cap) for journal ingestion. Keep model weights off OneDrive-synced folders.

**Division of labor confirmed:** local Ollama/llama.cpp = the unlimited private base; the free hosted
plants = big-model bursts. Don't fight 12GB to run a 120B locally — call Cerebras/NVIDIA free instead.
