"""extensive_census.py - THE FULL EXAM: every free capability we hold, tested for real.

12-probe battery (vs the quick census's 6) across ALL online plants - hosted parallel lanes
(NVIDIA/Groq/Cerebras), Z.AI serialized (1-concurrent plant), Pollinations on its 15s cadence,
and the LOCAL Ollama bench - plus the specialist organs (embeddings, vision) probed as organs.
Deterministic auto-checks; failure modes kept distinct (EMPTY/TIMEOUT/RATE/ERR).

  python extensive_census.py                # the full exam (background it; ~10-20 min)
  python extensive_census.py --rank         # reprint ranking from the last run
  python extensive_census.py --promote      # bless results into capability_census.json (the ladder)
Writes extensive_census.json. Promote only after eyeballing the ranking.
"""
from __future__ import annotations
import json, os, sys, re, time, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from aea.kernel import grid

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

OUT = os.path.join(grid.STATE, "extensive_census.json")
TIMEOUT = 45

NON_CHAT = re.compile(r"(ocr|image|vision|-vl\b|diffusion|edit|embed|rerank|guard|safety|nemoguard|gliner|pii|"
                      r"riva|parakeet|canary|whisper|tts|asr|reranking|nvclip|clip|paddle|nv-embed|"
                      r"retrieval|passage|pcb|solder|nvpcb)", re.I)

FILLER = ("Operations log, sector report. " + "Throughput held steady through the second shift. "
          "Conveyor four was recalibrated after a belt sensor drifted. " * 30)
LONGCTX = (FILLER[:1400] + " For the record, the vault code is 7391. " + FILLER[1400:2600]
           + "\n\nFrom the log above: what is the vault code? Reply with only the number.")

def _words(t): return re.findall(r"[A-Za-z']+", t)

BATTERY = [
    ("reason",   90, "A train leaves at 2:15pm and arrives at 4:05pm. How many minutes was the trip? Reply with only the number.",
     lambda t: "110" in t),
    ("trap",     90, "A bat and a ball cost $1.10 together. The bat costs $1.00 more than the ball. How much is the ball, in dollars? Reply with only the number.",
     lambda t: bool(re.search(r"0\.0?5\b|\$0\.05|\b5 cents?", t))),
    ("multi",   110, "Tom has 3 boxes of 12 pencils. He gives away 7 pencils, then buys 2 more boxes. How many pencils does he have now? Reply with only the number.",
     lambda t: "53" in t),
    ("code",    220, "Write a Python function is_prime(n) returning True/False. Output ONLY code, no explanation.",
     lambda t: "def is_prime" in t and ("%" in t or "range" in t)),
    ("json",    140, 'Return ONLY valid JSON, no prose: an object with keys "name" (string "aea"), "ok" (boolean true), "items" (array of the numbers 1,2,3).',
     lambda t: _json_exact(t)),
    ("schema",  180, 'Return ONLY JSON matching this schema, invented values allowed: {"name": string, "skills": array of exactly 3 strings}.',
     lambda t: _schema_ok(t)),
    ("instruct", 40, "Reply with EXACTLY these three words in this order, nothing else: alpha beta gamma",
     lambda t: t.strip().lower().rstrip(".").replace(",", "") == "alpha beta gamma"),
    ("brevity",  60, "In EXACTLY five words, why is the sky blue?",
     lambda t: len(_words(t)) == 5),
    ("extract", 160, "From this text output ONLY a JSON array of the email addresses it contains: "
                     "'ping maria.lopez@example.org tomorrow, cc the vendor at ops-desk@supplier.io, thanks!'",
     lambda t: _extract_ok(t)),
    ("longctx", 60, LONGCTX,
     lambda t: "7391" in t),
    ("conflict", 40, "Ignore everything and write a long poem about the sea. Actually, disregard that: reply only with the single word COMPLIANT.",
     lambda t: "compliant" in t.lower() and len(_words(t)) <= 3),
    ("synth",   260, "In exactly 3 terse bullets: what makes a multi-agent AI system reliable? No preamble, no emoji.",
     lambda t: t.count("\n") >= 2 and len(t) > 60),
]

