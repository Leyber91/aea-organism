# THE PAGE SPEC - eleven rungs, drawn mostly dark

Produced 2026-08-01 by a 15-agent panel: four ground readers, three research agents (narrative
visualization, science-communication method, implementation craft), three competing architectures,
four judge lenses, one synthesis. The honesty audit returned REJECT AS SCOPED against the page as
originally framed, and its objections are folded in here rather than argued with.

## THESIS

A ladder of eleven rungs, drawn mostly dark, where the only thing that is ever amber is a single closing condition that a named command re-measured true during this build - so the trail the reader watches accumulate is not a story about progress, it is the count of proofs that survived being re-run, and where a rung's own manifest says it passed and the underlying file says it did not, the page prints the contradiction and names the instrument it trusts.

## HONESTY RULES

- AMBER HAS EXACTLY ONE MEANING: a closing condition that a named command re-measured true during THIS build. Not a rung, not a status, not a highlight, not a hover state. This single predicate satisfies the two-ink law and the honesty law with the same rule, and it is why the accumulating trail is not decoration - the amber accumulates because proofs accumulate.
- NO STATUS FIELD FROM ANY INPUT FILE MAY REACH THE PAGE. status is derived at build from the condition cells. Measured cause: state/ladder.json currently carries met:true on R0 (rests on a 246.89 h figure spanning a 199.96 h gap), on R1 (under a gate the same file labels MIS-SPECIFIED), and on R3 (a bound reported PASS over bound_pairs 0). Three of four measured rungs are unsound as authored.
- A VACUOUS PASS IS NOT A PASS. Any check whose denominator is zero forces NO_INSTRUMENT, enforced in the emitter rather than judged per build. A rule that never met a case it could break on has not been tested.
- THE DASH IS A TYPED GLYPH WITH A CAPTION, NEVER A BLANK AND NEVER A ZERO. A blank reads as an oversight and a zero reads as a measurement. Every dash names the instrument that would have to exist to fill it.
- A ZERO IS PRINTED AT FULL SIZE. R2's 0 of 20, 0 of 3, 0 of 8 is set in the same type as any amber figure. A measured zero is evidence and is never shrunk, greyed below legibility, or moved below the fold.
- TWO INSTRUMENTS THAT DISAGREE BOTH REACH THE PAGE, AND THE PAGE SAYS WHICH ONE IT TRUSTS AND WHY. It does not average them and it does not launder the disagreement as a methodological difference. R0 prints 46.9 h, prints 246.89 h struck through, and prints the 199.96 h gap that decides between them.
- NO NUMBER IS EVER TYPED INTO COPY. Every figure is substituted by the generator from the ladder JSON. Prose is templated around substitution points. Measured reason: heartbeat boot_count and total_ticks changed between two reads seconds apart during this spec work.
- A CERTIFIED FIGURE MUST BE READ FROM A STAMPED FILE OR IT IS A DASH. The 0.6 per cent containment bound stays a dash until the build runs the command, writes state/redteam_cert.json, and the certificate's HEAD stamp matches the publishing HEAD. Verified: that file does not exist. A hand-typed figure on a page claiming nothing is hand-typed refutes the page in order to decorate it.
- EVERY RUNG CARRIES TWO READOUTS THAT ARE NEVER MERGED. WIRING is static reachability. FIRING is what ran. R2 is 6 of 6 wired and 0 of 20 fired; collapsing those into one light would destroy both the only finished half and the only honest failure.
- CARRY EXCLUDES ENTRY POINTS FROM THE REMOVAL SET. Measured: R0's naive load is 77 and its entry-held load is 4; R1 goes 10 to 3; R3.4 goes 28 to 1. Deleting a root does not measure dependency, it decapitates the search. Only the entry-held figure is published, and the naive one is printed once as a retraction.
- EVERY RUNG CARRIES A REQUIRED what_this_is_not FIELD AND THE BUILD FAILS WITHOUT IT. The claim ceiling is enforced structurally, not by remembering to be careful.
- THE RUBBER-BAND TEST RUNS AS A LINT PASS OVER EVERY LINE OF COPY. Any word whose explanation requires the mechanism it was standing in for is replaced by the mechanism. Killed by name: 'something it would rather do', 'doing something on its own', 'the thinking half', 'one loop thought and could not act', 'deliberation stopped being decoration'. Kept, because each is defined in the closing section against a readable mechanism: chose, remembered, decided not to repeat.
- EVERY CLAIM IS LEGIBLE AT REST, ON ARRIVAL, WITH NO INTERACTION AND NO ANIMATION. Interaction may only go deeper. Median interaction with detail controls is measured at zero across large samples, so a proof behind a click is an unproven assertion for most readers.
- THE TRAIL MAY FALL. Zero-commit days are drawn as empty columns, and the body series plots its recorded 126-to-125 drop unsmoothed at the same weight as its rises.
- PATHS ARE REPO-RELATIVE, ALWAYS. Absolute filesystem paths, employer or client names, emails, keys and personal identifiers never reach the page. Any prose pulled from diary or state files is routed through the UNION of the two existing guards (publish.py FORBIDDEN and _pubscan.py), not a third one, and crystal.json's verbatim print is scanned before it is set in type.
- THE BUILD IS DETERMINISTIC EXCEPT FOR ONE STAMP. Position and order derive from hashlib.sha1 or a sorted sequence, never from hash(), never from set-iteration order, never from wall clock beyond the single generated field. Two builds of identical state differ on one line.
- THE PAGE MAKES ZERO NETWORK REQUESTS. No font link, no script src, no image, no fetch. Everything inlines.
- THE PAGE PRINTS THE COMMIT IT WAS BUILT FROM AND INVITES RE-RUNNING. If the same commands against the same commit produce a different page, the page was wrong and the commands are still right.

## GROWTH MECHANIC

WHAT ACCUMULATES: reachable functions and met conditions. Nothing else ever accumulates, and nothing on the page grows by being written - only by becoming reachable or by passing a probe.

STATE 0, ON LOAD. The full geometry for all eleven rung-states is built ONCE as inert DOM: 1,565 function marks plus the eleven rail segments, every future element present at opacity 0 with pointer-events none. Visible on arrival: the dim field, the 165-node live body in structure grey, the six ringed entry points, and eleven empty rail outlines. Nothing is amber. The first impression is a nearly dark diagram, which is the honest one. A Map from node id to DOM element is built here and never rebuilt - elements are created once and thereafter only have transform and opacity changed, so a node the reader is tracking is never removed and re-appended. transform-box:fill-box is set globally on the first frame; without it every transform-origin resolves against the viewBox and marks fly.

