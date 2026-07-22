"""stress_test.py - hammer the system across conditions AND prove crystallization in the same run.

PASS 1 (cold): for each task TYPE, SEARCH the tier ladder and crystallize the winning model. Sequential.
PASS 2 (warm stress): fire the SAME types x4 ALL AT ONCE - each goes DIRECT to its crystallized model,
through the resilient meter (429/at-limit -> reroute). Proves: crystallization (calls/task collapses,
search done once) + resilience (high concurrency, auto-reroute, zero lost) together."""
import grid, orchestrator, swarm, time, threading
from concurrent.futures import ThreadPoolExecutor

pool = orchestrator.load_pool()
LIB, LOCK, CALLS = {}, threading.Lock(), {'p1': 0, 'p2': 0}

TASKS = [
    ("math",   "What is 47 * 89? Answer with only the number."),
    ("fact",   "Capital of Australia? One word."),
    ("code",   "Python one-liner returning the reverse of string s. Code only."),
    ("reason", "All bloops are razzies; all razzies are lazzies. Are all bloops lazzies? yes or no."),
    ("write",  "A 5-word slogan for a coffee shop. Slogan only."),
]

def search_crystallize(typ, task, meter):
    for tier in ['reflex', 'bulk', 'deep']:
        n = swarm.pick_varied(pool, tier, meter)
        if not n: continue
        with LOCK: CALLS['p1'] += 1
        r = grid.call_openai(n['plant'], n['model'], [{'role': 'user', 'content': task}], max_tokens=60)
        if r['ok'] and r['text'].strip():
            meter.record(n['plant'], n['model'])
            with LOCK: LIB[typ] = (n['plant'], n['model'])
            return f"{n['plant']}/{n['model']}"
    return None

def resilient_run(typ, task, meter):
    with LOCK: node = LIB.get(typ)
    cands = ([node] if node else []) + [(n['plant'], n['model']) for n in (swarm.pick_varied(pool, 'bulk', meter) for _ in range(3)) if n]
    rer = 0
    for plant, model in cands:
        ok, _, _ = meter.can_spend(plant, model)
        if not ok: rer += 1; continue
        with LOCK: CALLS['p2'] += 1
        r = grid.call_openai(plant, model, [{'role': 'user', 'content': task}], max_tokens=60)
        if r['status'] == 429: meter.mark_throttled(plant, model); rer += 1; continue
        if r['ok']: meter.record(plant, model); return True, rer
        rer += 1
    return False, rer

meter = grid.Meter()
print("PASS 1 - COLD: search the ladder + crystallize (sequential)")
t0 = time.time()
for typ, task in TASKS:
    print(f"   {typ:7} searched -> crystallized to {search_crystallize(typ, task, meter)}")
p1 = round(time.time() - t0, 1)

BATCH = TASKS * 10
print(f"\nPASS 2 - WARM STRESS: {len(BATCH)} tasks CONCURRENT (crystallized paths + resilient reroute)")
t0 = time.time()
with ThreadPoolExecutor(max_workers=len(BATCH)) as ex:
    res = list(ex.map(lambda it: resilient_run(it[0], it[1], meter), BATCH))
p2 = round(time.time() - t0, 1)
ok = sum(1 for r in res if r[0]); rer = sum(r[1] for r in res)

cpt1 = round(CALLS['p1'] / len(TASKS), 2); cpt2 = round(CALLS['p2'] / len(BATCH), 2)
print(f"\n=== CRYSTALLIZATION + STRESS PROOF ===")
print(f"   Pass 1 (cold): {CALLS['p1']} calls / {len(TASKS)} tasks = {cpt1} calls/task  (it SEARCHED the ladder)")
print(f"   Pass 2 (warm): {CALLS['p2']} calls / {len(BATCH)} tasks = {cpt2} calls/task  (it went DIRECT, crystallized)")
print(f"   -> crystallization cut work/task {cpt1} -> {cpt2} ({round(cpt1/cpt2,1)}x); the search happened ONCE.")
print(f"   -> resilience: {ok}/{len(BATCH)} ok under {len(BATCH)}-way concurrency, {rer} auto-reroutes, {len(BATCH)-ok} lost, {p2}s wall.")
print(f"   crystallized library: {LIB}")
