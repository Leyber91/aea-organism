"""capacity.py - THE LIVE CAPACITY GAUGE: how much free power do we ACTUALLY have, right now?

Not the June numbers - a live census. Models rot (8 NVIDIA models TIMEOUTed between the June battery
and today's fitness sweep), so capacity must be MEASURED, then TAMED (budgeted), never recalled.

What it does:
  1. NVIDIA census - list the catalog, then probe EVERY model with a 1-token call in parallel:
     how many actually answer chat right now (serving), vs 404/timeout. Capacity = serving x 40 rpm
     (per-model independent buckets, proven June 26: 0/121 429s when hitting all at once).
  2. Groq / Cerebras / Z.AI - one tiny call each, capturing the x-ratelimit-* RESPONSE HEADERS:
     the provider's OWN statement of our current requests/day + tokens/min. Ground truth, no guessing.
  3. Ollama (local) - model count + a warm tokens/sec measurement = the unlimited private floor.
  4. Writes capacity.json (the entity's power gauge - live.py/brief.py can read it) and prints
     the TAMING: aggregate capacity vs what the entity's real daily load consumes.

  python capacity.py            # full live census (~90s, ~130 one-token calls)
  python capacity.py --gauge    # just re-print the last census + budget math
"""
from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import grid

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

OUT = os.path.join(grid.HERE, "capacity.json")
TIMEOUT_PROBE = 25   # a model that can't emit 1 token in 25s is not interactive capacity


def _call_raw(base: str, keyname: str | None, model: str, max_tokens: int = 1, timeout: int = TIMEOUT_PROBE):
    """Raw chat call that RETURNS THE HEADERS (grid.call_openai discards them; the headers are the census)."""
    url = base.rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea-capacity/1.0"}
    if keyname:
        k = grid.key(keyname)
        if not k:
            return {"ok": False, "status": 0, "error": f"no key {keyname}", "headers": {}}
        headers["Authorization"] = f"Bearer {k}"
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": "hi"}],
                       "max_tokens": max_tokens, "temperature": 0}).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            rl = {k.lower(): v for k, v in r.headers.items() if "ratelimit" in k.lower()}
            return {"ok": True, "status": 200, "latency": round(time.time() - t0, 1), "headers": rl}
    except urllib.error.HTTPError as e:
        rl = {k.lower(): v for k, v in (e.headers or {}).items() if "ratelimit" in k.lower()}
        return {"ok": False, "status": e.code, "latency": round(time.time() - t0, 1), "headers": rl,
                "error": (e.read().decode("utf-8", "ignore")[:120] if hasattr(e, "read") else "")}
    except Exception as e:
        return {"ok": False, "status": 0, "latency": round(time.time() - t0, 1), "headers": {},
                "error": str(e)[:80]}


def _list_models(base: str, keyname: str | None) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 aea-capacity/1.0"}
    if keyname:
        k = grid.key(keyname)
        if not k:
            return []
        headers["Authorization"] = f"Bearer {k}"
    try:
        req = urllib.request.Request(base.rstrip("/") + "/models", headers=headers)
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return sorted(m.get("id", "") for m in data.get("data", []) if m.get("id"))
    except Exception:
        return []


# ------------------------------------------------------------------ NVIDIA: the full census
def census_nvidia() -> dict:
    models = _list_models("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY")
    print(f"[nvidia] catalog lists {len(models)} models - probing EVERY one with a 1-token call...")
    serving, dead, timeout_ = [], [], []
    def probe(m):
        r = _call_raw("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY", m)
        return m, r
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=14) as ex:
        for f in as_completed([ex.submit(probe, m) for m in models]):
            m, r = f.result()
            if r["ok"]:
                serving.append(m)
            elif r["status"] == 0 and "timed out" in (r.get("error") or ""):
                timeout_.append(m)
            else:
                dead.append(m)
    dt = round(time.time() - t0, 1)
    print(f"[nvidia] census done in {dt}s: {len(serving)} SERVING / {len(dead)} dead(4xx/5xx) / {len(timeout_)} timeout")
    return {"catalog": len(models), "serving": len(serving), "dead": len(dead), "timeout": len(timeout_),
            "rpm_per_model": 40, "rpm_total": len(serving) * 40,
            "rpd_total_theoretical": len(serving) * 40 * 60 * 24,
            "serving_models": serving, "timeout_models": timeout_}


# ------------------------------------------------------------------ header plants: their own statement
def census_headers(plant: str, base: str, keyname: str, models: list[str]) -> dict:
    out = {"models": {}}
    for m in models:
        r = _call_raw(base, keyname, m, max_tokens=1)
        out["models"][m] = {"ok": r["ok"], "status": r["status"], "ratelimit_headers": r["headers"]}
        hdr = ", ".join(f"{k}={v}" for k, v in sorted(r["headers"].items())) or "(no ratelimit headers)"
        print(f"[{plant}] {m}: {'ok' if r['ok'] else r['status']}  {hdr[:150]}")
        time.sleep(1.2)          # polite: these plants are org-bucketed, don't poison the reading
    return out