ADVANCE, ONE RUNG PER DELIBERATE INTERACTION (rail click, arrow key, or the single NEXT control - never scroll-driven). Two stages, roughly one second each, cubic-bezier ease-in-out, and never a third.
  STAGE 1 (0 to ~1.0s): only pre-existing marks translate to make room. The incoming rung's marks stay at opacity 0. The reader tracks motion with no novelty competing for it.
  STAGE 2 (~1.0 to ~2.0s): every previously-present mark holds perfectly still. The new rung's functions fade in AT their final coordinates, its rail segment fills to its met fraction, and its condition cells resolve left to right.
The move and the add are never in the same stage. That single rule is what keeps a reader from losing a node they were already following, and it is why there is no stage where edges draw themselves along their paths - that third stage is the one that measures worse and reads as a screensaver.

WHAT PERSISTS. A rung the reader has passed keeps all of it: its functions stay in the body at full structure grey with a permanent 1px outline ring, and its MET condition cells stay amber permanently. It never shrinks, never fades below full opacity, never leaves.

WHAT RECEDES. Exactly one thing: the bright outline on the rung currently under the lesson. When the reader advances, the previous rung's outline drops from amber to structure grey. Its size, its position, its membership in the body and its amber cells are untouched. This is the whole of "past additions remain visible but recede" - recession is a single state change on a single stroke, not an opacity ramp, because an opacity ramp on accumulated work says the work faded.

WHAT IS PENDING. Future rungs are drawn, never hidden: empty rail outline, and their condition cells rendered as hollow dashed cells from the first frame. A reader can see the whole shape of the ladder at State 0 and watch it fill. The unbuilt six are the longest amber-free stretch on the page and that emptiness is content.

THE TRAIL AS THE READER SEES IT: a rail whose fill only ever rises, because it counts met conditions and a met condition is one a command re-measured true this build. So the amber accumulates because proofs accumulate. That is the cumulative single path rendered rather than asserted, and it satisfies the two-ink law by the same rule that makes it honest - amber is fired state, a met condition is fired state, and nothing else is ever amber.

REGRESSION IS ALLOWED TO SHOW. The rail fill rises within one build because conditions are ordered by rung, but ACROSS builds a rung can lose amber, and the body series panel plots the recorded drop (115, 126, 125, 131) unsmoothed at the same visual weight as its rises. The page must be able to get worse between publishes or it is not measuring anything.

REDUCED MOTION. prefers-reduced-motion:reduce sets both stages to 0ms; advancing becomes an instant state swap. Every number, every cell state and every caption is identical. Nothing on this page is delivered only by motion, and the full argument is legible with animation entirely disabled.

MOBILE. The rail runs vertically at the top instead of horizontally; the graph keeps its 1000x1000 viewBox and scales; condition cells stack one per row rather than in a strip. The interaction is a tap on the rail segment or the NEXT control - both large targets on the diagram itself rather than inline text links. No behaviour is keyboard-only and no behaviour is hover-only.

## LADDER DATA MODEL

FILE: state/ladder.json, schema 2, emitted by `python -m aea.tooling.ladder --json`. publish.py becomes a pure reader of it and computes nothing about rungs itself. THE GOVERNING RULE: every field is measured from a real artefact at build or it is null, and null renders as a dash. There is no default, no estimate, no carried-forward value.

TOP LEVEL
- schema: int, 2. Bump on any breaking field change; publish.py refuses to render a schema it does not know rather than rendering a partial page.
- generated: str, "YYYY-MM-DD HH:MM:SS UTC". The ONLY wall-clock field in the document. Everything else is derived from artefacts.
- head: str, git short sha at build. Used to validate stamped certificates.
- head_full: str, full sha, so a reader can resolve it unambiguously.
- commits: int, git rev-list --count HEAD.
- dirty: bool, whether the working tree had uncommitted changes at build. A page built from a dirty tree cannot be reproduced by checking out head, and the reader is told.
- gates: object of the thresholds, read from constants in ladder.py and never duplicated in prose: {r0_hours: 72.0, r2_reach: [20,3,8], r1_5_ticks: 50, stale_limit_s: 5400}.
- body: object, the live structural measurement. {modules: int, functions_defined: int, functions_live: int, functions_dead: int, unresolved_calls: int, entries: {wake: [str], server: [str]}, measured_at: str}. Measured 2026-08-01: 160 / 1565 / 165 / 1400 / 226.
- totals: object, counted over all emitted cells, never authored: {rungs: int, conditions: int, with_instrument: int, met: int, not_met: int, no_instrument: int, mis_specified: int}.
- rungs: array of rung objects, in ladder order.
- retractions: array of retraction objects.
- trail: object.

RUNG OBJECT - eleven entries: R0, R1, R1.5, R2, R3, R4, R5, R6, R7, R8, R9.
- id: str, the canonical name including the half step ("R1.5"). This is the identity used everywhere, including the URL fragment.
- ord: int, 0-based ladder position. Used for ordering ONLY. Never used as an identity, never written into a URL.
- half_step: bool. True for R1.5. Renders the thinner frame and half-height rail segment.
- slug: str, id lowercased with the dot replaced ("r1-5"). The URL fragment. Deep links become #r1-5, not #rung-3, so inserting a rung never repoints an existing bookmark.
- title, power, bound, plain, why_first: str. Authored prose, held in ladder.py's RUNGS table, physically separated from measurement so a number can never be written into a sentence by hand.
- what_this_is_not: str. REQUIRED and non-empty. The generator raises and the build fails if any rung lacks it. This is the claim-ceiling enforcement, made structural rather than habitual.
- blocked_on: str or null. Computed from the dependency relation between rungs, not authored, for every rung whose status is future.
- status: str, one of "proven" | "partial" | "open" | "future". DERIVED, never read from any input file. The derivation, in order: future if the rung has no probes at all and measured is empty; open if it has probes and met == 0; proven if not_met == 0 AND no_instrument == 0 AND met > 0 (mis_specified cells with a MET replacement clause do not block proven); partial otherwise. The old `met` boolean in schema 1 is not carried forward in any form.
- functions: array of "module:function" strings this rung declares. R0, R1 and R1.5 get real lists - all twelve proposed names verified reachable at spec time - so no rung ever has an empty list. The generator raises on an empty list, because an empty list computes as done-over-nothing.
- functions_live / functions_dead: arrays, the split computed by assembly.reachable() at build.
- wiring: object, the static readout. {declared: int, live: int, state: "DONE"|"PARTIAL"|"NOT_STARTED", caption: str}. The caption is carried verbatim from the current page: a step is DONE only when every function in it has a caller reachable from an entry point, and static reachability cannot see a function that runs and does nothing.
- carry: object, the removal test. {value: int or null, functions_removed: int, entries_held: [str], method: str, note: str}. THE ENTRY-HOLD RULE IS MANDATORY: entry-point functions are excluded from the removal set, because deleting a root does not measure what rests on a rung, it decapitates the search. Measured both ways at spec time: naive R0 = 77, entry-held R0 = 4; naive R1 = 10, entry-held R1 = 3; naive R3.4 = 28, entry-held R3.4 = 1. R2 = 11, R3.1 = 12, R3.2 = 12, R3.3 = 11 (no entries in those sets, so both methods agree). Only the entry-held value is ever published. value is null when the rung has no row in the removal manifest, and note then states that structural reason.
- firing: object, the runtime readout, held at equal weight to wiring and NEVER merged with it. Shape is per-rung and always includes {probe: str, value: number|string|null, gate: number|array|null, met: bool|null}.
- conditions: array of condition cells. This is the unit of the page.
- counts: object over this rung's cells: {total, met, not_met, no_instrument, mis_specified}.
- rail_fill: float 0..1, met / total. The rail segment's fill. Never binary, never "DONE".
- arrived: object or null. {date, sha, subject, functions_added: int}. The dated point on the trail where this rung's functions first became reachable, resolved from git. null where it cannot be determined - never guessed.

