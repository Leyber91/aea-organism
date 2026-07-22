"""model_fitness.py - THE ENTITY LEARNS ITS OWN TOOLS.

Not a one-off benchmark (models_report.json already is one, and it's stale - it scored
qwen3-next-80b a 4/4, then that model TIMED OUT in brief.py and shipped a hole in the brief).
The failure that catalogue can't see is the one that matters: a model that answers fine on a
happy path and then EMPTY-texts on a low budget, HANGS past a timeout, or hits a rate wall.

So this measures FITNESS, not just quality - for every online general-purpose node, across a
battery shaped like the entity's REAL work, capturing the failure modes explicitly:
  ok | EMPTY (ok-but-blank, the reasoning-model budget trap) | TIMEOUT | RATE (429) | latency | tok/s

Output: model_fitness.json = the entity's self-knowledge, which a flexible per-node picker reads
to choose the right model AND avoid the ones that break for a given job. Meant to be re-run and,
later, updated live from every real call (fitness from use, not from a frozen report).

  python model_fitness.py            # sweep every online general node
  python model_fitness.py --tier deep
"""
import json, sys, time, os
from aea.kernel import grid
from aea.mind import orchestrator
from concurrent.futures import ThreadPoolExecutor, as_completed
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

OUT = os.path.join(grid.STATE, "model_fitness.json")

# The battery is shaped like the entity's ACTUAL jobs, and each probe targets a known failure mode.
BATTERY = {
    # tight budget on a reasoning task = the trap that empty-texted gpt-oss/qwen3 earlier
    "reason_tight": dict(prompt="A bat and ball cost 1.10 total; the bat costs 1.00 more than the ball. "
                                "How much is the ball? Give just the number.", mx=80, want="0.05"),
    # structured output (planner / formatter jobs)
    "json":         dict(prompt='Return ONLY this JSON and nothing else: {"ok": true, "n": 3}', mx=60, want='"n"'),
    # real synthesis load = the brief's actual section work, longer output (catches timeouts/truncation)
    "synth":        dict(prompt="In exactly 3 terse bullets, summarize what a personal AI companion running on "
                                "free infrastructure is for. No preamble, no emoji.", mx=320, want="-"),
    # exact instruction-following (HADES verdicts, routing)
    "instruct":     dict(prompt="Reply with exactly the single word: ONLINE", mx=16, want="ONLINE"),
}

TIMEOUT = 45   # a node that can't answer a tiny job in 45s is unfit for an interactive companion

def probe(plant, model, task, spec):
    t0 = time.time()
    r = grid.call_openai(plant, model, [{"role": "user", "content": spec["prompt"]}],
                         max_tokens=spec["mx"], temperature=0, timeout=TIMEOUT)
    dt = round(time.time() - t0, 1)
    text = (r.get("text") or "").strip()
    # classify the outcome honestly - EMPTY and TIMEOUT are distinct failures, not just "not ok"
    if not r["ok"]:
        err = (r.get("error") or "")
        if r.get("status") == 429 or "429" in err or "rate" in err.lower():
            outcome = "RATE"
        elif "timed out" in err.lower() or dt >= TIMEOUT - 1:
            outcome = "TIMEOUT"
        else:
            outcome = f"ERR{r.get('status')}"
    elif not text:
        outcome = "EMPTY"                     # ok=200 but no content = the silent killer
    else:
        outcome = "ok"
    tok_s = round(r.get("tokens", 0) / dt, 1) if (outcome == "ok" and dt > 0 and r.get("tokens")) else 0
    hit = spec["want"].lower() in text.lower() if outcome == "ok" else False
    return dict(task=task, outcome=outcome, correct=hit, latency=dt, tok_s=tok_s,
                sample=text[:60].replace("\n", " "))


def sweep_node(node):
    plant, model = node["plant"], node["model"]
    res = {"plant": plant, "model": model, "tier": orchestrator.tier_of(node),
           "zone": node["zone"], "probes": {}}
    for task, spec in BATTERY.items():
        res["probes"][task] = probe(plant, model, task, spec)
        time.sleep(0.15)   # gentle within a node; cross-node concurrency does the hammering
    probes = res["probes"].values()
    oks = [p for p in probes if p["outcome"] == "ok"]
    res["reliability"] = round(len(oks) / len(probes), 2)                 # fraction that produced usable text
    res["accuracy"] = round(sum(p["correct"] for p in probes) / len(probes), 2)
    res["avg_latency"] = round(sum(p["latency"] for p in oks) / len(oks), 1) if oks else None
    res["best_tok_s"] = max((p["tok_s"] for p in oks), default=0)
    res["failure_modes"] = sorted({p["outcome"] for p in probes if p["outcome"] != "ok"})
    return res


def main():
    tier = None
    if "--tier" in sys.argv:
        tier = sys.argv[sys.argv.index("--tier") + 1]
    pool = [n for n in orchestrator.load_pool() if orchestrator.is_general(n["model"])]
    if tier:
        pool = [n for n in pool if orchestrator.tier_of(n) == tier]
    print(f"FITNESS SWEEP - {len(pool)} general nodes x {len(BATTERY)} probes = {len(pool)*len(BATTERY)} real calls")
    print(f"battery: {list(BATTERY)}  |  timeout={TIMEOUT}s  |  hammering the grid in parallel\n" + "=" * 74)
    t0 = time.time()
    rows = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(sweep_node, n): n for n in pool}
        for f in as_completed(futs):
            r = f.result(); rows.append(r)
            fm = (" fails=" + ",".join(r["failure_modes"])) if r["failure_modes"] else ""
            print(f"  {r['reliability']:.2f} rel  {str(r['avg_latency']) + 's':>7}  {r['best_tok_s']:>5.0f} tok/s  "
                  f"{r['tier']:6} {r['plant']}/{r['model'][:40]:40}{fm}")
    rows.sort(key=lambda r: (-r["reliability"], -r["accuracy"], r["avg_latency"] if r["avg_latency"] else 99))
    report = {"generated": grid._today(), "timeout_s": TIMEOUT, "battery": list(BATTERY), "nodes": rows}
    grid.atomic_save_json(OUT, report, indent=2)   # readers (energy.ladder / load_pool) must never see a torn file
    print("=" * 74)
    fit = [r for r in rows if r["reliability"] == 1.0 and not r["failure_modes"]]
    print(f"  swept {len(rows)} nodes in {round(time.time()-t0,1)}s  |  {len(fit)} are FULLY FIT (1.0 rel, 0 failures)")
    print(f"  wrote {OUT}")

if __name__ == "__main__":
    main()