# ------------------------------------------------------------------ local floor
def census_local() -> dict:
    try:
        tags = json.loads(urllib.request.urlopen(
            urllib.request.Request("http://localhost:11434/api/tags"), timeout=6).read())
        n_models = len(tags.get("models", []))
    except Exception:
        return {"up": False}
    r = grid.call_openai("ollama", "llama3.1:8b", [{"role": "user", "content":
        "Count from one to ten in words, one per line."}], max_tokens=80, timeout=180)
    tps = round(r["tokens"] / r["latency"], 1) if (r["ok"] and r["latency"] > 0 and r["tokens"]) else 0
    print(f"[ollama] {n_models} models local; llama3.1:8b warm at {tps} tok/s (private, unlimited)")
    return {"up": True, "models": n_models, "warm_tok_s": tps, "rpm": None, "note": "unlimited, private floor"}


# ------------------------------------------------------------------ the taming: budget vs load
def gauge(report: dict):
    nv = report.get("nvidia", {})
    print("\n" + "=" * 76 + "\nTHE POWER GAUGE - live free capacity, and how tamed it is\n" + "=" * 76)
    rpm = nv.get("rpm_total", 0)
    print(f"  NVIDIA   : {nv.get('serving',0)}/{nv.get('catalog',0)} models serving NOW "
          f"-> {rpm:,} req/min aggregate ({nv.get('rpd_total_theoretical',0):,} req/day theoretical)")
    for plant in ("groq", "cerebras", "zai"):
        p = report.get(plant, {})
        for m, d in p.get("models", {}).items():
            h = d.get("ratelimit_headers", {})
            rd = h.get("x-ratelimit-limit-requests") or h.get("x-ratelimit-limit-requests-day") or "?"
            tm = h.get("x-ratelimit-limit-tokens") or h.get("x-ratelimit-limit-tokens-minute") or "?"
            td = h.get("x-ratelimit-limit-tokens-day") or ""
            print(f"  {plant:9}: {m[:40]:40} {'OK ' if d.get('ok') else str(d.get('status'))} "
                  f" req/day={rd}  tok/min={tm}" + (f"  tok/day={td}" if td else ""))
    lo = report.get("ollama", {})
    if lo.get("up"):
        print(f"  ollama   : {lo['models']} local models, {lo['warm_tok_s']} tok/s warm - UNLIMITED private floor")
    # the load side: what the entity actually consumes in a full day of life
    brief_calls, brief_toks = 6, 4_000
    slice_per_day = 48 * 3                     # live.py: 30-min ticks -> ~48 sleep ticks x 3 sessions (local only)
    print("-" * 76)
    print(f"  DAILY LOAD (the entity's real day): 1 brief ~{brief_calls} hosted calls + ~{brief_toks:,} tokens;")
    print(f"    consolidation ~{slice_per_day} sessions/day - LOCAL ONLY (zero hosted spend);")
    print(f"    fitness sweep 176 calls/week; HADES + trust: local.")
    if rpm:
        day_cap = nv.get("rpd_total_theoretical", 1)
        used = brief_calls + 176 / 7
        print(f"  UTILISATION of hosted capacity: ~{used:.0f} calls/day of ~{day_cap:,} available "
              f"= {100*used/day_cap:.4f}%  (we are using one ten-thousandth of the free power)")
    print("  TAMED means: the Meter paces per-bucket so 24/7 use NEVER browns out; the idle 99.99%")
    print("  is headroom for councils - N models arguing over one answer - which is what buys quality.")


def main():
    if "--gauge" in sys.argv:
        try:
            gauge(json.load(open(OUT, encoding="utf-8")))
        except Exception as e:
            print(f"no census yet ({e}) - run: python capacity.py")
        return
    report = {"generated": grid._today() + " " + time.strftime("%H:%M UTC", time.gmtime())}
    report["nvidia"] = census_nvidia()
    report["groq"] = census_headers("groq", "https://api.groq.com/openai/v1", "GROQ_API_KEY",
                                    ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "qwen/qwen3-32b"])
    report["cerebras"] = census_headers("cerebras", "https://api.cerebras.ai/v1", "CEREBRAS_API_KEY",
                                        ["gpt-oss-120b"])
    report["zai"] = census_headers("zai", "https://api.z.ai/api/paas/v4", "ZAI_API_KEY",
                                   ["glm-4.5-flash"])
    report["ollama"] = census_local()
    grid.atomic_save_json(OUT, report, indent=2)
    print(f"\nwrote {OUT}")
    gauge(report)


if __name__ == "__main__":
    main()
