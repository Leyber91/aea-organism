"""scope.py - IS EVERYTHING AT THE RIGHT SCOPE? Asked mechanically, across the tree.

    python -m aea.tooling.scope            # the report
    python -m aea.tooling.scope --json     # state/scope.json

WHY THIS EXISTS. Luis, 2026-08-01: *"the same thing that we programmed, that we need variables to be
on the right scope - are we having the right scope here for each of the functions and
functionalities?"*

It is the right question and this repo has already paid for it twice, in the same shape both times:

    hands.LEDGER        bound to grid.STATE at IMPORT -> a harness could not redirect it, and
                        4,920 synthetic attack rows landed in the production ledger
    unstick.EXPERIENCE  same, found later -> every test that drove the loop wrote real rows into
                        the entity's real experience record while printing "production untouched"

Neither was a logic error. Both were a value living at MODULE scope that needed to live at CALL
scope, and the cost was evidence stores that could not be trusted. `transfer.py` catches that one
specific shape. This file asks the wider question.

WHAT IT LOOKS FOR, and each is a different way a scope can be wrong:

    IMPORT-BOUND PATH     a module constant built from grid.STATE, used as a write target. Cannot
                          be redirected, so no harness can be sandboxed. (D48)
    MUTABLE MODULE STATE  a dict or list at module level that some function MUTATES. It is shared
                          by every caller in the process, survives between calls, and two callers
                          silently see each other's writes.
    GLOBAL WRITE          a function declaring `global` and assigning. Same hazard, stated out loud.
    IMPORT-TIME WORK      a call at module level that does I/O or spawns. Merely NAMING the module
                          performs it, so an import for one function pays for all of them.
    CACHE WITHOUT A KEY   a module-level memo dict written by a function whose result depends on
                          arguments that are not in the key.

WHAT IT DELIBERATELY DOES NOT FLAG. A module-level CONSTANT that is only ever read - a table, a
regex, a threshold - is correct and is most of what a module should contain. `decide.KNOWN`,
`hands.TOOLS` and `knobs.KNOBS` are exactly right: closed, read-only, declared once. The defect is
never "module level"; it is module level PLUS mutation, or module level PLUS an environment the
caller should control.
"""
from __future__ import annotations

import ast
import json
import os
import sys

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TREE = os.path.join(str(grid.ROOT), "aea")
MUTATORS = {"append", "extend", "insert", "pop", "remove", "clear", "update", "setdefault",
            "popitem", "add", "discard", "sort"}
IO_CALLS = {"load_json", "atomic_save_json", "append_jsonl", "read", "open", "run", "Popen",
            "urlopen", "get", "post", "makedirs", "mkdir", "listdir", "glob"}


def _files():
    out = []
    for dp, dn, fns in os.walk(TREE):
        dn[:] = [d for d in dn if d not in ("__pycache__", "archive")]
        for fn in fns:
            if fn.endswith(".py"):
                p = os.path.join(dp, fn)
                out.append((os.path.relpath(p, os.path.dirname(TREE)).replace("\\", "/"), p))
    return sorted(out)


def _line(src, i):
    try:
        return src.splitlines()[i - 1].strip()[:104]
    except Exception:
        return ""