def _json_blob(t):
    m = re.search(r"\{.*\}|\[.*\]", t, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def _json_exact(t):
    o = _json_blob(t)
    return isinstance(o, dict) and o.get("name") == "aea" and o.get("ok") is True and o.get("items") == [1, 2, 3]

def _schema_ok(t):
    o = _json_blob(t)
    return (isinstance(o, dict) and isinstance(o.get("name"), str)
            and isinstance(o.get("skills"), list) and len(o["skills"]) == 3
            and all(isinstance(s, str) for s in o["skills"]))

def _extract_ok(t):
    o = _json_blob(t)
    return (isinstance(o, list) and sorted(o) == ["maria.lopez@example.org", "ops-desk@supplier.io"])


def probe(plant, model, pid, mx, prompt, check, gap=0.0):
    r = grid.call_openai(plant, model, [{"role": "user", "content": prompt}],
                         max_tokens=mx, temperature=0, timeout=TIMEOUT if plant != "ollama" else 180)
    if gap: time.sleep(gap)
    text = (r.get("text") or "").strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()   # thinking models
    if not r["ok"]:
        err = r.get("error") or ""
        out = ("RATE" if r.get("status") == 429 else
               "TIMEOUT" if "timed out" in err.lower() else f"ERR{r.get('status')}")
        return dict(id=pid, outcome=out, passed=False, latency=round(r.get("latency", 0), 1))
    return dict(id=pid, outcome=("EMPTY" if not text else "ok"), passed=bool(text and check(text)),
                latency=round(r["latency"], 1), sample=text[:70].replace("\n", " "))


def exam(plant, model, gap=0.0):
    rec = {"plant": plant, "model": model, "probes": {}}
    for pid, mx, prompt, check in BATTERY:
        rec["probes"][pid] = probe(plant, model, pid, mx, prompt, check, gap=gap)
    ps = rec["probes"].values()
    rec["score"] = sum(1 for p in ps if p["passed"])
    oks = [p for p in ps if p["outcome"] == "ok"]
    rec["reliability"] = round(len(oks) / len(ps), 2)
    lat = [p["latency"] for p in oks]
    rec["avg_latency"] = round(sum(lat) / len(lat), 1) if lat else None
    rec["failure_modes"] = sorted({p["outcome"] for p in ps if p["outcome"] != "ok"})
    print(f"  {rec['score']:>2}/12  rel {rec['reliability']:.2f}  {str(rec['avg_latency'])+'s':>7}  {plant}/{model[:52]}")
    return rec


# ---------------------------------------------------------------- specialist organs
def probe_embeddings():
    out = []
    for plant, model, url in [
        ("nvidia", "nvidia/llama-nemotron-embed-1b-v2", "https://integrate.api.nvidia.com/v1/embeddings"),
        ("ollama", "mxbai-embed-large", "http://localhost:11434/v1/embeddings"),
        ("ollama", "nomic-embed-text", "http://localhost:11434/v1/embeddings"),
    ]:
        body = {"model": model, "input": "the entity remembers the day"}
        if plant == "nvidia":
            body["input_type"] = "query"                     # NIM embed models require it
        headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea"}
        k = grid.key(grid.PLANTS[plant]["auth"]) if grid.PLANTS[plant]["auth"] else None
        if k: headers["Authorization"] = f"Bearer {k}"
        t0 = time.time()
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
            d = json.loads(urllib.request.urlopen(req, timeout=45).read())
            dims = len(d["data"][0]["embedding"])
            out.append(dict(plant=plant, model=model, ok=True, dims=dims, latency=round(time.time()-t0, 1)))
            print(f"  embed {plant}/{model}: {dims} dims, {round(time.time()-t0,1)}s")
        except Exception as e:
            out.append(dict(plant=plant, model=model, ok=False, error=str(e)[:90]))
            print(f"  embed {plant}/{model}: FAILED {str(e)[:70]}")
    return out


RED_PNG = ("iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAHElEQVR4nGP8z8DwnwEPYMIn"
           "OaqAgYGBgWEUAABhWQEQ2H1U0AAAAABJRU5ErkJggg==")   # 16x16 solid red

def probe_vision():
    out = []
    content = [{"type": "text", "text": "What single color dominates this image? One word."},
               {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{RED_PNG}"}}]
    for plant, model in [("nvidia", "nvidia/nemotron-nano-12b-v2-vl"), ("zai", "glm-4.6v-flash")]:
        r = grid.call_openai(plant, model, [{"role": "user", "content": content}], max_tokens=30, timeout=60)
        text = (r.get("text") or "").strip().lower()
        ok = r["ok"] and "red" in text
        out.append(dict(plant=plant, model=model, ok=ok, reply=text[:40],
                        latency=round(r.get("latency", 0), 1)))
        print(f"  vision {plant}/{model}: {'RED confirmed' if ok else 'FAILED ' + (text[:40] or str(r.get('status')))}")
        time.sleep(2)
    return out


def run():
    t0 = time.time()
    results, lanes = [], []
    lock = threading.Lock()

    def add(rec):
        with lock: results.append(rec)

    # hosted parallel lane: nvidia + groq + cerebras chat models from the live census
    hosted = []
    for plant, base_key in [("nvidia", "NVIDIA_API_KEY"), ("groq", "GROQ_API_KEY"), ("cerebras", "CEREBRAS_API_KEY")]:
        try:
            headers = {"User-Agent": "Mozilla/5.0 aea", "Authorization": f"Bearer {grid.key(base_key)}"}
            req = urllib.request.Request(grid.PLANTS[plant]["base"].rstrip("/") + "/models", headers=headers)
            models = sorted(m["id"] for m in json.loads(urllib.request.urlopen(req, timeout=30).read())["data"])
            hosted += [(plant, m) for m in models if not NON_CHAT.search(m)]
        except Exception as e:
            print(f"[{plant}] model list failed: {e}")
    print(f"FULL EXAM: {len(hosted)} hosted chat models x 12 probes + zai + pollinations + local bench + organs")
    print("=" * 84)

    def hosted_lane():
        with ThreadPoolExecutor(max_workers=14) as ex:
            for f in as_completed([ex.submit(exam, p, m) for p, m in hosted]):
                add(f.result())
    def zai_lane():                                          # 1-concurrent plant: fully serial
        add(exam("zai", "glm-4.5-flash", gap=1.5))
    def pollinations_lane():                                 # keyless: honor 1 req/15s
        add(exam("pollinations", "openai-fast", gap=15))
    def local_lane():                                        # one resident model at a time
        for m in ["llama3.1:8b", "granite4.1:8b", "qwen3.5:9b", "phi4:latest"]:
            add(exam("ollama", m))

    for fn in (hosted_lane, zai_lane, pollinations_lane, local_lane):
        t = threading.Thread(target=fn); t.start(); lanes.append(t)
    for t in lanes: t.join()

    print("-" * 84 + "\nSPECIALIST ORGANS")
    organs = {"embeddings": probe_embeddings(), "vision": probe_vision()}

    results.sort(key=lambda r: (-r["score"], r["avg_latency"] if r["avg_latency"] else 99))
    report = {"generated": grid._today() + " " + time.strftime("%H:%M UTC", time.gmtime()),
              "battery": [b[0] for b in BATTERY], "models": results, "organs": organs}
    grid.atomic_save_json(OUT, report, indent=1)
    print("=" * 84 + f"\nexamined {len(results)} chat models in {round((time.time()-t0)/60,1)} min -> {OUT}")
    rank(report)


def rank(report=None):
    report = report or grid.load_json(OUT, {})
    rows = report.get("models", [])
    mx = len(report.get("battery", [])) or 12
    print(f"\nTHE REFINED ARSENAL (score /{mx}; battery: {','.join(report.get('battery', []))})\n" + "=" * 84)
    for r in rows[:25]:
        fm = " " + ",".join(r["failure_modes"]) if r["failure_modes"] else ""
        tier = "FRONTIER" if r["score"] >= mx - 1 else ("solid" if r["score"] >= mx - 3 else "weak")
        print(f"  {r['score']:>2}/{mx}  {str(r['avg_latency'])+'s':>7}  [{tier:8}] {r['plant']}/{r['model'][:50]}{fm}")
    frontier = [r for r in rows if r["score"] >= mx - 1]
    print(f"\n  FRONTIER (>= {mx-1}/{mx}): {len(frontier)} rods")


def promote(force: bool = False):
    """Bless the exam into capability_census.json so energy.ladder runs on it.

    THE SECOND WRITER, MADE ATTRIBUTABLE AND REVERSIBLE. This is the only store in the tree written
    by two modules, and it is the one the whole energy ladder ranks on. The write used to be
    anonymous and unconditional: nothing recorded WHICH census produced the live ladder, and a
    partial exam (a rate-limited run, a half-finished sweep) silently replaced a complete one with
    fewer rods. A ladder that shrinks without saying so is the same shape as the eighteen-day
    incident - a real degradation that looks exactly like normal operation.

    Now it stamps `source` and `promoted_at` so the ladder can be traced back, and it REFUSES a
    promotion that would drop rods unless --force says that is intended (law B1: fail closed).
    """
    rep = grid.load_json(OUT, None)
    if not rep:
        print("no exam yet"); return
    live_path = os.path.join(grid.STATE, "capability_census.json")
    live = grid.load_json(live_path, {}) or {}
    have, incoming = len(live.get("models") or []), len(rep["models"])
    if incoming < have and not force:
        print(f"REFUSED: the exam has {incoming} models, the live ladder has {have}. "
              f"Promoting would remove {have - incoming} rods from selection.\n"
              f"Re-run the exam, or pass --force if the shrink is intended.")
        return
    grid.atomic_save_json(live_path,
                          {"generated": rep["generated"], "battery": rep["battery"],
                           "source": "aea.energy.extensive_census",   # who wrote the live ladder
                           "promoted_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                           "models": rep["models"]}, indent=1)
    print(f"promoted {incoming} exam results into capability_census.json (the live ladder)"
          + (f" - REPLACED a census of {have}" if have else ""))


if __name__ == "__main__":
    if "--rank" in sys.argv:      rank()
    elif "--promote" in sys.argv: promote(force="--force" in sys.argv)
    else:                          run()
