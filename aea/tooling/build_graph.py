#!/usr/bin/env python
"""build_graph.py - the master orchestrator graph over subgraphs, for agent handoff.

Scans THIS repo (no LLM tokens) and writes graph.json at the repo root. A MASTER graph whose root
(THE_PROBE) connects to SUBGRAPHS, each reachable (access guaranteed) and independently queryable:

    code         - the runtime package: modules (across all subpackages), imports (via AST), endpoints
    plan          - the design corpus + docs (the design, chapter by chapter)
    reflections   - Luis's raw sparks (parsed from diary/REFLECTIONS.md)
    discoveries   - what we learned, as findings (parsed from diary/DISCOVERIES.md)
    references    - where the authoritative sources live (parsed from references/README.md)

A fresh conversation enters at the master, drills into one subgraph, and pulls only the
directly-connected neighbourhood of the node it needs - never re-scanning the tree.

Refresh any time:  python aea/tooling/build_graph.py
"""
import os, re, json, ast

HERE = os.path.dirname(os.path.abspath(__file__))          # aea/tooling/
AEA = os.path.dirname(HERE)                                # aea/  (the runtime package)
ROOT = os.path.dirname(AEA)                                # repo root
OUT = os.path.join(ROOT, "graph.json")


def sub_code():
    """Walk the whole aea/ package (all subpackages) for modules + their import edges.
    After the 2026-07-22 subpackage reorg, internal imports are `from aea.<pkg> import <mod>` or
    `from aea.<pkg>.<mod> import <name>` - detect both against the set of module basenames."""
    nodes, edges = [], []
    mods = {}                                              # basename -> repo-relative path
    for root, _dirs, files in os.walk(AEA):
        for f in sorted(files):
            if f.endswith(".py") and f != "__init__.py":
                mods[f[:-3]] = os.path.relpath(os.path.join(root, f), ROOT).replace(os.sep, "/")
    modset = set(mods)
    for m, rel in sorted(mods.items()):
        doc = ""
        try:
            tree = ast.parse(open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore").read())
            doc = (ast.get_docstring(tree) or "").split("\n")[0][:110]
            for n in ast.walk(tree):
                if isinstance(n, ast.ImportFrom) and n.module and n.module.startswith("aea."):
                    last = n.module.split(".")[-1]
                    if last in modset:                     # from aea.<pkg>.<mod> import X
                        edges.append({"src": m, "dst": last, "rel": "imports"})
                    else:                                  # from aea.<pkg> import <mod>[, <mod2>]
                        for a in n.names:
                            if a.name in modset:
                                edges.append({"src": m, "dst": a.name, "rel": "imports"})
        except Exception as e:
            doc = f"[parse error: {e}]"
        nodes.append({"id": m, "type": "module", "path": rel, "purpose": doc})
    cr = mods.get("controlroom")
    if cr:
        txt = open(os.path.join(ROOT, cr), encoding="utf-8", errors="ignore").read()
        for ep in sorted(set(re.findall(r'self\.path(?:\.startswith\(|\s*==\s*)"(/[a-z_/]*)', txt))):
            nodes.append({"id": ep, "type": "endpoint", "served_by": cr})
    return nodes, edges


def sub_plan():
    nodes = []
    for dirname in ("design", "docs"):
        d = os.path.join(ROOT, dirname)
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md") and os.path.isfile(os.path.join(d, f)):
                nodes.append({"id": f"{dirname}/{f}", "type": "design_doc", "path": f"{dirname}/{f}"})
    return nodes, []


def _headings(path, pat):
    if not os.path.isfile(path): return []
    out = []
    for ln in open(path, encoding="utf-8", errors="ignore"):
        m = re.match(pat, ln.strip())
        if m: out.append(m.group(1).strip())
    return out


def sub_discoveries():
    heads = _headings(os.path.join(ROOT, "diary", "DISCOVERIES.md"), r"^##\s+(.+)")
    nodes = [{"id": h.split("·")[0].strip() if "·" in h else h[:40], "type": "discovery",
              "title": h, "path": "diary/DISCOVERIES.md"} for h in heads]
    return nodes, []


def sub_reflections():
    heads = _headings(os.path.join(ROOT, "diary", "REFLECTIONS.md"), r"^##\s+(.+)")
    nodes = [{"id": h.split("·")[0].strip() if "·" in h else h[:40], "type": "reflection",
              "title": h, "path": "diary/REFLECTIONS.md"} for h in heads]
    return nodes, []


def sub_references():
    heads = _headings(os.path.join(ROOT, "references", "README.md"), r"^##\s+(.+)")
    nodes = [{"id": h.split("—")[0].strip() if "—" in h else h[:40], "type": "reference",
              "title": h, "path": "references/README.md"} for h in heads]
    return nodes, []


SUBS = {"code": sub_code, "plan": sub_plan, "reflections": sub_reflections,
        "discoveries": sub_discoveries, "references": sub_references}
subgraphs, master_edges = {}, []
for name, fn in SUBS.items():
    n, e = fn()
    subgraphs[name] = {"nodes": n, "edges": e}
    master_edges.append({"src": "THE_PROBE", "dst": name, "rel": "contains", "count": len(n)})

# access guarantee: every declared subgraph is present and non-empty
missing = [k for k, v in subgraphs.items() if not v["nodes"]]
assert not missing, f"ACCESS NOT GUARANTEED - empty subgraph(s): {missing}"

graph = {
    "_meta": {
        "what": "Master orchestrator graph over subgraphs of the THE PROBE / aea-city repo, for handoff.",
        "entry_point": "CLAUDE.md - the stable introduction (auto-loaded in Claude Code): HOW to work "
                       "here + WHERE everything is. It sends you here (the graph) and to diary/SESSION_LOG "
                       "(the state). Method+map live in CLAUDE.md; state lives in the diary.",
        "how_to_use": "Enter at master.root (THE_PROBE); follow a 'contains' edge into one subgraph; "
                      "query the node you need + its edges. Never re-scan the tree. "
                      "Regenerate: python aea/tooling/build_graph.py",
        "run_the_game": "python controlroom.py  (root shim -> `python -m aea.server.controlroom`, serves :7799)",
        "path_model": "grid.py (aea/kernel/) defines ROOT (walk up to design/.git), STATE=ROOT/state, "
                      "WEB=ROOT/web; .env (keys) loads from ROOT. Runtime code lives in aea/<domain>/ "
                      "subpackages: kernel mind energy memory bench io organs loop server tooling.",
        "subgraphs": {k: {"count": len(v["nodes"]), "source": v["nodes"][0]["path"] if v["nodes"] and "path" in v["nodes"][0] else "scanned"}
                      for k, v in subgraphs.items()},
    },
    "master": {"root": "THE_PROBE", "edges": master_edges},
    "subgraphs": subgraphs,
}
json.dump(graph, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = sum(len(v["nodes"]) for v in subgraphs.values())
print(f"graph.json: master + {len(subgraphs)} subgraphs, {tot} nodes total -> {OUT}")
for k, v in subgraphs.items():
    print(f"  {k:12} {len(v['nodes']):3} nodes  {len(v['edges']):3} edges")
