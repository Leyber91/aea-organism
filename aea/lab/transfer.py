"""transfer.py - WHERE ELSE IS THIS TRUE? Asked mechanically, every run.

    python -m aea.lab.transfer            # report violations
    python -m aea.lab.transfer --controls # show each detector catching the case it must catch

THE FAILURE THIS EXISTS TO STOP, counted 2026-07-30. Five times in one day a lesson was learned,
written down CORRECTLY, and left unapplied in another module carrying the identical defect:

    hands.probe mapped 410 to "retired" and said "Gone is permanent"     energy.draw retried corpses
    ladder()'s docstring stated the ratios "5/6, 4/6"                    the code said `mx - 1`
    tiers.py says "WHAT THIS IS NOT. It is not a council."               council.py used it as one
    OWN_PARAMS' comment described the max_tokens=256 confound            the default stayed 256
    movecontrol learned "a verdict names its rod"                        council.py recorded no rod

None of these was a memory failure. Every one was written down, correctly, within arm's reach of the
defect - in the same file, twice. What was missing is TRANSFER: a lesson is learned at a SITE, and
nothing schedules the question "where else is this shape?".

WHY THE BATTERY DOES NOT COVER THIS, which is the whole design argument. `battery.py` asserts
BEHAVIOUR AT A SITE: given this input, this function returns that. It is the right tool and it
cannot see this class, because the defect is never in the site it was written for - it is in the
OTHER site, the one nobody thought to write a test for, and you cannot write a test for a place you
have not realised is relevant. This file asserts a PROPERTY ACROSS THE TREE instead: not "does
`ladder` use a ratio" but "does anything, anywhere, threshold on a count where a ratio is meant".

------------------------------------------------------------------------------------------------
EVERY DETECTOR SHIPS WITH A CASE IT MUST CATCH, and that is not a nicety here - it is the only
thing keeping this file from becoming the sixth instance of its own subject.

D18 recorded the law after six of ten defects turned out to be in code written to CHECK something:
*a detector that has never been shown a positive it must catch has not been tested, it has only been
run*, and *a guard that never fires and a world with nothing to guard against look identical from
outside*. A cross-tree checker is exactly the kind of thing that silently stops matching after a
refactor and reports a clean sheet forever.

So `verify_detectors()` runs FIRST and this module REFUSES TO REPORT if any detector fails to flag
its own control. A green run from here means "the detectors demonstrably still fire, and found
nothing" - never "nothing matched".

EXEMPTIONS ARE NAMED, NOT SILENT. A property that cannot go green is a property that gets ignored
(the corollary D18 paid for: a permanently failing check disables every check sharing its verdict).
Each exemption below carries the reason it is not a defect, so the list is a review surface rather
than a mute button.
"""
from __future__ import annotations

import ast
import os
import re
import sys

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TREE = os.path.join(str(grid.ROOT), "aea")

# Files that legitimately contain the shapes below, with the reason. Anything not listed is a
# finding. Keep this SHORT - a long exemption list is a property nobody is really enforcing.
EXEMPT = {
    # this file quotes every shape it hunts for, in its own controls and docstrings
    "lab/transfer.py": "the detector's own controls and prose",
    "lab/battery.py": "asserts these shapes deliberately, including synthetic bad cases",
    "lab/protocol.py": "a corpus of deliberately malformed cases",
}

