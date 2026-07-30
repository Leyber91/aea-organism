"""orchestrator.py - the AEA orchestrator.

Takes a task, SPLITS it into parallel subtasks, assigns each to a NODE chosen by what
that node 'lets and doesn't let' (capability tier, privacy zone, rate budget), runs them
in parallel across independent per-model buckets, then synthesizes one answer.

Built on grid.py (Meter + client) + models_report.json (measured 4/4 scores + speed).

Tiers (what each node is FOR, from the measured battery):
  reflex  - fastest small models (Groq gpt-oss) : routing, classification, quick steps
  bulk    - the 4/4 workhorses (NVIDIA pool)     : the parallel swarm, one per bucket
  deep    - 120B+/675B (Cerebras, big NVIDIA)    : planning + synthesis (the frontier pass)
  vision  - VL models                            : screenshots/charts
  local   - Ollama                               : private, always-on heartbeat
"""
import json, os, time, re, sys
from aea.kernel import grid
from concurrent.futures import ThreadPoolExecutor
try: sys.stdout.reconfigure(encoding='utf-8')   # Windows console is cp1252; model output is utf-8
except Exception: pass

ZONE = {'local': 'private', 'no-train': 'private', 'trains': 'public', 'none': 'public'}

# MODEL POLICY (from the measured battery + SWARM_SPEC): special-purpose models score 4/4 on simple
# text so the router keeps grabbing them for GENERAL reasoning - wrong tool. Tag by TRUE purpose and
# exclude safety/guard/vision/embed/rerank/pii/ocr/translate from the general pool.
SPECIAL_PURPOSE = re.compile(
    r'(content-safety|safety-guard|nemoguard|gliner|pii|embed|rerank|translate|riva|calibration|'
    r'ocr|whisper|tts|diffusion|guard|-vl\b|vision)', re.I)
def is_general(model):
    return not SPECIAL_PURPOSE.search(model)

def load_pool():
    """Every ONLINE, LIVING, measured-good node, with its affordances.

    TWO FILTERS, AND THEY ANSWER DIFFERENT QUESTIONS. `grid.is_retired` asks whether the endpoint
    still EXISTS - measured from the endpoint itself, permanent, and it runs first. `model_fitness`
    then asks how WELL a living rod performs - a dated snapshot, and only ever a demotion.

    THE DOCSTRING USED TO CLAIM THE FIRST AND NEVER DO IT. It said a node "measured unfit (timeouts,
    empty-texts, **gone-404**) is EXCLUDED", and gone-404 was never checked at all: the only gate
    was `model_fitness` reliability, and MEASURED 2026-07-30 that store certifies four of the seven
    withdrawn rods in this pool at reliability 1.0. Seven of twenty-seven public candidates answered
    410 or 404, one of them at bulk rank 1, and in the `exclude=used` fan-out paths that corpse is
    hit deterministically on the second subtask.

    The false claim was the dangerous half, and it is why nobody looked here when `energy.ladder`
    was fixed for exactly this two hours earlier - a verifier called this function "energy.ladder()
    rewritten without the fix". A docstring that guarantees something it does not perform is worse
    than silence, because it answers the question that would have found the bug.

    Worse still, the failure was MISFILED: `trust.record('produce_brief', False)` demoted the
    entity's own capability for what was a supplier withdrawal, so the ledger blamed competence for
    someone else's decommissioning.

    (Local ollama nodes are kept regardless: they are the privacy floor; their quirks are handled
    at the call site.) Proof the fitness half matters: qwen3-next-80b scored 4/4 in the static
    battery, then timed out in production and shipped a hole in the brief; the sweep caught it."""
    rows = grid.load_json(os.path.join(grid.STATE, 'models_report.json'), [])
    fit = {}
    for r in grid.load_json(os.path.join(grid.STATE, 'model_fitness.json'), {}).get('nodes', []):
        fit[(r['plant'], r['model'])] = r
    pool = []
    for r in rows:
        plant, model = r['plant'], r['model']
        if plant not in grid.PLANTS:
            continue
        # DEAD BEFORE UNFIT. A tombstone is measured from the endpoint and is permanent; a fitness
        # row is a dated snapshot and only ever demotes. Checking existence first means a stale
        # sweep can never certify a corpse as healthy, which is exactly what it was doing.
        if grid.is_retired(plant, model):
            continue
        cap = grid.PLANTS[plant]
        online = (cap['auth'] is None) or bool(grid.key(cap['auth'])) or bool(cap.get('anon'))
        if not online:
            continue
        n = {'plant': plant, 'model': model, 'score': r['score'],
             'tok_s': r.get('tok_s') or 0, 'lat': r.get('avg_lat'),
             'privacy': cap['privacy'], 'zone': ZONE[cap['privacy']]}
        f = fit.get((plant, model))
        if f:
            n['reliability'] = f['reliability']
            n['failure_modes'] = f['failure_modes']
            if f['avg_latency'] is not None:
                n['lat'] = f['avg_latency']          # lived latency beats the stale report
            if f['reliability'] < 1.0 and plant != 'ollama':
                continue                              # measured-unfit hosted node: refuse it
        pool.append(n)
    return pool

