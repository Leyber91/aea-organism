"""rung.py - ONE JOB: render ONE rung's page. Ten identical shapes, nothing arranged by hand.

WHAT THIS FILE MAY NOT DO, following `render.py`'s rule for the same reason: compute a number. Every
figure comes from `aea.tooling.dossier`, which computes them once. Eight pages each doing their own
arithmetic is the 494-line `build()` again, spread across files instead of lines - two totals that
must agree, with nothing between them that could notice they do not.

THE SHAPE IS THE SAME FOR ALL TEN RUNGS AND THAT IS THE POINT. A page that is arranged per-rung is a
page whose emptiness can be hidden by rearranging it. Four sections, always, in this order:

    CLAIM        power / bound / gate, VERBATIM from ladder.py. A paraphrase of a contract is a
                 different contract
    MEASUREMENT  live, or the words "this rung has no measurement function" - which is the state
                 R5 sat in for a day while 66 of its claims already existed on disk
    JOURNEY      the claim-to-bytes chain, walkable. Empty rungs print WHY they are empty
    WIRING       what the rung declares, checked against the live call graph

THE JOURNEY IS THE TOKEN JOURNEY, AT THE RUNG'S OWN SCALE. The call-level view - prompt in,
39.7 seconds of invisible deliberation, answer out - is one tick. This is the same walk one level
up: a claim written and fsynced BEFORE any bytes existed, a probe, bytes hashed at the socket, a
verdict, a consequence. Both are the same question - what actually travelled, and what survived it -
and only R5 can answer it end to end today, because R5 is the first rung whose output IS evidence.
"""
from __future__ import annotations

import html
import time


def _e(x) -> str:
    return html.escape(str(x if x is not None else ""), quote=True)


def _ago(ts) -> str:
    try:
        d = time.time() - float(ts)
        return ("%.0fs" % d) if d < 90 else ("%.0fm" % (d / 60)) if d < 5400 else ("%.1fh" % (d / 3600))
    except Exception:
        return "-"


def _chips(m: dict) -> str:
    """Whatever the rung measured, as chips. Booleans read as words; None reads as a dash."""
    skip = {"met", "why"}
    out = []
    for k, v in (m or {}).items():
        if k in skip or k.startswith("gate_") or isinstance(v, (list, dict)):
            continue
        if v is None:
            val, cls = "-", " dash"
        elif isinstance(v, bool):
            val, cls = ("ok" if v else "FAILED"), (" hot" if v else " bad")
        else:
            val, cls = _e(v), ""
        out.append('<span class="chip%s"><b>%s</b> %s</span>' % (cls, _e(k), val))
    return "".join(out) or '<span class="chip dash">nothing measured</span>'


def _journey(j: dict) -> str:
    rows = j.get("rows") or []
    if not rows:
        return ('<p class="empty">No claim-to-bytes chain on this rung. %s</p>'
                % _e(j.get("why") or "No reason recorded, which is itself a defect."))
    died = [r for r in rows if r["status"] == "DIED"]
    ent = [r for r in rows if r.get("by_entity")]
    head = ('<div class="jstat"><span><b>%d</b> claims</span><span><b>%d</b> died</span>'
            '<span><b>%d</b> started by the entity</span>'
            '<span><b>%d</b> citations resolve to stored bytes</span></div>'
            % (len(rows), len(died),
               sum(1 for r in ent), sum(len(r["citations"]) for r in rows)))
    # the deaths first - a rung about being wrong should lead with the times it was
    order = died + [r for r in rows if r["status"] != "DIED"]
    cards = []
    for r in order[:14]:
        cites = "".join(
            '<div class="cite"><span class="mono">%s</span>'
            '<span class="url">%s</span>'
            '<span class="meta">%s bytes · src=%s · status=%s · %s</span></div>'
            % (_e((c.get("sha256") or "")[:16]), _e(c.get("url")),
               _e(c.get("bytes") if c.get("on_disk") else "MISSING"),
               _e(c.get("src")), _e(c.get("status")), _ago(c.get("at")))
            for c in r["citations"]) or '<div class="cite dash">no citation</div>'
        gap = ""
        try:
            if r.get("settled_at") and r.get("at"):
                gap = "%.1fs between the claim and its verdict" % (float(r["settled_at"]) - float(r["at"]))
        except Exception:
            gap = ""
        cards.append(
            '<article class="claim %s">'
            '<header><span class="st">%s</span><span class="hid">%s</span>%s</header>'
            '<div class="c">%s</div>'
            '<dl>'
            '<dt>stated before, as the thing that would kill it</dt><dd>%s</dd>'
            '<dt>where the record already asserted it</dt><dd class="src">%s</dd>'
            '%s'
            '<dt>the bytes that settled it</dt><dd>%s</dd>'
            '<dt>verdict</dt><dd>%s</dd>'
            '%s</dl></article>'
            % ("died" if r["status"] == "DIED" else "corr",
               _e(r["status"]), _e((r.get("hid") or "")[:12]),
               '<span class="by">entity</span>' if r.get("by_entity") else "",
               _e(r.get("claim")),
               _e(r.get("killer")),
               _e(r.get("from_record")),
               ('<dt>held fixed</dt><dd>%s</dd>' % _e("; ".join(r.get("holds_fixed") or [])))
               if r.get("holds_fixed") else "",
               cites, _e(r.get("why") or "-"),
               ('<dt>what changes</dt><dd class="cons">%s</dd>' % _e(r["consequence"]))
               if r.get("consequence") else ""))
    more = ('<p class="empty">%d further claims not shown; the store is the record.</p>'
            % (len(rows) - 14)) if len(rows) > 14 else ""
    return head + '<div class="claims">' + "".join(cards) + "</div>" + more


