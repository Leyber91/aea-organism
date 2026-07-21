"""capability_census.py - REFINE THE CATALOG: not "does it serve" but "how CAPABLE is it".

NVIDIA lists ~140 models; 121 in the API; ~39 actually answer; and serving is not capability.
This hammers every SERVING chat model in parallel with a hard battery that SEPARATES strong from
weak, auto-scores what is checkable, and ranks them - so the entity knows which free models are
frontier-grade (its core mind + the top of the escalation ladder) and which are filler.

Modality-aware: OCR / vision / image-edit / diffusion / embed / rerank / guard models are NOT chat;
they are specialist organs, listed apart, never handed a reasoning prompt (the router bug we fixed).

  python capability_census.py                 # full battery over live NVIDIA chat models (parallel)
  python capability_census.py --plants nvidia groq cerebras
  python capability_census.py --rank          # reprint the ranked shortlist from the last census
"""
from __future__ import annotations
import json, os, sys, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import grid

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

OUT = os.path.join(grid.HERE, "capability_census.json")
TIMEOUT = 40

NON_CHAT = re.compile(r"(ocr|image|vision|-vl\b|diffusion|edit|embed|rerank|guard|safety|nemoguard|"
                      r"riva|parakeet|canary|whisper|tts|asr|reranking|nvclip|clip|paddle|nv-embed|"
                      r"retrieval|passage|pcb|solder|nvpcb)", re.I)

# Battery: each item has an auto-check so scoring is deterministic where possible. Hard enough to separate tiers.
BATTERY = [
    dict(id="reason", mx=90, temp=0,
         prompt="A train leaves at 2:15pm and arrives at 4:05pm. How many minutes was the trip? Reply with only the number.",
         check=lambda t: "110" in t),
    dict(id="trap", mx=90, temp=0,
         prompt="A bat and a ball cost $1.10 together. The bat costs $1.00 more than the ball. How much is the ball, in dollars? Reply with only the number.",
         check=lambda t: bool(re.search(r"0\.0?5\b|\b5 cents?\b|\$0\.05", t))),
    dict(id="code", mx=220, temp=0,
         prompt="Write a Python function is_prime(n) that returns True/False. Output ONLY the code, no explanation.",
         check=lambda t: "def is_prime" in t and ("%" in t or "range" in t)),
    dict(id="json", mx=140, temp=0,
         prompt='Return ONLY valid JSON, no prose: an object with keys "name" (string "aea"), "ok" (boolean true), "items" (array of the numbers 1,2,3).',
         check=lambda t: _json_ok(t)),
    dict(id="instruct", mx=40, temp=0,
         prompt="Reply with EXACTLY these three words in this order, nothing else: alpha beta gamma",
         check=lambda t: t.strip().lower().rstrip(".").replace(",", "") == "alpha beta gamma"),
    dict(id="synth", mx=260, temp=0.2,
         prompt="In exactly 3 bullet points, state what makes a multi-agent AI system reliable. Terse, no preamble, no emoji.",
         check=lambda t: t.count("\n") >= 2 and len(t) > 60),   # coherence judged separately by the workflow
]


def _json_ok(t):
    m = re.search(r"\{.*\}", t, re.S)
    if not m:
        return False
    try:
        o = json.loads(m.group(0))
        return o.get("name") == "aea" and o.get("ok") is True and o.get("items") == [1, 2, 3]
    except Exception:
        return False


