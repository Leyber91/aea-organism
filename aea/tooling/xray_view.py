"""xray_view.py - the xray, rendered. GENERATED FROM THE CODE, NEVER HAND-AUTHORED.

THE ONE RULE THIS FILE EXISTS TO ENFORCE. A hand-drawn architecture diagram is wrong the day after
it is drawn, and this repo has the receipts: twenty-one budget systems, six model selectors, and the
whole unstick kernel orphaned from every wake path - none of it hidden, all of it simply never
rendered. So the view is a projection of `state/xray.json`, which is a projection of the AST. Nothing
here is typed by hand except the shapes and the colours.

THE VISUAL LAW IS THE PROJECT'S OWN, not a choice made here: void field plus structure grey, with
amber (#ffb000 / #d4a24c) reserved for the FIRED/ACTIVE state only - sparse, bright, earned. It maps
onto this data exactly, which is why it is worth obeying: a module reachable from a wake is LIT, and
everything else is structure. The picture makes the finding before any number is read.

  python -m aea.tooling.xray_view        writes web/xray.html from state/xray.json
"""
from __future__ import annotations

import json
import os

from aea.kernel import grid
from aea.tooling import xray, xray_graph

OUT = os.path.join(grid.WEB, "xray.html")

CSS = """
:root{
  --void:#07080a; --panel:#0c0e12; --line:#191c22; --line2:#23272f;
  --dim:#5c636e; --mid:#868e99; --text:#c3c8d0;
  --amber:#ffb000; --amber-dim:#d4a24c; --amber-ghost:rgba(255,176,0,.10);
}
*{box-sizing:border-box}
body{margin:0;background:var(--void);color:var(--text);
  font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:12px;line-height:1.5;font-variant-numeric:tabular-nums;
  -webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{display:grid;grid-template-columns:300px 1fr 340px;gap:1px;background:var(--line);
  min-height:100vh}
.col{background:var(--void);overflow-y:auto;max-height:100vh}
.win{border-bottom:1px solid var(--line)}
.win>h2{margin:0;padding:9px 12px;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--dim);font-weight:400;border-bottom:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:baseline}
.win>h2 b{color:var(--mid);font-weight:400;letter-spacing:.04em}
.win .body{padding:10px 12px}

/* the headline reading */
.verdict{padding:16px 12px 14px}
.verdict .n{font-size:44px;line-height:.92;letter-spacing:-.03em;color:var(--amber)}
.verdict .n small{font-size:15px;color:var(--dim);letter-spacing:0}
.verdict p{margin:8px 0 0;color:var(--mid);max-width:58ch}

/* meters */
.meter{margin:7px 0}
.meter .lab{display:flex;justify-content:space-between;color:var(--dim);font-size:11px}
.meter .lab b{color:var(--text);font-weight:400}
.bar{height:3px;background:var(--line2);margin-top:4px;position:relative;overflow:hidden}
.bar i{display:block;height:100%;background:var(--amber-dim)}
.bar.hot i{background:var(--amber)}

/* the map */
.map{padding:12px}
.pkg{margin-bottom:14px}
.pkg h3{margin:0 0 6px;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);font-weight:400}
.cells{display:flex;flex-wrap:wrap;gap:3px}
.cell{border:1px solid var(--line2);background:var(--panel);color:var(--dim);
  padding:5px 8px;cursor:pointer;font-size:11px;position:relative;transition:none}
.cell:hover{border-color:var(--mid);color:var(--text)}
.cell.lit{border-color:var(--amber);color:var(--amber);background:var(--amber-ghost)}
.cell.srv{border-color:var(--amber-dim);color:var(--amber-dim)}
.cell.sel{outline:1px solid var(--text);outline-offset:1px}
.cell .sz{color:var(--dim);margin-left:7px;font-size:10px}
.cell.lit .sz{color:var(--amber-dim)}

/* lists */
table{width:100%;border-collapse:collapse}
td,th{padding:3px 0;text-align:left;font-weight:400;vertical-align:top}
th{color:var(--dim);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  border-bottom:1px solid var(--line);padding-bottom:5px}
td.r{text-align:right;color:var(--mid)}
td+td{padding-left:10px}
tr.warn td{color:var(--amber-dim)}
/* The 300px rail cannot hold two columns of module paths side by side - the first render ran
   "capability_census.json" straight into its writer with no gap. Narrow panels stack instead. */
.stack{padding:5px 0;border-bottom:1px solid var(--line)}
.stack:last-child{border-bottom:0}
.stack b{display:block;color:var(--text);font-weight:400;word-break:break-word}
.stack span{display:block;color:var(--amber-dim);font-size:11px;word-break:break-word;
  padding-left:10px}
.stack.q b{color:var(--amber-dim)}
.k{color:var(--dim)}
.mono{color:var(--mid)}
.tag{display:inline-block;border:1px solid var(--line2);padding:0 5px;color:var(--dim);
  font-size:10px;margin:0 3px 3px 0}
.tag.on{border-color:var(--amber);color:var(--amber)}
.empty{color:var(--dim);font-style:normal}
.dash{color:var(--dim)}
#insp .name{color:var(--amber);font-size:13px;word-break:break-all}
#insp .head{color:var(--mid);margin:6px 0 10px}
#insp h4{margin:12px 0 4px;font-size:10px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--dim);font-weight:400}
.linklist span{display:block;color:var(--mid);cursor:pointer;padding:1px 0}
.linklist span:hover{color:var(--amber)}
.foot{padding:10px 12px;color:var(--dim);font-size:10px;border-top:1px solid var(--line)}
.filter{display:flex;gap:4px;padding:8px 12px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.filter button{background:none;border:1px solid var(--line2);color:var(--dim);cursor:pointer;
  padding:3px 8px;font:inherit;font-size:10px;letter-spacing:.08em;text-transform:uppercase}
.filter button.on{border-color:var(--amber);color:var(--amber)}
@media (max-width:1100px){.wrap{grid-template-columns:1fr}.col{max-height:none}}
"""
CSS += xray_graph.CSS

