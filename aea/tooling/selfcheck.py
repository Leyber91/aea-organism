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
    # THIS PATTERN WAS DEAD FOR ITS WHOLE LIFE. `\\\\` in a raw string is two escaped backslashes, so
    # it matched only the JSON/Python-escaped form `C:\\Users` and never a plain `C:\Users`, a
    # `c:/Users`, or a POSIX `/home/`. Measured 1 of 5 real forms. It was never noticed because the
    # emoji rule kept this check's verdict permanently red, so it never had to prove it could go
    # green for the right reason. A leak in `design/A16_WIRTHFORGE.md` sat inside it, committed.
    # The lookbehind keeps `https:` out; the bracket class in the POSIX branch keeps URLs out.
    "absolute windows path": r"(?<![A-Za-z])[A-Za-z]:[\\/]{1,4}(?:Users|home)\b"
                             r"|(?:^|[\s\"'(=`\[])/(?:home|Users)/",
    "employer name": r"(?i)\bindicia\b|\badm group\b",
    # example.org / example.com / .test are RESERVED for documentation (RFC 2606) and are the
    # correct thing to put in synthetic fixtures. Flagging them trains the reader to ignore the
    # check, which is how a real hit gets missed.
    "email address": r"[\w.+-]+@(?!example\.|supplier\.io)[\w-]+\.\w{2,}",
}
# HOUSE RULES ARE NOT LEAKS. An emoji is a style violation with zero blast radius; a leaked employer
# name is irreversible once pushed. They shared one verdict line, that line was permanently red from
# 18 emoji in design docs whose cleanup is a deliberate KILL, and so the privacy guard - the one rule
# this repo calls absolute - could not signal. Law W3: an invariant blocks, a candidate proposes.
HOUSE = {
    "emoji": "[\U0001F300-\U0001FAFF☀-➿]",
}
ALL_RULES = dict(LEAKS, **HOUSE)
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


# THE COUNT IS READ, NOT HARDCODED, AND IT HAS A FLOOR. Both this check and shadow's gate
# matched the literal string "all 31 frozen behaviours hold", so ADDING a frozen behaviour
# broke the gate - a maintenance trap that punishes the exact thing we want to happen. A regex
# alone would let a candidate DELETE behaviours and still pass, so the floor is the real check:
# the suite must report at least this many. Raise it when behaviours are added on purpose.
FROZEN_FLOOR = 139         # +3: a decision is carried out once          # +10: the decision chain, frozen end to end 2026-08-01
# +3 2026-08-02: every flag `live` ACCEPTS must be READ by live.main. `--once` was in KNOWN_FLAGS,
# in the docstring, and read by nothing - it ran one tick then slept the full 1800s default, so
# every caller hung or was killed and recorded as a failure. Unknown flags fail closed; a known
# flag with no implementation failed OPEN, which is worse, because the refusal lists it as accepted.
# +12 2026-08-02: R4b's dry certificate - 5 topics x 10 hostile search results, 0 bytes of any
# outbound request from model output, 0 selection bits, no socket, no model call. Plus the three
# rows asserting the rung stays SHUT: a computable half must never be reported as the whole gate.
# +2 2026-08-02: a private heartbeat key read and never written (hb["_last_decision"] was read three
# times and assigned nowhere for a day, while the frozen test passed because it exercised
# decide.choose directly and never the line in live.py that must write the value).
# +12 2026-08-02: the four kinds of evidence on a synthetic tree that produces all four, and
# verify_funcs' ability to say no - it had checked SPELLING, not reachability, since it was written.
# +6 2026-08-02: the publishing honesty gate, which existed only as a comment in render.py.
# +3 2026-08-02: every check_* defined in the suite must be CALLED by the suite. Two checks were
# written and never wired IN ONE DAY - one appended without an aggregation entry, one spliced into a
# triple-quoted fixture because the patch anchored on a `__main__` line that appears inside data.
# +7 2026-08-02: an entry point may not grade its own axiom (proved falsifiable by the same
# construction that exposed it), and the three scanners that agreed with an empty tree.
# THE FLOOR WAS ALSO STALE: it read 89 while the suite reported 117, so this check had been passing
# on a 28-behaviour margin - the same "raised one floor and not the other" defect it exists to stop.