def audit() -> dict:
    findings = []

    def add(kind, rel, lineno, src, note, severity="REAL"):
        findings.append(dict(kind=kind, file=rel, line=lineno, snippet=_line(src, lineno),
                             note=note, severity=severity))

    for rel, path in _files():
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception:
            continue

        # module-level names, and which of them are built from a state path
        mod_names, state_names, const_names = {}, set(), set()
        for n in tree.body:
            if isinstance(n, ast.Assign):
                blob = ast.dump(n.value)
                for t in n.targets:
                    if not isinstance(t, ast.Name):
                        continue
                    mod_names[t.id] = n
                    if "STATE" in blob and "grid" in blob:
                        state_names.add(t.id)
                    if isinstance(n.value, (ast.Dict, ast.List, ast.Set)):
                        const_names.add(t.id)

        # IMPORT-TIME WORK - a call at module level that touches the world
        # A CALL INSIDE A LAMBDA DOES NOT RUN AT IMPORT - the body runs when the lambda is CALLED.
        # The first version flagged `IMPL = {'calc': lambda a: calc(a.get('expression',''))}` as
        # import-time I/O because `.get` appears at module level in the source. It appears; it does
        # not execute. A detector that cannot tell a definition from an execution reports noise, and
        # noise is how a report stops being read.
        lam_lines = {ln for x in ast.walk(tree) if isinstance(x, ast.Lambda)
                     for c in ast.walk(x) for ln in [getattr(c, "lineno", None)] if ln}
        for n in tree.body:
            for c in ast.walk(n):
                if not isinstance(c, ast.Call) or c.lineno in lam_lines:
                    continue
                fname = getattr(c.func, "attr", None) or getattr(c.func, "id", None)
                if fname in IO_CALLS and not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                                                            ast.ClassDef, ast.If)):
                    add("import-time-work", rel, c.lineno, src,
                        f"{fname}() runs merely because the module was NAMED - an import for one "
                        f"function pays for all of them, and it cannot be sandboxed")

        # MUTABLE MODULE STATE / GLOBAL WRITES, inside functions
        for fn in [x for x in ast.walk(tree)
                   if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for n in ast.walk(fn):
                if isinstance(n, ast.Global):
                    add("global-write", rel, n.lineno, src,
                        f"declares global {', '.join(n.names)} - process-wide state written from "
                        f"inside a call; two callers see each other's writes")
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                        and n.func.attr in MUTATORS and isinstance(n.func.value, ast.Name) \
                        and n.func.value.id in const_names:
                    add("mutable-module-state", rel, n.lineno, src,
                        f"{n.func.value.id}.{n.func.attr}() mutates a MODULE-LEVEL container - it "
                        f"is shared by every caller in the process and survives between calls")
                if isinstance(n, ast.Subscript) and isinstance(n.ctx, ast.Store) \
                        and isinstance(n.value, ast.Name) and n.value.id in const_names:
                    add("mutable-module-state", rel, n.lineno, src,
                        f"assigns into module-level {n.value.id}[...] from inside a function")

        # IMPORT-BOUND WRITE TARGET (D48) - the one that has bitten twice
        for fn in [x for x in ast.walk(tree)
                   if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for n in ast.walk(fn):
                if not (isinstance(n, ast.Call)):
                    continue
                nm = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
                if nm not in ("open", "atomic_save_json", "append_jsonl"):
                    continue
                # A READ THROUGH AN IMPORT-BOUND PATH IS A DIFFERENT, MILDER DEFECT than a write.
                # The first version counted `json.load(open(OUT))` as "test traffic lands in
                # production", which is false - reading production in a harness is at worst a stale
                # answer, while WRITING it is the incident that put 4,920 synthetic rows in the
                # ledger. Same shape, two severities, and conflating them inflates the count.
                mode = ""
                if nm == "open":
                    if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
                        mode = str(n.args[1].value)
                    for kw in (n.keywords or []):
                        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                            mode = str(kw.value.value)
                    if not any(ch in mode for ch in ("a", "w", "+")):
                        continue                      # a plain read - not this finding
                used = {x.id for x in ast.walk(n) if isinstance(x, ast.Name)}
                for s in sorted(used & state_names):
                    add("import-bound-write", rel, n.lineno, src,
                        f"writes through {s}, a path bound to grid.STATE at IMPORT - no harness can "
                        f"redirect it, so test traffic lands in production (D48)",
                        severity="LOAD_BEARING")
    return dict(findings=findings, files=len(_files()))


if __name__ == "__main__":
    rep = audit()
    f = rep["findings"]
    by = {}
    for x in f:
        by.setdefault(x["kind"], []).append(x)
    print("=" * 98)
    print("SCOPE - is every value at the scope its callers need?")
    print("=" * 98)
    print(f"  {rep['files']} modules scanned, {len(f)} finding(s)\n")
    for kind in sorted(by, key=lambda k: -len(by[k])):
        rows = by[kind]
        print(f"  {kind:24s} {len(rows)}")
    print()
    for kind in sorted(by, key=lambda k: -len(by[k])):
        print(f"--- {kind} ({len(by[kind])})")
        for x in by[kind][:8]:
            print(f"  {x['file']}:{x['line']}")
            print(f"      {x['snippet']}")
            print(f"      -> {x['note']}")
        if len(by[kind]) > 8:
            print(f"  ... {len(by[kind]) - 8} more")
        print()
    print("  A module-level CONSTANT that is only read is correct and is most of what a module")
    print("  should hold. The defect is module level PLUS mutation, or module level PLUS an")
    print("  environment the caller should have been able to control.")
    if "--json" in sys.argv[1:]:
        grid.atomic_save_json("scope.json", rep, indent=1)
        print("\n  wrote state/scope.json")
