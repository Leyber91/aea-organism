"""assembly.py - IS THE ORGANISM ACTUALLY ASSEMBLED? The call tree from the entry points, and the
step manifest that grows as each rung is wired.

    python -m aea.tooling.assembly            # the step manifest: what must be live, and what is
    python -m aea.tooling.assembly --tree     # the growing tree, from the wake down
    python -m aea.tooling.assembly --dead     # defined, never called from any entry point
    python -m aea.tooling.assembly --json     # state/assembly.json, every run kept

WHY THIS EXISTS AND WHY `xray` DOES NOT ALREADY DO IT. `xray` records, per module, what it imports,
what imports it, what state it touches, and `defs` - the NAMES it defines. That is an IMPORT GRAPH,
and an import graph cannot answer the question that matters here.

MEASURED: `xray` reports `aea.kernel.unstick` as `reachable_from_wake: true` and `orphaned: false`,
because `live.py` imports it and calls `propose`. Meanwhile `unstick.record`, `unstick.tried_for`
and `unstick.moves_for` have **zero callers anywhere in the tree** - they are the three functions
that constitute "stop re-choosing what the record says failed", and they are dead code inside a
module the instrument calls live. `crystal.harvest`, `applicable`, `record_use` and `carry_out` are
the same, and `state/crystal.json` is 40 bytes because of it.

**A MODULE IS WIRED WHEN SOMETHING IMPORTS IT. A CAPABILITY IS WIRED WHEN SOMETHING CALLS IT.** The
repo's actual failure mode - many modules written, few reachable - hides in that gap, and the gap is
invisible to every instrument here until this one.

WHAT THIS IS HONEST ABOUT. Python calls cannot be fully resolved statically: `getattr`, dispatch
tables, and callables passed as arguments are all real and all invisible to an AST. So the analysis
is CONSERVATIVE and says so - it resolves `mod.func()` through the module's own import bindings,
bare `func()` against local defs and `from x import func`, and it REPORTS the count it could not
resolve rather than quietly treating unresolved as absent. A function reported DEAD may be reached
dynamically; a function reported LIVE definitely has a static caller. Over-claiming the resolver
would be the same defect as every other instrument that reported cleanly about something it could
not see.

IMPORTS INSIDE FUNCTION BODIES COUNT. `live._record_outcome` does `from aea.kernel import outcomes`
inside the function, which is the idiom this repo uses to avoid import cycles in the tick. An
analyser that only read module-level imports would declare R3's entire store unreachable.
"""
from __future__ import annotations

import ast
import json
import os
import sys
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TREE = os.path.join(str(grid.ROOT), "aea")
OUT = "assembly.json"

# THE ENTRY POINTS. Everything the organism does starts at one of these; anything not reachable
# from them is not part of the running system, whatever else is true of it.
ENTRIES = {
    "wake": ["aea.loop.live:main", "aea.loop.live:tick", "aea.loop.live:choose_action",
             "aea.loop.aea:tick", "aea.loop.aea:main"],
    "server": ["aea.server.controlroom:main"],
}