# REVIEWED ONCE, THEN SILENT - per shape, per site, with the judgement recorded.
#
# A checker that re-asks a settled question every run is training its reader to skip it, and the
# answer to "is this use inside the stated limit?" is a JUDGEMENT a static check cannot make. So it
# gets made once, by a person, and written here. A NEW importer of a module that carries a warning
# still surfaces, which is the whole point: the question fires for cases nobody has ruled on yet.
ACK = {
    ("scope-violation", "io/speak.py"):
        "uses tiers for VOICE routing - exactly the job its organs were measured for; the warning "
        "is about using them as a council, which this does not",
    ("scope-violation", "lab/convbench.py"): "voice benchmarking, the organs' measured purpose",
    ("scope-violation", "lab/duet.py"): "voice benchmarking, the organs' measured purpose",
    ("scope-violation", "lab/earbench.py"): "voice benchmarking, the organs' measured purpose",
    ("scope-violation", "organs/converse.py"): "the conversation path the organs were measured on",
    ("scope-violation", "organs/talk.py"): "the conversation path the organs were measured on",
    ("scope-violation", "io/listen.py"): "voice routing, the organs' measured purpose",
    ("scope-violation", "lab/party.py"): "multi-voice work, the organs' measured purpose",
    ("scope-violation", "mind/background.py"):
        "thinking WHILE the mouth is busy, inside a live spoken turn - latency is the constraint "
        "there, so a latency-measured organ is exactly right. Not a council in any sense",
    ("scope-violation", "mind/council.py"):
        "only `tiers.LOCAL` remains, as the last-resort floor when every hosted plant is down - a "
        "rod dict, not a roster. The seats and the roster designer both draw from the ladder now",
    ("expiring-only-retry", "kernel/grid.py"):
        "the 429 bucket cools by design and SHOULD - a rate limit is genuinely temporary. Permanent "
        "deadness is owned one layer up by energy._retire, which reads the same store",
}


def _py_files() -> list:
    out = []
    for dp, dn, fns in os.walk(TREE):
        dn[:] = [d for d in dn if d not in ("__pycache__", "archive")]
        for fn in fns:
            if fn.endswith(".py"):
                p = os.path.join(dp, fn)
                out.append((os.path.relpath(p, TREE).replace("\\", "/"), p))
    return sorted(out)


def _src(path):
    try:
        return open(path, encoding="utf-8").read()
    except Exception:
        return ""


def _strip_prose(src: str) -> str:
    """Source with comments and string literals removed, so a detector cannot match its own prose.

    This repo comments its decisions at length, which means the words a shape is named after appear
    constantly in text ABOUT the shape. A text detector that reads those is guaranteed to confirm
    itself - the purest form of measuring the instrument."""
    out = re.sub(r"#[^\n]*", "", src)
    out = re.sub(r'"""(?:.|\n)*?"""', "", out)
    out = re.sub(r"'''(?:.|\n)*?'''", "", out)
    return out


def _line(src, i):
    try:
        return src.splitlines()[i - 1].strip()[:110]
    except Exception:
        return ""


# =================================================================================================
# THE DETECTORS. Each returns a list of (relpath, lineno, snippet, note).
# =================================================================================================

def d_count_threshold(rel, src, tree):
    """A threshold computed from a collection SIZE with an arithmetic offset.

    D24: `score >= mx - 1` where `mx = len(battery)` meant 5/6 while the battery had six probes and
    silently became 11/12 when it grew to twelve. Nobody raised the tier; the tier raised itself.
    A ratio survives the collection changing size; a count does not."""
    hits = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Compare):
            continue
        for side in [n.left] + list(n.comparators):
            if not isinstance(side, ast.BinOp) or not isinstance(side.op, (ast.Sub, ast.Add)):
                continue
            # len(...) on either operand, offset by a constant
            for operand in (side.left, side.right):
                is_len = (isinstance(operand, ast.Call) and isinstance(operand.func, ast.Name)
                          and operand.func.id == "len")
                looks_sized = isinstance(operand, ast.Name) and re.search(
                    r"^(mx|n|total|count|size|maxi?)$", operand.id)
                if not (is_len or looks_sized):
                    continue
                other = side.right if operand is side.left else side.left
                if not (isinstance(other, ast.Constant) and isinstance(other.value, (int, float))):
                    continue
                # AN INDEX BOUND IS NOT A THRESHOLD. `i != len(order) - 1` and
                # `stage < len(guide) - 1` address the LAST ELEMENT, which is what `len - 1` means
                # and always will; the collection changing size does not change the meaning. The
                # shape only bites when the offset gates a QUALITY - a score, a pass count, a
                # quorum - because there the constant silently encodes a ratio.
                txt = _line(src, side.lineno).lower()
                if not re.search(r"\b(score|passed|pass_|votes?|agree\w*|quorum|rating|grade|"
                                 r"correct|hits?|matches)\b", txt):
                    continue
                hits.append((rel, side.lineno, _line(src, side.lineno),
                             "a QUALITY gate offsets a collection size by a constant - it encodes "
                             "a ratio that silently retunes when the collection changes size"))
    return hits


