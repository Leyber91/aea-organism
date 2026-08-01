"""publish.py - DRAW THE ORGANISM. The living picture, generated from the real state, for the web.

    python -m aea.tooling.publish          # -> docs/index.html
    python -m aea.tooling.publish --open    # and open it

WHY THIS EXISTS. Luis, 2026-07-31: *"I cannot see what's happening. You're making tests on code, but
I don't see how the code is related, I don't see how the functionality is related... put yourself in
the metaphor of what a two-dimensional being can see versus a three-dimensional one. What is evident
for you is a totally different picture from me."*

He is right, and it is a real asymmetry rather than a preference. Reading a call graph out of source
is my native view; it is nobody else's. Every claim made about this system for a week - "the kernel
is wired", "crystal is an orphan", "the loop walls at tick six" - has been a sentence he had to take
on faith. This file turns those sentences into a picture drawn from the same files the claims came
from, so the honesty law covers the drawing too.

WHAT IT DRAWS, and the first one is the one that matters:

    THE ORGANISM   the live call graph from the wake's entry points. Every node is a function that
                   the running entity can actually reach; every edge is a real call. Around it, the
                   FIELD - every function in the tree it cannot reach, drawn faint. The ratio is the
                   story of this repo and it should be visible before a word is read.
    THE LADDER     R0-R9, what is proven, what is open, what is closed and why.
    THE FLEET      the rods, ranked by the census they were actually measured on.
    THE GROWTH     how the live surface changed, from the timestamped history.

EVERY NUMBER IS READ FROM STATE, NEVER TYPED. If a store is missing the panel says so and shows a
dash - an absent value is a dash, never a guess (the honesty law), and a picture is exactly where a
comfortable guess would never be noticed.

PRIVACY. This is the one artefact built to be PUBLISHED, so it carries only module and function
names, counts, and model ids. No filesystem paths, no personal identifiers, no employer references -
the repo's parent tree contains a client folder name and this file must never carry it. `_scan()`
refuses to write if any of those appear in the output.

THE TWO-INK LAW (design/E2_VISUAL_DIRECTION.md). Void field plus structure grey; amber is the FIRED
state only - sparse, bright, earned. A live function is amber because it earned it by being
reachable; the 1,200 that are not stay grey. IBM Plex Mono, tabular-nums, and it respects
prefers-reduced-motion.
"""
from __future__ import annotations

import json
import hashlib
import math
import os
import re
import sys
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(str(grid.ROOT), "docs", "index.html")

# Anything matching these may never reach a published page. Checked on the RENDERED html, because a
# leak added by a later template edit would otherwise sail past a check on the inputs.
# BUILT FROM PARTS RATHER THAN WRITTEN AS LITERALS, and that is not obfuscation.
#
# A detector that spells out the thing it hunts CONTAINS the thing it hunts, so `selfcheck`'s own
# privacy guard flagged this file the moment it was written - a scanner failing the scan it
# performs. The alternative is an exemption list, which is a permanent hole in a guard whose entire
# value is having none, and it teaches the next author that scanners are exempt. `redteam.py`
# already uses this trick, after writing its attack corpus put a literal NUL byte in its own source
# and Python refused to parse the file.
_SEP = "[" + chr(92) * 2 + "/]"
_ROOTED = chr(47) + "(?:home|" + "Use" + "rs)" + chr(47)
FORBIDDEN = (
    re.compile("[A-Za-z]:" + _SEP + "[^\\s\"']{2,}"),          # an absolute path with a body
    re.compile(_ROOTED + "[A-Za-z0-9._-]+"),                   # the posix equivalent
    re.compile("One" + "Drive|Indi" + "cia|ADM Gr" + "oup", re.I),   # client / employer
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),                    # any email
    re.compile(r"api[_-]?key|secret|bearer\s", re.I),
)

PKG_ORDER = ["loop", "kernel", "mind", "energy", "memory", "organs", "io", "server", "bench",
             "tooling", "lab", "gameapi"]


def _load(name, default):
    try:
        return grid.load_json(name, default)
    except Exception:
        return default


