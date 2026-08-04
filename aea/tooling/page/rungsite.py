"""rungsite.py - THE ROUTES. One page per rung, plus the index, plus their one stylesheet.

    python -m aea.tooling.page.rungsite        write the site under web/ladder/

`render.build_site()` already returns a DICT KEYED BY ROUTE and says why in its own comment - "a
site, not a file. Each part is written where it belongs and linked, so a copy change is a diff of
the markup instead of a diff buried under 1,226 unchanged dots." Multipage is therefore not a new
system here. It is more keys.

ONE STYLESHEET FOR ALL TEN PAGES, not one per rung. A per-rung stylesheet is a per-rung look, and a
per-rung look is how a page with nothing in it gets arranged to look full.

THE PALETTE IS NOT CHOSEN HERE EITHER. aea-city's visual law is locked: void field + structure
grey, amber as the FIRED state only - sparse, bright, earned. Every colour below is that law, which
is why a DIED verdict is the only amber thing on a claim card. The rung was built to be wrong on
purpose; the moment it was is the thing worth lighting.
"""
from __future__ import annotations

import os
import sys

from aea.kernel import grid
from aea.tooling import dossier
from aea.tooling.page import chapters as C
from aea.tooling.page import rung as R

CSS = """
:root{--void:#08090a;--void2:#0e1012;--void3:#14171a;--hair:#21262b;--hair2:#2b3238;
--grey:#7b8288;--dim:#4b5258;--ink:#e9edf0;--ink2:#a8b0b6;--amber:#ffb000;--amber2:#d4a24c;
--ghost:rgba(255,176,0,.11);
--mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,"Cascadia Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--void);color:var(--grey);font-family:var(--mono);font-size:13.5px;
line-height:1.6;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased;
padding:44px 22px 100px;max-width:1020px;margin:0 auto}
a{color:inherit;text-decoration:none}
.eyebrow{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);margin:0 0 10px}
h1{font-size:clamp(24px,4.4vw,38px);line-height:1.1;font-weight:500;letter-spacing:-.02em;
color:var(--ink);margin:0 0 10px}
h1 span{color:var(--grey);font-size:.52em;letter-spacing:.14em;text-transform:uppercase;
display:block;margin-top:8px}
h2{font-size:11.5px;letter-spacing:.17em;text-transform:uppercase;font-weight:500;color:var(--grey);
margin:0 0 14px;padding-bottom:9px;border-bottom:1px solid var(--hair)}
.human{color:var(--ink2);font-size:14.5px;margin:0 0 14px;max-width:66ch}
.note{font-size:11.5px;color:var(--dim);max-width:72ch;margin:0 0 16px}
.empty{font-size:12px;color:var(--dim);border-left:2px solid var(--hair2);padding:9px 14px;margin:0}
em{color:var(--amber2);font-style:normal}
section{margin-top:44px}
/* nav */
.rnav{display:flex;flex-wrap:wrap;gap:1px;margin-bottom:34px;background:var(--hair);border:1px solid var(--hair)}
.rnav a{background:var(--void2);padding:7px 13px;font-size:11.5px;color:var(--dim);letter-spacing:.06em}
.rnav a.met{color:var(--grey)}
.rnav a.on{background:var(--ghost);color:var(--amber)}
.rnav a:hover,.rnav a:focus-visible{color:var(--ink);outline:none;background:var(--void3)}
.pill{display:inline-block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
padding:3px 10px;border:1px solid var(--hair2);color:var(--dim)}
.pill.proven{color:var(--amber);border-color:rgba(255,176,0,.42);background:var(--ghost)}
/* claim contract */
.claimdl{display:grid;grid-template-columns:82px 1fr;gap:10px 16px;margin:0}
.claimdl dt{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);padding-top:2px}
.claimdl dd{margin:0;color:var(--ink2);font-size:12.5px}
/* chips */
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:11px;border:1px solid var(--hair2);padding:2px 9px;color:#cdd4d9;background:var(--void3)}
.chip b{color:var(--dim);font-weight:400}
.chip.hot{border-color:rgba(255,176,0,.4);color:var(--amber)}
.chip.hot b{color:var(--amber2)}
.chip.bad{border-color:#5a3030;color:#e0a0a0}
.chip.dash{color:var(--dim)}
/* journey */
.jstat{display:flex;flex-wrap:wrap;gap:20px;margin-bottom:18px;font-size:12px;color:var(--dim)}
.jstat b{color:var(--ink);font-size:16px;font-weight:500;margin-right:5px}
.claims{display:grid;gap:1px;background:var(--hair);border:1px solid var(--hair)}
.claim{background:var(--void2);padding:15px 18px}
.claim.died{background:linear-gradient(90deg,var(--ghost),transparent 42%)}
.claim header{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.claim .st{font-size:10px;letter-spacing:.13em;padding:2px 8px;border:1px solid var(--hair2);color:var(--dim)}
.claim.died .st{color:var(--amber);border-color:rgba(255,176,0,.45)}
.claim .hid{font-size:10.5px;color:var(--dim)}
.claim .by{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--amber2);
border:1px solid rgba(255,176,0,.3);padding:1px 7px}
.claim .c{color:var(--ink);font-size:13.5px;margin-bottom:11px}
.claim dl{display:grid;grid-template-columns:190px 1fr;gap:7px 16px;margin:0}
.claim dt{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--dim);padding-top:3px}
.claim dd{margin:0;font-size:12px;color:var(--ink2)}
.claim dd.src{color:var(--dim);font-size:11.5px}
.claim dd.cons{color:var(--amber2)}
.cite{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;padding:5px 0;border-top:1px solid var(--hair)}
.cite:first-child{border-top:0}
.cite .mono{color:var(--amber2);font-size:11.5px}
.cite .url{color:var(--ink2);font-size:11.5px;overflow-wrap:anywhere}
.cite .meta{grid-column:1/-1;font-size:10.5px;color:var(--dim)}
.cite.dash{color:var(--dim);font-size:11.5px}
/* index */
.rlist{display:grid;gap:1px;background:var(--hair);border:1px solid var(--hair)}
.rrow{display:grid;grid-template-columns:56px 1fr 1fr 90px 92px;gap:14px;align-items:center;
background:var(--void2);padding:13px 17px;font-size:12px}
.rrow:hover,.rrow:focus-visible{background:var(--void3);outline:none}
.rrow .id{color:var(--ink);font-size:14px}
.rrow .ttl{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--grey)}
.rrow .hum{color:var(--ink2)}
.rrow .j{color:var(--dim);font-size:11px}
.rrow .st{font-size:9.5px;letter-spacing:.13em;color:var(--dim);text-align:right}
.rrow.met .id{color:var(--amber)}
.rrow.met .st{color:var(--amber2)}
/* chapters */
.cnav{display:flex;flex-wrap:wrap;gap:1px;margin-bottom:34px;background:var(--hair);border:1px solid var(--hair)}
.cnav a{background:var(--void2);padding:8px 15px;font-size:11.5px;color:var(--dim);letter-spacing:.07em}
.cnav a.on{background:var(--ghost);color:var(--amber)}
.cnav a:hover,.cnav a:focus-visible{color:var(--ink);background:var(--void3);outline:none}
.chead{margin-bottom:8px}
.chead h1{font-size:clamp(26px,4.8vw,42px)}
.lede{color:var(--ink2);font-size:15px;max-width:70ch;margin:0}
.body{color:var(--ink2);font-size:13px;max-width:72ch;margin:0 0 13px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1px;
background:var(--hair);border:1px solid var(--hair)}
.stats>div{background:var(--void2);padding:17px 19px}
.stats b{display:block;font-size:27px;color:var(--amber);font-weight:500;letter-spacing:-.01em}
.stats.small b{font-size:20px;color:var(--ink)}
.stats span{display:block;font-size:11px;color:var(--dim);margin-top:5px;line-height:1.45}
.stages{display:grid;gap:1px;background:var(--hair);border:1px solid var(--hair)}
.stage{background:var(--void2);padding:18px 20px}
.stage header{display:flex;align-items:baseline;gap:13px;margin-bottom:8px}
.stage .n{font-size:11px;color:var(--amber2);letter-spacing:.12em}
.stage h3{margin:0;font-size:14px;font-weight:500;color:var(--ink);letter-spacing:-.01em}
.stage p{margin:0;font-size:12.5px;color:var(--ink2);max-width:74ch}
.stage .out{margin-top:9px;font-size:11px;color:var(--amber2);letter-spacing:.04em}
.flag{border-left:2px solid var(--amber);background:var(--ghost);padding:14px 18px;
font-size:13px;color:#d8dee3;margin:0 0 14px}
.scroll{overflow-x:auto;border:1px solid var(--hair)}
table{border-collapse:collapse;width:100%;font-size:12.5px;min-width:520px}
th,td{text-align:left;padding:10px 13px;border-bottom:1px solid var(--hair)}
th{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);font-weight:500}
td.num{text-align:right;color:#cdd4d9}td.hot{color:var(--amber)}td.n{color:var(--dim)}
.cta{display:inline-block;margin-top:8px;border:1px solid rgba(255,176,0,.4);color:var(--amber);
padding:7px 15px;font-size:12px;background:var(--ghost)}
.cta:hover,.cta:focus-visible{background:rgba(255,176,0,.19);outline:none}
@media(max-width:760px){.rrow{grid-template-columns:46px 1fr;gap:4px}
.rrow .hum,.rrow .j{display:none}.claim dl,.claimdl{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

DOC = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>%s</title><link rel="stylesheet" href="rungs.css"></head><body>%s</body></html>')


def build_pages() -> dict:
    """Route -> bytes. Same contract as `render.build_site()`, so it composes with it."""
    d = dossier.build()
    rungs = d["rungs"]
    # THE DOSSIER IS THE SITE, NOT THE RUNG PAGES ALONE. The rungs record what is true; the
    # chapters record how it was arrived at, which is the half that makes the next rung cheaper.
    out = {"ladder/rungs.css": CSS,
           "ladder/index.html": DOC % ("The ladder dossier", C.intro(d)),
           "ladder/rungs.html": DOC % ("The rungs", R.index(rungs, d["at"], d["tick"])),
           "ladder/process.html": DOC % ("How R5 was arrived at", C.process(d)),
           "ladder/experiments.html": DOC % ("Experiments", C.experiments(d)),
           "ladder/blockers.html": DOC % ("One defect, eight times", C.blockers(d)),
           "ladder/journey.html": DOC % ("The token journey", C.journey(d))}
    for r in rungs:
        out["ladder/%s.html" % r["id"]] = DOC % (
            "%s %s" % (r["id"], r["title"]),
            R.page(r, d["wiring"], rungs, d["at"], d["tick"]))
    return out


def write(root: str = None) -> list:
    root = root or os.path.join(grid.WEB)
    written = []
    for route, body in build_pages().items():
        p = os.path.join(root, *route.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(body)
        written.append((route, len(body)))
    return written


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    for route, n in write():
        print("  %-26s %7s bytes" % (route, "{:,}".format(n)))