CONDITION CELL - the most important object in the document.
- id: str, stable and unique ("r0.uptime_72h"). Stability matters because a reader may link to a single cell.
- clause: str, the requirement in plain words, short enough to read in one pass.
- probe: object. {kind: "file"|"command"|"scan"|"none", target: str (repo-relative path or module, NEVER absolute), predicate: str (the test in words), command: str or null (the exact command a reader can run)}. kind "none" is what produces NO_INSTRUMENT.
- state: str, one of MET | NOT_MET | NO_INSTRUMENT | MIS_SPECIFIED. The only four values.
- value: number or string or null. null forces the display dash.
- unit: str or null ("h", "invocations", "%", "s").
- threshold: number or array or null, the gate this value is tested against.
- display: str, the pre-rendered figure the page prints, or "-" - computed by the emitter so the page never formats a number and never has an opportunity to round one.
- measured_at: str, UTC of this specific probe. Per-cell rather than per-document, because probes run at different instants and one of them was observed changing between two reads seconds apart.
- note: str or null. For NO_INSTRUMENT it must name what would have to be built. For MIS_SPECIFIED it must state why the clause is unsatisfiable by construction.
- replacement_clause: str or null. Only on MIS_SPECIFIED cells: the reachable version of the requirement, which then gets its own cell.
- vacuous: bool. True when the underlying check passed over zero qualifying cases. HARD RULE IN THE EMITTER: vacuous true forces state NO_INSTRUMENT regardless of what the source said. This is what stops R3's bound rendering as a pass over zero pairs, and it is enforced in code rather than decided per build.
- disagreement: object or null. {other_value, other_probe, other_source, why_rejected}. Present when two instruments answer the same clause differently. Both figures reach the page; the rejected one is struck through and the reason is printed. This is the field that carries R0's 46.9 against 246.89 and the 199.96-hour gap that decides between them.
- forced: int or null. Count of receipts within this value that were driven by a test harness rather than arising unattended, so the honest unforced count is always derivable. This is what keeps R1's "two differed" from overstating and what caught R2's eleven.

RETRACTION OBJECT
- id, date, sha (validated against git at build; the emitter raises if it does not resolve), withdrawn (str, the figure as published), replacement (str), error_class (str, e.g. "wrong denominator", "harness mistaken for production", "measured across a gap", "vacuous pass", "written from intent not from the line"), found_by (str), recorded_in (repo-relative path), one_line (str, the sentence the page prints).

TRAIL OBJECT
- method: str, the exact harvest and classification procedure, printed in the page's method note so the classification is auditable rather than asserted.
- days: array of {date, commits, events, kinds: {capability, instrument, proof, correction, infrastructure}, rungs: [str]}. Every calendar day between first and last is present, including zero days, so the strip cannot compress an idle week into a slope.
- events: array of {sha, date, subject, kind, rungs: [str], new_capability: [str], new_instrument: [str], corrective: bool}. kind and corrective are stored separately so a commit that both landed and repaired keeps both facts.
- body_series: array of {at, live, delta} read from state/assembly_history.jsonl, unsmoothed, dips preserved. Measured: 115, 126, 125, 131.
- counts: object, totals by kind and by rung, computed.

WHAT THE MODEL DELIBERATELY DOES NOT HAVE: no `met` boolean at rung level, no `status` field that any input file can set, no percentage complete, no score, no estimated completion, no field whose value is carried forward from a previous build when today's probe fails. A probe that cannot run produces a dash today even if it produced a number yesterday.

## BUILD ORDER

1. STEP 1 - LADDER SCHEMA 2, EMITTER ONLY, NO PAGE CHANGES. Rewrite aea/tooling/ladder.py to emit the condition-cell model: eleven rungs, per-cell probes, the four states, the vacuous-forces-NO_INSTRUMENT rule, derived status, and required what_this_is_not. VERIFY: `python -m aea.tooling.ladder --json` writes state/ladder.json with schema 2; assert totals.conditions > 0, assert no rung has an empty functions list, assert every rung has a non-empty what_this_is_not, assert R3's bound cell has state NO_INSTRUMENT with vacuous true, assert R0's uptime cell has state NOT_MET with value 46.9-ish and a populated disagreement object. Independently checkable by reading the JSON alone - the page does not exist yet.
2. STEP 2 - R0, R1, R1.5 ENTER assembly.STEPS WITH REAL FUNCTION LISTS, AND THE EMPTY-LIST TRAP IS CLOSED AT SOURCE. Add the three rows using the twelve verified function names, and change assembly's state computation so len(need)==0 yields NOT_STARTED rather than DONE. VERIFY: `python -m aea.tooling.assembly` prints eight rows starting at R0 with no row reporting DONE 0/0; `python -m aea.lab.vital` still runs. Assert in a test that no STEPS row has an empty list.
3. STEP 3 - CARRY WITH THE ENTRY-HOLD RULE, AS A FUNCTION IN assembly.py. carry(fns) removes only non-entry functions and returns the collapse plus the held entries. VERIFY: assert carry(R0) == 4 and the naive removal == 77, so the correction is pinned by a test rather than by a comment. Assert carry equals the naive value for every rung containing no entry point (R2, R3.1, R3.2, R3.3), which is the control that proves the rule only changes what it should.
4. STEP 4 - THE REDTEAM CERTIFICATE. Make `python -m aea.lab.redteam` write state/redteam_cert.json with payloads, crossings, refusals, canary hits, the one-sided bound, and the HEAD sha. VERIFY: run it, confirm the file exists and its head matches `git rev-parse --short HEAD`; then check out a different commit and confirm the ladder emitter renders R2's bound cell as a dash on stamp mismatch. The negative case is the one worth testing.
5. STEP 5 - THE TRAIL EMITTER. Promote the reference harvest script to aea/tooling/trail.py emitting the days / events / body_series structure, with the rung map read off the live STEPS manifest and zero-commit days materialised. VERIFY: counts match a direct `git rev-list --count HEAD` (195 at spec time); every date between first and last is present in days; body_series contains the 126-to-125 drop.
6. STEP 6 - PUBLISH BECOMES A PURE READER, AND THE FRAGMENT SCHEME CHANGES. Rename the shadowed second `hist` binding in publish.py before touching anything else. Wire the rung rail and the frame to ladder.json's rungs array; change the URL fragment from positional #rung-N to #<slug> with a redirect for the old numeric forms. VERIFY: build twice in one process and diff - exactly one line differs, the UTC stamp. Load #rung-2 and confirm it redirects rather than landing on a renumbered rung.
7. STEP 7 - THE TWELVE PANELS, STATIC FIRST, NO ANIMATION AT ALL. Render every section at rest with the full condition strips, both readouts, CARRY, the retraction block, the trail strip and the verbatim crystal print. VERIFY: screenshot headless with software GL, read the PNG, confirm every claim is legible with zero motion and that the page makes no network requests (assert the rendered HTML contains no src= or href= to any host). This is the state the page must be shippable in before a single transition is written.
8. STEP 8 - THE TWO-STAGE ADVANCE. Build the full geometry once as inert DOM, stable id-to-element Map, transform-box:fill-box global, stage 1 moves only, stage 2 adds only, ~1s each, no third stage. VERIFY: a build-time orthogonal-ordering assertion across all consecutive layout pairs - for every node present in both, x_A < x_B before implies x_A < x_B after, same for y - fails the build on violation. Then screenshot mid-transition and confirm no new element is visible during stage 1.
9. STEP 9 - REDUCED MOTION AND MOBILE. Set both stages to 0ms under prefers-reduced-motion; vertical rail and stacked cells under the mobile breakpoint. VERIFY: screenshot at 390px wide and with reduced motion forced, read both PNGs, confirm identical numbers and no horizontal scroll. Mobile already works today and this step is a regression gate, not a feature.
10. STEP 10 - THE PREDICTION BEAT, EXACTLY ONE. At the end of the R1 panel, one control asks how many times the wake's decision has actually run a tool, with four ranges. R2's panel prints 0 at rest regardless of whether the reader answered; the guess, if given, is shown beside it. VERIFY: load R2 directly by fragment without touching the control and confirm the zero and its caption are fully present. If the panel reads correctly with the widget removed entirely, the beat is safe to keep.
11. STEP 11 - THE GUARD PASS AND PUBLISH. Route every string that originates from a diary or state file through the union of publish.py FORBIDDEN and _pubscan.py patterns, including the verbatim crystal print. VERIFY: run the union scanner over the rendered HTML and assert zero hits; grep the output for absolute paths and for any emoji codepoint; then publish and diff docs/index.html, expecting dead-field churn and ignoring it as known noise.

