"""Quantify REAL capacity. Core question: are NVIDIA's 40 req/min buckets PER-MODEL
(so we can query many models in parallel for huge aggregate throughput)? Measure it."""
import grid, time, json, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

def nvidia_models():
    k = grid.key('NVIDIA_API_KEY')
    req = urllib.request.Request('https://integrate.api.nvidia.com/v1/models',
        headers={'Authorization': f'Bearer {k}', 'User-Agent': 'aea-grid'})
    return [m['id'] for m in json.loads(urllib.request.urlopen(req, timeout=30).read()).get('data', [])]

def ping(model, mx=1, prompt='hi'):
    t = time.time()
    r = grid.call_openai('nvidia', model, [{'role': 'user', 'content': prompt}], max_tokens=mx, timeout=45)
    return {'model': model, 'status': r['status'], 'ok': r['ok'], 'tokens': r['tokens'], 's': round(time.time() - t, 2)}

models = nvidia_models()
print(f"=== NVIDIA catalog: {len(models)} models ===\n")

# TEST 1 - fire 1 tiny request at EVERY model at once: cross-model concurrency + how many actually serve
print(f"TEST 1 - 1 request at all {len(models)} models simultaneously (pool=16):")
t0 = time.time(); res = []
with ThreadPoolExecutor(max_workers=16) as ex:
    for f in as_completed([ex.submit(ping, m) for m in models]):
        res.append(f.result())
el = time.time() - t0
ok = [r for r in res if r['ok']]
n404 = sum(1 for r in res if r['status'] == 404); n429 = sum(1 for r in res if r['status'] == 429)
print(f"  {round(el,1)}s | servable(200)={len(ok)} | 404(not served)={n404} | 429(rate)={n429} | other={len(res)-len(ok)-n404-n429}")
verdict = 'WORKS (independent per-model buckets)' if n429 < 5 else 'GLOBALLY CAPPED'
print(f"  observed {round(len(ok)/el*60)} ok-req/min across distinct models -> cross-model concurrency {verdict}\n")

# TEST 2 - 150-token generation at 5 servable models at once: aggregate token throughput
five = [r['model'] for r in ok][:5]
print(f"TEST 2 - 150-token generation at {len(five)} models in parallel:")
t0 = time.time(); gens = []
with ThreadPoolExecutor(max_workers=len(five)) as ex:
    for f in as_completed([ex.submit(ping, m, 150, 'Write 120 words about the ocean.') for m in five]):
        gens.append(f.result())
el = time.time() - t0
tot = sum(g['tokens'] for g in gens)
print(f"  {round(el,1)}s wall | {tot} tokens across {len(five)} models | aggregate {round(tot/el)} tok/s (vs ~25-60 tok/s single)")
for g in gens:
    print(f"   {g['model'][:44]:44} {g['tokens']:>4} tok  {g['s']}s")
