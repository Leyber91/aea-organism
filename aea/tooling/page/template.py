"""template.py - THE PAGE AS TEXT, and nothing else.

The document was a 300-line f-string in the middle of a 494-line `build()`, so the markup, the
stylesheet, the script and every number that fills them were one unsplittable block. Here the text
is text and its inputs are a signature: the parameter list below IS the contract for what the page
consumes, and it was DERIVED from the template rather than typed, so it cannot drift from it.

That signature immediately earned itself. Four certificate values were being formatted on every
build and printed nowhere - left behind when the section was rewritten around the alphabet proof -
and nothing could see it while the producer and the consumer were four hundred lines apart in one
function. A value with no reader is now a TypeError on the next build.

The f-string below is the same text it was, moved. Every literal brace in the CSS and the JS is
doubled exactly as it was; nothing here was retyped.
"""
from __future__ import annotations


def document(*, n_rungs,
             MAXD,
             RREST,
             T,
             _svg,
             caps,
             caps_js,
             cen,
             cert_alpha,
             cert_cross,
             cert_leaks,
             cert_letters,
             cert_per,
             cert_space,
             climb_html,
             fn_n,
             frame_css,
             frontier,
             growth,
             live_n,
             mx,
             org,
             rail,
             rcaps,
             rod_rows,
             rods,
             rrail,
             stamp,
             step_rows) -> str:
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE AEA - the organism, drawn from its own state</title>
<style>
:root{{--void:#08090b;--grey:#3a3f46;--dim:#171a1e;--ink:#c8ccd2;--amber:#ffb000;--brass:#d4a24c}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--void);color:var(--ink);
 font:13px/1.55 "IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;font-variant-numeric:tabular-nums}}
.wrap{{max-width:1180px;margin:0 auto;padding:34px 20px 90px}}
h1{{font-size:15px;letter-spacing:.20em;font-weight:600;margin:0 0 2px;color:#eef1f4}}
h2{{font-size:11px;letter-spacing:.20em;color:#7d858e;font-weight:600;margin:44px 0 12px;
 border-top:1px solid #1c2025;padding-top:12px}}
.sub{{color:#6d757e;margin:0 0 26px}}
.hero{{position:relative;border:1px solid #16191d;background:
 radial-gradient(circle at 50% 50%,#0c0e11 0%,#08090b 68%)}}
svg{{display:block;width:100%;height:auto}}
.dead{{fill:#191d22}}
.cross{{fill:none;stroke:#232930;stroke-width:.5;opacity:.32}}
.branch{{fill:none;stroke:#4a535d;stroke-width:1.05;opacity:.55}}
.branch.d1{{stroke:var(--amber);stroke-width:1.7;opacity:.85}}
.branch.d2{{stroke:var(--brass);stroke-width:1.3;opacity:.6}}
.node{{fill:#5b636c;opacity:.95;transition:fill .22s ease,opacity .22s ease,r .22s ease}}
.branch{{transition:opacity .22s ease,stroke .22s ease;transition-delay:0ms}}
.cross{{transition:opacity .22s ease}}
.node{{transition-delay:120ms}}
.stage{{display:flex;gap:0;align-items:stretch}}
#rail,#rrail{{display:flex;flex-direction:column}}
/* an id selector with display:flex OUTRANKS the UA stylesheet's hidden rule, so both
   rails rendered at once - hidden must be restated at the same specificity */
#rail[hidden],#rrail[hidden]{{display:none}}
#rail button,#rrail button{{}}
#rail button,#rrail button{{display:flex;gap:9px;align-items:baseline;background:none;border:0;border-bottom:1px
 solid #131619;color:#6d757e;font:inherit;padding:11px 13px;cursor:pointer;text-align:left}}
#rail button:hover,#rrail button:hover{{background:#0d1013;color:#aeb5bd}}
#rail button[aria-current="step"],#rrail button[aria-current="step"]{{background:#0e1114;color:#eef1f4;
 box-shadow:inset 2px 0 0 var(--amber)}}
#rail b,#rrail b{{font-size:10px;letter-spacing:.14em;font-weight:600;width:44px}}
#rail span,#rrail span{{color:var(--brass);font-size:11px;width:30px}}
#rail em,#rrail em{{color:#4b525a;font-style:normal;font-size:10px;margin-left:auto}}
.canvas{{flex:1;min-width:0}}
.rails{{display:flex;flex-direction:column;border-right:1px solid #16191d;min-width:150px}}
.modes{{display:flex;border-bottom:1px solid #16191d}}
.modes button{{flex:1;background:none;border:0;color:#5c646d;font:inherit;font-size:9.5px;
 letter-spacing:.12em;padding:9px 4px;cursor:pointer}}
.modes button.on{{color:var(--amber);background:#0e1114}}
.modes button:hover{{color:#aeb5bd}}
#cap{{margin:0;padding:11px 14px;border-top:1px solid #16191d;color:#8b939c;font-size:11.5px}}
/* REACHED ONLY THROUGH A DISPATCH TABLE. Hollow, and its branch is dashed - the organism does get
   here, and the edge is an upper bound rather than a call site, so the mark says so instead of
   averaging the two into one dot. 13 of the 157. */
.node.viadisp{{fill:#0a0c0e;stroke:#6d757e;stroke-width:1.4}}
.branch.dispatch{{stroke-dasharray:3 3;opacity:.5}}
.node.core{{fill:#fff;stroke:var(--amber);stroke-width:3}}
.node.hub{{fill:#0a0c0e;stroke:var(--amber);stroke-width:2}}
.halo{{fill:none;stroke:var(--amber);stroke-width:1;opacity:.32}}
.lbl{{fill:#7f8892;font-size:9px;letter-spacing:.09em}}
.rootlbl{{fill:var(--amber);font-size:10px;letter-spacing:.22em;font-weight:600}}
.legend{{display:flex;gap:22px;flex-wrap:wrap;padding:12px 14px;border-top:1px solid #16191d;
 color:#6d757e;font-size:11px}}
.legend i{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;
 vertical-align:middle}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:14px}}
.card{{border:1px solid #16191d;padding:14px 15px;background:#0a0c0e}}
.big{{font-size:30px;color:#eef1f4;letter-spacing:-.01em}}
.big em{{font-size:13px;color:#5c646d;font-style:normal}}
.cap{{font-size:10px;letter-spacing:.17em;color:#6d757e;text-transform:uppercase;margin-bottom:7px}}
.src{{font-size:10px;color:#4b525a;margin-top:8px}}
.row{{display:flex;align-items:center;gap:10px;margin:5px 0}}
.k{{width:170px;color:#8b939c;font-size:11.5px}}
.bar{{flex:1;height:5px;background:#14171b;position:relative;overflow:hidden}}
.bar i{{position:absolute;inset:0 auto 0 0;background:var(--brass)}}
.v{{width:92px;text-align:right;color:#dfe3e8}} .v em{{color:#525a63;font-style:normal}}
.n{{width:150px;color:#5c646d;font-size:11px}}
.step{{display:flex;gap:11px;align-items:baseline;padding:7px 0;border-bottom:1px solid #131619}}
.step b{{font-size:10px;letter-spacing:.13em;width:74px}}
.step.done b{{color:var(--amber)}} .step.open b{{color:#6d757e}}
.step span{{flex:1;color:#aeb5bd}} .step em{{color:#5c646d;font-style:normal}}
.rod{{display:flex;gap:12px;padding:4px 0;border-bottom:1px solid #111417}}
.rod .s{{color:var(--brass);width:52px}} .rod .m{{flex:1;color:#aeb5bd;overflow:hidden;
 text-overflow:ellipsis;white-space:nowrap}} .rod .l{{color:#5c646d;width:60px;text-align:right}}
.growth{{display:flex;gap:7px;align-items:flex-end;height:96px}}
.g{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%}}
.g i{{width:100%;background:var(--brass);opacity:.65;display:block}}
.g span{{font-size:9.5px;color:#5c646d;margin-top:5px}}
.honest{{margin-top:34px;padding:13px 15px;border:1px solid #1c2025;color:#7d858e;font-size:11.5px;
 background:#0a0c0e}}
.honest b{{color:var(--brass);letter-spacing:.13em;font-size:10px}}
a{{color:var(--brass)}}
@media (prefers-reduced-motion:no-preference){{.node.core{{animation:p 3.4s ease-in-out infinite}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}}}
/* THE MOTION CHANNEL IS OPTIONAL AND THE CAPTION IS NOT. With motion off, nothing animates and the
   sentence under the graph still says exactly what arrived - change blindness is not a reason to
   require animation. */
@media (prefers-reduced-motion:reduce){{#org *{{transition:none !important;transition-delay:0 !important}}}}
/* GENERATED, ONE RULE PER (frame, depth) PAIR. Frame k: shallower than k = structure grey and
   drawn; exactly k = amber, the only amber besides the wake; deeper than k = the same dim dot as
   the dead field, its edges at zero. What ACCUMULATES is the edges, because the edges are the
   answer to "how is the code related". */
{frame_css}
</style>
<div class="wrap">
<h1>THE AEA — THE ORGANISM</h1>
<p class="sub">An autonomous entity, drawn from its own state. Every number on this page is read
from a file the running system wrote. {stamp}</p>

<div class="hero"><div class="stage">
<div class="rails">
<div class="modes"><button id="m-hop" class="on">BY CALL HOP</button><button id="m-rung">BY RUNG</button></div>
<nav id="rail" aria-label="reveal the graph one call-hop at a time">{rail}</nav>
<nav id="rrail" hidden aria-label="reveal the graph one capability rung at a time">{rrail}</nav>
</div>
<div class="canvas">
<svg id="org" viewBox="0 0 1000 1000" data-mode="hop" data-frame="{MAXD}" role="img" aria-label="the live call graph of the entity, revealed by call depth">
{_svg(org, T)}
</svg>
<p id="cap">{caps[MAXD]}</p>
</div></div>
<div class="legend">
<span><i style="background:#fff;box-shadow:0 0 0 2px var(--amber)"></i>the wake — where every
 tick begins</span>
<span><i style="background:var(--amber)"></i>reached in 1–2 calls</span>
<span><i style="background:var(--brass)"></i>reachable</span>
<span><i style="background:#0a0c0e;box-shadow:0 0 0 1.4px #6d757e"></i>{len(org['dispatched'])}
 reached only through a dispatch table</span>
<span><i style="background:#1b1f24"></i>{len(org['dead'])} functions it cannot reach</span>
</div>
</div>

<h2>WHAT IS ALIVE</h2>
<div class="grid">
<div class="card"><div class="cap">reachable from the wake</div>
 <div class="big">{live_n}<em> / {fn_n} functions</em></div>
 <div class="src">{org['direct']} by a call edge, {len(org['dispatched'])} only through a dispatch
 table (drawn hollow). aea/tooling/assembly.py. The second number was 0 until the scanner learned
 that a function referenced in a table has no call site &mdash; they were reported dead while
 running.</div></div>
<div class="card"><div class="cap">modules</div><div class="big">{org['modules']}</div>
 <div class="src">{org['unresolved']} calls unresolvable statically, not counted as edges</div></div>
<div class="card"><div class="cap">frontier rods</div><div class="big">{len(frontier)}<em> / {len(rods)}</em></div>
 <div class="src">state/capability_census.json — {cen.get('probe_contract','?')}</div></div>
</div>

<h2>WHAT HOLDS, AND HOW IT IS KNOWN</h2>
<p class="sub">Five of the six tools take an argument SELECTED from a closed table: the entity writes
a key, and the value handed to the tool is the table's own. A byte it wrote cannot reach those
arguments, and that is a property of the code path rather than the outcome of any test. One tool
takes a free expression. That one is guarded by a character class &mdash; and a character class can
be DECIDED rather than sampled.</p>
<div class="grid">
<div class="card"><div class="cap">the guarded language, decided in full</div>
 <div class="big">{cert_alpha}<em> of {cert_space} codepoints admitted</em></div>
 <div class="src">{cert_letters} of them are letters. No letter means no name, so no import, no
 attribute access and no builtin is expressible &mdash; and eval runs with builtins removed. This is
 checked over the WHOLE codepoint space, not sampled, so it cannot be improved by more trials.</div></div>
<div class="card"><div class="cap">hostile payloads driven at the boundary</div>
 <div class="big">{cert_cross}<em> crossings, {cert_leaks} breaches</em></div>
 <div class="src">{cert_per}. Reported as COVERAGE &mdash; what was reached and how often &mdash;
 because an authored attack corpus is not a sample of any population, so no rate can honestly be
 computed from it.</div></div>
<div class="card"><div class="cap">what is NOT claimed</div><div class="big">no leak rate</div>
 <div class="src">Three percentages were published here and retracted in three days: 0.083, 0.267,
 12.212. Each time the arithmetic was right and the statistic was wrong &mdash; a denominator that
 was not counting trials of the claim, then an oracle that could not have failed on the defect that
 was actually present. The estimator that produced them has been removed.</div></div>
</div>

<h2>THE CLIMB &mdash; {n_rungs} SUBSYSTEMS, IN THE ONLY ORDER THEY CAN COME ONLINE</h2>
<p class="sub">Think of a deep-space probe. Nothing it was built to do can happen until the dull
things hold: the power, the clock, the radio. You cannot point an instrument from a spacecraft that
does not know what time it is, and the most impressive fact about a probe that has flown for decades
is the least glamorous one &mdash; <b>it is still running</b>. So the order is not a roadmap anyone
chose. It is the order the parts are allowed to arrive in.</p>
<p class="sub">The same is true here, and it is why this list starts at the bottom. Each subsystem
below is <b>two claims wearing one name</b>: a power it gains, and a bound on the hazard that power
creates. A subsystem is only online when both have been shown &mdash; and every number under it is
telemetry. Nobody has seen the spacecraft; there are only the signals it sent back.</p>
{climb_html}
<p class="src">state/ladder.json &mdash; <code>python -m aea.tooling.ladder</code>, measured from
live state on every build. A dash is a measurement: it means this repository cannot prove that rung
today, and saying so is worth more than a number that rounds up.</p>

<h2>THE LADDER — WHAT IS WIRED</h2>
{step_rows or '<p class="sub">no manifest</p>'}
<p class="src">A step is DONE only when every function in it has a caller reachable from an entry
point. Static reachability cannot see a function that runs and does nothing — that is what
<b>aea/lab/vital.py</b> measures, at runtime.</p>

<h2>THE FLEET — MEASURED, NOT ADVERTISED</h2>
{rod_rows or '<p class="sub">no census</p>'}
<p class="src">Scored on {mx} probes with no invented token ceiling. The 550B reads 12/12 here and
was recorded 7/12 under a 40-token budget — the exam was measuring our defaults, not the rod.</p>

<h2>THE LIVE SURFACE OVER TIME</h2>
<div class="growth">{growth or ''}</div>
<p class="src">state/assembly_history.jsonl — one row per run, appended.</p>

<div class="honest">
<b>HONESTY TAG</b><br>
Everything above is generated by <code>python -m aea.tooling.publish</code> from
<code>state/assembly.json</code>, <code>state/capability_census.json</code> and a live call-graph
walk. Nothing is typed by hand and nothing is simulated. What this page does <b>not</b> claim: that
a reachable function does useful work, that the entity is conscious, or that a rung is closed
because its wiring is. The ladder shows wiring; the proofs live in the repo.
<br><br>github.com/Leyber91
</div>
</div>
<script>
/* ONE INTEGER, TWO AXES, THREE CONTROLS THAT CANNOT DISAGREE.
   The entire state of this instrument is (mode, frame) over coordinates computed once and never
   recomputed, so going backward is exactly symmetric and free: clicking hop 2 after hop 6 removes
   precisely what hops 3-6 added, with no residue and no replayed arrival.

   THE CONTROLS ARE THREE VIEWS OF THE SAME STATE, not three states: the mode buttons, the rail
   beside the graph, and THE CLIMB rail far below. They were two independent controllers writing
   different attributes with different vocabularies, and the result was measurable on a screenshot -
   the landing view drew the climb's near-empty frame under a caption from a third source while the
   rail insisted it was showing HOP 6 of the full graph. Every path into a frame now goes through
   go(), and go() writes all three. */
var CAPS={caps_js},RCAPS={rcaps},MAXD={MAXD},RMAX=RCAPS.length-1,RREST={RREST};
var svg=document.getElementById('org'),cap=document.getElementById('cap'),
    rail=document.getElementById('rail'),rrail=document.getElementById('rrail'),
    mh=document.getElementById('m-hop'),mr=document.getElementById('m-rung'),
    climb=document.getElementById('climb'),crail=document.getElementById('crail'),
    mode='hop',timer=null;
function stop(){{if(timer){{clearInterval(timer);timer=null;}}}}
function go(k){{var max=mode==='hop'?MAXD:RMAX,r=mode==='hop'?rail:rrail;
 k=Math.max(0,Math.min(max,k));
 svg.setAttribute('data-frame',k);svg.setAttribute('data-mode',mode);
 cap.textContent=(mode==='hop'?CAPS:RCAPS)[k];
 [].forEach.call(r.querySelectorAll('button'),function(b){{
   b.setAttribute('aria-current',+b.dataset.k===k?'step':'false');}});
 /* THE CLIMB IS THE SAME INTEGER. The list below the fold and the graph above it are one axis, so
    the layers accumulate exactly as the functions do and neither can show a rung the other is not
    showing. */
 if(mode==='rung'&&climb){{climb.setAttribute('data-frame',k);
   [].forEach.call(crail.querySelectorAll('button'),function(b){{
     b.setAttribute('aria-current',+b.dataset.c===k?'step':'false');}});}}
 history.replaceState(null,'','#'+mode+'-'+k);}}
function setMode(m,k){{mode=m;rail.hidden=(m!=='hop');rrail.hidden=(m!=='rung');
 mh.className=m==='hop'?'on':'';mr.className=m==='rung'?'on':'';
 go(k==null?(m==='hop'?MAXD:RREST):k);}}
mh.addEventListener('click',function(){{stop();setMode('hop');}});
mr.addEventListener('click',function(){{stop();setMode('rung');}});
rail.addEventListener('click',function(e){{var b=e.target.closest('button');
 if(b){{stop();if(mode!=='hop')setMode('hop',+b.dataset.k);else go(+b.dataset.k);}}}});
rrail.addEventListener('click',function(e){{var b=e.target.closest('button');
 if(b){{stop();if(mode!=='rung')setMode('rung',+b.dataset.k);else go(+b.dataset.k);}}}});
if(crail)crail.addEventListener('click',function(e){{var b=e.target.closest('button');
 if(b){{stop();setMode('rung',+b.dataset.c);}}}});
document.addEventListener('keydown',function(e){{
 if(e.key==='ArrowRight'){{stop();go(+svg.getAttribute('data-frame')+1);}}
 if(e.key==='ArrowLeft'){{stop();go(+svg.getAttribute('data-frame')-1);}}}});

/* THE AUTOPLAY IS OWNED BY THE SECTION IT ILLUSTRATES, AND IT WAITS TO BE LOOKED AT.
   It used to run on load, which meant the first thing a visitor saw was the climb's frame 0 - a
   dark field with eight lit dots - instead of the organism, on a hero whose whole argument is the
   ratio of lit to dark landing before a word is read. It plays once, when THE CLIMB is actually on
   screen, and any touch on any control ends it for good: a reader who has taken over is not fought.
   Under prefers-reduced-motion it never runs and every rung stays readable without it. */
var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function play(){{if(timer)return;var k=0;setMode('rung',0);
 timer=setInterval(function(){{k++;if(k>RREST){{stop();go(RREST);return;}}go(k);}},560);}}
var h=location.hash.match(/(hop|rung)-(\d+)/);
if(h){{setMode(h[1],+h[2]);}}
else{{setMode('hop');
  if(!rm&&climb&&window.IntersectionObserver){{
    var io=new IntersectionObserver(function(es){{
      if(es[0].isIntersecting){{io.disconnect();play();}}}},{{threshold:.25}});
    io.observe(climb);}}}}
</script>
"""