def tier_of(n):
    m = n['model'].lower()
    if n['plant'] == 'groq': return 'reflex'
    if n['plant'] == 'cerebras' or any(x in m for x in ['120b', '675b', '253b', '235b', '-super-12']):
        return 'deep'
    if n['plant'] == 'ollama': return 'local'
    return 'bulk'

def pick(pool, tier=None, zone='public', meter=None, exclude=()):
    """Choose the best node that LETS this work: 4/4 quality, allowed in the privacy zone,
    matching tier if asked, with rate budget left. exclude = buckets already in use (fan out)."""
    cands = [n for n in pool if n['score'] == 4 and (n['plant'], n['model']) not in exclude
             and n['privacy'] in grid.ZONES[zone] and is_general(n['model'])]
    if tier:
        tiered = [n for n in cands if tier_of(n) == tier]
        cands = tiered or cands
    cands.sort(key=lambda n: (n['lat'] if n['lat'] is not None else 9))   # fastest first
    for n in cands:
        if meter:
            ok, _, _ = meter.can_spend(n['plant'], n['model'])
            if not ok:
                continue
        return n
    # THE METER IS NOT ADVISORY. This used to `return cands[0] if cands else None`, which handed
    # back the node the budget check had JUST refused - after consulting the meter, logging that it
    # was consulted, and then overruling it. That is worse than never checking, because the trace
    # says the guard ran. A rate limit exists to stop a request; a selector that proceeds anyway
    # converts a wait into a 429, and this repo has already written a 429 into an archive as a
    # capability result once. None means WAIT, and every caller in the repo already handles None
    # (brief.py:40, hades.py:40/73, relay.py:35).
    return None

def call_node(n, prompt, meter, max_tokens=400):
    r = grid.call_openai(n['plant'], n['model'], [{'role': 'user', 'content': prompt}], max_tokens=max_tokens)
    if r['ok'] and meter:
        meter.record(n['plant'], n['model'], r.get('tokens', 0))
    return r

PLAN_PROMPT = ('Split this task into 2 to 5 INDEPENDENT subtasks that can run in parallel. '
               'Output ONLY a JSON array, no prose: '
               '[{{"subtask": "<self-contained instruction>", "capability": "reasoning|code|knowledge"}}].\n'
               'TASK: {task}')

def plan(task, pool, meter):
    planner = pick(pool, 'deep', 'public', meter)
    r = call_node(planner, PLAN_PROMPT.format(task=task), meter, 600)
    try:
        arr = json.loads(re.search(r'\[.*\]', r['text'], re.S).group(0))[:5]
        assert arr and all('subtask' in s for s in arr)
    except Exception:
        arr = [{'subtask': task, 'capability': 'reasoning'}]
    return arr, planner

def run(task, zone='public'):
    meter = grid.Meter()
    pool = load_pool()
    print(f"TASK: {task}")
    print(f"POOL: {len(pool)} online nodes  |  zone='{zone}' lets {sorted(grid.ZONES[zone])}\n")

    subs, planner = plan(task, pool, meter)
    print(f"1) SPLIT  (planner: {planner['plant']}/{planner['model']})  ->  {len(subs)} parallel subtasks")
    used, assign = set(), []
    for s in subs:
        n = pick(pool, 'bulk', zone, meter, exclude=used)        # fan across DISTINCT buckets
        used.add((n['plant'], n['model']))
        assign.append((s, n))
        print(f"     [{s.get('capability','?'):9}] {s['subtask'][:50]:50} -> {n['plant']}/{n['model']}")

    print(f"\n2) EXECUTE  ({len(assign)} nodes, in parallel across independent buckets)")
    t0 = time.time()
    def work(item):
        s, n = item
        r = call_node(n, s['subtask'], meter, 350)
        return {'node': f"{n['plant']}/{n['model']}", 'subtask': s['subtask'],
                'ok': r['ok'], 'text': (r['text'] if r['ok'] else 'ERR ' + str(r['status'])), 'lat': round(r['latency'], 1)}
    with ThreadPoolExecutor(max_workers=min(8, len(assign))) as ex:
        results = list(ex.map(work, assign))
    wall = round(time.time() - t0, 1)
    for r in results:
        print(f"     {r['node']:42} {r['lat']}s  {'ok' if r['ok'] else r['text']}")
    print(f"     wall: {wall}s (slowest node, not the sum)")

    syn = pick(pool, 'deep', 'public', meter, exclude={(planner['plant'], planner['model'])})
    merged = "\n\n".join(f"### {r['subtask']}\n{r['text']}" for r in results if r['ok'])
    final = call_node(syn, f"Merge these sub-results into ONE tight answer to: '{task}'\n\n{merged}", meter, 600)
    print(f"\n3) SYNTHESIZE  ({syn['plant']}/{syn['model']})\n")
    print(final['text'])
    return {'task': task, 'split': [r['node'] for r in results], 'final': final['text']}

if __name__ == '__main__':
    run("Write a short technical brief on the AEA free-AI grid covering: "
        "(a) total request capacity and what bounds it, "
        "(b) why independent per-model rate buckets enable a parallel agent swarm, "
        "(c) the crystallize doctrine of dressing cheap models in frontier capability, "
        "(d) the single biggest risk to watch when running it.")
