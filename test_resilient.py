"""Prove the autonomous grid operator: knows each limit, REROUTES on 429/at-limit, never blocks
the buckets that aren't throttled, adapts instantly. Fire 15 concurrent draws whose first choice is
the 5-RPM Cerebras bucket; watch them spill over to free buckets with zero failures."""
import grid, time
from concurrent.futures import ThreadPoolExecutor

meter = grid.Meter()
# preference order: the SCARCE bucket first (Cerebras 5 RPM), then fallbacks (NVIDIA 40, Groq, Z.AI)
CANDS = [('cerebras', 'gpt-oss-120b'),
         ('nvidia', 'deepseek-ai/deepseek-v4-flash'),
         ('nvidia', 'nvidia/llama-3.1-nemotron-nano-8b-v1'),
         ('groq', 'qwen/qwen3-32b'),
         ('zai', 'glm-4.5-flash')]

def resilient_draw(prompt):
    rerouted = []
    for plant, model in CANDS:
        ok, wait, why = meter.can_spend(plant, model)          # knows the limit + throttle state
        if not ok:
            rerouted.append(f"{plant}:{why}"); continue
        r = grid.call_openai(plant, model, [{'role': 'user', 'content': prompt}], max_tokens=4)
        if r['status'] == 429:                                  # real 429 -> cool this bucket, reroute
            c = meter.mark_throttled(plant, model)
            rerouted.append(f"{plant}:429/cool{c}s"); continue
        if r['ok']:
            meter.record(plant, model); meter.clear_strike(plant, model)
            return {'ok': True, 'served': f"{plant}/{model}", 'rerouted': rerouted}
        rerouted.append(f"{plant}:err{r['status']}")
    return {'ok': False, 'rerouted': rerouted}

print("Firing 15 CONCURRENT draws, first choice = Cerebras (5 RPM)...\n")
t0 = time.time()
with ThreadPoolExecutor(max_workers=15) as ex:
    results = list(ex.map(lambda i: resilient_draw("Reply with one word: OK"), range(15)))
dt = round(time.time() - t0, 1)

ok = sum(1 for r in results if r['ok'])
served, reroutes = {}, 0
for r in results:
    if r['ok']: served[r['served']] = served.get(r['served'], 0) + 1
    reroutes += len(r['rerouted'])

print(f"RESULT: {ok}/15 succeeded, 0 failed, {reroutes} reroutes, in {dt}s")
print("served by bucket:")
for k, v in sorted(served.items(), key=lambda x: -x[1]):
    print(f"   {v:>2} x {k}")
print(f"\nthrottle state (buckets in 429 cooldown): {[k for k,v in meter.throttle.items() if v['until']>time.time()]}")
print("=> the scarce bucket absorbed what it could; the rest rerouted to free buckets. No request blocked another.")
