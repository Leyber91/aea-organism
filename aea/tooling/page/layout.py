"""layout.py - GEOMETRY, and no meaning. Where each mark goes, and nothing about what it says.

Coordinates are computed ONCE per build and never per frame: a mark that moves when its data has
not changed cannot be read (Heer & Robertson, InfoVis 2007; Misue et al, JVLC 1995). This module is
where that rule is kept, which is why it holds no colours, no captions and no state.
"""
from __future__ import annotations

import math

def _pkg(node: str) -> str:
    parts = node.split(":")[0].split(".")
    return parts[1] if len(parts) > 1 else "?"


PKG_HUE = {"loop": 38, "kernel": 44, "mind": 28, "energy": 50, "memory": 20, "organs": 34,
           "io": 24, "server": 15, "bench": 46, "tooling": 42, "lab": 30}


def _tree(org: dict) -> dict:
    """A REAL TREE, not an arc. Root is the wake; every node hangs under the parent that first
    reached it; angle is allocated by SUBTREE SIZE so siblings cluster and the shape is organic.

    The first version allocated angle by PACKAGE, which produced a lopsided crescent - `kernel` and
    `loop` hold most of the functions, so they ate the circle and the rest was empty space. It drew
    a bar chart bent into a ring, and Luis's whole point was that he could not see how the parts are
    LAID. A tidy radial tree shows exactly that: what the wake calls, what those call, outward."""
    from aea.tooling import assembly
    mods = assembly.scan()
    live = set(org["live"])
    entries = [e for e in assembly.ENTRIES["wake"] if e in live]
    root = "aea.loop.live:main" if "aea.loop.live:main" in live else (entries[0] if entries else None)
    if root is None:
        return dict(pos={}, tree=[], cross=[], root=None)

    # EVERY NODE HANGS WHERE IT TRULY BELONGS, AND THE PICTURE MAY NOT LIE.
    #
    # The first version BFS'd from `live:main` alone and then attached everything else to the root
    # "so nothing is silently dropped". Rendering it showed what that means: a dense fan of sixty
    # nodes radiating straight out of the wake, drawn exactly like real direct calls. The wake does
    # not call those sixty things. A drawing that cannot be told apart from a false claim is worse
    # than no drawing, because a picture is believed faster than a sentence.
    #
    # So: a synthetic ENTRY root, the REAL entry points as its children, BFS from all of them at
    # once. Anything still unreached is live only through a module body and is drawn in its own
    # arc, labelled as such, rather than borrowed by the wake.
    # DIRECT CALLS FIRST, DISPATCH SECOND, and the order is the claim. A node reached both ways
    # hangs off the direct caller, so a branch is only drawn as a dispatch when that is the only
    # way the organism gets there. Without this pass the thirteen table-invoked functions would
    # have fallen through to the `VIA-IMPORT` arc, which says "live only through a module body" -
    # a label that is false about every one of them.
    root = "ENTRY"
    kids, seen = {root: list(entries)}, set(entries) | {root}
    dbranch = set()
    frontier = list(entries)
    while frontier:
        nxt = []
        for kind in ("calls", "dcalls"):
            for n in frontier:
                m, _, f = n.partition(":")
                for c in sorted(mods.get(m, {}).get("defs", {}).get(f, {}).get(kind, [])):
                    if c in live and c not in seen:
                        seen.add(c); kids.setdefault(n, []).append(c); nxt.append(c)
                        if kind == "dcalls":
                            dbranch.add(c)
        frontier = nxt
    stray = sorted(n for n in live if n not in seen)
    if stray:
        kids[root] = list(kids[root]) + ["VIA-IMPORT"]
        kids["VIA-IMPORT"] = stray
        seen.add("VIA-IMPORT"); seen.update(stray)

    leaves = {}

    def count(n):
        ch = kids.get(n) or []
        leaves[n] = max(1, sum(count(c) for c in ch)) if ch else 1
        return leaves[n]
    count(root)

    # ADAPTIVE RING. `ring = 96` times a max depth of 6 puts nodes at radius 576 inside a viewBox
    # whose half-width is 500 - MEASURED: x ran from -54.4 to 1054.4 and THREE live functions were
    # drawn off-canvas, invisible, on a page whose tag says every mark is live system truth.
    # Budget now: tree 0-372, planned band 392-408, dead field 430-492, all inside 500 at any depth.
    _maxd = 1
    def _probe(n, d):
        nonlocal _maxd
        _maxd = max(_maxd, d)
        for c in (kids.get(n) or []):
            _probe(c, d + 1)
    _probe(root, 0)
    pos, depth, ring = {}, {root: 0}, 372.0 / max(1, _maxd)

    def place(n, a0, a1, d):
        a = (a0 + a1) / 2
        r = d * ring
        pos[n] = (round(500 + r * math.cos(a), 1), round(500 + r * math.sin(a), 1))
        depth[n] = d
        ch = kids.get(n) or []
        if not ch:
            return
        span, cur = a1 - a0, a0
        for c in ch:
            w = span * leaves[c] / leaves[n]
            place(c, cur, cur + w, d + 1)
            cur += w
    place(root, -math.pi / 2, 3 * math.pi / 2, 0)

    # ANGULAR SECTOR PER PACKAGE, so the dark halo can be read: a package whose live nodes sit at
    # angle X gets its dead nodes at angle X too, and the lit/dark ratio becomes visible per package.
    secs, span = {}, {}
    for n, (x, y) in pos.items():
        a = math.atan2(y - 500, x - 500) % (2 * math.pi)
        span.setdefault(_pkg(n), []).append(a)
    for k, v in span.items():
        secs[k] = (min(v), max(v)) if max(v) - min(v) < math.pi else (0.0, 2 * math.pi)

    tree = [(p, c) for p, ch in kids.items() for c in ch]
    tset = {(p, c) for p, c in tree}
    cross = [(a, b) for a, b in org["edges"]
             if (a, b) not in tset and a in pos and b in pos]
    # WHICH RUNG DECLARES THIS FUNCTION - the FUNCTIONAL axis, beside the structural one. The two
    # answer different questions: hop depth says "what calls what" and covers all 143; rung says
    # "what capability is this part of" and covers 28. Both are true, neither replaces the other,
    # and the page must never let a viewer mistake the 20% for the whole.
    #
    # THERE IS EXACTLY ONE RUNG VOCABULARY AND IT IS `ladder.json`. This map was built from
    # `assembly.STEPS` while the CLIMB below was built from `ladder.json`, so ONE PAGE carried two
    # ladders: the rail read R2 / R3.1 / R3.2 / R3.3 / R3.4 (five steps, beginning at R2) while the
    # climb read R0 ... R9 (eleven rungs, beginning at the root). They agreed about 12 of the 29
    # functions they between them named, so a circle could be R3.2 on one axis and R2 on the other.
    # That is discovery D14 - the architecture describing the same climb more than once and nothing
    # checking the descriptions against each other - reproduced INSIDE a single instrument.
    #
    # `assembly.STEPS` keeps its own job (the WHAT IS WIRED manifest, which is about wiring and not
    # about capability). It is no longer allowed to name a rung on the picture.
    lr = (org or {}).get("lr") or {}
    rung = {}
    for n in pos:
        k = lr.get(n.replace("aea.", "", 1))
        if k is not None:
            rung[n] = k
    return dict(pos=pos, tree=tree, cross=cross, root=root, depth=depth, leaves=leaves,
                sectors=secs, maxd=_maxd, rung=rung, lr=lr, dbranch=dbranch,
                dispatched=(org or {}).get("dispatched") or set(),
                standby=(org or {}).get("standby") or {})


pkg = _pkg
tree = _tree
