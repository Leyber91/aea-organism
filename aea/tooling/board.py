"""board.py - THE COMMAND CENTRE. A shell, not a page.

WHY THE FIRST VERSION FAILED, in the terms that diagnose it rather than describe it:

  TABS HIDE STATE. Correct for a document, wrong for an instrument. Everything behind a tab is state
  you have lost, and you cannot lose state in the thing you open to find out what is happening. The
  fix is a persistent shell with a changing working surface: the chrome proves you are still in the
  same place (Gestalt common region), the content moves inside it.

  THE DOCUMENTS WERE DUMPED, NOT READ. THE_LAWS.md rendered as scrollable prose is the source file
  with a font. A law has structure - an id, a claim, and the failure that paid for it - so it is
  parsed into that structure and each part is given its own weight. Same for OPEN_LOOPS: three
  verdicts are three columns, not three headings.

  THERE WAS NO PERIPHERY. Weiser's calm technology: most information should sit at the edge of
  attention so that GLANCING tells you something. A page with nothing at the edge gives you no reason
  to keep it open.

  RECOGNITION, NOT RECALL (Nielsen 6). The control room exposes ~15 routes reachable only by typing
  them. The rail enumerates every one, so the system's vocabulary never has to be held in your head.

THE TWO-INK LAW STILL HOLDS and does more work here than anywhere: void plus structure grey, amber
for the fired state only. Depth comes from elevation and hairlines, never from a second hue.

  python -m aea.tooling.board
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
import time

from aea.kernel import grid, laws, trust
from aea.tooling import xray, xray_graph

OUT = os.path.join(grid.WEB, "board.html")
LEVELS = ("FORBIDDEN", "DRAFT", "WATCHED", "TRUSTED")
E = html.escape


def _read(p, d=""):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return d


# ---------------------------------------------------------------------------------------------
# PARSERS. The documents have structure; render the structure, not the prose.
# ---------------------------------------------------------------------------------------------

def parse_laws() -> list:
    """Each law becomes {id, section, claim, body, paid}. `Paid for:` is the evidence and it is the
    reason the law is credible, so it is kept as its own field rather than buried in a paragraph."""
    out, sec = [], "?"
    for line in laws.text().splitlines():
        m = re.match(r"^##\s+([IVX]+)\s+-\s+(.+)$", line.strip())
        if m:
            sec = m.group(2).strip()
            continue
        m = re.match(r"^\*\*([A-Z]\d+)\.\s+(.+?)\*\*\s*(.*)$", line.strip())
        if m:
            body = m.group(3).strip()
            paid = ""
            pm = re.search(r"\*(?:Paid for|Origin):\*\s*(.+)", body)
            if pm:
                paid = pm.group(1).strip()
                body = body[:pm.start()].strip()
            out.append({"id": m.group(1), "section": sec, "claim": m.group(2).strip(),
                        "body": re.sub(r"[*`]", "", body), "paid": re.sub(r"[*`]", "", paid)})
    return out


def parse_loops() -> dict:
    """FINISH / LATER / KILL. Three verdicts, three columns."""
    txt = _read(os.path.join(grid.ROOT, "diary", "OPEN_LOOPS.md"))
    out = {"FINISH": [], "LATER": [], "KILL": []}
    cur = None
    for line in txt.splitlines():
        h = re.match(r"^##\s+(FINISH|LATER|KILL)\b", line.strip())
        if h:
            cur = h.group(1)
            continue
        if not cur:
            continue
        row = re.match(r"^\|\s*(\d+)\s*\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|", line)
        if row and cur == "FINISH":
            out[cur].append({"t": re.sub(r"[*`]", "", row.group(2)),
                             "w": re.sub(r"[*`]", "", row.group(3))[:200],
                             "size": re.sub(r"[*`]", "", row.group(4))})
            continue
        b = re.match(r"^-\s+\*\*(.+?)\*\*\s*(.*)$", line.strip())
        if b and cur in ("LATER", "KILL"):
            out[cur].append({"t": re.sub(r"[*`]", "", b.group(1)),
                             "w": re.sub(r"[*`]", "", b.group(2))[:220], "size": ""})
        elif cur in ("LATER", "KILL") and line.strip().startswith("- "):
            s = re.sub(r"[*`]", "", line.strip()[2:])
            out[cur].append({"t": s[:70], "w": s[70:260], "size": ""})
    return out


def usage() -> dict:
    """MY OWN COST, from the transcripts, because a control centre that cannot see its own spend is
    asking you to trust it. Real records, never an estimate; absent means absent."""
    d = os.path.dirname(os.path.dirname(grid.STATE))
    pat = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                       "c--REDACTED-dev-aea-city", "*.jsonl")
    tot = {"records": 0, "in": 0, "out": 0, "cache_read": 0, "cache_write": 0, "sessions": 0}
    per_day = {}
    for f in glob.glob(pat):
        tot["sessions"] += 1
        stamp = time.strftime("%m-%d", time.localtime(os.path.getmtime(f)))
        for line in open(f, encoding="utf-8", errors="ignore"):
            if '"usage"' not in line:
                continue
            try:
                u = (json.loads(line).get("message") or {}).get("usage") or {}
            except Exception:
                continue
            if not u:
                continue
            tot["records"] += 1
            tot["in"] += u.get("input_tokens", 0)
            tot["out"] += u.get("output_tokens", 0)
            tot["cache_read"] += u.get("cache_read_input_tokens", 0)
            tot["cache_write"] += u.get("cache_creation_input_tokens", 0)
            per_day[stamp] = per_day.get(stamp, 0) + u.get("output_tokens", 0)
    tot["per_day"] = per_day
    return tot


def routes() -> list:
    """Every route the server exposes, read from its source so the rail cannot go stale."""
    src = _read(os.path.join(grid.ROOT, "aea", "server", "controlroom.py"))
    found = set(re.findall(r'self\.path\s*==\s*"(/[a-z/]*)"', src))
    found |= set(re.findall(r'self\.path\.startswith\("(/[a-z/]*)"', src))
    found |= set(re.findall(r'"(/game/[a-z]+)"', src))
    skip = {"/", "/favicon.ico"}
    return sorted(r for r in found if r not in skip and len(r) > 1)


def _n(v) -> str:
    v = float(v)
    for u, d in (("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if v >= d:
            return "%.1f%s" % (v / d, u)
    return "%d" % v


# ---------------------------------------------------------------------------------------------

CSS = r"""
:root{
  /* L* ladder, measured: void 1.9 / sunk 5.0 / panel 11.1 / raised 15.9 / line 24.1 / strong 32.0
     Hue held at 214-218 to satisfy E8's cool-ink band. Base-to-white 20.1:1, above Material's 15.8 budget. */
  --void:#06070b; --deep:#0e1116; --panel:#191e25; --raise:#222832;
  --line:#313a46; --line2:#424c5b; --dim:#7c8798; --mid:#9aa5b4; --text:#ced5de; --hi:#f2f6fa;
  --amber:#ffb000; --amber-d:#d4a24c; --ghost:rgba(255,176,0,.09);
  /* THE ALARM MUST BE THE LOUDEST MARK. Measured: fail was 3.18:1 against pass at 10.40:1 -
     the all-clear shouted and the alarm whispered. NASA: highest-priority data, highest contrast. */
  --alarm:#fb923c; --alarm-bd:#c2410c; --kill:#5d6673;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--void);color:var(--text);font-size:12.5px;line-height:1.55;
  font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased;overflow:hidden}
