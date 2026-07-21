"""memory.py - the entity's persistent memory = the backwards channel (seed 10) + A-axis L2.
Local embeddings (Ollama mxbai-embed-large: free, unlimited, private) + cosine recall.
Grounds the swarm so it reasons over TRUTH instead of hallucinating. No API keys, no cloud."""
import json, os, math, urllib.request, grid

STORE = os.path.join(grid.HERE, 'memory.json')

def embed(text):
    body = json.dumps({'model': 'mxbai-embed-large', 'input': text}).encode()
    req = urllib.request.Request('http://localhost:11434/v1/embeddings', data=body,
                                 headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())['data'][0]['embedding']

def _load(): return grid.load_json(STORE, [])
def _save(m): grid.atomic_save_json(STORE, m)     # kill-safe (review 2026-07-10)

def remember(text):
    m = _load(); m.append({'text': text, 'emb': embed(text)}); _save(m); return len(m)

def _cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0

def recall(query, k=3):
    m = _load()
    if not m: return []
    q = embed(query)
    return [r['text'] for r in sorted(m, key=lambda r: -_cos(q, r['emb']))[:k]]

# The truth about Luis's grid - what the swarm must reason over instead of inventing.
FACTS = [
    "The AEA grid has a measured total capacity of about 2,234 requests per minute across hosted plants, plus unlimited local Ollama.",
    "The grid has about 59 independent parallel nodes (distinct model buckets). NVIDIA's 40 requests/minute limit is PER-MODEL with independent buckets - querying all 121 models at once produced zero 429 errors, so there is no global cap.",
    "Of 121 NVIDIA catalog models, 51 actually serve; across all plants 36 of 59 tested models scored a perfect 4/4 on the capability battery.",
    "Online plants: NVIDIA NIM (no-train, 40 rpm/model, full organ set), Groq (no-train, fastest at sub-0.3s, gpt-oss-20b hits 246 tok/s), Cerebras (no-train, 1M tokens/day, gpt-oss-120b at ~0.7s), Z.AI GLM-Flash (free reasoning+vision, public), Ollama (local, unlimited, private), Pollinations (keyless).",
    "The crystallize doctrine: a frontier model encodes a behavior into a tight scaffold that a cheap model then runs, so the cheap model borrows frontier judgment without the frontier cost.",
    "Privacy zones: residential = no-train plants safe for private data; industrial = trains-on-data plants for public data only. The orchestrator routes private tasks only to no-train or local nodes.",
    "The swarm ramifies recursively: a deep model (e.g. gpt-oss-120b) reasons at the root, fast Groq models do the leaves; an agent spawns sub-agents when its task decomposes into independent parts or exceeds its tier.",
    "Local stack: Ollama (32 models) + Fooocus SDXL on an RTX 3500 Ada 12GB = assistant tier (7-14B), not frontier; qwen3:8b runs about 27 tokens/sec warm.",
    "The canonical project lives at <REDACTED-PATH>/dev/aea-city (off OneDrive). LLM7.io was rejected: its free token returns 402 insufficient balance, so it is not actually free.",
    "The biggest risk to the project is that characterization keeps substituting for building - the entity must ship real artifacts, not just be measured and mapped.",
]

def seed():
    if os.path.exists(STORE): os.remove(STORE)
    for f in FACTS: remember(f)
    return len(FACTS)
