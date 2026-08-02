"""page - THE ORGANISM, DRAWN FROM ITS OWN STATE. One job per module.

    sources    every read of durable state, and what an absent store looks like
    graph      the live call graph, direct edges kept apart from dispatch edges
    layout     geometry: where each mark goes, and nothing about what it means
    marks      layout into SVG, the only module that emits a mark
    axes       the two axes as series - hop arrivals, rung accumulation, captions, rails
    climb      the ladder as accumulating layers, and the stylesheet that stacks them
    style      one generated CSS rule per (frame, layer), so state is one integer
    panels     the number panels: certificate, wiring, fleet, growth
    template   the page as text, with its inputs as a signature
    render     the orchestrator, which is allowed to contain none of the above
    guard      the privacy scan, run on the rendered output

KEPT DELIBERATELY THIN. `assembly.scan()` skips `__init__.py`, so anything living here is invisible
to the instrument this very package draws - a module that cannot be seen by the organism's own map
is the last place to put code.
"""
from __future__ import annotations

from aea.tooling.page.graph import organism            # noqa: F401
from aea.tooling.page.guard import FORBIDDEN, scan     # noqa: F401
from aea.tooling.page.render import build              # noqa: F401
from aea.tooling.page.sources import OUT               # noqa: F401
