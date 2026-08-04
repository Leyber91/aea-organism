"""dossier.py - EVERY NUMBER A RUNG PAGE SHOWS, COMPUTED ONCE, FROM DISK.

    python -m aea.tooling.dossier          the dossier, to stdout
    python -m aea.tooling.dossier --write  to state/ladder_dossier.json

WHY A SEPARATE MODULE FROM THE PAGES. `render.py`'s own rule - "what this file is not allowed to
contain: a number, a colour, a selector, or a sentence" - exists because a 494-line build held the
rail's arithmetic and the caption's arithmetic forty lines apart and they disagreed for a week. The
same failure is available to eight rung pages: each computes its own totals, two of them drift, and
nothing between them can notice. So the pages compute NOTHING. They read this.

WHAT A RUNG PAGE IS ALLOWED TO SAY, and the shape is identical for all ten so that no page is
special and nothing is arranged by hand:

    CLAIM        power, bound, gate - lifted VERBATIM from `ladder.RUNGS`. Never paraphrased,
                 because the gate is the contract and a paraphrase of a contract is a new contract
    MEASUREMENT  whatever `ladder.MEASURE[id]()` returns, live. A rung with no measurement function
                 returns {} and the page prints that it is unmeasured - which is the state R5 sat
                 in for a day while 66 of its claims already existed on disk
    JOURNEY      the evidence that rung actually produced, walkable to the stored bytes. Empty for
                 every rung that has produced none, with the reason stated
    WIRING       the functions the rung declares, checked against the live call graph

A RUNG WITH NO JOURNEY SAYS SO. It does not borrow another rung's evidence and it does not fill the
space with prose. `journey()` returns `rows=[]` and a `why`, and the renderer prints the why. The
honesty law is not suspended for a page that would look better full.
"""
from __future__ import annotations

import json
import os
import sys

from aea.kernel import grid


def _rows(name: str) -> list:
    p = os.path.join(grid.STATE, name)
    out = []
    if not os.path.exists(p):
        return out
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def _fold(rows: list, key: str = "hid") -> list:
    """Later rows win, so a settlement supersedes its proposal - the same fold `state()` uses."""
    latest = {}
    for r in rows:
        k = r.get(key)
        if k:
            latest[k] = r
    return list(latest.values())


def journey(rid: str) -> dict:
    """The evidence a rung actually produced, walkable from claim to stored bytes.

    R5 IS THE ONLY RUNG THAT CAN ANSWER THIS TODAY, and that is a fact about the repository rather
    than a limit of this function. R5 is the first rung whose whole output is a chain - a claim
    written before the evidence, a probe, bytes hashed at the socket, a verdict, a consequence - so
    it is the first that can be WALKED. Every rung below leaves rows (outcomes, ledgers, decisions)
    but none of them links a claim to the bytes that settled it, because none of them made a claim.

    Every other rung returns an empty chain and the reason. When R6 starts linking memories to their
    sources it will fill this in the same shape, and nothing here needs editing."""
    if rid != "R5":
        return dict(rows=[], why="this rung produces outcomes, not claims - there is no "
                                 "claim-to-bytes chain to walk. R5 is the first rung whose output "
                                 "is evidence rather than action")
    hyp = _fold(_rows("hypotheses.jsonl"))
    art = {}
    for a in _rows("artefacts.jsonl"):
        for k in (a.get("id"), a.get("sha256")):
            if k:
                art[str(k).lower()] = a
    rows = []
    for h in sorted(hyp, key=lambda x: -(x.get("settled_at") or x.get("at") or 0)):
        cites = []
        for c in (h.get("citations") or []):
            a = art.get(str(c).lower())
            if not a:
                continue
            blob = os.path.join(grid.STATE, "artefacts", "%s.bin" % a.get("sha256"))
            cites.append(dict(id=a.get("id"), sha256=a.get("sha256"), url=a.get("url"),
                              at=a.get("at"), src=a.get("src"), status=a.get("status"),
                              bytes=(os.path.getsize(blob) if os.path.exists(blob) else None),
                              on_disk=os.path.exists(blob)))
        rows.append(dict(hid=h.get("hid"), status=h.get("status"), claim=h.get("claim"),
                         killer=h.get("killer"), from_record=h.get("from_record"),
                         holds_fixed=h.get("holds_fixed") or [],
                         consequence=h.get("consequence") or "", why=h.get("why") or "",
                         run=h.get("run"), at=h.get("at"), settled_at=h.get("settled_at"),
                         by_entity=str(h.get("run") or "").startswith("belief_"),
                         citations=cites))
    return dict(rows=rows, why="")


def build() -> dict:
    from aea.tooling import ladder
    specs = getattr(ladder, "RUNGS", None) or getattr(ladder, "LADDER", [])
    try:
        wiring = ladder.verify_funcs()
    except Exception as e:
        wiring = dict(error="%s: %s" % (type(e).__name__, str(e)[:60]))
    out = []
    for spec in specs:
        rid = spec.get("id")
        fn = ladder.MEASURE.get(rid)
        m, unmeasured = {}, True
        if fn:
            unmeasured = False
            try:
                m = fn() or {}
            except Exception as e:
                m = dict(why="%s: %s" % (type(e).__name__, str(e)[:70]))
        out.append(dict(id=rid, title=spec.get("title"), human=spec.get("human"),
                        power=spec.get("power"), bound=spec.get("bound"), gate=spec.get("gate"),
                        plain=spec.get("plain"), beat=spec.get("beat"),
                        blocked_on=spec.get("blocked_on"),
                        funcs=list(ladder.RUNG_FUNCS.get(rid) or []),
                        measured=m, unmeasured=unmeasured, met=bool(m.get("met")),
                        journey=journey(rid)))
    st = grid.load_json(os.path.join(grid.STATE, "aea_state.json"), {})
    return dict(schema="aea.dossier/1",
                at=__import__("time").strftime("%Y-%m-%d %H:%M:%S UTC",
                                               __import__("time").gmtime()),
                tick=st.get("tick"), rungs=out, wiring=wiring)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    d = build()
    if "--write" in sys.argv:
        p = os.path.join(grid.STATE, "ladder_dossier.json")
        grid.atomic_save_json(p, d, indent=1)
        print("wrote %s" % p)
    for r in d["rungs"]:
        j = r["journey"]
        print("  %-5s %-32s %-11s funcs=%-2d journey=%s"
              % (r["id"], str(r["title"])[:32],
                 "UNMEASURED" if r["unmeasured"] else ("met" if r["met"] else "not met"),
                 len(r["funcs"]),
                 ("%d rows" % len(j["rows"])) if j["rows"] else "-"))
    print("\n  wiring: checked=%s missing=%s unwired=%s"
          % (d["wiring"].get("checked"), len(d["wiring"].get("missing") or []),
             len(d["wiring"].get("unwired") or [])))