# WHERE THE ORPHAN COUNT WAS WHEN IT WAS FIRST MEASURED. A ratchet, not a goal: the number may fall
# freely and may not climb without someone deciding to raise this line. 130 of 169 modules are
# reachable from nothing, which is the honest shape of this repo and was previously reported under a
# hardcoded "pass": True.
ORPHAN_FLOOR = 131
# +1 2026-08-02: `aea/lab/dispatch_cert.py`. R4b's dry certificate is a CLI instrument - a human or
# the frozen suite runs it, and the ORGANISM must not reach it, because reaching dispatch is the
# capability a council refused three times. So the orphan is deliberate and the ratchet firing on it
# is the ratchet working: a new unreachable module now costs an acknowledged line rather than
# disappearing into a number nobody reads. Every future rise needs the same sentence.
# +8 2026-08-02: the dispatch edge, with a two-armed control (a planted dead detector and a planted
# rubber stamp must each make it FAIL). The count on the other side is now COUNTED rather than
# hand-summed - the comment below was true of this constant and false of the number it reads.


def check_frozen() -> dict:
    """The 31 frozen behaviours. Two are frozen at a KNOWN-BAD value on purpose: fixing the reader
    is SUPPOSED to break this, which is what makes it a frozen test rather than a passing one."""
    p = os.path.join(ROOT, "aea", "lab", "tests", "test_golden.py")
    if not os.path.exists(p):
        return {"check": "%d frozen behaviours" % FROZEN_FLOOR, "pass": False, "detail": "test file missing"}
    rc, out = _py([p])
    m = re.search(r"all (\d+) frozen behaviours hold", out)
    n = int(m.group(1)) if m else 0
    ok = rc == 0 and n >= FROZEN_FLOOR
    return {"check": "%d frozen behaviours" % FROZEN_FLOOR, "pass": ok,
            "detail": ("all %d hold" % n) if ok else out.strip()[-180:]}


def check_structure() -> dict:
    """Reachability and import-time behaviour, from the AST. Catches the failure a test suite is
    blind to: a module that still works and that nothing can reach any more."""
    from aea.tooling import xray
    d = xray.build()
    c = d["counts"]
    # THE VERDICT WAS THE LITERAL `True`. This printed PASS for months while reporting 130 of 169
    # modules orphaned, and it would have printed PASS over a scan that read zero modules - the
    # strongest possible statement made on the weakest possible evidence. A check whose result does
    # not depend on its input is a label, not a check.
    #
    # ORPHAN_FLOOR is a RATCHET, not a target: it records where the number was when it was first
    # measured, so the count can fall and cannot quietly climb. Lower it when work lands.
    ok = c["modules"] > 0 and c["orphaned"] <= ORPHAN_FLOOR
    why = ("scanned 0 modules - a broken scan, not a clean tree" if not c["modules"]
           else "%d orphaned, above the %d ratchet" % (c["orphaned"], ORPHAN_FLOOR)
           if c["orphaned"] > ORPHAN_FLOOR else None)
    return {"check": "structure", "pass": ok,
            "detail": ("%d modules, %d reachable from a wake, %d orphaned (ratchet %d), "
                       "%d act at import"
                       % (c["modules"], c["reachable_from_wake"], c["orphaned"], ORPHAN_FLOOR,
                          len(d["import_time_effects"]))) if ok else why,
            "data": {"modules": c["modules"], "wake": c["reachable_from_wake"],
                     "orphans": d["orphans"], "effects": d["import_time_effects"]}}


_SCAN_CACHE = {}


def _scan(patterns: dict) -> list:
    """Every tracked file against every pattern given. Memoised on the pattern set, because splitting
    privacy from house style meant two callers over one tree and a measured pass costs 2.5s against a
    7.4s whole check. The two callers now share one walk of the merged set."""
    key = tuple(sorted(patterns))
    if key in _SCAN_CACHE:
        return _SCAN_CACHE[key]
    if patterns is not ALL_RULES:                       # one walk, then filter by kind
        want = set(patterns)
        out = [h for h in _scan(ALL_RULES) if h.rpartition(": ")[2] in want]
        return _SCAN_CACHE.setdefault(key, out)
    hits = []
    n_read = 0
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
            n_read += 1
            for name, pat in patterns.items():
                if re.search(pat, s):
                    hits.append("%s: %s" % (rel, name))
    # A PRIVACY GUARD THAT READ NOTHING REPORTS CLEAN. This walked ROOT and counted no files, so a
    # wrong root, an over-eager skip list, or a rename would have produced a green "no private data
    # in tracked files" over an unexamined tree - and this is the guard standing between the repo and
    # a permanent public leak. Nothing here asserted the scan had a subject until an audit pointed
    # at it. The floor is deliberately far below the real count (~400) so it fails on a broken scan,
    # never on a normal deletion.
    if n_read < 50:
        raise RuntimeError("selfcheck._scan read %d files under %s - a broken scan, not a clean "
                           "repo" % (n_read, ROOT))
    return _SCAN_CACHE.setdefault(key, sorted(set(hits)))