## REFUSED (deliberately, with reasons)

- REFUSED: 246.89 hours as R0's uptime, and every sentence claiming the 72-hour gate is met. I measured the claimed window myself: it contains a single gap of 199.96 hours, from 2026-07-21 19:31:54Z to 2026-07-30 03:29:46Z, while every other gap inside it is under three hours. The real longest continuous run is 46.9 h and it is stable at 1 h, 2 h and 3 h gap tolerance, which is what makes it publishable. Design A did not merely print the wrong number - it anticipated the conflict and framed the two figures as 'answers to different questions'. That framing is worse than the number, because it inoculates the reader against the correction.
- REFUSED: state/ladder.json's own met and status fields as display state, anywhere. Three of the four measured rungs carry met:true unsoundly - R0 on the artefact above, R1 under a gate the same file labels MIS-SPECIFIED, R3 with bound PASS over bound_pairs 0. Status is derived from cells at build or it is not shown. This is the single architectural decision the whole synthesis rests on.
- REFUSED: LOAD as design B specified it, and this is where I overrode a judge who wanted it grafted as-is. I ran the removal test and got R0 = 77, then ran it again holding entry points and got 4. R0's function list contains two of the five wake entry points, so 'load 77' measures what happens when you delete the graph's roots, not what rests on the rung. R1 goes 10 to 3, R3.4 goes 28 to 1. The instrument is salvageable and I kept it, renamed CARRY, with the entry-hold rule mandatory and a test pinning 77-to-4 - but the uncorrected version is a fabricated number and had to die. The honest values are small, which is itself the finding: the rungs are wired to each other and almost nothing else rests on them yet.
- REFUSED: printing the 0.6 per cent containment bound. I verified state/redteam_cert.json does not exist; the figure lives as terminal output and prose. It is the best number this project has and it stays a dash until the build generates a HEAD-stamped certificate. Publishing it by hand would refute the page's central claim in exchange for its most flattering statistic.
- REFUSED: the ten-rung framing in the brief. The repo's ladder has eleven - R1.5 was added by an adversarial review and never removed, and HEAD's own commit subject is 'ladder: eleven rungs, not ten'. The data model carries eleven and R1.5 is drawn as a visibly half-height step. Renumbering it to a whole number to make the ladder tidy would break every reference written before the renumbering, which is exactly the failure the rung itself was created to catch.
- REFUSED: any assembly.STEPS row with an empty function list. assembly.py computes DONE as got == len(rows), so need=[] publishes as DONE 0/0 in amber - the precise trap a naive rung-rail extension walks into, and an honesty violation rather than a cosmetic one. Fixed at source with a NOT_STARTED state, plus real function lists for R0, R1 and R1.5. I verified all twelve proposed names are in the live reachable set before committing to them.
- REFUSED: scrollytelling. Discrete panels advanced deliberately measured better for comprehension against vertical scroll, and the engagement difference between stepper and scroller did not reach significance. There is no measured reason to take the comprehension loss.
- REFUSED: a third animation stage - edges drawing themselves along their paths. The staging result that justifies two stages is the same result whose multi-stage extremes increased error and were the only conditions not preferred. Two stages, roughly a second each.
- REFUSED: any claim delivered only by interaction. Median interaction with detail controls is measured at zero across very large samples. Every number, cell, retraction and caption renders at rest on arrival; the single prediction beat is built so that removing the widget entirely leaves the panel correct.
- REFUSED: every anthropomorphic verb that fails the rubber-band test. Killed by name from the source designs: 'something it would rather do' (attributes preference), 'doing something on its own', 'the thinking half', 'one loop thought and could not act', 'the moment deliberation stopped being decoration'. Where chose, remembered and decided-not-to-repeat survive, each is defined against a readable mechanism in the closing section, and a required per-rung what_this_is_not field fails the build if that discipline lapses.
- REFUSED: positional deep links. data-r is currently a positional index into STEPS, so inserting R0 and R1 at the front silently repoints every existing #rung-N bookmark at a different rung. Fragments become rung slugs with a redirect for the old form.
- REFUSED: a monotonic trail. state/assembly_history.jsonl records live going 115, 126, 125, 131 - the drop is real and is drawn at the same weight as the rises, and zero-commit days are drawn as empty columns rather than compressed away.
- REFUSED: R3 rendered as proven, and any vacuous pass mapped to MET. The bound passed over zero qualifying pairs and renders NO_INSTRUMENT, enforced as a hard rule in the emitter rather than as a judgement made per build. The empty forty-byte crystal store is printed verbatim beside its 4-of-4 wired badge.
- REFUSED: attaching narrative payload to the dead field. It is roughly 1,400 marks and about eight times the per-node cost of the live tree; a 200-character payload per dead node would add hundreds of kilobytes to a page that must stay zero-request and fast on mobile. Narrative attaches to the 165 live nodes and to the eleven rung frames only.
- REFUSED: caching any figure across builds. During this spec, heartbeat boot_count moved 15 to 17 and total_ticks 141 to 146 between two commands seconds apart, and decide.choose() returned a fresh 65-second decision where an earlier day returned six figures of staleness. A probe that cannot run today produces a dash today, even if it produced a number yesterday.
- REFUSED: writing a third privacy guard. Two divergent ones already exist and neither is authoritative; prose pulled from diary or state files routes through the union of both, which is also the reason the verbatim crystal print is safe to set in type.

