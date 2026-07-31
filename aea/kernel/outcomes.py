"""outcomes.py - THE RECORD OF WHETHER IT ACTUALLY WORKED. One append-only row per action.

    python -m aea.kernel.outcomes            # the store: counts by class, by move, by src
    python -m aea.kernel.outcomes --schema   # what a row must carry, and what is refused

THE MISSING FIELD. Of R3's tuple - (decided, called, returned, did-it-match) - the first is durable
in `aea_state.json`, the second is split across two stores, the third survives only as an 80-char
truncation or a 16-hex hash, and **the fourth does not exist anywhere in the tree.** This file is
the fourth.

THE ONE REFUSAL THAT DOES THE WORK, and everything else here is bookkeeping around it:

    A ROW MAY NOT CLAIM SUCCESS WITHOUT A POST-CONDITION THAT WAS EVALUATED.

Three lines in the running system manufacture a false success today, and this refusal converts all
three into loud failures the first time they execute:

    live.py:284   ok, tail = True, str(out)[:300]      success is HARDCODED on the tool branch
    hands.py:342  return "ERROR: no such state file"   an error string returned as a NORMAL value
    live.py:69    return r.returncode == 0             exit 0 measured 25 times while nothing happened

That third one is not a worry about the future. `consolidate` exited 0 twenty-five times in a
recorded run while `state_bytes` rose monotonically with zero decreases - the process succeeded and
the work did not happen. An outcome store that believes exit codes would have written twenty-five
"it worked" rows, and R3's whole claim is that this record can be trusted.

WHY IT RAISES INSTEAD OF SKIPPING. `hands._ledger` wraps its append in `except Exception: pass`
because "bookkeeping never stops the gate" - correct for a gate that must keep serving, and fatal
for an evidence store, where **a lost failure row is indistinguishable from a success that never
happened.** `grid.append_jsonl` raises, `require` raises, and a tick that cannot record what it did
dies loudly rather than quietly teaching the entity from a corpus with holes in it. The idiom is
lifted verbatim from `harness.py:846-848`, which already refuses to persist an unstamped row.

PROVENANCE IS FAIL-CLOSED. `src` defaults to `unattributed`, never to `wake`. On 2026-07-31 the
hands ledger held 4,925 rows and every one was synthetic - written by a red-team harness that
redirected the state file it read but not the ledger it wrote - and only 5 carried the canary,
because attack payloads are refused BEFORE the boundary while the clean crossings that DO land are
indistinguishable from entity history by content. Any statistic that does not filter `src` is a
statistic about test harnesses. Forgetting to label a new caller therefore EXCLUDES it.

EVERY ROW CARRIES THE CODE THAT PRODUCED IT. `shadow.head()` plus a dirty flag: without it, "did
the change help?" is unanswerable, because two rows from two versions of the decider are not
comparable. This is the smallest honest version stamp; `harness.check_id` and `fuel.require` are the
same move on other axes and this reuses their shape rather than inventing a third.
"""
from __future__ import annotations

import json
import os
import sys
import time

from aea.kernel import cause, grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STORE = "outcomes.jsonl"          # resolved through grid.STATE; NEVER truncated, never rotated out

# The row's required shape. A missing key here is a refusal, not a default: a store that fills in
# what a caller forgot cannot be read back as evidence of what the caller knew.
REQUIRED = ("at", "src", "move", "kind", "ok", "cause", "code")


class Unrecordable(ValueError):
    """The row cannot be written, and the reason is always named. Never swallowed."""


def _path() -> str:
    """Resolved AT CALL TIME so a harness can be sandboxed - D48. A module constant bound to
    `grid.STATE` at import is why 4,920 synthetic rows landed in the production hands ledger."""
    return os.environ.get("AEA_OUTCOMES") or os.path.join(str(grid.STATE), STORE)


def _code() -> dict:
    """The version of the decider that produced this row. Cheap, and the only thing that makes two
    rows comparable."""
    try:
        d = shadow_dirty()
        return dict(commit=(shadow_head() or "")[:12], dirty=bool(d))
    except Exception:
        return dict(commit="", dirty=None)          # None means UNKNOWN, which is not False


def shadow_head():
    from aea.kernel import shadow
    return shadow.head()


def shadow_dirty():
    from aea.kernel import shadow
    # `dirty()` returns a list that includes git's LF/CRLF warnings on Windows; a warning line is
    # not a modified file, and counting it would mark every row dirty forever.
    return [f for f in (shadow.dirty() or []) if not str(f).startswith("warning:")]


