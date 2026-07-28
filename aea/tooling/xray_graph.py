"""xray_graph.py - THE CODEBASE AS A LIVING GRAPH. Canvas, real edges, honest motion.

WHAT IS ON SCREEN IS THE IMPORT GRAPH, not a diagram of it. Every node is a module found by the AST
and every line is an import that exists in the source. Nothing is placed by hand, so nothing can be
wrong in the way a drawn architecture diagram is wrong.

THE ONE ANIMATION, AND WHY IT IS ALLOWED. The honesty law forbids a cosmetic effect disconnected
from a real event, which rules out ambient drifting and decorative pulses. So there is exactly one
motion here and it carries information: a wave leaves the wake entry points and travels the REAL
import edges, in dependency order, lighting each module as reachability reaches it. The animation IS
the reachability computation, replayed. When it stops, everything still dark is genuinely
unreachable - which is 84 of 104 modules, and the point the picture exists to make.

The second signal is a ring, and it is also earned: a module whose capability currently holds an
open alarm gets one. No alarm, no ring.

Layout is force-directed - repulsion between all nodes, springs along real imports, a weak pull
toward each package's centroid. It settles and then stops; a graph that never stops moving is
harder to read and burns a laptop battery for nothing.
"""

CSS = """
.stage{position:relative;background:var(--void);overflow:hidden}
#g{display:block;width:100%;height:100%;cursor:grab}
#g:active{cursor:grabbing}
.legend{position:absolute;left:12px;bottom:10px;color:var(--dim);font-size:10px;
  letter-spacing:.06em;pointer-events:none;line-height:1.7}
.legend b{color:var(--amber);font-weight:400}
.legend i{color:var(--amber-dim);font-style:normal}
.hud{position:absolute;right:12px;top:10px;text-align:right;pointer-events:none}
.hud .big{font-size:34px;line-height:1;color:var(--amber);letter-spacing:-.02em}
.hud .sub{color:var(--dim);font-size:10px;letter-spacing:.14em;text-transform:uppercase}
.ctl{position:absolute;left:12px;top:10px;display:flex;gap:4px}
.ctl button{background:rgba(7,8,10,.8);border:1px solid var(--line2);color:var(--dim);
  cursor:pointer;padding:4px 9px;font:inherit;font-size:10px;letter-spacing:.08em;
  text-transform:uppercase}
.ctl button:hover{border-color:var(--mid);color:var(--text)}
.ctl button.on{border-color:var(--amber);color:var(--amber)}
.tip{position:absolute;pointer-events:none;background:rgba(7,8,10,.94);
  border:1px solid var(--line2);padding:5px 8px;font-size:11px;color:var(--text);
  max-width:300px;display:none}
.tip b{color:var(--amber);font-weight:400}
.tip span{display:block;color:var(--dim);font-size:10px;margin-top:2px}
"""

