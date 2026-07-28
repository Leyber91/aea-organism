"""heal.py - DETERMINISTIC DETECTORS THAT LOOK FOR WHAT COULD BE BETTER, NOT FOR WHAT IS BROKEN.

TWO KINDS OF CHECK, AND MIXING THEM RUINS BOTH:

    INVARIANT             violated means BROKEN. Blocks. Lives in selfcheck.py.
    IMPROVEMENT CANDIDATE nothing is broken; it could be better. PROPOSES, never applies.

A repo that reports "37 improvements available" alongside "the ledger is corrupt" trains you to skim
past both. So this file never returns a failure and never edits anything. It returns candidates,
ranked, with the evidence attached.

NOT AI, AND THAT IS THE WHOLE DESIGN. Every detector here is an AST or string computation with a
deterministic answer. A language model asked to "find improvements" will always find some, because
producing text is what it does - it cannot return an honest empty result. Detection has to be
mechanical so that ZERO CANDIDATES IS A REAL ANSWER. The model's place is one step later: writing
the change a detector already justified, which `shadow.propose` then gates against tests the model
cannot author.

WHY THESE FIVE DETECTORS AND NOT OTHERS. Each one is here because it would have caught something
this repo actually paid for:

    near-duplicate functions   would have found the SIX independent model selectors, each ranking
                               on a different key, none calling another
    repeated literals          would have found the TWENTY-ONE places holding rate-limit numbers,
                               four of which disagreed with each other
    swallowed errors           `except Exception: pass` hid a state-destroying quarantine for weeks
    stub bodies                a function that returns an empty list by construction reported
                               "nothing was toxic" instead of "nothing was tested"
    god modules                harness.py is 983 lines and every defect found in it was a defect of
                               nobody being able to hold it in their head

THE RULE THAT KEEPS THIS FROM BECOMING CHURN. A candidate is only worth acting on if the change is
DEMONSTRABLY better, and `shadow.gate` is what demonstrates it. Improvement for its own sake is the
failure mode on one side; "it works, do not touch it" is the failure mode on the other. The gate is
what lets you refuse both: change it if the evidence says better, keep it if it does not.

  python -m aea.tooling.heal            the candidates, ranked
  python -m aea.tooling.heal --json     state/heal.json
  python -m aea.tooling.heal --kind K   one detector only
"""
from __future__ import annotations

import ast
import collections
import io
import json
import os
import re
import sys
import time

from aea.kernel import grid

ROOT = grid.ROOT
PKG = os.path.join(ROOT, "aea")
OUT = os.path.join(grid.STATE, "heal.json")

MIN_FN_LINES = 6          # below this, two functions being alike means nothing
GOD_MODULE = 500          # lines; above this, nobody holds it in their head
LONG_FN = 60              # lines in one function
MIN_LITERAL_REPEATS = 3   # a number in three files is a constant that escaped


def _files() -> list:
    out = []
    for root, dirs, files in os.walk(PKG):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", "site_assets")]
        for f in files:
            if f.endswith(".py"):
                out.append(os.path.join(root, f))
    return sorted(out)


def _rel(p: str) -> str:
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def _parse(p: str):
    try:
        src = io.open(p, encoding="utf-8", errors="ignore").read()
        return src, ast.parse(src)
    except Exception:
        return None, None


def _shape(fn: ast.AST) -> str:
    """A function's STRUCTURE with every name erased.

    Two functions doing the same thing under different names produce the same shape. That is the
    point: the six selectors in this repo are not textual copies - they are the same walk over a
    list with a different sort key, which no text-similarity tool would have flagged.
    """
    parts = []
    for n in ast.walk(fn):
        if isinstance(n, (ast.For, ast.While, ast.If, ast.Try, ast.With, ast.Return,
                          ast.Compare, ast.BoolOp, ast.Call, ast.ListComp, ast.Assign,
                          ast.Raise, ast.Subscript, ast.Attribute)):
            parts.append(type(n).__name__)
    return ",".join(parts)


# ---------------------------------------------------------------------------------------------