def require(row: dict) -> dict:
    """{"ok": True} or {"ok": False, "refused": <the reason>}. The gate, in one function.

    THE CENTRAL CLAUSE is the success check. Everything else is shape."""
    if not isinstance(row, dict):
        return dict(ok=False, refused="a row must be a dict")
    for k in REQUIRED:
        if k not in row:
            return dict(ok=False, refused=f"{k} REQUIRED - an unstamped row refuses loudly, never half-records")

    c = row.get("cause") or {}
    if not isinstance(c, dict) or c.get("class") not in cause.CLASSES:
        return dict(ok=False, refused=f"cause.class must be one of {cause.CLASSES}, got {c.get('class')!r}")

    # THE CLAUSE THAT DOES THE WORK. A success needs a post-condition that was actually evaluated.
    # `ok` is not evidence: three call sites in this repo produce ok=True without checking anything.
    if row.get("ok"):
        v = row.get("verify")
        if not isinstance(v, dict) or "result" not in v:
            return dict(ok=False, refused=(
                "ok=True with no verify block - a success must name the post-condition that was "
                "evaluated and its verdict. live.py:284 hardcodes ok=True, hands.py:342 returns an "
                "error string as a normal value, and live.py:69 grades on an exit code that was 0 "
                "for 25 consolidates that did nothing. This refusal is the point of the module."))
        if not v.get("result"):
            return dict(ok=False, refused="ok=True but the verify block says the post-condition was FALSE")

    if row.get("counts_toward_move") and not cause.counts(c.get("class")):
        return dict(ok=False, refused=(
            f"counts_toward_move=True on a {c.get('class')} row - only {sorted(cause.GRADES_THE_MOVE)} "
            f"may credit or discredit a move. This is the 429-teaches-abandon-brief failure."))
    return dict(ok=True)


def build(move: str, kind: str, ok: bool, *, src: str = "unattributed", decision_id=None,
          run: str = "", args=None, result=None, verify=None, exc=None, note: str = "",
          signature: str = "") -> dict:
    """Assemble a row and classify it. The ONLY intended way to construct one."""
    c = cause.classify(result=result, verify=verify, exc=exc, note=note)
    return dict(
        at=time.time(), at_iso=time.strftime("%Y-%m-%d %H:%M:%S"),
        run=run or "", decision_id=decision_id,
        move=move, kind=kind, args=args, src=src,
        ok=bool(ok), verify=verify, cause=c,
        counts_toward_move=bool(c.get("counts_toward_move")),
        signature=signature, note=str(note or "")[:300],
        code=_code(),
    )


def write(row: dict) -> dict:
    """Persist, or RAISE with the reason. There is no third outcome and no silent path."""
    chk = require(row)
    if not chk["ok"]:
        raise Unrecordable("refusing to record this outcome: " + chk["refused"])
    grid.append_jsonl(_path(), row)
    return row


def record(move: str, kind: str, ok: bool, **kw) -> dict:
    """build + write. The one-liner every call site should use."""
    return write(build(move, kind, ok, **kw))


def read(where=None, wake_only: bool = False) -> list:
    """Every row, oldest first. `wake_only` is the fail-closed filter for any claim about the ENTITY."""
    p = _path()
    if not os.path.exists(p):
        return []
    out = []
    for ln in open(p, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            r = json.loads(ln)
        except Exception:
            continue                      # a corrupt line is not a reason to lose the rest
        if wake_only and r.get("src") != "wake":
            continue
        if where and not where(r):
            continue
        out.append(r)
    return out


def tally(rows=None) -> dict:
    rows = read() if rows is None else rows
    by = {}
    for r in rows:
        k = (r.get("cause") or {}).get("class", "?")
        by[k] = by.get(k, 0) + 1
    return by


if __name__ == "__main__":
    if "--schema" in sys.argv[1:]:
        print("=" * 96)
        print("OUTCOME ROW - required keys and the refusals")
        print("=" * 96)
        print("  REQUIRED:", ", ".join(REQUIRED))
        print()
        for bad, why in (
            (dict(), "an empty row"),
            (dict(at=1, src="wake", move="brief", kind="script", ok=True,
                  cause=dict(**{"class": "OK"}), code={}), "ok=True with no verify block"),
            (dict(at=1, src="wake", move="brief", kind="script", ok=False,
                  cause=dict(**{"class": "TRANSIENT_EXTERNAL"}), code={},
                  counts_toward_move=True), "a transient row trying to grade the move"),
        ):
            r = require(bad)
            print(f"  {why:44s} -> {'ACCEPTED (BUG)' if r['ok'] else 'refused'}")
            if not r["ok"]:
                print(f"       {r['refused'][:150]}")
        sys.exit(0)

    rows = read()
    print("=" * 96)
    print(f"OUTCOMES - {len(rows)} rows at {_path()}")
    print("=" * 96)
    if not rows:
        print("  EMPTY. No action has been recorded through this store yet.")
        print("  That is not a pass and not a failure: nothing has been observed.")
        sys.exit(0)
    for k, v in sorted(tally(rows).items(), key=lambda kv: -kv[1]):
        print(f"  {k:22s} {v}")
    print()
    srcs = {}
    for r in rows:
        srcs[r.get("src", "?")] = srcs.get(r.get("src", "?"), 0) + 1
    print("  by src:", ", ".join(f"{k}={v}" for k, v in sorted(srcs.items())))
    print(f"  grading the move: {sum(1 for r in rows if r.get('counts_toward_move'))}")