def d_silent_default(rel, src, tree):
    """`except: return <empty>` - a failure and a real empty answer become the same value.

    The most expensive failure shape in this repo (D19/D21/D31): a NONE that means broken, a rest
    that means dead, a green that means unmeasured. `decide.py`'s first law is the counter - every
    refusal returns (value, why) - and it is exactly the discipline that does not travel."""
    hits = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.ExceptHandler):
            continue
        body = [b for b in n.body if not isinstance(b, ast.Pass)]
        if len(body) != 1 or not isinstance(body[0], ast.Return):
            continue
        v = body[0].value
        empty = (v is None
                 or (isinstance(v, ast.Constant) and v.value in (None, "", 0, False))
                 or (isinstance(v, (ast.Dict, ast.List, ast.Tuple, ast.Set)) and not getattr(v, "elts", getattr(v, "keys", []))))
        if empty:
            hits.append((rel, n.lineno, _line(src, n.lineno),
                         "swallows the error and returns an empty value - the caller cannot tell "
                         "'it failed' from 'the answer is empty'. Carry the reason."))
    return hits


def d_invented_ceiling(rel, src, tree):
    """A literal `max_tokens=<int>` - a ceiling we invented rather than the rod's own.

    D29: the provider bills neither tokens nor requests, so every ceiling below the rod's published
    window only truncates thinking and corrupts the measurement taken through it. Resolution is
    explicit-arg > published ceiling > omit the field."""
    hits = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        for kw in (n.keywords or []):
            if kw.arg in ("max_tokens", "mx") and isinstance(kw.value, ast.Constant) \
                    and isinstance(kw.value.value, int):
                hits.append((rel, kw.value.lineno, _line(src, kw.value.lineno),
                             f"{kw.arg}={kw.value.value} is a ceiling we chose - pass None and let "
                             f"the rod's published window decide, or name what the number buys"))
    return hits


def d_expiring_only(rel, src, tree):
    """A module with a cooldown/backoff and no way to say NEVER AGAIN.

    D22: `_cooling` expired by design so a rod "gets another chance" - right for a throttle, wrong
    for 410 Gone. Any retry policy whose window expires cannot express a permanent condition, so a
    system built only from cooldowns re-attempts every corpse it owns."""
    # `\bCOOL_\b` NEVER MATCHED: `_` is a word character, so there is no boundary between `COOL_`
    # and `AFTER`, and the detector silently matched nothing forever. Caught on this file's first
    # run by its own control - which is the entire argument for shipping controls (D18).
    #
    # AND IT READS CODE, NOT PROSE. The first version matched the WORD "cooldown" anywhere, so a
    # comment explaining someone else's cooldown counted as owning one - `rodprobe.py` and
    # `prosody.py` were both flagged for describing the concept. A checker that reads its own
    # documentation as evidence will always find what it is looking for.
    code = _strip_prose(src)
    has_cool = re.search(r"\b(COOL_\w*|COOLDOWN|BACKOFF|RETRY_AFTER|cooldown)\b", code)
    has_perm = re.search(r"\b(retire|tombstone|permanent|withdrawn|_retire|retired_at)\b", src, re.I)
    if has_cool and not has_perm:
        ln = src[:has_cool.start()].count("\n") + 1
        return [(rel, ln, _line(src, ln),
                 "defines a cooldown/backoff with no permanent branch - a condition that is "
                 "genuinely final will be retried forever")]
    return []


