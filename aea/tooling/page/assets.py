"""assets.py - THE STYLESHEET AND THE SCRIPT, as files the page LINKS rather than swallows.

MEASURED, and the measurement is the whole argument. The published page was 2,328 lines:

    1,226   dark-field dots that no frame rule ever touches   -> assets/field.svg
      327   generated frame rules, one per (frame, layer)     -> assets/frames.css
      143   this stylesheet                                    -> assets/base.css
       64   this script                                        -> assets/page.js
      108   the actual markup of the page

So 93 percent of the artefact was material nobody reads and every diff of a one-line copy change
arrived buried in it. Splitting costs the page its single-file portability - it now needs its
`assets/` beside it - and buys a document a person can read, a diff that shows what changed, and
four files a browser can cache separately.

BOTH BODIES MOVED VERBATIM, as f-strings. Every literal brace in the CSS and the JS is doubled
exactly as it was inside the template; re-deriving that by hand is precisely how a moved block
stops being the same block.
"""
from __future__ import annotations


def base_css() -> str:
    """The hand-written stylesheet. The GENERATED frame rules are a separate file - they are
    machine output with one rule per frame, and mixing them here hid 327 lines inside 143."""
    return f""":root{{--void:#08090b;--grey:#3a3f46;--dim:#171a1e;--ink:#c8ccd2;--amber:#ffb000;--brass:#d4a24c;
/* TWO TYPE ROLES, AND THE DIFFERENCE CARRIES MEANING RATHER THAN TASTE.
   PROSE is a person explaining. MONO is the machine's measured output - an id, a count, a receipt.
   Setting the whole page in mono made every word look like output, which is the exact costume every
   dashboard on the internet is wearing, and it wasted the one signal that should mean "this number
   was measured". Measured on the field: `ourworldindata` pairs a serif display with a humanist sans
   and reserves Menlo for figures; `distill.pub` sets its body in Georgia at a 700-800px measure;
   `quanta` runs a 520px column of near-black with a single orange accent. None of them sets an
   article in a terminal face. No webfont is loaded - a page whose claim is that it needs nothing
   from anywhere should not open a connection to fetch a letterform. */
/* THE SCALES. Before this, every value was invented at its call site - 34px here, 44px there,
   13px, 11.5px, 9.5px - so each new section re-negotiated its own rhythm and the page drifted a
   little further from itself every time something was added. A scale is not decoration: it is the
   thing that makes the NEXT section free instead of a fight.
   Spacing is a x1.6 progression; type is a x1.25 minor-third, the interval editorial pages use
   because adjacent steps stay distinguishable without shouting. */
--s1:4px;--s2:8px;--s3:13px;--s4:21px;--s5:34px;--s6:55px;--s7:89px;
--t0:11px;--t1:13px;--t2:14.5px;--t3:16px;--t4:20px;--t5:26px;
/* CONTRAST, MEASURED AGAINST --void #08090b RATHER THAN CHOSEN BY EYE. Four text roles were
   below the 4.5:1 floor, and the worst of them - 2.52:1 - was `.src`, the provenance line that
   names the file each number came from. A page whose moral position is "here is where I read this"
   printing that sentence at half legibility is the least affordable failure available to it.
   --f1 5.3:1 · --f2 4.9:1 · both pass at the small sizes actually used here. */
--f1:#7d858e;--f2:#828b95;--f3:#3f4750;
--prose:"Iowan Old Style",Palatino,"Palatino Linotype",Georgia,"Times New Roman",serif;
--mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--void);color:var(--ink);
 font:16px/1.62 var(--prose);font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1180px;margin:0 auto;padding:var(--s5) var(--s4) var(--s7)}}
/* MEASURE. 74ch of 13px mono is a wall; the sites that are read for pleasure sit
   between 520 and 800px. Prose narrows, the instrument keeps the whole width. */
.sub,.rplain,.youare,.honest{{max-width:64ch}}
h1{{font:600 15px/1.4 var(--mono);letter-spacing:.20em;margin:0 0 2px;color:#eef1f4}}
h2{{font:600 11px/1.4 var(--mono);letter-spacing:.20em;color:#7d858e;margin:var(--s6) 0 var(--s3);
 border-top:1px solid #1c2025;padding-top:12px}}
.sub{{color:#96a0aa;margin:0 0 24px;max-width:62ch;font-size:16.5px;line-height:1.66}}
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
 solid #131619;color:var(--f2);font:inherit;padding:11px 13px;cursor:pointer;text-align:left}}
#rail button:hover,#rrail button:hover{{background:#0d1013;color:#aeb5bd}}
#rail button[aria-current="step"],#rrail button[aria-current="step"]{{background:#0e1114;color:#eef1f4;
 box-shadow:inset 2px 0 0 var(--amber)}}
#rail b,#rrail b{{font-size:10px;letter-spacing:.14em;font-weight:600;width:44px}}
#rail span,#rrail span{{color:var(--brass);font-size:11px;width:30px}}
#rail em,#rrail em{{color:var(--f1);font-style:normal;font-size:10px;margin-left:auto}}
.canvas{{flex:1;min-width:0}}
.rails{{display:flex;flex-direction:column;border-right:1px solid #16191d;min-width:150px}}
.modes{{display:flex;border-bottom:1px solid #16191d}}
.modes button{{flex:1;background:none;border:0;color:var(--f1);font:inherit;font-size:9.5px;
 letter-spacing:.12em;padding:9px 4px;cursor:pointer}}
.modes button.on{{color:var(--amber);background:#0e1114}}
.modes button:hover{{color:#aeb5bd}}
#cap{{margin:0;padding:11px 14px;border-top:1px solid #16191d;color:#8b939c;font-size:11.5px}}
/* REACHED ONLY THROUGH A DISPATCH TABLE. Hollow, and its branch is dashed - the organism does get
   here, and the edge is an upper bound rather than a call site, so the mark says so instead of
   averaging the two into one dot. 13 of the 157. */
.node.viadisp{{fill:#0a0c0e;stroke:var(--f2);stroke-width:1.4}}
.branch.dispatch{{stroke-dasharray:3 3;opacity:.5}}
.node.core{{fill:#fff;stroke:var(--amber);stroke-width:3}}
.node.hub{{fill:#0a0c0e;stroke:var(--amber);stroke-width:2}}
.halo{{fill:none;stroke:var(--amber);stroke-width:1;opacity:.32}}
.lbl{{fill:#7f8892;font-size:9px;letter-spacing:.09em}}
.rootlbl{{fill:var(--amber);font-size:10px;letter-spacing:.22em;font-weight:600}}
.legend{{display:flex;gap:22px;flex-wrap:wrap;padding:12px 14px;border-top:1px solid #16191d;
 color:var(--f2);font-size:11px}}
.legend i{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;
 vertical-align:middle}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:var(--s3)}}
.card{{border:1px solid #16191d;padding:var(--s4);background:#0a0c0e}}
.big{{font:30px/1.2 var(--mono);color:#eef1f4;letter-spacing:-.02em}}
.big em{{font-size:13px;color:var(--f1);font-style:normal}}
.cap{{font-size:10px;letter-spacing:.17em;color:var(--f2);text-transform:uppercase;margin-bottom:7px}}
.src{{font-size:10px;color:var(--f1);margin-top:8px}}
.row{{display:flex;align-items:center;gap:10px;margin:5px 0}}
.k{{width:170px;color:#8b939c;font-size:11.5px}}
.bar{{flex:1;height:5px;background:#14171b;position:relative;overflow:hidden}}
.bar i{{position:absolute;inset:0 auto 0 0;background:var(--brass)}}
.v{{width:92px;text-align:right;color:#dfe3e8}} .v em{{color:#525a63;font-style:normal}}
.n{{width:150px;color:var(--f1);font-size:11px}}
.step{{display:flex;gap:11px;align-items:baseline;padding:7px 0;border-bottom:1px solid #131619}}
.step b{{font-size:10px;letter-spacing:.13em;width:74px}}
.step.done b{{color:var(--amber)}} .step.open b{{color:var(--f2)}}
.step span{{flex:1;color:#aeb5bd}} .step em{{color:var(--f1);font-style:normal}}
.rod{{display:flex;gap:12px;padding:4px 0;border-bottom:1px solid #111417}}
.rod .s{{color:var(--brass);width:52px}} .rod .m{{flex:1;color:#aeb5bd;overflow:hidden;
 text-overflow:ellipsis;white-space:nowrap}} .rod .l{{color:var(--f1);width:60px;text-align:right}}
.growth{{display:flex;gap:7px;align-items:flex-end;height:96px}}
.g{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%}}
.g i{{width:100%;background:var(--brass);opacity:.65;display:block}}
.g span{{font-size:9.5px;color:var(--f1);margin-top:5px}}
.honest{{margin-top:var(--s6);padding:var(--s4);border:1px solid #1c2025;color:#7d858e;font-size:11.5px;
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
/* THE CLIMB IS THE READING PART OF THE PAGE, so it takes the prose face and the mono keeps the
   identifiers and the receipts. The plain name is the headline a stranger reads; the formal title
   and the evidence line stay machine-voiced, which is what they are. */
.rhuman{{font:17px/1.35 var(--prose);letter-spacing:0}}
.rplain{{font:15px/1.62 var(--prose)}}
.rid,.rtitle,.rev,.rwait,.rstat{{font-family:var(--mono)}}
.youare{{font:15.5px/1.66 var(--prose)}}
.honest{{font:14.5px/1.6 var(--prose)}}
.honest b{{font-family:var(--mono)}}
.src,.cap,.k,.n,.v,#cap,.legend,.step,.rod,.g span{{font-family:var(--mono)}}
/* THE DECK. One line under each heading saying why this section follows the last one. Four sections
   of equal weight with nothing between them read as an inventory; an argument needs connectives. */
/* FOCUS WAS UNSTYLED ON ALL 32 CONTROLS - `border:0;background:none` leaves only the UA ring, which
   differs per browser and is invisible on several. Amber is earned here: focus IS an active state. */
#rail button:focus-visible,#rrail button:focus-visible,#crail button:focus-visible,
.modes button:focus-visible{{outline:2px solid var(--amber);outline-offset:-2px}}

/* THE HERO WAS 118px WIDE ON A PHONE. The rails hold a 150px minimum against a 318px stage, so the
   graph got what was left and a 3px node drew at 0.35px - the entire argument, unreadable. Below
   760px the rails become a horizontal strip and the picture takes the full width. */
@media (max-width:760px){{
 .stage{{flex-direction:column}}
 .rails{{border-right:0;border-bottom:1px solid #16191d;min-width:0}}
 #rail,#rrail{{flex-direction:row;overflow-x:auto;-webkit-overflow-scrolling:touch}}
 #rail button,#rrail button{{border-bottom:0;border-right:1px solid #131619;white-space:nowrap}}
 #rail em,#rrail em{{display:none}}
 .rod .m{{white-space:normal;overflow-wrap:anywhere}}
}}
.deck{{margin:0 0 var(--s4);max-width:66ch;font:var(--t2)/1.6 var(--prose);color:#7d858e}}
/* THE CONTROL SAYS IT IS A CONTROL. It was a rail of buttons with no affordance, so the opening
   had to explain in prose that the picture could be stepped. A label beats a sentence about it. */
.railhint{{margin:0;padding:var(--s2) var(--s3) 0;font:var(--t0)/1.4 var(--mono);letter-spacing:.1em;
 color:var(--f1);text-transform:uppercase}}
.railhint kbd{{font:inherit;border:1px solid #2b3138;border-radius:2px;padding:0 4px;color:#8b939c}}
"""


