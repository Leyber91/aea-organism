"""journey_check.py - THE ENFORCEMENT. Are the three ladders the same ladder?

THE PROBLEM THIS EXISTS FOR. The project carries three descriptions of the same climb and nothing checks
them against each other:

  THE RAIL       what the bench can actually seat - tap, scaffold, governor, ladder, scorer
  THE JOURNEY    design/THE_JOURNEY.md - ten necessity-ordered rows, each "everything above plus one part"
  THE HIERARCHY  design/THE_LINEAR_HIERARCHY.md - nine rungs, an exact partition of all 86 census items

They have already drifted apart. The playable sequence in web/game/js/mission.js admits THE DRAW and THE
MEASURE (journey rows 1-2, rungs L0-L1), then jumps straight to THE LADDER (row 6, rung L4), skipping THE
READOUT, THE FRAME and THE CRITIC - which are the three cheapest rungs and carry two of the strongest
measured receipts in the project. Nothing failed when that happened, because no mission file declares which
element of the architecture it admits or what it requires first. "Cumulative" was prose, so it could not be
violated.

WHAT THIS CHECKS, and every one of these can fail:

  1  the hierarchy markdown is an exact partition of C-01..C-86 - every item once, none dropped
  2  each journey row's items sit at ONE rung, and the rows never descend
  3  every mission declares `rung`, `adds` and `requires`
  4  the mission sequence never descends a rung - the climb is monotonic
  5  a mission never requires something no earlier mission added
  6  every census id named anywhere actually exists

It also writes web/game/data/canon/hierarchy.json so the partition survives as DATA. The script that
generated THE_LINEAR_HIERARCHY.md lived in a session scratchpad and is gone; the markdown is now the only
copy of a result that took an audit to produce, and a markdown table is not something the game can read.

This is a CHECKER, not a fixer. It reports what is wrong and exits non-zero. Deciding what to do about a
skipped rung is a design call and stays with the author.

Run: python -m aea.tooling.journey_check
"""
from __future__ import annotations

import json
import os
import re
import sys

from aea.kernel import grid

CENSUS_N = 86
RAIL = ("tap", "scaffold", "governor", "ladder", "scorer")


# --- PARSE THE THREE LADDERS ------------------------------------------------------------------------

def read_hierarchy() -> tuple:
    """(item -> rung index, rung index -> title). Refuses to return a partial partition."""
    p = os.path.join(grid.ROOT, "design", "THE_LINEAR_HIERARCHY.md")
    txt = open(p, encoding="utf-8").read()
    at, rungs, place = None, {}, {}
    for line in txt.splitlines():
        m = re.match(r"^##\s+L(\d+)\s*[-–—]\s*(.+?)\s*$", line)
        if m:
            at = int(m.group(1))
            rungs[at] = m.group(2).strip()
            continue
        m = re.match(r"^\|\s*(C-\d+)\s*\|\s*(.+?)\s*\|\s*([ECMO])\s*\|", line)
        if m and at is not None:
            cid, label, disp = m.group(1), m.group(2).strip(), m.group(3)
            if cid in place:
                raise ValueError("%s is placed twice: L%d and L%d" % (cid, place[cid]["rung"], at))
            place[cid] = {"rung": at, "label": label, "disposition": disp}
    return place, rungs


def read_journey() -> list:
    """The journey table as [{n, name, items, wall, state}]. The census ids are the join key."""
    p = os.path.join(grid.ROOT, "design", "THE_JOURNEY.md")
    rows = []
    for line in open(p, encoding="utf-8").read().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else []
        if len(cells) < 6 or not cells[0].isdigit():
            continue
        name = re.sub(r"[*`]", "", cells[1])
        rows.append({"n": int(cells[0]),
                     "name": name.split("·")[0].strip(),
                     "items": re.findall(r"C-\d+", cells[1]),
                     "wall": cells[2], "state": re.sub(r"[*]", "", cells[5])})
    return rows


def read_sequence() -> list:
    """The playable order, read from mission.js so there is ONE source of truth for it."""
    p = os.path.join(grid.WEB, "game", "js", "mission.js")
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"var\s+SEQ\s*=\s*\[(.*?)\]", txt, re.S)
    if not m:
        raise ValueError("no SEQ array in mission.js - the playable order cannot be read")
    return re.findall(r"[\"']([^\"']+\.json)[\"']", m.group(1))


def read_missions(seq: list) -> list:
    d = os.path.join(grid.WEB, "game", "data", "missions")
    out = []
    for fn in seq:
        p = os.path.join(d, fn)
        if not os.path.exists(p):
            out.append({"file": fn, "missing_file": True})
            continue
        j = json.load(open(p, encoding="utf-8"))
        j["file"] = fn
        out.append(j)
    return out


# --- THE CHECKS -------------------------------------------------------------------------------------

