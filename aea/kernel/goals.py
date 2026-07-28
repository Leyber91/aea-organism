"""goals.py - IT CAN BE GIVEN A JOB. The largest missing element until now.

WHAT WAS WRONG. The entity had exactly one job and it was hardcoded: produce the brief. There was no
slot for a second. Every mechanism built around it - the trust ledger, the impasse detector, the
unstick loop - is machinery for getting unstuck on a task it was GIVEN, and it had only ever been
given one. An assistant you cannot ask for anything is not an assistant.

A GOAL NEEDS FOUR FIELDS TO BE REAL, AND THE LAST TWO ARE THE ONES PEOPLE LEAVE OUT:

    what        the statement, in a sentence
    done_when   how anyone tells whether it is finished - checkable, not felt
    capability  which charter capability it runs as, so THE LEDGER CAN GRADE IT
    zone        where it may run, so THE PRIVACY BOUNDARY CAN BOUND IT

Without `capability` a goal cannot be graded, so it can never earn autonomy and never demote when it
fails - it sits outside the only mechanism that makes unattended work safe. Without `zone` it cannot
be bounded, so a goal touching private data has no rule saying it must stay local. A goal missing
either is a WISH, and `add()` refuses one rather than storing it.

WHY `done_when` IS A STRING AND NOT A PREDICATE. A checkable statement a human can read beats a
lambda nobody can audit. When a goal graduates to something the entity checks for itself, that check
becomes a crystallized part with its own trust level - which is the right place for it, because then
the check is graded too. Today the honest position is that a human or HADES reads the statement.

  python -m aea.kernel.goals              the board
  python -m aea.kernel.goals --seed       register the brief as goal one
"""
from __future__ import annotations

import os
import sys
import time

from aea.kernel import grid, trust

GOALS = os.path.join(grid.STATE, "goals.json")
ZONES = ("public", "private", "sensitive")
STATUS = ("open", "active", "done", "blocked", "retired")


class Rejected(ValueError):
    """A goal that cannot be graded or bounded is not stored. It is a wish."""


def _load() -> dict:
    return grid.load_json(GOALS, {"schema": "aea.goals/1", "goals": []})


def _save(doc: dict):
    grid.atomic_save_json(GOALS, doc)


def add(gid: str, what: str, done_when: str, capability: str, zone: str = "public",
        every: str | None = None, note: str = "") -> dict:
    """Register a goal. REFUSES one that cannot be graded or bounded.

    `every` is an optional cadence hint for the wake loop ("daily", "hourly"); a goal with no cadence
    is done once and retired.
    """
    if capability not in trust.CHARTER:
        raise Rejected(
            "capability %r is not in the charter, so the ledger could never grade this goal and it "
            "could neither earn autonomy nor demote on failure. Charter has: %s"
            % (capability, ", ".join(trust.CHARTER)))
    if zone not in ZONES:
        raise Rejected("zone %r is not one of %s, so the privacy boundary could not bound this goal"
                       % (zone, ZONES))
    if not (done_when or "").strip():
        raise Rejected("a goal with no done_when cannot be finished, only abandoned")

    doc = _load()
    doc["goals"] = [g for g in doc["goals"] if g["id"] != gid]
    doc["goals"].append({
        "id": gid, "what": what.strip(), "done_when": done_when.strip(),
        "capability": capability, "zone": zone, "every": every, "note": note,
        "status": "open", "added": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "runs": 0, "last": None, "last_outcome": None})
    _save(doc)
    return doc["goals"][-1]


def get(gid: str) -> dict | None:
    return next((g for g in _load()["goals"] if g["id"] == gid), None)


def due() -> list:
    """What the entity should pick up on this wake, and what it is ALLOWED to pick up.

    A goal whose capability sits at FORBIDDEN is not offered at all - there is no point waking to a
    job the charter forbids. A goal at DRAFT is offered and will produce something a human must
    approve, which is the correct behaviour rather than a failure.
    """
    out = []
    for g in _load()["goals"]:
        if g["status"] in ("done", "retired"):
            continue
        t = trust.check(g["capability"])
        if t["level"] <= 0:
            continue
        out.append({**g, "level": t["level"], "level_name": t["name"], "allowed": t["allowed"]})
    return out


def record(gid: str, ok: bool, note: str = "") -> dict:
    """One attempt at a goal. Grades the CAPABILITY it runs as - goals do not get a private ledger.

    This is deliberate. A goal is a job; a capability is the competence the job needs. Ten goals that
    all produce briefs should all sharpen the same competence, and inventing a second grading system
    beside the trust ledger would put two numbers on one thing and let them disagree.
    """
    doc = _load()
    g = next((x for x in doc["goals"] if x["id"] == gid), None)
    if not g:
        raise KeyError(gid)
    g["runs"] += 1
    g["last"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    g["last_outcome"] = "ok" if ok else "fail"
    if ok and not g.get("every"):
        g["status"] = "done"
    elif ok:
        g["status"] = "active"
    _save(doc)
    return trust.record(g["capability"], ok, note=note or ("goal:" + gid))


def render() -> str:
    rows = _load()["goals"]
    L = ["GOALS - what it has been asked to do", "=" * 78,
         "%-16s %-9s %-11s %-8s %-6s %s" % ("id", "status", "capability", "zone", "runs", "done when")]
    for g in rows:
        t = trust.check(g["capability"])
        L.append("%-16s %-9s %-11s %-8s %-6s %s"
                 % (g["id"], g["status"], "%s %s" % (t["level"], t["name"][:4]),
                    g["zone"], g["runs"], g["done_when"][:38]))
    if not rows:
        L.append("(none - it has never been asked for anything)")
    d = due()
    L.append("")
    L.append("%d due on the next wake%s" % (len(d), (": " + ", ".join(x["id"] for x in d)) if d else ""))
    return "\n".join(L)


if __name__ == "__main__":
    if "--seed" in sys.argv:
        # THE JOB IT ALREADY DOES, MADE EXPLICIT. Until now this lived as hardcoded control flow in
        # organs/brief.py and could not be listed, graded as a goal, added to, or turned off.
        g = add("morning-brief",
                what="Produce Luis's morning brief: what he is moving on, one AI opportunity, and "
                     "today's first focus.",
                done_when="brief_output.md written with all three sections present, no ERR, and "
                          "HADES returns accept",
                capability="produce_brief", zone="sensitive", every="daily",
                note="the entity's first job; ran unattended from 2026-07-10")
        print("registered:", g["id"], "->", g["capability"], "/", g["zone"])
        print()
    print(render())