def captions_js(*, caps_js, rcaps, MAXD, RREST) -> str:
    """PURE DATA, and the only file that changes when the entity ticks.

    It was one 8 KB line wedged into the middle of the controller, so every rebuild rewrote the
    whole script and a behaviour change could not be told from a caption moving. Data and behaviour
    in one file means neither has a readable history."""
    return f"""/* GENERATED. Every string here was measured; none was written. */
window.AEA={{
  hop:{caps_js},
  rung:{rcaps},
  maxd:{MAXD},
  rest:{RREST}
}};


"""


def instrument_js() -> str:
    """THE CONTROLLER. One integer of state, three controls that cannot disagree."""
    return f"""/* ONE INTEGER, TWO AXES, THREE CONTROLS THAT CANNOT DISAGREE.
   The entire state of this instrument is (mode, frame) over coordinates computed once and never
   recomputed, so going backward is exactly symmetric and free: clicking hop 2 after hop 6 removes
   precisely what hops 3-6 added, with no residue and no replayed arrival.

   THE CONTROLS ARE THREE VIEWS OF THE SAME STATE, not three states: the mode buttons, the rail
   beside the graph, and THE CLIMB rail far below. They were two independent controllers writing
   different attributes with different vocabularies, and the result was measurable on a screenshot -
   the landing view drew the climb's near-empty frame under a caption from a third source while the
   rail insisted it was showing HOP 6 of the full graph. Every path into a frame now goes through
   go(), and go() writes all three. */
var D=window.AEA||{{hop:[],rung:[],maxd:0,rest:0}};
var CAPS=D.hop,RCAPS=D.rung,MAXD=D.maxd,RMAX=RCAPS.length-1,RREST=D.rest;
var svg=document.getElementById('org'),cap=document.getElementById('cap'),
    rail=document.getElementById('rail'),rrail=document.getElementById('rrail'),
    mh=document.getElementById('m-hop'),mr=document.getElementById('m-rung'),
    climb=document.getElementById('climb'),crail=document.getElementById('crail'),
    mode='hop',timer=null;
function stop(){{if(timer){{clearInterval(timer);timer=null;}}}}
function go(k){{var max=mode==='hop'?MAXD:RMAX,r=mode==='hop'?rail:rrail;
 k=Math.max(0,Math.min(max,k));
 svg.setAttribute('data-frame',k);svg.setAttribute('data-mode',mode);
 var _t=(mode==='hop'?CAPS:RCAPS)[k]||'';cap.textContent=_t;
 /* THE PICTURE MUST SAY WHAT CHANGED. A static label across 7 hops and 12 rungs
    means a keyboard user operates 32 controls and is told nothing. */
 svg.setAttribute('aria-label',_t);
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

"""


def playback_js() -> str:
    """THE NARRATION. Owned by the section it illustrates, and it waits to be looked at."""
    return f"""
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
"""