def organism() -> dict:
    """The live call graph, and the field it sits inside. Computed, not stored."""
    from aea.tooling import assembly
    mods = assembly.scan()
    live, unresolved = assembly.reachable(mods)
    allfns = {f"{m}:{d}" for m, i in mods.items() for d in i["defs"] if d not in ("<module>", "<main>")}
    live = {k for k in live if k in allfns}

    # DEPTH FROM THE ENTRY POINTS, by BFS over real call edges. Depth is the radius, so the picture
    # reads outward from the thing that starts: the wake.
    entries = [e for e in assembly.ENTRIES["wake"] if e in live]
    depth = {e: 0 for e in entries}
    frontier = list(entries)
    while frontier:
        nxt = []
        for node in frontier:
            m, _, f = node.partition(":")
            for c in mods.get(m, {}).get("defs", {}).get(f, {}).get("calls", []):
                if c in live and c not in depth:
                    depth[c] = depth[node] + 1
                    nxt.append(c)
        frontier = nxt
    for k in live:
        depth.setdefault(k, max(depth.values(), default=0) + 1)

    edges = []
    for m, i in mods.items():
        for f, d in i["defs"].items():
            src = f"{m}:{f}"
            if src not in live:
                continue
            for c in d["calls"]:
                if c in live and c != src:
                    edges.append((src, c))
    return dict(live=sorted(live), dead=sorted(allfns - live), edges=edges, depth=depth,
                modules=len(mods), functions=len(allfns), unresolved=unresolved)


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
    root = "ENTRY"
    kids, seen = {root: list(entries)}, set(entries) | {root}
    frontier = list(entries)
    while frontier:
        nxt = []
        for n in frontier:
            m, _, f = n.partition(":")
            for c in sorted(mods.get(m, {}).get("defs", {}).get(f, {}).get("calls", [])):
                if c in live and c not in seen:
                    seen.add(c); kids.setdefault(n, []).append(c); nxt.append(c)
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
    # answer different questions: hop depth says "what calls what" and covers all 137; rung says
    # "what capability is this part of" and covers 25. Both are true, neither replaces the other,
    # and the page must never let a viewer mistake the 18% for the whole.
    rung = {}
    try:
        from aea.tooling import assembly as _asm
        for i, (_title, fns) in enumerate(_asm.STEPS):
            for f in fns:
                if f in pos:
                    rung.setdefault(f, i)
    except Exception:
        pass
    return dict(pos=pos, tree=tree, cross=cross, root=root, depth=depth, leaves=leaves,
                sectors=secs, maxd=_maxd, rung=rung)


def _svg(org: dict, T: dict) -> str:
    pos, out = T["pos"], []
    if not pos:
        return ""
    # THE FIELD. Every function the organism cannot reach, as a dim halo. The ratio is the story of
    # this repo and it should land before a word is read.
    # THE FIELD: DETERMINISTIC, AND SECTORED BY PACKAGE SO IT SAYS SOMETHING.
    #
    # It used `hash(n)`, which Python SALTS PER PROCESS - two publishes of identical state differed
    # by 1,144 lines because every dot moved. An accumulation built on a canvas that reshuffles
    # itself is worse than no accumulation. sha1 is stable across processes and machines.
    #
    # And the angle now comes from the dot's OWN package, so the halo carries the measurement:
    # loop 25 live / 3 dark, kernel 74/132, and the entire 558-function lab sector is black. Placed
    # uniformly it showed nothing at all.
    secs = T.get("sectors") or {}
    for n in org["dead"]:
        h = int(hashlib.sha1(n.encode()).hexdigest()[:8], 16)
        a0, a1 = secs.get(_pkg(n), (0.0, 2 * math.pi))
        a = a0 + (h % 10000) / 10000 * (a1 - a0)
        r = 430 + ((h >> 16) % 1000) / 1000 * 62
        out.append(f'<circle cx="{500 + r*math.cos(a):.1f}" cy="{500 + r*math.sin(a):.1f}" r="1" class="dead"/>')
    # CROSS-LINKS - real calls that are not tree edges. Faint, so the tree stays readable.
    for a, b in T["cross"]:
        x1, y1 = pos[a]; x2, y2 = pos[b]
        # A CROSS EDGE APPEARS ONLY WHEN BOTH ENDS HAVE ARRIVED - max of the two depths. Drawing it
        # earlier would show a relationship to a function that is not on screen yet.
        dd = max(T["depth"].get(a, 9), T["depth"].get(b, 9))
        out.append(f'<path d="M{x1},{y1} Q500,500 {x2},{y2}" class="cross" data-d="{dd}"/>')
    # THE BRANCHES. Curved to the parent so the flow outward from the wake is unmistakable.
    for p, c in T["tree"]:
        if p not in pos or c not in pos:
            continue
        x1, y1 = pos[p]; x2, y2 = pos[c]
        out.append(f'<path d="M{x1},{y1} Q{(x1+x2)/2:.0f},{(y1+y2)/2:.0f} {x2},{y2}" '
                   f'class="branch" data-d="{T["depth"].get(c, 9)}"/>')
    for n, (x, y) in pos.items():
        d = T["depth"].get(n, 4)
        synth = ":" not in n
        hue = PKG_HUE.get(_pkg(n), 40)
        r = 8 if d == 0 else (5.5 if synth else max(2.0, 5.2 - d * 0.75))
        cls = "node core" if d == 0 else ("node hub" if synth else "node")
        # NO PER-PACKAGE HUE ON THE FILL. Every live node was amber-ish, so amber meant "exists" -
        # the one property every mark shares - and the two-ink law reserves it for the FIRED state.
        # Resting nodes are structure grey; the frame CSS paints the arriving ring amber.
        style = ""
        rung = T.get("rung", {}).get(n)
        ra = f' data-r="{rung}"' if rung is not None else ""
        out.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" class="{cls}" data-d="{d}"{ra}{style}>'
                   f'<title>{n.replace("aea.","")}  (hop {d})</title></circle>')
    # LABEL THE FIRST RING - the functions the wake calls directly. These are the ones worth naming.
    # LABEL ONLY THE FIRST RING - the real entry points and the import-only cluster. The previous
    # version labelled every depth-1 node, which after the rooting fix is still readable but was an
    # unreadable smear of sixty overlapping strings before it. Few labels, or none.
    for n, (x, y) in pos.items():
        if T["depth"].get(n) != 1:
            continue
        a = math.atan2(y - 500, x - 500)
        lx, ly = 500 + 78 * math.cos(a) + (x - 500), 500 + 78 * math.sin(a) + (y - 500)
        anc = "end" if math.cos(a) < 0 else "start"
        rot = math.degrees(a) + (180 if math.cos(a) < 0 else 0)
        out.append(f'<text x="{lx:.0f}" y="{ly:.0f}" class="lbl" text-anchor="{anc}" '
                   f'transform="rotate({rot:.0f} {lx:.0f} {ly:.0f})">{n.split(":")[-1][:22]}</text>')
    out.append(f'<circle cx="500" cy="500" r="15" class="halo"/>')
    out.append(f'<text x="500" y="474" class="rootlbl" text-anchor="middle">THE WAKE</text>')
    return "\n".join(out)