# ONLY EXPLICIT, STRONG PROHIBITIONS. The first version also matched "not for", "it is not" and
# every incidental negation in a docstring, which returned forty scope questions - and forty
# questions is zero questions, because nobody reads a list that long. A checker that cries wolf
# disables itself, which is D18's corollary applied to this file rather than by it.
_PROHIBIT = re.compile(
    r"(?:^|\n)\s*(?:#\s*)?((?:WHAT THIS IS NOT|DO NOT USE|NEVER USE|MUST NOT BE USED|"
    r"THIS IS NOT A |IT IS NOT A )[^\n]{0,120})")


def scope_warnings() -> dict:
    """Modules that state, in their own docstring, how they must NOT be used.

    D30: `tiers.py` says "WHAT THIS IS NOT. It is not a council." in capitals, and `council.py`
    seated its debaters from that table anyway. A warning at the DESTINATION is the direction nobody
    checks - the lesson did not fail to travel, it was already there and unread."""
    out = {}
    for rel, path in _py_files():
        src = _src(path)
        try:
            doc = ast.get_docstring(ast.parse(src)) or ""
        except Exception:
            doc = ""
        for m in _PROHIBIT.finditer(doc):
            out.setdefault(rel, []).append(m.group(1).strip()[:110])
    return out


def d_scope_violation(rel, src, tree, warnings=None):
    """A module importing another that warned it is not for this purpose.

    Reported for a HUMAN to judge: the check can see that a warning exists and that this module
    imports the warner, never whether the warning applies. Printed as a question, not a verdict -
    a checker that cannot be sure must say which of the two it is."""
    warnings = warnings if warnings is not None else scope_warnings()
    hits = []
    mods = {w.replace(".py", "").replace("/", "."): txts for w, txts in warnings.items()}
    for n in ast.walk(tree):
        names = []
        if isinstance(n, ast.ImportFrom):
            # BOTH HALVES. Collecting only `n.module` reads `from aea.mind import tiers` as the
            # package "aea.mind" and never sees `tiers` at all - so the one import shape this
            # detector exists to catch was the one it could not see. Its control said so.
            if n.module:
                names.append(n.module)
            names += [a.name for a in n.names]
        elif isinstance(n, ast.Import):
            names += [a.name for a in n.names]
        for full in names:
            tail = full.split(".")[-1]
            for mod, txts in mods.items():
                if mod.split(".")[-1] == tail and not rel.endswith(mod.replace(".", "/") + ".py"):
                    hits.append((rel, n.lineno, _line(src, n.lineno),
                                 f"imports {tail}, which states: {txts[0]!r} - does this use "
                                 f"fall inside that limit?"))
    return hits


# BLOCKING vs ADVISORY, and the split is deliberate.
#
# D18's corollary, paid for once already: *a permanently failing check disables every check that
# shares its verdict*. Style and safety must never share a line - one reports, the other blocks.
# `silent-default` and `invented-ceiling` match dozens of sites, many of them fine (a spoken reply
# SHOULD be short; a liveness ping SHOULD ask for 8 tokens). Letting those fail the run would train
# everyone to ignore the run. They report; the two high-confidence shapes block.
DETECTORS = [
    ("count-threshold", d_count_threshold, "D24 - growing the exam shrank the ladder", True,
     "def f(cap, battery):\n    mx = len(battery)\n    return [r for r in cap if r['score'] >= mx - 1]\n"),
    ("expiring-only-retry", d_expiring_only, "D22 - a cooldown cannot express 'never again'", True,
     "COOL_AFTER = 3\nCOOL_SECONDS = 900\n\ndef cooling(e):\n    return e['fails'] >= COOL_AFTER\n"),
    ("scope-violation", d_scope_violation, "D30 - a warning at the destination, unread", True,
     "from aea.mind import tiers\n\ndef seat():\n    return tiers.organ('reflex')\n"),
    ("silent-default", d_silent_default, "D19/D21 - a null indistinguishable from a real result", False,
     "def f(p):\n    try:\n        return open(p).read()\n    except Exception:\n        return {}\n"),
    ("invented-ceiling", d_invented_ceiling, "D29 - a limit that buys nothing only costs", False,
     "def f(c):\n    return c.call(model='m', messages=[], max_tokens=256)\n"),
]


