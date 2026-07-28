"""rescore.py - READ A STORED RUN AGAIN, WITH A DIFFERENT READER, FOR NOTHING.

WHY THIS EXISTS. Eighteen instrument defects have been found in this lab and several of them were in
the READ: a 320-character window, a dialect that returns an addend, a fallback that manufactures a
value out of a refusal. Each one was discovered after the calls were spent, and each one made the
affected runs unusable, because scoring was fused to generation - the only way to apply a corrected
reader was to buy the whole experiment again.

That is the wrong shape and every serious evaluation framework fixes it the same way: generation and
scoring are separate stages over an immutable archive of what the model actually said. A score is not
a fact about the run. It is a HYPOTHESIS about the run, and a hypothesis you cannot revise is a
hypothesis you are stuck with.

THE RULE, AND IT IS THE ONLY ONE HERE: A SCORE SET IS APPENDED, NEVER OVERWRITTEN. The original
reading stays exactly where it was, with its own id, forever. `rescore` adds a new one beside it and
reports the DIFF between them - and that diff is the size of the measurement bug, which is a number
this lab has never been able to see.

This only works on runs whose rows store the full reply text. Runs that stored `chars` and no text
cannot be re-read and are listed as such rather than silently skipped.

  python -m aea.lab.rescore                             what is re-scorable
  python -m aea.lab.rescore x24_the_store_and_the_door  re-read the newest run with every reader
"""
from __future__ import annotations

import hashlib
import os
import re
import sys

from aea.kernel import grid

# --- THE READERS. Each is a named, fingerprinted function over one reply. Adding one is additive:
# ---  no existing score set changes, and the new one appears beside them.

_ANCHOR = re.compile(r"(?im)^\s*ANSWER:\s*(-?\d{1,9})\s*$")
_LAST = re.compile(r"-?\d+")
_STATE = re.compile(r"(?im)^\s*STATE:\s*value\s*=\s*(-?\d{1,9})")


def _anchored(text):
    m = _ANCHOR.findall(text or "")
    return int(m[-1]) if m else None


def _last_int(text):
    n = _LAST.findall((text or "").replace(",", ""))
    return int(n[-1]) if n else None


def _last_int_no_state(text):
    """The last integer, ignoring a trailing STATE or NOTE block. The naive last-number read took
    `step=1` as the value and scored five rods at 0.00 in x23b; this is that lesson as a reader."""
    head = re.split(r"(?im)^\s*(?:STATE|NOTE):", text or "")[0]
    return _last_int(head)


def _stated_declining(text):
    """None when the reply declines. Declining and being wrong are different behaviours and the
    chain currently cannot tell them apart, because it substitutes the previous value."""
    t = (text or "").lower()
    if any(p in t for p in ("i cannot", "i can't", "unable to determine", "not enough information")):
        return None
    return _last_int_no_state(text)


READERS = {
    "anchored": _anchored,
    "last_int": _last_int,
    "last_int_no_state": _last_int_no_state,
    "stated_declining": _stated_declining,
    "state_line": lambda t: (lambda m: int(m[-1]) if m else None)(_STATE.findall(t or "")),
}


def reader_id(name):
    """The fingerprint stored with a score set. Change a reader's code and this changes, so two
    score sets with different ids are never confused for the same reading."""
    import inspect
    try:
        src = inspect.getsource(READERS[name])
    except (OSError, TypeError):
        src = repr(READERS[name])
    return "%s:%s" % (name, hashlib.sha1(src.encode()).hexdigest()[:8])


# --- THE ARCHIVE ---------------------------------------------------------------------------------

def runs_dir(experiment):
    return os.path.join(grid.STATE, "lab", "runs", experiment)


def newest(experiment):
    d = runs_dir(experiment)
    if not os.path.isdir(d):
        return None
    fs = sorted(f for f in os.listdir(d) if f.endswith(".json"))
    return os.path.join(d, fs[-1]) if fs else None


def steps_of(doc):
    """Every stored step that carries its reply text, with enough context to re-score it."""
    out = []
    for row in doc.get("rows", []):
        for rec in row.get("records", []) or []:
            for s in rec.get("trace", []):
                if s.get("ok") and s.get("text") is not None:
                    out.append((row, rec, s))
    return out