JS = """
const D = window.XRAY;
const M = D.modules;
let filter = 'all', sel = null;

function pkgOf(n){ const p = n.split('.'); return p.length>2 ? p[1] : 'root'; }

function drawMap(){
  const host = document.getElementById('map'); if(!host) return; host.innerHTML = '';
  const groups = {};
  Object.keys(M).sort().forEach(n=>{
    const m = M[n];
    if(filter==='wake' && !m.reachable_from_wake) return;
    if(filter==='orphan' && !m.orphaned) return;
    if(filter==='effects' && !(m.import_time_effects||[]).length) return;
    (groups[pkgOf(n)] = groups[pkgOf(n)] || []).push(n);
  });
  const order = Object.keys(groups).sort((a,b)=>groups[b].length-groups[a].length);
  if(!order.length){ host.innerHTML = '<p class="empty">nothing matches this filter.</p>'; return; }
  order.forEach(p=>{
    const d = document.createElement('div'); d.className='pkg';
    const lit = groups[p].filter(n=>M[n].reachable_from_wake).length;
    d.innerHTML = '<h3>'+p+' <span class="k">'+lit+' of '+groups[p].length+' reachable</span></h3>';
    const c = document.createElement('div'); c.className='cells';
    groups[p].forEach(n=>{
      const m = M[n];
      const b = document.createElement('div');
      b.className = 'cell' + (m.reachable_from_wake?' lit':(m.reachable_from_server?' srv':''))
                  + (n===sel?' sel':'');
      b.innerHTML = n.split('.').slice(2).join('.') + '<span class="sz">'+m.lines+'</span>';
      b.title = m.headline || n;
      b.onclick = ()=>{ sel = n; drawMap(); inspect(n); };
      c.appendChild(b);
    });
    d.appendChild(c); host.appendChild(d);
  });
}

function inspect(n){
  const m = M[n], h = document.getElementById('insp');
  const tags = [];
  tags.push('<span class="tag'+(m.reachable_from_wake?' on':'')+'">wake</span>');
  tags.push('<span class="tag'+(m.reachable_from_server?' on':'')+'">server</span>');
  if(m.orphaned) tags.push('<span class="tag">orphaned</span>');
  if((m.import_time_effects||[]).length) tags.push('<span class="tag on">acts on import</span>');
  const list = (arr, empty) => arr && arr.length
    ? '<div class="linklist">'+arr.map(x=> M[x]
        ? '<span onclick="sel=\\''+x+'\\';drawMap();inspect(\\''+x+'\\')">'+x+'</span>'
        : '<span class="mono">'+x+'</span>').join('')+'</div>'
    : '<p class="empty">'+empty+'</p>';
  h.innerHTML =
    '<div class="name">'+n+'</div>'+
    '<div class="head">'+(m.headline||'&mdash;')+'</div>'+
    tags.join('')+
    '<h4>path</h4><p class="mono">'+m.path+' &middot; '+m.lines+' lines</p>'+
    '<h4>imports ('+(m.imports||[]).length+')</h4>'+list(m.imports,'nothing internal')+
    '<h4>imported by ('+(m.imported_by||[]).length+')</h4>'+
      list(m.imported_by,'nothing imports this')+
    '<h4>writes</h4>'+list((m.state||{}).writes,'no state written')+
    '<h4>reads</h4>'+list((m.state||{}).reads,'no state read');
}

window.inspect = inspect;
document.querySelectorAll('.filter button').forEach(b=>{
  b.onclick = ()=>{
    document.querySelectorAll('.filter button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on'); filter = b.dataset.f; if(document.getElementById('map')) drawMap();
  };
});
if(document.getElementById('map')) drawMap();
"""


