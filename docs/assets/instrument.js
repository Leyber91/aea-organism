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
var D=window.AEA||{hop:[],rung:[],maxd:0,rest:0};
var CAPS=D.hop,RCAPS=D.rung,MAXD=D.maxd,RMAX=RCAPS.length-1,RREST=D.rest;
var svg=document.getElementById('org'),cap=document.getElementById('cap'),
    rail=document.getElementById('rail'),rrail=document.getElementById('rrail'),
    mh=document.getElementById('m-hop'),mr=document.getElementById('m-rung'),
    climb=document.getElementById('climb'),crail=document.getElementById('crail'),
    mode='hop',timer=null;
function stop(){if(timer){clearInterval(timer);timer=null;}}
function go(k){var max=mode==='hop'?MAXD:RMAX,r=mode==='hop'?rail:rrail;
 k=Math.max(0,Math.min(max,k));
 svg.setAttribute('data-frame',k);svg.setAttribute('data-mode',mode);
 var _t=(mode==='hop'?CAPS:RCAPS)[k]||'';cap.textContent=_t;
 /* THE PICTURE MUST SAY WHAT CHANGED. A static label across 7 hops and 12 rungs
    means a keyboard user operates 32 controls and is told nothing. */
 svg.setAttribute('aria-label',_t);
 [].forEach.call(r.querySelectorAll('button'),function(b){
   b.setAttribute('aria-current',+b.dataset.k===k?'step':'false');});
 /* THE CLIMB IS THE SAME INTEGER. The list below the fold and the graph above it are one axis, so
    the layers accumulate exactly as the functions do and neither can show a rung the other is not
    showing. */
 if(mode==='rung'&&climb){climb.setAttribute('data-frame',k);
   [].forEach.call(crail.querySelectorAll('button'),function(b){
     b.setAttribute('aria-current',+b.dataset.c===k?'step':'false');});}
 history.replaceState(null,'','#'+mode+'-'+k);}
function setMode(m,k){mode=m;rail.hidden=(m!=='hop');rrail.hidden=(m!=='rung');
 mh.className=m==='hop'?'on':'';mr.className=m==='rung'?'on':'';
 go(k==null?(m==='hop'?MAXD:RREST):k);}
mh.addEventListener('click',function(){stop();setMode('hop');});
mr.addEventListener('click',function(){stop();setMode('rung');});
rail.addEventListener('click',function(e){var b=e.target.closest('button');
 if(b){stop();if(mode!=='hop')setMode('hop',+b.dataset.k);else go(+b.dataset.k);}});
rrail.addEventListener('click',function(e){var b=e.target.closest('button');
 if(b){stop();if(mode!=='rung')setMode('rung',+b.dataset.k);else go(+b.dataset.k);}});
if(crail)crail.addEventListener('click',function(e){var b=e.target.closest('button');
 if(b){stop();setMode('rung',+b.dataset.c);}});
document.addEventListener('keydown',function(e){
 if(e.key==='ArrowRight'){stop();go(+svg.getAttribute('data-frame')+1);}
 if(e.key==='ArrowLeft'){stop();go(+svg.getAttribute('data-frame')-1);}});

