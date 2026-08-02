"""style.py - THE GENERATED STYLESHEET. One CSS rule per (frame, layer) pair, written out.

THE ENTIRE STATE OF THE INSTRUMENT IS ONE INTEGER ATTRIBUTE over coordinates computed once, and
this file is why: every frame of both axes exists as a static rule, so stepping is an attribute
write and stepping BACKWARD is exactly symmetric and free. No per-frame relayout, no replayed
arrival, no residue. A mark must not move when its data has not changed (Heer & Robertson, InfoVis
2007; Misue et al, JVLC 1995), and the surest way to obey that is to have nothing able to move it.

THE HOP AXIS REVEALS AND THE RUNG AXIS ACCUMULATES, and that difference is a claim rather than a
style. A hop is a slice of a structure that already exists, so shallower hops are context and the
current one is the arrival. A rung was BUILT ON the rungs beneath it, so everything below stays
lit and later rungs are not drawn AT ALL - drawing them faint would be a claim about the future.

THERE USED TO BE A THIRD MODE. `climb` had its own attribute (`data-climb`) and its own copy of
these accumulation rules keyed on a second rung vocabulary, driven by a control the mode buttons
did not know about. Measured on the rendered page: the landing view drew the climb's near-empty
frame under a caption from a third source while the rail said HOP 6. One mode, one attribute, one
integer, two rails onto it - and the absence of that duplicate is the fix.
"""
from __future__ import annotations

from aea.tooling.page.climb import CLIMB_BASE_CSS


def frame_rules(n_rungs: int, maxd: int, climb_css: str = "") -> str:
    """Every frame of both axes, as static CSS."""
    out = []

    # --- BY RUNG: nothing declared is drawn until its rung arrives, then it stays -----------------
    out.append('#org[data-mode="rung"] .node{fill:#222930;opacity:.26}')
    out.append('#org[data-mode="rung"] .branch{opacity:.05}')
    out.append('#org[data-mode="rung"] .cross{opacity:0}')
    out.append('#org[data-mode="rung"] .node[data-r]{opacity:0}')
    out.append('#org[data-mode="rung"] .branch[data-r]{opacity:0}')
    out.append('#org[data-mode="rung"] .node,#org[data-mode="rung"] .branch'
               '{transition:opacity .5s ease,fill .5s ease,r .5s ease,stroke .5s ease}')
    for k in range(n_rungs):
        for d in range(k + 1):
            out.append(f'#org[data-mode="rung"][data-frame="{k}"] .node[data-r="{d}"]'
                       f'{{opacity:.95;fill:{"var(--amber)" if d == k else "#818b96"}}}')
            out.append(f'#org[data-mode="rung"][data-frame="{k}"] .branch[data-r="{d}"]'
                       f'{{opacity:{".85" if d == k else ".30"};'
                       f'stroke:{"var(--amber)" if d == k else "#4d555e"}}}')
        out.append(f'#org[data-mode="rung"][data-frame="{k}"] .node[data-r="{k}"]{{r:4.4px}}')
        # THE STANDBY DOTS LIGHT ONLY ON THEIR OWN RUNG, in brass, out in the field where they
        # actually live. On every other frame they are one more dot in the dark, which is exactly
        # what they are to the running organism. Brass and not amber: amber is the FIRED state
        # under the two-ink law and none of these has ever run.
        out.append(f'#org[data-mode="rung"][data-frame="{k}"] .standby[data-r="{k}"]'
                   f'{{fill:var(--brass);r:2.6px;opacity:.95}}')

    # --- BY CALL HOP: shallower is context, exactly k is the arrival, deeper is not there yet ----
    for k in range(maxd + 1):
        for d in range(k + 1, maxd + 1):
            out.append(f'#org[data-mode="hop"][data-frame="{k}"] .node[data-d="{d}"]'
                       f'{{fill:#191d22;opacity:.28;r:1.2px}}')
            out.append(f'#org[data-mode="hop"][data-frame="{k}"] .branch[data-d="{d}"],'
                       f'#org[data-mode="hop"][data-frame="{k}"] .cross[data-d="{d}"]{{opacity:0}}')
        out.append(f'#org[data-mode="hop"][data-frame="{k}"] .node[data-d="{k}"]'
                   f'{{fill:var(--amber)}}')
        out.append(f'#org[data-mode="hop"][data-frame="{k}"] .branch[data-d="{k}"]'
                   f'{{stroke:var(--amber);opacity:.92}}')

    return "\n".join(out) + CLIMB_BASE_CSS + climb_css
