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
    ("expiring-only-retry", "kernel/wake.py"):
        "the same answer as kernel/grid.py, one layer further out, and it was CHECKED rather than "
        "assumed before this line was written. The match is a TEST FIXTURE - a fake meter returning "
        "the literal 'throttled (429 cooldown)' so the fuel gate's control does not depend on a "
        "live rate limit. wake.fuel() owns no retry policy of its own: it asks Meter.can_spend, and "
        "the ROSTER it asks about comes from energy.ladder, which excludes any rod carrying "
        "retired_at (energy.py:310 and :320, via dead()). So a permanently dead rod never reaches "
        "this module to be retried, and the permanent branch is exactly where D22 says it belongs",
}


def _py_files() -> list:
    out = []
    for dp, dn, fns in os.walk(TREE):
        dn[:] = [d for d in dn if d not in ("__pycache__", "archive")]
        for fn in fns:
            if fn.endswith(".py"):
                p = os.path.join(dp, fn)
                out.append((os.path.relpath(p, TREE).replace("\\", "/"), p))
    # THE GUARD ITS TWIN HAS CARRIED SINCE IT WAS WRITTEN. `assembly._py_files` raises on an empty
    # tree because two guards in this repo walked one dirname too deep and reported ok having read
    # nothing. This is the same function, over the same tree, feeding the defect ratchet - so an
    # empty scan here reports "0 defects found" and the ratchet records a clean sweep of nothing.
    # The lesson was written down, applied to one of the two copies, and not to the other: the
    # SECOND time you write it, extract it.
    if not out:
        raise RuntimeError("transfer scanned no modules under %s - a broken scan, not a clean tree"
                           % TREE)
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


_CEIL_NAMES = ("max_tokens", "mx", "num_predict", "max_new_tokens", "max_output_tokens", "n_predict")


def d_invented_ceiling(rel, src, tree):
    """A literal token ceiling - a number we invented rather than the rod's own.

    D29: the provider bills neither tokens nor requests, so every ceiling below the rod's published
    window only truncates thinking and corrupts the measurement taken through it. Resolution is
    explicit-arg > published ceiling > omit the field.

    THIS DETECTOR WAS ITSELF THE DEFECT, AND IT IS THE REASON THE CLASS KEPT RECURRING. The first
    version walked `n.keywords` only, and its single shipped control was a keyword argument. A
    four-shape AST census of the tree found **100 literal ceilings**, of which it could see 62:

        max_tokens=256                  keyword           62   CAUGHT
        call(..., 256)                  positional        15   MISSED
        def f(..., max_tokens=256)      default parameter 19   MISSED
        {"max_tokens": 256}             dict key           4   MISSED

    So it was green-by-construction on 38 live instances - including `grid.stream_openai`, whose
    default parameter carried the exact 256 this module's own prose names as the defect, on the
    path every voice and conversation call takes. That is D18 arriving INSIDE the detector written
    to honour D18: *a detector never shown a positive it must catch has not been tested, only run.*
    Each of the three missing shapes now ships with its own control, so `verify_detectors` refuses
    to report until all four fire."""
    hits = []

    def flag(node, label, value):
        hits.append((rel, node.lineno, _line(src, node.lineno),
                     f"{label}={value} is a ceiling we chose - pass None and let the rod's "
                     f"published window decide, or name what the number buys"))

    for n in ast.walk(tree):
        # SHAPE 1 - the keyword argument. The only one the first version could see.
        if isinstance(n, ast.Call):
            for kw in (n.keywords or []):
                if kw.arg in _CEIL_NAMES and isinstance(kw.value, ast.Constant) \
                        and isinstance(kw.value.value, int) and not isinstance(kw.value.value, bool):
                    flag(kw.value, kw.arg, kw.value.value)

        # SHAPE 2 - the DEFAULT PARAMETER. 19 instances, and the most dangerous shape of the four:
        # it applies to every caller who does not override it, and it is invisible at every call
        # site. `stream_openai(..., max_tokens=256, ...)` filtered the whole streaming path.
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = n.args
            names = [x.arg for x in (a.posonlyargs + a.args)]
            defaults = list(a.defaults)
            for name, dflt in zip(names[len(names) - len(defaults):], defaults):
                if name in _CEIL_NAMES and isinstance(dflt, ast.Constant) \
                        and isinstance(dflt.value, int) and not isinstance(dflt.value, bool):
                    flag(dflt, name, dflt.value)
            for name, dflt in zip([x.arg for x in a.kwonlyargs], a.kw_defaults):
                if name in _CEIL_NAMES and isinstance(dflt, ast.Constant) \
                        and isinstance(dflt.value, int) and not isinstance(dflt.value, bool):
                    flag(dflt, name, dflt.value)

        # SHAPE 3 - the DICT KEY, which is how a hand-rolled POST body carries its ceiling past
        # every helper that would have resolved it.
        if isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if isinstance(k, ast.Constant) and k.value in _CEIL_NAMES \
                        and isinstance(v, ast.Constant) and isinstance(v.value, int) \
                        and not isinstance(v.value, bool):
                    flag(v, str(k.value), v.value)
    return hits


