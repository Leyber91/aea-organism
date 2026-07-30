"""
grid.py - the AEA entity's power grid (the city's electricity layer).

THE CITY MODEL
  Plant      = a provider (NVIDIA, Groq, Cloudflare, Ollama, ...)   = a power plant
  Generator  = a model = one turbine inside a plant
  Meter      = the grid operator: tracks consumption, never lets a plant brown out (HTTP 429)
  Zone       = privacy ring: residential(private/no-train) vs industrial(public/trains-on-data)
  Density    = pico / nano / micro / normal / large = model size by agent depth (ramification)
  Router     = the road network: dispatch a request to the cheapest plant that has spare
               capacity right now AND sits in the allowed zone AND has the needed capability.

The whole point: run a 24/7 entity on FREE energy without ever tripping a breaker.
The Meter enforces each plant's published free limit (e.g. NVIDIA's 40 req/min/model), so
sub-agents, sub-sub-agents and sub-sub-sub-agents can all draw power without overrunning it.

Stdlib only - no pip install. Python 3.8+.
"""

from __future__ import annotations
import json, os, time, threading, urllib.request, urllib.error
from contextlib import contextmanager
from datetime import datetime, timezone

try:
    import msvcrt                      # Windows file locking (this machine); None elsewhere
except ImportError:                    # pragma: no cover
    msvcrt = None

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_root(start):
    """Walk up from HERE to the repo root (the dir that holds design/ or .git), so state
    resolves to the SAME place whether this module sits at root or in a runtime/ subfolder."""
    d = start
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "design")) or os.path.isdir(os.path.join(d, ".git")):
            return d
        p = os.path.dirname(d)
        if p == d:
            break
        d = p
    return start


ROOT = _find_root(HERE)
STATE = os.path.join(ROOT, "state")          # the one home for runtime state on disk


def ensure_state() -> str:
    """Create `state/` on FIRST WRITE rather than on import (law S3: nothing acts at import time).

    `os.makedirs(STATE)` sat at module level, so merely naming `aea.kernel.grid` touched the disk,
    and every module in this tree imports grid. That made the whole codebase unsafe to scan or to
    import inside a test, which is the same class of defect as `build_graph` rewriting tracked files
    on import - the one that made the analyser parse instead of import in the first place.
    """
    os.makedirs(STATE, exist_ok=True)
    return STATE
WEB = os.path.join(ROOT, "web")              # the front-end: html + js + game/ served from here


HOME = os.path.expanduser("~")               # resolved, never typed


def _state(path: str) -> str:
    """A bare filename -> under STATE/. An already-qualified path -> unchanged."""
    return os.path.join(STATE, path) if os.path.dirname(path) == "" else path


def external(env_key: str, *parts, default_under_home: str = None) -> str | None:
    """A location OUTSIDE this repo, resolved at runtime. NOTHING ABOUT IT IS TYPED IN.

    THE RULE, AND IT IS THE WHOLE POINT: the only path this system knows is its own root, found by
    walking up. Everything else is expressed relative to an ANCHOR - ROOT for anything inside the
    repo, HOME or a declared .env key for anything outside it. A literal path in source is a machine
    the code cannot leave: move the checkout, change the user, run it anywhere else, and it breaks
    silently because the folder simply is not there.

    Six such literals were found in this repo on 2026-07-28 - a Claude projects directory, three
    document trees, and a fact string naming the repo's own location. Every one of them named a
    specific machine and a specific user.

    Resolution order, and it FAILS HONESTLY rather than guessing:
        1 the .env key, if set                     the deliberate answer
        2 HOME/<default_under_home>, if it exists  the conventional answer
        3 None                                     say so; do not invent a path

    Returning None matters. A caller that gets a fabricated path will create an empty directory and
    report success over nothing, which is the honesty law's exact failure mode in filesystem form.
    """
    base = (key(env_key) or "").strip().strip('"').strip("'")
    if not base and default_under_home:
        cand = os.path.join(HOME, *default_under_home.split("/"))
        if os.path.exists(cand):
            base = cand
    if not base:
        return None
    p = os.path.join(base, *parts) if parts else base
    return p if os.path.exists(os.path.dirname(p) or p) or not parts else p


# --------------------------------------------------------------------------------------
# 0a. DURABLE PERSISTENCE - the one home for state on disk (engine review 2026-07-10:
#     every store was truncate-written and every loader silently reset to empty on a torn
#     file; for an entity whose thesis is "continuity lives in the files", that was the
#     single worst defect class). All state goes through these three helpers now.
# --------------------------------------------------------------------------------------
# WINDOWS RENAMES AND OPENS FAIL TRANSIENTLY, AND THIS SYSTEM RUNS ON WINDOWS FOR WEEKS.
# A sharing violation (WinError 32/5) lasts milliseconds - another process, or a virus scanner, has
# the file open. Both helpers below retry before treating it as anything worse.
_IO_RETRIES = 5
_IO_BACKOFF = 0.05


def atomic_save_json(path: str, data, indent=None):
    """Write-to-temp then os.replace: a kill mid-write can never leave a truncated store.

    THE REPLACE IS RETRIED. `os.replace` raises PermissionError on Windows when anything holds the
    destination open, and this repo writes the same stores from the wake loop, the control room and
    the CLI at once. An unretried replace turns a momentary lock into a lost write - and for the
    trust ledger a lost write is a lost demotion, which is the one direction that must never be lost.
    """
    path = _state(path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)   # was at import time; see ensure_state
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    last = None
    for i in range(_IO_RETRIES):
        try:
            os.replace(tmp, path)
            return
        except PermissionError as e:                  # Windows sharing violation; momentary
            last = e
            time.sleep(_IO_BACKOFF * (2 ** i))
    raise last


class StateUnreadable(OSError):
    """The file exists and could not be read. NOT the same as corrupt, and NOT the same as absent."""


def load_json(path: str, default):
    """Missing file -> default. CORRUPT file -> quarantine and return default. LOCKED file -> RAISE.

    THE DISTINCTION THIS FUNCTION USED TO MISS, AND IT IS A STATE-DESTROYING ONE.

    The old body caught bare `Exception`, so EVERY failure was treated as corruption: the file was
    RENAMED AWAY and the permissive `default` returned. `PermissionError` from a Windows sharing
    violation is not corruption - the store is perfectly valid and simply held open by another
    process for a few milliseconds. For `state/trust_ledger.json` the default is `{}`, and `_entry`
    then rebuilds every capability at its CHARTER STARTING LEVEL. So one momentary file lock could
    silently restore autonomy the entity had lost, and erase the accountability history the ledger
    exists to keep. `state/bench_runs.json.corrupt.<ts>` is tracked in this repo: it already fired.

    Three outcomes now, because there are three situations:
      absent      -> default. Nothing was lost; there was nothing there.
      unparseable -> quarantine loudly and return default. The old behaviour, for the case it was
                     actually written for: JSONDecodeError / UnicodeDecodeError.
      unreadable  -> retry, then RAISE. A caller must never silently proceed on a default standing
                     in for a file that exists. Failing loudly is recoverable; a reset ledger is not.
    """
    path = _state(path)
    last = None
    for i in range(_IO_RETRIES):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            try:
                q = f"{path}.corrupt.{int(time.time())}"
                os.replace(path, q)
                print(f"[grid] WARNING: {os.path.basename(path)} unparseable ({str(e)[:60]}) "
                      f"-> quarantined to {os.path.basename(q)}; starting from default")
            except Exception:
                pass
            return default
        except OSError as e:                          # locked, busy, permission - transient
            last = e
            time.sleep(_IO_BACKOFF * (2 ** i))
    raise StateUnreadable(
        f"{path} exists but could not be read after {_IO_RETRIES} attempts ({last}). Refusing to "
        f"return the default: for a ledger or a save, a default is not a safe stand-in for a file "
        f"that is present.")