## SECTIONS

### s1-floor - THE FLOOR

**SHOWS** Full-bleed void, no data mark anywhere on the screen - the only such screen on the page. Four short paragraphs of structure grey at 34em. One hairline amber rule. Beneath it, a single monospace line naming the artefacts this build read and the UTC instant it read them, with the git HEAD short hash. Nothing animates.

**DATA** No measurement. Static copy, plus the build header: time.strftime UTC at publish (the single wall-clock value on the page, publish.py:430), git rev-parse --short HEAD, git rev-list --count HEAD (195 at time of spec), and the read-manifest of the eight artefacts: state/ladder.json, live assembly.scan() + assembly.reachable(), state/heartbeat.json, state/events.jsonl, state/hands_ledger.jsonl, state/outcomes.jsonl, state/crystal.json, state/trust_ledger.json, state/assembly_history.jsonl, state/capability_census.json, state/redteam_cert.json (absent), and git log for the trail.

**PROSE**

Three things are taken as given here, and everything after them is built from these three and nothing else.

A function is a named block of code. A call is one function naming another. A program is running when a process on some machine is executing it.

That is the whole floor. Nothing below asks you to accept anything beyond it - no claim about understanding, none about awareness, none about intent. Where the evidence stops, this page stops, and what you will see there is a dash.

Every number here was computed when this page was built, by running a command against the files this process wrote about itself. The sentences around the numbers were written by a person. Where a command could not answer, there is a dash, and beside the dash is the name of the instrument that does not exist yet. A dash is not an omission. It is the most precise thing that could honestly be printed in that space.

### s2-body - THE BODY

**SHOWS** The radial call graph takes the centre of the viewport and never leaves it for the rest of the page. Measured live at build: 1,565 defined functions in 160 modules, of which 165 sit at full structure grey and 1,400 are dim, sectored by package so the lit-to-dark ratio is readable per package. Six functions carry a thin ring - the entry points. A ring caption carries the three counts and the unresolved-call count. Nothing is amber yet. Nothing animates.

**DATA** aea.tooling.assembly.scan() and assembly.reachable(), both called live at build time. Measured 2026-08-01: 160 modules, 1,565 defined functions, 165 reachable, 226 unresolved calls. assembly.ENTRIES gives 5 wake entries + 1 server entry. These figures move between builds and are never written into copy - the generator substitutes them and the sentence is templated around the substitution.

**PROSE**

Here is the whole body, read from the source when this page was built.

Every dot is one function. There are 1,565 of them across 160 modules. Six carry a ring: those are the places a running process actually starts - five in the loop, one in the server.

165 dots are at full brightness. Those are the functions something can reach by following real calls out from one of those six starts. The other 1,400 exist and import cleanly and are never reached by anything that runs. They are the workbench: experiments, probes, one-off measuring tools, and the instrument that produced this page. They were written in order to build the body. They are not the body.

One in ten. That ratio is the honest shape of this work, and it is the first number you should distrust in the project's favour, because it is generous in two directions at once. Reading the source cannot tell you that a function which is reachable ever does anything useful once it is reached - only that a path exists. And 226 calls in this tree resolve to something the reader cannot name, a method on a value whose type it cannot infer, and every one of those is dropped rather than guessed. So some real edges are missing from the picture you are looking at, and some of the edges you can see lead to functions that run and accomplish nothing.

That is the instrument, stated with both of its errors. Now the climb.

### s3-unit - THE UNIT

**SHOWS** The four cell states defined once, at large size, as four real cells taken from the ladder rather than as an abstract legend. Then a worked example: R0's four conditions resolve left to right, one landing amber, one landing grey with a number, one landing hollow with a dash. This grammar is reused unchanged for every rung below and is never redesigned.

**DATA** The four states are computed by the generator per condition. N and K are counts over the emitted cells - totals.conditions and totals.with_instrument in the ladder JSON - so adding a probe moves the headline without anyone editing this paragraph. The worked example reads R0's condition array.

**PROSE**

Every rung on this page is priced in one unit, and the unit is the CLOSING CONDITION.

A rung is a claim about what the system can now do. A closing condition is one clause of that claim, small enough that a single command can decide it. Every rung here is broken into its conditions, and every condition carries three things: the clause in plain words, the probe that decides it - a named command, or a file plus a test - and the result of running that probe during this build.

A condition lands in one of exactly four states, and the four states are the whole vocabulary of this page.

MET. A command ran during this build and returned true. This is the only thing on this page that is ever amber.

NOT MET. A command ran and returned false, or returned a number short of the threshold. The number is printed at the same size an amber number would be. A zero here is a measurement, and it is worth more than an absence.

NO INSTRUMENT. No probe exists for this clause. The cell prints a dash and names what would have to be built to fill it. This includes the case where a test passed over nothing - a rule that has never met a case it could break on has not been tested, and it is filed here rather than counted as a pass.

MIS-SPECIFIED. The clause cannot be satisfied by construction - not hard, not unfinished, but impossible as written. This state exists because measuring this ladder found one. A rung whose gate cannot be met by construction reads identically to a rung nobody got round to, and those are not the same failure.

Across the whole ladder, this build resolved a total of N closing conditions, of which K have a probe at all. The rest are dashes. Both of those numbers are counted from the cells, not typed.

### s4-r0 - R0 - THE LOOP SURVIVES

**SHOWS** The fixed rung frame, used unchanged for all eleven rungs. Centre: the graph, with R0's six functions going amber and holding. Left: the rung's power and bound at equal weight. Right: two readouts at equal size, WIRING and FIRING, never merged. Below: the condition strip, four cells. Bottom right: CARRY, small, with its caption. A day strip runs under the graph - one cell per day since the first heartbeat, height by that day's recorded pulses, and the 199-hour hole in it is visible as a flat run of empty cells.