def rescorable(experiment):
    p = newest(experiment)
    if not p:
        return None
    doc = grid.load_json(p, None)
    if not doc:
        return None
    n = len(steps_of(doc))
    return {"experiment": experiment, "path": p, "run_id": doc.get("run_id"),
            "design_id": doc.get("design_id"), "steps_with_text": n,
            "rescorable": n > 0}


def rescore(experiment, readers=None, *, write=True):
    """Read every stored step again with each named reader. Appends; never overwrites."""
    p = newest(experiment)
    if not p:
        raise FileNotFoundError("no stored run for %s" % experiment)
    doc = grid.load_json(p, None)
    steps = steps_of(doc)
    if not steps:
        return {"experiment": experiment, "run_id": doc.get("run_id"), "refused":
                "no stored reply text - this run was written before the text was archived and "
                "cannot be re-read. The calls would have to be bought again."}

    names = list(readers or READERS)
    sets = {}
    for name in names:
        fn = READERS[name]
        hits = agrees = parsed = 0
        by_cell = {}
        for row, rec, s in steps:
            v = fn(s.get("text"))
            k = "%s|%s" % (row.get("form"), row.get("rod"))
            c = by_cell.setdefault(k, {"parsed": 0, "hit": 0, "of": 0})
            c["of"] += 1
            if v is not None:
                parsed += 1
                c["parsed"] += 1
                if v == s.get("truth"):
                    hits += 1
                    c["hit"] += 1
            if v == s.get("value"):
                agrees += 1
        sets[reader_id(name)] = {
            "reader": name, "steps": len(steps), "parsed": parsed, "hits": hits,
            "parse_rate": round(parsed / len(steps), 4),
            "hit_rate_of_parsed": round(hits / parsed, 4) if parsed else None,
            # THE NUMBER THIS FILE EXISTS FOR: how often this reader and the reader that scored the
            # run live disagree about what the model said.
            "agrees_with_original": round(agrees / len(steps), 4),
            "by_cell": by_cell}

    out = {"experiment": experiment, "run_id": doc.get("run_id"), "design_id": doc.get("design_id"),
           "source": os.path.relpath(p, grid.STATE).replace("\\", "/"),
           "steps_rescored": len(steps), "score_sets": sets}
    if write:
        # APPEND. The original document is not touched; the score sets live beside it under their
        # own key, keyed by reader fingerprint, and re-running adds rather than replaces.
        doc.setdefault("score_sets", {}).update(sets)
        grid.atomic_save_json(p, doc)
    return out


def render(out):
    if out.get("refused"):
        return "REFUSED %s: %s" % (out["experiment"], out["refused"])
    L = ["%s  run %s  design %s" % (out["experiment"], out["run_id"], out["design_id"]),
         "%d stored steps re-read at zero token cost" % out["steps_rescored"], "",
         "%-24s %-8s %-10s %-12s %s" % ("READER", "PARSED", "HIT/PARSED", "AGREES-ORIG", "ID")]
    for rid, s in out["score_sets"].items():
        L.append("%-24s %-8.3f %-10s %-12.3f %s"
                 % (s["reader"], s["parse_rate"],
                    "%.3f" % s["hit_rate_of_parsed"] if s["hit_rate_of_parsed"] is not None else "-",
                    s["agrees_with_original"], rid.split(":")[1]))
    worst = min((s["agrees_with_original"], s["reader"]) for s in out["score_sets"].values())
    L.append("")
    L.append("The spread between readers on IDENTICAL generations is the instrument's own error "
             "bar. Lowest agreement with the live reading: %s at %.3f." % (worst[1], worst[0]))
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(render(rescore(sys.argv[1])))
    else:
        d = os.path.join(grid.STATE, "lab", "runs")
        print("readers: %s\n" % ", ".join(READERS))
        print("%-38s %-10s %s" % ("EXPERIMENT", "STEPS", "RE-SCORABLE"))
        for e in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            r = rescorable(e)
            if r:
                print("%-38s %-10d %s" % (e[:37], r["steps_with_text"],
                                          "yes" if r["rescorable"] else
                                          "no - stored before replies were archived"))