# ---------------------------------------------------------------------------------------------
# THE STEP MANIFEST - THE TREE THAT GROWS. Each step declares the functions that MUST be live once
# that step is wired. A step is DONE only when every function in it has a static caller reachable
# from an entry point. This is the difference between "I committed the code" and "the organism can
# reach it", and it is checked rather than remembered.
#
# ADD A STEP WHEN YOU START IT, NOT WHEN YOU FINISH IT. A manifest that only ever contains finished
# work cannot tell you that you stopped halfway, which is the failure this file is here to prevent.
# ---------------------------------------------------------------------------------------------
STEPS = [
    ("R2  the wake's decision reaches a tool", [
        "aea.kernel.decide:choose", "aea.kernel.decide:latest", "aea.kernel.decide:parse",
        "aea.kernel.hands:invoke", "aea.kernel.hands:allowed", "aea.kernel.hands:_ledger",
    ]),
    ("R3.1 the outcome is recorded", [
        "aea.kernel.grid:append_jsonl",
        "aea.kernel.cause:classify",
        "aea.kernel.outcomes:build", "aea.kernel.outcomes:write", "aea.kernel.outcomes:require",
        "aea.loop.live:_record_outcome", "aea.loop.live:_post_for",
    ]),
    ("R3.2 it stops re-choosing what the record says fails", [
        "aea.kernel.impasse:read",
        "aea.kernel.unstick:propose",
        "aea.kernel.unstick:record",        # 0 callers as of 2026-07-31
        "aea.kernel.unstick:tried_for",     # 0 callers
        "aea.kernel.unstick:moves_for",     # 0 callers
        "aea.kernel.unstick:check_invariants",
    ]),
    ("R3.3 what works twice becomes a part, and one bad night cannot delete it", [
        "aea.kernel.crystal:harvest",       # 0 callers
        "aea.kernel.crystal:applicable",    # 0 callers
        "aea.kernel.crystal:record_use",    # 0 callers
        "aea.kernel.crystal:carry_out",     # 0 callers
    ]),
    ("R3.4 the record reaches the wake's eyes", [
        "aea.kernel.impasse:scan",          # 0 callers
        "aea.loop.aea:tick",
    ]),
]


def _modname(path: str) -> str:
    rel = os.path.relpath(path, os.path.dirname(TREE)).replace("\\", "/")
    return rel[:-3].replace("/", ".")


def _py_files():
    out = []
    for dp, dn, fns in os.walk(TREE):
        dn[:] = [d for d in dn if d not in ("__pycache__", "archive")]
        for fn in fns:
            if fn.endswith(".py") and fn != "__init__.py":
                out.append(os.path.join(dp, fn))
    return sorted(out)


class _Scope(ast.NodeVisitor):
    """Per-module: the functions it defines, and for each, the calls it makes.

    Import bindings are collected from EVERYWHERE, including inside function bodies, because the
    tick uses function-local imports to avoid cycles."""

    def __init__(self, mod: str):
        self.mod = mod
        self.alias: dict = {}          # local name -> full module path
        self.direct: dict = {}         # local name -> "mod:func"  (from x import func)
        self.defs: dict = {}           # func name -> {"line": n, "calls": set()}
        self.stack: list = []

    # --- bindings -----------------------------------------------------------------------------
    def visit_Import(self, n):
        for a in n.names:
            self.alias[a.asname or a.name.split(".")[-1]] = a.name
        self.generic_visit(n)

    def visit_ImportFrom(self, n):
        if not n.module:
            return self.generic_visit(n)
        for a in n.names:
            full = f"{n.module}.{a.name}"
            local = a.asname or a.name
            # `from aea.kernel import cause` binds a MODULE; `from x import func` binds a FUNCTION.
            # Both are common here and they resolve differently, so record both readings and let
            # the resolver prefer whichever exists.
            self.alias[local] = full
            self.direct[local] = f"{n.module}:{a.name}"
        self.generic_visit(n)

    # --- definitions --------------------------------------------------------------------------
    def _fn(self, n):
        name = ".".join([*self.stack, n.name]) if self.stack else n.name
        self.defs.setdefault(name, {"line": n.lineno, "calls": set()})
        self.stack.append(n.name)
        self.generic_visit(n)
        self.stack.pop()

    visit_FunctionDef = _fn
    visit_AsyncFunctionDef = _fn

    def visit_ClassDef(self, n):
        self.stack.append(n.name)
        self.generic_visit(n)
        self.stack.pop()

    def visit_If(self, n):
        """`if __name__ == "__main__":` IS A HUMAN AT A TERMINAL, NOT THE ORGANISM.

        Caught by tracing this tool's own first green: it reported R3.4 DONE because
        `impasse.scan` was reachable - via `impasse.render`, whose ONLY caller is
        `print(render())` inside that module's `__main__` guard. That is a person typing a
        command. The organism has never called it, `state/crystal.json` is 40 bytes, and the
        step was not done at all.

        Every module here has a CLI. Folding those blocks into the module body makes almost
        everything look reachable and turns this instrument into the thing it was built to
        replace. They go in a separate `<main>` bucket that the organism walk never enters."""
        test = n.test
        is_main = (isinstance(test, ast.Compare)
                   and isinstance(test.left, ast.Name) and test.left.id == "__name__"
                   and any(isinstance(c, ast.Constant) and c.value == "__main__"
                           for c in test.comparators))
        if not is_main:
            return self.generic_visit(n)
        self.stack.append("<main>")
        for child in n.body:
            self.visit(child)
        self.stack.pop()
        for child in n.orelse:
            self.visit(child)

    # --- calls --------------------------------------------------------------------------------
    def visit_Call(self, n):
        here = ".".join(self.stack) if self.stack else "<module>"
        slot = self.defs.setdefault(here, {"line": 0, "calls": set()})
        f = n.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            base = f.value.id
            if base in self.alias:
                slot["calls"].add(f"{self.alias[base]}:{f.attr}")
            else:
                slot["calls"].add(f"?{base}:{f.attr}")          # unresolved, and counted as such
        elif isinstance(f, ast.Name):
            if f.id in self.direct:
                slot["calls"].add(self.direct[f.id])
            else:
                slot["calls"].add(f"{self.mod}:{f.id}")          # same-module call
        self.generic_visit(n)