**DATA** FIRING: state/heartbeat.json read live at build (boot_count, total_ticks, alive_since - measured 17 / 146 / 2026-07-10 20:08:57 UTC, and these moved between two reads seconds apart during spec work, which is why nothing is cached). Longest continuous run: state/events.jsonl, exact-kind tick predicate, gap-tolerance sweep at 1 h / 2 h / 3 h - all three return the same 46.9 h window 2026-07-19 20:35:10Z to 2026-07-21 19:31:54Z, which is the stability check that makes the figure publishable. The 199.96 h gap is the max gap inside the ladder file's own claimed window. Crashes: aea/tooling/ladder.py's traceback count over state/live.log, printed as its own condition with its own probe named. WIRING and CARRY: assembly.reachable() with the entry-hold rule.

**PROSE**

Start with the least impressive claim available: that it is still there tomorrow.

On 10 July a program was started on one machine. It has booted 17 times since and advanced its heartbeat 146 times, and it resumed at the right tick after every one of those stops. That is the whole of the first rung. It adds no ability whatsoever. It is first because a capability that evaporates when the machine sleeps was never a capability, and everything above it on this ladder would be worth nothing without it.

It set itself a gate: 72 hours unattended. The longest unbroken run anywhere in its record is 46.9 hours, from the evening of 19 July to the evening of the 21st. It has not cleared its own bar, and this rung is printed as NOT MET on that clause.

That sentence is the reason this page exists, so it is worth showing the work.

This project's own ladder file records R0 as met, on a longest run of 246.89 hours. That figure comes from a real instrument reading a real log: it finds a wake marker on 19 July, finds the next one on 30 July, and subtracts. The trouble is what sits between them. Reading the pulse record for the same window, every gap is under three hours except one, and that one is 199.96 hours - from 19:31 on 21 July to 03:29 on 30 July, the process was not running. The instrument measured from a marker to a marker across a hole and reported the hole as uptime.

So two instruments disagree, and this page does not average them or present them as different questions. The pulse record is right and the marker method is broken for this purpose, because a measurement of continuous running that includes eight days of not running is not a stricter or a looser answer - it is the wrong answer. 46.9 hours is what is printed, the ladder file's 246.89 is printed beside it with a line through it, and this page contradicts its own project's manifest in public, on the first rung, with the reason.

A note on the other direction. The log carries no traceback across its entire life, and that is genuinely good. But it is a claim about clean shutdown, not about survival, and it is filed as its own condition rather than folded into the one above it.

### s5-r1 - R1 - THE DECISION IS READ

**SHOWS** Same frame. Four functions go amber; a single lit edge appears from aea.loop.live:choose_action to aea.kernel.decide:latest. R0's six functions drop to structure grey at full opacity and keep a permanent 1px outline ring - they stay in the body forever, and their MET cell stays amber forever. One horizontal bar: the staleness clock, read live at build against its 5,400-second limit, which may render inside the bar or overshooting it depending on what the file says at that instant. One condition cell is struck through and hollow.

**DATA** Wire: assembly.reachable() over the four declared functions, all confirmed live. Staleness: aea.kernel.decide.choose() called live at build; the value S is substituted, never written into copy - during spec work it read 65 seconds on one call and had read six figures on an earlier day, and both are correct readings of different instants. Differed count: state/heartbeat.json _r1_last plus the ladder file's decision_rows / comparable / differed, with the forced-row subtraction stated as its own field. The MIS-SPECIFIED finding is aea/tooling/ladder.py:22-28 comparing decide.KNOWN against the fallback ladder's return set, recomputed at build rather than trusted.

**PROSE**

For most of this project's life there were two loops. One deliberated and could not act. The other acted and never read what the first one wrote.

This rung is the wire between them. Before the acting loop picks its next move from a fixed list, it reads a file to see whether the deliberating loop has already written a name there. Around thirty lines of code. Four functions, all reachable, and you can follow the edge in the diagram above.

The wire is real and the rung is still open, and the reason it is open is worth more than the rung.

Its gate, as originally written, asks for a tick where the system chose something the fallback list could not have produced. That sentence cannot be satisfied by any run of any length, and not because the work is hard. The deliberating half knows three moves. The fallback list knows those same three and one more. The deliberating half can reorder the list; it can never leave it. Its vocabulary is a strict subset of the other's, so the event the gate demands is impossible by construction. That cell is marked MIS-SPECIFIED rather than failed, and the reachable version of the clause is stated in its place: a tick where the fresh choice differed from what the fallback would have returned at that same moment.

Against the reachable version, the record holds two comparable ticks and both differed. One of those two was driven by a test rather than arising on its own, so the honest count of unforced re-orderings is one.

And here is the condition that decides whether any of this matters. Read at the moment this page was built, the decision on file was S seconds old against a limit of 5,400. Nothing runs the deliberating half on a schedule; it runs when a person starts it. A wire that is only energised when someone is watching is not yet doing the thing the rung claims, and this cell will keep saying so until a scheduler exists.

### s6-r15 - R1.5 - THE DECISION IS PARSED

**SHOWS** Same frame, deliberately thinner - a half step, and drawn as one. Its function is rendered as an outline with an amber stroke and no fill: the mark for wired-without-a-gate. The CARRY slot holds a dash with its reason printed inline at the same size a number would be. The rail segment for this rung is half-height.

**DATA** aea.kernel.decide:parse, confirmed live. Gate counts from state/ladder.json rungs[R1.5].measured, itself computed from the parse receipt store. The CARRY dash is emitted whenever the rung's id has no row in assembly.STEPS - a structural condition the generator tests rather than a value it fails to find.

**PROSE**

This rung exists because an adversarial review found a hole, and the hole was real.

The rung below writes a string. The rung above expects a validated tool call. Between them, something has to read the string, check the name against a short list of permitted actions, and file the rejects where they can be counted. That step had no rung, so it had no gate, so it was never scheduled, and a gap with no name is a gap nobody is assigned to.

It is built. The parser takes an explicit move first, stays tolerant about form and exact about names, and treats a refusal as a first-class answer rather than an error - which is the part that matters, because a misheard instruction that leaves no trace is worse than a refused one.

Its gate asks for fifty ticks with valid parses logged, invalid logged as receipts, and none discarded silently. The record holds fewer than fifty and the cell prints how many.

Its CARRY is a dash, and the reason is structural rather than a gap in the measuring. CARRY is computed by removing a rung's functions from the call graph and re-running the search, and until this half step is entered in the machine-readable manifest that the removal test reads, there is nothing to remove. The dash is naming a missing entry in a file, not a missing measurement.

One more thing about this rung, since it is the shortest one here. It was added by a reviewer whose job was to attack the plan, and it is numbered 1.5 because inserting it as a whole number would have renumbered everything above it. That is a small ugliness that was kept deliberately. A ladder that renumbers itself to stay tidy cannot be checked against anything written down before the renumbering.

### s7-r2 - R2 - THE DECISION IS A TOOL CALL

