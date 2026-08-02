"""perceive.py - THE RECEIPT FOR R4a. What the entity chose to look at, and whether that was a CHOICE.

    python -m aea.kernel.perceive            what it has been looking at, and how varied
    python -m aea.kernel.perceive --json     the same as JSON

WHY THIS EXISTS BEFORE THE CAPABILITY DOES, which is the whole point.

R1 sat at "open" for weeks with a working wire, because nothing wrote down the comparison it was
supposed to demonstrate. The wire worked; the receipt did not exist; and from outside, "the wire has
never fired" and "nobody is writing it down" look identical. That cost weeks and it was free to
avoid. R6 has the same hole today - its gate says a reflection is "used in a later decision" and no
artefact anywhere could show it.

So R4a's instrument is built FIRST, against a capability that is only half present, on purpose.

WHAT R4a CLAIMS, and it is deliberately narrower than the original R4:

    What the entity looks at NEXT is chosen by the previous tick, not fixed in advance.

The original rung bundled that with reaching the WORLD, and the world half is the one a council
refused three times. Perception becoming a choice does not require the network: choosing which of
sixteen state files to read, or which of four self-map topics, IS perception as a choice, over local
data, with the certified enum boundary already underneath it. R4b - perception reaching the world -
stays shut behind `dispatch`, and stays shut with a stated condition rather than a feeling.

WHAT A PERCEPTION RECEIPT HOLDS, and why each field is there:

    source      (tool, argument) - WHAT it looked at. The unit of a perceptual choice
    previous    what it looked at last time. Without this, "chose differently" is unanswerable
    differed    the claim itself, computed here rather than inferred later by a reader
    why         the wake's own stated reason, verbatim. A choice with no reason is a coin toss,
                and a coin toss satisfies a variety counter perfectly while demonstrating nothing
    decision    the decision's own tick, so a receipt joins to the decision that caused it

THE FAILURE THIS FIELD SET IS BUILT AGAINST. A gate that counts only distinct sources can be
satisfied by an entity cycling blindly through a list. Requiring a REASON, recorded at the moment of
choosing, is what separates choosing from rotating - and it is checkable, because the reason comes
from the wake's decision rather than from this module.
"""
from __future__ import annotations

import json
import os
import sys
import time

from aea.kernel import grid

STORE = "perception.jsonl"


def _path() -> str:
    """Honours AEA_PERCEPTION so a test never writes production. D48: a path bound at import cannot
    be sandboxed, so this is resolved at CALL time."""
    return os.environ.get("AEA_PERCEPTION") or os.path.join(grid.STATE, STORE)


def read(path: str = None) -> list:
    p = path or _path()
    if not os.path.exists(p):
        return []
    out = []
    for line in open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue                 # a corrupt line is not a perception; it is also not a lie
    return out


def record(tool: str, args: dict, why: str = "", decision: int = None, src: str = "wake") -> dict:
    """Write one perceptual choice, with what preceded it so `differed` is decided here.

    `src` FAILS CLOSED for the same reason `hands` does: a harness that looks at something is not
    the entity choosing to. Only rows written by the live loop may claim to be the entity's."""
    prev = None
    for r in reversed(read()):
        if r.get("src") == "wake":
            prev = r
            break
    source = [str(tool or ""), json.dumps(args or {}, sort_keys=True)]
    row = dict(at=time.time(),
               at_iso=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
               source=source,
               previous=(prev or {}).get("source"),
               differed=bool(prev and prev.get("source") != source),
               why=str(why or "")[:200],
               decision=decision,
               src=src)
    grid.append_jsonl(_path(), row)
    return row


def verdict(rows=None) -> dict:
    """How much of what the entity looked at was actually CHOSEN.

    Only rows the live loop wrote count, and only ones carrying a reason. A choice with no stated
    reason is indistinguishable from a rotation, and this rung is about the difference."""
    rows = read() if rows is None else rows
    mine = [r for r in rows if r.get("src") == "wake"]
    reasoned = [r for r in mine if (r.get("why") or "").strip()]
    changed = [r for r in reasoned if r.get("differed")]
    sources = {tuple(r.get("source") or []) for r in mine}
    return dict(total=len(rows), by_entity=len(mine), with_reason=len(reasoned),
                changed_with_reason=len(changed), distinct_sources=len(sources),
                claim="a perceptual choice is one where the entity looked at something other than "
                      "last time AND said why. Rotation satisfies a counter; it does not satisfy "
                      "this.")


if __name__ == "__main__":
    v = verdict()
    if "--json" in sys.argv:
        print(json.dumps(v, indent=1))
        sys.exit(0)
    print("PERCEPTION - what the entity chose to look at")
    print("=" * 92)
    for k in ("total", "by_entity", "with_reason", "changed_with_reason", "distinct_sources"):
        print("  %-22s %s" % (k, v[k]))
    print()
    print("  %s" % v["claim"])
    print()
    for r in read()[-8:]:
        print("   %s  %-34s %s%s" % (str(r.get("at_iso"))[:19],
                                     " ".join(r.get("source") or [])[:34],
                                     "CHANGED " if r.get("differed") else "same    ",
                                     str(r.get("why"))[:44]))
