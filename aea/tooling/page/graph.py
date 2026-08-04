"""graph.py - THE LIVE CALL GRAPH, computed from the tree every build. Never stored.

One job: ask `assembly` what the running entity can reach, and return it with the two strengths of
evidence kept apart - a direct call edge, and an edge that only exists through a dispatch table.
"""
from __future__ import annotations


def organism(lr=None, standby=None) -> dict:
    """The live call graph, and the field it sits inside. Computed, not stored."""
    from aea.tooling import assembly
    mods = assembly.scan()
    # TWO STRENGTHS OF EVIDENCE, KEPT APART. A function invoked out of a module-level table has no
    # call site, so it read as dead while running - `hands._read_state` has 68 ledger invocations
    # and was drawn in the dark field. The edge is real and it is weaker than a direct call, because
    # which entry a dispatch selects is a runtime fact. The picture draws both and marks which.
    live, unresolved, via = assembly.reachable(mods, detail=True)
    # THE DARK FIELD IS NOT ONE THING, and drawing it as one was the biggest untruth left in the
    # picture. `assembly` already buckets `if __name__ == "__main__"` separately, on the grounds
    # that a person typing a command is not the organism - so the tree divides three ways, not two:
    # what the loop reaches, what only a HUMAN AT A TERMINAL can reach, and what nothing reaches at
    # all. Measured here: the middle group is the largest of the three. This repo is mostly
    # instruments somebody runs by hand, and until now the page drew all of them as absence.
    mains = ["%s:<main>" % m for m, i in mods.items() if "<main>" in i["defs"]]
    human, _hu = assembly.reachable(mods, entries=mains) if mains else (set(), 0)
    allfns = {f"{m}:{d}" for m, i in mods.items() for d in i["defs"] if d not in ("<module>", "<main>")}
    live = {k for k in live if k in allfns}
    dispatched = {k for k in via["dispatch"] if k in allfns}
    human = {k for k in human if k in allfns} - live

    # DEPTH FROM THE ENTRY POINTS, by BFS over real call edges. Depth is the radius, so the picture
    # reads outward from the thing that starts: the wake.
    entries = [e for e in assembly.ENTRIES["wake"] if e in live]
    depth = {e: 0 for e in entries}
    frontier = list(entries)
    while frontier:
        nxt = []
        for node in frontier:
            m, _, f = node.partition(":")
            slot = mods.get(m, {}).get("defs", {}).get(f, {})
            for c in list(slot.get("calls", [])) + list(slot.get("dcalls", [])):
                if c in live and c not in depth:
                    depth[c] = depth[node] + 1
                    nxt.append(c)
        frontier = nxt
    for k in live:
        depth.setdefault(k, max(depth.values(), default=0) + 1)

    edges, dedges = [], set()
    for m, i in mods.items():
        for f, d in i["defs"].items():
            src = f"{m}:{f}"
            if src not in live:
                continue
            for c in d["calls"]:
                if c in live and c != src:
                    edges.append((src, c))
            for c in d.get("dcalls", []):
                if c in live and c != src:
                    edges.append((src, c))
                    dedges.add((src, c))
    return dict(lr=lr, standby=standby or {}, live=sorted(live), dead=sorted(allfns - live),
                human=human, cli_modules=len(mains),
                edges=edges, dedges=dedges, dispatched=dispatched, depth=depth,
                modules=len(mods), functions=len(allfns), unresolved=unresolved,
                direct=len({k for k in via["direct"] if k in allfns}))
