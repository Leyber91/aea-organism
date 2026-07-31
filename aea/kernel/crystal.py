"""crystal.py - A RESOLUTION THAT HELD, BECOMING A PART THE ENTITY KNOWS IT HAS.

WHAT CRYSTALLIZATION IS HERE. Something the system did once, that worked, promoted into a thing it
can reach for again without re-deriving it. The field calls this library learning or skill induction:
SOAR chunking 1986, Voyager 2023, SkillWeaver 2025.

AND THE PART EVERYONE GETS WRONG. The 2026 consensus is unambiguous and it is not what people build:

    CREATING THE PART IS EASY. ADMITTING IT IS HARD.

There is measured evidence that growing skill libraries make agents WORSE - skill shadowing, where a
near-miss part gets selected ahead of the right one and the library's own size degrades it. So this
file is mostly an ADMISSION GATE and a RETIREMENT rule, and only incidentally a store. A part that
cannot be demoted is a liability with a nice name.

THE TRIGGER IS AN IMPASSE, NOT A SUCCESS, and SOAR named that in 1986. Do not crystallize because
something worked - things work all the time. Crystallize because the system was STUCK and got
unstuck: that is the moment a result is worth keeping forever, because it is the moment re-deriving
it was expensive. `unstick` produces exactly that record, which is why it had to exist first.

THREE THINGS THE ENTITY MUST BE ABLE TO ANSWER, and they are what make a library different from a
junk drawer:

    WHAT DO I HAVE          `board()`     the parts, their level, their record
    DOES ANY OF IT APPLY    `applicable()` indexed by the impasse signature, not by name
    HOW DO I CARRY IT OUT   `carry_out()`  the part IS an executable move, not a description

The second is the one that matters. A part addressed by name requires the entity to already know what
it is looking for. A part addressed BY SITUATION answers the question it actually has, which is "I am
stuck like this - have I been here before".

ADMISSION AND RETIREMENT, both graded by the same ledger the capabilities use:

    seen SEEN_BEFORE times resolving the same impasse   -> admitted at DRAFT
    PROMOTE_AFTER clean reuses                          -> WATCHED, then TRUSTED
    any failure on reuse                                -> demoted one level, instantly
    demoted below DRAFT                                 -> RETIRED, and it is not offered again

  python -m aea.kernel.crystal              the library
  python -m aea.kernel.crystal --harvest    admit anything the experience record has earned
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time

from aea.kernel import grid, unstick

LIBRARY = os.path.join(grid.STATE, "crystal.json")


def _lib_path() -> str:
    """RESOLVED AT CALL TIME so a harness can be sandboxed - D48, same as `unstick._exp_path`."""
    return os.environ.get("AEA_CRYSTAL") or os.path.join(str(grid.STATE), "crystal.json")

SEEN_BEFORE = 2        # distinct times a move must resolve the SAME impasse before admission
PROMOTE_AFTER = 3      # clean reuses per level
LEVELS = {0: "RETIRED", 1: "DRAFT", 2: "WATCHED", 3: "TRUSTED"}
CEILING = 3


def _load() -> dict:
    return grid.load_json(_lib_path(), {"schema": "aea.crystal/1", "parts": {}})


def _save(doc: dict):
    grid.atomic_save_json(_lib_path(), doc)


def part_id(signature: str, move: dict) -> str:
    """A part IS the pairing of a situation and the move that resolved it. Either alone is useless:
    a move with no situation cannot be selected, and a situation with no move is just a complaint."""
    blob = json.dumps({"sig": signature, "move": move}, sort_keys=True)
    return "p_" + hashlib.sha1(blob.encode()).hexdigest()[:10]


def name_for(signature: str, move: dict) -> str:
    """A readable name, so the board can be read by a person. Never used for lookup - lookup is by
    situation, because the entity does not know the name of the thing it needs."""
    knob = move.get("knob", "?")
    sig = (signature or "")[:44].replace("fail -> ", "").strip()
    return "when [%s] then %s -> %s" % (sig, move.get("move", "?"), move.get("to", "?"))


def harvest(min_seen: int = SEEN_BEFORE) -> dict:
    """Read the experience record and admit anything that has earned it.

    ADMISSION IS DELIBERATELY CONSERVATIVE. A move that resolved an impasse ONCE is a coincidence
    until it does it again; the literature's failure mode is a library that fills with one-offs and
    then shadows the parts that work. `min_seen` is the whole gate and raising it is always safe.
    """
    exp = grid.load_json(unstick._exp_path(), {"attempts": []})
    doc = _load()
    wins = {}
    for a in exp.get("attempts", []):
        if not a.get("worked"):
            continue
        k = (a["signature"], json.dumps(a["move"], sort_keys=True))
        wins.setdefault(k, []).append(a)

    admitted = []
    for (sig, mjson), rows in wins.items():
        if len(rows) < min_seen:
            continue
        move = json.loads(mjson)
        pid = part_id(sig, move)
        if pid in doc["parts"]:
            continue
        unstick.check_invariants(move)          # a part may not encode a permission change, ever
        doc["parts"][pid] = {
            "id": pid, "name": name_for(sig, move), "signature": sig, "move": move,
            "level": 1, "streak": 0, "uses": 0, "wins": 0, "fails": 0,
            "admitted": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
            "evidence": "resolved this impasse %d times before admission" % len(rows)}
        admitted.append(doc["parts"][pid])
    _save(doc)
    return {"admitted": admitted, "library": len(doc["parts"])}


def applicable(signature: str, min_level: int = 1) -> list:
    """THE QUESTION THE ENTITY ACTUALLY HAS: I am stuck like this - have I been here before?

    Matched on the impasse signature, so the lookup key is the SITUATION rather than a name. Retired
    parts are never offered. Ordered by level then by record, so the most-proven part goes first.
    """
    doc = _load()
    # A RESTED PART COMES BACK. `record_use` puts a part at the floor to REST rather than deleting
    # it, and this is where the rest ends - so the un-retire path exists and is exercised by the
    # same call that would otherwise never offer it again.
    woke = [p for p in doc["parts"].values() if _rested(p)]
    if woke:
        _save(doc)
    out = [p for p in doc["parts"].values()
           if p["level"] >= max(1, min_level) and p["signature"] == signature]
    out.sort(key=lambda p: (-p["level"], -p["wins"], p["fails"]))
    return out


def carry_out(pid: str, apply_fn=None) -> dict:
    """Execute a part. `apply_fn(move)` does the real work and returns truthy on success.

    WITHOUT `apply_fn` THIS IS A DRY RUN and says so. Nothing here reaches into the world by itself:
    the part describes a move, the caller owns the doing. That keeps the library inert on its own,
    which is the correct default for a store that grows without supervision.
    """
    doc = _load()
    p = doc["parts"].get(pid)
    if not p:
        raise KeyError(pid)
    if p["level"] < 1:
        return {"ok": False, "why": "part is RETIRED and is not offered", "part": p}
    unstick.check_invariants(p["move"])
    if apply_fn is None:
        return {"ok": None, "dry_run": True, "move": p["move"], "part": p,
                "why": "no apply_fn given; the part describes the move, the caller performs it"}
    ok = bool(apply_fn(p["move"]))
    return {"ok": ok, "move": p["move"], "part": record_use(pid, ok)}


DEMOTE_AFTER = 2       # attributable failures before a level is taken away
COOLDOWN_S = 3600      # a part at the floor rests; it is not destroyed


def record_use(pid: str, worked: bool, counts: bool = True, why: str = "") -> dict:
    """Grade a part: slow up, slow down, REST at the floor - never deleted by one bad night.

    THIS FUNCTION USED TO BE THE FALSE POSITIVE THE WHOLE DESIGN EXISTS TO PREVENT. It read
    `p["level"] -= 1` on any failure, and a part is admitted at level 1, so the FIRST failure drove
    it to 0 and stamped `retired` - with the comment "RETIRED. Never offered again by
    applicable()." There was no n, no cause check and no un-retire path anywhere in the module.
    Admission required a move to resolve the same impasse SEEN_BEFORE=2 times; deletion required
    one. A single 429 during a storm permanently destroyed a capability the entity had earned.

    THREE CHANGES, and they mirror `energy._retire`/`_cooling`, which already got this right for
    rods: a cooldown expires by design and cannot express "never again", so permanence is reserved
    for a thing that genuinely answered Gone.

    1 `counts=False` IS NOT A FAILURE, IT IS NOT EVIDENCE. A use whose outcome row was classed
      TRANSIENT_EXTERNAL, CODE_FAULT or UNATTRIBUTABLE says nothing about the part. It is recorded
      as a use and it moves nothing. It does NOT silently skip - the row is kept with its reason,
      because a use that vanished is indistinguishable from a use that never happened.
    2 DEMOTE_AFTER attributable failures before a level is taken, so n=1 cannot demote.
    3 THE FLOOR IS A COOLDOWN, NOT A TOMBSTONE. A part at level 0 rests for COOLDOWN_S and is then
      offered again at DRAFT. Nothing in this module may make a part unreachable forever.
    """
    doc = _load()
    p = doc["parts"][pid]
    p["uses"] += 1
    if not counts:
        p["unattributed"] = int(p.get("unattributed") or 0) + 1
        p["last_unattributed_why"] = str(why)[:120]
        _save(doc)
        return p
    if worked:
        p["wins"] += 1
        p["streak"] += 1
        p.pop("resting_until", None)         # a win ends a rest immediately
        if p["streak"] >= PROMOTE_AFTER and p["level"] < CEILING:
            p["level"] += 1
            p["streak"] = 0
    else:
        p["fails"] += 1
        p["streak"] = 0
        p["since_demote"] = int(p.get("since_demote") or 0) + 1
        if p["since_demote"] >= DEMOTE_AFTER:
            p["since_demote"] = 0
            p["level"] -= 1
            if p["level"] < 1:
                p["level"] = 0
                p["resting_until"] = time.time() + COOLDOWN_S
                p["rested_why"] = str(why)[:120] or "at the floor after attributable failures"
    _save(doc)
    return p


def _rested(p: dict) -> bool:
    """A part at the floor whose rest has expired comes back at DRAFT. Called by `applicable`."""
    until = p.get("resting_until")
    if not until or time.time() < float(until):
        return False
    p["level"] = 1
    p["since_demote"] = 0
    p.pop("resting_until", None)
    p["returned"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    return True


def board() -> str:
    doc = _load()
    parts = sorted(doc["parts"].values(), key=lambda p: (-p["level"], -p["wins"]))
    L = ["THE CRYSTAL LIBRARY - resolutions that held, and what they are trusted to do", "=" * 92,
         "%-9s %-10s %-6s %-6s %s" % ("level", "uses", "wins", "fails", "part")]
    for p in parts:
        L.append("%-9s %-10s %-6s %-6s %s"
                 % ("%d %s" % (p["level"], LEVELS[p["level"]]), p["uses"], p["wins"], p["fails"],
                    p["name"][:58]))
    if not parts:
        L.append("(empty - nothing has resolved the same impasse twice yet)")
    exp = grid.load_json(unstick._exp_path(), {"attempts": []})
    L.append("")
    L.append("experience holds %d attempts; admission needs the same move to resolve the same "
             "impasse %d times." % (len(exp.get("attempts") or []), SEEN_BEFORE))
    return "\n".join(L)


if __name__ == "__main__":
    if "--harvest" in sys.argv:
        r = harvest()
        print("admitted %d new part(s); library holds %d" % (len(r["admitted"]), r["library"]))
        for p in r["admitted"]:
            print("   %s  [%s]" % (p["name"], p["evidence"]))
        print()
    print(board())