def check() -> dict:
    fails, notes, defers = [], [], []
    place, rungs = read_hierarchy()

    # 1 EXACT PARTITION. A hierarchy that leaves items unplaced is a filing preference, not a claim.
    expect = {"C-%02d" % i for i in range(1, CENSUS_N + 1)}
    missing, extra = sorted(expect - set(place)), sorted(set(place) - expect)
    if missing or extra:
        fails.append("hierarchy is not an exact partition of C-01..C-%d: missing %s, unexpected %s"
                     % (CENSUS_N, missing or "none", extra or "none"))

    # 2 THE JOURNEY AGAINST THE HIERARCHY. Two partitions of the same architecture may legitimately
    # differ - but a difference must be NAMED, not discovered later as a bug.
    journey, high = read_journey(), -1
    for r in journey:
        rs = sorted({place[c]["rung"] for c in r["items"] if c in place})
        # AN ID ABOVE THE CENSUS IS A CANDIDATE, NOT AN ERROR. THE READOUT (C-87) was found by watching a
        # rod work rather than by auditing the architecture's description, so the 86 is a floor and new
        # items are expected to appear. x07 produced a second candidate the same way. A checker that
        # failed on them would punish the project's most useful habit.
        cand = [c for c in r["items"] if c not in place and int(c[2:]) > CENSUS_N]
        unknown = [c for c in r["items"] if c not in place and c not in cand]
        r["rungs"], r["candidates"] = rs, cand
        if cand:
            notes.append("journey row %d (%s) rests on candidate %s - outside the 86, found by building"
                         % (r["n"], r["name"], ", ".join(cand)))
        if unknown:
            fails.append("journey row %d (%s) names ids absent from the census: %s"
                         % (r["n"], r["name"], unknown))
        if len(rs) > 1:
            notes.append("journey row %d (%s) SPANS rungs %s - the two partitions place its items "
                         "differently, and that fork is unrecorded"
                         % (r["n"], r["name"], ", ".join("L%d" % x for x in rs)))
        if rs and rs[-1] < high:
            fails.append("journey row %d (%s) DESCENDS to L%d after L%d" % (r["n"], r["name"], rs[-1], high))
        high = max(high, rs[-1] if rs else high)

    # 3-5 THE PLAYABLE SEQUENCE. This is the check that would have caught the L1 -> L4 jump.
    seq, held, prev = read_missions(read_sequence()), set(), -1
    for ms in seq:
        who = ms.get("id") or ms["file"]
        if ms.get("missing_file"):
            fails.append("mission %s is in SEQ but the file does not exist" % who)
            continue
        rung, adds, req = ms.get("rung"), ms.get("adds") or [], ms.get("requires") or []
        cand, kind = ms.get("candidates") or [], ms.get("kind") or "rung"
        if rung is None:
            fails.append("mission %s declares no `rung` - cumulativeness is unenforceable for it" % who)
        # A MISSION MAY LEGITIMATELY ADD NOTHING FROM THE CENSUS, in exactly two cases, and both must be
        # declared rather than left to be inferred from an empty field: an INTERSTITIAL (a recap or a fog
        # reveal, which admits no new element), or a CANDIDATE (a part the game needed and the audit never
        # named - the same way THE READOUT was found).
        if not adds and kind != "interstitial" and not cand:
            fails.append("mission %s declares no `adds` - name the census ids it wires, or declare "
                         "`candidates` for an element outside the 86, or `kind: interstitial`" % who)
        if "requires" not in ms:
            fails.append("mission %s declares no `requires` - a skipped rung cannot be detected" % who)
        if cand:
            notes.append("mission %s rests on candidate %s - an element the 86-item audit never named, "
                         "found by building the game rather than by auditing the architecture"
                         % (who, ", ".join(cand)))
        for c in adds + req:
            if c not in place and int(c[2:]) <= CENSUS_N:
                fails.append("mission %s names %s, which is not in the census" % (who, c))
        if isinstance(rung, int):
            if rung < prev:
                fails.append("mission %s DESCENDS to L%d after L%d - the climb is not monotonic"
                             % (who, rung, prev))
            # A SKIP MAY BE DECLARED, NEVER SILENT. Some rungs cannot be admitted yet - L3 needs a critic
            # part the rail does not have - so a rule that only failed would force either a lie or a
            # disabled check. `defers` makes the debt DATA: {"L3": "why"}. It is deliberately not a rubber
            # stamp - every deferral is reported, and the count is printed beside the failures, the same
            # way the harness carries verification debt rather than discharging it quietly.
            gap = [r for r in range(prev + 1, rung) if r >= 0]
            dec = ms.get("defers") or {}
            if prev >= 0 and gap:
                undeclared = [g for g in gap if not dec.get("L%d" % g)]
                if undeclared:
                    fails.append("mission %s SKIPS %s with no reason declared - the sequence jumps L%d to "
                                 "L%d, so the journey is not cumulative. admit the rung, or declare it in "
                                 "`defers`" % (who, ", ".join("L%d" % g for g in undeclared), prev, rung))
                for g in gap:
                    if dec.get("L%d" % g):
                        defers.append("%s defers L%d: %s" % (who, g, dec["L%d" % g]))
            prev = max(prev, rung)
        for c in req:
            if c not in held:
                fails.append("mission %s requires %s, which no earlier mission added" % (who, c))
        held |= set(adds)

    # 6 THE FORGE QUEUE - THE FOURTH LADDER, and it was invisible until modules.json was read as an
    # ORDERING rather than as a registry. `status: FORGE-PENDING` rows carry `forge.queue`, which is a build
    # order, and a build order over architecture parts is a claim about what comes first. Nothing joined it
    # to the other three.
    reg = grid.load_json(os.path.join(grid.STATE, "modules.json"), {}) or {}
    queue = sorted(((v.get("forge") or {}).get("queue"), k) for k, v in (reg.get("modules") or {}).items()
                   if (v.get("forge") or {}).get("queue") is not None)
    for q, part in queue:
        row = (reg.get("modules") or {}).get(part) or {}
        if not row.get("rung") and not row.get("adds"):
            notes.append("forge queue %s (%s) declares no rung or census ids - the build ORDER cannot be "
                         "checked against the hierarchy, so a queue that skips a rung fails nothing"
                         % (q, part))
    ql = [p for _, p in queue]

    # 6 THE RAIL. A mission cannot honestly admit a part the bench has no fire path for.
    bc = open(os.path.join(grid.ROOT, "aea", "bench", "bench_core.py"), encoding="utf-8").read()
    wired = [p for p in RAIL if 'part == "%s"' % p in bc]
    if sorted(wired) != sorted(RAIL):
        notes.append("rail parts declared FIREABLE with no fire path: %s"
                     % ", ".join(sorted(set(RAIL) - set(wired))))

    return {"place": place, "rungs": rungs, "journey": journey, "seq": seq,
            "wired_rail": wired, "forge_queue": ql, "fails": fails, "notes": notes,
            "defers": defers}


