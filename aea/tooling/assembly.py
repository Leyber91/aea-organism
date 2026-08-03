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
        self.defs: dict = {}           # func name -> {"line": n, "calls": set(), "dcalls": set()}
        self.stack: list = []
        self.tables: dict = {}         # module-level container name -> {"mod:func", ...}
        self.derived: dict = {}        # local name -> the table it was taken out of
        self.n_calls = 0               # EVERY Call node seen - the honest denominator
        self.n_unhandled = 0           # ...of which this resolver has no branch for at all
        self.n_methods = 0             # defs nested inside a ClassDef: a stated blind spot
        self.localdefs = set()         # every QUALIFIED def name, prepassed - see visit_Call
        self.in_class = 0

    def _rel(self, module, level) -> str:
        """`from . import x` and `from .kernel import grid` resolved against THIS module's package.

        Both forms were dropped: `prepare` required `n.module` and `visit_ImportFrom` returned early
        without it, so a relative import bound nothing and every call through it resolved to a key
        that exists nowhere in the tree. This repo writes absolute imports by convention, so the
        defect is latent rather than active - which is exactly the kind that survives, because
        nothing fails until the day someone writes the idiom Python has always allowed."""
        if not level:
            return module or ""
        parts = self.mod.split(".")
        base = parts[:max(0, len(parts) - level)]
        return ".".join(base + ([module] if module else []))

    # --- dispatch tables ----------------------------------------------------------------------
    # THE EDGE THAT WAS NEVER DRAWN. `visit_Call` records call SITES, and a dispatch table holds a
    # function REFERENCE - `TOOLS = {"calc": dict(impl=_calc, ...)}` - so `_calc` had no caller
    # anywhere in the graph and was reported dead. It runs 68 times in the ledger. Measured across
    # the tree: 83 functions in 27 module-level containers, every one of them a false orphan,
    # including `selfcheck.CHECKS` (9), `transfer.DETECTORS` (6) and `ladder.MEASURE` (5) - the
    # instruments this repo verifies itself with were themselves reported as dead code.
    #
    # WHAT IS AND IS NOT AN EDGE, because the loose version of this is a rubber stamp. Holding a
    # reference is not calling it. `hands.schema` READS TOOLS to build a prompt and must not make
    # nine implementations reachable. The edge is drawn only where a call is made on something
    # taken OUT of the container - `TOOLS[k](...)`, `t["impl"](**kw)` after `t = TOOLS.get(name)`,
    # or `fn(...)` inside `for fn in DETECTORS`. `TOOLS.get(...)` and `TOOLS.items()` are lookups
    # and draw nothing.
    #
    # It is still an OVER-APPROXIMATION and it is labelled as one: which entry a dispatch selects
    # is a runtime fact, so reaching the table means every entry is reachable THROUGH it. That is
    # an upper bound, `reachable(detail=True)` separates it from the direct set, and the page draws
    # the difference rather than absorbing it.
    _CONTAINER_METHODS = {"get", "items", "keys", "values", "append", "extend", "pop", "index",
                          "setdefault", "update", "copy", "count", "sort", "insert", "remove",
                          "add", "discard", "join", "format", "split", "strip"}

    def prepare(self, tree):
        """Bindings and containers FIRST, in one pre-pass. A table is routinely defined below the
        function that dispatches through it (`hands.TOOLS` is 300 lines above `invoke` and
        `selfcheck.CHECKS` is below every check it holds), and a visitor in source order would see
        half of them. Reading the whole module before answering is the difference.

        THE SAME ARGUMENT APPLIES TO NESTED DEFS, and that is why they are prepassed here too: a
        nested function may be defined BELOW the call that uses it, and a bare name must resolve
        against the enclosing scopes innermost-out, exactly as Python resolves it. Without this,
        every call to a nested function produced an edge to a key that does not exist."""
        def _walk_defs(node, path):
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    q = path + [ch.name]
                    self.localdefs.add(".".join(q))
                    _walk_defs(ch, q)
                elif isinstance(ch, ast.ClassDef):
                    _walk_defs(ch, path + [ch.name])
                else:
                    _walk_defs(ch, path)
        _walk_defs(tree, [])

        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    self.alias[a.asname or a.name.split(".")[-1]] = a.name
            elif isinstance(n, ast.ImportFrom):
                mod = self._rel(n.module, n.level)
                if not mod:
                    continue
                for a in n.names:
                    self.alias[a.asname or a.name] = f"{mod}.{a.name}"
                    self.direct[a.asname or a.name] = f"{mod}:{a.name}"
        top = {n.name for n in tree.body
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                targets, value = node.targets, node.value
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value = [node.target], node.value
            else:
                continue
            names = [t.id for t in targets if isinstance(t, ast.Name)]
            if not names:
                continue
            entries = set()
            for sub in ast.walk(value):
                if isinstance(sub, ast.Name) and sub.id in top:
                    entries.add(f"{self.mod}:{sub.id}")
                elif isinstance(sub, ast.Name) and sub.id in self.direct:
                    entries.add(self.direct[sub.id])
                elif (isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name)
                      and sub.value.id in self.alias):
                    entries.add(f"{self.alias[sub.value.id]}:{sub.attr}")
            if entries:
                self.tables[names[0]] = entries

    def _table_root(self, node):
        """The container a value was taken out of, following subscripts, attributes and calls."""
        cur, hops = node, 0
        while hops < 12:
            hops += 1
            if isinstance(cur, ast.Subscript):
                cur = cur.value
            elif isinstance(cur, ast.Attribute):
                cur = cur.value
            elif isinstance(cur, ast.Call):
                cur = cur.func
            else:
                break
        if isinstance(cur, ast.Name):
            if cur.id in self.tables:
                return cur.id
            return self.derived.get(cur.id)
        return None

    def _dispatch_table(self, f):
        """The table whose entries this call could be invoking, or None if it is a lookup."""
        if isinstance(f, ast.Subscript):
            return self._table_root(f)
        if isinstance(f, ast.Name):
            return self.derived.get(f.id)
        if isinstance(f, ast.Attribute):
            if f.attr in self._CONTAINER_METHODS:
                return None
            if isinstance(f.value, ast.Name):
                return self.derived.get(f.value.id)
            if isinstance(f.value, ast.Subscript):
                return self._table_root(f.value)
        return None

    def _bind(self, target, table):
        if isinstance(target, ast.Name):
            self.derived[target.id] = table
        elif isinstance(target, (ast.Tuple, ast.List)):
            for e in target.elts:
                self._bind(e, table)

    def visit_Assign(self, n):
        t = self._table_root(n.value)
        if t:
            for tgt in n.targets:
                self._bind(tgt, t)
        self.generic_visit(n)

    def visit_For(self, n):
        t = self._table_root(n.iter)
        if t:
            self._bind(n.target, t)
        self.generic_visit(n)

    # --- bindings -----------------------------------------------------------------------------
    def visit_Import(self, n):
        for a in n.names:
            self.alias[a.asname or a.name.split(".")[-1]] = a.name
        self.generic_visit(n)

    def visit_ImportFrom(self, n):
        mod = self._rel(n.module, n.level)
        if not mod:
            return self.generic_visit(n)
        for a in n.names:
            full = f"{mod}.{a.name}"
            local = a.asname or a.name
            # `from aea.kernel import cause` binds a MODULE; `from x import func` binds a FUNCTION.
            # Both are common here and they resolve differently, so record both readings and let
            # the resolver prefer whichever exists.
            self.alias[local] = full
            self.direct[local] = f"{mod}:{a.name}"
        self.generic_visit(n)

    # --- definitions --------------------------------------------------------------------------
    def _fn(self, n):
        name = ".".join([*self.stack, n.name]) if self.stack else n.name
        if self.in_class:
            # A STATED BLIND SPOT, COUNTED RATHER THAN FABRICATED. `visit_Call` resolves a bare name
            # and an attribute-on-an-imported-module. It resolves NO method call, because the type of
            # a receiver is a runtime fact - so every method in the tree reads NONE, including the
            # handler methods that ARE `controlroom:main`. The honest move is to publish the number
            # and the limitation; inventing an edge from "exactly one class defines this name" would
            # be a guess dressed as a graph, which is the failure this whole file is written against.
            self.n_methods += 1
        self.defs.setdefault(name, {"line": n.lineno, "calls": set(), "dcalls": set()})
        self.stack.append(n.name)
        # `derived` IS A FUNCTION-LOCAL FACT AND WAS KEPT PER-MODULE.
        #
        # `visit_Assign` records "this local name came out of that table", and the binding then
        # LEAKED FORWARD into every later function that happened to reuse the name. So a DISPATCH
        # label could rest on nothing but a naming coincidence between two unrelated functions -
        # the resolver had no evidence for the edge, it had a collision. Confirmed by construction
        # 2026-08-03; on the real tree it removes 2 DISPATCH labels and 10 dispatch edges, and both
        # removals are honest: the resolver cannot follow a table value through a return, so it
        # never had grounds for them.
        _derived_outer = dict(self.derived)
        self.generic_visit(n)
        self.derived = _derived_outer
        self.stack.pop()

    visit_FunctionDef = _fn
    visit_AsyncFunctionDef = _fn

    def visit_Lambda(self, n):
        """A LAMBDA BODY IS ITS OWN SCOPE, AND WAS CREDITED TO THE SCOPE THAT DEFINED IT.

        Confirmed by construction 2026-08-03. A module-level table of lambdas - `IMPL = {"calc":
        lambda a: calc(a)}` - had every lambda body attributed to `<module>`, so the calls inside
        them became MODULE-LEVEL calls. A module body is followed by `reachable` (importing runs
        it), so every function reachable only through the table was promoted to EXTRACTED.

        That collapses DISPATCH into EXTRACTED - an UPPER BOUND printed as a fact - which is the one
        thing this module's own docstring says may never happen: "nothing in this repo may print the
        union as though it were the direct set". The lambda body now lands in its own frame, so its
        calls belong to the lambda and not to whoever wrote it down."""
        self.stack.append("<lambda@%d>" % getattr(n, "lineno", 0))
        self.generic_visit(n)
        self.stack.pop()

    def visit_ClassDef(self, n):
        self.stack.append(n.name)
        self.in_class += 1
        self.generic_visit(n)
        self.in_class -= 1
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
        slot = self.defs.setdefault(here, {"line": 0, "calls": set(), "dcalls": set()})
        f = n.func
        self.n_calls += 1
        tbl = self._dispatch_table(f)
        if tbl:
            slot.setdefault("dcalls", set()).update(self.tables.get(tbl) or ())
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            base = f.value.id
            if base in self.alias:
                slot["calls"].add(f"{self.alias[base]}:{f.attr}")
            else:
                slot["calls"].add(f"?{base}:{f.attr}")          # unresolved, and counted as such
        elif isinstance(f, ast.Name):
            # A BARE NAME IS RESOLVED AGAINST THE ENCLOSING SCOPES FIRST, INNERMOST OUT.
            #
            # THE DEFECT THIS CLOSES, confirmed by construction and then measured on the real tree:
            # `_fn` keys a nested def as "outer.inner", and this branch wrote the bare call as
            # "module:inner". THE TWO KEYSPACES NEVER MET. So every call to a nested function
            # produced an edge to a name that does not exist, silently - not counted as unresolved
            # either, because it took this branch rather than the `?` one.
            #
            # Consequence: all 111 nested defs in the tree read NONE, the label documented as
            # "nothing reaches it by any route", and 19 top-level functions were false-dead through
            # the same mechanism. About 23% of the published dead list was a resolver artifact.
            #
            # Python resolves a bare name innermost-out, so this does too - `self.localdefs` was
            # prepassed for exactly this reason, since a nested def may be defined BELOW the call
            # that uses it.
            local = None
            for k in range(len(self.stack), 0, -1):
                cand = ".".join(self.stack[:k] + [f.id])
                if cand in self.localdefs:
                    local = cand
                    break
            if local:
                slot["calls"].add(f"{self.mod}:{local}")
            elif f.id in self.direct:
                slot["calls"].add(self.direct[f.id])
            else:
                slot["calls"].add(f"{self.mod}:{f.id}")          # same-module call
        else:
            # THE THIRD CASE, WHICH FELL THROUGH SILENTLY. `obj.attr.method()`, `f()()`,
            # `things[i].run()`, a lambda call - every form whose func is neither a bare Name nor an
            # Attribute-on-a-Name hit NEITHER branch and recorded nothing at all: no edge AND no `?`.
            # Measured at 2,825 sites, 14.3% of every Call node in the tree, and the published
            # `unresolved_share` was computed over the `?` set, so it excluded all of them. The
            # module's honest claim - "it REPORTS the count it could not resolve rather than quietly
            # treating unresolved as absent" - was true of one blind spot and false of the larger one.
            self.n_unhandled += 1
            slot["calls"].add(f"?<{type(f).__name__}>")
        self.generic_visit(n)


