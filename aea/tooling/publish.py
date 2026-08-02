"""publish.py - the run shim. THE CODE MOVED TO `aea/tooling/page/`; the command did not.

    python -m aea.tooling.publish          # -> docs/index.html

WHY THIS FILE STILL EXISTS AS A FILE. It was 997 lines holding five jobs - reading state, walking
the call graph, laying out the geometry, generating the stylesheet, and the entire HTML document -
with a single `build()` of 494 lines at the centre of it. The cost was never that it was ugly. It
was that the rail's arithmetic and the caption's arithmetic lived forty lines apart inside one
function and disagreed for a week, and that four certificate values were formatted on every build
and printed nowhere, and NOTHING BETWEEN THEM COULD NOTICE - which is the specific failure a long
function produces: two things that must agree, with no boundary that could tell they do not.

    aea/tooling/page/
        sources    every read of durable state, and what an absent store looks like
        graph      the live call graph, direct edges kept apart from dispatch edges
        layout     geometry: where each mark goes, and nothing about what it means
        marks      layout into SVG, the only module that emits a mark
        axes       the two axes as series - arrivals, accumulation, captions, rails
        climb      the ladder as accumulating layers, and the stylesheet that stacks them
        style      one generated CSS rule per (frame, layer), so page state is one integer
        panels     the number panels: certificate, wiring, fleet, growth
        template   the page as text, with its inputs as a derived signature
        render     the orchestrator, which is allowed to contain none of the above
        guard      the privacy scan, run on the rendered output

THE SPLIT WAS PROVED, not asserted: the monolith and the package were both built at the same tree
state and their output was compared byte for byte. Identical. A refactor of a generator has exactly
one honest control available to it and this is it.

WHY THE SHIM RATHER THAN A RENAME. `python -m aea.tooling.publish` is in CLAUDE.md, in the page's
own honesty tag, and in the handoff prompt. Moving code is not a reason to break a documented
command, and a shim that re-exports is cheaper than every caller learning a new name.
"""
from __future__ import annotations

import sys

from aea.tooling.page import guard
from aea.tooling.page.graph import organism            # noqa: F401  (re-exported)
from aea.tooling.page.guard import FORBIDDEN           # noqa: F401  (re-exported)
from aea.tooling.page.render import build              # noqa: F401  (re-exported)
from aea.tooling.page.sources import OUT               # noqa: F401  (re-exported)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def _scan(html: str) -> list:
    """Kept under its old name because `selfcheck` and the handoff both refer to it."""
    return guard.scan(html)


if __name__ == "__main__":
    from aea.tooling.page.__main__ import main
    raise SystemExit(main())