def emit(res: dict) -> str:
    """Write the partition as DATA. The generator that produced the markdown is lost; this makes the
    result reproducible from the document and readable by the game."""
    by_rung = {}
    for cid, v in res["place"].items():
        by_rung.setdefault(v["rung"], []).append(cid)
    out = {"note": "generated by aea/tooling/journey_check.py from design/THE_LINEAR_HIERARCHY.md - "
                   "an exact partition of C-01..C-%d. do not hand-edit." % CENSUS_N,
           "count": len(res["place"]),
           "rungs": [{"rung": r, "title": res["rungs"].get(r, ""),
                      "items": sorted(by_rung.get(r, []), key=lambda c: int(c[2:])),
                      "cumulative": sum(len(by_rung.get(k, [])) for k in range(r + 1))}
                     for r in sorted(res["rungs"])],
           "items": {c: {"rung": v["rung"], "label": v["label"], "disposition": v["disposition"]}
                     for c, v in sorted(res["place"].items(), key=lambda kv: int(kv[0][2:]))},
           "journey": [{"row": r["n"], "name": r["name"], "items": r["items"],
                        "rungs": r.get("rungs", []), "state": r["state"]} for r in res["journey"]]}
    p = os.path.join(grid.WEB, "game", "data", "canon", "hierarchy.json")
    grid.atomic_save_json(p, out)
    return p


def main() -> int:
    res = check()
    print("HIERARCHY  %d items across %d rungs" % (len(res["place"]), len(res["rungs"])))
    print("JOURNEY    %d rows, naming %d census items"
          % (len(res["journey"]), len({c for r in res["journey"] for c in r["items"]})))
    print("SEQUENCE   %s" % " -> ".join((m.get("id") or m["file"]) for m in res["seq"]))
    print("RAIL WIRED %s" % ", ".join(res["wired_rail"]))
    print("FORGE QUEUE %s" % (" -> ".join(res["forge_queue"]) or "empty"))
    print()
    print("THE CLIMB THE MISSIONS ACTUALLY WALK")
    for m in res["seq"]:
        print("  %-6s %-16s rung %-4s adds %-22s requires %s"
              % (m.get("id") or "?", (m.get("title") or "")[:16], m.get("rung"),
                 ",".join(m.get("adds") or []) or "-", ",".join(m.get("requires") or []) or "-"))
    print()
    for d in res["defers"]:
        print("DEBT  %s" % d)
    for n in res["notes"]:
        print("NOTE  %s" % n)
    for f in res["fails"]:
        print("FAIL  %s" % f)
    print()
    p = emit(res)
    print("wrote %s" % os.path.relpath(p, grid.ROOT).replace("\\", "/"))
    print("%d failures, %d declared deferrals, %d notes"
          % (len(res["fails"]), len(res["defers"]), len(res["notes"])))
    return 1 if res["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
