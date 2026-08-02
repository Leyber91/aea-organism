"""render.py - THE ORCHESTRATOR. Reads state, computes the two axes, hands the template its inputs.

WHAT THIS FILE IS NOT ALLOWED TO CONTAIN: a number, a colour, a selector, or a sentence. It was a
494-line `build()` holding all four - state loading, graph maths, CSS generation, and the whole HTML
document - and the cost was not ugliness. It was that the rail's arithmetic and the caption's
arithmetic sat forty lines apart inside one function and disagreed for a week, which is precisely
the failure a long function hides: two things that must agree, with nothing between them that could
notice they do not.

THE ORDER MATTERS AND IT IS THE ONE THING THIS FILE DECIDES. The rung map is built BEFORE the graph
because `graph.organism()` tags nodes as it walks them - the picture is labelled while it is drawn,
never decorated afterwards, so a node cannot be given a rung the walk did not actually reach.
"""
from __future__ import annotations

import json
import time

from aea.tooling.page import (assets, axes, climb, graph, layout, marks, panels,
                              sources, style, template)


def build_site() -> dict:
    lad = sources.load("ladder.json", {})
    cert = sources.load("redteam_cert.json", {})
    asm = sources.load("assembly.json", {})
    cen = sources.load("capability_census.json", {})

    # FUNCTION -> RUNG, lowest wins, and the standby map beside it. Names are checked against the
    # live call graph by `ladder.verify_funcs()`; a non-empty `funcs_check.missing` means the build
    # is describing code that is not there.
    lr, sby = {}, {}
    for k, r in enumerate(lad.get("rungs") or []):
        for f in (r.get("funcs") or []):
            lr.setdefault(f, k)
        for f in (r.get("standby") or []):
            sby.setdefault(f, k)

    org = graph.organism(lr, sby)
    T = layout.tree(org)

    climb_html, climb_css = climb.render(lad)
    maxd, per_hop, cum = axes.hop_series(T)
    rungs, per_rung, rcum = axes.rung_series(lad, T)
    rest = axes.rung_rest(rungs)

    caps = axes.hop_captions(T, maxd, per_hop)
    rcaps = axes.rung_captions(rungs, T, per_rung, rcum)

    html = template.document(
        stamp=time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        org=org, T=T, _svg=marks.svg,
        MAXD=maxd,
        rail=axes.hop_rail(maxd, per_hop, cum),
        rrail=axes.rung_rail(rungs, per_rung, rcum, rest),
        caps=caps,
        climb_html=climb_html, n_rungs=len(rungs),
        step_rows=panels.step_rows(asm),
        growth=panels.growth(sources.history()),
        live_n=len(org["live"]), fn_n=org["functions"], cen=cen,
        **dict(zip(("rod_rows", "rods", "frontier", "mx"), panels.fleet(cen))),
        **panels.certificate(cert))

    # A SITE, NOT A FILE. Each part is written where it belongs and linked, so a copy change is a
    # diff of the markup instead of a diff buried under 1,226 unchanged dots.
    return {
        "index.html": html,
        "assets/base.css": assets.base_css(),
        "assets/frames.css": style.frame_rules(len(rungs), maxd, climb_css),
        "assets/page.js": assets.page_js(caps_js=json.dumps(caps), rcaps=rcaps,
                                         MAXD=maxd, RREST=rest),
        "assets/field.svg": marks.field(org, T),
    }


def build() -> str:
    """The page alone, for callers that only want the document. The site is `build_site()`."""
    return build_site()["index.html"]