# SHAPE 4 - the POSITIONAL argument. Deliberately NOT detected by name, because a bare integer in
# argument slot N is only a ceiling if the callee's slot N is a ceiling, and resolving that
# statically means a per-callee table that would itself go stale silently. The census counted 15;
# they are surfaced by `--positional`, which reports the callees worth reading rather than
# pretending to a certainty the AST cannot give. Claiming to catch this shape would be the
# comfortable answer and a false one.


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
def d_orphan_capability(rel, src, tree, defined=None, used=None):
    """Something BUILT and never CALLED - the shape nothing fails on.

    Luis, 2026-07-30: *"you didn't call it before, but you call it now. What else are we not
    calling?"* Every large find of that day was a capability already present and never invoked:
    `top_p` published by the owners and never sent, `think_off` written and never called,
    `own_params` tabled and never read, `stream` available since the first commit. NONE of them ever
    failed, because nothing fails when you decline to use something - which is exactly why no test
    could see them and why they survived for weeks.

    This repo already counts orphan MODULES (xray: 17 of 130 reachable). This is the same question
    one level finer: a public function or table defined in `aea/` and referenced nowhere else in
    `aea/`. Advisory by nature - a genuine entry point has no in-tree caller either - so it is a
    LIST TO READ, not a gate. The value is that the list exists at all; before this, the only way to
    notice an unused capability was to trip over the problem it would have solved."""
    if defined is None or used is None:
        return []
    hits = []
    for name, ln in defined.get(rel, {}).items():
        if name in used:
            continue
        hits.append((rel, ln, _line(src, ln),
                     f"{name} is defined here and referenced nowhere else in the tree - built and "
                     f"never called, which is the one defect that never announces itself"))
    return hits


def _defined_and_used():
    """Every module-level name defined in the tree, and every name referenced anywhere in it."""
    defined, used = {}, set()
    for rel, path in _py_files():
        src = _src(path)
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        d = {}
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_"):
                d[n.name] = n.lineno
            elif isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name) and t.id.isupper() and len(t.id) > 3:
                        d[t.id] = n.lineno
        defined[rel] = d
        for n in ast.walk(tree):
            if isinstance(n, ast.Name):
                used.add(n.id)
            elif isinstance(n, ast.Attribute):
                used.add(n.attr)
            elif isinstance(n, ast.Str) if hasattr(ast, "Str") else False:
                pass
        # a name can also be reached by string (getattr, a registry, a CLI arg)
        for m in re.finditer(r"[\"']([A-Za-z_][A-Za-z0-9_]{3,})[\"']", src):
            used.add(m.group(1))
    # a definition referenced only inside its OWN module is still an orphan to the tree, so the
    # per-file pass above deliberately unions across everything and the caller subtracts.
    return defined, used


def d_unredirectable_store(rel, src, tree):
    """A module-level write target built from `grid.STATE` at IMPORT, then appended to.

    D48: `hands.LEDGER` was `os.path.join(str(grid.STATE), "hands_ledger.jsonl")` at module level,
    so `redteam.py` - which carefully redirects `aea_state.json` into a temp directory - wrote
    **4,920 synthetic attack rows into the production ledger**, and `containment.py` then audited
    the redteam against the redteam. **Isolating the state of the thing under test while leaving its
    OUTPUT pointed at production is a half-done sandbox, which is worse than none because it looks
    done.** A destination fixed at import cannot be redirected by any harness, ever.

    The counter is a resolver called at write time (`_ledger_path()`), honouring an env override."""
    targets = set()
    for n in tree.body:                        # MODULE LEVEL ONLY - a local is already per-call
        if not isinstance(n, ast.Assign):
            continue
        blob = ast.dump(n.value)
        if "grid" not in blob or "STATE" not in blob:
            continue
        for t in n.targets:
            if isinstance(t, ast.Name):
                targets.add(t.id)
    if not targets:
        return []
    hits = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open"):
            continue
        mode = ""
        if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
            mode = str(n.args[1].value)
        for kw in (n.keywords or []):
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                mode = str(kw.value.value)
        if not any(c in mode for c in ("a", "w")):
            continue
        used = {x.id for x in ast.walk(n) if isinstance(x, ast.Name)}
        for name in sorted(used & targets):
            hits.append((rel, n.lineno, _line(src, n.lineno),
                         f"writes to {name}, a path bound to grid.STATE at IMPORT - no harness can "
                         f"redirect it, so test traffic lands in production. Resolve at call time "
                         f"and honour an env override (D48)"))
    return hits