def near_duplicates() -> list:
    fns = []
    for p in _files():
        src, tree = _parse(p)
        if tree is None:
            continue
        lines = src.splitlines()
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                span = (getattr(n, "end_lineno", n.lineno) or n.lineno) - n.lineno + 1
                if span < MIN_FN_LINES:
                    continue
                sh = _shape(n)
                if len(sh) < 40:
                    continue
                fns.append({"file": _rel(p), "line": n.lineno, "name": n.name,
                            "lines": span, "shape": sh})
    by = collections.defaultdict(list)
    for f in fns:
        by[f["shape"]].append(f)
    out = []
    for sh, group in by.items():
        files = {g["file"] for g in group}
        if len(group) < 2 or len(files) < 2:
            continue
        out.append({
            "kind": "near-duplicate", "weight": len(group) * 2 + len(files),
            "what": "%d functions in %d files share an identical control-flow shape"
                    % (len(group), len(files)),
            "where": ["%s:%d %s()" % (g["file"], g["line"], g["name"]) for g in group],
            "why": "the same procedure written more than once drifts apart; this repo carried six "
                   "model selectors ranking on four different keys before anyone counted them",
        })
    return sorted(out, key=lambda x: -x["weight"])


def disagreeing_constants() -> list:
    """THE SAME NAMED SETTING HOLDING DIFFERENT VALUES IN DIFFERENT FILES.

    The first version of this detector flagged any repeated literal and reported that "the literal 3
    appears in 63 files" - true, meaningless, and a check nobody would read twice. Small integers are
    indices and slices, not configuration.

    The real defect is narrower and this catches it exactly: a setting with ONE NAME and MORE THAN
    ONE VALUE. That is what `rpm` being 40 in the plant table, 25 in a measurement note and 8 in the
    lab's semaphore actually looked like, and it is why four rate limits in this repo disagreed with
    each other while every one of them looked deliberate in its own file.

    Only module-level CONSTANTS (uppercase) and string-keyed dict entries count, because those are
    the two ways configuration is written here.
    """
    vals = collections.defaultdict(lambda: collections.defaultdict(list))
    for p in _files():
        src, tree = _parse(p)
        if tree is None:
            continue
        rel = _rel(p)
        for n in tree.body:                        # module level only
            if isinstance(n, ast.Assign) and isinstance(getattr(n, "value", None), ast.Constant):
                for t in n.targets:
                    name = getattr(t, "id", "")
                    if name.isupper() and len(name) > 2 and isinstance(n.value.value, (int, float)):
                        vals[name][n.value.value].append("%s:%d" % (rel, n.lineno))
        # ONLY DICTS THAT ARE CONFIGURATION TABLES, meaning assigned at module level to an
        # UPPERCASE name - grid.PLANTS is the shape this is for. Walking every dict in the tree
        # instead reported 'truth', 'tokens' and 'ms' holding many values, which are DATA RECORDS
        # with per-row numbers, not settings that disagree. A detector that cannot tell a record
        # from a setting produces confident noise, and noise is how the real find gets skipped.
        for n in tree.body:
            if not isinstance(n, ast.Assign):
                continue
            names = [getattr(t, "id", "") for t in n.targets]
            if not any(x.isupper() and len(x) > 2 for x in names):
                continue
            for sub in ast.walk(n.value):
                if not isinstance(sub, ast.Dict):
                    continue
                for k, v in zip(sub.keys, sub.values):
                    if (isinstance(k, ast.Constant) and isinstance(k.value, str)
                            and isinstance(v, ast.Constant)
                            and isinstance(v.value, (int, float))
                            and not isinstance(v.value, bool)):
                        vals[k.value][v.value].append("%s:%d" % (rel, getattr(k, "lineno", 0)))
    out = []
    for name, by_val in vals.items():
        if len(by_val) < 2:
            continue
        files = {w.split(":")[0] for ws in by_val.values() for w in ws}
        if len(files) < 2:
            continue
        out.append({
            "kind": "disagreeing-constant", "weight": len(by_val) * 3 + len(files),
            "what": "%r holds %d different values across %d files: %s"
                    % (name, len(by_val), len(files),
                       ", ".join(str(v) for v in sorted(by_val, key=str)[:5])),
            "where": ["%s = %s" % (w, v) for v, ws in sorted(by_val.items(), key=str)
                      for w in ws[:2]],
            "why": "one name, more than one value - whichever file you happen to read decides what "
                   "you believe. This is what four disagreeing rate limits looked like.",
        })
    return sorted(out, key=lambda x: -x["weight"])[:12]


def swallowed_errors() -> list:
    """`except: pass` - the construct that hid a state-destroying quarantine for weeks."""
    out = []
    for p in _files():
        src, tree = _parse(p)
        if tree is None:
            continue
        for n in ast.walk(tree):
            if not isinstance(n, ast.ExceptHandler):
                continue
            body = [b for b in n.body if not isinstance(b, ast.Expr)
                    or not isinstance(getattr(b, "value", None), ast.Constant)]
            if len(body) == 1 and isinstance(body[0], ast.Pass):
                broad = n.type is None or getattr(n.type, "id", "") in ("Exception", "BaseException")
                out.append({
                    "kind": "swallowed-error", "weight": 3 if broad else 1,
                    "what": "an exception handler whose whole body is `pass`",
                    "where": ["%s:%d" % (_rel(p), n.lineno)],
                    "why": "a failure that leaves no trace is indistinguishable from success, which "
                           "is the one thing an unattended system may never allow",
                })
    return sorted(out, key=lambda x: -x["weight"])