def list_serving(plant: str, base: str, keyname: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 aea-cap/1.0"}
    k = grid.key(keyname)
    if keyname and not k:
        return []
    if k:
        headers["Authorization"] = f"Bearer {k}"
    try:
        req = urllib.request.Request(base.rstrip("/") + "/models", headers=headers)
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return sorted(m.get("id", "") for m in data.get("data", []) if m.get("id"))
    except Exception as e:
        print(f"[{plant}] /models failed: {e}"); return []


def probe(plant, base, keyname, model, item):
    r = grid.call_openai(plant, model, [{"role": "user", "content": item["prompt"]}],
                         max_tokens=item["mx"], temperature=item["temp"], timeout=TIMEOUT)
    text = (r.get("text") or "").strip()
    if not r["ok"]:
        return dict(id=item["id"], outcome=("TIMEOUT" if "timed out" in (r.get("error") or "").lower()
                    else f"ERR{r.get('status')}"), passed=False, latency=round(r.get("latency", 0), 1), sample="")
    return dict(id=item["id"], outcome=("EMPTY" if not text else "ok"),
                passed=bool(text and item["check"](text)), latency=round(r["latency"], 1),
                tokens=r.get("tokens", 0), sample=text[:80].replace("\n", " "))


def battery(plant, base, keyname, model):
    rec = {"plant": plant, "model": model, "probes": {}, "synth_sample": ""}
    for item in BATTERY:
        p = probe(plant, base, keyname, model, item)
        rec["probes"][item["id"]] = p
        if item["id"] == "synth" and p["outcome"] == "ok":
            rec["synth_sample"] = p["sample"]
        time.sleep(0.1)
    ps = rec["probes"]
    rec["score"] = sum(1 for p in ps.values() if p["passed"])          # 0..6, deterministic
    oks = [p for p in ps.values() if p["outcome"] == "ok"]
    rec["reliability"] = round(len(oks) / len(ps), 2)
    lat = [p["latency"] for p in oks]
    rec["avg_latency"] = round(sum(lat) / len(lat), 1) if lat else None
    rec["failure_modes"] = sorted({p["outcome"] for p in ps.values() if p["outcome"] != "ok"})
    return rec


def run(plants):
    endpoints = {"nvidia": ("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY"),
                 "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
                 "cerebras": ("https://api.cerebras.ai/v1", "CEREBRAS_API_KEY")}
    jobs, specialists = [], {}
    for plant in plants:
        base, keyname = endpoints[plant]
        models = list_serving(plant, base, keyname)
        chat = [m for m in models if not NON_CHAT.search(m)]
        spec = [m for m in models if NON_CHAT.search(m)]
        specialists[plant] = spec
        print(f"[{plant}] {len(models)} serving = {len(chat)} chat + {len(spec)} specialist organs")
        for m in chat:
            jobs.append((plant, base, keyname, m))
    print(f"\nCAPABILITY BATTERY: {len(jobs)} chat models x {len(BATTERY)} probes = {len(jobs)*len(BATTERY)} calls, parallel\n" + "=" * 84)
    rows = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = [ex.submit(battery, p, b, k, m) for (p, b, k, m) in jobs]
        for f in as_completed(futs):
            r = f.result(); rows.append(r)
    rows.sort(key=lambda r: (-r["score"], r["avg_latency"] if r["avg_latency"] else 99))
    report = {"generated": grid._today() + " " + time.strftime("%H:%M UTC", time.gmtime()),
              "battery": [b["id"] for b in BATTERY], "specialists": specialists, "models": rows}
    grid.atomic_save_json(OUT, report, indent=2)   # readers (energy.ladder per draw) must never see a torn file
    print(f"swept {len(rows)} chat models in {round(time.time()-t0,1)}s -> {OUT}\n")
    rank(report)


def rank(report=None):
    report = report or json.load(open(OUT, encoding="utf-8"))
    rows = report["models"]
    print("=" * 84 + "\nREFINED CAPABILITY RANKING (score /6: reason,trap,code,json,instruct,synth)\n" + "=" * 84)
    for r in rows[:22]:
        fm = " " + ",".join(r["failure_modes"]) if r["failure_modes"] else ""
        badge = "FRONTIER" if r["score"] >= 5 else ("solid" if r["score"] >= 4 else "weak")
        print(f"  {r['score']}/6  {str(r['avg_latency'])+'s':>7}  [{badge:8}] {r['plant']}/{r['model'][:52]:52}{fm}")
    frontier = [r for r in rows if r["score"] >= 5]
    print("-" * 84)
    print(f"  FRONTIER tier (>=5/6): {len(frontier)} models -> candidates for the CORE MIND + escalation apex")
    print(f"  specialist organs (non-chat) held apart: "
          + ", ".join(f"{p}:{len(m)}" for p, m in report.get("specialists", {}).items()))


if __name__ == "__main__":
    a = sys.argv
    if "--rank" in a:
        rank()
    else:
        plants = a[a.index("--plants") + 1:] if "--plants" in a else ["nvidia", "groq", "cerebras"]
        run(plants)