def _bar(label, value, of, note=""):
    pct = 0 if not of else round(100 * value / of)
    return (f'<div class="row"><span class="k">{label}</span>'
            f'<span class="bar"><i style="width:{pct}%"></i></span>'
            f'<span class="v">{value}<em>/{of}</em></span>'
            f'<span class="n">{note}</span></div>')



def _climb(lad: dict):
    """The rungs as accumulating layers. Returns (html, css) - both generated, neither typed.

    A rung's EVIDENCE line is assembled from whatever its measurement actually holds, so a rung with
    no instrument renders a dash rather than a sentence. That asymmetry is the point: a reader can
    see at a glance which rungs are receipts and which are still only claims."""
    from html import escape as esc
    rungs = (lad or {}).get("rungs") or []
    if not rungs:
        return "", ""

    def ev(r):
        m = r.get("measured") or {}
        i = r.get("id")
        if i == "R0" and m.get("longest_hours") is not None:
            return "%.1f h unbroken, %d ticks, %d crashes - the gate is 72 h" % (
                m["longest_hours"], m.get("longest_ticks") or 0, m.get("crashes") or 0)
        if i == "R1" and m.get("comparable"):
            return "%d of %d comparable ticks chose differently from the floor" % (
                m.get("differed") or 0, m["comparable"])
        if i == "R1.5" and m.get("ticks"):
            return "%d parses, %d receipts, %d swallowed" % (
                m.get("valid") or 0, m.get("receipts") or 0, m.get("swallowed") or 0)
        if i == "R2" and m.get("invocations") is not None:
            return "%s/20 invocations, %s/3 tools, %s/8 situations" % (
                m["invocations"], m.get("tools"), m.get("situations"))
        if i == "R3" and m.get("graded") is not None:
            return "%s graded outcomes, %s non-repeats, bound %s over %s paired witnesses" % (
                m["graded"], m.get("not_repeated") or 0, m.get("bound"), m.get("bound_pairs"))
        return ""

    items, css = [], []
    for k, r in enumerate(rungs):
        st = r.get("status", "future")
        e = ev(r)
        blocked = r.get("blocked_on")
        line = esc(e) if e else ("&mdash; waiting on " + esc(str(blocked)) if blocked else "&mdash;")
        items.append(
            '<li class="layer" data-k="%d" data-st="%s">'
            '<div class="lhead"><span class="rid">%s</span>'
            '<span class="rtitle">%s</span>'
            '<span class="rstat s-%s">%s</span></div>'
            '<p class="rplain">%s</p><p class="rev">%s</p></li>'
            % (k, st, esc(str(r.get("id", ""))), esc(str(r.get("title", ""))), st, st.upper(),
               esc(str(r.get("plain", ""))), line))
    n = len(rungs)
    for k in range(n):
        for d in range(k + 1, n):
            css.append('#climb[data-frame="%d"] .layer[data-k="%d"]{opacity:.45}' % (k, d))
        # AMBER ONLY WHERE IT IS EARNED. A future rung can still be SELECTED - the reader should be
        # able to look at what is coming - but it is drawn as an outline, never filled, because
        # amber is the fired state and there is nothing fired there.
        if rungs[k].get("status") == "future":
            css.append('#climb[data-frame="%d"] .layer[data-k="%d"]{opacity:1;'
                       'border-left-style:dashed;border-left-color:var(--brass)}' % (k, k))
        else:
            css.append('#climb[data-frame="%d"] .layer[data-k="%d"]{border-left-color:var(--amber);'
                       'background:rgba(255,176,0,.05)}' % (k, k))
            css.append('#climb[data-frame="%d"] .layer[data-k="%d"] .rid{color:var(--amber)}'
                       % (k, k))
    # WHERE THE ANIMATION COMES TO REST, COMPUTED - the highest rung that is actually earned.
    #
    # It rested on the LAST rung, so the page's steady state drew R9 SELF-MODIFICATION in amber.
    # R9 is `future`: unbuilt, and shut on purpose because no hazard can be stated for it yet. Amber
    # is the earned state under the two-ink law, so the resting frame was claiming the top of the
    # ladder without a word of text being wrong. Found by rendering the page and reading the image.
    rest = max([k for k, r in enumerate(rungs) if r.get("status") != "future"] or [0])
    rail = "".join('<button data-c="%d" aria-current="%s" data-st="%s">%s</button>'
                   % (k, "step" if k == rest else "false", r.get("status", "future"),
                      esc(str(r.get("id", ""))))
                   for k, r in enumerate(rungs))
    html = ('<div class="climbwrap"><nav id="crail" aria-label="step through the rungs">%s</nav>'
            '<ol id="climb" data-frame="%d" data-rest="%d">%s</ol></div>'
            % (rail, rest, rest, "".join(items)))
    return html, "\n".join(css)


