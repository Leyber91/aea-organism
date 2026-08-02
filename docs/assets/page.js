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
var CAPS=["HOP 0 \u2014 the entry bracket, which is not a function. The 5 real entry points the wake starts from arrive at hop 1.", "HOP 1 \u2014 5 functions arrive \u2014 5 of 160 reachable \u2014 first reach into aea.loop", "HOP 2 \u2014 39 functions arrive \u2014 44 of 160 reachable \u2014 first reach into aea.energy, aea.kernel, aea.mind, aea.server", "HOP 3 \u2014 50 functions arrive \u2014 94 of 160 reachable \u2014 first reach into aea.io, aea.memory", "HOP 4 \u2014 44 functions arrive \u2014 138 of 160 reachable \u2014 first reach into -", "HOP 5 \u2014 18 functions arrive \u2014 156 of 160 reachable \u2014 first reach into -", "HOP 6 \u2014 4 functions arrive \u2014 160 of 160 reachable \u2014 first reach into -"],RCAPS=["R0 THE LOOP SURVIVES \u2014 7 functions declared \u2014 7 of 33 the ladder names, 127 of 160 live functions declared by no rung.  Start with the least impressive claim available: that it is still here tomorrow. Everything above this is worthless without it.", "R1 THE DECISION IS READ \u2014 5 functions declared \u2014 12 of 33 the ladder names, 127 of 160 live functions declared by no rung.  There were two loops - one that thought and could not act, one that acted and could not think. This is the wire between them.", "R1.5 THE DECISION IS PARSED \u2014 3 functions declared \u2014 15 of 33 the ladder names, 127 of 160 live functions declared by no rung.  Between deciding and doing sits a translation, and it is where systems like this quietly break. This rung does only the translation, so a mishearing leaves a trace.", "R2 THE DECISION IS A TOOL CALL \u2014 8 functions declared \u2014 23 of 33 the ladder names, 127 of 160 live functions declared by no rung.  An intention is a sentence, and nothing executes a sentence. Here it becomes an instruction - and a wall goes up between what the system says and what it may hand to a tool.", "R3 THE OUTCOME IS REMEMBERED \u2014 8 functions declared \u2014 31 of 33 the ladder names, 127 of 160 live functions declared by no rung.  Until now it remembered what it MEANT to do. Improvement is the gap between that and what happened, so this is the first rung where the word learning is defensible.", "R4a PERCEPTION IS A CHOICE \u2014 2 functions declared \u2014 33 of 33 the ladder names, 127 of 160 live functions declared by no rung. 1 declared function on this rung is not reachable from the wake: kernel.perceive:verdict.  Fixed inputs are not perception. Here what it examines becomes something it chose - and choosing is not the same as rotating, which is why the record keeps the reason.", "R4b PERCEPTION REACHES THE WORLD \u2014 nothing in the live graph belongs to this rung. Waiting on dispatch running dry, then a reconvened council. The organism stops growing here: 33 of 160 functions are declared by any rung, and every one of them was added below this line. 8 functions for this rung already exist and nothing calls them (aea.kernel.dispatch, held: written, zero callers) \u2014 lit in brass out in the field, because they are written and have never run.  The fork. Let it choose what to look at and the query itself becomes a way out of the machine. A council refused this three times. It waits, and the waiting is the design.", "R5 RESEARCH \u2014 nothing in the live graph belongs to this rung. Waiting on R4 (egress) and R3 (storing what came back). The organism stops growing here: 33 of 160 functions are declared by any rung, and every one of them was added below this line.  A summary cannot be wrong, which is exactly why it cannot be useful. The test of this rung is not what it finds - it is whether it ever admits being wrong.", "R6 REFLECTION \u2014 nothing in the live graph belongs to this rung. Waiting on R5 (material worth linking). The organism stops growing here: 33 of 160 functions are declared by any rung, and every one of them was added below this line.  Storage and recall already work. This is where something notices what several memories mean together, and must keep a thread back to what produced it.", "R7 THE COUNCIL ON ITS OWN PLANS \u2014 nothing in the live graph belongs to this rung. Waiting on R3 through R6 running with a track record. The organism stops growing here: 33 of 160 functions are declared by any rung, and every one of them was added below this line.  The easiest thing on this ladder to fake, because a review that always approves looks exactly like a review that was never needed.", "R8 THE DRIVE \u2014 nothing in the live graph belongs to this rung. Waiting on an unsolved research problem, not code. The organism stops growing here: 33 of 160 functions are declared by any rung, and every one of them was added below this line.  Wanting is not a feature you add; it is a target you can be tricked by. This stays shut, and it stays shut because nobody has solved it - not this project, not the literature.", "R9 SELF-MODIFICATION \u2014 nothing in the live graph belongs to this rung. Waiting on every rung below it, and a statable hazard. The organism stops growing here: 33 of 160 functions are declared by any rung, and every one of them was added below this line.  Named here so that nobody arrives at it by accident. Listed as closed rather than omitted, because a ladder that stops before its last rung invites the wrong assumption."],MAXD=6,RMAX=RCAPS.length-1,RREST=6;
var svg=document.getElementById('org'),cap=document.getElementById('cap'),
    rail=document.getElementById('rail'),rrail=document.getElementById('rrail'),
    mh=document.getElementById('m-hop'),mr=document.getElementById('m-rung'),
    climb=document.getElementById('climb'),crail=document.getElementById('crail'),
    mode='hop',timer=null;
function stop(){if(timer){clearInterval(timer);timer=null;}}
function go(k){var max=mode==='hop'?MAXD:RMAX,r=mode==='hop'?rail:rrail;
 k=Math.max(0,Math.min(max,k));
 svg.setAttribute('data-frame',k);svg.setAttribute('data-mode',mode);
 cap.textContent=(mode==='hop'?CAPS:RCAPS)[k];
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

/* THE AUTOPLAY IS OWNED BY THE SECTION IT ILLUSTRATES, AND IT WAITS TO BE LOOKED AT.
   It used to run on load, which meant the first thing a visitor saw was the climb's frame 0 - a
   dark field with eight lit dots - instead of the organism, on a hero whose whole argument is the
   ratio of lit to dark landing before a word is read. It plays once, when THE CLIMB is actually on
   screen, and any touch on any control ends it for good: a reader who has taken over is not fought.
   Under prefers-reduced-motion it never runs and every rung stays readable without it. */
var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function play(){if(timer)return;var k=0;setMode('rung',0);
 timer=setInterval(function(){k++;if(k>RREST){stop();go(RREST);return;}go(k);},560);}
var h=location.hash.match(/(hop|rung)-(\d+)/);
if(h){setMode(h[1],+h[2]);}
else{setMode('hop');
  if(!rm&&climb&&window.IntersectionObserver){
    var io=new IntersectionObserver(function(es){
      if(es[0].isIntersecting){io.disconnect();play();}},{threshold:.25});
    io.observe(climb);}}