def verify_detectors() -> list:
    """Show every detector the case it MUST catch. A detector that misses its control is BROKEN,
    and this module refuses to report until it is fixed - see the header. This is the difference
    between "found nothing" and "matched nothing", which are the same sentence from outside."""
    bad = []
    for name, fn, _why, _blk, control in DETECTORS:
        try:
            tree = ast.parse(control)
            kw = {}
            if fn is d_scope_violation:
                kw["warnings"] = {"mind/tiers.py": ["THIS IS NOT a council"]}
            got = fn("control.py", control, tree, **kw)
        except Exception as e:
            bad.append((name, f"RAISED {type(e).__name__}: {str(e)[:60]}"))
            continue
        if not got:
            bad.append((name, "did NOT flag its own positive control"))
    return bad


def run(verbose: bool = True) -> dict:
    broken = verify_detectors()
    if broken:
        if verbose:
            print("DETECTORS BROKEN - refusing to report, because a checker that cannot catch its")
            print("own control reports a clean sheet for the wrong reason (D18).\n")
            for n, why in broken:
                print(f"  {n}: {why}")
        return dict(ok=False, broken=broken, findings=[])

    warnings = scope_warnings()
    findings = []
    for rel, path in _py_files():
        if rel in EXEMPT:
            continue
        src = _src(path)
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for name, fn, _why, blocking, _c in DETECTORS:
            kw = {"warnings": warnings} if fn is d_scope_violation else {}
            for hit in fn(rel, src, tree, **kw):
                if (name, rel) in ACK:
                    continue                     # ruled on once, by a person, with the reason above
                findings.append(dict(shape=name, file=hit[0], line=hit[1], blocking=blocking,
                                     snippet=hit[2], note=hit[3]))

    if verbose:
        print("=" * 96)
        print("TRANSFER - where else is this true?")
        print("=" * 96)
        print(f"  {len(DETECTORS)} detectors, all verified against their own controls")
        print(f"  {len(_py_files())} modules scanned, {len(EXEMPT)} exempt by name\n")
        by = {}
        for f in findings:
            by.setdefault(f["shape"], []).append(f)
        for name, _fn, why, _blk, _c in DETECTORS:
            got = by.get(name, [])
            print(f"  {name:22s} {len(got):3d}   ({why})")
        for name, _fn, _why, _blk, _c in DETECTORS:
            got = by.get(name, [])
            if not got:
                continue
            print(f"\n--- {name} ({len(got)})")
            for f in got[:12]:
                print(f"  {f['file']}:{f['line']}")
                print(f"      {f['snippet']}")
                print(f"      -> {f['note']}")
            if len(got) > 12:
                print(f"  ... {len(got) - 12} more")
        blk = [f for f in findings if f.get("blocking")]
        print(f"\n  BLOCKING: {len(blk)}    advisory: {len(findings) - len(blk)}")
        print("  A green run means the detectors demonstrably still fire and found nothing.")
        print("  It never means 'nothing matched'.")
    return dict(ok=True, broken=[], findings=findings)


if __name__ == "__main__":
    if "--controls" in sys.argv[1:]:
        print("EVERY DETECTOR AGAINST THE CASE IT MUST CATCH:\n")
        for name, fn, why, _blk, control in DETECTORS:
            kw = {"warnings": {"mind/tiers.py": ["THIS IS NOT a council"]}} \
                if fn is d_scope_violation else {}
            got = fn("control.py", control, ast.parse(control), **kw)
            print(f"  {name:22s} {'CAUGHT' if got else 'MISSED  <-- BROKEN'}   {why}")
            for line in control.strip().splitlines():
                print(f"        {line}")
            print()
        sys.exit(0)
    r = run()
    # ADVISORY SHAPES DO NOT FAIL THE RUN. D18's corollary: a permanently failing
    # check disables every check that shares its verdict, so style and safety must
    # never share an exit code.
    sys.exit(0 if r["ok"] and not [f for f in r["findings"] if f.get("blocking")] else 1)