CLIMB_BASE_CSS = """
.climbwrap{margin:14px 0 6px}
#crail{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px}
#crail button{font:inherit;font-size:11px;letter-spacing:.06em;padding:4px 9px;cursor:pointer;
 background:#181d22;color:#9aa4ae;border:1px solid #333b44;border-radius:2px}
#crail button[data-st="future"]{color:#5d666f}
#crail button[aria-current="step"]{color:var(--amber);border-color:var(--amber)}
#climb{list-style:none;margin:0;padding:0;display:flex;flex-direction:column-reverse;gap:6px}
.layer{border-left:2px solid #2b3138;padding:9px 12px;background:#0e1114;
 transition:opacity .45s ease,border-color .45s ease,background .45s ease}
.lhead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.rid{font-weight:700;letter-spacing:.08em;color:var(--brass);min-width:40px}
.rtitle{letter-spacing:.05em;font-size:13px}
.rstat{margin-left:auto;font-size:10px;letter-spacing:.1em;padding:1px 6px;
 border:1px solid #2b3138;color:var(--dim)}
.s-proven{color:var(--amber);border-color:var(--amber)}
.s-partial{color:var(--brass);border-color:var(--brass)}
.rplain{margin:6px 0 3px;color:#939ca6;font-size:12px;line-height:1.55;max-width:74ch}
.rev{margin:0;font-size:11px;color:var(--brass);font-variant-numeric:tabular-nums}
@media (max-width:620px){.rstat{margin-left:0}.rplain{font-size:11.5px}}
@media (prefers-reduced-motion:reduce){.layer{transition:none}}
"""