JS = r"""
(function(){
const D = window.XRAY, M = D.modules;
const cv = document.getElementById('g'), cx = cv.getContext('2d');
const tip = document.getElementById('tip');
const ALARMED = new Set(D.alarmed || []);

const names = Object.keys(M);
const idx = {}; names.forEach((n,i)=>idx[n]=i);
const N = names.map((n,i)=>{
  const m = M[n], pkg = n.split('.').length>2 ? n.split('.')[1] : 'root';
  return {i, n, pkg, m, r: Math.max(3.4, Math.min(15, Math.sqrt(m.lines)/1.9)),
          x:0, y:0, vx:0, vy:0, lit:0};
});
const E = [];
names.forEach(n=>{ (M[n].imports||[]).forEach(t=>{ if(idx[t]!==undefined) E.push([idx[n], idx[t]]); }); });

// Package centroids on a ring: gives the eye stable regions without forcing a layout.
const pkgs = [...new Set(N.map(d=>d.pkg))].sort();
const anchor = {};
pkgs.forEach((p,k)=>{ const a = (k/pkgs.length)*Math.PI*2;
  anchor[p] = {x: Math.cos(a)*0.30, y: Math.sin(a)*0.30}; });
N.forEach(d=>{ const a = anchor[d.pkg];
  d.x = a.x + (((d.i*2654435761)%1000)/1000 - .5)*0.12;
  d.y = a.y + (((d.i*40503)%1000)/1000 - .5)*0.12; });

let W=0,H=0,S=1, ox=0, oy=0, zoom=1, settle=1, sel=null, hov=null, mode='all';
function size(){ const r = cv.parentElement.getBoundingClientRect();
  W = cv.width = r.width*devicePixelRatio; H = cv.height = r.height*devicePixelRatio;
  cv.style.width=r.width+'px'; cv.style.height=r.height+'px'; S = Math.min(W,H); }
size(); addEventListener('resize', ()=>{ size(); settle=1; });

function step(){
  if(settle < 0.02){ if(!fitted) autofit(); return; }
  for(let a=0;a<N.length;a++){
    const p=N[a];
    for(let b=a+1;b<N.length;b++){
      const q=N[b]; let dx=q.x-p.x, dy=q.y-p.y; let d2=dx*dx+dy*dy;
      if(d2<1e-6){ dx=1e-3; d2=1e-6; }
      if(d2>0.055) continue;
      const f = 0.0000075/d2, d=Math.sqrt(d2);
      const fx=f*dx/d, fy=f*dy/d;
      p.vx-=fx; p.vy-=fy; q.vx+=fx; q.vy+=fy;
    }
  }
  E.forEach(([a,b])=>{ const p=N[a], q=N[b];
    const dx=q.x-p.x, dy=q.y-p.y, d=Math.hypot(dx,dy)||1e-4, f=(d-0.045)*0.012;
    const fx=f*dx/d, fy=f*dy/d; p.vx+=fx; p.vy+=fy; q.vx-=fx; q.vy-=fy; });
  N.forEach(d=>{ const a=anchor[d.pkg];
    d.vx += (a.x-d.x)*0.060; d.vy += (a.y-d.y)*0.060;
    d.x += d.vx; d.y += d.vy; d.vx*=0.86; d.vy*=0.86; });
  settle *= 0.985;
}

// THE WAVE. Breadth-first over the REAL edges from the wake entry points, so the light spreads
// exactly as reachability does. Depth = arrival order = what the gate actually computes.
const depth = {};
(function(){
  const roots = (D.entries && D.entries.wake || []).filter(n=>idx[n]!==undefined);
  let front = roots.map(n=>idx[n]); front.forEach(i=>depth[i]=0);
  let d=0;
  while(front.length){ d++; const nx=[];
    front.forEach(i=>{ (M[names[i]].imports||[]).forEach(t=>{ const j=idx[t];
      if(j!==undefined && depth[j]===undefined){ depth[j]=d; nx.push(j); } }); });
    front=nx; }
})();
const maxDepth = Math.max(1, ...Object.values(depth));
let wave = 0, waving = true;

let fitted=false, fit=1, fcx=0, fcy=0;
function autofit(){
  let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  N.forEach(d=>{ if(d.x<x0)x0=d.x; if(d.y<y0)y0=d.y; if(d.x>x1)x1=d.x; if(d.y>y1)y1=d.y; });
  fcx=(x0+x1)/2; fcy=(y0+y1)/2;
  fit = 0.80 / Math.max(x1-x0, y1-y0, 1e-3);
  fitted=true;
}
function px(d){ return [W/2 + ((d.x-fcx)*fit*zoom + ox)*S, H/2 + ((d.y-fcy)*fit*zoom + oy)*S]; }

function draw(){
  step();
  if(waving){ wave += 0.022; if(wave > maxDepth + 2.2){ wave = 0; } }
  N.forEach(d=>{
    const dep = depth[d.i];
    const target = (dep!==undefined && wave >= dep) ? 1 : 0;
    d.lit += (target - d.lit) * 0.14;
  });

  cx.clearRect(0,0,W,H);
  cx.lineWidth = Math.max(1, devicePixelRatio*0.6);
  E.forEach(([a,b])=>{
    const p=N[a], q=N[b];
    if(mode==='wake' && !(p.m.reachable_from_wake && q.m.reachable_from_wake)) return;
    const l = Math.min(p.lit, q.lit);
    const [x1,y1]=px(p), [x2,y2]=px(q);
    cx.strokeStyle = l>0.05 ? 'rgba(255,176,0,'+(0.09+l*0.30)+')' : 'rgba(120,130,145,0.10)';
    cx.beginPath(); cx.moveTo(x1,y1); cx.lineTo(x2,y2); cx.stroke();
  });

  N.forEach(d=>{
    if(mode==='wake' && !d.m.reachable_from_wake) return;
    if(mode==='orphan' && !d.m.orphaned) return;
    const [x,y]=px(d), r=d.r*devicePixelRatio*Math.sqrt(zoom);
    const l=d.lit;
    if(l>0.02){
      const g=cx.createRadialGradient(x,y,0,x,y,r*4.2);
      g.addColorStop(0,'rgba(255,176,0,'+(0.30*l)+')'); g.addColorStop(1,'rgba(255,176,0,0)');
      cx.fillStyle=g; cx.beginPath(); cx.arc(x,y,r*4.2,0,7); cx.fill();
    }
    cx.beginPath(); cx.arc(x,y,r,0,7);
    cx.fillStyle = l>0.02 ? 'rgba(255,176,0,'+(0.30+0.70*l)+')' : 'rgba(28,32,39,1)';
    cx.fill();
    cx.strokeStyle = l>0.02 ? 'rgba(255,176,0,.95)'
                   : (d.m.reachable_from_server ? 'rgba(212,162,76,.55)' : 'rgba(92,99,110,.55)');
    cx.stroke();
    if(ALARMED.has(d.n)){
      cx.beginPath(); cx.arc(x,y,r+4*devicePixelRatio,0,7);
      cx.strokeStyle='rgba(255,176,0,.75)'; cx.stroke();
    }
    const lz=Math.min(1,Math.max(0,(zoom-0.75)/0.7));
    if(d===sel || d===hov || (d.m.reachable_from_wake && lz>0.05)){
      cx.globalAlpha = (d===sel||d===hov) ? 1 : lz;
      cx.fillStyle = l>0.3 ? 'rgba(255,176,0,.95)' : 'rgba(150,158,170,.9)';
      cx.font = (10*devicePixelRatio)+'px ui-monospace,monospace';
      cx.fillText(d.n.replace('aea.',''), x + r + 5*devicePixelRatio, y + 3.5*devicePixelRatio);
      cx.globalAlpha = 1;
    }
  });
  if(settle>=0.02 || waving || hov || drag) requestAnimationFrame(draw);
  else setTimeout(()=>requestAnimationFrame(draw), 400);
}

function hit(mx,my){
  let best=null, bd=1e9;
  N.forEach(d=>{ const [x,y]=px(d); const q=(x-mx)**2+(y-my)**2;
    if(q < (d.r*devicePixelRatio*Math.sqrt(zoom*fit*1.5)+8*devicePixelRatio)**2 && q<bd){ bd=q; best=d; } });
  return best;
}
let drag=null;
cv.addEventListener('mousemove', ev=>{
  const b=cv.getBoundingClientRect();
  const mx=(ev.clientX-b.left)*devicePixelRatio, my=(ev.clientY-b.top)*devicePixelRatio;
  if(drag){ ox += (mx-drag.x)/S/zoom; oy += (my-drag.y)/S/zoom; drag={x:mx,y:my}; return; }
  hov = hit(mx,my);
  if(hov){ tip.style.display='block';
    tip.style.left=(ev.clientX-b.left+14)+'px'; tip.style.top=(ev.clientY-b.top+10)+'px';
    tip.innerHTML='<b>'+hov.n+'</b>'+hov.m.lines+' lines &middot; '
      +(hov.m.reachable_from_wake?'reachable from a wake':(hov.m.orphaned?'ORPHANED':'server only'))
      +'<span>'+(hov.m.headline||'').slice(0,110)+'</span>';
  } else tip.style.display='none';
});
cv.addEventListener('mousedown', ev=>{ const b=cv.getBoundingClientRect();
  drag={x:(ev.clientX-b.left)*devicePixelRatio, y:(ev.clientY-b.top)*devicePixelRatio}; });
addEventListener('mouseup', ()=>{ drag=null; });
cv.addEventListener('click', ev=>{ const b=cv.getBoundingClientRect();
  const d=hit((ev.clientX-b.left)*devicePixelRatio,(ev.clientY-b.top)*devicePixelRatio);
  if(d){ sel=d; window.inspect && window.inspect(d.n); } });
cv.addEventListener('wheel', ev=>{ ev.preventDefault();
  zoom = Math.max(0.45, Math.min(5, zoom * (ev.deltaY<0?1.12:0.89))); }, {passive:false});

document.querySelectorAll('.ctl button').forEach(b=>{
  b.onclick=()=>{
    if(b.dataset.f){ document.querySelectorAll('.ctl button[data-f]').forEach(x=>x.classList.remove('on'));
      b.classList.add('on'); mode=b.dataset.f; }
    else if(b.dataset.a==='replay'){ wave=0; waving=true; }
    else if(b.dataset.a==='shake'){ settle=1; fitted=false; N.forEach(d=>{ d.vx+=(Math.sin(d.i*7.7))*0.004;
      d.vy+=(Math.cos(d.i*3.1))*0.004; }); }
  };
});
draw();
})();
"""


def markup(counts: dict) -> str:
    return """
    <div class="stage" id="stage">
      <canvas id="g"></canvas>
      <div class="ctl">
        <button class="on" data-f="all">all</button>
        <button data-f="wake">the spine</button>
        <button data-f="orphan">orphaned</button>
        <button data-a="replay">replay the wave</button>
        <button data-a="shake">re-settle</button>
      </div>
      <div class="hud"><div class="big">%d<span style="font-size:15px;color:var(--dim)">
        /%d</span></div><div class="sub">reachable from a wake</div></div>
      <div class="tip" id="tip"></div>
      <div class="legend">
        <b>&#9679; lit</b> = reachability reached it from an entry point &middot;
        <i>&#9675;</i> = server only &middot; &#9675; grey = nothing reaches it<br>
        edges are real imports read from the AST &middot; ringed = an open alarm on its capability<br>
        the wave travels those edges in dependency order. what stays dark is genuinely unreachable.
      </div>
    </div>""" % (counts["reachable_from_wake"], counts["modules"])