@contextmanager
def file_lock(path: str, timeout: float = 5.0):
    """Cross-process advisory lock on <path>.lock (msvcrt). Yields True if held. On timeout
    yields False and proceeds unlocked - the entity must degrade, never deadlock."""
    path = _state(path)
    if msvcrt is None:
        yield True; return
    f = open(path + ".lock", "a+b")
    got = False
    t0 = time.time()
    try:
        while time.time() - t0 < timeout:
            try:
                f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                got = True; break
            except OSError:
                time.sleep(0.05)
        yield got
    finally:
        if got:
            try:
                f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except Exception:
                pass
        f.close()


def fetch_json(url: str, timeout: int = 20):
    """The shared sense helper (was duplicated verbatim in brief.py and aea.py)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 aea-grid/1.0",
                                               "Accept": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore"))


# --------------------------------------------------------------------------------------
# 0. Keys - read .env then fall back to OS environment (NVIDIA already lives in OS env)
# --------------------------------------------------------------------------------------
def load_env() -> dict:
    env = dict(os.environ)
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.split("#", 1)[0].strip()   # strip inline comments + whitespace
                if v:                      # blank in .env -> keep the OS env value
                    env[k.strip()] = v
    return env

ENV = load_env()
def key(name: str) -> str | None:
    v = ENV.get(name)
    return v if v else None


# --------------------------------------------------------------------------------------
# 1. The plants - capacity is MACHINE-READABLE here (energy.json holds the human map).
#    limits: rpm/rpd per (plant,model); tpd/neurons_day/monthly_* are account-wide.
#    privacy: local | no-train | trains | none        zone routing keys off this.
# --------------------------------------------------------------------------------------
UNLIMITED = None

PLANTS = {
    "ollama": dict(privacy="local", base="http://localhost:11434/v1", auth=None, openai=True,
                   rpm=UNLIMITED, rpd=UNLIMITED, note="local, private, unlimited"),
    # rpm=40 is the PUBLISHED figure; MEASURED 2026-07-25 the real ceiling is ~25 IN FLIGHT per rod,
    # per-model (not shared): 50 concurrent on one model -> 25 ok / 25 rejected in 1.8s, while three
    # other models answered 200 in the same second; 78 requests cleared in <7s. max_inflight=20
    # keeps a safety margin under the measured 25.
    "nvidia": dict(privacy="no-train", base="https://integrate.api.nvidia.com/v1", auth="NVIDIA_API_KEY", openai=True,
                   rpm=40, rpd=UNLIMITED, max_inflight=20,
                   note="118 models; ~25 in-flight/rod measured, per-model not shared; 256K ctx"),
    "groq": dict(privacy="no-train", base="https://api.groq.com/openai/v1", auth="GROQ_API_KEY", openai=True,
                 rpm=30, rpd=1000, note="fast; qwen3-32b is 60 rpm"),
    "cerebras": dict(privacy="no-train", base="https://api.cerebras.ai/v1", auth="CEREBRAS_API_KEY", openai=True,
                     rpm=5, rpd=UNLIMITED, tpd=1_000_000, note="VERIFIED 5 RPM (burst 12->5 ok, 2026-06-27); 30K TPM, 8K ctx free; ~2000 tok/s - BATCH/LEAF only, not interactive"),
    "sambanova": dict(privacy="no-train", base="https://api.sambanova.ai/v1", auth="SAMBANOVA_API_KEY", openai=True,
                      rpm=20, rpd=20, tpd=200_000, note="20 rpd/model x6 = ~120/day"),
    "ovh": dict(privacy="no-train", base="https://oai.endpoints.kepler.ai.cloud.ovh.net/v1", auth="OVH_AI_ENDPOINTS_TOKEN", openai=True,
                rpm=400, rpd=UNLIMITED, note="EU, no-train; 2 rpm keyless / 400 rpm with token"),
    "cloudflare": dict(privacy="no-train", base="https://api.cloudflare.com/client/v4/accounts", auth="CLOUDFLARE_API_TOKEN", openai=False,
                       rpm=300, neurons_day=10_000, note="edge; 10k neurons/day hard-stop"),
    "gemini": dict(privacy="trains", base="https://generativelanguage.googleapis.com/v1beta/openai", auth="GEMINI_API_KEY", openai=True,
                   rpm=10, rpd=1500, note="PUBLIC data only on free (trains)"),
    "mistral": dict(privacy="trains", base="https://api.mistral.ai/v1", auth="MISTRAL_API_KEY", openai=True,
                    rpm=2, rpd=UNLIMITED, monthly_tokens=1_000_000_000, note="EU; 2 rpm; opt out before private use"),
    "openrouter": dict(privacy="trains", base="https://openrouter.ai/api/v1", auth="OPENROUTER_API_KEY", openai=True,
                       rpm=20, rpd=50, note="22 :free models; 50 rpd free / 1000 after $10"),
    "zai": dict(privacy="trains", base="https://api.z.ai/api/paas/v4", auth="ZAI_API_KEY", openai=True,
                rpm=10, rpd=1000, note="GLM-Flash FREE: reasoning(4.5)+vision(4.6V), 128K; ~1 concurrent so serialize; Singapore; public-only"),
    "github": dict(privacy="trains", base="https://models.github.ai/inference", auth="GITHUB_MODELS_TOKEN", openai=True,
                   rpm=15, rpd=150, note="RETIRING + closed to new customers"),
    "cohere": dict(privacy="trains", base="https://api.cohere.com/v2", auth="COHERE_API_KEY", openai=False,
                   rpm=10, monthly_calls=1000, note="rerank only; 1000 calls/MONTH; non-commercial"),
    "pollinations": dict(privacy="none", base="https://text.pollinations.ai/openai", auth=None, openai=True,
                         rpm=4, rpd=UNLIMITED, note="keyless; 1 req/15s; public data only"),
    # llm7 REMOVED 2026-06-26: token authenticates but EVERY call returns 402 "insufficient balance" - NOT free despite the no-card token. Research overclaimed; live test refuted.
    "hf": dict(privacy="none", base="https://router.huggingface.co/v1", auth="HF_TOKEN", openai=True,
               rpm=UNLIMITED, monthly_usd=0.10, note="$0.10/mo - failover/embeddings layer only"),
}

# Density: smaller models live deeper in the agent ramification.
SIZES = ["pico", "nano", "micro", "normal", "large"]
DEPTH_TO_SIZE = {0: "large", 1: "normal", 2: "micro", 3: "nano"}   # deeper -> default pico
def size_for_depth(depth: int) -> str:
    return DEPTH_TO_SIZE.get(depth, "pico")

# A representative generator registry (the full list is energy.json). (plant, model, modality, size)
GENERATORS = [
    # NVIDIA - the full organ set on one key
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b", "reasoning", "large"),  # PROBED 2026-07-19: 3/3 @ 1.9s - served DIRECT by NVIDIA (no openrouter detour)
    ("nvidia", "minimaxai/minimax-m3", "reasoning", "large"),               # PROBED 2026-07-19: 3/3 @ 5.7s - roster-ready
    # z-ai/glm-5.2: 3/3 correct but ~55s hidden reasoning EVERY call -> batch/long-horizon lane only,
    # needs timeout>=150 + generous max_tokens; NOT in GENERATORS (would read as dead on interactive paths)
    ("nvidia", "deepseek-ai/deepseek-v4-pro", "reasoning", "large"),   # ultra-253b is catalog-listed but 404s (not served)
    ("nvidia", "nvidia/llama-3.3-nemotron-super-49b-v1.5", "reasoning", "normal"),
    ("nvidia", "deepseek-ai/deepseek-v4-flash", "reasoning", "micro"),
    ("nvidia", "nvidia/llama-3.1-nemotron-nano-8b-v1", "text", "nano"),
    ("nvidia", "nvidia/nemotron-nano-12b-v2-vl", "vision", "micro"),
    ("nvidia", "nvidia/llama-nemotron-embed-1b-v2", "embed", "pico"),
    # Ollama - the private local base
    ("ollama", "qwen3.5:9b", "reasoning", "normal"),
    ("ollama", "deepseek-r1:8b", "reasoning", "micro"),
    ("ollama", "granite4.1:3b", "text", "nano"),   # reliable non-thinking instruct (qwen3:1.7b returns empty under /no_think)
    ("ollama", "qwen3:0.6b", "text", "pico"),
    ("ollama", "mxbai-embed-large", "embed", "pico"),
    # Groq - speed (needs key)
    ("groq", "qwen/qwen3-32b", "reasoning", "normal"),
    ("groq", "llama-3.3-70b-versatile", "text", "normal"),
    # Cloudflare / SambaNova / Cerebras / OVH - no-train hosted (need keys)
    ("cloudflare", "@cf/qwen/qwen3-30b-a3b-fp8", "reasoning", "normal"),
    ("cloudflare", "@cf/baai/bge-m3", "embed", "pico"),
    ("sambanova", "gpt-oss-120b", "reasoning", "large"),
    ("cerebras", "gpt-oss-120b", "reasoning", "large"),
    ("ovh", "Qwen2.5-VL-72B-Instruct", "vision", "normal"),
    # Public-zone plants (trains on data)
    ("gemini", "gemini-2.5-flash-lite", "reasoning", "micro"),
    ("mistral", "mistral-small-latest", "reasoning", "normal"),
    ("openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free", "reasoning", "large"),
    ("zai", "glm-4.5-flash", "reasoning", "normal"),
    ("zai", "glm-4.6v-flash", "vision", "normal"),
    # Keyless fallback
    ("pollinations", "openai-fast", "reasoning", "micro"),
]

# THE THINKING SWITCH. MEASURED 2026-07-28 against the hosted endpoint, 67 calls, same answer (391)
# in every cell that returned. `mind/fuel.py` recorded thinking as an untamed property of the fuel
# because setting it by system prompt gave identical output; that test used the wrong string for the
# family. There are TWO switches and they do not cross over:
#
#   LLAMA-NEMOTRON (llama-3.3-nemotron-super-49b-v1.5, nvidia-nemotron-nano-9b-v2)
#       system message "/no_think"      -> 0 chars of reasoning, 2-5 output tokens, 0.4-1.5s
#       (default on the 49B: 3024 chars, 991 tokens, 71s. Same answer.)
#       chat_template_kwargs and reasoning_budget are IGNORED here.
#   NEMOTRON 3 (nemotron-3-nano-30b-a3b, nemotron-3-super-120b-a12b)
#       chat_template_kwargs {"enable_thinking": False}  -> 0 chars, 4 tokens
#       "/no_think" is IGNORED here.
#   GPT-OSS      reasoning_effort low|medium|high        -> 20 / 66 / 249 chars, monotonic
#   OLLAMA       native /api/chat {"think": False}       -> 0 chars, 4 tokens vs 691 with
#                the OpenAI-compat base at :11434/v1 CANNOT reach it; the compat path ignores it.
#
# WHAT DOES NOT WORK ON THE HOSTED ENDPOINT, despite being documented: `nvext.max_thinking_tokens`
# and `reasoning_budget`. NVIDIA's own example targets base_url=localhost:8000, i.e. self-hosted NIM.
# minimax-m3 and glm-5.2 reject reasoning_budget outright with 400 "Unsupported parameter".
#
# SENDING THE WRONG ONE IS NOT FREE. mistral-medium-3.5 returns HTTP 400 "chat_template is not
# supported" for any chat_template_kwargs, so a blanket switch breaks it. Hence: match the family,
# or send nothing. Unknown family -> no switch, which is the fail-closed reading of law B1.
THINK_OFF = (
    ("nemotron-3-",            {"chat_template_kwargs": {"enable_thinking": False}}),
    ("nemotron-nano-9b",       {"_system": "/no_think"}),
    ("nemotron-super-49b",     {"_system": "/no_think"}),
    ("nemotron-super-",        {"_system": "/no_think"}),
    ("gpt-oss",                {"reasoning_effort": "low"}),
)


def think_off(model: str) -> dict:
    """Extra request fields that turn reasoning off for THIS model, or {} when none is measured.
    A `_system` key means "prepend this system message" rather than a body field. Returns {} for an
    unmeasured family rather than guessing, because the wrong switch is a 400 on some plants."""
    m = (model or "").lower()
    for frag, opt in THINK_OFF:
        if frag in m:
            return dict(opt)
    return {}


# WHAT EACH MODEL'S OWNER PUBLISHES, lifted 2026-07-28 from the Python example on each model's own
# build.nvidia.com page. Not defaults we chose, not defaults we inherited: the recommended call.
#
# THIS IS A CONFOUND IN EVERY MEASUREMENT THIS PROJECT HAS TAKEN. `call_openai` sends
# temperature=0.2 and max_tokens=256 to every rod and never sends top_p at all. The owners publish
# temperature 0.2 to 1, top_p 0.7 to 1, and max_tokens 1024 to 20480. The worst case is
# `nemotron-3-nano-omni-30b-a3b-reasoning`, whose owner asks for 20480 tokens and gets 256 from us:
# a reasoning rod handed 256 tokens spends them thinking and never reaches an answer, which is
# exactly the empty-reply failure already recorded in unstick.py and in the x12 run. Every fitness
# score, census and tool probe in this repo was taken through that filter.
#
# 16 of 102 pages publish a callable example. Of the 86 that do not, 68 are also not served, so a
# missing example is a weak signal of a retired rod. The other 18 are pages this extractor could
# not read, which is a gap in the reader rather than a fact about the model.
OWN_PARAMS = {
    # id: (temperature, top_p, max_tokens)
    "deepseek-ai/deepseek-v4-flash":                 (1.0, 0.95, 16384),
    "deepseek-ai/deepseek-v4-pro":                   (1.0, 0.95, 16384),
    "meta/llama-3.2-1b-instruct":                    (0.2, 0.70,  1024),
    "meta/llama-3.2-3b-instruct":                    (0.2, 0.70,  1024),
    "mistralai/mistral-nemotron":                    (0.6, 0.70,  4096),
    "nvidia/nemotron-3-nano-30b-a3b":                (1.0, 1.00, 16384),
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning": (0.6, 0.95, 20480),
    "nvidia/nemotron-3-super-120b-a12b":             (1.0, 0.95, 16384),
    "nvidia/nemotron-3-ultra-550b-a55b":             (1.0, 0.95, 16384),
    "nvidia/nemotron-mini-4b-instruct":              (0.2, 0.70,  1024),
    "nvidia/nvidia-nemotron-nano-9b-v2":             (0.6, 0.95,  2048),
    "openai/gpt-oss-120b":                           (1.0, 1.00,  4096),
    "openai/gpt-oss-20b":                            (1.0, 1.00,  4096),
    "poolside/laguna-xs-2.1":                        (1.0, 0.95,  8192),
    "thinkingmachines/inkling":                      (1.0, 0.95,  8192),
    "z-ai/glm-5.2":                                  (1.0, 1.00, 16384),
}


def _rod_facts(model: str) -> dict:
    """What `aea.energy.rodprobe` measured about this rod, read from the store rather than imported,
    because the kernel may not depend on a package above it. Absent store means an empty dict, which
    is the fail-closed reading: no fact rather than an invented one."""
    doc = load_json(os.path.join(STATE, "rods.json"), {})
    return (doc.get("rods") or {}).get(model) or {}


def is_retired(plant: str, model: str) -> bool:
    """Has this rod been MEASURED dead? One predicate, tombstone only, for every selector.

    THE FOURTH COPY IS WHY THIS LIVES HERE. `energy.ladder` learned to skip tombstoned rods (D22),
    and a cross-tree sweep then found the same blindness in two more selectors that had never been
    touched: `orchestrator.load_pool` - which the verifier called "energy.ladder() rewritten without
    the fix" - and `controlroom`'s status panel, a hand-copied `_cooling` with the permanent branch
    deleted. Each had grown its own liveness rule and each expired.

    IT IS IN `grid`, NOT `energy`, DELIBERATELY. Every selector already imports `grid`; `mind/`
    imports no `energy/` today and pointing it there for a one-line predicate would invert the
    dependency direction for nothing. `energy_usage.json` already resolves through `grid.STATE`.

    AND IT IS TOMBSTONE-ONLY, WHICH `energy._cooling` IS NOT. That function returns True for a
    retirement AND for a fifteen-minute cooldown, so promoting it would let a transient throttle
    delete a rod from a pool the way a withdrawal must. A permanent fact and a temporary one need
    different answers - conflating them is the defect in the other direction."""
    e = (load_json(os.path.join(STATE, "energy_usage.json"), {}) or {}).get(f"{plant}/{model}")
    return bool(isinstance(e, dict) and e.get("retired_at"))


def own_params(model: str) -> dict:
    """The owner's published temperature/top_p/max_tokens for this model, or {} if nothing was
    published. Returns {} rather than a house default, so a caller can tell the difference between
    "measured" and "we guessed" - the same reason an absent value renders as a dash.

    The MEASURED store wins over the literal table below, so re-running the probe updates behaviour
    without a code edit, and the table remains the answer when the store has not been built."""
    pub = (_rod_facts(model).get("published") or {})
    got = {k: pub[k] for k in ("temperature", "top_p", "max_tokens") if pub.get(k) is not None}
    if got:
        return got
    p = OWN_PARAMS.get(model)
    return {} if not p else {"temperature": p[0], "top_p": p[1], "max_tokens": p[2]}


ZONES = {            # which privacy classes a zone may use
    "sensitive": {"local"},
    "private":   {"local", "no-train"},
    "public":    {"local", "no-train", "trains", "none"},
}
# cheapest-first plant preference (local before free-hosted before keyless)
PLANT_RANK = {p: i for i, p in enumerate(
    ["ollama", "ovh", "cloudflare", "cerebras", "sambanova", "nvidia", "groq",
     "gemini", "mistral", "openrouter", "zai", "github", "pollinations", "cohere", "hf"])}


# --------------------------------------------------------------------------------------
# 2. The Meter - the grid operator. Tracks consumption, answers "is there power right now?"
# --------------------------------------------------------------------------------------
def _today() -> str:  return datetime.now(timezone.utc).strftime("%Y-%m-%d")
def _month() -> str:  return datetime.now(timezone.utc).strftime("%Y-%m")

class Meter:
    """STATELESS-OVER-FILE (engine review 2026-07-10): the old Meter cached state at __init__
    and blind-overwrote grid_state.json, so every process - and even two Meter instances in ONE
    process - owned a private fiction of the rpm budget. Now every operation is a locked
    read-modify-write of the file, and the 60s rpm windows + 429 cooldowns persist in it too.
    Any number of Meter instances anywhere now share one truth; construction is free."""

    def __init__(self, state_path: str | None = None):
        self.state_path = state_path or os.path.join(STATE, "grid_state.json")
        self.lock = threading.Lock()          # in-process threads; file_lock covers processes

    # -- state plumbing -----------------------------------------------------------------
    def _fresh(self) -> dict:
        st = load_json(self.state_path, {})
        for k, d in (("daily", {}), ("monthly", {}), ("rpm", {}), ("throttle", {})):
            st.setdefault(k, d)
        return st

    @staticmethod
    def _roll(st: dict, plant: str):
        d = st["daily"].setdefault(plant, {"date": _today(), "rpd": 0, "tokens": 0, "neurons": 0})
        if d["date"] != _today():
            d.update(date=_today(), rpd=0, tokens=0, neurons=0)
        m = st["monthly"].setdefault(plant, {"month": _month(), "calls": 0, "tokens": 0})
        if m["month"] != _month():
            m.update(month=_month(), calls=0, tokens=0)
        return d, m

    @staticmethod
    def _win(st: dict, mk: str, now: float) -> list:
        win = [t for t in st["rpm"].get(mk, []) if now - t <= 60]
        st["rpm"][mk] = win
        return win

    # -- reads --------------------------------------------------------------------------
    def status(self, plant: str, model: str) -> dict:
        """How much headroom is left right now (fresh from the shared file)."""
        with self.lock, file_lock(self.state_path):
            st = self._fresh(); d, m = self._roll(st, plant)
            cap = PLANTS[plant]; now = time.time()
            win = self._win(st, f"{plant}:{model}", now)
            return {
                "rpm_used": len(win), "rpm_cap": cap.get("rpm"),
                "rpd_used": d["rpd"], "rpd_cap": cap.get("rpd"),
                "tokens_today": d["tokens"], "tpd_cap": cap.get("tpd"),
                "neurons_today": d["neurons"], "neurons_cap": cap.get("neurons_day"),
                "calls_month": m["calls"], "monthly_calls_cap": cap.get("monthly_calls"),
            }

    # IN-FLIGHT, per rod. MEASURED 2026-07-25: firing 50 concurrent requests at ONE nvidia model
    # returned 25 x 200 and 25 x 429 in 1.8s, while three OTHER models answered 200 in the same
    # second. So the ceiling that actually rejects you is CONCURRENCY PER ROD - not requests per
    # minute, and not shared across the plant. 78 requests went through in under 7s (~670/min),
    # which no rpm model predicts. The meter was guarding the wrong dimension.
    _inflight: dict = {}

    def enter(self, plant: str, model: str) -> None:
        """Claim an in-flight slot on this rod (call immediately before the request)."""
        with self.lock:
            mk = f"{plant}:{model}"
            Meter._inflight[mk] = Meter._inflight.get(mk, 0) + 1

    @staticmethod
    def ceiling(plant: str) -> int | None:
        """The concurrency this plant ACTUALLY tolerates, measured, falling back to the declared
        constant. MEASURED 2026-07-29 on nvidia: clean at 4, three of eight throttled at 8, against
        a declared `max_inflight` of 20. The constant came from a 2026-07-25 run that no longer
        reproduces, and being 5x too high is why every burst today earned a 429 the meter believed
        was impossible. A ceiling nobody re-measures is a number, not a limit."""
        doc = load_json(os.path.join(STATE, "plant_ceiling.json"), {})
        got = ((doc.get("plants") or {}).get(plant) or {}).get("clean_at")
        if isinstance(got, int) and got > 0:
            return got
        return (PLANTS.get(plant) or {}).get("max_inflight")

    def try_enter(self, plant: str, model: str) -> bool:
        """CHECK AND CLAIM UNDER ONE LOCK. True if a slot was taken, False if the rod is saturated.

        `can_spend()` then `enter()` is a check-then-act race and it is decorative under exactly the
        burst it exists to stop. MEASURED 2026-07-28: thirty threads launched together all called
        can_spend, all read inflight=0 because none had claimed yet, all passed, and fifteen of them
        earned a 429 from a rod the meter believed was idle. Two lock acquisitions cannot guard one
        invariant. This holds the lock across both halves, so the twenty-first caller is refused
        rather than merely counted.
        """
        with self.lock:
            mk = f"{plant}:{model}"
            mif = Meter.ceiling(plant)          # measured first, declared constant as fallback
            if mif is not None and Meter._inflight.get(mk, 0) >= mif:
                return False
            Meter._inflight[mk] = Meter._inflight.get(mk, 0) + 1
            return True

    def leave(self, plant: str, model: str) -> None:
        """Release the slot (ALWAYS, in a finally - a leaked slot silently shrinks the rod)."""
        with self.lock:
            mk = f"{plant}:{model}"
            Meter._inflight[mk] = max(0, Meter._inflight.get(mk, 0) - 1)

    def inflight(self, plant: str, model: str) -> int:
        return Meter._inflight.get(f"{plant}:{model}", 0)

    def can_spend(self, plant: str, model: str, est_tokens: int = 800):
        """(ok, wait_seconds, reason). wait_seconds = how long until a slot frees (rpm only)."""
        with self.lock, file_lock(self.state_path):
            st = self._fresh(); d, m = self._roll(st, plant)
            cap = PLANTS[plant]; mk = f"{plant}:{model}"; now = time.time()
            tt = st["throttle"].get(mk)
            if tt and now < tt["until"]:                    # bucket in 429 cooldown -> route around it
                return (False, round(tt["until"] - now, 1), "throttled (429 cooldown)")
            # the real ceiling first: too many already in flight ON THIS ROD -> the next one 429s.
            # Spreading across rods costs nothing, so this pushes the ladder toward rod DIVERSITY,
            # which is what the measurement says the platform actually rewards.
            mif = Meter.ceiling(plant)          # measured first, declared constant as fallback
            if mif is not None and Meter._inflight.get(mk, 0) >= mif:
                return (False, 1.0, "in-flight (rod saturated)")
            win = self._win(st, mk, now)
            rpm = cap.get("rpm")
            if rpm is not None and len(win) >= rpm:
                return (False, max(0.0, 60 - (now - win[0])), "rpm")
            rpd = cap.get("rpd")
            if rpd is not None and d["rpd"] >= rpd:
                return (False, None, "rpd (resets 00:00 UTC)")
            tpd = cap.get("tpd")
            if tpd is not None and d["tokens"] + est_tokens > tpd:
                return (False, None, "tokens/day")
            mc = cap.get("monthly_calls")
            if mc is not None and m["calls"] >= mc:
                return (False, None, "calls/month")
            return (True, 0.0, "ok")

    # -- writes (locked read-modify-write + atomic replace) ------------------------------
    def record(self, plant: str, model: str, tokens: int = 0, neurons: int = 0):
        with self.lock, file_lock(self.state_path):
            st = self._fresh(); d, m = self._roll(st, plant)
            now = time.time()
            self._win(st, f"{plant}:{model}", now).append(now)
            d["rpd"] += 1; d["tokens"] += tokens; d["neurons"] += neurons
            m["calls"] += 1; m["tokens"] += tokens
            atomic_save_json(self.state_path, st)

    def mark_throttled(self, plant: str, model: str, retry_after: float | None = None):
        """A 429 hit THIS bucket: cool it (Retry-After, else exponential backoff). Others untouched."""
        with self.lock, file_lock(self.state_path):
            st = self._fresh()
            mk = f"{plant}:{model}"
            t = st["throttle"].get(mk, {"until": 0.0, "strikes": 0})
            t["strikes"] += 1
            cool = retry_after if retry_after else float(min(60, 2 ** t["strikes"]))   # 2,4,8..60s
            t["until"] = time.time() + cool
            st["throttle"][mk] = t
            atomic_save_json(self.state_path, st)
            return cool

    def clear_strike(self, plant: str, model: str):
        """A success on this bucket resets its strike counter."""
        with self.lock, file_lock(self.state_path):
            st = self._fresh()
            mk = f"{plant}:{model}"
            if mk in st["throttle"]:
                st["throttle"][mk]["strikes"] = 0
                atomic_save_json(self.state_path, st)


METER = Meter()          # the shared default - construct your own only for a different state file


# --------------------------------------------------------------------------------------
# 3. The Router - the roads. Pick the best powered plant for a job.
# --------------------------------------------------------------------------------------
class Router:
    def __init__(self, meter: Meter | None = None):
        self.meter = meter or Meter()

    def candidates(self, capability: str, zone: str = "private", size: str | None = None):
        allowed = ZONES[zone]
        out = []
        for plant, model, modality, msize in GENERATORS:
            if modality != capability:               continue
            if PLANTS[plant]["privacy"] not in allowed: continue
            if size and msize != size:                continue
            if PLANTS[plant]["auth"] and not key(PLANTS[plant]["auth"]):  # needs a key we don't have
                continue
            out.append((plant, model, msize))
        out.sort(key=lambda t: (PLANT_RANK.get(t[0], 99), SIZES.index(t[2])))
        return out

    def pick(self, capability: str, zone: str = "private", size: str | None = None, depth: int | None = None):
        """Return (plant, model, wait_seconds) for the cheapest powered plant, or (None, None, None)."""
        if size is None and depth is not None:
            size = size_for_depth(depth)
        # try the exact size, then relax up the density ladder
        tries = [size] + [s for s in SIZES if s != size] if size else [None]
        best_wait = None
        for sz in tries:
            for plant, model, _ in self.candidates(capability, zone, sz):
                ok, wait, _why = self.meter.can_spend(plant, model)
                if ok:
                    return (plant, model, 0.0)
                if wait is not None:
                    best_wait = wait if best_wait is None else min(best_wait, wait)
        return (None, None, best_wait)


# --------------------------------------------------------------------------------------
# 4. The client - actually draw the power (OpenAI-compatible plants). Always metered.
# --------------------------------------------------------------------------------------
def _read_stream(r):
    """Assemble an SSE completion, returning (payload_like, message) or (None, None) if not a stream.

    EVERY DELTA RESETS THE SOCKET'S READ CLOCK, which is the whole point: `urlopen(timeout=N)`
    applies N per blocking read, so with a stream N is an INACTIVITY budget and without one it is a
    total deadline. Nothing here keeps its own clock - the semantics come from the transport, and a
    clock we maintained ourselves would be one more thing to get wrong.

    Reasoning deltas are READ so they count as liveness, and DISCARDED so they never reach a caller
    as if they were the answer. Both halves matter: the 550b emits reasoning for 13s before its
    first content token, so ignoring the channel makes a working rod look dead; and D13 recorded a
    rod whose whole budget went into reasoning while `content` stayed empty, so treating reasoning
    AS content turns a non-answer into a plausible one.

    Returns (None, None) when the response is not an event stream, so the caller can retry
    unstreamed rather than guess - a provider that ignores `stream: true` answers with ordinary
    JSON, and mistaking that for an empty stream would record a healthy rod as silent.
    """
    # DETECT THE STREAM FROM THE BYTES, NOT FROM THE HEADER.
    #
    # This checked `Content-Type` for "event-stream" and returned "not a stream" otherwise, which
    # silently demoted OLLAMA to the unstreamed path - measured: every telemetry field came back
    # None for `qwen2.5:7b` while a raw probe against the same endpoint had read 272 deltas from it
    # minutes earlier. The local floor lost its inactivity semantics to a header string.
    #
    # A header is the server's DESCRIPTION of the body; the first line is the body. Same law as
    # everywhere else today - ask the live thing - and it costs one readline. Providers that stream
    # perfectly well while labelling it `application/x-ndjson`, `text/plain` or nothing at all now
    # work, and a genuine non-stream is still detected because its first bytes are `{`.
    first = b""
    try:
        first = r.readline()
    except Exception:
        return None, None
    if not first.lstrip().startswith(b"data:"):
        # Not SSE. Hand the whole body back as ordinary JSON so the caller does not re-request it.
        try:
            rest = first + r.read()
            payload = json.loads(rest.decode("utf-8"))
        except Exception:
            return None, None
        m = (payload.get("choices") or [{}])[0].get("message", {}) or {}
        return payload, m
    content, reasoning, tool_calls = [], [], None
    usage, finish = {}, None
    # STREAM TELEMETRY - the data a single blocking read threw away.
    #
    # A non-streamed call yields one number, total latency, and every question worth asking about a
    # rod is invisible inside it. Each field below answers something this project has already paid
    # to learn the hard way:
    #   ttfb            queue/prefill vs generation speed. The 550b's 10.7s prefill was
    #                   indistinguishable from "a slow rod" and got it ranked as one.
    #   reason_chars    D13 ("a rod spending its whole budget in the reasoning field and returning
    #                   empty content") was INFERRED from an empty answer. Now it is measured.
    #   finish_reason   `length` says outright that a budget truncated the answer. D28 - the census
    #                   scoring the 550b's cut-off deliberation - took a re-score plus a control to
    #                   establish, and this one field would have stated it.
    #   deltas/gaps     a mid-generation stall is invisible in a total; here it is a number.
    #   partial output  a stream that dies still leaves what arrived, so "dead peer" and "still
    #                   working when we gave up" stop being the same observation.
    t0 = time.time()
    tel = dict(ttfb=None, ttfc=None, deltas=0, reason_deltas=0, reason_chars=0,
               content_chars=0, worst_gap=0.0, stalled=False)
    last = None
    stream_err = None
    # THE PARTIAL IS KEPT WHEN THE STREAM DIES. Without this the timeout exception propagates and
    # everything that arrived is thrown away, so "the peer was never there" and "the peer was
    # working and we gave up" produce the identical record - which is the exact conflation this
    # whole rung keeps paying for. `deltas > 0` on a stalled read says the rod WAS alive; `deltas
    # == 0` says nothing ever came. Different diagnoses, different fixes.
    try:
        for raw in r:                              # each iteration is one blocking read = one clock reset
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"):
                continue
            chunk = line[5:].strip()
            if chunk == "[DONE]":
                break
            try:
                d = json.loads(chunk)
            except Exception:
                continue
            if isinstance(d.get("error"), dict):   # a 200 carrying an error object
                return dict(error=d["error"], choices=[], telemetry=tel), {}
            if d.get("usage"):
                usage = d["usage"]
            ch = (d.get("choices") or [{}])[0]
            finish = ch.get("finish_reason") or finish
            delta = ch.get("delta") or {}
            c = delta.get("content") or ""
            rc = delta.get("reasoning_content") or delta.get("reasoning") or ""
            if c or rc:
                now = time.time()
                if tel["ttfb"] is None:
                    tel["ttfb"] = round(now - t0, 3)
                if last is not None:
                    tel["worst_gap"] = max(tel["worst_gap"], round(now - last, 3))
                last = now
                tel["deltas"] += 1
            if c:
                if tel["ttfc"] is None:
                    tel["ttfc"] = round(time.time() - t0, 3)
                content.append(c)
                tel["content_chars"] += len(c)
            # read for liveness, keep out of the answer - see the note above
            if rc:
                reasoning.append(rc)
                tel["reason_deltas"] += 1
                tel["reason_chars"] += len(rc)
            if delta.get("tool_calls"):
                tool_calls = _merge_tool_calls(tool_calls, delta["tool_calls"])
    except Exception as e:
        # The inactivity budget fired, or the peer vanished. Keep what arrived and SAY SO.
        stream_err = f"{type(e).__name__}: {str(e)[:60]}"
        tel["stalled"] = True
    text = "".join(content)
    tel["stream_error"] = stream_err
    # THE SHARE OF THE ANSWER SPENT THINKING. A rod at 0.95 here is not weak, it is deliberating -
    # and it is the difference between a bad rod and a mis-budgeted one, which is exactly the
    # distinction D28 cost a day to make.
    tot = tel["reason_chars"] + tel["content_chars"]
    tel["reason_share"] = round(tel["reason_chars"] / tot, 3) if tot else None
    tel["finish_reason"] = finish
    tel["truncated"] = (finish == "length")
    # ONLY IF NOTHING ELSE CAME does reasoning stand in for the answer, matching the unstreamed
    # path's long-standing fallback (three field names, not two - ollama and cerebras use
    # `reasoning`). A rod that returned pure deliberation is still a non-answer and must fall
    # through the ladder, and it does, because the ladder tests for empty TEXT.
    msg = {"content": text or "".join(reasoning), "tool_calls": tool_calls}
    return dict(choices=[{"message": msg, "finish_reason": finish}], usage=usage,
                telemetry=tel), msg


def _merge_tool_calls(acc, deltas):
    """Tool calls arrive in fragments across deltas: index, then name, then argument slices."""
    acc = list(acc or [])
    for d in deltas:
        i = d.get("index", 0)
        while len(acc) <= i:
            acc.append({"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
        if d.get("id"):
            acc[i]["id"] = d["id"]
        fn = d.get("function") or {}
        if fn.get("name"):
            acc[i]["function"]["name"] = fn["name"]
        if fn.get("arguments"):
            acc[i]["function"]["arguments"] += fn["arguments"]
    return acc


def call_openai(plant: str, model: str, messages, max_tokens=None, temperature=None, timeout=60,
                tools=None, schema=None, seed=None):
    # `schema` AND `seed` - two capabilities the endpoints have always accepted and we never sent.
    #
    # MEASURED 2026-07-30 across all four plants: `seed` accepted everywhere and genuinely
    # deterministic (llama-3.1-70b and groq returned byte-identical output three times at
    # temperature 1.0); `response_format: json_schema` accepted on nvidia and ollama.
    #
    # `seed` turns a standing unknown into a decidable question: `movecontrol` found 3 of 9 cells
    # flipping on identical input and nothing could separate sampling noise from genuine prompt
    # ambiguity. Under a fixed seed, noise disappears and ambiguity does not.
    #
    # `schema` removes a whole failure class. `aea/loop/aea.py` `structure()` exists ONLY because
    # the core could not be trusted to emit clean JSON, and it was the wake's single unladdered
    # dependency - it 429'd on 21 of 27 samples in the frontier run (D29). A rod that can be handed
    # a schema does not need a second model to tidy up after it.
    # `max_tokens=None` MEANS "AS MUCH AS THIS ROD WILL GIVE", NOT 256.
    #
    # Luis, 2026-07-30: "thinking budget shouldn't be cut off. You have to let it think as much as
    # it needs. If not, you're cutting ideas short, you're cutting consensus short. It's like
    # someone is talking and you just suddenly shut him up." And on the economics: NVIDIA charges
    # nothing per token and nothing per request - the only real limits are 40 req/min PER MODEL and
    # the context window the rod itself supports. Every token ceiling below that was invented here.
    #
    # THE COMMENT ABOVE `OWN_PARAMS` HAS SAID THIS SINCE 2026-07-28: "call_openai sends
    # temperature=0.2 and max_tokens=256 to every rod... a reasoning rod handed 256 tokens spends
    # them thinking and never reaches an answer... EVERY fitness score, census and tool probe in
    # this repo was taken through that filter." The table of published values was added. The default
    # that actually decides was not touched, so the diagnosis sat two hundred lines above the defect
    # for two days while every measurement kept going through it. D26, a fifth time - and this is
    # the instance that corrupted the most.
    #
    # RESOLUTION ORDER, most-specific first:
    #   an explicit argument            the caller knows something we do not - always wins
    #   the owner's published ceiling   OWN_PARAMS, lifted from the model's own example
    #   OMIT THE FIELD ENTIRELY         we do not know this rod's ceiling, so we do not invent one;
    #                                   the provider then applies the model's own maximum
    # The last branch is the important one. A "generous default" is still a number we made up, and
    # a made-up number that is too LARGE gets a 400 from rods with small windows. Sending nothing
    # says the true thing: we have no opinion, use yours.
    pub = own_params(model)
    if max_tokens is None:
        max_tokens = pub.get("max_tokens")          # may stay None -> field omitted below
    if temperature is None:
        temperature = pub.get("temperature", 0.2)
    # TIMEOUT IS AN INACTIVITY BUDGET, NOT A DEADLINE, AND `None` MEANS AWAIT THE RESPONSE.
    # Luis, 2026-07-25: "for any model, experimenting and waiting for a response, more than setting
    # timeouts, should be async await for the response... otherwise on chain of tasks it might fail
    # for the wait." He is right, and it was already live: deepseek-v4-pro took 31.1s to return a
    # TWELVE token reply, and the two big nemotrons emit reasoning before their answer. A rod that
    # thinks for 90s before its first byte would trip a fixed 60s wait and be recorded as a FAILURE -
    # a SLOW rod scored as an UNRELIABLE one, which is the same class of error as counting an outage
    # as a wrong answer. urllib applies this value per blocking socket operation rather than to the
    # whole exchange, so passing None waits as long as the peer is alive. Interactive paths keep 60;
    # the lab passes None because a measurement must never be truncated by our own impatience.
    """Low-level OpenAI-compatible chat call.

    Returns dict(ok, latency, text, tokens, prompt_tokens, total_tokens, tool_calls, deprecation,
    status, error).

    THE FULL BILL (2026-07-25): completion_tokens alone is HALF the invoice. Everything the AEA
    actually spends on - the system frame, conversation history, tool schemas, retrieved context -
    arrives as PROMPT tokens and was being discarded. An economy measured on half its cost cannot
    be honest, so both halves are carried now.

    DEPRECATION: platforms announce a rod's death in the response header (NVIDIA sends
    `Deprecation: <iso8601>`). That is ROT with a real timestamp, read rather than simulated - the
    ladder can route off a dying rod BEFORE it dies instead of discovering it as a failure.

    `tools` is passed through when given, so the tool-schema tax can be measured against the
    identical prompt with and without it (the largest invisible cost in an agentic construct).
    """
    cap = PLANTS[plant]
    url = cap["base"].rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) aea-grid/0.1"}  # Groq/CF block default urllib UA (err 1010)
    if cap["auth"]:
        k = key(cap["auth"])
        if not k:
            return dict(ok=False, latency=0, text="", tokens=0, status=0, error=f"no key {cap['auth']}")
        headers["Authorization"] = f"Bearer {k}"
    elif cap.get("anon"):
        headers["Authorization"] = f"Bearer {cap['anon']}"   # keyless-with-placeholder-token (LLM7 'unused')
    payload_out = {"model": model, "messages": messages, "temperature": temperature}
    if max_tokens is not None:                # omitted entirely when unknown - see the note above
        payload_out["max_tokens"] = int(max_tokens)
    if pub.get("top_p") is not None:          # the owners publish 0.7-1.0 and we never sent it
        payload_out["top_p"] = pub["top_p"]
    # EVERY RESPONSE IS STREAMED, SO `timeout` BECOMES A REAL INACTIVITY BUDGET.
    #
    # Luis, 2026-07-30: "all our responses are the streaming kind, so we know in real time that the
    # model is actually thinking. One minute with stream on means dead."
    #
    # THE TWO HALVES ARE ONE DESIGN, and neither works without the other. A NON-streaming call sends
    # nothing until the whole completion is finished, so the socket is idle for the entire
    # generation - "inactive" and "still thinking" are the same observation, and any budget short
    # enough to catch a dead peer also kills a rod mid-thought. That is the corner this code was in:
    # TIMEOUT=45 killed reasoning rods, and raising it to 300 only meant a dead peer held a slot for
    # five minutes. Streaming separates the two, so a rod may think for as long as it likes while a
    # genuinely dead peer is noticed in a minute.
    #
    # urllib applies `timeout` PER BLOCKING SOCKET READ. With a stream, each delta is a read, so the
    # inactivity semantics come out of the transport for free - no clock to keep, nothing to get
    # wrong. Without a stream the same parameter silently means total time. One flag changes what
    # the number means.
    #
    # MEASURED across nvidia, groq and ollama before switching: worst inter-delta gap on ANY rod
    # 0.65s, max p95 0.048s. A 60s budget is ~92x the worst gap observed.
    #
    # LIVENESS COUNTS ANY DELTA, INCLUDING REASONING WE THROW AWAY. `stream_openai` drops
    # `reasoning_content` on purpose (D13 - never speak a rod's private deliberation aloud), which
    # is right for a voice and fatal for a timeout: nemotron-3-ultra-550b emitted SIXTY reasoning
    # deltas before its first content token at 13.0s. Judged on content alone it looked silent the
    # whole time. Here both channels are read; only content is kept.
    payload_out["stream"] = True
    # ASK FOR THE BILL. A stream omits `usage` unless it is requested, and MEASURED on the switch:
    # nvidia and ollama returned tokens=0 on every streamed call while groq still reported. Token
    # accounting feeds the Meter and the cost record, and "THE FULL BILL" note below is explicit
    # that half an invoice is not an honest economy - so silently losing it to a transport change
    # would be the same class of defect as the census measuring its own harness.
    payload_out["stream_options"] = {"include_usage": True}
    if seed is not None:
        payload_out["seed"] = int(seed)
    if schema is not None:
        payload_out["response_format"] = (
            schema if isinstance(schema, dict) and "type" in schema
            else {"type": "json_schema",
                  "json_schema": {"name": "out", "strict": True, "schema": schema}})
    if tools:
        payload_out["tools"] = tools          # the schema rides on EVERY call, used or not - the tax
    body = json.dumps(payload_out).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            dep = r.headers.get("Deprecation")     # the rod's announced death, when the plant says so
            payload, m = _read_stream(r)
        dt = time.time() - t0
        if payload is None:                        # this endpoint will not stream - fall back once
            payload_out.pop("stream", None)
            req = urllib.request.Request(url, data=json.dumps(payload_out).encode("utf-8"),
                                         headers=headers, method="POST")
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=max(timeout, 300)) as r:
                dep = r.headers.get("Deprecation")
                payload = json.loads(r.read().decode("utf-8"))
            dt = time.time() - t0
            m = (payload.get("choices") or [{}])[0].get("message", {}) or {}
        # THREE FIELD NAMES, NOT TWO. nvidia uses reasoning_content, cerebras and OLLAMA use
        # `reasoning`. Reading only the first two returns an empty string from every local
        # qwen3 model, which becomes `ERR:` in a brief section, which fails sections_ok,
        # which demotes the capability. Verified 2026-07-28 against ollama qwen3:1.7b:
        # fields present were [role, reasoning] and content was empty.
        text = (m.get("content") or m.get("reasoning_content") or m.get("reasoning") or "")
        # A 200 carrying an error object is the server failing inside a success envelope,
        # which is how the local llama-server reports its own crash. Labelled here, at the
        # only place that can see the payload.
        _srv_err = isinstance(payload.get("error"), dict)
        usage = payload.get("usage", {}) or {}
        toks = usage.get("completion_tokens", 0) or 0
        ptoks = usage.get("prompt_tokens")
        ttoks = usage.get("total_tokens")
        return dict(ok=True, latency=dt, text=text, tokens=toks, transport=_srv_err,
                    prompt_tokens=ptoks, total_tokens=ttoks,
                    tool_calls=(m.get("tool_calls") or None),
                    telemetry=(payload.get("telemetry") or {}),   # {} on the unstreamed fallback
                    deprecation=dep, status=200, error=None)
    except urllib.error.HTTPError as e:
        # A PROVIDER THAT REJECTS THE STREAM FLAGS IS NOT A FAILING ROD. Some endpoints 400 on
        # `stream_options` (or on `stream` itself) rather than ignoring it, and recording that as
        # the model answering badly is defect 19 again - a transport condition stored as a
        # capability. One retry with the flags removed, then the normal labelling applies.
        if e.code in (400, 422) and payload_out.get("stream"):
            for k in ("stream", "stream_options"):
                payload_out.pop(k, None)
            try:
                req2 = urllib.request.Request(url, data=json.dumps(payload_out).encode("utf-8"),
                                              headers=headers, method="POST")
                t0 = time.time()
                with urllib.request.urlopen(req2, timeout=max(timeout, 300)) as r2:
                    dep = r2.headers.get("Deprecation")
                    payload = json.loads(r2.read().decode("utf-8"))
                m = (payload.get("choices") or [{}])[0].get("message", {}) or {}
                text = (m.get("content") or m.get("reasoning_content") or m.get("reasoning") or "")
                usage = payload.get("usage", {}) or {}
                return dict(ok=True, latency=time.time() - t0, text=text,
                            tokens=usage.get("completion_tokens", 0) or 0,
                            transport=isinstance(payload.get("error"), dict),
                            prompt_tokens=usage.get("prompt_tokens"),
                            total_tokens=usage.get("total_tokens"),
                            tool_calls=(m.get("tool_calls") or None),
                            deprecation=dep, status=200, error=None)
            except Exception:
                pass                              # fall through to the normal error labelling
        # THE LAYER THAT KNOWS IS THE LAYER THAT LABELS. A caller downstream cannot tell a crashed
        # server from a wrong answer by inspecting an error string, and trying to is whack-a-mole
        # against every provider's phrasing forever. This is the same bug TCP had over wireless
        # links, where congestion control read a lossy radio as congestion and collapsed; the fix
        # there was Explicit Loss Notification - the layer that observed the loss says what kind it
        # was. Everything at or above 500, plus 408 and 429, is the SERVER failing, not the model
        # answering badly. That single bit is what stops an outage being recorded as incompetence.
        return dict(ok=False, latency=time.time() - t0, text="", tokens=0, prompt_tokens=None,
                    transport=(e.code >= 500 or e.code in (408, 429)),
                    total_tokens=None, tool_calls=None, deprecation=None, status=e.code,
                    error=(e.read().decode("utf-8", "ignore")[:200] if hasattr(e, "read") else str(e)))
    except Exception as e:
        # Never reached the peer, or the peer died mid-reply: socket errors, DNS, timeouts, a
        # llama-server that terminated. Transport by construction - there is no answer to be wrong.
        return dict(ok=False, latency=time.time() - t0, text="", tokens=0, prompt_tokens=None,
                    transport=True,
                    total_tokens=None, tool_calls=None, deprecation=None, status=0, error=str(e))


def stream_openai(plant: str, model: str, messages, max_tokens=256, temperature=0.2, timeout=60,
                  receipt: dict | None = None):
    """Same call as `call_openai`, but YIELD the answer in pieces as the rod emits them.

    WHY THIS EXISTS, measured 2026-07-29: a spoken turn cannot start until the mind has finished
    thinking, so the person waits the FULL generation before hearing a syllable. Measured on the
    conversation path that is 1.49s of silence on a 550B rod, on top of a 1.15s endpointer. With
    deltas, the first sentence is usually complete after ~0.5s and can be sent to the voice while
    the rest is still being written. The wait stops being the whole reply and becomes the first
    clause of it.

    Yields CONTENT deltas only. A reasoning rod's `reasoning_content` is deliberately dropped:
    D13 recorded a rod spending its whole budget in the reasoning field and returning empty
    content, and speaking a rod's private deliberation aloud would be the same defect wearing a
    different coat. If nothing but reasoning ever arrives, the caller sees zero deltas and an
    `ok` receipt with empty text - which is a non-answer, and must fall through the ladder.

    `receipt` is filled IN PLACE (ok/latency/text/tokens/status/error/transport) because a
    generator cannot return a value the caller can reach. Same error labelling as `call_openai`:
    >=500, 408 and 429 are the SERVER failing, not the model answering badly.

    Metering is the CALLER's job here, exactly as it is for `call_openai` - `complete()` is the
    layer that records spend, and this function stays a pure transport so the two cannot disagree.
    """
    rec = receipt if receipt is not None else {}
    rec.update(ok=False, latency=0.0, text="", tokens=0, prompt_tokens=None, total_tokens=None,
               status=0, error=None, transport=False, plant=plant, model=model, ttfb=None)
    cap = PLANTS[plant]
    url = cap["base"].rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json", "Accept": "text/event-stream",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) aea-grid/0.1"}
    if cap["auth"]:
        k = key(cap["auth"])
        if not k:
            rec.update(error=f"no key {cap['auth']}")
            return
        headers["Authorization"] = f"Bearer {k}"
    elif cap.get("anon"):
        headers["Authorization"] = f"Bearer {cap['anon']}"
    payload_out = {"model": model, "messages": messages, "max_tokens": max_tokens,
                   "temperature": temperature, "stream": True,
                   "stream_options": {"include_usage": True}}
    body = json.dumps(payload_out).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    t0 = time.time()
    parts: list[str] = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            rec["status"] = 200
            for raw in r:                              # urllib yields lines as the socket fills
                line = raw.decode("utf-8", "replace").strip()
                if not line or line.startswith(":") or not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                except ValueError:
                    continue                           # a half-line is not an error, it is a frame
                u = obj.get("usage") or {}
                if u:                                  # the final usage frame, when the plant sends one
                    rec["tokens"] = u.get("completion_tokens", rec["tokens"]) or rec["tokens"]
                    rec["prompt_tokens"] = u.get("prompt_tokens", rec["prompt_tokens"])
                    rec["total_tokens"] = u.get("total_tokens", rec["total_tokens"])
                for ch in (obj.get("choices") or []):
                    piece = ((ch.get("delta") or {}).get("content")
                             or (ch.get("message") or {}).get("content") or "")
                    if piece:
                        if rec["ttfb"] is None:
                            rec["ttfb"] = round(time.time() - t0, 3)
                        parts.append(piece)
                        yield piece
        rec.update(ok=True, text="".join(parts), latency=time.time() - t0)
    except urllib.error.HTTPError as e:
        rec.update(latency=time.time() - t0, status=e.code, text="".join(parts),
                   transport=(e.code >= 500 or e.code in (408, 429)),
                   error=(e.read().decode("utf-8", "ignore")[:200] if hasattr(e, "read") else str(e)))
    except Exception as e:
        rec.update(latency=time.time() - t0, status=0, text="".join(parts),
                   transport=True, error=str(e))


def complete(prompt: str, capability="reasoning", zone="private", depth=0,
             max_tokens=256, router: Router | None = None) -> dict:
    """The entity's front door: route by capability+zone+depth, draw metered power, return text."""
    router = router or Router()
    plant, model, wait = router.pick(capability, zone, depth=depth)
    if not plant:
        return dict(ok=False, text="", error=f"no powered plant for {capability}/{zone} (wait ~{wait}s)")
    res = call_openai(plant, model, [{"role": "user", "content": prompt}], max_tokens=max_tokens)
    if res["status"] == 429:                       # 429 = the breaker: cool THIS bucket (was dead code - review 2026-07-10)
        router.meter.mark_throttled(plant, model)
    else:
        router.meter.record(plant, model, tokens=res.get("tokens", 0))
        if res["ok"]:
            router.meter.clear_strike(plant, model)
    res.update(plant=plant, model=model)
    return res