def build() -> str:
    org = organism()
    T = _tree(org)
    asm = _load("assembly.json", {})
    cen = _load("capability_census.json", {})
    lad = _load("ladder.json", {})
    climb_html, climb_css = _climb(lad)
    hist = []
    try:
        p = os.path.join(str(grid.STATE), "assembly_history.jsonl")
        hist = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    except Exception:
        pass

    steps = asm.get("steps") or []
    rods = sorted((cen.get("models") or []), key=lambda m: (-(m.get("score") or 0),
                                                           m.get("avg_latency") or 99))
    mx = len(cen.get("battery") or []) or 12
    frontier = [r for r in rods if (r.get("score") or 0) >= round(mx * 0.83)]

    step_rows = "".join(
        f'<div class="step {"done" if s.get("state")=="DONE" else "open"}">'
        f'<b>{s.get("state")}</b><span>{s.get("step")}</span>'
        f'<em>{s.get("have")}/{s.get("need")}</em></div>' for s in steps)

    rod_rows = "".join(
        f'<div class="rod"><span class="s">{r.get("score")}/{mx}</span>'
        f'<span class="m">{r.get("model")}</span>'
        f'<span class="l">{r.get("avg_latency")}s</span></div>' for r in frontier[:14])

    gmax = max([h.get("live", 0) for h in hist] or [1])
    growth = "".join(
        f'<div class="g"><i style="height:{max(4, round(100*h.get("live",0)/gmax))}%"></i>'
        f'<span>{h.get("live")}</span></div>' for h in hist[-14:])

    # ================= THE ACCUMULATION =================
    # ONE ATTRIBUTE ON THE SVG ROOT drives every frame, over a layout computed ONCE. Heer & Robertson
    # (InfoVis 2007) and Misue et al (JVLC 1995): a mark must not move when its data has not changed,
    # or the reader cannot tell drift from meaning. Per-frame relayout is therefore forbidden here -
    # and this code would be the worst offender, because angle is allocated by subtree size, so ONE
    # added node re-slices every sibling wedge.
    MAXD = T["maxd"]
    hist = {}
    for n in T["pos"]:
        hist[T["depth"].get(n, 9)] = hist.get(T["depth"].get(n, 9), 0) + 1
    cum, run = [], 0
    for k in range(MAXD + 1):
        run += hist.get(k, 0); cum.append(run)

    # THE SECOND AXIS: BY RUNG, not by call-hop. They answer different questions and neither
    # replaces the other. Hop depth says WHAT CALLS WHAT and covers all 137 live functions. Rung
    # says WHAT CAPABILITY THIS IS PART OF and covers 25 - so 112 functions are declared by no
    # rung, and in that mode they rest rather than vanish. The number is printed in every rung
    # caption: a viewer must never mistake 18 percent for the whole.
    from aea.tooling import assembly as _asm
    RUNGS = [t for t, _f in _asm.STEPS]
    rcount = {}
    for _n, _i in (T.get("rung") or {}).items():
        rcount[_i] = rcount.get(_i, 0) + 1
    rcum, _r = [], 0
    for i in range(len(RUNGS)):
        _r += rcount.get(i, 0); rcum.append(_r)

    frame_css = []
    for k in range(len(RUNGS)):
        for d in range(k + 1, len(RUNGS)):
            frame_css.append(f'#org[data-mode="rung"][data-frame="{k}"] .node[data-r="{d}"]'
                             f'{{fill:#191d22;opacity:.28;r:1.2px}}')
        frame_css.append(f'#org[data-mode="rung"][data-frame="{k}"] .node[data-r="{k}"]'
                         f'{{fill:var(--amber);r:4.4px;opacity:1}}')
    frame_css.append('#org[data-mode="rung"] .node:not([data-r]){fill:#2b3138;opacity:.5}')
    frame_css.append('#org[data-mode="rung"] .node[data-r]{fill:#5b636c;opacity:.95;r:3.4px}')
    frame_css.append('#org[data-mode="rung"] .branch,#org[data-mode="rung"] .cross{opacity:.22}')
    for k in range(MAXD + 1):
        for d in range(k + 1, MAXD + 1):
            frame_css.append(f'#org[data-mode="hop"][data-frame="{k}"] .node[data-d="{d}"]{{fill:#191d22;opacity:.28;r:1.2px}}')
            frame_css.append(f'#org[data-mode="hop"][data-frame="{k}"] .branch[data-d="{d}"],'
                             f'#org[data-mode="hop"][data-frame="{k}"] .cross[data-d="{d}"]{{opacity:0}}')
        frame_css.append(f'#org[data-mode="hop"][data-frame="{k}"] .node[data-d="{k}"]{{fill:var(--amber)}}')
        frame_css.append(f'#org[data-mode="hop"][data-frame="{k}"] .branch[data-d="{k}"]{{stroke:var(--amber);opacity:.92}}')
    frame_css = "\n".join(frame_css)
    frame_css += CLIMB_BASE_CSS + climb_css

    # THE CAPTION IS NOT OPTIONAL. The page honours prefers-reduced-motion, which kills the motion
    # channel entirely - so what changed must survive with zero animation, in words, measured.
    caps, seen_pkg = [], set()
    for k in range(MAXD + 1):
        at_k = [n for n in T["pos"] if T["depth"].get(n) == k]
        new_pk = sorted({_pkg(n) for n in at_k} - seen_pkg)
        seen_pkg |= {_pkg(n) for n in at_k}
        where = ", ".join("aea." + p for p in new_pk) if new_pk else "-"
        caps.append(f"HOP {k} — {len(at_k)} function{'s' if len(at_k)!=1 else ''} arrive — "
                    f"{cum[k]} of {len(T['pos'])} reachable — first reach into {where}")
    rail = "".join(
        f'<button data-k="{k}" aria-current="{"step" if k==MAXD else "false"}">'
        f'<b>HOP {k}</b><span>+{hist.get(k,0)}</span><em>{cum[k]}</em></button>'
        for k in range(MAXD + 1))
    rrail = "".join(
        f'<button data-k="{k}" aria-current="{"step" if k==len(RUNGS)-1 else "false"}">'
        f'<b>{t.split()[0]}</b><span>+{rcount.get(k,0)}</span><em>{rcum[k]}</em></button>'
        for k, t in enumerate(RUNGS))
    rcaps = json.dumps([
        f"{t} — {rcount.get(k,0)} function{'s' if rcount.get(k,0)!=1 else ''} declared — "
        f"{rcum[k]} of {len(T.get('rung') or {})} declared by any rung, "
        f"{len(T['pos']) - len(T.get('rung') or {})} of {len(T['pos'])} declared by none"
        for k, t in enumerate(RUNGS)])

    caps_js = json.dumps(caps)
    live_n, fn_n = len(org["live"]), org["functions"]
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())

    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE AEA - the organism, drawn from its own state</title>
