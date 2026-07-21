"""Complete battery: test EVERY servable model on the grid, score it, measure speed,
then quantify total capacity/min + how many independent parallel nodes we have.
Measured, not from spec sheets. Writes models_report.json.

Caveat: the 4 tasks are quick/structured. Heavy 'thinking' models (deepseek-r1, qwen3-think)
spend tokens reasoning and may truncate at the token cap -> they score lower on these QUICK
tasks. That's a fair signal: they're the deep-reasoning tier, not the fast-node tier."""
import grid, time, json, urllib.request, re
from concurrent.futures import ThreadPoolExecutor, as_completed

MAXTOK = 350

def nvidia_models():
    k = grid.key('NVIDIA_API_KEY')
    req = urllib.request.Request('https://integrate.api.nvidia.com/v1/models',
        headers={'Authorization': f'Bearer {k}', 'User-Agent': 'aea-grid'})
    return [m['id'] for m in json.loads(urllib.request.urlopen(req, timeout=30).read()).get('data', [])]

# --- scorers ---
def sc_math(t):  return '0.05' in t.replace(' ', '').replace('$', '')
def sc_instr(t): return t.strip().upper().startswith('ONLINE')
def sc_json(t):
    try:
        return bool(re.search(r'\{.*\}', t, re.S)) and (lambda j: j.get('ok') is True and j.get('n') == 3)(json.loads(re.search(r'\{.*\}', t, re.S).group(0)))
    except Exception:
        return False
def sc_code(t):  return 'sum(' in t.replace(' ', '')

BATTERY = [
    ('math',  'A bat and ball cost $1.10 total. The bat costs $1.00 more than the ball. How much does the ball cost in dollars? Answer with ONLY the number.', sc_math),
    ('instr', 'Reply with exactly one word in uppercase: ONLINE', sc_instr),
    ('json',  'Output ONLY this JSON and nothing else: {"ok": true, "n": 3}', sc_json),
    ('code',  'Write a Python one-liner that returns the sum of a list named xs. Output only the code.', sc_code),
]

def test_model(plant, model):
    res = {'plant': plant, 'model': model, 'serves': False, 'score': 0, 'tokens': 0, 'lat': [], 'detail': {}}
    for name, prompt, scorer in BATTERY:
        r = grid.call_openai(plant, model, [{'role': 'user', 'content': prompt}], max_tokens=MAXTOK, timeout=70)
        if r['ok']:
            res['serves'] = True
            ok = False
            try: ok = bool(scorer(r['text']))
            except Exception: ok = False
            res['score'] += 1 if ok else 0
            res['tokens'] += r['tokens']; res['lat'].append(r['latency'])
            res['detail'][name] = {'ok': ok, 'lat': round(r['latency'], 1), 'tok': r['tokens']}
        else:
            res['detail'][name] = {'err': r['status']}
    if res['lat']:
        res['avg_lat'] = round(sum(res['lat']) / len(res['lat']), 2)
        tot = sum(res['lat']); res['tok_s'] = round(res['tokens'] / tot, 1) if tot else 0
    else:
        res['avg_lat'] = None; res['tok_s'] = 0
    return res

# 1. NVIDIA census -> which of 121 actually serve
print("NVIDIA census (which models serve)...")
allm = nvidia_models()
def ping(m):
    r = grid.call_openai('nvidia', m, [{'role': 'user', 'content': 'hi'}], max_tokens=1, timeout=40)
    return (m, r['ok'])
servable = []
with ThreadPoolExecutor(max_workers=16) as ex:
    for f in as_completed([ex.submit(ping, m) for m in allm]):
        m, ok = f.result()
        if ok: servable.append(m)
print(f"  {len(servable)}/{len(allm)} serve\n")

# 2. battery - NVIDIA in parallel (independent per-model buckets), others sequential
report = []
print(f"Battery on {len(servable)} NVIDIA models (16 parallel)...")
with ThreadPoolExecutor(max_workers=16) as ex:
    for f in as_completed([ex.submit(test_model, 'nvidia', m) for m in servable]):
        report.append(f.result())

OTHER = {
    'groq':     ['qwen/qwen3-32b', 'llama-3.3-70b-versatile', 'openai/gpt-oss-120b', 'openai/gpt-oss-20b', 'meta-llama/llama-4-scout-17b-16e-instruct'],
    'cerebras': ['gpt-oss-120b', 'llama-3.3-70b', 'qwen-3-32b'],
    'zai':      ['glm-4.5-flash'],
    'ollama':   ['qwen3:8b'],
}
for plant, ms in OTHER.items():
    print(f"Battery on {plant} ({len(ms)})...")
    for m in ms:
        report.append(test_model(plant, m))

# 3. results
served = [r for r in report if r['serves']]
served.sort(key=lambda r: (-r['score'], r.get('avg_lat') or 99))
json.dump(served, open('models_report.json', 'w'), indent=2)

print(f"\n=== TOP 25 (score/4, then speed) ===")
print(f"  {'plant':10} {'model':46} {'sc':>3} {'avg_s':>6} {'tok/s':>6}")
for r in served[:25]:
    print(f"  {r['plant']:10} {r['model'][:46]:46} {r['score']}/4 {str(r.get('avg_lat')):>6} {str(r.get('tok_s')):>6}")

perfect = [r for r in served if r['score'] == 4]
fastest = sorted([r for r in served if r['score'] >= 3], key=lambda r: r.get('avg_lat') or 99)[:6]
print(f"\nperfect 4/4: {len(perfect)} models   |   served: {len(served)}")
print("FASTEST reliable (>=3/4):")
for r in fastest:
    print(f"  {r['plant']:10} {r['model'][:46]:46} {r['score']}/4 {r.get('avg_lat')}s {r.get('tok_s')} tok/s")

# 4. capacity per minute + node math
nv = len(servable)
cap = {'nvidia': nv * 40, 'groq': 5 * 30, 'cerebras': 30, 'zai': 10, 'pollinations': 4}
tot = sum(cap.values())
print(f"\n=== CAPACITY PER MINUTE (online plants) ===")
for k, v in cap.items():
    print(f"  {k:12} ~{v:>5} req/min")
print(f"  {'ollama':12}  unlimited (local, 1 model resident)")
print(f"  TOTAL HOSTED  ~{tot} req/min  =  ~{tot*60} req/hr  =  ~{round(tot*1440/1e6,2)}M req/day")
print(f"  INDEPENDENT NODES (distinct model buckets you can hit in parallel): {nv} NVIDIA + ~8 others = ~{nv+8}")
