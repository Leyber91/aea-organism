"""swarm.py - the recursive, self-monitoring swarm. Answers: WHEN does a role spawn a sub-agent?

Each agent runs a fast TRIAGE (the spawn decision) before acting:
  - decompose -> the task has independent parts -> spawn one sub-agent per part (parallel, P-fork/M-growth)
  - escalate  -> needs deeper reasoning than this tier -> hand to a deeper node (ceiling-detect / seed 7)
  - answer    -> atomic -> answer directly
  - depth cap -> at MAX_DEPTH it MUST answer (the pico floor; no infinite ramification)

Size shrinks with depth (deep@root -> reflex@leaf = pico..large ramification).
Every agent logs task->node->output->eval into a TRACE TREE = the PROPAGATE verb
(the swarm aware of its own tasks + outputs), with a SILENT-WRONG-WORK flag (the honesty node)."""
import json, re, sys, time, random, threading
from aea.kernel import grid
from aea.mind import orchestrator
from concurrent.futures import ThreadPoolExecutor
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

MAX_DEPTH = 2                                 # depths 0,1,2 -> 3 levels; depth 2 = forced leaf
DEPTH_TIER = {0: 'deep', 1: 'bulk', 2: 'reflex'}
TRACE, TLOCK = [], threading.Lock()

def pick_varied(pool, tier, meter, topk=8):
    """Spread load across DISTINCT buckets: random among the top-k fast 4/4 nodes of a tier."""
    c = [n for n in pool if n['score'] == 4 and orchestrator.tier_of(n) == tier and n['privacy'] in grid.ZONES['public']]
    c.sort(key=lambda n: n['lat'] if n['lat'] is not None else 9)
    c = c[:topk] or [n for n in pool if n['score'] == 4]
    random.shuffle(c)
    for n in c:
        ok, _, _ = meter.can_spend(n['plant'], n['model'])
        if ok: return n
    return c[0] if c else None

TRIAGE = ('You are a sub-agent at depth {d}. Decide how to handle the task.\n'
          'Output ONLY JSON: {{"action":"answer"|"decompose","subtasks":["...","..."]}}\n'
          '- "decompose" with 2-4 INDEPENDENT subtasks ONLY if it genuinely has separable parts.\n'
          '- else "answer". At depth {m} you MUST answer.\nTASK: {t}')

def triage(task, depth, pool, meter):
    if depth >= MAX_DEPTH:
        return ('answer', [])
    n = pick_varied(pool, 'reflex', meter) or pick_varied(pool, 'bulk', meter)
    r = orchestrator.call_node(n, TRIAGE.format(d=depth, m=MAX_DEPTH, t=task), meter, 300)
    try:
        j = json.loads(re.search(r'\{.*\}', r['text'], re.S).group(0))
        if j.get('action') == 'decompose' and len(j.get('subtasks', [])) >= 2:
            return ('decompose', [s for s in j['subtasks'][:4] if isinstance(s, str)])
    except Exception:
        pass
    return ('answer', [])

def agent(task, depth, pool, meter, parent):
    action, subtasks = triage(task, depth, pool, meter)
    with TLOCK:
        nid = len(TRACE)
        rec = {'id': nid, 'parent': parent, 'depth': depth, 'task': task,
               'action': action, 'node': None, 'output': '', 'eval': None, 'children': []}
        TRACE.append(rec)
    if action == 'decompose':
        with ThreadPoolExecutor(max_workers=min(4, len(subtasks))) as ex:
            kids = list(ex.map(lambda st: agent(st, depth + 1, pool, meter, nid), subtasks))
        rec['children'] = [k['id'] for k in kids]
        syn = orchestrator.pick(pool, 'deep', 'public', meter)
        rec['node'] = f"{syn['plant']}/{syn['model']}"
        merged = "\n\n".join(f"- {TRACE[c]['task']}: {TRACE[c]['output'][:300]}" for c in rec['children'])
        r = orchestrator.call_node(syn, f"Synthesize these into one tight answer for '{task}':\n{merged}", meter, 450)
        rec['output'] = r['text']; rec['eval'] = 'ok' if r['ok'] else 'FLAG'
    else:
        n = pick_varied(pool, DEPTH_TIER.get(depth, 'reflex'), meter) or pick_varied(pool, 'bulk', meter)
        rec['node'] = f"{n['plant']}/{n['model']}"
        r = orchestrator.call_node(n, task, meter, 300)
        rec['output'] = r['text'] if r['ok'] else ('ERR ' + str(r['status']))
        rec['eval'] = 'ok' if (r['ok'] and len(r['text'].strip()) > 25) else 'SILENT-WRONG-WORK'
    return rec

def render(rid=0, indent=0):
    r = TRACE[rid]
    pad = '   ' * indent
    mark = '+' if r['action'] == 'decompose' else '-'
    flag = '' if r['eval'] in (None, 'ok') else f"  [!{r['eval']}]"
    print(f"{pad}{mark} d{r['depth']} ({r['action']:9}) {r['task'][:58]}")
    print(f"{pad}     -> {r['node']}{flag}")
    for c in r['children']:
        render(c, indent + 1)

if __name__ == '__main__':
    meter = grid.Meter(); pool = orchestrator.load_pool()
    task = ("Design a 3-tier loyalty program for a specialty coffee shop: the tiers and their perks, "
            "the points mechanics, and a 2-week launch plan.")
    print(f"ROOT TASK: {task}\nPOOL: {len(pool)} online nodes  |  depth cap {MAX_DEPTH}\n")
    t0 = time.time()
    root = agent(task, 0, pool, meter, None)
    wall = round(time.time() - t0, 1)
    print("=== PROPAGATE TRACE  (the swarm's awareness of its own work) ===")
    render(0)
    spawned = len(TRACE)
    flags = sum(1 for r in TRACE if r['eval'] not in (None, 'ok'))
    print(f"\nagents spawned: {spawned}  |  silent-wrong-work flags: {flags}  |  wall: {wall}s")
    print(f"\n=== ROOT OUTPUT ===\n{root['output'][:900]}")