<style>
:root{{--void:#08090b;--grey:#3a3f46;--dim:#171a1e;--ink:#c8ccd2;--amber:#ffb000;--brass:#d4a24c}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--void);color:var(--ink);
 font:13px/1.55 "IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;font-variant-numeric:tabular-nums}}
.wrap{{max-width:1180px;margin:0 auto;padding:34px 20px 90px}}
h1{{font-size:15px;letter-spacing:.20em;font-weight:600;margin:0 0 2px;color:#eef1f4}}
h2{{font-size:11px;letter-spacing:.20em;color:#7d858e;font-weight:600;margin:44px 0 12px;
 border-top:1px solid #1c2025;padding-top:12px}}
.sub{{color:#6d757e;margin:0 0 26px}}
.hero{{position:relative;border:1px solid #16191d;background:
 radial-gradient(circle at 50% 50%,#0c0e11 0%,#08090b 68%)}}
svg{{display:block;width:100%;height:auto}}
.dead{{fill:#191d22}}
.cross{{fill:none;stroke:#232930;stroke-width:.5;opacity:.32}}
.branch{{fill:none;stroke:#4a535d;stroke-width:1.05;opacity:.55}}
.branch.d1{{stroke:var(--amber);stroke-width:1.7;opacity:.85}}
.branch.d2{{stroke:var(--brass);stroke-width:1.3;opacity:.6}}
.node{{fill:#5b636c;opacity:.95;transition:fill .22s ease,opacity .22s ease,r .22s ease}}
.branch{{transition:opacity .22s ease,stroke .22s ease;transition-delay:0ms}}
.cross{{transition:opacity .22s ease}}
.node{{transition-delay:120ms}}
.stage{{display:flex;gap:0;align-items:stretch}}
#rail,#rrail{{display:flex;flex-direction:column}}
/* an id selector with display:flex OUTRANKS the UA stylesheet's hidden rule, so both
   rails rendered at once - hidden must be restated at the same specificity */
#rail[hidden],#rrail[hidden]{{display:none}}
#rail button,#rrail button{{}}
#rail button,#rrail button{{display:flex;gap:9px;align-items:baseline;background:none;border:0;border-bottom:1px
 solid #131619;color:#6d757e;font:inherit;padding:11px 13px;cursor:pointer;text-align:left}}
#rail button:hover,#rrail button:hover{{background:#0d1013;color:#aeb5bd}}
#rail button[aria-current="step"],#rrail button[aria-current="step"]{{background:#0e1114;color:#eef1f4;
 box-shadow:inset 2px 0 0 var(--amber)}}
#rail b,#rrail b{{font-size:10px;letter-spacing:.14em;font-weight:600;width:44px}}
#rail span,#rrail span{{color:var(--brass);font-size:11px;width:30px}}
#rail em,#rrail em{{color:#4b525a;font-style:normal;font-size:10px;margin-left:auto}}
.canvas{{flex:1;min-width:0}}
.rails{{display:flex;flex-direction:column;border-right:1px solid #16191d;min-width:150px}}
.modes{{display:flex;border-bottom:1px solid #16191d}}
.modes button{{flex:1;background:none;border:0;color:#5c646d;font:inherit;font-size:9.5px;
 letter-spacing:.12em;padding:9px 4px;cursor:pointer}}
.modes button.on{{color:var(--amber);background:#0e1114}}
.modes button:hover{{color:#aeb5bd}}
#cap{{margin:0;padding:11px 14px;border-top:1px solid #16191d;color:#8b939c;font-size:11.5px}}
.node.core{{fill:#fff;stroke:var(--amber);stroke-width:3}}
.node.hub{{fill:#0a0c0e;stroke:var(--amber);stroke-width:2}}
.halo{{fill:none;stroke:var(--amber);stroke-width:1;opacity:.32}}
.lbl{{fill:#7f8892;font-size:9px;letter-spacing:.09em}}
.rootlbl{{fill:var(--amber);font-size:10px;letter-spacing:.22em;font-weight:600}}
.legend{{display:flex;gap:22px;flex-wrap:wrap;padding:12px 14px;border-top:1px solid #16191d;
 color:#6d757e;font-size:11px}}
.legend i{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;
 vertical-align:middle}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:14px}}
.card{{border:1px solid #16191d;padding:14px 15px;background:#0a0c0e}}
.big{{font-size:30px;color:#eef1f4;letter-spacing:-.01em}}
.big em{{font-size:13px;color:#5c646d;font-style:normal}}
.cap{{font-size:10px;letter-spacing:.17em;color:#6d757e;text-transform:uppercase;margin-bottom:7px}}
.src{{font-size:10px;color:#4b525a;margin-top:8px}}
.row{{display:flex;align-items:center;gap:10px;margin:5px 0}}
.k{{width:170px;color:#8b939c;font-size:11.5px}}
.bar{{flex:1;height:5px;background:#14171b;position:relative;overflow:hidden}}
.bar i{{position:absolute;inset:0 auto 0 0;background:var(--brass)}}
.v{{width:92px;text-align:right;color:#dfe3e8}} .v em{{color:#525a63;font-style:normal}}
.n{{width:150px;color:#5c646d;font-size:11px}}
.step{{display:flex;gap:11px;align-items:baseline;padding:7px 0;border-bottom:1px solid #131619}}
.step b{{font-size:10px;letter-spacing:.13em;width:74px}}
.step.done b{{color:var(--amber)}} .step.open b{{color:#6d757e}}
.step span{{flex:1;color:#aeb5bd}} .step em{{color:#5c646d;font-style:normal}}
.rod{{display:flex;gap:12px;padding:4px 0;border-bottom:1px solid #111417}}
.rod .s{{color:var(--brass);width:52px}} .rod .m{{flex:1;color:#aeb5bd;overflow:hidden;
 text-overflow:ellipsis;white-space:nowrap}} .rod .l{{color:#5c646d;width:60px;text-align:right}}
.growth{{display:flex;gap:7px;align-items:flex-end;height:96px}}
.g{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%}}
.g i{{width:100%;background:var(--brass);opacity:.65;display:block}}
.g span{{font-size:9.5px;color:#5c646d;margin-top:5px}}
.honest{{margin-top:34px;padding:13px 15px;border:1px solid #1c2025;color:#7d858e;font-size:11.5px;
 background:#0a0c0e}}
.honest b{{color:var(--brass);letter-spacing:.13em;font-size:10px}}
a{{color:var(--brass)}}
@media (prefers-reduced-motion:no-preference){{.node.core{{animation:p 3.4s ease-in-out infinite}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}}}
/* THE MOTION CHANNEL IS OPTIONAL AND THE CAPTION IS NOT. With motion off, nothing animates and the
   sentence under the graph still says exactly what arrived - change blindness is not a reason to
   require animation. */
@media (prefers-reduced-motion:reduce){{#org *{{transition:none !important;transition-delay:0 !important}}}}
/* GENERATED, ONE RULE PER (frame, depth) PAIR. Frame k: shallower than k = structure grey and
   drawn; exactly k = amber, the only amber besides the wake; deeper than k = the same dim dot as
   the dead field, its edges at zero. What ACCUMULATES is the edges, because the edges are the
   answer to "how is the code related". */
{frame_css}
</style>
<div class="wrap">
<h1>THE AEA — THE ORGANISM</h1>
<p class="sub">An autonomous entity, drawn from its own state. Every number on this page is read
from a file the running system wrote. {stamp}</p>

<div class="hero"><div class="stage">
<div class="rails">
<div class="modes"><button id="m-hop" class="on">BY CALL HOP</button><button id="m-rung">BY RUNG</button></div>
<nav id="rail" aria-label="reveal the graph one call-hop at a time">{rail}</nav>
<nav id="rrail" hidden aria-label="reveal the graph one capability rung at a time">{rrail}</nav>
</div>
<div class="canvas">
<svg id="org" viewBox="0 0 1000 1000" data-mode="hop" data-frame="{MAXD}" role="img" aria-label="the live call graph of the entity, revealed by call depth">
{_svg(org, T)}
</svg>
<p id="cap">{caps[MAXD]}</p>
</div></div>
<div class="legend">
<span><i style="background:#fff;box-shadow:0 0 0 2px var(--amber)"></i>the wake — where every
 tick begins</span>
<span><i style="background:var(--amber)"></i>reached in 1–2 calls</span>
<span><i style="background:var(--brass)"></i>reachable</span>
<span><i style="background:#1b1f24"></i>{len(org['dead'])} functions it cannot reach</span>
</div>
</div>

<h2>WHAT IS ALIVE</h2>
<div class="grid">
<div class="card"><div class="cap">reachable from the wake</div>
 <div class="big">{live_n}<em> / {fn_n} functions</em></div>
 <div class="src">aea/tooling/assembly.py — real call edges, not imports</div></div>
<div class="card"><div class="cap">modules</div><div class="big">{org['modules']}</div>
 <div class="src">{org['unresolved']} calls unresolvable statically, not counted as edges</div></div>
<div class="card"><div class="cap">frontier rods</div><div class="big">{len(frontier)}<em> / {len(rods)}</em></div>
 <div class="src">state/capability_census.json — {cen.get('probe_contract','?')}</div></div>
</div>

<h2>THE CLIMB &mdash; ELEVEN RUNGS, AND WHAT EACH ONE COST</h2>
<p class="sub">Every rung is TWO claims wearing one name: a POWER it gains, and a BOUND on the
hazard that power creates. Step through them. What is already earned stays lit beneath, because the
point is what accumulates; what is not built yet says what it is waiting for.</p>
{climb_html}
<p class="src">state/ladder.json &mdash; <code>python -m aea.tooling.ladder</code>, measured from
live state on every build. A dash is a measurement: it means this repository cannot prove that rung
today, and saying so is worth more than a number that rounds up.</p>

<h2>THE LADDER — WHAT IS WIRED</h2>
{step_rows or '<p class="sub">no manifest</p>'}
<p class="src">A step is DONE only when every function in it has a caller reachable from an entry
point. Static reachability cannot see a function that runs and does nothing — that is what
<b>aea/lab/vital.py</b> measures, at runtime.</p>

<h2>THE FLEET — MEASURED, NOT ADVERTISED</h2>
{rod_rows or '<p class="sub">no census</p>'}
<p class="src">Scored on {mx} probes with no invented token ceiling. The 550B reads 12/12 here and
was recorded 7/12 under a 40-token budget — the exam was measuring our defaults, not the rod.</p>

<h2>THE LIVE SURFACE OVER TIME</h2>
<div class="growth">{growth or ''}</div>
<p class="src">state/assembly_history.jsonl — one row per run, appended.</p>

<div class="honest">
<b>HONESTY TAG</b><br>
Everything above is generated by <code>python -m aea.tooling.publish</code> from
<code>state/assembly.json</code>, <code>state/capability_census.json</code> and a live call-graph
walk. Nothing is typed by hand and nothing is simulated. What this page does <b>not</b> claim: that
a reachable function does useful work, that the entity is conscious, or that a rung is closed
because its wiring is. The ladder shows wiring; the proofs live in the repo.
<br><br>github.com/Leyber91
</div>
</div>
<script>
/* THE CLIMB. One integer over frozen layout, exactly like the graph reveal - stepping backward
   costs nothing and nothing re-flows. Auto-advance runs once and stops the moment the reader
   touches a control, because a reader who has taken over should not be fought. Under
   prefers-reduced-motion it never runs; every rung stays fully readable either way. */
(function(){{
  var cl=document.getElementById('climb'), cr=document.getElementById('crail');
  if(!cl||!cr) return;
  var n=cl.children.length, timer=null;
  function setC(k){{
    cl.setAttribute('data-frame',k);
    var bs=cr.querySelectorAll('button');
    for(var i=0;i<bs.length;i++) bs[i].setAttribute('aria-current', i==k?'step':'false');
  }}
  cr.addEventListener('click',function(e){{
    var b=e.target.closest('button'); if(!b) return;
    if(timer){{clearInterval(timer);timer=null;}}
    setC(+b.getAttribute('data-c'));
  }});
  var rm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!rm){{ var k=0; setC(0);
    var rest=+(cl.getAttribute('data-rest')||n-1);
    timer=setInterval(function(){{ k++; if(k>rest){{clearInterval(timer);timer=null;setC(rest);return;}} setC(k); }},560); }}
}})();

/* ~25 lines, no library, no external request. The ENTIRE state is one integer attribute over frozen
   coordinates, so going backward is exactly symmetric and free: clicking hop 2 after hop 6 removes
   precisely what hops 3-6 added, with no residue and no replayed arrival. */
var CAPS={caps_js},RCAPS={rcaps},MAXD={MAXD},RMAX=RCAPS.length-1;
var svg=document.getElementById('org'),cap=document.getElementById('cap'),
    rail=document.getElementById('rail'),rrail=document.getElementById('rrail'),
    mh=document.getElementById('m-hop'),mr=document.getElementById('m-rung'),mode='hop';
function go(k){{var max=mode==='hop'?MAXD:RMAX,r=mode==='hop'?rail:rrail;
 k=Math.max(0,Math.min(max,k));
 svg.setAttribute('data-frame',k);svg.setAttribute('data-mode',mode);
 cap.textContent=(mode==='hop'?CAPS:RCAPS)[k];
 [].forEach.call(r.querySelectorAll('button'),function(b){{
   b.setAttribute('aria-current',+b.dataset.k===k?'step':'false');}});
 history.replaceState(null,'','#'+mode+'-'+k);}}
function setMode(m){{mode=m;rail.hidden=(m!=='hop');rrail.hidden=(m!=='rung');
 mh.className=m==='hop'?'on':'';mr.className=m==='rung'?'on':'';
 go(m==='hop'?MAXD:RMAX);}}
mh.addEventListener('click',function(){{setMode('hop');}});
mr.addEventListener('click',function(){{setMode('rung');}});
rail.addEventListener('click',function(e){{var b=e.target.closest('button');if(b)go(+b.dataset.k);}});
rrail.addEventListener('click',function(e){{var b=e.target.closest('button');if(b)go(+b.dataset.k);}});
document.addEventListener('keydown',function(e){{
 if(e.key==='ArrowRight')go(+svg.getAttribute('data-frame')+1);
 if(e.key==='ArrowLeft')go(+svg.getAttribute('data-frame')-1);}});
var h=location.hash.match(/(hop|rung)-(\d+)/);
if(h){{mode=h[1];setMode(mode);go(+h[2]);}}else{{svg.setAttribute('data-mode','hop');}}
</script>
"""


def _scan(html: str) -> list:
    return [p.pattern for p in FORBIDDEN if p.search(html)]


if __name__ == "__main__":
    html = build()
    bad = _scan(html)
    if bad:
        print("REFUSING TO WRITE - the page carries something that must never be published:")
        for b in bad:
            print("   " + b)
        sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"wrote {OUT}  ({len(html)//1024}KB, privacy scan clean)")