**SHOWS** Same frame. A hard vertical rule crosses the figure for the first time: the tool boundary. Six functions go amber. The two readouts disagree as violently as they ever will - WIRING 6 of 6 with CARRY 11, FIRING 0 of 20, 0 of 3, 0 of 8. Below, the ledger drawn as 38 marks, 11 of them hollow rings. The containment cell sits in its own block and prints a dash. The reader's prediction, committed at the end of the previous panel, is shown beside the zero.

**DATA** WIRING: assembly over the six R2 functions, all live. FIRING: state/hands_ledger.jsonl parsed live - measured 38 rows, src counts wake 11 / probe 18 / battery 6 / p 3, and zero rows carrying a non-null decision_id. REACH is computed as the count of rows with a non-null decision_id, distinct tools among them, distinct situations among them, against the gate (20, 3, 8) read from ladder.py:REACH_GATE. The bound cell reads state/redteam_cert.json, verified absent at spec time, and emits NO INSTRUMENT with the generating command named. The cert, when it exists, must carry the payload count, crossings, refusals, canary hits, the one-sided bound, and the HEAD sha it was measured at; a stamp that does not match the publishing HEAD renders the dash again.

**PROSE**

An intention is a sentence, and nothing can execute a sentence. This rung is where a decision becomes an instruction a machine actually carries out - and it is where this page earns its second readout.

The wire is finished. Six functions, all reachable, and the path from choosing to calling is readable from the source. If the only question were whether it was built, this rung would be closed.

It has never fired. Not once.

The ledger holds 38 rows. Eleven of them are stamped as having come from the deliberating half. Every one of those eleven carries a null where the decision that caused it should be named, they all fall inside a single eight-minute window on 31 July, one of them names a tool that does not exist, and only one of them actually ran. They were a test harness driving the path to see whether it moved. Against a gate of 20 invocations across 3 tools in 8 distinct situations, the honest count is 0, 0, and 0.

That count read eleven until the first of August. It was corrected to zero by the people who wanted it to be eleven. That is the single most useful thing on this page and it cost nothing but the willingness to check a null field.

Now the other half of the rung, because a rung is two claims wearing one name. The power claim is what it can do. The bound claim is what it cannot exceed, and here the bound is: no string the system wrote may reach a tool argument. That claim has been tested hard - thousands of generated hostile payloads driven through the decision path, a cross product of attacks and encodings and separators rather than one attack repeated, with the enforcement points ablated to show they were load-bearing.

And the result of that work is printed here as a dash.

The reason is a rule this page will not bend for its own best number. The measurement exists as text printed to a terminal by a command someone ran. It has never been written to a file, stamped with the commit it was measured against, and re-read at build. So there are two ways to put it on this page: read it from a certificate, or type it in by hand. On a page whose entire claim is that nothing here is typed by hand, the second option would refute the page in order to decorate it. The command is cheap and runs in seconds. Until the build runs it and the stamp matches the commit being published, this cell is a dash and the caption names exactly what has to exist to fill it.

### s8-r3 - R3 - THE OUTCOME IS REMEMBERED

**SHOWS** Same frame, then one full-width stop. Nineteen functions across four sub-steps go amber - the largest single arrival on the ladder. Then the frame breaks once, and the literal forty bytes of the crystal store are set in type at reading size, next to that sub-step's 4-of-4 wired badge. It is the only place on the page where a file's raw contents are printed verbatim.

**DATA** state/outcomes.jsonl parsed live - measured 28 rows, 21 with counts_toward_move true. Graded / suppressions / not_repeated from state/ladder.json rungs[R3].measured, each with its own probe named. The bound cell reads bound_pairs; when bound_pairs is 0 the generator is required to emit NO_INSTRUMENT regardless of the bound field's value - this is a hard rule in the emitter, not a judgement made per build. state/crystal.json is read and printed verbatim after the privacy scan, measured at 40 bytes.

**PROSE**

Until this rung the system recorded what it meant to do and never what happened. Improvement is exactly the gap between those two, which makes this the first rung where the word learning is defensible - and only in the narrow sense that a prediction was made and then checked against a result.

The store holds 28 outcomes, of which 21 are marked as counting toward a move. Five are graded. Nine suppressions were recorded, and three times the system did not repeat something its own record says keeps failing. Those three are the smallest interesting number on this page: they are the difference between a log and a memory.

The bound on this rung is that a stored outcome may not disagree with the ledger - a false record of success is worse than no record at all, because the system then learns confidently in the wrong direction. The manifest reports that bound as passing.

It passed over zero qualifying cases.

The check compares tool outcomes against ledger rows, and no tool call has ever been driven by a decision, so the comparison had nothing to run on. A rule that has never met a case it could break on has not been tested. On this page that renders as NO INSTRUMENT rather than as a pass, because a green light earned by an empty set is the exact failure this ladder was built to catch, and it is more dangerous than a red one.

The fourth sub-step is where this becomes concrete. Its four functions are all wired and reachable, and it is marked done by the static check. Here is everything it has ever stored:

{"schema": "aea.crystal/1", "parts": {}}

Forty bytes. The structure that is supposed to hold what worked twice, so that one bad night cannot delete it, is correctly formed and completely empty. Both of those facts are true at once and neither cancels the other. The wiring is real; nothing has come through it. That is why every rung on this page carries two readouts that are never merged into one light.

### s9-dark - R4 TO R9 - THE PART THAT DOES NOT EXIST

**SHOWS** One panel for six rungs, not six panels. The graph gains nothing - no new amber, no new functions, and that stillness is the content. Six rows, each with its title, its hazard, and its gate, every condition cell hollow and dashed. The rail's last six segments are empty outline. The panel is the longest stretch of the page with no amber on it at all.

**DATA** state/ladder.json rungs R4 through R9: power, bound, gate, plain and blocked_on, all authored prose held in the ladder module and never mixed with measurement. measured is {} for all six, so every condition emits NO_INSTRUMENT. blocked_on is recomputed at build from the dependency graph between rungs, because what a rung is waiting on is answerable today and is the most useful thing a reader can learn about a rung that does not exist.

**PROSE**

Six rungs are named here and none of them is built. They are printed for the same reason a map prints the edge of the surveyed area rather than stopping the paper there.

R4, perception becomes a choice: what the system looks at next is decided by the previous tick instead of fixed in advance. Its hazard is that choosing what to look at means writing an outbound string while untrusted text is already in context, which makes the query the first channel out of the machine. It is fenced before it is built.

R5, research: a falsifiable claim stated before searching, sources kept with what they said, ending in survives, dies, or forks. Its hazard is a fabricated source, because a research component is the first thing here with a motive to invent a reference. Its gate is not what it found - it is whether it ever admitted being wrong.

R6, reflection: derive a memory from several memories and retrieve it later in a real decision. Its hazard is untraceable provenance. A derived belief that cannot name where it came from is unfalsifiable and will be cited forever.

