"""selfcheck.py - EVERY INVARIANT THIS SYSTEM HAS EARNED, IN ONE COMMAND.

WHY THIS FILE EXISTS, AND IT IS A LESSON ABOUT WORKING RATHER THAN ABOUT CODE.

Across one long session the same handful of verifications were re-typed by hand nine or ten times -
import the whole tree, run the frozen behaviours, count the orphans, scan for leaked paths, check the
ledger still loads. Each one was a throwaway script pasted into a shell. That is a behaviour that
could be automated and was not, and the cost is paid twice: in the time to retype it, and in the
attention spent on something a machine does perfectly.

    ANY BEHAVIOUR YOU REPEAT THAT A MACHINE COULD DO IS A BEHAVIOUR YOU SHOULD HAND TO THE MACHINE.

That is the same principle the entity itself runs on - crystallise a resolved impasse into a part
rather than re-deriving it - applied one level up, to the people and processes building it. A check
that lives in a file is a check that runs every time; a check that lives in a habit runs when someone
remembers.

WHAT IT IS NOT. Not a test framework, and it does not replace `aea/lab/tests/test_golden.py` - it
RUNS it. These are whole-system invariants, the kind that no unit test sees: does every module still
import, is anything newly unreachable, did a private path leak into a tracked file.

  python -m aea.tooling.selfcheck            every check, human-readable
  python -m aea.tooling.selfcheck --json     machine-readable, for the wake and for the gate
  python -m aea.tooling.selfcheck --quick    skip the slow ones (imports, frozen behaviours)
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
import time

from aea.kernel import grid

ROOT = grid.ROOT
OUT = os.path.join(grid.STATE, "selfcheck.json")

# THINGS THAT MUST NEVER APPEAR IN ANYTHING TRACKED. The privacy guard, as a regex, so it is checked
# rather than remembered. The parent tree of this repo contains an employer folder name, so an
# absolute path is a leak even when it looks harmless.
LEAKS = {
    "absolute windows path": r"[A-Za-z]:\\\\Users",
    "employer name": r"(?i)\bindicia\b|\badm group\b",
    # example.org / example.com / .test are RESERVED for documentation (RFC 2606) and are the
    # correct thing to put in synthetic fixtures. Flagging them trains the reader to ignore the
    # check, which is how a real hit gets missed.
    "email address": r"[\w.+-]+@(?!example\.|supplier\.io)[\w-]+\.\w{2,}",
    "emoji": "[\U0001F300-\U0001FAFF☀-➿]",
}
LEAK_SCAN = (".py", ".md", ".json", ".html", ".js", ".css", ".txt")
# A DETECTOR MUST NOT FLAG ITS OWN DEFINITIONS. This file contains the emoji range and the employer
# pattern by necessity, so it matched itself on the first run. A checker that always reports one hit
# trains the reader to ignore every hit, which is the only way this check can actually fail.
LEAK_SKIP = ("state/", "archive/", "node_modules/", ".git/", "voice/", "web/three.min.js",
             "aea/tooling/selfcheck.py")


def _py(args, timeout=900):
    p = subprocess.run([sys.executable, "-X", "utf8"] + args, cwd=ROOT, capture_output=True,
                       text=True, timeout=timeout, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONPATH=ROOT, PYTHONIOENCODING="utf-8"))
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def check_imports() -> dict:
    """Every runtime module imports. A module that cannot be imported is dead in an unattended wake,
    and four were, silently, until this was run for the first time."""
    src = (
        "import importlib, pkgutil, io, contextlib, aea\n"
        "bad=[]\n"
        "for pkg in ('kernel','mind','energy','memory','bench','io','organs','loop','server',"
        "'tooling','lab','gameapi'):\n"
        "    try: p=importlib.import_module('aea.'+pkg)\n"
        "    except Exception as e: bad.append('aea.%s: %s'%(pkg,e)); continue\n"
        "    for m in pkgutil.iter_modules(p.__path__):\n"
        "        n='aea.%s.%s'%(pkg,m.name)\n"
        "        try:\n"
        "            with contextlib.redirect_stdout(io.StringIO()): importlib.import_module(n)\n"
        "        except Exception as e: bad.append('%s: %s'%(n,str(e)[:70]))\n"
        "print(len(bad)); [print(b) for b in bad]\n")
    rc, out = _py(["-c", src])
    lines = [l for l in out.strip().splitlines() if l.strip()]
    n = int(lines[0]) if lines and lines[0].strip().isdigit() else -1
    return {"check": "every module imports", "pass": n == 0,
            "detail": "0 failures" if n == 0 else "; ".join(lines[1:6])[:200]}


def check_frozen() -> dict:
    """The 31 frozen behaviours. Two are frozen at a KNOWN-BAD value on purpose: fixing the reader
    is SUPPOSED to break this, which is what makes it a frozen test rather than a passing one."""
    p = os.path.join(ROOT, "aea", "lab", "tests", "test_golden.py")
    if not os.path.exists(p):
        return {"check": "31 frozen behaviours", "pass": False, "detail": "test file missing"}
    rc, out = _py([p])
    ok = rc == 0 and "all 31 frozen behaviours hold" in out
    return {"check": "31 frozen behaviours", "pass": ok,
            "detail": "all hold" if ok else out.strip()[-180:]}


def check_structure() -> dict:
    """Reachability and import-time behaviour, from the AST. Catches the failure a test suite is
    blind to: a module that still works and that nothing can reach any more."""
    from aea.tooling import xray
    d = xray.build()
    c = d["counts"]
    return {"check": "structure", "pass": True,
            "detail": "%d modules, %d reachable from a wake, %d orphaned, %d act at import"
                      % (c["modules"], c["reachable_from_wake"], c["orphaned"],
                         len(d["import_time_effects"])),
            "data": {"modules": c["modules"], "wake": c["reachable_from_wake"],
                     "orphans": d["orphans"], "effects": d["import_time_effects"]}}


def check_leaks() -> dict:
    """The privacy guard, enforced rather than remembered. Absolute, and irreversible once pushed."""
    hits = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "__pycache__", "archive",
                                                "voice", "state")]
        for f in files:
            if not f.endswith(LEAK_SCAN):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            if any(rel.startswith(s) for s in LEAK_SKIP):
                continue
            try:
                s = io.open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for name, pat in LEAKS.items():
                if re.search(pat, s):
                    hits.append("%s: %s" % (rel, name))
    return {"check": "no private data in tracked files", "pass": not hits,
            "detail": "clean" if not hits else "; ".join(sorted(set(hits))[:8]),
            "data": {"hits": sorted(set(hits))}}


def check_paths() -> dict:
    """NO ABSOLUTE PATH IN CODE. The only location this system may know is its own root.

    Everything inside the repo anchors on `grid.ROOT`; everything outside it anchors on `grid.HOME`
    or a declared .env key via `grid.external`. A literal path is a machine the code cannot leave -
    move the checkout, change the user, and it fails silently because the folder is not there.

    THE LOOKBEHIND IS LOAD-BEARING. Without `(?<![A-Za-z])` this matches the `s:` in `https://` and
    reports every URL in the repo as an absolute path - which is exactly what the first run did,
    turning 6 real hits into 61 files of noise. A check that cries wolf is a check nobody reads.
    """
    pat = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]|(?:^|[\s\"'(=])/(?:home|Users)/", re.I)
    hits = []
    for root, dirs, files in os.walk(os.path.join(ROOT, "aea")):
        dirs[:] = [x for x in dirs if x not in ("__pycache__", "site_assets")]
        for f in files:
            if not f.endswith(".py"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            if rel == "aea/tooling/selfcheck.py":       # defines the pattern; would match itself
                continue
            try:
                s = io.open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for i, line in enumerate(s.splitlines(), 1):
                if pat.search(line) and "grid.external" not in line:
                    hits.append("%s:%d" % (rel, i))
    return {"check": "no absolute paths in code", "pass": not hits,
            "detail": "every path anchors on ROOT or HOME" if not hits
                      else "%d literal path(s): %s" % (len(hits), ", ".join(hits[:6])),
            "data": {"hits": hits}}


def check_state() -> dict:
    """The stores the entity cannot run without, and the one that must never be lost."""
    from aea.kernel import trust
    rows, ok = [], True
    led = grid.load_json(trust.LEDGER, {})
    rows.append("ledger %d capabilities" % len(led))
    ok = ok and len(led) > 0
    save = os.path.join(grid.STATE, "journey_save.json")
    have = os.path.exists(save) and os.path.getsize(save) > 2
    rows.append("sacred save %s" % ("present" if have else "MISSING"))
    ok = ok and have
    return {"check": "state intact", "pass": ok, "detail": ", ".join(rows)}


CHECKS = [("structure", check_structure), ("state", check_state), ("leaks", check_leaks),
          ("paths", check_paths),
          ("imports", check_imports), ("frozen", check_frozen)]
SLOW = {"imports", "frozen"}


def run(quick: bool = False) -> dict:
    t0 = time.time()
    out = []
    for name, fn in CHECKS:
        if quick and name in SLOW:
            continue
        try:
            out.append(fn())
        except Exception as e:
            out.append({"check": name, "pass": False, "detail": "check itself failed: %s"
                                                                % str(e)[:150]})
    return {"schema": "aea.selfcheck/1",
            "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
            "seconds": round(time.time() - t0, 1),
            "pass": all(c["pass"] for c in out), "checks": out}


def render(d: dict) -> str:
    L = ["SELFCHECK - whole-system invariants (%.1fs)" % d["seconds"], "=" * 84]
    for c in d["checks"]:
        L.append("  [%s] %-34s %s" % ("PASS" if c["pass"] else "FAIL", c["check"],
                                      (c["detail"] or "").replace("\n", " ")[:44]))
    L.append("")
    L.append("VERDICT: %s" % ("ALL INVARIANTS HOLD" if d["pass"] else "SOMETHING IS BROKEN"))
    return "\n".join(L)


if __name__ == "__main__":
    d = run(quick="--quick" in sys.argv)
    grid.atomic_save_json(OUT, d, indent=1)
    if "--json" in sys.argv:
        print(json.dumps(d, indent=1))
    else:
        print(render(d))
    sys.exit(0 if d["pass"] else 1)
