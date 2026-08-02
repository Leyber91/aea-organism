"""marks.py - LAYOUT INTO SVG. The only module that emits a mark.

It decides nothing about what is true; it is handed positions and classifications and turns them
into circles, branches and bars. Anything that reads as a claim - hollow for dispatch-reached,
brass for standby, amber for fired - is a class name here and a rule in `style`.
"""
from __future__ import annotations

import hashlib
import math

from aea.tooling.page.layout import PKG_HUE, _pkg

def _lrb(T, child):
    """A branch belongs to the rung of the node it ARRIVES at. Drawing an edge into a node that has
    not been revealed is the visual form of claiming something exists before it was built.

    ONE ATTRIBUTE. Nodes and branches both carry `data-r`, and `data-r` means one thing: the index
    of the rung in `ladder.json` that declares this function. There used to be a second attribute,
    `data-lr`, holding the other ladder's answer for the same circle."""
    k = T.get("rung", {}).get(child)
    return f' data-r="{k}"' if k is not None else ""


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
    # STANDBY, DRAWN IN THE FIELD AND NEVER IN THE BODY. A rung that has not started can still own
    # code: `dispatch.py` is R4's egress path, written, refused in its obvious shape by four council
    # seats, and left with zero callers on purpose. Before this it was one more anonymous dot in the
    # 1,182 - so "not built" and "built and deliberately held" looked the same, which is the
    # difference between an empty rung and a fenced one. Brass, not amber: amber is the fired state
    # under the two-ink law and none of these has ever run in the loop.
    standby = T.get("standby") or {}
    secs = T.get("sectors") or {}
    for n in org["dead"]:
        h = int(hashlib.sha1(n.encode()).hexdigest()[:8], 16)
        a0, a1 = secs.get(_pkg(n), (0.0, 2 * math.pi))
        a = a0 + (h % 10000) / 10000 * (a1 - a0)
        r = 430 + ((h >> 16) % 1000) / 1000 * 62
        k = standby.get(n.replace("aea.", "", 1))
        if k is None:
            out.append(f'<circle cx="{500 + r*math.cos(a):.1f}" cy="{500 + r*math.sin(a):.1f}" r="1" class="dead"/>')
        else:
            out.append(f'<circle cx="{500 + r*math.cos(a):.1f}" cy="{500 + r*math.sin(a):.1f}" '
                       f'r="1" class="dead standby" data-r="{k}">'
                       f'<title>{n.replace("aea.","")}  (written for rung {k}, zero callers)</title></circle>')
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
        _dk = " dispatch" if c in (T.get("dbranch") or ()) else ""
        out.append(f'<path d="M{x1},{y1} Q{(x1+x2)/2:.0f},{(y1+y2)/2:.0f} {x2},{y2}" '
                   f'class="branch{_dk}" data-d="{T["depth"].get(c, 9)}"'
                   f'{_lrb(T, c)}/>')
    for n, (x, y) in pos.items():
        d = T["depth"].get(n, 4)
        synth = ":" not in n
        hue = PKG_HUE.get(_pkg(n), 40)
        r = 8 if d == 0 else (5.5 if synth else max(2.0, 5.2 - d * 0.75))
        cls = "node core" if d == 0 else ("node hub" if synth else "node")
        if n in (T.get("dispatched") or ()):
            cls += " viadisp"
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


# PUBLIC NAMES. The bodies above are the same text they were inside `publish.py`, underscore
# prefixes and all - a rename would have hidden a moved line inside a diff that is supposed to
# prove nothing moved.
svg = _svg
branch_rung = _lrb