def scan(report: bool = False):
    """Every module, parsed. A file that CANNOT be parsed is reported, never dropped.

    THE DEFECT THIS CLOSES, confirmed by construction 2026-08-03: the old `except Exception:
    continue` deleted an unreadable module from the analysis entirely - and every function it called
    then read NONE, the label documented as "nothing reaches it by any route". So NONE meant two
    different things, "measured, nothing reaches it" and "never measured", and a reader could not
    tell them apart. In a tool that sits in the boot chain, that is the whole defect class this repo
    is built against.

    Failures are collected under the `__scan__` key rather than raised, because one broken file in
    `archive/` must not take down the graph - but the count travels with every consumer, and
    `report()` prints it above the evidence table."""
    mods, skipped = {}, []
    for p in _py_files():
        rel = os.path.relpath(p, str(grid.ROOT)).replace("\\", "/")
        try:
            src = open(p, encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception as e:
            skipped.append(dict(path=rel, error="%s: %s" % (type(e).__name__, str(e)[:90])))
            continue
        m = _modname(p)
        s = _Scope(m)
        s.prepare(tree)
        s.visit(tree)
        mods[m] = dict(path=os.path.relpath(p, str(grid.ROOT)).replace("\\", "/"),
                       calls_seen=s.n_calls, calls_unhandled=s.n_unhandled, methods=s.n_methods,
                       tables={k: sorted(v) for k, v in s.tables.items()},
                       defs={k: {"line": v["line"], "calls": sorted(v["calls"]),
                                 "dcalls": sorted(v.get("dcalls") or ())}
                             for k, v in s.defs.items()})
    # A SCAN THAT FINDS NOTHING AGREES WITH EVERYTHING, and it must never do so quietly. Two guards
    # in this repo walked `aea/aea/` - one dirname too deep - and reported ok having read an empty
    # tree; the caller count came back 0 and the import scan passed, both vacuously. That failure
    # is one wrong join away from every consumer of this function, all of which read "0 orphans,
    # everything reachable" as good news.
    if not mods:
        raise RuntimeError("assembly.scan found no modules under %s - this is a broken scan, "
                           "not an empty tree" % TREE)
    # WHAT WAS READ AND WHAT WAS NOT, recorded BESIDE the result rather than inside it.
    #
    # The obvious move - a reserved key in `mods` - would have been a defect of its own: every
    # consumer iterates this dict and `reachable` does `info["defs"]` unguarded, so a sentinel entry
    # raises KeyError. Caught before writing it, by asking what iterates the thing rather than by
    # running it.
    return (mods, dict(files_seen=len(_py_files()), files_parsed=len(mods),
                       skipped=skipped)) if report else mods


def reachable(mods: dict, entries=None, detail: bool = False, dispatch: bool = True) -> tuple:
    """BFS over call edges from the entry functions. Returns (live set, unresolved count).

    A module-level call (`<module>`) is followed too: importing a module runs its body, so anything
    it calls at import time IS reachable.

    DISPATCH EDGES ARE FOLLOWED BY DEFAULT AND ARE SEPARABLE ON REQUEST. A function invoked out of
    a module-level table has no call site to find, so before this it was reported dead while
    running - `hands._read_state` has 68 invocations in the ledger. Following the edge is correct
    and it is also weaker evidence than a direct call, because which entry a dispatch selects is a
    runtime fact. `detail=True` returns a third element separating the two, and nothing in this
    repo may print the union as though it were the direct set:

        live, unresolved, via = reachable(mods, detail=True)
        via["direct"]     reached by call edges alone
        via["dispatch"]   reached ONLY through a table, i.e. an upper bound

    `dispatch=False` gives the old, strictly-direct answer for anything that needs the floor."""
    if detail:
        direct, unres = reachable(mods, entries, dispatch=False)
        allset, _u = reachable(mods, entries, dispatch=True)
        return allset, unres, dict(direct=direct, dispatch=allset - direct)
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
        slot = info["defs"].get(fn, {})
        edges = list(slot.get("calls", []))
        if dispatch:
            edges += list(slot.get("dcalls", []))
        for c in edges:
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


# =================================================================================================
# WHAT KIND OF EVIDENCE REACHES THIS FUNCTION. The distinction this module always computed and never
# handed anybody in a usable form.
#
# `reachable(detail=True)` has separated direct from dispatch since it was written, and this file's
# own docstring says nothing here may print the union as though it were the direct set. Then
# `report()` did exactly that, and so did five other call sites, because the split was available
# only as a tuple element that every caller dropped. A distinction nobody can reach is not a
# distinction; it is a comment.
#
# MEASURED at the time this was added: 6,470 call edges, 120 dispatch edges, and 2,699 call sites
# the resolver could not resolve at all - 29% of every call in the tree is invisible to it. A
# consumer reading `live` as fact is reading an upper bound built on top of a 71% view.
#
# THE FOUR KINDS, and the fourth is the one that changes an answer:
#
#   EXTRACTED  a call site exists in the source and its target is unambiguous. The organism reaches
#              this. The only kind that is a fact rather than a resolution
#   DISPATCH   reachable only by following a module-level container something calls THROUGH. An
#              upper bound BY CONSTRUCTION - which entry a dispatch selects is a runtime fact - so
#              it is honest evidence of "could be reached", never of "is reached". Where a receipt
#              exists (`hands._read_state` has 62 ledger invocations) the receipt is the stronger
#              claim and the static graph simply cannot see it
#   TOOL       reachable only from a `__main__` guard: A HUMAN AT A TERMINAL, not the organism. This
#              is a legitimate and necessary kind - `perceive.verdict` is a READER, and demanding
#              the wake call it would push an instrument into the tick to satisfy a checker. It is
#              also the exact disguise `impasse.scan` wore when this tool first reported R3.4 DONE
#   ENTRY      IT IS WHERE THE WALK STARTS. Its reachability is an ASSUMPTION, not a measurement,
#              and the first version of this labelling got that wrong. `reachable()` seeds the entry
#              set straight into `live`, and the only test before `live.add` is that the function
#              is DEFINED - so an entry was stamped EXTRACTED whether or not one line of code called
#              it. Proved by construction: deleting all three call sites of `aea.loop.aea:tick`
#              left STEPS R3.4 reading DONE with both functions EXTRACTED, while the control
#              (`impasse:scan`, same step, not an entry) correctly flipped to PARTIAL/NONE. Five
#              declared names across STEPS and RUNG_FUNCS are entries, so for those the wiring
#              check was unfalsifiable. Three entries - `live:main`, `aea:main`,
#              `controlroom:main` - have ZERO callers anywhere but their own `<main>` guard
#   NONE       nothing anywhere reaches it, by any route
#
# Naming TOOL separately is what stops the two opposite errors: counting a human-typed command as
# organism capability, and calling a working instrument dead because the wake does not read it.
# Naming ENTRY separately is what stops a check from grading its own axiom.
# =================================================================================================
EVIDENCE = ("EXTRACTED", "DISPATCH", "ENTRY", "TOOL", "NONE")

# WHAT THE LAST scan() READ, AND WHAT IT COULD NOT. Set by scan(), read by report() and the census.
# NONE must never mean two different things - "measured, and nothing reaches it" versus "never
# measured at all" - and before this existed it meant both, because an unparseable module was
# dropped in silence and every function it called then read NONE.
# NO MODULE-LEVEL SCAN RECORD, AND THE RATCHET IS WHY.
#
# The first version stashed it in a global that scan() rebound - `global-write 7 -> 8`, caught the
# minute it shipped. A global mutated by a function is shared state between every caller, and the
# obvious dodge (clear-and-update in place, so the `global` keyword disappears) would game the
# detector without changing the fact. So the record is RETURNED: `scan(report=True)` gives
# (mods, {files_seen, files_parsed, skipped}), and plain `scan()` is unchanged for every existing
# caller.


def tool_entries(mods: dict) -> list:
    """Every `__main__` bucket - the CLI surface. `visit_If` files those calls under `<main>`, so
    they are already segregated from the organism walk; this is the entry set that walks them ON
    PURPOSE, to tell "a person can run it" apart from "nothing reaches it"."""
    return sorted("%s:<main>" % m for m, info in mods.items() if "<main>" in (info.get("defs") or {}))


def incoming(mods: dict, only_from=None) -> dict:
    """target -> how many REAL call sites point at it, excluding `<main>` buckets and self-calls.

    This is what makes ENTRY honest rather than merely separate: an entry with callers and an entry
    with none are different situations, and collapsing them would trade one blind spot for another.
    `<main>` is excluded because a person typing the command is the very thing `visit_If` segregates.
    """
    n = {}
    for m, info in mods.items():
        for d, slot in (info.get("defs") or {}).items():
            if d == "<main>" or d.startswith("<main>."):
                continue
            here = "%s:%s" % (m, d)
            # only_from RESTRICTS THE WITNESSES. Without it this counted call sites inside
            # functions the same run grades TOOL or NONE, so dead code could vouch for an entry and
            # promote it out of ENTRY into EXTRACTED. A caller that nothing reaches is not evidence
            # that its callee is reached.
            if only_from is not None and here not in only_from:
                continue
            for c in list(slot.get("calls", [])) + list(slot.get("dcalls") or ()):
                if c.startswith("?") or c == here:
                    continue
                n[c] = n.get(c, 0) + 1
    return n


def provenance(mods: dict = None, entries=None) -> dict:
    """{function -> one of EVIDENCE} for every function defined in the tree.

    Kinds are assigned STRONGEST FIRST, so a function reachable both directly and through a table
    reads EXTRACTED. Precedence is the point: the label answers "what is the best evidence for
    this", and a weaker route never weakens a fact.

    ENTRY OUTRANKS EVERYTHING, because it is not evidence at all - it is the axiom the walk begins
    from. A check that grades a name it also assumed is not a check, and that is exactly what this
    function did until an audit deleted every caller of an entry and watched the row stay green."""
    mods = mods or scan()
    # ENTRY MEANS ASSERTED **AND** UNMEASURED. An entry with real call sites is not a tautology -
    # `loop.aea:tick` has three callers, and demoting it would trade a false pass for a false fail.
    # The tautology is only ever an entry that NOTHING calls, where the seed IS the whole evidence.
    # This is also what restores falsifiability: strip tick's three callers and `incoming` drops to
    # zero, so it becomes ENTRY and its STEPS row flips to PARTIAL - the exact behaviour the audit
    # proved was impossible before.
    #
    # AND THE CALLER MUST ITSELF BE PART OF THE ORGANISM, which the first version did not require.
    #
    # Confirmed by construction 2026-08-03: `incoming()` counted EVERY call site, including ones
    # inside functions this same run grades TOOL or NONE. So an entry could be promoted out of ENTRY
    # - out of "asserted and unmeasured" and into "a fact" - by a caller the tool itself says nothing
    # reaches. The falsifiability fix had a hole exactly the width of its own dead code.
    #
    # Resolved in two passes rather than by circular reasoning: seed EVERY entry, compute what is
    # reachable from that, and only then count callers whose OWNING function survived that pass. One
    # pass is enough here - a caller that is itself only reachable through the entry it vouches for
    # is not independent evidence, and this drops that case.
    all_ents = list(entries or [x for v in ENTRIES.values() for x in v])
    seeded, _u0 = reachable(mods, all_ents, dispatch=True)
    inc = incoming(mods, only_from=seeded - set(all_ents))
    ents = {e for e in all_ents if not inc.get(e)}
    direct, _u = reachable(mods, entries, dispatch=False)
    union, _u2 = reachable(mods, entries, dispatch=True)
    viacli, _u3 = reachable(mods, entries=tool_entries(mods), dispatch=True)
    out = {}
    for m, info in mods.items():
        for d in (info.get("defs") or {}):
            # A LAMBDA FRAME IS A SCOPE MARKER, NOT A FUNCTION ANYONE CAN CALL, so it is excluded
            # exactly as <module> and <main> are. Giving lambdas their own scope added 114 frames
            # and every one read NONE, inflating the dead list by 124 - a fix creating the very
            # artifact it was removing. Counted as functions, they would also be uncallable by
            # construction, which is not the same fact as unreached code.
            if d == "<module>" or d.startswith("<main>") or "<lambda@" in d:
                continue
            f = "%s:%s" % (m, d)
            out[f] = ("ENTRY" if f in ents else
                      "EXTRACTED" if f in direct else
                      "DISPATCH" if f in union else
                      "TOOL" if f in viacli else "NONE")
    return out


def evidence_census(mods: dict = None) -> dict:
    """The counts, plus the resolver's own blindness. Both belong to any claim built on this graph.

    `unresolved_share` is reported because it bounds every other number here: a graph that cannot
    see 29% of the call sites cannot honestly present "dead" as "never called". It is the difference
    between a measurement and an assertion, and it was not on the page."""
    mods = mods or scan()
    prov = provenance(mods)
    counts = {k: 0 for k in EVIDENCE}
    for v in prov.values():
        counts[v] = counts.get(v, 0) + 1
    n_call = n_disp = n_unres = 0
    for _m, info in mods.items():
        for _d, slot in (info.get("defs") or {}).items():
            for c in slot.get("calls", []):
                if c.startswith("?"):
                    n_unres += 1
                else:
                    n_call += 1
            n_disp += len(slot.get("dcalls") or ())
    # THE DENOMINATOR IS CALL SITES, NOT DEDUPLICATED EDGES. Counting `?` entries in an edge SET
    # under-reports twice: identical unresolved forms in one function collapse to one entry, and
    # until the terminal `else` above existed, 2,825 sites produced no entry at all. `calls_seen` is
    # every ast.Call node the visitor walked, which is the quantity the share claims to be about.
    seen = sum(int(i.get("calls_seen") or 0) for i in mods.values())
    unhandled = sum(int(i.get("calls_unhandled") or 0) for i in mods.values())
    methods = sum(int(i.get("methods") or 0) for i in mods.values())
    return dict(functions=len(prov), by_evidence=counts,
                call_edges=n_call, dispatch_edges=n_disp, unresolved_edges=n_unres,
                call_sites=seen, unhandled_sites=unhandled, method_defs=methods,
                unresolved_share=(round(100.0 * unhandled / seen, 1) if seen else None),
                note="unresolved_share is the fraction of ast.Call SITES this resolver has no "
                     "branch for at all. It bounds every other number here, and two further blind "
                     "spots are not in it: %d method definitions (a receiver's type is a runtime "
                     "fact, so no method call resolves - every method reads NONE, including the "
                     "handlers that ARE the server entry), and getattr/callables-passed-as-"
                     "arguments. DEAD means 'no static caller found', never 'never runs'."
                     % methods)


def report(mods=None) -> dict:
    mods = mods or scan()
    live, unresolved = reachable(mods)
    # EVERY STEP FUNCTION NOW CARRIES THE KIND OF EVIDENCE THAT REACHES IT, not a boolean. A step
    # reported DONE on three dispatch edges and a step reported DONE on three call sites are not the
    # same claim, and until now they printed identically.
    prov = provenance(mods)
    steps = []
    for title, need in STEPS:
        rows = [(f, prov.get(f, "NONE")) for f in need]
        got = sum(1 for _f, k in rows if k in ("EXTRACTED", "DISPATCH"))
        firm = sum(1 for _f, k in rows if k == "EXTRACTED")
        steps.append(dict(step=title, have=got, need=len(rows), extracted=firm,
                          state=("DONE" if got == len(rows) else
                                 "PARTIAL" if got else "NOT STARTED"),
                          upper_bound=bool(got == len(rows) and firm < len(rows)),
                          functions=[dict(fn=f, live=k in ("EXTRACTED", "DISPATCH"), evidence=k)
                                     for f, k in rows]))
    allfns = {f"{m}:{d}" for m, info in mods.items() for d in info["defs"] if d != "<module>"}
    cen = evidence_census(mods)
    return dict(at=time.time(), at_iso=time.strftime("%Y-%m-%d %H:%M:%S"),
                modules=len(mods), functions=len(allfns), live=len(live & allfns),
                unresolved_calls=unresolved, steps=steps,
                evidence=cen["by_evidence"], census=cen,
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
    c = r["census"]
    e = r["evidence"]
    print(f"  {r['modules']} modules, {r['functions']} functions")
    print()
    inc = incoming(mods)
    print("  BY WHAT KIND OF EVIDENCE - the union was printed as the direct set for months")
    print(f"    EXTRACTED  {e['EXTRACTED']:5d}   a call site exists in the source. A fact")
    print(f"    DISPATCH   {e['DISPATCH']:5d}   only through a table. An UPPER BOUND by construction")
    print(f"    ENTRY      {e['ENTRY']:5d}   where the walk STARTS. An assumption, never a measurement")
    print(f"    TOOL       {e['TOOL']:5d}   only from a __main__ guard. A human at a terminal")
    print(f"    NONE       {e['NONE']:5d}   nothing reaches it by any route")
    print()
    print("  THE ENTRIES, and how many real callers each actually has:")
    for en in sorted(set(x for v in ENTRIES.values() for x in v)):
        print(f"    {inc.get(en, 0):3d}  {en}" + ("   <- asserted only" if not inc.get(en) else ""))
    print()
    print(f"  {c['call_sites']} call sites walked; {c['call_edges']} edges drawn, "
          f"{c['dispatch_edges']} dispatch edges, {c['unhandled_sites']} sites this resolver has")
    print(f"  no branch for at all ({c['unresolved_share']}%).")
    print(f"  Two further blind spots are NOT in that share: {c['method_defs']} method definitions")
    print("  (no method call resolves - a receiver's type is a runtime fact) and getattr. DEAD")
    print("  means 'no static caller found', never 'never runs'.")
    print()
    for s in r["steps"]:
        mark = {"DONE": "DONE      ", "PARTIAL": "PARTIAL   ", "NOT STARTED": "NOT STARTED"}[s["state"]]
        bound = "  (UPPER BOUND - not every function has a call site)" if s["upper_bound"] else ""
        print(f"  {mark} {s['have']}/{s['need']}  {s['step']}{bound}")
        for f in s["functions"]:
            if f["evidence"] != "EXTRACTED":
                print(f"                    {f['evidence']:<10s} {f['fn']}")
    print()
    bad = [s for s in r["steps"] if s["state"] != "DONE"]
    print("  A step is DONE only when every function in it has a caller reachable from an entry.")
    print("  " + ("EVERY DECLARED STEP IS WIRED." if not bad else
                  f"{len(bad)} step(s) not fully wired - the organism cannot do what they claim."))