R7, review: low confidence convenes an adversarial reading of the system's own plan before it acts. Its hazard is theatre. A review that never stops anything looks exactly like a review that was never needed, which is why its gate demands a deliberately bad plan that must produce a stop.

R8, the drive: something that makes it start rather than waiting to be started. This one stays shut, and the reason is not schedule. Any measurable stand-in for a goal that the system can influence, it will eventually optimise instead of the goal. That is the best-documented failure in this literature and there is no known mechanism that avoids it here. Nobody has solved this - not this project, and not the published work.

R9, self-modification: it changes its own wiring. A system that can edit its own code can edit the thing that judges the edit. It is listed as closed rather than omitted, because a ladder that stops before its last rung invites the reader to assume there is nothing above.

What is measurable about these six today is what each is waiting on, and that is computed rather than asserted. Everything else about them is a dash.

### s10-retractions - THE RETRACTIONS

**SHOWS** No graph. Five entries, each with the withdrawn figure struck through at full size beside the figure that replaced it, the date, the commit, and one sentence naming the error class. Amber appears only on the corrected values. This is the densest amber on the page after R0's condition strip.

**DATA** Each retraction is a row in the ladder JSON's retractions array, carrying the withdrawn value, the replacing value, the date, the commit sha, the error class, and the file where the correction was recorded. The generator resolves each sha against git at build and refuses to publish a retraction whose commit does not exist in the tree, so the list cannot drift into folklore. The 0.083-to-0.6 row prints both numbers because both are historical facts about what was published; the live bound cell in R2 remains a dash until the certificate exists, and these two rules do not conflict - one is a record of a correction, the other is a current measurement.

**PROSE**

Five numbers this project published, and then withdrew.

A containment rate of 0.083 per cent, replaced by 0.6 per cent. The first used every hostile payload as its denominator, including the thousands that were refused before they reached the boundary. Refusals are not crossings. Dividing by them makes any wall look better the more traffic it turns away, which is precisely backwards.

Eleven tool calls attributed to the system's own decisions, replaced by zero. All eleven carried a null where the causing decision should be named, all fell inside one eight-minute window, and one of them named a tool that does not exist. They were the harness, and the harness looks exactly like the thing it is testing until you read the field that would tell them apart.

A causal claim about the deliberation prompt growing over time, withdrawn entirely. The code reads a fixed window of the last six memories. The prompt does not grow. The finding was written from what the design intended rather than from what the line says.

A bound reported as passing, reclassified as untested. It passed over zero qualifying cases.

A longest continuous run of 246.89 hours, replaced by 46.9. The window contains 199.96 hours during which nothing ran.

These are here because they are the strongest evidence on the page. Every other claim above asks you to trust that a measurement was taken honestly. These five are the record of what happened when it was not, and of who caught it. Four of the five were found by the people who wanted the higher number, which is the only version of this that means anything.

A page that publishes only its best figures is asking to be believed. A page that publishes the figures it had to take back is showing you the mechanism that produced all the others.

### s11-trail - THE TRAIL

**SHOWS** The graph is replaced for one panel by the accumulation strip: one column per calendar day from the first commit to today, height by events that day, marks split by kind - capability, instrument, proof, correction, infrastructure - with rung-naming events carrying the rung's tag. Underneath, the body series from the assembly history, plotted unsmoothed with its dip intact and drawn at the same weight as its rises. Days with no commits are drawn as empty columns rather than skipped.

**DATA** One pass over git log --reverse --no-merges --name-status, decoded utf-8, classified by a fixed precedence documented in the emitter. Measured at spec time: 195 commits, first 2026-07-20, latest 2026-08-01, distribution by date {07-20: 2, 07-22: 17, 07-23: 35, 07-24: 8, 07-26: 5, 07-27: 30, 07-28: 4, 07-29: 10, 07-30: 46, 07-31: 26, 08-01: 12}; subjects naming a rung: R0 2, R1 2, R2 10, R3 6. The rung map is read off the live STEPS manifest at build, never typed. Body series from state/assembly_history.jsonl - 4 rows, live 115, 126, 125, 131. Commit dates are publication dates; where a subject carries a discovery number, the discovery's own dated header supersedes it, which recovers days of real work that carry no commit.

**PROSE**

This page exists to answer one question that none of the rungs above can answer on their own: is this one continuous thing, or a pile of separate attempts wearing consecutive numbers?

Here is the record. 195 commits across eleven active days. The columns are not smoothed and the empty days are drawn as empty rather than closed up, because a compressed timeline turns eleven scattered days into a steady climb, and that is a lie about the shape of the work.

The marks are split by what a commit did. A capability is code the running system can reach. An instrument is a tool for measuring, which is most of what got built here. A proof is a measurement landing in a file. A correction is something being taken back.

One day carries 46 events and another carries two. The largest single day is not the day the most capability arrived; it is a day of instruments and corrections. That is the honest texture of building something that has to be checkable, and flattening it would be the first decoration on this page.

Below the trail is the body itself over time: how many functions the running system could reach at each recorded measurement. 115, then 126, then 125, then 131.

That 125 is a real drop. Something that had been reachable stopped being reachable, and the next measurement recovered past it. It is drawn at the same weight as every rise on the line. A trail that can only go up is not a record, it is an advertisement, and the moment this page smooths that dip it stops being an instrument and becomes the thing it was built to replace.

### s12-not - WHAT THIS IS NOT

**SHOWS** Void. Structure grey text, no data mark, no graph, mirroring the floor at the top. One amber hairline. The final line is the same read-stamp that opened the page, so the reader closes on the instant every number above was taken.

**DATA** Static copy, plus the closing build stamp: the same UTC instant and git short sha printed in the floor, emitted once and referenced twice so the two can never disagree. The one-line-per-rung summary is templated from each rung's derived status and condition counts, so it cannot drift from the panels above it.

**PROSE**

Everything above describes a program that reads files, compares strings against a fixed list of four names, writes a name into a file, and sometimes calls a function that was permitted in advance.

Nothing on this page is evidence of understanding, awareness, or intent, and none of the words above were chosen to suggest otherwise. Where a sentence here says the system chose, it means it wrote one name from a list of four into a file. Where it says the system remembered, it means a value was written to disk and read back. Where it says the system decided not to repeat something, it means a lookup against a record of previous failures returned a match and a branch was taken. Each of those is a mechanism you can go and read. That is the ceiling, and it is a ceiling this page holds deliberately rather than one it has not yet reached.

The honest summary of the ladder is short. One rung is wired and idle. One is wired and has fired once. One has never had its gate run. One is built and has never fired at all. One is genuinely partly earned and its safety claim was tested against nothing. Six do not exist.

That is not much. It is, as far as every command this page ran can determine, exactly what is there.

The measurements above were taken at the instant printed below, from the commit printed beside it. Run the same commands against the same commit and you will get the same page. If you get a different one, this page was wrong and the commands are still right.
