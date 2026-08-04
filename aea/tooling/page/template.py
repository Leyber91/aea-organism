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


def document(*, MAXD,
             T,
             _svg,
             caps,
             cen,
             cert_alpha,
             cert_cross,
             cert_leaks,
             cert_letters,
             cert_per,
             cert_space,
             climb_html,
             coda,
             fn_n,
             frontier,
             growth,
             invariants,
             live_n,
             mx,
             n_rungs,
             org,
             overture,
             rail,
             rod_rows,
             rods,
             rrail,
             stamp,
             step_rows) -> str:
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE AEA - an autonomous entity, drawn from its own state</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/overture.css">
<link rel="stylesheet" href="assets/invariants.css">
<link rel="stylesheet" href="assets/frames.css">
<div class="wrap">
{overture}

<div class="hero"><div class="stage">
<div class="rails">
<p class="railhint">step through it &mdash; or use <kbd>&larr;</kbd> <kbd>&rarr;</kbd></p><div class="modes"><button id="m-hop" class="on">BY CALL HOP</button><button id="m-rung">BY RUNG</button></div>
<nav id="rail" aria-label="reveal the graph one call-hop at a time">{rail}</nav>
<nav id="rrail" hidden aria-label="reveal the graph one capability rung at a time">{rrail}</nav>
</div>
<div class="canvas">
<svg id="org" viewBox="0 0 1000 1000" data-mode="hop" data-frame="{MAXD}" role="img" aria-label="the live call graph of the entity, revealed by call depth">
{_svg(org, T)}
</svg>
<p id="cap" aria-live="polite" aria-atomic="true">{caps[MAXD]}</p>
</div></div>
<div class="legend">
<span><i style="background:#fff;box-shadow:0 0 0 2px var(--amber)"></i>the wake — where every
 tick begins</span>
<span><i style="background:var(--amber)"></i>reached in 1–2 calls</span>
<span><i style="background:var(--brass)"></i>reachable</span>
<span><i style="background:#0a0c0e;box-shadow:0 0 0 1.4px #6d757e"></i>{len(org['dispatched'])}
 reached only through a dispatch table</span>
<span><i style="background:#2b333b"></i>{len(org['human'])} a person can run, it cannot</span>
<span><i style="background:#1b1f24"></i>{len(org['dead']) - len(org['human'])} reached by nothing</span>
</div>
</div>

<h2>WHAT THE LOOP CAN TOUCH</h2>
<p class="deck">The picture above, as three numbers. This is the whole claim of the page in its smallest form.</p>
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
<p class="deck">Reachability says what the system CAN touch. This says what it can never touch &mdash; the only claim on this page backed by an adversary rather than by a count.</p>
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

<h2>WHAT IS WIRED, FUNCTION BY FUNCTION</h2>
<p class="deck">The climb above is about capability. This is the narrower question underneath it: for each declared step, can the running loop actually reach every function it names.</p>
{step_rows or '<p class="sub">no manifest</p>'}
<p class="src">A step is DONE only when every function in it has a caller reachable from an entry
point. Static reachability cannot see a function that runs and does nothing — that is what
<b>aea/lab/vital.py</b> measures, at runtime.</p>

<h2>THE FLEET — MEASURED, NOT ADVERTISED</h2>
<p class="deck">None of the above means anything if the models underneath were scored on an exam we bent. These are the ones that passed a census with no invented ceiling.</p>
{rod_rows or '<p class="sub">no census</p>'}
<p class="src">Scored on {mx} probes with no invented token ceiling. The 550B reads 12/12 here and
was recorded 7/12 under a 40-token budget — the exam was measuring our defaults, not the rod.</p>

<h2>THE LIVE SURFACE OVER TIME</h2>
<p class="deck">And the only honest way to read any of it: does the reachable surface actually grow, or does the story grow while the surface stays flat.</p>
<div class="growth">{growth or ''}</div>
<p class="src">state/assembly_history.jsonl — one row per run, appended.</p>

<h2>WHAT IT CHECKS ABOUT ITSELF</h2>
<p class="deck">Everything above reports what the system is. This reports how it is kept honest
&mdash; and the verdict is produced by a machine on a schedule rather than by a person remembering
to look. The finding underneath it was expensive: a detection that changes no number and fails no
command is indistinguishable from no detection.</p>
{invariants}

{coda}
<div class="honest">
<b>HONESTY TAG</b><br>
Generated {stamp}.<br>
Everything above is generated by <code>python -m aea.tooling.publish</code> from
<code>state/assembly.json</code>, <code>state/capability_census.json</code> and a live call-graph
walk. Nothing is typed by hand and nothing is simulated. What this page does <b>not</b> claim: that
a reachable function does useful work, that the entity is conscious, or that a rung is closed
because its wiring is. The ladder shows wiring; the proofs live in the repo.
<br><br>github.com/Leyber91
</div>
</div>
<script src="assets/captions.js"></script>
<script src="assets/instrument.js"></script>
<script src="assets/playback.js"></script>
"""