def stub_bodies() -> list:
    """Functions that cannot do anything, and functions that say they are unfinished."""
    out = []
    for p in _files():
        src, tree = _parse(p)
        if tree is None:
            continue
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body = [b for b in n.body if not (isinstance(b, ast.Expr)
                        and isinstance(getattr(b, "value", None), ast.Constant))]
                if len(body) == 1 and isinstance(body[0], (ast.Pass, ast.Ellipsis)):
                    out.append({
                        "kind": "stub", "weight": 2,
                        "what": "%s() has an empty body" % n.name,
                        "where": ["%s:%d" % (_rel(p), n.lineno)],
                        "why": "a stub that is called returns nothing and reports no error",
                    })
        for i, line in enumerate(src.splitlines(), 1):
            if re.search(r"#\s*(TODO|FIXME|XXX|HACK)\b", line):
                out.append({
                    "kind": "stub", "weight": 1,
                    "what": line.strip()[:90],
                    "where": ["%s:%d" % (_rel(p), i)],
                    "why": "an unfinished intention recorded in a comment nobody greps",
                })
    return sorted(out, key=lambda x: -x["weight"])


def god_modules() -> list:
    out = []
    for p in _files():
        src, tree = _parse(p)
        if tree is None:
            continue
        n_lines = len(src.splitlines())
        if n_lines > GOD_MODULE:
            out.append({
                "kind": "god-module", "weight": n_lines // 100,
                "what": "%s is %d lines" % (_rel(p), n_lines),
                "where": [_rel(p)],
                "why": "every defect found in this repo's largest file was a defect of nobody being "
                       "able to hold the whole file in their head at once",
            })
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                span = (getattr(n, "end_lineno", n.lineno) or n.lineno) - n.lineno + 1
                if span > LONG_FN:
                    out.append({
                        "kind": "god-module", "weight": span // 30,
                        "what": "%s() is %d lines" % (n.name, span),
                        "where": ["%s:%d" % (_rel(p), n.lineno)],
                        "why": "a function longer than a screen hides its own branches",
                    })
    return sorted(out, key=lambda x: -x["weight"])


DETECTORS = {
    "near-duplicate": near_duplicates,
    "disagreeing-constant": disagreeing_constants,
    "swallowed-error": swallowed_errors,
    "stub": stub_bodies,
    "god-module": god_modules,
}


def scan(kinds=None) -> dict:
    t0 = time.time()
    cands = []
    for k, fn in DETECTORS.items():
        if kinds and k not in kinds:
            continue
        try:
            cands += fn()
        except Exception as e:
            cands.append({"kind": k, "weight": 0, "what": "detector failed: %s" % str(e)[:110],
                          "where": [], "why": "a broken detector is worse than no detector"})
    cands.sort(key=lambda c: -c["weight"])
    return {"schema": "aea.heal/1",
            "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
            "seconds": round(time.time() - t0, 1),
            "counts": dict(collections.Counter(c["kind"] for c in cands)),
            "candidates": cands}


def render(d: dict, top: int = 16) -> str:
    L = ["HEAL - improvement candidates. NOTHING HERE IS BROKEN, and nothing here is applied.",
         "=" * 96,
         "%d candidates in %.1fs   %s" % (len(d["candidates"]), d["seconds"],
                                          "  ".join("%s %d" % (k, v)
                                                    for k, v in sorted(d["counts"].items())))]
    L.append("")
    for c in d["candidates"][:top]:
        L.append("[%2d] %-16s %s" % (c["weight"], c["kind"], c["what"][:66]))
        for w in c["where"][:4]:
            L.append("       %s" % w)
        if len(c["where"]) > 4:
            L.append("       ... and %d more" % (len(c["where"]) - 4))
    if len(d["candidates"]) > top:
        L.append("")
        L.append("... %d more. Ranked by weight; nothing is applied by this tool."
                 % (len(d["candidates"]) - top))
    return "\n".join(L)


if __name__ == "__main__":
    kinds = None
    if "--kind" in sys.argv:
        kinds = {sys.argv[sys.argv.index("--kind") + 1]}
    d = scan(kinds)
    grid.atomic_save_json(OUT, d, indent=1)
    print(json.dumps(d, indent=1) if "--json" in sys.argv else render(d))
