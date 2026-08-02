"""sources.py - WHERE THE NUMBERS COME FROM. Every read of durable state, in one place.

An absent store returns the default and the page renders a dash. That is the honesty law's smallest
unit: a value that is not there is shown as not there, and this module is the only thing entitled to
decide what "not there" looks like.
"""
from __future__ import annotations

import json
import os
import sys

from aea.kernel import grid

OUT = os.path.join(str(grid.ROOT), "docs", "index.html")


def load(name, default):
    try:
        return grid.load_json(name, default)
    except Exception:
        return default


def history() -> list:
    """The appended run-log behind THE LIVE SURFACE OVER TIME.

    NEVER WRITTEN AND UNREADABLE ARE DIFFERENT ANSWERS. This was one `except Exception: return []`
    around the whole read, so a missing file, a corrupt row and a permissions error all rendered as
    the same empty growth strip - and the repo's own ratchet caught it the moment the block moved
    out of `build()` into a function, because `pass` inside a long function and `return []` from a
    short one are the same defect wearing different clothes and only one of them is detectable.
    D19/D21: a null must not be indistinguishable from a real result.

    A file that does not exist yet is a real, knowable state and returns no rows. A row that will
    not parse is COUNTED and said out loud, and the rest of the log still renders."""
    p = os.path.join(str(grid.STATE), "assembly_history.jsonl")
    if not os.path.exists(p):
        return []
    rows, bad = [], 0
    with open(p, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except ValueError:
                bad += 1
    if bad:
        print("assembly_history.jsonl: %d unparseable row(s) skipped, %d kept" % (bad, len(rows)),
              file=sys.stderr)
    return rows