def _by_kind(hits: list) -> str:
    """Group before truncating. The old detail line sorted by PATH and cut at eight, so a real hit in
    web/ sat behind eighteen in design/ and never printed. A truncation that can hide the finding is
    the check failing quietly."""
    kinds = {}
    for h in hits:
        rel, _, kind = h.rpartition(": ")
        kinds.setdefault(kind, []).append(rel)
    return " | ".join("%s x%d (%s%s)" % (k, len(v), v[0], ", +%d" % (len(v) - 1) if len(v) > 1 else "")
                      for k, v in sorted(kinds.items()))


def check_leaks() -> dict:
    """The privacy guard, enforced rather than remembered. Absolute, and irreversible once pushed."""
    hits = _scan(LEAKS)
    return {"check": "no private data in tracked files", "pass": not hits,
            "detail": "clean" if not hits else _by_kind(hits),
            "data": {"hits": hits}}


def check_house() -> dict:
    """House rules. ADVISORY: it reports and never blocks, because a style violation must not be able
    to mask an invariant. Counted so that zero is still a real answer."""
    hits = _scan(HOUSE)
    return {"check": "house style", "pass": True, "advisory": True,
            "detail": "clean" if not hits else _by_kind(hits),
            "data": {"hits": hits}}


def check_paths() -> dict:
    """NO ABSOLUTE PATH IN CODE. The only location this system may know is its own root.

    Everything inside the repo anchors on `grid.ROOT`; everything outside it anchors on `grid.HOME`
    or a declared .env key via `grid.external`. A literal path is a machine the code cannot leave -
    move the checkout, change the user, and it fails silently because the folder is not there.

    THE LOOKBEHIND IS LOAD-BEARING. Without `(?<![A-Za-z])` this matches the `s:` in `https://` and
    reports every URL in the repo as an absolute path - which is exactly what the first run did,
    turning 6 real hits into 61 files of noise. A check that cries wolf is a check nobody reads.
    """
    # AND THE PATH MUST HAVE A BODY. `[A-Za-z]:[\\/]` alone matches `e:\` inside the ordinary
    # Python source line `"except Exception as e:\n"` - a drive letter followed by the escape of a
    # newline. Found 2026-07-29 by this check firing on a file that contains no path at all.
    # Requiring two further non-quote, non-space characters keeps `<path>` and `c:/Users/` and
    # rejects every `X:\n"` / `X:\t"` in a string literal. Same discipline as the lookbehind above:
    # a checker that cries wolf is a checker nobody reads.
    pat = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s\"'\\]{2,}"
                     r"|(?:^|[\s\"'(=])/(?:home|Users)/", re.I)
    # THE SCAN ROOT IS ASSERTED BEFORE IT IS WALKED. `os.walk` on a path that does not exist yields
    # nothing and raises nothing, so this returned "every path anchors on ROOT or HOME" over an
    # empty tree - the identical failure as the two guards that walked `aea/aea/`, in the guard that
    # protects the repo's hardest privacy rule. `assembly.scan` has carried this guard since it was
    # written; copying it here cost two lines and was never done.
    tree = os.path.join(ROOT, "aea")
    if not os.path.isdir(tree):
        return {"check": "no absolute paths in code", "pass": False,
                "detail": "no aea/ under %s - a broken scan, not a clean tree" % ROOT,
                "data": {"hits": []}}
    hits, n_read = [], 0
    for root, dirs, files in os.walk(tree):
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
            n_read += 1
            for i, line in enumerate(s.splitlines(), 1):
                if pat.search(line) and "grid.external" not in line:
                    hits.append("%s:%d" % (rel, i))
    if n_read < 50:
        return {"check": "no absolute paths in code", "pass": False,
                "detail": "read %d python files under %s - a broken scan, not a clean tree"
                          % (n_read, tree), "data": {"hits": hits}}
    return {"check": "no absolute paths in code", "pass": not hits,
            "detail": "every path anchors on ROOT or HOME (%d files)" % n_read if not hits
                      else "%d literal path(s): %s" % (len(hits), ", ".join(hits[:6])),
            "data": {"hits": hits, "files": n_read}}


# STORES THAT MUST NEVER BE COMMITTABLE. Not their CONTENT - their IGNORE COVERAGE. Adopted from
# NVIDIA's aiq-deploy skill, which runs `git check-ignore deploy/.env` BEFORE writing any secret
# rather than trusting that the rule exists. We scanned content for leaks and never once asserted
# that the private stores are actually ignored, so an edit to .gitignore would have been invisible
# until something leaked. A guard that assumes its own precondition is not a guard.
MUST_IGNORE = (
    ".env",
    "state/private_today.json",
    "state/luis_memory.json",
    "state/grid_state.json",
    "state/trust_ledger.json",
)