#amb{position:fixed;inset:0;z-index:0;opacity:.5}
.shell{position:relative;z-index:1;display:grid;
  grid-template-columns:212px 1fr 264px;grid-template-rows:auto 1fr;height:100vh}

/* ---- top strip: the three answers, always visible ---- */
.strip{grid-column:1/-1;display:grid;grid-template-columns:212px 1fr 264px;
  border-bottom:1px solid var(--line);background:linear-gradient(180deg,#0b0d12,#08090c)}
.brand{padding:13px 16px;border-right:1px solid var(--line)}
.brand b{display:block;color:var(--amber);font-weight:400;letter-spacing:.22em;font-size:11px}
.brand span{color:var(--dim);font-size:9.5px;letter-spacing:.1em}
.answers{display:grid;grid-template-columns:repeat(3,1fr)}
.ans{padding:10px 18px;border-right:1px solid var(--line);position:relative}
.ans .lab{font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--dim)}
.ans .val{font-size:22px;line-height:1.2;color:var(--hi);letter-spacing:-.012em;
  white-space:normal;overflow-wrap:anywhere}
.ans .val.hot{color:var(--amber)}
.ans .sub{font-size:10.5px;color:var(--mid)}
.clock{padding:10px 16px;text-align:right}
.clock .t{font-size:19px;color:var(--hi)}
.clock .d{font-size:9.5px;color:var(--dim);letter-spacing:.1em}

/* ---- rail ---- */
.rail{border-right:1px solid var(--line);overflow-y:auto;background:linear-gradient(180deg,#090b0e,#07080a)}
.rail h4{margin:16px 14px 5px;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);font-weight:400}
.rail a,.rail button{display:flex;justify-content:space-between;align-items:center;gap:8px;
  width:100%;text-align:left;background:none;border:0;border-left:2px solid transparent;
  color:var(--mid);cursor:pointer;padding:5px 14px;font:inherit;font-size:11.5px;text-decoration:none}
.rail button:hover,.rail a:hover{color:var(--hi);background:rgba(255,255,255,.022)}
.rail button.on{color:var(--amber);border-left-color:var(--amber);background:var(--ghost)}
.rail .c{font-size:10px;color:var(--dim)}
.rail button.on .c{color:var(--amber-d)}

/* ---- centre ---- */
.work{overflow-y:auto;padding:22px 26px 80px;
  background:radial-gradient(120% 80% at 50% -10%,rgba(150,175,205,.045),transparent 60%)}
.work::-webkit-scrollbar,.rail::-webkit-scrollbar,.side::-webkit-scrollbar{width:9px}
.work::-webkit-scrollbar-thumb,.rail::-webkit-scrollbar-thumb,.side::-webkit-scrollbar-thumb{
  background:var(--line2);border:3px solid var(--void)}
.view{display:none}.view.on{display:block;animation:in .22s ease}
@keyframes in{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
h2{margin:0 0 3px;font-size:14px;font-weight:400;color:var(--hi);letter-spacing:.01em}
.lede{color:var(--dim);font-size:11.5px;margin:0 0 16px;max-width:82ch}

/* ---- cards with real elevation ---- */
.grid{display:grid;gap:10px}
.g3{grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}
.g2{grid-template-columns:repeat(auto-fill,minmax(400px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);
  border-radius:6px;padding:16px 18px;position:relative;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.055);
  transition:border-color .16s cubic-bezier(.2,0,.38,.9),background .16s cubic-bezier(.2,0,.38,.9)}
.card:hover{border-color:var(--line2);background:var(--raise)}
.card.lit{border-left:1px solid var(--line)}
.card.alarm{border-left:2px solid var(--alarm)}
.card.kill{border-left:2px solid var(--kill);opacity:.72}
.card.later{border-left:2px solid var(--line2)}
.tag{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);font-weight:500}
.rail h4,.side h4,th,.ans .lab,.st .k,.col h3,.filters button{font-weight:500}
h2,.claim,.st .n,.ans .val,.card .lid{font-weight:600}
.claim{color:var(--hi);font-size:12.5px;margin:3px 0 4px;line-height:1.45}
.body{color:var(--mid);font-size:11.5px}
.paid{margin-top:7px;padding-top:7px;border-top:1px dashed var(--line2);color:var(--amber-d);font-size:10.5px}
.lid{position:absolute;right:10px;top:9px;color:var(--line2);font-size:15px;letter-spacing:.04em}
.card:hover .lid{color:var(--amber-d)}

/* ---- meters / stats ---- */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);margin-bottom:16px}
.st{background:linear-gradient(180deg,#0e1116,#0a0c10);padding:11px 13px}
.st .n{font-size:34px;line-height:1.05;color:var(--hi);letter-spacing:-.022em}
.st.hot .n{color:var(--amber);text-shadow:0 0 22px rgba(255,176,0,.35)}
.st .k{font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-top:3px}
.st .s{font-size:10.5px;color:var(--mid)}
.bar{height:2px;background:var(--line2);margin-top:7px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--amber-d)}
table{width:100%;border-collapse:collapse}
td,th{padding:3.5px 10px 3.5px 0;text-align:left;font-weight:400;vertical-align:top}
th{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid var(--line)}
td.r{text-align:right}
tr.warn td{color:var(--amber-d)}
.pill{display:inline-block;padding:0 6px;border:1px solid var(--line2);font-size:9.5px;color:var(--dim);letter-spacing:.08em}
.pill.go{border-color:var(--line2);color:var(--dim)}
.pill.no{border-color:var(--alarm-bd);color:var(--alarm);background:rgba(251,146,60,.10);font-weight:600}
.pips{display:flex;gap:3px;margin:6px 0}
.pip{flex:1;height:3px;background:var(--kill)}
.pip.ok{background:var(--amber)}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;align-items:start}
.col h3{margin:0 0 8px;font-size:10px;letter-spacing:.18em;text-transform:uppercase;font-weight:400}
.col.f h3{color:var(--amber)}.col.l h3{color:var(--mid)}.col.k h3{color:var(--kill)}
.col .n{font-size:10px;color:var(--dim);margin-left:6px}
iframe{width:100%;height:calc(100vh - 190px);border:1px solid var(--line2);background:var(--void)}
.filters{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:12px}
.filters button{background:none;border:1px solid var(--line2);color:var(--dim);cursor:pointer;
  padding:3px 9px;font:inherit;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase}