# --------------------------------------------------------------------------------------
# 5. `python grid.py` -> the city dashboard
# --------------------------------------------------------------------------------------
def dashboard():
    print("AEA GRID - the city's power plants\n" + "=" * 64)
    keyed = unkeyed = 0
    for plant in sorted(PLANTS, key=lambda p: PLANT_RANK.get(p, 99)):
        c = PLANTS[plant]
        has = (c["auth"] is None) or bool(key(c["auth"]))
        keyed += has; unkeyed += (not has)
        zone = {"local": "RESIDENTIAL (private)", "no-train": "RESIDENTIAL (private)",
                "trains": "INDUSTRIAL (public)", "none": "OUTSKIRTS (no guarantee)"}[c["privacy"]]
        lim = []
        if c.get("rpm"): lim.append(f"{c['rpm']} rpm")
        if c.get("rpd"): lim.append(f"{c['rpd']} rpd")
        if c.get("tpd"): lim.append(f"{c['tpd']:,} tok/day")
        if c.get("neurons_day"): lim.append(f"{c['neurons_day']:,} neurons/day")
        if c.get("monthly_calls"): lim.append(f"{c['monthly_calls']}/month")
        flag = "ONLINE " if has else "no-key "
        print(f"  [{flag}] {plant:12} {zone:26} {', '.join(lim) or 'unlimited':28} {c['note']}")
    gens = len(GENERATORS)
    print("=" * 64)
    print(f"  plants online: {keyed}   awaiting key: {unkeyed}   registered generators: {gens}")
    print("  zones: private -> local + no-train only | public -> any | sensitive -> local only")
    print("  density: depth0=large depth1=normal depth2=micro depth3=nano depth4+=pico")

if __name__ == "__main__":
    dashboard()
