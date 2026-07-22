#!/usr/bin/env python
"""build_graph.py - deterministic repo knowledge-graph for agent handoff.

Scans THIS repo (no LLM tokens) and writes ../graph.json: modules + their imports, the design
corpus, state files, web assets, and server endpoints. A fresh conversation reads graph.json to
orient - the directly-connected neighbourhood of a node - instead of re-reading the whole tree.

Refresh any time:  python aea/build_graph.py
"""
import os, re, json, ast

HERE = os.path.dirname(os.path.abspath(__file__))            # aea/
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "graph.json")

nodes, edges = [], []
def node(nid, ntype, **kw): nodes.append({"id": nid, "type": ntype, **kw})
def edge(src, dst, rel): edges.append({"src": src, "dst": dst, "rel": rel})

# --- 1. the runtime package: modules + import edges (deterministic, via AST) ---
mods = sorted(f[:-3] for f in os.listdir(HERE) if f.endswith(".py"))
modset = set(mods)
for m in mods:
    p = os.path.join(HERE, m + ".py")
    doc = ""
    try:
        tree = ast.parse(open(p, encoding="utf-8", errors="ignore").read())
        doc = (ast.get_docstring(tree) or "").split("\n")[0][:120]
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name in modset: edge(m, a.name, "imports")
            elif isinstance(n, ast.ImportFrom) and n.module in modset:
                edge(m, n.module, "imports")
    except Exception as e:
        doc = f"[parse error: {e}]"
    node(m, "module", path=f"aea/{m}.py", purpose=doc)

# --- 2. server endpoints (regex the router) + which module each dispatches to ---
cr = open(os.path.join(HERE, "controlroom.py"), encoding="utf-8", errors="ignore").read()
for ep in sorted(set(re.findall(r'self\.path(?:\.startswith\(|\s*==\s*)"(/[a-z_/]*)', cr))):
    node(ep, "endpoint", served_by="aea/controlroom.py")

# --- 3. design corpus, state, web (leaves - counted, top-level listed) ---
def scan(dirname, ntype, exts):
    d = os.path.join(ROOT, dirname)
    if not os.path.isdir(d): return
    for f in sorted(os.listdir(d)):
        if any(f.endswith(e) for e in exts) and os.path.isfile(os.path.join(d, f)):
            node(f"{dirname}/{f}", ntype, path=f"{dirname}/{f}")
scan("design", "design_doc", [".md"])
scan("state", "state_file", [".json", ".jsonl"])
scan("docs", "doc", [".md"])

counts = {}
for n in nodes: counts[n["type"]] = counts.get(n["type"], 0) + 1
counts["design_concept_sheets"] = len([f for f in os.listdir(os.path.join(ROOT, "design", "concepts")) if f.endswith(".png")]) if os.path.isdir(os.path.join(ROOT, "design", "concepts")) else 0
counts["web_files"] = sum(len(fs) for _, _, fs in os.walk(os.path.join(ROOT, "web")))

graph = {
    "_meta": {
        "what": "Deterministic knowledge-graph of the THE PROBE / aea-city repo, for agent handoff.",
        "how_to_use": "Query a node's directly-connected edges instead of re-reading the tree. "
                      "Regenerate after structural changes: python aea/build_graph.py",
        "run_the_game": "python controlroom.py   (root shim -> aea/controlroom.py, serves :7799)",
        "path_model": "grid.py defines ROOT (walk up to design/.git), STATE=ROOT/state, "
                      "WEB=ROOT/web; .env (keys) loads from ROOT. Code lives in aea/.",
        "counts": counts,
        "node_types": sorted(counts.keys()),
    },
    "nodes": nodes,
    "edges": edges,
}
json.dump(graph, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"graph.json written: {len(nodes)} nodes, {len(edges)} edges -> {OUT}")
print("  counts:", counts)
