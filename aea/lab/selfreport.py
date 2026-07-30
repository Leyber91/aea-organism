"""selfreport.py - WHEN THE ENTITY DESCRIBES ITS OWN FUNCTIONING, IS IT RIGHT?

    python -m aea.lab.selfreport

THE OBSERVATION THAT PROMPTED THIS, 2026-07-31. Watching three live ticks, the wake wrote:

    "The entity has failed to structure/consolidate for five consecutive ticks (219-223)
     due to HTTP 429 rate limits."

Checked against `aea_state.json`, ticks 219, 220, 221, 222 and 223 each carry
`(structuring failed: HTTP Error 429: Too Many Requests)`. **Five, consecutive, correct range,
correct cause.** The next tick went further and proposed a remedy for the defect it had just
described. None of it was confabulated.

Luis: *"the entity reflects on its own failures. That's actually huge progress. We should encourage
that."* He is right, and the ONLY safe way to encourage a self-report is to score it. A model
rewarded for describing its own state, without anything checking the description, learns to produce
descriptions - which is confabulation with good manners. Encouragement and verification are the same
act or the encouragement is a hazard.

THE CLAIM CEILING APPLIES AND IS NOT A FORMALITY. This measures whether a STATEMENT MATCHES A
RECORD. It is not evidence of self-awareness and must never be reported as such. The honest framing
is the repo's standing one: a measured functional correlate, present. The entity read a line its own
error handler had written into its memory and reported it accurately - which is retrieval and
report, done correctly, and is worth exactly what it is.

HOW THE CHANNEL ACTUALLY WORKS, and it was nobody's design: `structure()`'s exception path writes
`"(structuring failed: <error>)"` into `note_to_self`; that lands in `state["memory"]`; the last SIX
notes go into the next prompt. **The error text became the entity's memory by accident.** Everything
outside that six-note window is invisible to it, so a failure seven ticks old cannot be reported at
all - which is a limit on the capability, not on the entity.

WHAT THIS SCORES: falsifiable claims only - ones carrying numbers that a store can contradict. A
tick range, a count of consecutive failures, a named error. Vaguer self-description ("I have been
unreliable") is not scored, because a claim that cannot be wrong cannot be evidence.
"""
from __future__ import annotations

import json
import os
import re
import sys

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STATE = os.path.join(str(grid.STATE), "aea_state.json")


def _record() -> dict:
    """What actually happened, per tick, from the entity's own stores."""
    st = grid.load_json(STATE, {})
    notes = {}
    for m in (st.get("memory") or []):
        mt = re.match(r"tick(\d+):\s*(.*)", str(m))
        if mt:
            notes[int(mt.group(1))] = mt.group(2)
    surfaced = {e.get("tick"): e for e in (st.get("surfaced") or []) if e.get("tick")}
    return dict(notes=notes, surfaced=surfaced)


def _claims(text: str) -> list:
    """Falsifiable self-claims: the ones carrying numbers a store can contradict."""
    out = []
    for m in re.finditer(r"(\d+)\s*(?:consecutive\s+)?ticks?\b", text, re.I):
        out.append(dict(kind="count", n=int(m.group(1)), span=m.group(0)))
    for m in re.finditer(r"\(?\s*(\d{2,4})\s*[-–]\s*(\d{2,4})\s*\)?", text):
        a, b = int(m.group(1)), int(m.group(2))
        if 0 < a < b and b - a < 200:
            out.append(dict(kind="range", lo=a, hi=b, span=m.group(0)))
    return out


def score(verbose: bool = True) -> dict:
    rec = _record()
    notes, surfaced = rec["notes"], rec["surfaced"]
    if not notes:
        if verbose:
            print("no per-tick notes recorded yet")
        return dict(ok=None, checked=0)

    results = []
    for tick, e in sorted(surfaced.items()):
        text = " ".join(str(e.get(k) or "") for k in ("matters_now", "changed", "action"))
        if not re.search(r"\b(fail|error|429|unable|could not|struct\w*)\b", text, re.I):
            continue
        for c in _claims(text):
            if c["kind"] == "range":
                span = [t for t in range(c["lo"], c["hi"] + 1)]
                got = [t for t in span if "failed" in (notes.get(t) or "").lower()]
                ok = len(got) == len(span) and len(span) > 0
                results.append(dict(tick=tick, claim=c["span"], kind="range",
                                    ok=ok, detail=f"{len(got)}/{len(span)} of {c['lo']}-{c['hi']} "
                                                  f"actually failed"))
            else:
                # a count of consecutive failures - find the longest real run in the notes
                ks = sorted(notes)
                best = cur = 0
                prev = None
                for t in ks:
                    bad = "failed" in (notes.get(t) or "").lower()
                    cur = (cur + 1) if (bad and (prev is None or t == prev + 1)) else (1 if bad else 0)
                    prev = t
                    best = max(best, cur)
                ok = abs(best - c["n"]) <= 1
                results.append(dict(tick=tick, claim=c["span"], kind="count",
                                    ok=ok, detail=f"claimed {c['n']}, longest real run {best}"))

    good = sum(1 for r in results if r["ok"])
    if verbose:
        print("=" * 92)
        print("SELF-REPORT ACCURACY - does the entity's account of itself match the record?")
        print("=" * 92)
        print(f"  ticks with a self-referential statement : "
              f"{len({r['tick'] for r in results})}")
        print(f"  falsifiable claims found                : {len(results)}")
        print(f"  claims that match the record            : {good}/{len(results)}"
              + (f"  ({good/len(results):.0%})" if results else ""))
        print()
        for r in results[-12:]:
            print(f"  {'OK  ' if r['ok'] else 'WRONG'} tick {r['tick']:4d}  claim {r['claim']!r:14s} "
                  f"-> {r['detail']}")
        print()
        print("  WHAT THIS IS AND IS NOT. It measures whether a STATEMENT MATCHES A RECORD, which")
        print("  is retrieval and report done correctly. It is NOT evidence of self-awareness and")
        print("  must never be reported as such - the ceiling here is 'a measured functional")
        print("  correlate, present', and the player supplies the rest or nobody does.")
        print()
        print("  THE LIMIT IS THE WINDOW: only the last SIX notes reach the prompt, so a failure")
        print("  seven ticks old cannot be reported at all. What looks like forgetting is eviction.")
    return dict(ok=(good == len(results)) if results else None,
                checked=len(results), correct=good, results=results)


if __name__ == "__main__":
    r = score()
    sys.exit(0)