def _meter(label, n, total, hot=False):
    pct = (100.0 * n / total) if total else 0
    return ('<div class="meter"><div class="lab"><span>%s</span><b>%d<span class="k">/%d</span>'
            '</b></div><div class="bar%s"><i style="width:%.1f%%"></i></div></div>'
            % (label, n, total, " hot" if hot else "", pct))


def html(d: dict) -> str:
    c, lv = d["counts"], d["live"]
    orph_kernel = [n for n in d["orphans"] if n.startswith("aea.kernel.")]
    orph_lines = sum(d["modules"][n]["lines"] for n in d["orphans"])

    graph = xray_graph.markup(c)
    caps = "".join(
        '<tr%s><td>%s</td><td class="r">%s</td><td class="r">%s</td><td class="r">%s</td></tr>'
        % (' class="warn"' if (v.get("down") or 0) else "", k,
           ["FORBIDDEN", "DRAFT", "WATCHED", "TRUSTED"][v.get("level") or 0],
           v.get("runs") or 0, v.get("fails") or 0)
        for k, v in sorted(lv["capabilities"].items()))

    seats = "".join('<tr><td>%s</td><td class="mono">%s</td><td class="r">%s</td></tr>'
                    % (k, v.get("zone"), "%s/%s" % (v.get("wins") or 0, v.get("runs") or 0))
                    for k, v in sorted(lv["seats"].items())) \
        or '<tr><td colspan="3" class="empty">no seats</td></tr>'

    multi = {k: sorted(set(v["writers"])) for k, v in d["stores"].items()
             if len(set(v["writers"])) > 1}
    stores = "".join('<div class="stack q"><b>%s</b>%s</div>'
                     % (k, "".join("<span>%s</span>" % x for x in w))
                     for k, w in sorted(multi.items())) \
        or '<p class="empty">every store has one writer</p>'

    effects = "".join('<div class="stack q"><b>%s</b><span>%s</span></div>'
                      % (n, ", ".join(sorted({e["call"] for e in
                                              d["modules"][n]["import_time_effects"]})))
                      for n in d["import_time_effects"]) \
        or '<p class="empty">no module acts at import</p>'

    alarms = (", ".join(lv["open_alarms"]) if lv["open_alarms"]
              else '<span class="dash">&mdash;</span>')
    hb = lv["heartbeat"]

    return f"""<title>XRAY &mdash; what this system is made of</title>
<style>{CSS}</style>
<div class="wrap">

  <div class="col">
    <div class="win"><h2>the reading <b>{d['generated']}</b></h2>
      <div class="verdict">
        <div class="n">{c['reachable_from_wake']}<small> of {c['modules']} modules</small></div>
        <p>reachable from an unattended wake. {c['orphaned']} modules and
        {orph_lines:,} lines cannot be reached from any entry point &mdash; including
        {len(orph_kernel)} in <b>kernel</b>, the package that is supposed to BE the entity.</p>
      </div>
      <div class="body">
        {_meter("reachable from a wake", c['reachable_from_wake'], c['modules'], hot=True)}
        {_meter("reachable from the server", c['reachable_from_server'], c['modules'])}
        {_meter("orphaned", c['orphaned'], c['modules'])}
      </div>
    </div>

    <div class="win"><h2>orphaned kernel <b>{len(orph_kernel)}</b></h2>
      <div class="body"><table>
        {''.join('<tr><td>%s</td><td class="r">%d</td></tr>'
                 % (n.split('.')[-1], d['modules'][n]['lines']) for n in orph_kernel)
         or '<tr><td class="empty">none</td></tr>'}
      </table></div>
    </div>

    <div class="win"><h2>acts at import</h2>
      <div class="body">{effects}</div>
    </div>

    <div class="win"><h2>stores with two writers</h2>
      <div class="body">{stores}</div>
    </div>
  </div>

  <div class="col">
{graph}
  </div>

  <div class="col">
    <div class="win"><h2>live &mdash; the ledger</h2>
      <div class="body"><table>
        <tr><th>capability</th><th class="r">level</th><th class="r">runs</th><th class="r">fails</th></tr>
        {caps}
      </table></div>
    </div>
    <div class="win"><h2>seats</h2>
      <div class="body"><table>
        <tr><th>id</th><th>zone</th><th class="r">wins</th></tr>{seats}
      </table></div>
    </div>
    <div class="win"><h2>state</h2>
      <div class="body"><table>
        <tr><td class="k">goals</td><td class="r">{len(lv['goals'])}</td></tr>
        <tr><td class="k">crystal parts</td><td class="r">{lv['crystal_parts']}</td></tr>
        <tr><td class="k">experience</td><td class="r">{lv['experience_attempts']}</td></tr>
        <tr><td class="k">boots</td><td class="r">{hb.get('boots') or '&mdash;'}</td></tr>
        <tr><td class="k">ticks</td><td class="r">{hb.get('ticks') or '&mdash;'}</td></tr>
        <tr><td class="k">last brief</td><td class="r">{hb.get('last_brief_date') or '&mdash;'}</td></tr>
        <tr class="warn"><td class="k">open alarms</td><td class="r">{alarms}</td></tr>
      </table></div>
    </div>
    <div class="win"><h2>inspector</h2>
      <div class="body" id="insp"><p class="empty">click a module in the map.</p></div>
    </div>
  </div>
</div>
<script>window.XRAY={json.dumps(_slim(d))};{JS}
{xray_graph.JS}</script>"""


def _slim(d: dict) -> dict:
    """Only what the view reads. `defs` is the bulk and nothing renders it."""
    mods = {}
    for n, m in d["modules"].items():
        mods[n] = {k: m[k] for k in
                   ("path", "lines", "headline", "imports", "imported_by", "state",
                    "reachable_from_wake", "reachable_from_server", "orphaned",
                    "import_time_effects") if k in m}
    alarmed = set()
    for cap in (d.get("live", {}) or {}).get("open_alarms", []):
        for n, m in d["modules"].items():
            if cap in (m.get("headline") or "") or n.endswith("." + cap.split("_")[0]):
                alarmed.add(n)
    return {"generated": d["generated"], "counts": d["counts"], "modules": mods,
            "entries": d.get("entries", {}), "alarmed": sorted(alarmed)}


if __name__ == "__main__":
    d = xray.build()
    grid.atomic_save_json(xray.OUT, d, indent=1)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html(d))
    print("wrote %s  (%d modules, %d wake-reachable, %d orphaned)"
          % (OUT, d["counts"]["modules"], d["counts"]["reachable_from_wake"],
             d["counts"]["orphaned"]))