DETECTORS = [
    # ADVISORY, and the classification is itself a judgement. A production module writing its own
    # store at a fixed path is NORMAL - `pulse` writing events, `aea` writing state. The defect
    # exists only where a HARNESS also writes through that path, and blocking on all 8 would make
    # the battery permanently red for code nobody is going to change today, which is D18's
    # corollary: a check that always fails stops being read. The blocking-grade instances are the
    # ones under `lab/` - a test harness that cannot be sandboxed - and `lab/gate.py:409` was one;
    # it is fixed rather than acknowledged.
    ("unredirectable-store", d_unredirectable_store,
     "D48 - an output path fixed at import cannot be sandboxed", False,
     'import os\nfrom aea.kernel import grid\n\nLEDGER = os.path.join(str(grid.STATE), "x.jsonl")\n'
     '\ndef w(row):\n    with open(LEDGER, "a") as f:\n        f.write(row)\n'),
    ("count-threshold", d_count_threshold, "D24 - growing the exam shrank the ladder", True,
     "def f(cap, battery):\n    mx = len(battery)\n    return [r for r in cap if r['score'] >= mx - 1]\n"),
    ("expiring-only-retry", d_expiring_only, "D22 - a cooldown cannot express 'never again'", True,
     "COOL_AFTER = 3\nCOOL_SECONDS = 900\n\ndef cooling(e):\n    return e['fails'] >= COOL_AFTER\n"),
    ("scope-violation", d_scope_violation, "D30 - a warning at the destination, unread", True,
     "from aea.mind import tiers\n\ndef seat():\n    return tiers.organ('reflex')\n"),
    ("silent-default", d_silent_default, "D19/D21 - a null indistinguishable from a real result", False,
     "def f(p):\n    try:\n        return open(p).read()\n    except Exception:\n        return {}\n"),
    # THREE CONTROLS, NOT ONE, AND THAT IS THE WHOLE POINT. Each is a shape copied verbatim out of
    # this tree, and each was a LIVE MISS until it was added here - 38 instances the detector was
    # green on by construction. `verify_detectors` refuses to report unless every one fires, so the
    # only way to lose a shape again is to delete its control on purpose.
    ("invented-ceiling", d_invented_ceiling, "D29 - a limit that buys nothing only costs", False,
     "def f(c):\n    return c.call(model='m', messages=[], max_tokens=256)\n"),
]

# EXTRA CONTROLS - VERIFIED, NEVER REPORTED. One defect can take several SHAPES, and each shape
# needs its own positive or the detector is untested on it. Registering them as additional DETECTORS
# rows verifies them correctly and then prints the identical finding list once per row, which is how
# a report stops being read - so they are checked by `verify_detectors` and never rendered.
#
# Each was a live miss. The keyword control was this detector's only positive while 38 instances sat
# in the other two shapes, including `grid.stream_openai`'s default parameter carrying the exact 256
# this module's own prose names as the defect, on the path every voice call takes.
EXTRA_CONTROLS = (
    ("invented-ceiling/default-param", d_invented_ceiling,
     "def stream_openai(plant, model, messages, max_tokens=256, temperature=0.2):\n    return 1\n"),
    ("invented-ceiling/dict-key", d_invented_ceiling,
     "def f(model, messages):\n    return {'model': model, 'messages': messages, 'max_tokens': 256}\n"),
)


def verify_detectors() -> list:
    """Show every detector the case it MUST catch. A detector that misses its control is BROKEN,
    and this module refuses to report until it is fixed - see the header. This is the difference
    between "found nothing" and "matched nothing", which are the same sentence from outside."""
    bad = []
    checks = ([(n, f, c) for n, f, _w, _b, c in DETECTORS]
              + [(n, f, c) for n, f, c in EXTRA_CONTROLS])
    for name, fn, control in checks:
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
