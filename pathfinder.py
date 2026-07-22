"""pathfinder.py - the increase-by-step CRYSTALLIZED PATH algorithm.

The crystallize doctrine applied to the PATH layer (AEA P-axis + seed-3 crystallize + seed-5
self-version + seed-7 ceiling-detect):

  1. CLASSIFY the task into a type (cheap reflex call).
  2. If a CRYSTALLIZED path exists for that type -> use it directly (skip the search). <- the payoff.
  3. Else ESCALATE BY STEP up the tier ladder reflex -> bulk -> deep, with a quality gate
     (ceiling-detect) after each. Goal is re-injected each step (Focused ReAct, the anti-drift win).
     On the hard (deep) step, BURST across N parallel buckets (the energy-unaware burst capacity).
  4. CRYSTALLIZE the winning tier into paths.json -> next same-type task goes straight to it.

Search once, crystallize, run cheap forever. Energy spent on the FIRST instance, not every instance."""
import grid, orchestrator, swarm, sys, json, os
from concurrent.futures import ThreadPoolExecutor
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

PATHS = os.path.join(grid.STATE, 'paths.json')
LADDER = ['reflex', 'bulk', 'deep']

def load(): return json.load(open(PATHS, encoding='utf-8')) if os.path.exists(PATHS) else {}
def save(p): json.dump(p, open(PATHS, 'w', encoding='utf-8'), indent=2)

def classify(task, pool, meter):
    n = swarm.pick_varied(pool, 'reflex', meter) or swarm.pick_varied(pool, 'bulk', meter)
    r = orchestrator.call_node(n, f"Classify this task in ONE lowercase word (math/code/reasoning/write/lookup/extract/other). Output only the word.\nTASK: {task}", meter, 8)
    w = (r['text'] or 'other').strip().lower().split()[0] if r['ok'] else 'other'
    return ''.join(c for c in w if c.isalpha())[:16] or 'other'

def gate(task, ans, pool, meter):
    """ceiling-detect quality gate: did this answer actually solve it?"""
    if not ans or len(ans.strip()) < 3: return False
    n = swarm.pick_varied(pool, 'reflex', meter)
    r = orchestrator.call_node(n, f"Reply ONLY yes or no: does the ANSWER correctly and fully solve the TASK?\nTASK: {task}\nANSWER: {ans[:500]}", meter, 4)
    return r['ok'] and r['text'].strip().lower().startswith('y')

def attempt(task, tier, pool, meter, n_nodes=1):
    prompt = f"TASK (this is your goal - stay on it): {task}\nAnswer it directly and completely."
    nodes = [x for x in (swarm.pick_varied(pool, tier, meter) for _ in range(n_nodes)) if x]
    if not nodes:               # rate-trough / thin pool: a failed tier, not a crash (review 2026-07-10)
        return []
    def work(nd):
        r = orchestrator.call_node(nd, prompt, meter, 400)
        return (nd, r['text'] if r['ok'] else '')
    if len(nodes) == 1:
        return [work(nodes[0])]
    with ThreadPoolExecutor(max_workers=len(nodes)) as ex:
        return list(ex.map(work, nodes))

def solve(task, pool, meter):
    paths = load()
    sig = classify(task, pool, meter)
    steps, answer, final = [], '', None
    # 1. crystallized? -> use the EXACT winning model, not just the tier
    cp = paths.get(sig)
    if cp and cp.get('wins', 0) >= 1 and cp.get('model'):
        nd = {'plant': cp['plant'], 'model': cp['model']}
        prompt = f"TASK (this is your goal - stay on it): {task}\nAnswer it directly and completely."
        r = orchestrator.call_node(nd, prompt, meter, 400); ans = r['text'] if r['ok'] else ''
        steps.append(f"CRYSTALLIZED '{sig}' -> {cp['plant']}/{cp['model']}")
        if gate(task, ans, pool, meter):
            cp['wins'] += 1; save(paths)
            _render(task, sig, True, steps, cp['model'], ans); return ans
        steps.append("  crystallized path failed gate -> re-escalating")
    # 2. escalate by step
    for i, tier in enumerate(LADDER):
        burst = 3 if tier == 'deep' else 1
        results = attempt(task, tier, pool, meter, n_nodes=burst)
        if not results:
            steps.append(f"step {i+1}: {tier:6} no node available - skipping tier"); continue
        if burst > 1:
            steps.append(f"step {i+1}: BURST x{len(results)} @ {tier} (parallel buckets)")
        for nd, ans in results:
            ok = gate(task, ans, pool, meter)
            if burst == 1:
                steps.append(f"step {i+1}: {tier:6} {nd['plant']}/{nd['model'][:30]:30} gate={'PASS' if ok else 'fail'}")
            if ok:
                paths[sig] = {'plant': nd['plant'], 'model': nd['model'], 'tier': tier,
                              'wins': paths.get(sig, {}).get('wins', 0) + 1}; save(paths)
                _render(task, sig, False, steps, f"{nd['model']}{'(burst)' if burst > 1 else ''}", ans); return ans
        answer, final = results[0][1], tier
    _render(task, sig, False, steps, final + '(unverified)', answer); return answer

def _render(task, sig, cryst, steps, tier, ans):
    print(f"\nTASK: {task[:66]}")
    print(f"  type='{sig}'  {'[CRYSTALLIZED -> instant]' if cryst else '[searched the ladder]'}")
    for s in steps: print(f"   {s}")
    print(f"  => final tier: {tier}   answer: {(ans or '').strip()[:90]}")

if __name__ == '__main__':
    pool = orchestrator.load_pool(); meter = grid.Meter()
    if os.path.exists(PATHS): os.remove(PATHS)        # clean demo
    for t in [
        "What is 17 * 23 + 5?",                        # math: first time -> searches + crystallizes
        "Compute 144 / 12 - 3.",                       # math AGAIN -> uses the crystallized path instantly
        "Write a two-line poem about the sea.",        # write: new type -> searches
        "What is 100 - 37 * 2?",                        # math AGAIN -> crystallized
    ]:
        solve(t, pool, meter)
    print(f"\n=== CRYSTALLIZED PATH LIBRARY (paths.json) ===")
    print(json.dumps(load(), indent=2))