def check_ignored() -> dict:
    """Every private store is gitignored, verified with git rather than assumed."""
    bad = []
    for rel in MUST_IGNORE:
        p = os.path.join(ROOT, rel)
        r = subprocess.run(["git", "check-ignore", "-q", rel], cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode != 0:                       # not ignored
            tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT,
                                     capture_output=True, text=True).returncode == 0
            bad.append("%s (%s)" % (rel, "TRACKED IN GIT" if tracked
                                    else "not ignored" + ("" if os.path.exists(p) else ", absent")))
    return {"check": "private stores are gitignored", "pass": not bad,
            "detail": "%d stores verified ignored" % len(MUST_IGNORE) if not bad
                      else "; ".join(bad[:4]), "data": {"unignored": bad}}


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


BASELINE = "defect_baseline.json"


def check_ratchet() -> dict:
    """COUNTED DEFECTS DO NOT INCREASE. The one check that changes the rate rather than the count.

    THE PROBLEM IT SOLVES, named by a hard audit on 2026-07-31: *a detection that changes no number
    and fails no command is indistinguishable from no detection.* `transfer` reports 118 advisory
    findings and `scope` reports 60, and nothing anywhere recorded that they were 118 and 60 - so
    the 119th and the 61st were invisible by construction. Every instrument in this repo could see
    the defect and none of them could see the defect ARRIVING.

    WHY A RATCHET AND NOT `blocking=True`. `transfer.py` already records the reason: a check that
    always fails stops being read, and then it disables every check sharing its verdict (D18's
    corollary). A ratchet tolerates the 80 invented ceilings we have decided to live with, and makes
    the 81st a hard stop. It is the only shape that survives a backlog.

    RAISING A BASELINE IS A DELIBERATE ACT. `--rebaseline` writes the current counts and says how
    many rose. Doing it to silence a red run is possible and is a choice a person makes with the
    numbers in front of them, which is exactly the property a mute button lacks."""
    import subprocess
    cur, detail = {}, []
    for mod, keys in (("aea.lab.transfer", ("invented-ceiling", "silent-default",
                                            "unredirectable-store", "count-threshold",
                                            "expiring-only-retry", "scope-violation")),
                      ("aea.tooling.scope", ("import-bound-write", "global-write",
                                             "mutable-module-state", "import-time-work"))):
        try:
            r = subprocess.run([sys.executable, "-m", mod], cwd=str(grid.ROOT),
                               capture_output=True, text=True, timeout=300)
            for line in (r.stdout or "").splitlines():
                p = line.split()
                if len(p) >= 2 and p[0] in keys and p[1].isdigit():
                    cur[p[0]] = int(p[1])
        except Exception as e:
            return {"check": "defect ratchet", "pass": False,
                    "detail": f"could not run {mod}: {str(e)[:60]}"}
    if not cur:
        return {"check": "defect ratchet", "pass": False,
                "detail": "no counts parsed - the detectors changed their output shape"}

    base = grid.load_json(BASELINE, None)
    if base is None:
        grid.atomic_save_json(BASELINE, {"counts": cur, "set": time.strftime("%Y-%m-%d %H:%M UTC",
                                                                            time.gmtime())}, indent=1)
        return {"check": "defect ratchet", "pass": True,
                "detail": "baseline written (%d shapes) - first run" % len(cur)}

    prev, risen = base.get("counts") or {}, []
    for k, v in sorted(cur.items()):
        was = prev.get(k)
        if was is not None and v > was:
            risen.append(f"{k} {was}->{v}")
        detail.append(f"{k} {v}" + ("" if was is None or v == was else f" (was {was})"))
    return {"check": "defect ratchet", "pass": not risen,
            "detail": (", ".join(detail) if not risen
                       else "ROSE: " + "; ".join(risen) + " - a NEW instance of a known defect")}


CHECKS = [("structure", check_structure), ("state", check_state), ("leaks", check_leaks), ("ignored", check_ignored),
          ("paths", check_paths),
          ("imports", check_imports), ("frozen", check_frozen), ("house", check_house),
          ("ratchet", check_ratchet)]
SLOW = {"imports", "frozen", "ratchet"}


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
            # An advisory row never moves the verdict. If it could, the verdict would be reporting
            # style and the reader would learn to ignore a red line.
            "pass": all(c["pass"] for c in out if not c.get("advisory")), "checks": out}


def render(d: dict) -> str:
    L = ["SELFCHECK - whole-system invariants (%.1fs)" % d["seconds"], "=" * 84]
    for c in d["checks"]:
        mark = "note" if c.get("advisory") else ("PASS" if c["pass"] else "FAIL")
        L.append("  [%4s] %-34s %s" % (mark, c["check"],
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
