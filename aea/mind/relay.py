"""relay.py - the GENETIC-MEMORY pipeline. Proves dynamic pathing: a fresh model each step reads
ONLY the capsule (goal + what's done + what tools were crystallized) and CONTINUES - a cell
transmitting to the next. = AEA S-axis L5 (predecessor->successor over the backwards channel)
+ seed 10 (backwards channel) + seed 3 (crystallize) + seed 5 (self-version).
Verifiable: did later agents REUSE the crystallized tools? If yes, the memory transmitted."""
import sys
from aea.kernel import grid
from aea.mind import orchestrator
from aea.mind import swarm
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

GOAL = ("Build a tiny shopping-cart pricing toolkit in Python. Each function becomes a crystallized "
        "tool that later functions REUSE by exact name.")
SPEC = [
    ("to_cents",      "to_cents(dollars: float) -> int",               "Convert dollars to integer cents (rounded).", []),
    ("line_total",    "line_total(price_cents: int, qty: int) -> int", "Cents total for one line item.", []),
    ("cart_subtotal", "cart_subtotal(items: list) -> int",             "Sum over items (each a dict with price_cents and qty). You MUST call line_total.", ["line_total"]),
    ("apply_tax",     "apply_tax(subtotal_cents: int, rate: float) -> int", "Add tax to a subtotal in cents (rounded).", []),
    ("checkout",      "checkout(items: list, tax_rate: float) -> str", "Return a receipt string with the dollar total. You MUST call cart_subtotal and apply_tax.", ["cart_subtotal", "apply_tax"]),
]

def extract_def(text):
    t = text.replace('```python', '').replace('```', '')
    i = t.find('def ')
    return t[i:].strip() if i >= 0 else t.strip()

def run():
    pool = orchestrator.load_pool(); meter = grid.Meter()
    capsule = {"goal": GOAL, "tools": {}, "done": []}     # the genetic memory
    print(f"CHALLENGE: {GOAL}\n")
    print("RELAY (each row = a DIFFERENT model, fed ONLY the capsule):")
    log = []
    for (name, sig, desc, expect) in SPEC:
        n = swarm.pick_varied(pool, 'bulk', meter) or orchestrator.pick(pool, 'bulk', 'public', meter)
        tools_txt = "\n".join(f"  - {t}: {capsule['tools'][t]}" for t in capsule['tools']) or "  (none yet)"
        prompt = (f"GOAL: {capsule['goal']}\n"
                  f"CRYSTALLIZED TOOLS already built (call them by exact name where required):\n{tools_txt}\n\n"
                  f"Write ONLY the next Python function (def ...), no prose, no tests:\n  {sig}\n  # {desc}")
        r = orchestrator.call_node(n, prompt, meter, 300)
        code = extract_def(r['text']) if r['ok'] else '# ERR'
        capsule['tools'][name] = sig
        capsule['done'].append({"name": name, "code": code})
        reused = [t for t in expect if t in code]
        ok = set(reused) == set(expect)
        log.append({"name": name, "node": f"{n['plant']}/{n['model']}", "ok": ok, "reused": reused})
        tag = ('reuse ' + ', '.join(expect) + ' -> ' + ('OK' if ok else 'MISS ' + str(reused))) if expect else 'base tool'
        print(f"  [{name:13}] {n['plant']}/{n['model'][:34]:34}  {tag}")
    req = [s for s in SPEC if s[3]]
    passed = sum(1 for l in log if l['reused'] is not None and l['ok'] and [s for s in SPEC if s[0] == l['name']][0][3])
    distinct = len(set(l['node'] for l in log))
    print(f"\n=== GENETIC-MEMORY TRANSMISSION ===")
    print(f"  {distinct} distinct models built {len(SPEC)} functions, each reading ONLY the capsule.")
    print(f"  reuse-required handoffs passed: {passed}/{len(req)}  ->  {'TRANSMITTED' if passed == len(req) else 'PARTIAL'}")
    print(f"\n=== ASSEMBLED TOOLKIT (built across the relay) ===")
    for d in capsule['done']:
        body = d['code'].split('\n')
        head = body[0] if body else ''
        print(f"  {d['name']:13} {head[:70]}")
    return capsule, log

if __name__ == '__main__':
    run()
