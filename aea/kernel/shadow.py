"""shadow.py - THE ENTITY TESTS A CHANGE TO ITSELF WITHOUT BECOMING IT YET.

THE LOOP THIS COMPLETES, and every step before the last one already exists:

    know what I am made of      state/xray.json          BUILT
    hit a blocker               impasse.read             BUILT
    locate the cause            xray + the ledger        BUILT
    propose a change            a declaration, not code  unstick.moves_for is the pattern
    COPY MYSELF                 this file
    TEST THE COPY               this file
    promote only if better      this file - AND IT REFUSES TO DO IT ALONE
    keep the old self reachable git, which already does this perfectly

WHY GIT AND NOT A COPY. `git worktree` produces a complete, isolated checkout in about a second
without duplicating a single blob, and the store it draws from is already content-addressed,
diffable, and auditable. A hand-rolled copy of the tree would be slower, would drift, and would
reinvent - worse - the one tool on this machine designed for exactly this. The previous self is not
something this module has to store. It is a commit.

THE TWO RULES THAT MAKE SELF-MODIFICATION SAFE RATHER THAN SUICIDAL:

  1 THE ENTITY MAY NOT AUTHOR THE TEST THAT JUDGES ITS OWN CHANGE.
    If it writes both the improvement and the proof, the proof passes. That is criterion
    contamination, and this repo hit it three times on 2026-07-28 alone - a capability promoted
    because two files opened, a brief section reading "(grid busy)" graded a clean run, and
    gather_public graded on a substring of the model's own prose. So the GATE below is built only
    from checks that already existed and that a proposal cannot edit: the frozen golden behaviours,
    a whole-tree import smoke test, and a no-new-orphans comparison. A proposal that touches the
    gate is REJECTED for that reason alone.

  2 ROLLBACK TARGETS THE LAST *PROVEN* VERSION, NOT THE LAST ONE.
    "Keep the previous version" is worthless if the previous version was also broken. Known-good is
    a status a commit EARNS by passing the gate, recorded in state/known_good.json.

AND THE CEILING HOLDS. `self_modify_code` is pinned at ceiling 1 - DRAFT, a reviewable diff. So
`propose()` writes a proposal and a verdict and stops. There is deliberately no promote() in this
file. Autonomy over one's own source is granted, never taken, and the gap between "the tests passed"
and "this is now what I am" is where a human belongs.

  python -m aea.kernel.shadow --gate       run the gate against the working tree
  python -m aea.kernel.shadow --try FILE   open a shadow, apply a file, gate it, write a proposal
  python -m aea.kernel.shadow --proposals  what has been proposed and how it scored
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

from aea.kernel import grid

ROOT = grid.ROOT
SHADOWS = os.path.join(grid.STATE, "shadows")
PROPOSALS = os.path.join(grid.STATE, "proposals")
KNOWN_GOOD = os.path.join(grid.STATE, "known_good.json")

# FILES A PROPOSAL MAY NOT TOUCH. Not a style rule - the gate must be unauthorable by the thing it
# judges, and a test the candidate rewrote is not evidence.
PROTECTED = (
    "aea/lab/tests/",          # the 31 frozen behaviours
    "aea/kernel/shadow.py",    # this file: the judge
    "aea/kernel/trust.py",     # the ledger and the CHARTER ceilings
    "aea/tooling/xray.py",     # computes gate checks 3 and 4 - see GATE_FILES
    "aea/tooling/selfcheck.py",
    "aea/lab/stats.py",        # the tests any future gate would use to say "better"
    "aea/lab/grader.py",
    ".git",
)

# EVERY FILE THAT COMPUTES ANY PART OF A VERDICT. Restored from the running self into the shadow
# AFTER the candidate's changes are applied, so the gate is always the JUDGE'S code and never the
# CANDIDATE'S - however the candidate's version got there.
# THE COUNT IS READ, NOT HARDCODED, AND IT HAS A FLOOR. Both this check and shadow's gate
# matched the literal string "all 31 frozen behaviours hold", so ADDING a frozen behaviour
# broke the gate - a maintenance trap that punishes the exact thing we want to happen. A regex
# alone would let a candidate DELETE behaviours and still pass, so the floor is the real check:
# the suite must report at least this many. Raise it when behaviours are added on purpose.
FROZEN_FLOOR = 46

GATE_FILES = (
    "aea/tooling/xray.py",
    "aea/tooling/selfcheck.py",
    "aea/lab/tests/test_golden.py",
    "aea/lab/stats.py",
    "aea/lab/grader.py",
)

# ------------------------------------------------------------------------------------------------
# THE LADDER: dev -> qa -> prod, WITH THE ROLE THAT OWNS EACH RUNG AND WHAT IT CANNOT SEE.
#
# Luis, 2026-07-29, authorising self-modification: "you do develop, then dev, then qa, then prod...
# only to pass verification, not to mess things up, be able to do it correctly."
#
# The stages already existed in this file as unnamed steps. Naming them buys three things a nameless
# sequence cannot give: a proposal can record HOW FAR it got and why it stopped, each rung declares
# the authority that owns it, and - the part that matters most - each rung states WHAT IT DOES NOT
# COVER. A pipeline that implies coverage it does not have is more dangerous than no pipeline,
# because it converts an unexamined risk into a green tick. Every `blind` entry below is a real gap
# measured in this repo, not a hypothetical.
STAGES = (
    {
        "stage": "dev",
        "role": "DEVELOPER",
        "may": "write any file that is not PROTECTED, inside a throwaway git worktree",
        "may_not": "touch a GATE file, or judge the result",
        "advances_when": "the change applies cleanly to a shadow of the RUNNING self",
        "blind": [
            "syntax is not checked here; a file that cannot parse still applies cleanly",
            "nothing has been executed at this rung, so 'it applies' says nothing about behaviour",
        ],
    },
    {
        "stage": "qa",
        "role": "VERIFIER",
        "may": "run the four unauthorable checks and return a verdict",
        "may_not": "edit a check, add one, or write to the candidate. GATE files are RESTORED from "
                   "the running self before judging, so editing one cannot help a proposal pass",
        "advances_when": "every check passes: own-code-loaded, all modules import, the frozen "
                         "behaviours, no new orphans, no new import-time effects, and ONE REAL "
                         "model call through the candidate's own draw",
        "blind": [
            "a change can pass every check and still be WRONG - the gate proves not-broken, never good",
            "the live call proves the candidate can think AT ALL; it does not measure quality, "
            "cost or whether the answer got better",
            "the orphan comparison is structural: it cannot see a module that is still imported and "
            "no longer does anything",
            "performance, cost and latency are entirely unmeasured at this rung",
        ],
    },
    {
        "stage": "prod",
        "role": "RELEASE (a human, always)",
        "may": "promote a passing proposal into the running self",
        "may_not": "be automated. There is deliberately no promote() in this module",
        "advances_when": "a person reads the diff and the verdict and says so",
        "blind": [
            "a human reviewer is the last check and also the least deterministic one",
        ],
    },
)


def stages() -> str:
    """The ladder, as text, so the entity can state what its own pipeline covers and what it does
    not. Law S7: an outline may abbreviate detail, it may never drop existence - and the existence
    most often dropped is the blind spot."""
    L = ["THE SELF-MODIFICATION LADDER - dev -> qa -> prod", "=" * 92]
    for s in STAGES:
        L.append("")
        L.append("%-6s owned by %s" % (s["stage"].upper(), s["role"]))
        L.append("   may        %s" % s["may"])
        L.append("   may NOT    %s" % s["may_not"])
        L.append("   advances   %s" % s["advances_when"])
        for b in s["blind"]:
            L.append("   BLIND TO   %s" % b)
    L += ["", "A proposal records the furthest rung it reached. Reaching qa is not passing qa, and "
              "passing qa is not release."]
    return "\n".join(L)


def _run(args, cwd=None, timeout=900, env=None):
    p = subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True, env=env,
                       timeout=timeout, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def _pyenv(path: str) -> dict:
    """A candidate must import ITS OWN tree, not the one this process was started from.

    `PYTHONDONTWRITEBYTECODE` IS NOT HYGIENE. IT IS A CORRECTNESS GATE.

    CPython validates a cached `.pyc` against exactly two things: the source mtime truncated to
    whole seconds, and the source size. A self-modifying agent's most common edit - flip a constant,
    swap `>` for `<`, change one digit - produces a file with the SAME SIZE in the SAME SECOND, so
    the stale bytecode passes both checks and the candidate runs the OLD code while the gate reports
    a pass. `sys.dont_write_bytecode` does not save you: it suppresses writing, not reading.

    Measured on this machine: a forced same-mtime, same-size edit re-ran the previous value. For a
    system whose whole purpose is judging a change to itself, testing the version you did not write
    is the worst possible failure, because it is indistinguishable from success.
    """
    return dict(os.environ, PYTHONPATH=path, PYTHONIOENCODING="utf-8",
                PYTHONDONTWRITEBYTECODE="1")


def head() -> str:
    code, out = _run(["git", "rev-parse", "HEAD"])
    return out.strip() if code == 0 else "?"


def dirty() -> list:
    """Tracked files modified but not committed. THE SELF THAT IS RUNNING vs THE SELF GIT KNOWS.

    This distinction broke the first version of this module within minutes of writing it. A shadow
    is checked out from a COMMIT, so it contains HEAD - but what is actually running is the working
    tree, and here those differed by a full day of fixes. The consequence was two-fold and both
    halves are the same error: the gate tested a version nobody runs, and `mark_known_good` stamped
    the WORKING TREE's passing verdict onto HEAD's commit hash. A verdict attached to the wrong tree
    is not a weaker claim, it is a false one.
    """
    out = []
    # MODIFIED TRACKED FILES...
    code, mod = _run(["git", "diff", "--name-only", "HEAD"])
    if code == 0:
        out += [l.strip() for l in mod.splitlines() if l.strip()]
    # ...AND FILES GIT HAS NEVER HEARD OF, WHICH IS THE HALF THAT BROKE IT.
    #
    # The first version used `git diff` alone. That lists modified TRACKED files - so every module
    # written today and not yet committed (xray, shadow, hands, seats, fit, goals, crystal, impasse,
    # unstick: nine of them, most of the kernel) was invisible to it, and the shadow was built
    # WITHOUT THEM. The control run failed and the harness looked broken, which is exactly what a
    # control is for. `--exclude-standard` keeps gitignored state and secrets out.
    code, new = _run(["git", "ls-files", "--others", "--exclude-standard"])
    if code == 0:
        out += [l.strip() for l in new.splitlines() if l.strip()]
    return sorted(set(out))


def _carry_worktree(dest: str, skip=()) -> list:
    """Copy the uncommitted working-tree state into a shadow, so the shadow is WHAT IS RUNNING.

    A proposal has to be tested against the current self, not against the last commit. Without this
    the gate answers a question nobody asked.
    """
    carried = []
    for rel in dirty():
        if rel in skip or protected(rel) or rel.endswith("/"):
            continue
        # NEVER CARRY `state/`, AND THERE ARE TWO SEPARATE REASONS.
        #
        # 1 RECURSION. Shadows are created under state/shadows/, inside the repo, so they show up as
        #   untracked files and the copier tried to copy a shadow into a shadow. It crashed on the
        #   directory entry, which was lucky - silently succeeding would have been worse.
        # 2 A CANDIDATE MUST NOT INHERIT THE LIVE LEDGER. state/ is runtime truth: the trust ledger,
        #   the sacred save, the experience record. A version being tested should start from a clean
        #   state directory, or its run contaminates the record of the self that is actually running.
        if rel.startswith("state/") or rel.startswith("state\\"):
            continue
        src = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(src):          # deleted, or a directory entry
            continue
        dst = os.path.join(dest, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        carried.append(rel)
    return carried


# ---------------------------------------------------------------------------------------------
# THE GATE. Only checks that already existed and that a proposal cannot edit.
# ---------------------------------------------------------------------------------------------

def gate(path: str = None, baseline: dict = None) -> dict:
    """Run every unauthorable check inside `path`. Returns a verdict with one row per check.

    Each check answers a different way the system can be broken, and the third is the one a test
    suite cannot see: a change that keeps every test green while quietly disconnecting a module from
    the wake. That is not hypothetical - it is the state this repo is in right now, with seven kernel
    modules orphaned and every test passing.
    """
    path = path or ROOT
    env = _pyenv(path)
    checks = []

    # 0 WHOSE CODE ARE WE ABOUT TO JUDGE. Asked FIRST, because every check below is worthless if the
    #   answer is wrong, and the wrong answer looks exactly like a pass.
    #
    #   The live tree and the candidate both contain a package called `aea` and a file called
    #   `test_golden.py`. Under Python's default path handling the first `aea` imported wins for the
    #   whole process - so a misconfigured PYTHONPATH or cwd yields a run where the CANDIDATE'S
    #   tests execute against the LIVE package and report a confident green. Verified here rather
    #   than assumed: the candidate must prove its own `aea` is the one that loaded.
    rc, out = _run([sys.executable, "-X", "utf8", "-c",
                    "import aea, sys; sys.stdout.write(aea.__file__)"], cwd=path, env=env)
    loaded = out.strip()
    own = rc == 0 and loaded.lower().startswith(os.path.abspath(path).lower())
    checks.append({"check": "the candidate's own code is what loaded", "pass": own,
                   "detail": loaded[-120:] if loaded else "no import"})
    if not own:
        return {"path": path, "checks": checks, "pass": False, "structure": None}

    # 1 EVERY MODULE IMPORTS. Cheapest possible proof that the tree is not broken.
    rc, out = _import_smoke(path, env)
    checks.append({"check": "every module imports", "pass": rc == 0, "detail": out[-200:]})

    # 2 THE FROZEN BEHAVIOURS. 31 of them, and two are deliberately frozen at a KNOWN-BAD value,
    #   so "fixing" the reader is supposed to break this file. That is the point of a frozen test.
    tpath = os.path.join(path, "aea", "lab", "tests", "test_golden.py")
    if os.path.exists(tpath):
        rc, out = _run([sys.executable, "-X", "utf8", tpath], cwd=path, env=env)
        m = re.search(r"all (\d+) frozen behaviours hold", out)
        n = int(m.group(1)) if m else 0
        ok = rc == 0 and n >= FROZEN_FLOOR
        checks.append({"check": "%d frozen behaviours" % FROZEN_FLOOR, "pass": ok, "detail": out.strip()[-200:]})
    else:
        checks.append({"check": "%d frozen behaviours" % FROZEN_FLOOR, "pass": False,
                       "detail": "the test file is missing from the candidate"})

    # 3 NO NEW ORPHANS. A change that disconnects a module from every entry point passes every test
    #   and makes the system smaller. Only a structural comparison catches it.
    rc, out = _run([sys.executable, "-X", "utf8", "-c", XRAY_COUNT], cwd=path, env=env)
    try:
        cur = json.loads(out.strip().splitlines()[-1])
    except Exception:
        cur = None
    if cur is None:
        checks.append({"check": "no new orphans", "pass": False,
                       "detail": "could not read the candidate's structure: %s" % out[-160:]})
    elif baseline:
        new = sorted(set(cur["orphans"]) - set(baseline["orphans"]))
        checks.append({"check": "no new orphans", "pass": not new,
                       "detail": ("newly unreachable: " + ", ".join(new)) if new
                                 else "%d orphans, unchanged or fewer" % len(cur["orphans"])})
    else:
        checks.append({"check": "no new orphans", "pass": True,
                       "detail": "no baseline given; recorded %d orphans" % len(cur["orphans"])})

    # 4 NO NEW IMPORT-TIME SIDE EFFECTS. A module that acts on being named cannot be safely scanned
    #   or tested, and two in this repo rewrote tracked files that way.
    if cur is not None and baseline:
        new = sorted(set(cur["effects"]) - set(baseline["effects"]))
        checks.append({"check": "no new import-time effects", "pass": not new,
                       "detail": ("new: " + ", ".join(new)) if new else "unchanged"})

    # 5 THE CANDIDATE CAN STILL THINK. One REAL model call, through the candidate's own energy.draw,
    #   graded on arithmetic it cannot negotiate with.
    #
    #   THIS CLOSES THE BLIND SPOT THE qa RUNG DECLARES ABOUT ITSELF. Checks 1-4 are static: they
    #   prove the tree imports, that frozen behaviours hold, and that nothing was disconnected.
    #   MEASURED 2026-07-29: a sabotage making `own_params()` return a fixed temperature on every
    #   call - which corrupts every request the entity makes - passed ALL of them and was rejected
    #   only by an unrelated orphan comparison. Everything under a live call (the ladder, the meter,
    #   the parameter resolution, the transport) was untested by a gate whose whole job is to say
    #   "this change is safe to become".
    #
    #   UNAVAILABLE IS NOT A PASS. With no network or no key this cannot be verified, and an
    #   unverifiable change must not be promoted into a running system. It is reported as its own
    #   state so a human sees "could not check" rather than "checked and fine" - law B1, fail closed,
    #   and the honesty law's rule that an absent value is a dash rather than a guess.
    rc, out = _run([sys.executable, "-X", "utf8", "-c", LIVE_DRAW], cwd=path, env=env, timeout=300)
    tail = (out or "").strip().splitlines()[-1:] or [""]
    verdict = tail[0].strip()
    live_ok = rc == 0 and verdict.startswith("LIVE_OK")
    checks.append({"check": "the candidate can still think",
                   "pass": live_ok,
                   "detail": verdict[:180] if verdict else "no output from the live draw"})

    return {"path": path, "checks": checks, "pass": all(c["pass"] for c in checks),
            "structure": cur}


# Run INSIDE the candidate, so it is the candidate's grid, ladder, meter and parameters under test.
# Deliberately tiny: this asks "can it still think at all", never "is it good".
LIVE_DRAW = (
    "import sys\n"
    "try:\n"
    "    from aea.energy import energy\n"
    # NO EXPLICIT mx/temp. Passing them wins over the published values, which means the probe would
    # bypass `own_params` - the exact code path it exists to exercise. MEASURED 2026-07-29: with
    # `temp=0` this check reported LIVE_OK against a candidate whose own_params was sabotaged to
    # return temperature 99 on every call. A live check that routes around the change is theatre.
    "    r = energy.draw('What is 17 * 23? Reply with only the number.', tier='solid',\n"
    "                    zone='private')\n"
    "    txt = (r.get('text') or '').replace(',', '').replace(' ', '')\n"
    "    if not r.get('ok'):\n"
    "        print('LIVE_UNAVAILABLE no rod answered: ' + str(r.get('tried'))[:120])\n"
    "    elif '391' in txt:\n"
    "        print('LIVE_OK %s/%s in %ss' % (r.get('plant'), r.get('model'), r.get('latency')))\n"
    "    else:\n"
    "        print('LIVE_WRONG %s/%s said %r' % (r.get('plant'), r.get('model'), txt[:40]))\n"
    "except Exception as e:\n"
    "    print('LIVE_UNAVAILABLE %s: %s' % (type(e).__name__, str(e)[:120]))\n"
)


XRAY_COUNT = (
    "import json,sys\n"
    "from aea.tooling import xray\n"
    "d = xray.build()\n"
    "print(json.dumps({'orphans': d['orphans'], 'effects': d['import_time_effects'],"
    " 'modules': d['counts']['modules'], 'wake': d['counts']['reachable_from_wake']}))\n"
)


def _import_smoke(path: str, env: dict):
    src = (
        "import importlib, pkgutil, io, contextlib, aea\n"
        "bad = []\n"
        "for pkg in ('kernel','mind','energy','memory','bench','io','organs','loop','server',"
        "'tooling','lab'):\n"
        "    try: p = importlib.import_module('aea.' + pkg)\n"
        "    except Exception as e: bad.append('aea.%s: %s' % (pkg, e)); continue\n"
        "    for m in pkgutil.iter_modules(p.__path__):\n"
        "        n = 'aea.%s.%s' % (pkg, m.name)\n"
        "        try:\n"
        "            with contextlib.redirect_stdout(io.StringIO()):\n"
        "                importlib.import_module(n)\n"
        "        except Exception as e: bad.append('%s: %s' % (n, str(e)[:70]))\n"
        "print('IMPORT FAILURES: %d' % len(bad))\n"
        "[print('  ' + b) for b in bad[:10]]\n"
        "raise SystemExit(1 if bad else 0)\n")
    p = subprocess.run([sys.executable, "-X", "utf8", "-c", src], cwd=path, env=env,
                       capture_output=True, text=True, timeout=900,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# ---------------------------------------------------------------------------------------------
# THE SHADOW. A whole second copy of the system, cheap, isolated, disposable.
# ---------------------------------------------------------------------------------------------

def open_shadow(name: str, ref: str = "HEAD") -> str:
    """A complete isolated checkout. Fast because git shares the object store rather than copying."""
    os.makedirs(SHADOWS, exist_ok=True)
    dest = os.path.join(SHADOWS, name)
    if os.path.exists(dest):
        close_shadow(name)
    rc, out = _run(["git", "worktree", "add", "--detach", dest, ref])
    if rc != 0:
        raise RuntimeError("could not open a shadow: %s" % out[-300:])
    return dest


def close_shadow(name: str):
    dest = os.path.join(SHADOWS, name)
    _run(["git", "worktree", "remove", "--force", dest])
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)
    _run(["git", "worktree", "prune"])


def restore_gate(dest: str) -> list:
    """Overwrite the shadow's copy of every gate file with the RUNNING SELF's copy.

    A BLOCKLIST IS A REFUSAL AT ONE WRITE-SITE. THIS IS AN INVARIANT.

    The first version of this module relied on `PROTECTED` alone, and it had a hole that was proven
    by running it: `aea/tooling/xray.py` was not on the list, and gate checks 3 and 4 ("no new
    orphans", "no new import-time effects") are computed by running xray INSIDE the candidate. Five
    lines replacing `build()` with a stub returning empty lists made both checks pass
    unconditionally - measured, not theorised:

        candidate replaced xray.py: ACCEPTED (not protected)
        gate checks 3+4 now read: {"orphans": [], "effects": [], "modules": 999, "wake": 999}

    That is the Darwin Godel Machine's documented Node 114 failure in miniature - an agent scoring
    perfect by deleting the markers its detector looked for - and it violated this file's own Rule 1
    while Rule 1 was written at the top of it.

    Extending the blocklist fixes the one file. Restoring fixes the CLASS: it does not matter whether
    a gate file was written by `apply_to`, carried in from the working tree, or already differed in
    the checkout - after this runs, the gate is the judge's code. SWE-bench's harness does exactly
    this, and does it both before and after each evaluation, for exactly this reason.

    Ground truth is the RUNNING self, not HEAD, because most of these files are not yet committed.
    """
    restored = []
    for rel in GATE_FILES:
        src = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(src):
            continue
        dst = os.path.join(dest, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        restored.append(rel)
    return restored


def protected(rel: str) -> bool:
    r = rel.replace("\\", "/")
    return any(r.startswith(p) or ("/" + p) in ("/" + r) for p in PROTECTED)


def apply_to(dest: str, changes: dict) -> list:
    """Write proposed file contents into a shadow. REFUSES anything in PROTECTED.

    `changes` is {repo_relative_path: new_full_text}. Whole files rather than patches, because a
    patch that half-applies is a third state nobody reasoned about.
    """
    written = []
    for rel, text in changes.items():
        if protected(rel):
            raise PermissionError(
                "%s is PROTECTED: a proposal may not edit the gate that judges it. A test the "
                "candidate rewrote is not evidence." % rel)
        p = os.path.join(dest, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        written.append(rel)
    return written


# ---------------------------------------------------------------------------------------------
# KNOWN-GOOD, AND THE PROPOSAL THAT NEVER PROMOTES ITSELF
# ---------------------------------------------------------------------------------------------

def mark_known_good(verdict: dict, note: str = "") -> dict:
    """Record the CURRENT commit as proven. Only a passing gate earns this."""
    if not verdict.get("pass"):
        raise ValueError("a failing gate cannot mark a known-good version")
    d = dirty()
    if d:
        # A KNOWN-GOOD MUST BE SOMETHING YOU CAN RETURN TO, AND YOU CANNOT RETURN TO A WORKING TREE.
        # The first run of this recorded HEAD's hash beside a verdict earned by a working tree that
        # differed from it by a day of edits. Reverting to that commit would have restored a version
        # the gate had never actually seen.
        raise ValueError(
            "%d tracked file(s) are modified but not committed, so there is no commit that holds "
            "the tree this verdict came from. Commit first - a known-good version has to be one you "
            "can actually return to. Modified: %s" % (len(d), ", ".join(d[:6])))
    doc = grid.load_json(KNOWN_GOOD, {"schema": "aea.known_good/1", "versions": []})
    doc["versions"].append({
        "commit": head(), "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "note": note, "checks": [c["check"] for c in verdict["checks"]],
        "structure": verdict.get("structure")})
    doc["versions"] = doc["versions"][-50:]
    doc["latest"] = doc["versions"][-1]["commit"]
    grid.atomic_save_json(KNOWN_GOOD, doc)
    return doc["versions"][-1]


def last_known_good() -> dict | None:
    doc = grid.load_json(KNOWN_GOOD, {"versions": []})
    return (doc.get("versions") or [None])[-1]


def propose(what: str, changes: dict, why: str, baseline: dict = None) -> dict:
    """Test a change to this system in a shadow and WRITE A PROPOSAL. It never promotes.

    THERE IS NO promote() IN THIS FILE AND THAT IS THE DESIGN. `self_modify_code` is pinned at
    ceiling 1 in the charter - a reviewable diff. The gap between "the tests passed" and "this is
    now what I am" is exactly where a human belongs, and the entrustment model the research surfaced
    says the same thing: autonomy is granted, never taken.
    """
    os.makedirs(PROPOSALS, exist_ok=True)
    pid = "prop_" + hashlib.sha1(
        (what + json.dumps(sorted(changes))).encode()).hexdigest()[:10]
    name = pid
    dest = open_shadow(name)
    try:
        # THE SHADOW MUST BE THE RUNNING SELF PLUS THE PROPOSAL - not HEAD plus the proposal.
        carried = _carry_worktree(dest, skip=set(changes))
        written = apply_to(dest, changes)
        # LAST, AFTER EVERYTHING ELSE HAS WRITTEN. Order is the whole guarantee: whatever the
        # candidate put in a gate file is overwritten by the judge's copy before a verdict is
        # computed from it.
        restored = restore_gate(dest)
        v = gate(dest, baseline=baseline or (last_known_good() or {}).get("structure"))
        rc, diff = _run(["git", "diff", "--stat"], cwd=dest)
        # THE FURTHEST RUNG THIS PROPOSAL REACHED, recorded so "how far did it get" is a fact rather
        # than an inference from a boolean. `qa` means the checks RAN; `qa-passed` means they passed.
        # Nothing here can ever write `prod`: that rung is a human's and this module cannot reach it.
        stage_reached = ("qa-passed" if v["pass"]
                         else "qa" if v.get("checks") else "dev")
        rec = {
            "id": pid, "what": what, "why": why,
            "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
            "from_commit": head(), "uncommitted_carried": len(carried),
            "gate_files_restored": restored,
            "stage_reached": stage_reached,
            "stage_blind_to": [b for s in STAGES if s["stage"] == "qa" for b in s["blind"]],
            "files": written, "diffstat": diff.strip()[-800:],
            "gate": v, "verdict": "PASSED THE GATE" if v["pass"] else "REJECTED BY THE GATE",
            "applied": False,
            "next_step": ("A human reviews this diff and applies it. self_modify_code is ceiling 1 "
                          "in the charter, so nothing here may apply itself."),
        }
        grid.atomic_save_json(os.path.join(PROPOSALS, pid + ".json"), rec, indent=1)
        return rec
    finally:
        close_shadow(name)


def proposals() -> list:
    if not os.path.isdir(PROPOSALS):
        return []
    out = []
    for f in sorted(os.listdir(PROPOSALS)):
        if f.endswith(".json"):
            out.append(grid.load_json(os.path.join(PROPOSALS, f), {}))
    return out


def render(v: dict) -> str:
    L = ["THE GATE - checks the candidate cannot author", "=" * 78]
    for c in v["checks"]:
        L.append("  [%s] %-30s %s" % ("PASS" if c["pass"] else "FAIL", c["check"],
                                      (c["detail"] or "").replace("\n", " ")[:70]))
    L.append("")
    L.append("VERDICT: %s" % ("PASSED" if v["pass"] else "REJECTED"))
    kg = last_known_good()
    L.append("last known-good: %s" % (kg["commit"][:10] + "  " + kg["at"] if kg else "none yet"))
    return "\n".join(L)


if __name__ == "__main__":
    if "--proposals" in sys.argv:
        ps = proposals()
        print("%d proposal(s)" % len(ps))
        for p in ps:
            print("  %-12s %-9s %-46s %s"
                  % (p.get("id"), "PASS" if p.get("gate", {}).get("pass") else "REJECT",
                     (p.get("what") or "")[:44], ",".join(p.get("files") or [])[:40]))
    elif "--try" in sys.argv:
        i = sys.argv.index("--try")
        rel = sys.argv[i + 1]
        src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        r = propose("dry run: re-apply %s unchanged" % rel, {rel: src},
                    why="proves the shadow, the gate and the proposal path end to end")
        print(json.dumps({k: r[k] for k in ("id", "verdict", "files")}, indent=1))
        print(render(r["gate"]))
    else:
        v = gate()
        print(render(v))
        if "--mark" in sys.argv and v["pass"]:
            g = mark_known_good(v, note=" ".join(sys.argv[sys.argv.index("--mark") + 1:]))
            print("\nmarked known-good: %s" % g["commit"][:12])
