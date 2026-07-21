"""
probe.py - the grid inspector. Measures the REAL capacity of each plant:
  - connectivity + latency + tokens/sec across a battery of prompt types
  - the actual rate-limit boundary (does NVIDIA truly hold 40 req/min/model?)

Writes benchmarks.json (the control room reads it). Stdlib only.

  python probe.py                 # battery on every ONLINE plant we have a key for
  python probe.py nvidia          # battery on one plant
  python probe.py nvidia --rpm 50 # fire 50 tiny requests at the smallest model to find the 429 wall
"""
import sys, json, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
import grid

OUT = os.path.join(grid.HERE, "benchmarks.json")

# A battery of prompt TYPES - we learn each model's real behaviour, not one happy path.
BATTERY = {
    "factual":   "In one sentence, what is the Kibble-Zurek mechanism?",
    "reasoning": "A bat and ball cost 1.10 total. The bat costs 1.00 more than the ball. How much is the ball? Answer with just the number.",
    "json":      "Return ONLY this JSON, no prose: {\"ok\": true, \"n\": 3}",
    "instruct":  "Reply with exactly the single word: ONLINE",
}

def online_plants():
    out = []
    for plant, c in grid.PLANTS.items():
        if not c["openai"]:                      # probe only OpenAI-compatible plants for now
            continue
        if c["auth"] and not grid.key(c["auth"]):
            continue
        out.append(plant)
    return out

def models_for(plant):
    return [(m, modality, size) for (p, m, modality, size) in grid.GENERATORS
            if p == plant and modality in ("reasoning", "text")]   # chat models only in v0

def battery(plant):
    rows = []
    for model, modality, size in models_for(plant):
        rec = {"plant": plant, "model": model, "size": size, "prompts": {}}
        for name, prompt in BATTERY.items():
            r = grid.call_openai(plant, model, [{"role": "user", "content": prompt}], max_tokens=64)
            tps = (r["tokens"] / r["latency"]) if (r["ok"] and r["latency"] > 0 and r["tokens"]) else 0
            rec["prompts"][name] = {
                "ok": r["ok"], "status": r["status"], "latency_s": round(r["latency"], 2),
                "tokens": r["tokens"], "tok_per_s": round(tps, 1),
                "reply": (r["text"][:80].replace("\n", " ") if r["ok"] else (r["error"] or "")[:80]),
            }
            time.sleep(0.4)                       # be polite; stay well under rpm during the battery
        oks = [p["ok"] for p in rec["prompts"].values()]
        rec["pass_rate"] = round(sum(oks) / len(oks), 2) if oks else 0
        lat = [p["latency_s"] for p in rec["prompts"].values() if p["ok"]]
        rec["avg_latency_s"] = round(sum(lat) / len(lat), 2) if lat else None
        rows.append(rec)
        print(f"  {plant:11} {model:48} pass={rec['pass_rate']}  avg={rec['avg_latency_s']}s")
    return rows

def rpm_wall(plant, n=50, workers=12):
    """Fire n tiny requests at the smallest chat model to find the real 429 boundary."""
    chat = models_for(plant)
    if not chat:
        return {}
    model = sorted(chat, key=lambda t: grid.SIZES.index(t[2]))[0][0]   # smallest
    print(f"\n  RPM WALL probe -> {plant}:{model}  firing {n} tiny requests (max_tokens=1) ...")
    msg = [{"role": "user", "content": "hi"}]
    def one(_):
        t = time.time()
        r = grid.call_openai(plant, model, msg, max_tokens=1, timeout=30)
        return (time.time(), t, r["status"], r["ok"])
    t0 = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(one, i) for i in range(n)]):
            results.append(f.result())
    elapsed = time.time() - t0
    ok = sum(1 for *_, o in results if o)
    r429 = sum(1 for *_, s, _ in results if s == 429)
    other = n - ok - r429
    eff_rpm = round(ok / elapsed * 60, 1) if elapsed > 0 else 0
    out = {"model": model, "fired": n, "ok": ok, "http_429": r429, "other_fail": other,
           "elapsed_s": round(elapsed, 2), "effective_rpm_observed": eff_rpm,
           "verdict": ("429 wall hit - real limit enforced" if r429 else
                       f"no 429 in {n} reqs (~{eff_rpm} rpm sustained) - limit not reached at this burst")}
    print(f"  -> ok={ok} 429={r429} other={other} in {out['elapsed_s']}s  => observed ~{eff_rpm} rpm; {out['verdict']}")
    return out

def main():
    raw = sys.argv[1:]
    do_rpm = "--rpm" in raw
    n = 50; skip = set()
    if do_rpm:
        i = raw.index("--rpm")
        if i + 1 < len(raw) and raw[i + 1].isdigit():
            n = int(raw[i + 1]); skip.add(i + 1)
    args = [a for j, a in enumerate(raw) if not a.startswith("--") and j not in skip]
    plants = args or online_plants()
    print(f"GRID INSPECTOR - probing: {', '.join(plants)}\n" + "=" * 70)
    report = {"generated": grid._today(), "plants": {}}
    for plant in plants:
        if plant not in grid.PLANTS:
            print(f"  unknown plant: {plant}"); continue
        print(f"\n[{plant}] {grid.PLANTS[plant]['note']}")
        report["plants"][plant] = {"battery": battery(plant)}
        if do_rpm:
            report["plants"][plant]["rpm_wall"] = rpm_wall(plant, n=n)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("\n" + "=" * 70 + f"\n  wrote {OUT}")

if __name__ == "__main__":
    main()
