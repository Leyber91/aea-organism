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
os.makedirs(STATE, exist_ok=True)
WEB = os.path.join(ROOT, "web")              # the front-end: html + js + game/ served from here


def _state(path: str) -> str:
    """A bare filename -> under STATE/. An already-qualified path -> unchanged."""
    return os.path.join(STATE, path) if os.path.dirname(path) == "" else path


# --------------------------------------------------------------------------------------
# 0a. DURABLE PERSISTENCE - the one home for state on disk (engine review 2026-07-10:
#     every store was truncate-written and every loader silently reset to empty on a torn
#     file; for an entity whose thesis is "continuity lives in the files", that was the
#     single worst defect class). All state goes through these three helpers now.
# --------------------------------------------------------------------------------------
def atomic_save_json(path: str, data, indent=None):
    """Write-to-temp then os.replace: a kill mid-write can never leave a truncated store."""
    path = _state(path)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    os.replace(tmp, path)


def load_json(path: str, default):
    """Missing file -> default. CORRUPT file -> quarantine it loudly (never let the next
    save silently cement the loss) and return default."""
    path = _state(path)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception as e:
        try:
            q = f"{path}.corrupt.{int(time.time())}"
            os.replace(path, q)
            print(f"[grid] WARNING: {os.path.basename(path)} unreadable ({str(e)[:60]}) "
                  f"-> quarantined to {os.path.basename(q)}; starting from default")
        except Exception:
            pass
        return default


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
            mif = cap.get("max_inflight")
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
def call_openai(plant: str, model: str, messages, max_tokens=256, temperature=0.2, timeout=60,
                tools=None):
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
    payload_out = {"model": model, "messages": messages,
                   "max_tokens": max_tokens, "temperature": temperature}
    if tools:
        payload_out["tools"] = tools          # the schema rides on EVERY call, used or not - the tax
    body = json.dumps(payload_out).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8")
            dep = r.headers.get("Deprecation")     # the rod's announced death, when the plant says so
        payload = json.loads(raw)
        dt = time.time() - t0
        m = (payload.get("choices") or [{}])[0].get("message", {}) or {}
        text = m.get("content") or m.get("reasoning_content") or ""   # reasoning models put text here
        usage = payload.get("usage", {}) or {}
        toks = usage.get("completion_tokens", 0) or 0
        ptoks = usage.get("prompt_tokens")
        ttoks = usage.get("total_tokens")
        return dict(ok=True, latency=dt, text=text, tokens=toks,
                    prompt_tokens=ptoks, total_tokens=ttoks,
                    tool_calls=(m.get("tool_calls") or None),
                    deprecation=dep, status=200, error=None)
    except urllib.error.HTTPError as e:
        return dict(ok=False, latency=time.time() - t0, text="", tokens=0, prompt_tokens=None,
                    total_tokens=None, tool_calls=None, deprecation=None, status=e.code,
                    error=(e.read().decode("utf-8", "ignore")[:200] if hasattr(e, "read") else str(e)))
    except Exception as e:
        return dict(ok=False, latency=time.time() - t0, text="", tokens=0, prompt_tokens=None,
                    total_tokens=None, tool_calls=None, deprecation=None, status=0, error=str(e))


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
