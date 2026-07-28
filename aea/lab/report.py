"""report.py - THE EVIDENCE, BROWSABLE. Every reply, and every judgement made about it.

A number in a verdict line is the END of a chain of decisions about a piece of text, and until now
none of that chain was inspectable. This renders one stored run as a single self-contained page:
what the rod actually said, what each reader extracted from it, which gate it passed, and how those
became a rate with an interval.

It also renders THE ARCHIVE COVERAGE, which is its own finding: the lab stores replies in three
different regimes and nine experiments stored none at all.

Honours the project's locked visual law: void field, structure grey, amber for the FIRED state only.

  python -m aea.lab.report x24_the_store_and_the_door out.html
"""
from __future__ import annotations

import html
import json
import os
import sys

from aea.kernel import grid

MAX_REPLIES = 400          # capped, and the omitted count is printed. Never a silent truncation.


def _newest(experiment):
    d = os.path.join(grid.STATE, "lab", "runs", experiment)
    fs = sorted(f for f in os.listdir(d) if f.endswith(".json")) if os.path.isdir(d) else []
    return os.path.join(d, fs[-1]) if fs else None


def coverage():
    """What reply text each experiment's newest run actually holds. Three regimes, and the third
    is the one that matters: an experiment that stored nothing can never be re-read."""
    d = os.path.join(grid.STATE, "lab", "runs")
    out = []
    for e in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        p = _newest(e)
        if not p:
            continue
        doc = grid.load_json(p, {}) or {}
        found = {}

        def rec(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in ("text", "raw") and isinstance(v, str):
                        c, m = found.get(k, (0, 0))
                        found[k] = (c + 1, max(m, len(v)))
                    else:
                        rec(v)
            elif isinstance(x, list):
                for v in x:
                    rec(v)
        rec(doc)
        n_full, max_full = found.get("text", (0, 0))
        n_raw, max_raw = found.get("raw", (0, 0))
        regime = ("FULL" if n_full else "TAIL ONLY" if n_raw else "NONE")
        out.append({"experiment": e, "regime": regime, "replies": n_full or n_raw,
                    "longest": max_full or max_raw,
                    "rescorable": regime == "FULL"})
    return out


def _esc(s):
    return html.escape(str(s) if s is not None else "")


def _dash(v, fmt="%s"):
    """Absent is a dash. Never a guess, never a zero standing in for a missing measurement."""
    return "&mdash;" if v is None else fmt % v


def _wilson(d):
    w = (d or {}).get("wilson95") or (None, None)
    if w[0] is None:
        return "&mdash;"
    return "%.2f&ndash;%.2f" % (w[0], w[1])


CSS = """
<style>
:root{
  --void:#08090a; --panel:#0e1012; --rule:#1c1f23; --rule-hi:#2a2f35;
  --ink:#d8dade; --ink-dim:#8a8f96; --ink-faint:#5c6169;
  --amber:#ffb000; --amber-dim:#d4a24c; --amber-glow:rgba(255,176,0,.10);
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:"IBM Plex Sans",ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--void);color:var(--ink);font-family:var(--mono);
  font-size:13px;line-height:1.55;font-variant-numeric:tabular-nums;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 96px}
header.top{border-bottom:1px solid var(--rule);padding:40px 0 24px;margin-bottom:8px}
h1{font-family:var(--sans);font-size:26px;font-weight:600;letter-spacing:-.01em;margin:0 0 6px;
  text-wrap:balance}
.sub{color:var(--ink-dim);font-size:12px}
.meta{display:flex;flex-wrap:wrap;gap:6px 20px;margin-top:16px;color:var(--ink-faint);font-size:11px}
.meta b{color:var(--ink-dim);font-weight:400}
h2{font-family:var(--sans);font-size:12px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;
  color:var(--amber-dim);margin:56px 0 4px;padding-bottom:8px;border-bottom:1px solid var(--rule)}
h2 .n{color:var(--ink-faint);margin-right:10px;font-weight:400}
p.lede{font-family:var(--sans);color:var(--ink-dim);font-size:13.5px;line-height:1.65;
  max-width:66ch;margin:14px 0 22px}
p.lede strong{color:var(--ink);font-weight:600}
.scroll{overflow-x:auto;border:1px solid var(--rule);border-radius:2px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:12px;min-width:640px}
th{text-align:left;font-weight:400;color:var(--ink-faint);font-size:10.5px;letter-spacing:.09em;
  text-transform:uppercase;padding:10px 12px;border-bottom:1px solid var(--rule-hi);
  white-space:nowrap;position:sticky;top:0;background:var(--panel)}
td{padding:8px 12px;border-bottom:1px solid var(--rule);white-space:nowrap;color:var(--ink-dim)}
tr:last-child td{border-bottom:0}
td.k{color:var(--ink)}
.num{text-align:right}
.fired{color:var(--amber)}
.dim{color:var(--ink-faint)}
.tag{display:inline-block;padding:1px 7px;border-radius:2px;font-size:10px;letter-spacing:.06em;
  border:1px solid var(--rule-hi);color:var(--ink-faint)}
.tag.on{border-color:rgba(255,176,0,.4);color:var(--amber);background:var(--amber-glow)}
.tag.off{border-color:var(--rule-hi);color:var(--ink-faint)}
.tag.warn{border-color:rgba(212,162,76,.35);color:var(--amber-dim)}
.bar{display:inline-block;height:3px;background:var(--rule-hi);width:70px;vertical-align:middle;
  margin-left:8px;position:relative}
.bar i{position:absolute;left:0;top:0;bottom:0;background:var(--amber);display:block}
/* THE PIPELINE. Numbered because it IS an ordered sequence - the number carries information. */
ol.pipe{list-style:none;counter-reset:s;padding:0;margin:22px 0 0}
ol.pipe li{counter-increment:s;position:relative;padding:0 0 20px 46px;border-left:1px solid var(--rule);
  margin-left:13px}
ol.pipe li:last-child{border-left-color:transparent;padding-bottom:0}
ol.pipe li::before{content:counter(s,decimal-leading-zero);position:absolute;left:-13px;top:-2px;
  width:26px;height:26px;border:1px solid var(--rule-hi);border-radius:50%;background:var(--void);
  color:var(--ink-faint);font-size:10px;display:grid;place-items:center}
ol.pipe li.gate::before{border-color:rgba(255,176,0,.45);color:var(--amber);background:var(--amber-glow)}
ol.pipe h3{font-family:var(--sans);font-size:13px;font-weight:600;margin:0 0 3px;color:var(--ink)}
ol.pipe p{margin:0;color:var(--ink-dim);font-size:12px;max-width:74ch;font-family:var(--sans)}
ol.pipe code{color:var(--amber-dim);font-family:var(--mono);font-size:11.5px}
/* THE REPLY BROWSER */
details.rep{border:1px solid var(--rule);border-radius:2px;background:var(--panel);margin-bottom:5px}
details.rep[open]{border-color:var(--rule-hi)}
summary{cursor:pointer;padding:9px 12px;display:grid;
  grid-template-columns:auto auto 1fr auto auto;gap:14px;align-items:center;list-style:none;
  font-size:11.5px}
summary::-webkit-details-marker{display:none}
summary:hover{background:rgba(255,255,255,.02)}
summary:focus-visible{outline:1px solid var(--amber);outline-offset:-1px}
.sid{color:var(--ink-faint);min-width:132px}
.sform{color:var(--ink-dim);min-width:96px}
.spre{color:var(--ink-faint);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  font-size:11px;opacity:.75}
.body{padding:4px 12px 14px;border-top:1px solid var(--rule)}
pre.reply{white-space:pre-wrap;word-break:break-word;background:var(--void);border:1px solid var(--rule);
  border-radius:2px;padding:11px 13px;margin:12px 0;color:var(--ink);font-size:11.5px;
  line-height:1.6;max-height:340px;overflow:auto}
.readers{display:grid;grid-template-columns:repeat(auto-fill,minmax(196px,1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:2px;margin:12px 0 0}
.rd{background:var(--panel);padding:8px 11px}
.rd .lab{color:var(--ink-faint);font-size:10px;letter-spacing:.07em;text-transform:uppercase}
.rd .val{font-size:14px;margin-top:2px}
.note{font-family:var(--sans);color:var(--ink-faint);font-size:11.5px;margin-top:12px;max-width:74ch}
footer{margin-top:64px;padding-top:18px;border-top:1px solid var(--rule);color:var(--ink-faint);
  font-size:11px;font-family:var(--sans);max-width:74ch}
@media (max-width:640px){
  summary{grid-template-columns:1fr auto;gap:6px}
  .spre,.sform{display:none}
  .wrap{padding:0 13px 64px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>
"""

PIPELINE = [
    ("The call returns text", False,
     "The rod's reply arrives as a string. Nothing has been decided yet. "
     "<code>overseer.inspect()</code> flags it first: empty, truncated mid-word, echoing the prompt, "
     "leaking reasoning. A flag is a note about the reply, never a score."),
    ("The naive read", False,
     "<code>stated()</code> takes the number the reply appears to state. This is the floor every "
     "organism has, because a bare call's only capacity is that a value comes back."),
    ("The readout, if seated", False,
     "<code>read_work()</code> ignores what the reply CLAIMS and reads its WORKING - enumerated "
     "lines, a labelled total, a solved equation. This is the part that recovers a right answer out "
     "of correct arithmetic with a wrong final sentence."),
    ("The guard, if seated", False,
     "<code>Validation</code> may DECLINE. An abstention ends the read; it is not a wrong answer and "
     "is never counted as one."),
    ("The container extracts the running value", False,
     "<code>Carry.extract</code> per form. <code>checkpoint</code> reads its own STATE line, "
     "<code>free</code> splits off its NOTE, <code>none</code> and <code>conversation</code> take "
     "the stated answer."),
    ("The strict anchor - THIS IS WHAT SCORES", True,
     "Every step must end <code>ANSWER: &lt;integer&gt;</code>. That line, and only that line, is "
     "what x24 scores on. The lab's own reader runs beside it and the two are compared: their "
     "DISAGREEMENT RATE is the instrument's error bar on itself."),
    ("Hit, miss, or parse failure - three outcomes, not two", True,
     "Anchor equals truth is a hit. Anchor differs is a miss. <strong>No anchor at all is a PARSE "
     "FAILURE, counted apart and never scored wrong</strong> - otherwise a container that changes "
     "format compliance masquerades as one that changes capability."),
    ("The sequence, which is the unit", True,
     "A chain is correct only if it completed every step AND its last step hit. Sixteen steps of one "
     "chain are not sixteen independent trials: miss step 4 and the rest are wrong by construction."),
    ("The cell, with an interval", True,
     "A Wilson 95% interval over sequences. No flat band: at n=8 two arms from the SAME distribution "
     "differ by 0.10 most of the time, so the old band was calibrated to noise."),
    ("The comparison, paired", True,
     "The same chain runs under every container, so containers are compared by McNemar exact on "
     "discordant pairs. Task difficulty is the dominant variance term and pairing removes it."),
]


def render(experiment):
    p = _newest(experiment)
    doc = grid.load_json(p, {}) or {}
    rows = [r for r in doc.get("rows", []) if r.get("kind") != "pilot"]
    pilots = [r for r in doc.get("rows", []) if r.get("kind") == "pilot"]
    cov = coverage()

    H = [CSS, "<title>THE PROBE &middot; lab evidence</title>", '<div class="wrap">']
    H.append('<header class="top"><h1>Lab evidence &middot; %s</h1>' % _esc(experiment))
    H.append('<div class="sub">Every reply, and every judgement made about it.</div>')
    H.append('<div class="meta"><span><b>run</b> %s</span><span><b>design</b> %s</span>'
             '<span><b>started</b> %s</span><span><b>status</b> %s</span>'
             '<span><b>cells</b> %d</span></div></header>'
             % (_esc(doc.get("run_id")), _esc(doc.get("design_id")), _esc(doc.get("at")),
                _esc(doc.get("status")), len(rows)))

    # ---- 1 ARCHIVE COVERAGE -----------------------------------------------------------------
    H.append('<h2><span class="n">01</span>What the archive actually keeps</h2>')
    n_none = sum(1 for c in cov if c["regime"] == "NONE")
    n_tail = sum(1 for c in cov if c["regime"] == "TAIL ONLY")
    n_full = sum(1 for c in cov if c["regime"] == "FULL")
    H.append('<p class="lede">Replies are stored in three regimes and only one of them can be read '
             'again. <strong>%d experiments kept the full reply. %d kept the last 320 characters '
             'only. %d kept nothing at all</strong> and can never be re-scored, which means a defect '
             'found in their reader can only be fixed by buying every call again.</p>' %
             (n_full, n_tail, n_none))
    H.append('<div class="scroll"><table><thead><tr><th>Experiment</th><th>Regime</th>'
             '<th class="num">Replies</th><th class="num">Longest kept</th>'
             '<th>Re-scorable</th></tr></thead><tbody>')
    for c in cov:
        cls = {"FULL": "on", "TAIL ONLY": "warn", "NONE": "off"}[c["regime"]]
        H.append('<tr><td class="k">%s</td><td><span class="tag %s">%s</span></td>'
                 '<td class="num">%s</td><td class="num">%s</td><td>%s</td></tr>'
                 % (_esc(c["experiment"]), cls, c["regime"],
                    c["replies"] or "&mdash;", c["longest"] or "&mdash;",
                    '<span class="fired">yes</span>' if c["rescorable"]
                    else '<span class="dim">no</span>'))
    H.append("</tbody></table></div>")

    # ---- 2 THE PIPELINE ---------------------------------------------------------------------
    H.append('<h2><span class="n">02</span>How a reply becomes a pass or a fail</h2>')
    H.append('<p class="lede">Ten decisions stand between what the rod said and the number in a '
             'verdict line. The amber steps are the ones that can change a score.</p>')
    H.append('<ol class="pipe">')
    for title, gate, body in PIPELINE:
        H.append('<li class="%s"><h3>%s</h3><p>%s</p></li>'
                 % ("gate" if gate else "", _esc(title), body))
    H.append("</ol>")

    # ---- 3 CALIBRATION ----------------------------------------------------------------------
    if pilots:
        H.append('<h2><span class="n">03</span>Calibration &middot; chain length per rod</h2>')
        H.append('<p class="lede">A cell pinned at 0.00 or 1.00 has no variance and can show '
                 'nothing. Each rod is measured for per-step accuracy, then given the chain length '
                 'that puts its sequence rate near the middle. <strong>A rod that cannot be tuned '
                 'into range is marked, not quietly run at the floor.</strong></p>')
        H.append('<div class="scroll"><table><thead><tr><th>Rod</th><th class="num">Per-step</th>'
                 '<th class="num">Ideal length</th><th class="num">Chosen</th>'
                 '<th class="num">Predicted sequence</th><th>In range</th></tr></thead><tbody>')
        for r in pilots:
            H.append('<tr><td class="k">%s</td><td class="num">%s</td><td class="num">%s</td>'
                     '<td class="num fired">%s</td><td class="num">%s</td><td>%s</td></tr>'
                     % (_esc(r["rod"]), _dash(r.get("per_step_accuracy"), "%.3f"),
                        _dash(r.get("ideal_length"), "%.2f"), r.get("length_chosen"),
                        _dash(r.get("predicted_sequence_rate"), "%.2f"),
                        '<span class="fired">yes</span>' if r.get("in_range")
                        else '<span class="tag warn">descriptive only</span>'))
        H.append("</tbody></table></div>")

    # ---- 4 CELLS ----------------------------------------------------------------------------
    H.append('<h2><span class="n">04</span>Results &middot; one row per container and rod</h2>')
    H.append('<p class="lede">Never pooled across rods: four providers with different tokenizers and '
             'sampling defaults, where a pooled rate is a Simpson&rsquo;s-paradox generator and the '
             'between-rod difference is the finding. <strong>Read the intervals, not the point '
             'estimates.</strong> The last two columns are the instrument measuring itself.</p>')
    H.append('<div class="scroll"><table><thead><tr><th>Container</th><th>Rod</th>'
             '<th class="num">Len</th><th class="num">Correct</th><th class="num">Wilson 95%</th>'
             '<th class="num">Flip</th><th class="num">Token recall</th>'
             '<th class="num">Parse fail</th><th class="num">Reader disagree</th>'
             '</tr></thead><tbody>')
    for r in rows:
        c, t = r.get("correct") or {}, r.get("token_retrieval") or {}
        rate = c.get("rate") or 0
        H.append('<tr><td class="k">%s</td><td>%s</td><td class="num">%s</td>'
                 '<td class="num">%s/%s<span class="bar"><i style="width:%.0f%%"></i></span></td>'
                 '<td class="num">%s</td><td class="num">%s</td>'
                 '<td class="num %s">%s/%s</td><td class="num">%s</td><td class="num">%s</td></tr>'
                 % (_esc(r["form"]), _esc(r["rod"]), r.get("length"),
                    c.get("k"), c.get("n"), min(100, rate * 100), _wilson(c),
                    _dash((r.get("within_chain_disagreement") or {}).get("rate"), "%.2f"),
                    "fired" if (t.get("k") or 0) else "dim", t.get("k"), t.get("n"),
                    _dash((r.get("parse_fail_steps") or {}).get("rate"), "%.2f"),
                    _dash((r.get("read_disagreement") or {}).get("rate"), "%.2f")))
    H.append("</tbody></table></div>")

    # ---- 5 THE REPLIES ----------------------------------------------------------------------
    H.append('<h2><span class="n">05</span>The replies</h2>')
    steps = []
    for r in rows:
        for rec in r.get("records") or []:
            for s in rec.get("trace") or []:
                if s.get("ok") and s.get("text") is not None:
                    steps.append((r, rec, s))
    shown = steps[:MAX_REPLIES]
    H.append('<p class="lede">What the rod said, and what every reader made of it. '
             '<strong>Showing %d of %d stored replies</strong>%s. Open any row for the full text and '
             'the judgement chain.</p>'
             % (len(shown), len(steps),
                "" if len(shown) == len(steps) else
                " &mdash; the rest are in the run JSON, and this cap is stated rather than silent"))
    for r, rec, s in shown:
        hit = s.get("hit_anchored")
        pf = s.get("parse_fail")
        state = ("PARSE FAIL" if pf else "HIT" if hit else "MISS")
        cls = "warn" if pf else "on" if hit else "off"
        pre = (s.get("text") or "").replace("\n", " ")[:150]
        H.append('<details class="rep"><summary>'
                 '<span class="sid">chain %s.%s &middot; step %s</span>'
                 '<span class="sform">%s</span>'
                 '<span class="spre">%s</span>'
                 '<span class="dim">%s</span>'
                 '<span class="tag %s">%s</span></summary>'
                 % (rec.get("chain"), rec.get("sample"), s.get("step"),
                    _esc(r["form"]), _esc(pre), _esc(r["rod"].split("/")[-1]), cls, state))
        H.append('<div class="body"><pre class="reply">%s</pre>' % _esc(s.get("text")))
        H.append('<div class="readers">')
        for lab, val, fire in [
            ("truth", s.get("truth"), False),
            ("ANSWER anchor &middot; scores", s.get("anchored"), hit),
            ("lab reader", s.get("value"), False),
            ("read by", s.get("read_by"), False),
            ("showed working", "yes" if s.get("showed_work") else "no", False),
            ("on task", "yes" if s.get("on_task") else "no", False),
            ("flags", ", ".join(s.get("flags") or []) or None, False),
            ("context chars", s.get("context_chars"), False),
        ]:
            H.append('<div class="rd"><div class="lab">%s</div><div class="val %s">%s</div></div>'
                     % (lab, "fired" if fire else "", _dash(_esc(val) if val is not None else None)))
        H.append("</div>")
        if s.get("read_disagrees"):
            H.append('<div class="note">The strict anchor and the lab&rsquo;s own reader disagree on '
                     'this reply. One of them is wrong, and this is the disagreement the summary '
                     'table counts.</div>')
        probes = [pb for pb in (rec.get("probes") or [])
                  if pb.get("depth") == s.get("step") and not pb.get("unreachable")]
        for pb in probes:
            H.append('<div class="note">Probed at this depth. Token wanted <code>%s</code>, got '
                     '<code>%s</code> &mdash; %s. The token cannot be recomputed, so reproducing it '
                     'is retrieval and can be nothing else.</div>'
                     % (_esc(pb.get("token_want")), _dash(_esc(pb.get("token_got"))
                                                          if pb.get("token_got") else None),
                        '<span class="fired">retrieved</span>' if pb.get("token_ok")
                        else '<span class="dim">not retrieved</span>'))
        H.append("</div></details>")

    H.append('<footer>Generated from <code>%s</code>. Every value here is read from the stored run; '
             'an absent measurement renders as a dash and never as a zero. Two-ink visual law: void '
             'field, structure grey, amber for the fired state only.</footer>' % _esc(
                 os.path.relpath(p, grid.STATE).replace("\\", "/")))
    H.append("</div>")
    return "\n".join(H)


if __name__ == "__main__":
    exp = sys.argv[1] if len(sys.argv) > 1 else "x24_the_store_and_the_door"
    out = sys.argv[2] if len(sys.argv) > 2 else "lab_evidence.html"
    page = render(exp)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("wrote %s  (%d KB)" % (out, len(page) // 1024))