.filters button.on{border-color:var(--amber);color:var(--amber)}

/* ---- right periphery ---- */
.side{border-left:1px solid var(--line);overflow-y:auto;padding:14px 14px 40px;
  background:linear-gradient(180deg,#090b0e,#07080a)}
.side h4{margin:0 0 7px;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);font-weight:400}
.side section{margin-bottom:20px}
.kv{display:flex;justify-content:space-between;gap:8px;padding:2.5px 0;font-size:11.5px}
.kv b{font-weight:500;color:var(--hi);white-space:nowrap}
.kv.warn b{color:var(--amber)}
.spark{display:flex;align-items:flex-end;gap:2px;height:34px;margin:6px 0}
.spark i{flex:1;background:var(--amber-d);min-height:1px;opacity:.75}
.spark i:last-child{background:var(--amber);opacity:1}
"""

JS = r"""
// AMBIENT FIELD. Not decoration: the points ARE the modules and the lines ARE imports, drawn from
// the same graph the map uses, at low opacity. It gives the shell depth and it is still true.
(function(){
  const c=document.getElementById('amb'), x=c.getContext('2d');
  const P=(window.AMB||[]).map(p=>({x:p[0],y:p[1],r:p[2],lit:p[3],t:Math.random()*6.28}));
  function sz(){c.width=innerWidth*devicePixelRatio;c.height=innerHeight*devicePixelRatio;}
  sz(); addEventListener('resize',sz);
  let k=0;
  (function loop(){
    k+=0.0035; x.clearRect(0,0,c.width,c.height);
    const S=Math.max(c.width,c.height);
    P.forEach(p=>{
      const px=c.width*0.5+(p.x+Math.sin(k+p.t)*0.004)*S*0.62;
      const py=c.height*0.5+(p.y+Math.cos(k*0.8+p.t)*0.004)*S*0.62;
      const r=Math.max(0.6,p.r*devicePixelRatio*0.5);
      x.beginPath(); x.arc(px,py,r,0,7);
      x.fillStyle = p.lit ? 'rgba(255,176,0,0.16)' : 'rgba(120,132,150,0.055)';
      x.fill();
      if(p.lit){ const g=x.createRadialGradient(px,py,0,px,py,r*9);
        g.addColorStop(0,'rgba(255,176,0,0.05)'); g.addColorStop(1,'rgba(255,176,0,0)');
        x.fillStyle=g; x.beginPath(); x.arc(px,py,r*9,0,7); x.fill(); }
    });
    requestAnimationFrame(loop);
  })();
})();

function show(id){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('on'));
  document.querySelectorAll('.rail button').forEach(b=>b.classList.remove('on'));
  const v=document.getElementById(id); if(v)v.classList.add('on');
  const b=document.querySelector('.rail button[data-v="'+id+'"]'); if(b)b.classList.add('on');
  location.hash=id;
}
document.querySelectorAll('.rail button[data-v]').forEach(b=>b.onclick=()=>show(b.dataset.v));
document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{
  const g=b.dataset.g;
  document.querySelectorAll('.filters button[data-g="'+g+'"]').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  document.querySelectorAll('[data-sec]').forEach(c=>{
    c.style.display=(b.dataset.f==='*'||c.dataset.sec===b.dataset.f)?'':'none';});
});
addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT')return;
  const m={'1':'v-status','2':'v-loops','3':'v-laws','4':'v-props','5':'v-map','6':'v-routes'};
  if(m[e.key]) show(m[e.key]);
});
show((location.hash||'#v-status').slice(1));
setTimeout(()=>location.reload(), 300000);   // the board is derived; 5-min refresh keeps it true
"""


def build() -> str:
    d = xray.build()
    c, lv = d["counts"], d["live"]
    led = grid.load_json(trust.LEDGER, {})
    hb = grid.load_json(os.path.join(grid.STATE, "heartbeat.json"), {})
    sc = grid.load_json(os.path.join(grid.STATE, "selfcheck.json"), {})
    al = lv["open_alarms"]
    L, loops, us = parse_laws(), parse_loops(), usage()

    stale = 0
    try:
        import datetime as dt
        stale = (dt.date.today() - dt.date.fromisoformat(hb.get("last_brief_date"))).days
    except Exception:
        pass

    # ambient field: real module positions on the package ring, real lit flag
    pk = sorted({m["package"] for m in d["modules"].values()})
    amb = []
    import math
    for i, (n, m) in enumerate(sorted(d["modules"].items())):
        a = (pk.index(m["package"]) / max(1, len(pk))) * 6.283
        j = ((i * 2654435761) % 997) / 997.0 - .5
        amb.append([round(math.cos(a) * .34 + j * .13, 4), round(math.sin(a) * .34 + j * .13, 4),
                    round(max(1.0, min(6.0, (m["lines"] ** .5) / 4)), 2),
                    1 if m["reachable_from_wake"] else 0])

    # ---- the three answers ----
    broke = [ch for ch in (sc.get("checks") or []) if not ch["pass"]]
    answers = [
        ("what is broken", "%d" % (len(al) + len(broke)), bool(al or broke),
         (", ".join(al) or "no open alarms") + (" &middot; %d invariant" % len(broke) if broke else "")),
        ("what changed", "%d/%d" % (c["reachable_from_wake"], c["modules"]), False,
         "reachable from a wake &middot; %d orphaned" % c["orphaned"]),
        ("what is next", loops["FINISH"][0]["t"][:42] if loops["FINISH"] else "nothing queued",
         True, "%d to finish &middot; %d killed" % (len(loops["FINISH"]), len(loops["KILL"]))),
    ]
    strip = "".join(
        '<div class="ans"><div class="lab">%s</div><div class="val%s">%s</div><div class="sub">%s</div></div>'
        % (E(k), " hot" if h else "", E(str(v)), s) for k, v, h, s in answers)

    # ---- rail ----
    nav = [("v-status", "status", ""), ("v-loops", "open loops", str(len(loops["FINISH"]))),
           ("v-laws", "the laws", str(len(L))), ("v-props", "proposals", ""),
           ("v-map", "the map", ""), ("v-routes", "endpoints", "")]
    props_dir = os.path.join(grid.STATE, "proposals")
    npro = len([f for f in os.listdir(props_dir) if f.endswith(".json")]) if os.path.isdir(props_dir) else 0
    nav[3] = ("v-props", "proposals", str(npro))
    rl = "".join('<button data-v="%s"><span>%s</span><span class="c">%s</span></button>'
                 % (i, E(t), E(n)) for i, t, n in nav)
    rt = "".join('<a href="%s" target="_blank">%s</a>' % (E(r), E(r)) for r in routes()[:18])

    # ---- status ----
    stats = [("brief", hb.get("last_brief_date") or "never", "%d days ago" % stale if stale else "today", stale >= 1),
             ("reachable", c["reachable_from_wake"], "of %d" % c["modules"], False),
             ("orphaned", c["orphaned"], "unreachable", True),
             ("alarms", len(al), ", ".join(al)[:26] or "none", bool(al)),
             ("ticks", hb.get("total_ticks") or 0, "%s boots" % hb.get("boot_count"), False),
             ("laws", len(L), "earned", False)]
    sts = "".join('<div class="st%s"><div class="n">%s</div><div class="k">%s</div><div class="s">%s</div></div>'
                  % (" hot" if h else "", E(str(v)), E(k), E(str(s))) for k, v, s, h in stats)
    ledr = "".join('<tr%s><td>%s</td><td>%s</td><td class="r">%s</td><td class="r">%s</td></tr>'
                   % (' class="warn"' if (e.get("down") or 0) else "", E(k), LEVELS[e.get("level") or 0],
                      e.get("runs") or 0, e.get("fails") or 0) for k, e in sorted(led.items()))
    inv = "".join('<tr%s><td><span class="pill %s">%s</span></td><td>%s</td></tr>'
                  % ("" if ch["pass"] else ' class="warn"', "go" if ch["pass"] else "no",
                     "pass" if ch["pass"] else "fail", E(ch["check"]))
                  for ch in (sc.get("checks") or []))

    # ---- laws as cards ----
    secs = sorted({x["section"] for x in L})
    lf = ('<div class="filters"><button data-g="s" data-f="*" class="on">all %d</button>' % len(L)
          + "".join('<button data-g="s" data-f="%s">%s</button>' % (E(s), E(s)) for s in secs) + "</div>")
    lc = "".join(
        '<div class="card lit" data-sec="%s"><div class="lid">%s</div><div class="tag">%s</div>'
        '<div class="claim">%s</div><div class="body">%s</div>%s</div>'
        % (E(x["section"]), E(x["id"]), E(x["section"]), E(x["claim"]), E(x["body"]),
           ('<div class="paid">%s</div>' % E(x["paid"])) if x["paid"] else "")
        for x in L)

    # ---- loops as three columns ----
    def col(k, cls):
        items = loops[k]
        return ('<div class="col %s"><h3>%s<span class="n">%d</span></h3>%s</div>'
                % (cls, k, len(items), "".join(
                    '<div class="card %s"><div class="claim">%s</div><div class="body">%s</div>%s</div>'
                    % ("lit" if k == "FINISH" else ("kill" if k == "KILL" else "later"),
                       E(i["t"]), E(i["w"]),
                       ('<div class="tag" style="margin-top:6px">%s</div>' % E(i["size"])) if i["size"] else "")
                    for i in items) or '<p class="body">none</p>'))

    # ---- proposals ----
    props = []
    if os.path.isdir(props_dir):
        for f in sorted(os.listdir(props_dir), reverse=True):
            if not f.endswith(".json"):
                continue
            p = grid.load_json(os.path.join(props_dir, f), {})
            g = p.get("gate", {})
            chk = g.get("checks") or []
            props.append(
                '<div class="card %s"><div class="tag">%s &middot; %s</div>'
                '<div class="claim">%s</div><div class="pips">%s</div>'
                '<div class="body">%s</div><div class="paid">%s</div></div>'
                % ("lit" if g.get("pass") else "kill",
                   "passed the gate" if g.get("pass") else "rejected by the gate", E(p.get("at", "")),
                   E(p.get("what", "?")),
                   "".join('<span class="pip %s" title="%s"></span>'
                           % ("ok" if ch["pass"] else "", E(ch["check"])) for ch in chk),
                   E(p.get("why", "")), E(", ".join(p.get("files") or []))))

    # ---- usage ----
    days = sorted(us["per_day"].items())
    mx = max([v for _, v in days] or [1])
    spark = "".join('<i style="height:%d%%" title="%s: %s"></i>' % (max(3, int(100 * v / mx)), k, _n(v))
                    for k, v in days)
    side = (
        '<section><h4>my usage</h4>'
        '<div class="kv"><span>output</span><b>%s</b></div>'
        '<div class="kv"><span>input</span><b>%s</b></div>'
        '<div class="kv"><span>cache read</span><b>%s</b></div>'
        '<div class="kv"><span>cache write</span><b>%s</b></div>'
        '<div class="kv"><span>api calls</span><b>%s</b></div>'
        '<div class="spark">%s</div>'
        '<div class="kv"><span>sessions</span><b>%d</b></div></section>'
        '<section><h4>the ledger</h4>%s</section>'
        '<section><h4>heartbeat</h4>'
        '<div class="kv"><span>boots</span><b>%s</b></div>'
        '<div class="kv"><span>ticks</span><b>%s</b></div>'
        '<div class="kv%s"><span>last brief</span><b>%s</b></div>'
        '<div class="kv"><span>goals</span><b>%d</b></div>'
        '<div class="kv"><span>crystal parts</span><b>%d</b></div>'
        '<div class="kv"><span>experience</span><b>%d</b></div></section>'
        % (_n(us["out"]), _n(us["in"]), _n(us["cache_read"]), _n(us["cache_write"]),
           _n(us["records"]), spark, us["sessions"],
           "".join('<div class="kv%s"><span>%s</span><b>%s</b></div>'
                   % (" warn" if (e.get("level") or 0) < 2 else "", E(k), LEVELS[e.get("level") or 0][:4])
                   for k, e in sorted(led.items())),
           hb.get("boot_count"), hb.get("total_ticks"),
           " warn" if stale else "", hb.get("last_brief_date") or "never",
           len(lv["goals"]), lv["crystal_parts"], lv["experience_attempts"]))

    V = lambda i, t, l, b: ('<div class="view" id="%s"><h2>%s</h2><p class="lede">%s</p>%s</div>'
                            % (i, t, l, b))
    views = (
        V("v-status", "status", "Everything on this page is read from state on disk at generation time.",
          '<div class="stats">%s</div><div class="grid g2">'
          '<div class="card"><div class="tag">the ledger</div><table>'
          '<tr><th>capability</th><th>level</th><th class="r">runs</th><th class="r">fails</th></tr>%s</table></div>'
          '<div class="card"><div class="tag">invariants &middot; %s</div><table>%s</table></div></div>'
          % (sts, ledr, E(sc.get("at", "never")), inv)) +
        V("v-loops", "open loops",
          "Every item carries a verdict. A LATER still sitting at LATER becomes a KILL.",
          '<div class="cols">%s%s%s</div>' % (col("FINISH", "f"), col("LATER", "l"), col("KILL", "k"))) +
        V("v-laws", "the laws",
          "%d laws, each paid for by a real failure. Loaded into the entity's own context by aea.kernel.laws."
          % len(L), lf + '<div class="grid g3">%s</div>' % lc) +
        V("v-props", "proposals",
          "A change to this system, tested in an isolated shadow. Four gate checks the candidate cannot author.",
          '<div class="grid g2">%s</div>' % ("".join(props) or '<p class="body">No proposals yet.</p>')) +
        V("v-map", "the map", "The real import graph. Amber is reachable from an unattended wake.",
          '<iframe src="xray.html" title="import graph"></iframe>') +
        V("v-routes", "endpoints", "Every route the control room exposes, read from its source.",
          '<div class="grid g3">%s</div>' % "".join(
              '<a class="card" href="%s" target="_blank" style="text-decoration:none;display:block">'
              '<div class="claim">%s</div><div class="body">open in a new tab</div></a>'
              % (E(r), E(r)) for r in routes())))

    return ("<title>AEA command centre</title>"
            "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
            "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?"
            "family=IBM+Plex+Mono:wght@300;400;500;600;700&display=swap'>"
            "<style>%s</style><canvas id='amb'></canvas>"
            "<div class='shell'><div class='strip'>"
            "<div class='brand'><b>AEA</b><span>command centre</span></div>"
            "<div class='answers'>%s</div>"
            "<div class='clock'><div class='t'>%s</div><div class='d'>%s</div></div></div>"
            "<div class='rail'><h4>views</h4>%s<h4>live endpoints</h4>%s</div>"
            "<div class='work'>%s</div><div class='side'>%s</div></div>"
            "<script>window.AMB=%s;%s</script>"
            % (CSS, strip, time.strftime("%H:%M"), time.strftime("%Y-%m-%d"),
               rl, rt, views, side, json.dumps(amb), JS))


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print("wrote %s  ->  http://localhost:7799/board.html" % OUT)
