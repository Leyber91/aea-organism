
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