def page(rung: dict, wiring: dict, all_rungs: list, at: str, tick) -> str:
    rid = rung["id"]
    nav = "".join('<a class="%s" href="%s.html">%s</a>'
                  % ("on" if r["id"] == rid else
                     ("met" if r.get("met") else "fut"), _e(r["id"]), _e(r["id"]))
                  for r in all_rungs)
    unwired = [u for u in (wiring.get("unwired") or [])
               if any(f.split(":")[0] in u for f in rung["funcs"])]
    status = ("PROVEN" if rung.get("met")
              else "UNMEASURED" if rung.get("unmeasured") else "PARTIAL")
    meas = ('<p class="empty">This rung has no measurement function, so the ladder reports it '
            'FUTURE. That is not the same as unproven - R5 read FUTURE for a day while 66 of its '
            'claims already existed on disk.</p>' if rung.get("unmeasured")
            else '<div class="chips">%s</div>' % _chips(rung.get("measured")))
    return (
      '<nav class="rnav">%s</nav>'
      '<header class="rhead"><p class="eyebrow">aea-city · the ladder · %s · tick %s</p>'
      '<h1>%s <span>%s</span></h1><p class="human">%s</p>'
      '<span class="pill %s">%s</span></header>'
      '<section><h2>The claim</h2><dl class="claimdl">'
      '<dt>power</dt><dd>%s</dd><dt>bound</dt><dd>%s</dd><dt>gate</dt><dd>%s</dd>%s</dl></section>'
      '<section><h2>The measurement</h2>%s</section>'
      '<section><h2>The journey</h2>'
      '<p class="note">A claim written and fsynced <em>before</em> any bytes existed, a probe, '
      'bytes hashed at the socket, a verdict, a consequence. Every hash below resolves to a file '
      'on disk.</p>%s</section>'
      '<section><h2>The wiring</h2><div class="chips">%s</div>%s</section>'
      % (nav, _e(at), _e(tick),
         _e(rid), _e(rung.get("title")), _e(rung.get("human")),
         status.lower(), status,
         _e(rung.get("power") or "-"), _e(rung.get("bound") or "-"), _e(rung.get("gate") or "-"),
         ('<dt>blocked on</dt><dd>%s</dd>' % _e(rung["blocked_on"])) if rung.get("blocked_on") else "",
         meas,
         _journey(rung.get("journey") or {}),
         ("".join('<span class="chip">%s</span>' % _e(f) for f in rung["funcs"])
          or '<span class="chip dash">declares nothing</span>'),
         ('<p class="empty">unwired: %s</p>' % _e(", ".join(unwired))) if unwired else
         '<p class="note">Checked against the live call graph, not against whether the names exist.</p>'))


def index(rungs: list, at: str, tick) -> str:
    rows = "".join(
        '<a class="rrow %s" href="%s.html"><span class="id">%s</span>'
        '<span class="ttl">%s</span><span class="hum">%s</span>'
        '<span class="j">%s</span><span class="st">%s</span></a>'
        % ("met" if r.get("met") else "fut", _e(r["id"]), _e(r["id"]), _e(r["title"]),
           _e(r.get("human")),
           ("%d claims" % len(r["journey"]["rows"])) if r["journey"]["rows"] else "-",
           "PROVEN" if r.get("met") else ("UNMEASURED" if r.get("unmeasured") else "PARTIAL"))
        for r in rungs)
    return ('<header class="rhead"><p class="eyebrow">aea-city · %s · tick %s</p>'
            '<h1>The ladder</h1><p class="human">One page per rung: what it claims, what was '
            'measured, and the evidence it produced.</p></header>'
            '<section><div class="rlist">%s</div></section>' % (_e(at), _e(tick), rows))