def scan() -> dict:
    mods = {}
    for p in _py_files():
        try:
            src = open(p, encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception:
            continue
        m = _modname(p)
        s = _Scope(m)
        s.visit(tree)
        mods[m] = dict(path=os.path.relpath(p, str(grid.ROOT)).replace("\\", "/"),
                       defs={k: {"line": v["line"], "calls": sorted(v["calls"])}
                             for k, v in s.defs.items()})
    return mods


def reachable(mods: dict, entries=None) -> tuple:
    """BFS over call edges from the entry functions. Returns (live set, unresolved count).

    A module-level call (`<module>`) is followed too: importing a module runs its body, so anything
    it calls at import time IS reachable."""
    ents = entries or [e for v in ENTRIES.values() for e in v]
    known = {f"{m}:{d}" for m, info in mods.items() for d in info["defs"]}
    live, unresolved, q = set(), 0, list(ents)
    # import-time bodies of every module an entry can reach are handled by seeding <module> nodes
    # lazily: when a call resolves into module M, M's <module> body becomes reachable too.
    while q:
        node = q.pop()
        if node in live or node not in known:
            continue
        live.add(node)
        mod, _, fn = node.partition(":")
        info = mods.get(mod)
        if not info:
            continue
        modbody = f"{mod}:<module>"
        if modbody in known and modbody not in live:
            q.append(modbody)
        for c in info["defs"].get(fn, {}).get("calls", []):
            if c.startswith("?"):
                unresolved += 1
                continue
            if c in known:
                q.append(c)
            else:
                # `from aea.kernel import cause` binds cause -> aea.kernel.cause; a call written as
                # `cause.classify()` therefore resolves to `aea.kernel.cause:classify` already. But
                # `from aea.kernel import grid` + `grid.STATE` style attribute access on a MODULE
                # imported by name needs the same treatment one level up.
                alt = c.rsplit(".", 1)
                if len(alt) == 2:
                    cand = f"{alt[0]}:{alt[1].split(':')[-1]}"
                    if cand in known:
                        q.append(cand)
    return live, unresolved


def report(mods=None) -> dict:
    mods = mods or scan()
    live, unresolved = reachable(mods)
    steps = []
    for title, need in STEPS:
        rows = [(f, f in live) for f in need]
        got = sum(1 for _f, ok in rows if ok)
        steps.append(dict(step=title, have=got, need=len(rows),
                          state=("DONE" if got == len(rows) else
                                 "PARTIAL" if got else "NOT STARTED"),
                          functions=[dict(fn=f, live=ok) for f, ok in rows]))
    allfns = {f"{m}:{d}" for m, info in mods.items() for d in info["defs"] if d != "<module>"}
    return dict(at=time.time(), at_iso=time.strftime("%Y-%m-%d %H:%M:%S"),
                modules=len(mods), functions=len(allfns), live=len(live & allfns),
                unresolved_calls=unresolved, steps=steps,
                dead=sorted(allfns - live))


def tree_lines(mods: dict, root: str, live: set, depth: int = 4, seen=None, pre="") -> list:
    """The growing tree, rendered from one entry down through real call edges."""
    seen = seen if seen is not None else set()
    out = []
    if depth <= 0 or root in seen:
        return out
    seen.add(root)
    mod, _, fn = root.partition(":")
    kids = [c for c in mods.get(mod, {}).get("defs", {}).get(fn, {}).get("calls", [])
            if not c.startswith("?") and c in live and c not in seen
            and c.split(":")[0].startswith("aea.")]
    for i, c in enumerate(sorted(kids)):
        last = i == len(kids) - 1
        out.append(f"{pre}{'`-- ' if last else '|-- '}{c}")
        out += tree_lines(mods, c, live, depth - 1, seen, pre + ("    " if last else "|   "))
    return out


if __name__ == "__main__":
    mods = scan()
    r = report(mods)
    live, _u = reachable(mods)

    if "--tree" in sys.argv[1:]:
        print("=" * 100)
        print("THE CALL TREE FROM THE WAKE - only edges that actually exist in the code")
        print("=" * 100)
        for e in ENTRIES["wake"]:
            if e.split(":")[0] in mods:
                print(f"\n{e}")
                for ln in tree_lines(mods, e, live, depth=4):
                    print("  " + ln)
        sys.exit(0)

    if "--dead" in sys.argv[1:]:
        print("=" * 100)
        print(f"DEFINED BUT NEVER CALLED FROM ANY ENTRY POINT - {len(r['dead'])} functions")
        print("=" * 100)
        print("  A static analyser cannot see getattr or dispatch tables, so treat this as a")
        print("  QUESTION LIST, not a delete list. But every R3 capability that is dead here is")
        print("  dead for real - it was written and never called.\n")
        by = {}
        for d in r["dead"]:
            by.setdefault(d.split(":")[0], []).append(d.split(":")[1])
        for m in sorted(by):
            if m.startswith("aea.kernel") or m.startswith("aea.loop"):
                print(f"  {m}")
                print(f"      {', '.join(sorted(by[m])[:14])}")
        sys.exit(0)

    if "--json" in sys.argv[1:]:
        grid.atomic_save_json(OUT, r, indent=1)
        grid.append_jsonl("assembly_history.jsonl",
                          {k: r[k] for k in ("at", "at_iso", "modules", "functions", "live",
                                             "unresolved_calls")})
        print(f"wrote {OUT} (+ appended to assembly_history.jsonl)")

    print("=" * 100)
    print("ASSEMBLY - is the organism actually wired, function by function?")
    print("=" * 100)
    print(f"  {r['modules']} modules, {r['functions']} functions, "
          f"{r['live']} reachable from an entry point")
    print(f"  {r['unresolved_calls']} calls could not be resolved statically and are NOT counted "
          f"as edges")
    print()
    for s in r["steps"]:
        mark = {"DONE": "DONE      ", "PARTIAL": "PARTIAL   ", "NOT STARTED": "NOT STARTED"}[s["state"]]
        print(f"  {mark} {s['have']}/{s['need']}  {s['step']}")
        for f in s["functions"]:
            if not f["live"]:
                print(f"                    DEAD  {f['fn']}")
    print()
    bad = [s for s in r["steps"] if s["state"] != "DONE"]
    print("  A step is DONE only when every function in it has a caller reachable from an entry.")
    print("  " + ("EVERY DECLARED STEP IS WIRED." if not bad else
                  f"{len(bad)} step(s) not fully wired - the organism cannot do what they claim."))
