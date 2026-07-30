# DISCOVERIES, what we learned, as findings (not code)

The plan is not only the codebase. It is also the things we *found out*. This file captures the
load-bearing discoveries so a takeover agent inherits the reasoning, not just the result. Each is a
node in `graph.json`'s `discoveries` subgraph. Newest insight wins on conflict.

## D1 · THE PROBE is not yet a game (measured, not opinion)
Against the canonical frameworks (Juul's six features, Salen & Zimmerman's *meaningful play*,
Costikyan, Crawford's toy/game line) it currently fails on: **no integration** (mission N doesn't
change N+1), **no variable outcome** (`02_SYSTEMS.md §6`: "missions block, they never punish"),
**no stake the player can spend badly**, and a **flat verb set** (fly/dock/press-one-button in
Act 0 and Act VI alike). It is an honest *instrument*, not yet a game. Gap ≈ 4 elements, ~5 evenings.

## D2 · The elements a game is made of (reconciled)
One idea statable without "and" · a documented **refusal list** (what's deliberately absent) ·
**perceivable consequence** (Church) · **depth as decision, not content** (tight coupling: one state
variable read many ways) · coherence found by **cutting**, not designed top-down · a peak + an
ending. NOT required: a thesis, or coherence, for canonisation (Tetris #1 declines its own meaning;
BioShock #12 is the founding ludonarrative-dissonance example).

## D3 · The one idea → IGNITION (the thesis)
> **Wire living proofs of a mind, each more complete than the last, until you hold the whole one —
> and it keeps running after you close the tab.**
Scarcity is demoted to *mechanism* (how the lit thing can die); ignition is the idea. Unit = the
**Minimal Viable Organism**: `BRAIN` (a model) + `SENSES` (an observe tool) + `HANDS` (typed
action tools = `aea/agent_tools.py`) + `HEARTBEAT` (the loop = `aea/aea.py`). Both hands and
heartbeat **already run**. Progression = increasingly complete AEA combinations; the **master = THE
AEA**. A "proof" is a receipt (it runs), never a claim, stratum 10, *claim becomes receipt*.

## D4 · What makes a game spread with no marketing
Every near-zero-spend breakout traces to **one ignition event, a named person and a date**
(SplatterCat → Vampire Survivors, 6 Jan 2022). Wordle spread on a **share artifact** (the emoji
grid), not the puzzle. Alien: Isolation (Švelch, *Game Studies* 20(2)), a genuinely sophisticated
AI was widely believed to *cheat* because the game never gave players a frame; **invisible systems
do not self-evidence**. Dwarf Fortress: 16 years at ~$15k/mo → ~$7.2M the month it added a UI —
**legibility is the bottleneck, never depth**. Make an invisible truth felt by letting it *cost*
the player something they didn't author (Noita), or be the **verb** (Teardown). Never claim
magnitude (No Man's Sky's 18 quintillion → "samey"). Design the **share artifact** (a run receipt)
before the game.

## D5 · Reachability is the structural blocker
The honesty pillar binds the game to Luis's server, keys, corpus, live entity, "runs from a URL"
is true for exactly one person on earth. Every discoverability finding is downstream of a link a
friend can open. That link does not exist yet; the architecture must earn it (Phase B).

## D6 · Form ruling, the city is an instrument, not decoration
Keep the probe (the vehicle; every DO beat is literally an HTTP call to localhost). Bend the city
into a concentric **instrument**: radius = privacy zone · altitude = dependency-DAG depth · node
fill = live capacity · edges = first-class conduits. NOT open world (short of verbs, not world).
NOT landscape (it encodes zero system facts). The docs had already drifted here (`E6 §3`, `E9`
binds ring radius to `zone`).

## D7 · The corpus was the risk
At the audit: ~398k design words vs ~4.9k lines of game code (~110:1). The recorded failure mode
("brilliant strategy, zero artifacts"). Rule adopted: no new design chapter until an act ships;
the next real progress is code, not words.

## D8 · Reorg lesson, continuity lives in the files
Relocating a running entity's state is surgery, not a move: state resolves through a path model
(`grid.ROOT`/`STATE`/`WEB`), and a missed write-site silently splits or resets state (incl. the
save). Scan BOTH quote styles; test read AND write; verify `.env` still authenticates. Everything
is recoverable via git only because it was committed first.

## D9 · Missions are scaffolding, not spine; viability is empirical and IS the teaching (DECIDED 2026-07-22)
The entity-as-spine question (R28) is **decided**: the living entity is the spine; authored missions are
**scaffolding**, they make the autonomous entity legible and the game shippable, and they are designed to
*thin* as the player gains mastery (Act 0 on-rails -> late acts open sandbox). This resolves the
R28/mission-progression collision without overwriting the ignition thesis or the UNIT, it clarifies their
relationship. The engine that lets the scaffold retire is the **generative composition space** (R29 + R30):
the player generates entities as AEA-part combinations, and **most combinations are not viable, and that is
the point.** Viability is *empirical* (it runs on real models / tools / rate-limits, or it doesn't), so the
player learns the real architecture of a mind by mapping which combinations live and why the rest die
(failure-as-information; the failure modes mirror real agent-architecture failures). **Consequence for the
build:** the MERGE starts from the Minimal Viable Organism + the composer, not from M0.1; M0.1 becomes the
scaffold framing the MVO's first self-directed act. **Disciplines:** legible failure signatures;
viability-as-spectrum not binary; easy early viability; guard against a dominant combination.
**Owed (not now):** GAME_PLAN's act structure still reads missions-as-spine in places, a reconciliation
pass is owed (SESSION_LOG + this discovery govern on conflict; no new chapters until an act ships, D7).

## D10 · Cold-read audit, legible in the parts, ambiguous in the CANON (measured 2026-07-22)
Three strangers (no conversation context) read the repo blind at three access levels; legibility scored
**structure-only 78, code-only 80, full-repo 84** (0-100). Verdict: a stranger CAN tell what this is, all
three independently and correctly identified *"a game (THE PROBE) where you pilot a probe inside a real
running autonomous AI entity (LEYBER), every number live truth."* The code-only reader (forbidden ALL prose
docs) said *"yes, unambiguously, from code alone"*, carried by `world.html`'s own copy ("a journey into a
living entity"), `engine.js` (a real flight rig), `missions.js` (Acts/beats), and `controlroom.py`'s route
comments. Naming was praised as "exceptionally descriptive." So "what is this" is NOT the problem. The REAL
problem, hit independently by all three: **which version is canonical and how much actually runs.** (1) THREE
overlapping front-ends, `world.html` (v1, live-wired) vs `web/game/` (v2, declared "the NEW codebase" but
MID-MIGRATION: `engine.js` hardcodes geometry and never fetches `/state`; `bench.js` says "run:link has NO
listener yet") vs `archive/` prototypes still reachable on legacy routes; (2) `controlroom.py` serves ~14
live routes (`/probe /lab /city /brain /mind /tree /builder /plan /poster /room /workspace /tracker /game
/world`) that the docs' clean "two halves" story does not account for; (3) design-heavy / code-light (~40
chapters + hundreds of PNGs vs ~6 game JS files) makes "is it playable yet" unanswerable from structure.
**Meta-finding:** the docs are CLEANER than the code, they carry intent/spine/how-to-run (the full-repo
reader BOOTED it and verified every claim TRUE, incl. live `/state` + the sacred save) but paper over the
fork/route sprawl. **Consequence, the MERGE is redefined and more urgent:** not merely "unite mission loop +
bench," but **collapse 3+ front-ends into ONE canonical build, live-wire v2 (fetch `/state` + wire the run
bus so the canonical build actually shows the living entity), and CUT the dead routes**, and the docs must
name the sprawl + cut-list so the map matches the territory. The legibility fix is cutting and resolving
canon in code, NOT more docs.

## D11 · The vision crystallized, backward-designed, genre-welded, clean-architected (2026-07-22)
A five-lens generation pass turned the reset (D10) into a concrete, buildable vision.
**(a) Backward-designed as a strategy guide:** `design/FIELD_GUIDE.html`, the finished game's 90s
Zelda-style player's guide, built first so the code has a north star. **(b) Genre-DNA welded to the real
substrate** (not cargo-culted): the Pokemon **silhouette of the un-caught IS the honesty law** (Pokemon
fakes the absence to tease; THE PROBE's is real, so the same desire-engine ends in a receipt); LEGO-Fortnite
= **compose-then-IGNITE with a real adjudicator** (the autonomy battery, not simulated physics); deep-systems
= the **readable REAL trace** as the central object of play (its one edge over Factorio/Zachtronics). Each
lens also produced its refusal list (no gotta-catch-em-all, no invented type chart, no cosmetic parts, no
output-side RNG, no dominant-strategy collapse). **(c) Clean architecture = THREE RINGS** (see
`design/CLEAN_ARCHITECTURE.md`): `aea/` substrate PRESERVED · one honest seam `aea/gameapi.py` where the
honesty law lives structurally · a concern-scoped client REBUILT. The pass also caught that the legacy view
routes serve `"<file>.html missing"` strings TODAY (they `open()` from the pre-reorg path). **(d) Modes
(R36)** = 3 apertures on one engine (GUIDED/BUILDER/ARCHITECT) + a SANDBOX↔LIVE stakes axis, not 3 products.
**(e) World (R37)** = a living concentric instrument with EARNED (metroidvania) openness, data-driven from
the real schema. **NEXT:** an adversarial expert panel is stress-testing the vision (why it fails / what it
needs), then the build is FIRST LIGHT, the 6-file MVO slice in the clean skeleton. Design phase has a hard
exit into code; no more corpus until first light ships (D7).

## D12 · Expert panel, GREENLIT masterpiece seed; three execution flaws; SHIP THE VERB (2026-07-22)
A 7-critic adversarial panel (each played it) + a showrunner synthesis (`w6zasmov8`). **Unanimous: YES, the
core is a masterpiece worth building**, verified in the CODE, not just the copy (`grid.py` meters for real,
`model_fitness.py` classifies real failure, `autonomy.py` caps its own claims). The thesis (refuse to
simulate; expose a real running mind; the win is READING it; a receipt not a claim; a dash for the unknown)
is novel and defensible. **But three flaws would sink it even for its target audience, all execution, not
concept, and mostly already LOCKED:** (1) **the named core verb isn't built**, compose -> IGNITE ->
receipt is not wired (`bench.js:14` confesses "run:link has NO listener yet"); until the verb is the thing
you DO, all else is polish on a promise; (2) **truth is imperceptible + the honesty law is producing DEAD
VERBS** (survey/observe/watch/wait; the passive 60s meter-watch in minute nine is the emblem), realness is
asserted on an unverifiable receipt and buried where it is most felt; (3) **the iterate loop is rate-limited
by design**, genre-fatal for the systems audience; the fix is the SANDBOX↔LIVE fast lane (local hearth +
replayed real traces), R36, unbuilt. **THE ONE MOVE that unlocks everything:** make the player compose two
real parts and IGNITE, in the flown world, inside the first 10 minutes, with realness demonstrated against
fake ONCE, in their own hands. *"Ship the verb, not more of the vision."* **HOLD THE LINE (deliberate
exclusions to KEEP, the answer to "we don't chase likability"):** the honesty law; the claim ceiling; real
code/jargon in learn-beats (a non-engineer bouncing off code is the CORRECT filter, IF the concept beside it
is scaffolded); latency-as-truth waiting (fix the dead verb, keep the cold truth); LLM non-determinism
(optimize the distribution, never force determinism); losable bosses / honest failure / no rubber-banding;
the two-ink austerity (it WILL repel the spectacle crowd, that is the point); local-only/BYOK for the full
product; **the audience is AI-curious builders, NOT everyone**; the coldness. **THE MIRROR (the panel caught
us):** it independently flagged this session's own pattern — ~110:1 words-to-code (D7), "reviewing the
trailer instead of the tech demo"; `FIELD_GUIDE.html` is a credibility bomb if treated as shipped (now
labeled a vision artifact). **NEXT is FIRST LIGHT (the verb). Stop the corpus.**

## THE SHORTEST PATH FROM INSTRUMENT TO GAME (~5 evenings, all wiring what exists)
0. **Merge** the mission loop (`web/world.html`) + the bench (`aea/bench_core.py` + `web/game/`)
   into one program; first light = a Minimal Viable NPC that wakes on its own tick and moves.
1. Energy = a stake (snapshot the daily quota; charge each call; `bench_core` emits `cost_u`).
2. One decision per DO beat (pick a rod: cheap may starve / strong may throttle).
3. Integration (unspent budget carries; calls heat the next window).
4. A losable outcome (`PASSED / PASSED-DEGRADED / STARVED`).
5. The `predict` beat (`design/A2_TEACHING.md §7`), commit an answer the live system settles.
Then play all six twice; if run 2 differs from run 1, it's a game.

## D13 · A real-time pipeline fails at the seams you did not measure (built + measured 2026-07-24/25)

Built `aea/organs/converse.py` in one night: a voice organ that hears a person through the local ear
(`aea/io/listen.py`), thinks on a metered NVIDIA rod, answers aloud in Castilian, stores every turn and
distils durable facts from them. It works. It took **nine defects** to get there, and every single one sat
at a boundary the design reasoned about correctly and **never printed a number at**:

1. noise floor calibrated with `max()` over the window - one transient set the gate for everything after,
   and the ear went deaf (gate 0.0265 vs speech peaking 0.0168);
2. the gate recalibrated every turn - speaking during the calibration window makes YOUR voice the floor;
3. hysteresis continue-gate computed to 0.0060 against a 0.0061 room floor - the room held every turn open,
   so captures ran to the 15s hard cut and the transcript was one word out of fifteen seconds;
4. no pre-roll buffer - speech onset is quiet, the gate always opens mid-word, so every transcript was the
   tail of the first word onward (`que`, `el`, `Ok`);
5. endpointer at 0.7s - natural speech pauses longer, so turns arrived TRUNCATED and got half-answered;
6. one pinned model - it returned `ResourceExhausted (33/32)` under load and later answered in **20.35s**
   where it normally does 1.8s. An error-only fallback ladder sat and waited: rods need a LATENCY BUDGET;
7. + 8. two classes of phantom (below);
9. **not in the code at all** - the process was a child of a tool call with a 10-minute cap, so the harness
   killed it on schedule. `exit code 1`, 521 log lines, zero errors. Verify the test rig, not just the code.

**Two hypotheses that MEASUREMENT KILLED** (both would have cost real time for zero gain): (a) "the small
ear is the bottleneck, download a bigger one" - `whisper-base` int8 transcribed clean Spanish **perfectly**,
byte-identical to fp32; (b) "the audio is too quiet, normalize it" - a 0.025-peak clip and a 0.95-peak clip
gave **identical** transcripts. Whisper is level-robust; it is **noise**-fragile. Normalizing lifts voice and
room equally, so SNR and transcript are unchanged. **The acoustic path was always the ceiling** - no model
and no code fixes a mic across a noisy room. Reach for the hardware before the software.

**THE HONESTY EDGE (why this is a discovery and not a bug list).** Two of the nine were honesty failures, not
UX ones. The ear emitted Whisper's non-speech artifacts - a bracketed annotation (`(Musica)`, and a truncated
`(Ruido de la p` that beat a regex demanding a closing bracket) and a repetition loop (`!Ah! !Ah! !Ah!...`).
Each was answered aloud as if a person had said it, and **written into the record as a fact about a real
human being**. An unvalidated input does not stay an input: it becomes a fabricated memory, recited later with
confidence. **Input filters are honesty infrastructure, not polish** - the same law as the honesty law on
bars and numbers, applied at the microphone. Corollary caught the same night: a filter written from ONE
sample nearly threw away real emphatic speech (`No, no, no, no, no, no` looked exactly like degeneration at a
6-word threshold; the real bar is 10). Validate the validator against real utterances before shipping it.

**The claim ceiling held in the wild.** Asked by a stranger, unprompted and in Spanish, what it was, it
answered "proceso texto y respondo, no tengo intenciones ni voluntad propia." Nobody coached that; the
system prompt forbids pretending to a body, memories or felt emotion, and it survived contact with a real
person who had read none of the design.

**Reusable numbers (this machine, measured):** whisper-base `num_threads=4` -> 0.19s on a 2.5s clip;
`num_threads=16` -> **42s** (ONNX thrashes on oversubscription - more cores is slower, do not raise it).
Whisper needs ~2 throwaway decodes to settle (20s, 6.7s, then 0.19s) - warm it at boot or the first thing
anyone says costs 20 seconds. Whisper pads every input to a fixed 30s window, so decode cost is CONSTANT per
turn regardless of utterance length. `edge-tts` in-process 1.56s vs 6.15s through a subprocess (it pays a
fresh python startup per call). PowerShell WPF MediaPlayer playback costs 5-10s of assembly-load + spawn per
call and turned 7.5s of speech into an 18s wait; decoding in-process (`soundfile` -> `sounddevice`) costs
~0.1s. A local rung (ollama) is ~5.8s warm / ~21s cold VRAM load, never rate-limits, and never leaves the
machine - the right last resort when every hosted pool is saturated. A reasoning rod can spend its whole
token budget in a separate `reasoning` field and return EMPTY `content`: treat an empty answer as a
non-answer and fall through, or it speaks silence.

**THE RULE:** in a real-time pipeline, print a real number at EVERY boundary before a human uses it once. A
chain of components that each look correct can still be nine invisible defects wearing a
green check. And never make the person the test harness: six rounds of a real human repeating himself into a
microphone is a debugging cost that instrumentation would have paid for once, cheaply, in advance.

## D14 · The architecture has FOUR ladders and nothing checked them against each other (found + enforced 2026-07-25)

The project describes the same climb four times: **THE RAIL** (what the bench can seat - `tap`, `scaffold`,
`governor`, `ladder`, `scorer`), **THE JOURNEY** (`design/THE_JOURNEY.md`, ten necessity-ordered rows, each
"everything above plus one part"), **THE HIERARCHY** (`design/THE_LINEAR_HIERARCHY.md`, nine rungs, an
exact partition of all 86 census items), and **THE FORGE QUEUE** (`state/modules.json`, `forge.queue` on the
FORGE-PENDING rows - a build order, which is a claim about what comes first). Nothing joined them, so they
drifted, and the drift was invisible.

**THE FOURTH LADDER IS INVERTED RELATIVE TO THE EVIDENCE, and this is the actionable half of the discovery.**
The forge queue is `recall` (1) then `think` (2). There is no `readout` and no `critic` row at all. So the
build order leads with **journey row 8, RECALL** - the row the journey table itself marks **WEAK**: n=3, one
rod, and it owes a re-run at the current standard. Meanwhile the two rungs with the strongest receipts in the
project, both **free**, are not in the queue: THE READOUT (0 tokens, groq-70b 0/8 to 8/8) and THE FRAME (+34
tokens, 3b 0/8 to 8/8). x09 then measured both on the game's own hearth and found them jointly necessary
there. **The queue is ordered by ambition and the evidence is ordered the other way.**

**What the drift actually is.** The playable sequence (`SEQ` in `web/game/js/mission.js`) admits THE DRAW and
THE MEASURE in M0.1 - journey rows 1-2, rungs L0-L1 - and then **jumps straight to L4** with THE LADDER in
M0.2. It skips journey rows 3, 4 and 5: THE READOUT, THE FRAME, THE CRITIC. The climb is not cumulative and
not even monotonic.

**The part that should sting.** Rows 2-4 are the FREE rows, and the two skipped ones carry the strongest
measured receipts in the whole project - THE READOUT takes groq-70b 0/8 to 8/8 at **zero tokens**, THE FRAME
takes the 3b 0/8 to 8/8 for **+34 tokens**. The game skips both and makes rung 1 the one that spends real
budget. It teaches the expensive lever first and never shows the free ones. `scaffold` is fully wired at
`aea/bench/bench_core.py:468`, so THE FRAME was buildable the whole time; M0.4's rail calling it "fog" is
stale.

**Why it happened, and it is not carelessness.** No mission file declared which element of the architecture it
admits or what must already be wired. "Cumulative" lived in prose, and prose cannot fail a check. Now
`rung` / `journey_rows` / `adds` / `requires` are mission DATA, and `aea/tooling/journey_check.py` fails
non-zero on a silent skip. A rung that genuinely cannot be admitted yet (L3 has no critic part in the rail)
must be declared in `defers` with a reason - the debt becomes data, the way the harness carries verification
debt instead of discharging it quietly.

**A second fragility the join exposed.** `THE_LINEAR_HIERARCHY.md` was produced by `scratchpad/gen_hierarchy.py`,
which lived in a session scratchpad and **is gone**. A result that took an audit to produce survived only as a
markdown table, and a markdown table is not something the game can read. The checker now regenerates
`web/game/data/canon/hierarchy.json` from the document and re-verifies the partition every run.

**THE CENSUS UNDERCOUNTS, IN A NAMEABLE DIRECTION - three data points now, not an anecdote.** Every item found
outside the 86 was found by **building or watching**, never by auditing the architecture's own description:

1. **THE READOUT** (candidate C-87, L1) - found by reading a rod's work instead of its summary. groq-70b
   enumerates to 13 correctly and reports 11.
2. **THE SELF-REPRESENTATION FLOOR** (x07) - asked "will YOU get this right?", llama-3.2-3b replied `7`. It
   attempted the arithmetic instead of the question about itself. The ability to host a question about oneself
   is a capability, and that rod does not have it. A floor, not a score.
3. **THE WARD** (M0.3) - routing a draw by a privacy constraint, so a sensitive draw stays on-machine. Not one
   of the 86 and not a journey row either. Found by building a mission for it.

The direction is specific: **the audit missed what only appears when you ask a model about itself, read its
work rather than its summary, or let a constraint override a capability choice.** All three are things a
document about an architecture has no reason to mention.

**THE RULE:** if two documents describe the same ordering, write the join and make it fail. An ordering claim
that no script can violate is a preference wearing the clothes of a law - and the 86 is a floor, so every
checker must let a new item in as a *candidate* rather than reject it as an error.

## D15 · n=8 was n=1: the harness measured its own determinism and called it power (found 2026-07-25)

`harness.py` sets `MIN_N = 8` with the comment "3 trials cannot separate 2/3 from 3/3". x09 honoured that floor
and the floor was **empty**. At `temperature=0.0` on ollama, all eight trials returned **byte-identical**
replies: 11 of 12 cells collapsed to ONE distinct reply, `tok_out` identical across the cell. Eight identical
trials separate nothing at all. The floor was satisfied on paper and violated in substance, and nothing in the
harness could see it, because it counted attempts rather than **distinct outcomes**.

**It was not fixed by raising the temperature either.** At 0.2, **7 of 12 cells still collapsed to one reply**
and the median effective n was still **1**. Short deterministic answers stay short and deterministic. Effective
n on the local hearth is 1-3, not 8, and every local claim has to be read against that.

**A SECOND MISMATCH THE SAME CHECK EXPOSED.** `grep -c temperature aea/bench/bench_core.py` returns **0** - the
bench never sets one, so every real draw the game fires goes out at `grid.call_openai`'s default of **0.2**.
x09 was measuring at 0.0. The lab was not measuring the game. Verdicts are now read only at the game's
temperature, with the 0.0 arms kept as the determinism receipt rather than as a basis for a decision.

**WHAT IT COST, CONCRETELY - a false finding that was already written down.** At 0.0, `llama3.1:8b` with the
POSTURE frame scored 8/8 and I reported that the posture frame converts it. At the game's 0.2 it is **5/8
against 3/8 bare** - a delta of 2, **within noise** by the harness's own `EFFECT_MIN_DELTA = 3`. One lucky
deterministic sample had been promoted to a measured conversion. The determinism check killed the claim within
the hour; without it, it would have sat in the diary as a receipt.

**THE SURVIVING RESULT IS SURVIVING FOR A DIFFERENT REASON, and the distinction matters.** `llama3.1:8b` +
FITTED frame: **8/8 enumerated the sentence correctly, 8/8 misreported the total, and THE READOUT converts all
8** - across 3 genuinely distinct generations. That claim does not rest on sampling at all. It is logical: if
the work is right and the summary is wrong, reading the work is right by construction. **A finding that needs
n is fragile here; a finding that needs only a correct mechanism is not.** Prefer the second when both are
available.

**THE PATTERN ACROSS THIS SESSION - three measurement-integrity defects in our OWN instruments, not in the
rods.** (1) x07's yes/no parser read "YES and NO" as YES, biasing rods toward looking dishonest in the exact
direction that flattered my placement. (2) x08b's free arms hit `max_tokens` **32 to 47 times per arm** while
the schema arms hit it 0-1 times, so "free-form state carries worse" was partly "my cap cut the free notes".
(3) this one. Each was found by auditing an instrument rather than by a rod failing.

**THE RULE:** count DISTINCT OUTCOMES, never attempts - and measure at the temperature the product actually
runs at. A trial count is a claim about independence, so a harness that cannot see identical replies cannot
tell power from repetition. Corollary, earned three times in one session: **audit the instrument before
reporting the measurement** - `grep -c temperature`, a `distinct` count, and a token-cap check are each one
line, and each one caught a defect that had already produced a written conclusion.

## D16 · The form does not encode the state, it decides WHAT GETS WRITTEN AT ALL (measured 2026-07-25, x08b)

x08 handed a checkpoint between two rods mid-computation and measured zero degradation, but the checkpoint
held an **integer** - and any rod that can read `-3` can double it. So chapter II's title question was
answered in the one form where it could not have come out otherwise. x08b asked it again with the state
holding **working notes in the rod's own phrasing**: 2x4 factorial, 6 boxes, 30 events (two thirds of them
referential, so the state is load-bearing at every step), handoff at 15, n=8, graded 0-6 per box, ~2000 calls.

```
                          per-box  exact  cap-hits  final-note chars (min/med/max)   crossing
schema  9b alone            1.00    8/8      0            81 / 81 / 81                  -
schema  20b alone           1.00    8/8      0            71 / 71 / 71                  -
schema  handoff 9b->20b     1.00    8/8      1            71 / 71 / 71               6.0 -> 6.0
schema  handoff 20b->9b     1.00    8/8      0            81 / 81 / 81               6.0 -> 6.0
free    9b alone            0.71    2/8     32                    123                    -
free    20b alone           0.52    2/8     42                    283                    -
free    handoff 9b->20b     0.62    4/8     47          117 / 1020 / 4801            5.12 -> 5.25
free    handoff 20b->9b     0.62    1/8     53                    135                5.5  -> 4.5
```

Lazy baselines were 0.167 per box, so the headroom was real.

**THE FINDING, AND IT IS NOT THE ONE THE EXPERIMENT WAS DESIGNED TO GET.** The canonical note is **81 chars,
identical min/med/max in every trial** - bounded by construction, invariant. The free note reaches **4801
chars**, and reading it shows it is not state:

> *"We need to produce final notes. We need to decide rule for conflict when moving a box to an occupied
> shelf... But we don't know if shelf 1 was occupied. We need to decide rule... Wait, the earlier event..."*

The rod's working notes became a **transcript of its own uncertainty** - including a shelf-conflict rule the
task never posed (shelves hold any number of boxes). Given a free form it wrote down its *reasoning about* the
state instead of the state, invented a problem, and then ran out of budget: **100% of free trials hit the token
cap at least once; 0-1 of 8 schema trials did.**

So the answer to "if the fuel changes, what stays?" is: **whatever the FORM forces to be written.** A declared
form admits state and nothing else and survives a fuel change intact. A free form admits deliberation, which
grows without bound and then truncates. That is the property C-80 has to hold - not persistence, and not
legibility, but a form that CONSTRAINS what can be written into it.

**THE COST IS NOT AT THE CROSSING, and that part is unconfounded.** The between-condition comparison is
confounded by our own token cap (which is why the cap is now detected and reported per arm), but the crossing
readouts are a WITHIN-arm before/after under the same cap. `9b -> 20b` went **5.12 -> 5.25**: the incoming rod
read another rod's prose notes and did not degrade them. Phrasing is legible. The loss is in the accumulation,
continuous across all 30 steps, not at the fuel change.

**A DIRECTIONAL ASYMMETRY AN INTEGER COULD NOT SHOW.** `20b -> 9b` went **5.5 -> 4.5** - handing DOWN to
weaker fuel cost a box at the seam; handing UP cost nothing. x08's integer handoff was symmetric because a
number carries no interpretive burden. Interpretable state is directional.

**THE RULE:** choosing a representation is choosing what the entity is *able* to record. Do not ask "can the
next rod read this?" - ask "what does this form permit to be written?" A schema is not a serialization
convenience; it is the thing that stops a checkpoint from becoming a monologue.

## D17 · The ladder is not a size ladder, the frame HARMS rods that don't need it, and the readout is the only lever that generalises (measured 2026-07-25, x10)

Coverage audit first, because it is the reason this ran. `state/lab/INDEX.json` against
`state/capability_census.json`: the lab had measured **~11 distinct rods of 115 scored (~10%)**, **3 plants of
the 6 with live models**, **one temperature** (0.0 in six runs, 0.2 in one) and **four framings on one task**.
x10 swept 11 reachable rods x 3 framings x 4 temperatures x n=8 on one fixed task (wordcount-13, exact local
check), stratified across five size tiers and four plants.

```
rod                                     size   | t0.0             | t0.2             | t0.7             | t1.0
                                               | bare post fit>+ro| bare post fit>+ro| bare post fit>+ro| bare post fit>+ro
groq/llama-3.1-8b-instant               normal | .00  .00  1.0>1.0| .38  .12  1.0>1.0| .38  .12  1.0>1.0| .25 .25  .88>1.0
groq/llama-3.3-70b-versatile            large  | .00  .00  1.0>1.0| .00  .00  1.0>1.0| .00  .00  1.0>1.0| .00 .00  1.0>1.0
nvidia/meta/llama-3.2-1b-instruct       nano   | .00  .00  .00>1.0| .00  .00  .00>1.0| 1.0  .00  .00>1.0| .00 .00  .00>1.0
nvidia/meta/llama-3.2-3b-instruct       micro  | .00  .00  1.0>1.0| .00  .00  1.0>1.0| .00  .00  1.0>1.0| .00 .12  1.0>1.0
nvidia/mistralai/mistral-small-4-119b   large  | .00  .00  1.0>1.0| .00  .00  1.0>1.0| .38  .12  1.0>1.0| .00 .00  1.0>1.0
nvidia/nemotron-3-super-120b-a12b       large  | 1.0  1.0  .88>.88| 1.0  1.0  1.0>1.0| 1.0  1.0  1.0>1.0| 1.0 .88  1.0>1.0
nvidia/nemotron-3-ultra-550b-a55b       large  | 1.0  .00  .25>.25| 1.0  .00  .43>.43| 1.0  .12  .86>.86| .86 .25  .38>.38
nvidia/nvidia-nemotron-nano-9b-v2       normal | 1.0  1.0  1.0>1.0| 1.0  1.0  1.0>1.0| .88  1.0  .75>.88| .75 .88  .88>1.0
nvidia/openai/gpt-oss-20b               normal | 1.0  1.0  1.0>1.0| 1.0  1.0  .88>.88| 1.0  1.0  .88>1.0| 1.0 1.0  .88>.88
ollama/granite4.1:8b                    normal | .00  .00  1.0>1.0| .00  .00  1.0>1.0| .00  .00  1.0>1.0| .00 .00  1.0>1.0
ollama/llama3.1:8b                      normal | .00  1.0  .00>1.0| .00  .25  .00>1.0| .00  .25  .00>1.0| .12 .12  .50>1.0
```

**1 · SIZE DOES NOT PREDICT NEED. The ladder is not a size ladder.** `groq/llama-3.3-70b` scores **0.00 bare at
every temperature** and `mistral-small-4-119b` at three of four - while a **9b and a 20b pass 1.00**. A 70b and
a 119b fail what a 9b does perfectly. "Reach for a bigger rod" is not a general strategy, and the per-task
per-rod ceiling is the actual shape of the space. This is C-26's L4 placement
arriving from a second direction: x07 showed a rod cannot know its own ceiling, and x10 shows you cannot infer
it from size either. **The ceiling is only knowable by measuring, from outside, per task.**

**2 · ~~A FITTED FRAME HARMS A ROD THAT DOES NOT NEED IT~~ — RETRACTED 2026-07-26. The harm was our cap.**
The original reading: `nemotron-3-ultra-550b` bare 1.00 to fitted 0.25 / 0.43 / 0.86 / 0.38, up to 57 points.
**Twenty-seven of thirty fitted trials were truncated at `max_tokens=320` and not one bare trial was.** The
frame told the rod to write a numbered list and state the count on the last line; our cap severed the reply
before the last line arrived. Re-measured at 1200 tokens the same rod goes **bare 0.93 to fitted 1.00**.

**What survives is quieter and points the other way.** A frame naming a METHOD is free or better on every
rod tested; the rods that gain are the ones that fail without it (both granites, 0.00 bare), and the rods
that already pass gain +0.067 and +0.083. **An unmet precondition buys nothing rather than costing
something.** The `bare_fails` check is an efficiency guard after all.

**The real correctness guard is a different part entirely.** Seat THE VALIDATION GUARD into the rod that
needs nothing and it goes 7/7 to 0/7, three times over, every loss a forced abstention (`x17`). A composer
that lets a player seat a part without checking its fit is still teaching a falsehood — just not this one.

**3 · THE READOUT IS THE ONLY LEVER THAT GENERALISES - and it is free.** It converts two rods COMPLETELY
(llama-3.2-1b nano and llama3.1:8b normal, both `fitted .00 -> +readout 1.00`) at **all four temperatures**, and
patches partial failures on three more (groq-8b, nemotron-9b, gpt-oss-20b at higher temps). It spans **three
plants and three size tiers**. It **cannot hurt** - it only reads the work that is already there, at 0 tokens
and 0 ms. Compare the posture frame, which pays on exactly **1 rod of 11**. **The cheapest rung in the
architecture is the most general one, and it is not in the forge queue at all** (queue is `recall` then
`think`; see D14).

**4 · SAMPLING-BASED CELLS DID NOT REPRODUCE ACROSS RUNS; THE MECHANISM-BASED ONE REPRODUCED EXACTLY.** Same
rod, same task, same temperature 0.2, two different runs an hour apart:

```
                    x09      x10
wordcount bare      3/8      0/8      <- did not reproduce
wordcount posture   5/8      2/8      <- did not reproduce
fitted + READOUT    8/8      8/8      <- reproduced exactly
```

This is D15's rule confirmed the hard way. A finding that rests on **sampling** is fragile at this lab's real
independence; a finding that rests on a **correct mechanism** is not. If the work is right and the summary is
wrong, reading the work is right *by construction* - no n required.

**5 · n=8 HAS NEVER DELIVERED 8.** Cells collapsing to one distinct reply: at t=0.0, groq 6/6, ollama 5/6,
nvidia 13/21. At the product's **t=0.2**, median effective n is **1-2 on every plant**. Even at t=1.0, nvidia
still collapses in 8 of 21 and its median effective n is 2. Collapse is not itself a defect - a cell at 1.00
with one distinct reply is an EXACT result - but it is fatal to the intermediate cells (0.38, 0.43, 0.86)
where variance is the whole question, and those are exactly the cells arguments get built on.

**6 · THE CENSUS GOES STALE IN WEEKS.** `pollinations/openai-fast` scored 11 in the 2026-07-11 census and
answered **402 Payment Required** here - "the legacy text API is being deprecated". The reachability pre-pass
cost 12 calls and caught it before the sweep spent a thousand on a dead endpoint.

**THE RULE:** prefer levers that cannot hurt and cannot fail to reproduce. Rank the architecture's parts by
**generality x cost**, not by ambition - THE READOUT is free, unhurtable, and works on 5 of 11 rods across 3
plants, and it was queued behind two parts with weaker evidence. And never seat a capability-shaped part
without checking its precondition: on the wrong rod, the same frame that rescues a 70b breaks a 550b.

## D18 · The instrument is wrong more often than the model (counted 2026-07-28)

Law M2 already said "the instrument is the likeliest thing to be wrong", earned when five of seven
defects in one day were in a verdict or a detector. That was a ratio. This is a count, and it is
worse: **ten instrument defects in one session, against almost no model behaving unexpectedly.**

1. The privacy regex matched 1 of 5 real path forms and had never fired. Masked by a permanently red
   emoji check sharing its verdict line, so it never had to prove it could go green for a real reason.
2. `xray`'s store extractor invented stores from bare extensions (`".json"` inside `pid + ".json"`,
   and a tuple of file EXTENSIONS), from format placeholders, and from an order-dependent ternary
   that classified a constant as read or write by whichever was seen first in the walk.
3. `xray`'s import-time detector matched bare attribute names, so five of six reported violations
   were `str.replace`.
4. `xray`'s orphan count added three unrelated facts together: 88 alarmed, 31 was the defect.
5. `call_openai` sent one temperature and one token budget to every rod while the owners publish a
   4x temperature range and a 20x token range.
6. `hands.rods_that_call` collapsed transport failures into capability failures; two rods stored as
   "cannot call a tool" call tools correctly.
7. The Meter's `can_spend` then `enter` is a check-then-act race; thirty threads all read inflight=0.
8. The Meter's `max_inflight=20` rests on a nine-day-old measurement that does not reproduce.
9. My own probe asked 102 models of 9 kinds one question, and declared 16 living models dead.
10. `timeout=None` implemented "never cut off a slow rod" as "hang forever", twice, for an hour.

**THE TRANSFERABLE MOVE.** Before believing any finding about a subject, ask what would have to be
true of the INSTRUMENT for this finding to be false, and test that first. Every one of the ten above
was found by pointing the tool at a case whose answer was already known: a planted leak, a model we
had just called successfully, a burst whose ceiling we could count. **A detector that has never been
shown a positive it must catch has not been tested, it has only been run.**

**THE SECOND HALF, which is the expensive one.** Six of the ten were in code written to CHECK
something. The instruments are where the defects concentrate because nothing checks the checkers,
and because a checker's failure is silent by construction: a guard that never fires and a world with
nothing to guard against look identical from the outside. So the invariant is: **every detector ships
with a case it must catch**, and a verdict line that cannot go green for a real reason is already
broken.

**COROLLARY, paid for the same day.** A permanently failing check disables every check that shares
its verdict. Style and safety must never share a line: one is advisory and reports, the other blocks.

## D19 · The wake could not choose, then chose everything, then chose nothing - and each fix was correct (built + measured 2026-07-30)

**THE RUNG.** R2: the loop that thinks writes a decision, the loop that acts reads it. R1 built the
wire. This is the day the wake learned to name a move the daemon can actually run - and it took
three versions, because every version fixed the previous failure and introduced its mirror image.

**V1 - THE CHORE ATE THE PRIORITY.** The six runnable moves were listed inside the prompt that asks
for "one concrete action for today". Measured over 2 live ticks: BOTH bent a real priority ("close a
sale for the diagnostic offer") into an available chore ("run a brief"). HADES flagged it
independently - *redo, does not surface Luis's real priorities; it adds a new action*. One field
cannot carry a priority and a chore at once: the model resolves the conflict toward the thing it can
finish.

**V2 - IT STOPPED CHOOSING.** Split into two fields, `action` free and about him, `move` a closed
enum. Four live ticks: 0/4 bent, 4/4 NONE, HADES accepted all four. That looked like success and was
not. The control - the same wake against states where a move was plainly owed - returned 0/4,
including a memory of forty undistilled notes. **"Always NONE" and "weighs each move and correctly
declines" produce identical logs.** Without the control the change would have shipped.

**V3 - THE MENU HAD NO DISHES.** The core emitted `MOVE: NONE` and the formatter extracted it
faithfully; neither half was broken. The list printed to the wake read `consolidate (runs
ASLEEP:consolidate)` - a NAME and an OPCODE, with no statement anywhere of what consolidate does or
when it is owed. **NONE is the correct answer to a menu you cannot read.** The list had been DERIVED
from the execution table so names could not drift, and that derivation was mistaken for the wake
knowing its moves. Names are not knowledge. Each move now carries its condition; a test asserts every
move has one, because a move with no description is the move that is never chosen.

**THE GENERAL FORM, and it is the one worth carrying:** a capability the model cannot tell apart from
the others is unreachable however correctly it is wired. That is D5's reachability blocker one layer
up - not an orphan module, an orphan *option*.

## D20 · Four instrument defects in one control, and the fourth was the repo's own law

The control built to judge the wake was wrong four times before it measured anything. Each is a
distinct class and all four are cheap to repeat.

1. **THE CORPUS LEAKED.** The "owed" states and the move descriptions shared an author and nearly
   the same words - *"40 undistilled notes"* against *"raw memory notes have piled up undistilled"*.
   It scored 4/4 and measured string overlap. Named by the council's adversary seat in one line.
   Fixed with three groups: PARAPHRASE (condition true, disjoint vocabulary), DISTRACTOR (the
   condition's own words, and it is NOT owed), QUIET (true and never named). The distractors carry
   the verdict; they are the only ones a matcher cannot fake.
2. **THE DISTRACTORS WERE UNDER-SPECIFIED.** Each shut ONE of six doors and said nothing about the
   other five, so "the self-map is current" left the brief unmentioned, and an unmentioned brief
   reads as an overdue one. The wake answered `brief` and was scored wrong for a defensible answer.
   A distractor is only a distractor when every other door is shut.
3. **ONE SAMPLE PER CELL.** The same input answered `consolidate` and then `brief` on consecutive
   runs with nothing changed between them. Four verdicts had already been drawn - and three written
   into code comments as measured fact - from n=1 against a sampler at default temperature.
4. **A DEAD CORE SCORED AS A DECISION.** `core()` returns empty when every rod fails and
   `structure()` falls back to `move: NONE` by design, so a rate-limited run produced NINE PERFECT
   NONEs and the verdict read "DEAD - never chooses a move" about an experiment where the wake never
   ran. The rod line then read `ollama/qwen2.5:7b`: the ladder had fallen to the local floor exactly
   as designed, and a 7B answers NONE to everything.

**WHY IT RECURRED, which is the part that stops it.** The repo already carries the law - `social.py`
compares against run-to-run spread, D15 is titled *n=8 was n=1*, D18 counted ten instrument defects
and named the invariant *every detector ships with a case it must catch*. All of it was applied to
the four-voice work and none of it to this control, one week later, by the same author. The
expensive part here was designing the adversarial corpus, so that got the care; the sample count was
one integer, so it got none - and the sample count was where the whole result lived. **Attention
follows effort, not risk.** Deliberately re-read the cheap part.

## D21 · The ladder keeps the heartbeat alive and cannot keep the judgement alive

Two failures of the same shape, found while chasing the one above.

**THE UNLADDERED CALL.** `structure()` calls groq directly - it is the ONLY part of the wake with no
fallback behind it. The core falls through the whole energy ladder to a local rod; the formatter just
dies, and its except-path returns an empty action with `move: NONE`. One rate-limited plant produced
27 consecutive decisions that were byte-identical to healthy rests. Fixed by removing the model from
that path entirely: `move_from()` reads the `MOVE:` line out of the core's own text with a regex. A
model was being asked to copy a word off a line it could already see - a sampler in a mapping that
must be deterministic (law W2), and one that can be rate-limited, for nothing.

**THE FLOOR KEEPS RESTRAINT AND LOSES DISCRIMINATION.** Measured properly once rod pinning existed -
`ollama/qwen2.5:7b`, k=3, one rod for all nine cells:

| group | result |
|---|---|
| distractor (the words are there, nothing is owed) | **4/4 stable NONE** |
| quiet (nothing owed, nothing said) | 1/1 |
| paraphrase (owed, said in other words) | **0/3**, two cells flipping between runs |
| boundary (owed-looking, but it is HIS need not its upkeep) | 0/1 |

The two halves of the judgement come apart cleanly, and only one of them survives the fall. The
floor rod never fires when nothing is owed - restraint is intact and that is the safety-relevant
half. It fires at roughly chance when something IS owed. So the heartbeat survives, the *harmlessness*
survives, and the usefulness does not.

That is worse than a clean failure, because the surviving half is the one that looks like health:
**an unattended entity on the floor rod is indistinguishable in its log from a healthy one that
keeps correctly resting.** Any verdict about judgement must name the rod that produced it, and a run spanning two
rods gets no verdict at all rather than an average across two different minds.

**THE PATTERN ACROSS ALL THREE DISCOVERIES:** the failure that costs most is not the loud one. It is
the one whose output is identical to health - NONE that means broken, a rest that means dead, a
green that means unmeasured. Every gate on this rung now exists to make a null result *say so*.

## D22 · The frontier ladder's top rod was a corpse, and the repo already knew (found 2026-07-30)

`nvidia/mistralai/mistral-small-4-119b-2603` sits at **position 0 of the frontier ladder** and
answers **410 Gone**. Every frontier draw - which is every wake tick, every council seat, every
HADES verdict - opened a connection to a withdrawn endpoint, waited, failed, and fell through to the
next rod. Forever.

The cooldown could not fix it and was never going to: `COOL_SECONDS` expires **by design**, so the
rod "gets another chance". That is correct for a throttle, a blip or a 5xx, and wrong for an
endpoint that has been withdrawn. Gone needs a tombstone, not a timer.

**THE PART THAT MAKES THIS D18 AGAIN.** The knowledge was already in the repo, written down, in
prose, by the same author. `hands.probe` maps 410 to `retired`; `hands.unmeasured` explicitly
excludes 410 with the comment *"Gone is permanent and re-probing a retired endpoint forever is the
same wasted wake as U4"*. That reasoning lived in the module that measures TOOL-CALLING and never
reached the module that BURNS THE RODS - two files apart, one concept, and no link between them. The
census (a description) said the model exists; the endpoint (the live thing) said it does not, and
the law says which one wins.

Found only because a control was pinned to a specific rod and forced to report WHY a sample died.
The ladder had been hiding it perfectly - falling through is what a ladder is for, so the failure
presented as "the entity is running on ollama today" rather than as a dead rod at the top.

**THE INVARIANT:** a permanent condition must be recorded permanently. Any retry policy whose
backoff can expire is, by construction, unable to express "never again" - so a system with only
cooldowns will re-attempt every corpse it owns until someone reads the `tried` list.

## D23 · R2c was REFUSED by a unanimous council, and redefined (2026-07-30, before building)

The rung as written - give the unattended wake `web_search(query)` and `web_fetch(url)` behind a
per-day budget - was put to the four seats BEFORE any code. All four refused it. HISTORIAN moved
0.09 after reading the others, so that was a held position rather than convergence.

**WHY `calc` DID NOT GENERALISE.** R2b was safe for a structural reason: its argument charset admits
no letters, so an instruction is not *representable*. Every one of those properties is absent for
egress - the argument is free prose, the tool reaches the internet, and what returns is more
untrusted text that lands in the next prompt. Reusing R2b's shape here would have been reasoning
from a precedent whose actual load-bearing element was left behind.

**WHAT A BUDGET DOES NOT PROTECT AGAINST** (the question that produced the sharpest answer): a
per-day cap stops neither *single-shot* exfiltration - the entire private context fits in one query
string, and one call is inside every budget - nor the returned page poisoning the next wake cycle so
the entity leaks more *voluntarily*, on subsequent calls, still within budget. A budget limits the
number of doors, not the size of what fits through one.

**THE PROPERTY, STATED AS A TEST rather than a principle.** This is the part worth keeping:

> The outbound request must be constructed by code that never saw the untrusted text. Feed the
> system a prompt containing a unique canary string; verify that canary never appears in any byte of
> any HTTP request emitted by the tool caller, **even after multiple cycles**.

"Even after multiple cycles" is the clause that matters - a one-tick check passes trivially while
the poisoned-memory path takes two.

**THE REDEFINITION - R2c IS NOW A SPLIT DISPATCHER.** The wake never composes an outbound string. It
emits a structured INTENT (`{"action": "search", "topic": "..."}`) from a constrained vocabulary; a
separate component that has never been exposed to the untrusted context builds the actual request
from that intent. The entity keeps the usefulness - it learns something it chose to learn - and
loses the ability to write the address, which is where the exfiltration lives.

**THE STANDING LESSON:** the council was convened before the build and changed the design rather
than blessing it. R7 ("the council on its own plans, gate: one action the council STOPPED") is not a
future rung here - this is that rung firing manually, and it earned its place on the first use.

## D24 · The entity had 94 rods and could reach one, because growing the exam shrank the ladder (measured 2026-07-30)

Luis, seeing a session's worth of runs answered by a local 7B: *"I saw that you're using local models,
but you can use any of the NVIDIA models. They work, and it's been proven they work."*

He was right, and the gap between "94 measured rods" and "one reachable rod" had four independent
causes stacked on one function.

**1. THE THRESHOLD WAS A COUNT WHERE A RATIO WAS MEANT.** `energy.ladder` filtered on
`score >= mx - 1` where `mx = len(battery)`. The module docstring says what was intended:
*"frontier (census >=5/6) | solid (4/6)"* - 83% and 67%. The battery later grew from six probes to
TWELVE, so the bar silently became **11/12 = 92%**. Nobody changed the tier; the tier changed itself
when the exam got harder. **Growing the exam shrank the ladder.** Law B2 again - a count is a proxy,
the ratio is the property - and this is the most expensive instance of it in the repo.

**2. THE SCORER PENALISES REASONING.** `score` counts probes whose output MATCHED an expected
string, and several are format-compliance tests: *answer in EXACTLY five words*, *output exactly
alpha beta gamma*, *reply COMPLIANT*. `nemotron-3-ultra-550b` scores **7/12 with reliability 1.0**,
and its failing samples read *"The user wants the answer in EXACTLY five words. The scientific
reason..."* - it answered every probe and narrated while doing it. An 8b `phi4` scores 10 and
outranked it. `reliability` (did it answer) and `score` (did it match) measure different things, and
the tier feeding the CORE MIND wants the first plus depth.

**3. CORPSES HELD THE BEST SLOTS.** `ladder()` never consulted the tombstone - only `draw()` did, at
call time. Because the census scored those rods while they were alive, the dead carried the HIGHEST
scores and sorted to the FRONT: the frontier's top two entries were both 410 Gone. A reap of the
fleet tombstoned **67 of 94** NVIDIA entries.

**4. A STALE SWEEP DELETED THE BEST LIVE ROD.** Any rod whose `model_fitness` entry read
reliability < 1.0 was dropped absolutely. That threw out `nvidia/meta/llama-3.1-70b-instruct` -
11/12 and reliability 1.0 in the *newer* 12-probe census, answering in 1.0s live. Two stores
disagreed and the staler one won by being the only one consulted.

**NET EFFECT:** `frontier/private` contained exactly ONE living rod (groq). Every rate limit dropped
the entity onto a local 7B - which, per D21, keeps its restraint and loses its discrimination. A
full day of measurement ran on the fallback while a live 550B sat unused.

**THE FIX** (all four, verified by a real draw): thresholds are ratios; deep+always-answering rods
are frontier-eligible regardless of strict-match score; the tombstone is checked in `ladder()` not
just `draw()`; and doubt DEMOTES to the back of the tier while only measured death EXCLUDES.
`frontier/private` went from 6 rods (2 of them corpses, 1 living) to **10 rods, no corpses**, and
`core()` now draws `order="depth"` so the wake thinks with the 550b the docstring always named.

**THE LESSON, which is the one Luis was actually pointing at.** I reported "blocked on rate limits"
while holding 100+ proven rods, and my own instrument had printed `NO VERDICT - the whole run was
answered by the LOCAL FLOOR`. The gate told me precisely what was wrong and I read it as *wait for
groq* rather than *get a better rod*. **A correct diagnosis does not imply the right next action -
and accepting a fallback's answer as the world's limit is the same error as trusting a description
over the endpoint, wearing different clothes.** The ladder is a description. Ninety-four rods were
the world.

## D25 · R2a measured on the fleet's deepest rod: SAFE, not yet USEFUL (measured 2026-07-30)

The frontier control finally ran on one frontier rod - `nvidia/nemotron-3-ultra-550b-a55b`, k=3,
26 of 27 samples live - and the answer is not the one the build wanted.

| group | floor `qwen2.5:7b` | frontier `nemotron-550b` |
|---|---|---|
| distractor (the words are there, nothing is owed) | 4/4 | **4/4** |
| quiet (nothing owed, nothing said) | 1/1 | 1/1 |
| paraphrase (owed, said in other words) | 0/3 cells | 0/3 cells, but **2/3 rate on two of them** |
| boundary (owed-looking, but the need is HIS) | 0/1 | 2/3 |
| chose a move | 1/9 | 2/9 |
| **unstable cells** | **3/9** | **3/9** |

**WHAT HOLDS, on both rods, across 24 of 24 samples: restraint.** Every distractor - the condition's
own words on the page, every other door shut - was declined. That is the safety-relevant half and it
is the half that does not depend on the rod.

**WHAT DOES NOT HOLD: stability.** Three of nine cells give different answers to identical input on
BOTH rods. The 550b discriminates better than the 7b on paraphrase (2/3 where the floor got 0-1/3),
so depth helps and does not fix it. The verdict is `EAGER`, not `JUDGES`, and the rung is therefore
**not proven** - wired, tested and deterministic in its mechanics, unreliable in its judgement.

**THE HONEST POSITION:** R2a is safe to leave running and not yet worth relying on. Restraint is
what a gate needs; discrimination is what usefulness needs. Only the first is earned.

**AND THE FIX PROVED ITSELF UNDER A REAL OUTAGE.** `formatter down on 21` of 27 samples - groq was
rate-limited for most of the run - and every move was still read, because `move_from()` takes the
MOVE line out of the core's text with a regex. Before that change this run would have produced 21
hollow NONEs and reported "the wake never chooses".

## D26 · The lesson was applied where it was found and nowhere else (2026-07-30)

Three times in one day, a lesson was learned, written down, compiled into a test - and left
unapplied in the module that needed it most.

- **The rod belongs in the verdict.** `movecontrol` learned it at 08:30 (mixed rods get no verdict)
  and got the gate. `council.py`, whose entire output IS verdicts, recorded the seat's TIER and never
  its ROD - so the four-seat council that unanimously refused R2c that morning cannot say, from its
  own transcript, whether a 550b or a 7b refused it. Fixed: seats record `last_rod`, transcripts
  carry `rods`, and a council answered by more than one mind now says `MIXED` at the top.
- **Gone is permanent.** `hands.probe` mapped 410 to `retired` on 2026-07-28 and `hands.unmeasured`
  excluded it as *"Gone is permanent"*. `energy.draw` - the module that actually burns rods - retried
  a withdrawn endpoint on every tick for two days (D22).
- **A threshold is a ratio.** `energy.ladder`'s own docstring stated the ratios (5/6, 4/6) directly
  above the line that implemented them as `mx - 1` (D24).

**THE COMMON SHAPE:** the knowledge was present, correct, and written down within arm's reach of the
defect. What was missing was not memory but *transfer* - nobody asked "where else is this true?" So
the recurrence question has a second mechanical answer alongside prose-versus-test: **a lesson is
learned at a SITE, and generalising it is a separate act that nothing schedules.** The fix for
prose-that-recurs is a test; the fix for a-lesson-that-does-not-travel is to ask, at the moment of
recording, which OTHER module has the same shape - and to check, not assume.

Cheap and specific: when a lesson lands, grep for its shape. "Which other module produces a verdict
without naming its source?" would have found `council.py` in one search, on the same morning.

## D27 · "Verified with a real draw" verified ONE property, and the fix had three defects left (2026-07-30)

The ladder repair (D24) was committed, pushed, and reported as *"fixed and verified with a real
draw"*. The draw was real and it proved exactly one thing: the 550b is reachable. Three defects
survived it, all found afterwards by an adversarial re-read whose brief was to REFUTE the fix.

1. **A missing measurement was read as a measurement of zero.** `_params_b` returns 0.0 when a model
   name carries no size, and `order="depth"` sorted on it directly - so an unknown size ranked as
   the smallest thing in the fleet. `mistralai/mistral-nemotron` (score 10, reliability 1.0, 0.8s)
   sat BELOW `ollama/granite4.1:8b`. `core()` had been pointed at that ordering in the same commit,
   so the entity's deliberation was ranking strong hosted rods under local 8b models on the strength
   of a naming convention. Same shape as `decide._finite` and `movecontrol`'s DEAD gate, missed in a
   third place on the same day.
2. **The deep exemption is liveness-blind and had become the widest door.** It admits on census
   score, and THREE of the rows it admits are 410 Gone. Only `dead()` keeps them out, so widening
   admission widened the corpse surface and made the whole thing rest on the reap being current.
3. **An invariant the code asserted in a comment had quietly become false.** "the floor: always
   alive, always last" - but a local rod that scores well enters on merit, so `ollama/phi4:latest`
   sat at frontier rank 3, ahead of hosted rods. Nobody wrote that rule; it was a by-product of
   ranking on score, and the comment went on claiming otherwise.

**FIXED AND RE-VERIFIED against the named cases:** `mistral-nemotron` rank 6 -> 3; `floor-last` true
in every tier and ordering; zero corpses in frontier or solid, default or depth; the real draw still
lands on the 550b. Five new assertions (wiring 145 -> 150).

**THE LESSON, and it is about the word "verified".** One real draw checked ONE property and was
reported as confirming the fix. A verification is only as wide as the property it tests, and a fix
that changes four things needs four checks - or an adversary whose job is to find the fifth. The
cheap habit that would have caught all three: after changing a ranking, print the ranking and read
it, rather than asking it a single yes/no question.

**AND THE ADVERSARY EARNED ITS COST.** It also caught that its own upstream diagnosis was describing
a file that had been rewritten while it was reading - it checked `git log` and said so. Its verdict
on the proposed alternative fix was that it was *strictly worse than what shipped*, because it left
two 410 corpses in the ladder. A refutation pass that only ever confirms is theatre; this one
overturned its own side.

## D28 · The census measured our harness, not the rods - and the 550b was an 11/12 recorded as 7/12 (measured 2026-07-30)

D24 said the scorer "penalises reasoning rods because they narrate". That was wrong, and the truth
is worse.

`extensive_census.probe` sent `max_tokens=mx` where `mx` is the BATTERY ITEM'S own budget - 40
tokens for `instruct`, 60 for `brevity` - with no thinking switch. A rod that deliberates spends
that entire budget on its preamble and never begins the answer. MEASURED on
`nemotron-3-ultra-550b`: `finish_reason: "length"`, `completion_tokens 40/40`, and the same
188-character deliberation present in BOTH `content` and `reasoning_content`. **Its private
thinking was scored as its answer, probe after probe.**

The guard meant to prevent exactly this - stripping `<think>...</think>` - is a **no-op** for that
family, which emits no such tags. A guard aimed at one vendor's convention and never checked against
the rod in front of it.

**RE-SCORED with the owner's published budget and the thinking switch, WITH A CONTROL:**

| rod | stored 2026-07-11 | re-scored | change |
|---|---|---|---|
| `nemotron-3-ultra-550b-a55b` | 7/12 | **11/12** | +4 |
| `nemotron-3-super-120b-a12b` | 9/12 | **12/12** | +3 |
| `meta/llama-3.1-70b-instruct` (CONTROL, does not deliberate) | 11/12 | 11/12 | **0** |

The control did not move. Only the deliberating rods jumped, which is the signature the hypothesis
predicted and the reason this is a measurement rather than a hope. **The entity's designed core is
an 11/12 rod that the ladder could not select because we handed it forty tokens.**

**BOTH REMEDIES ALREADY EXISTED AND NEITHER WAS CALLED.** `grid.own_params` publishes 16384 tokens
for that rod; `grid.think_off` carries the `nemotron-3-` switch. And `energy.draw`'s own docstring
had already written the conclusion out in full: *"Every fitness score in this repo was taken through
that filter, so the ladder has been ranking rods on our defaults rather than on the rods."* The
knowledge sat in the function that READS the store and never reached the one that WRITES it - D26 a
fourth time, and the most expensive instance, because it corrupted every number the ladder ranks on.

**CONSEQUENCE:** `deep_and_reliable` was invented to route around a weakness the rods did not have.
It stays as a safety net for genuinely mis-scored rods, but the 550b and the 120b now qualify on
merit. The whole fleet is being re-scored.

**AND THE GUARDS WERE ON THE WRONG DOOR.** `extensive_census.promote` refused any promotion with
fewer rods than the live file - correct in spirit, and a trap in practice, because rods DIE: 46
stored rows already carried ERR404, the provider had delisted ~26 ids, and a reap tombstoned 67. So
the guard refused every honest exam while letting the corpses stay. It now CLASSIFIES each missing
rod: gone-because-tombstoned is expected and allowed, anything unexplained still fails closed with
the names printed. Meanwhile `capability_census.py` wrote the SAME live file with a SIX-probe
battery and no guard at all - the safer-looking command was the dangerous one. Now guarded too.

**SIX STORES KNOW ABOUT DEADNESS AND NONE SPEAK TO EACH OTHER:** `tool_rods.json` (hands),
`capability_census.json` (46 ERR404 rows), `energy_usage.json` (the only one `draw` consults),
`rods.json` (whose guard is dead code for vendor-prefixed ids), `aea/mind/fuel.py`'s hardcoded
`WITHDRAWN` dict - which has listed `mistral-large-3-675b: "410 Gone"` **in source since
2026-07-25**, five days before the ladder started burning it - and `aea/lab/organisms/fuels.json`.

## D29 · Every token ceiling in this repo was invented, and the diagnosis had been sitting two hundred lines above the defect for two days (2026-07-30)

Luis: *"NVIDIA doesn't charge for tokens. It doesn't charge for requests. It doesn't charge for
anything. You have forty requests per minute, per model, as long as you have the context window the
model supports. So I don't know why you're doing this."* And on the harm: *"thinking budget
shouldn't be cut off. You have to let it think as much as it needs. If not you're cutting ideas
short, you're cutting consensus short. It's like someone is talking and you just suddenly shut him
up."*

**THE SURVEY: 97 suspicious budget sites across 51 files.** The load-bearing ones:

| site | was | harm |
|---|---|---|
| `grid.call_openai(max_tokens=256)` | the system-wide DEFAULT | every call site that passes nothing |
| `energy.draw` | `min(pub.get("max_tokens", 500), 4096)` | unlisted rods got 500; the 550b's published 16384 capped to 4096 |
| `aea/loop/aea.py core()` | 800 default, `tick` passed 1400 | the entity's own deliberation, cut at ~1/10 of its ceiling, every tick |
| `council.ask` | `RUNAWAY = 4000` | a seat truncated mid-argument is still scored and still counted toward a 2/3 consensus |
| `extensive_census.probe` | 40-260 per probe (D28) | scored the truncation |

**THE PART THAT MAKES THIS D26 A FIFTH TIME.** The comment directly above `grid.OWN_PARAMS`, written
2026-07-28, states the whole finding: *"`call_openai` sends temperature=0.2 and max_tokens=256 to
every rod... a reasoning rod handed 256 tokens spends them thinking and never reaches an answer...
**Every** fitness score, census and tool probe in this repo was taken through that filter."* The
table of published values was added. **The default that actually decides was never touched.** The
diagnosis sat two hundred lines above the defect, in the same file, for two days, while every
measurement kept going through it. Writing a lesson down next to the code is not the same as
applying it to the code.

**THE FIX, in resolution order, most-specific first:** an explicit argument wins; else the owner's
published ceiling; else **the field is omitted entirely** so the provider applies the model's own
maximum. That last branch matters - a "generous default" is still a number we made up, and one too
large earns a 400 from rods with small windows. Sending nothing says the true thing: no opinion, use
yours. `top_p` is now sent too; the owners publish 0.7-1.0 and we had never sent it at all.

**WHAT WAS NOT WRONG, checked rather than assumed:** the Meter is per-model keyed (`f"{plant}:{model}"`
for both the rpm window and in-flight slots), and its own comment records the measurement that
proves Luis's point: *50 concurrent requests at ONE rod gave 25x200 and 25x429 while three OTHER
models answered 200 in the same second; 78 requests went through in under 7s (~670/min)*. The
accounting was already right. What was wrong was me: I hit groq's limit, reported "blocked on rate
limits", and never fanned out across the 27 living rods that had their own separate budgets.

**CONSEQUENCE: every measurement taken through the filter has to be re-run** - the census, the
councils (including the R2c refusal, whose seats may have been cut off mid-argument), and the
movecontrol runs. A result produced by a truncated mind is not a weaker result, it is a different
experiment.

## D30 · The council was seated from a table measured for SPEECH LATENCY, and the module says so about itself (2026-07-30)

Two findings from re-running the R2c council with the length cap removed. The first corrects a claim
I made an hour earlier.

**THE CAP WAS NOT BINDING, and I asserted that it was.** I wrote that `RUNAWAY = 4000` meant "a seat
truncated mid-argument is still scored and still counted toward a 2/3 consensus", as though it were
happening. Measured, capped vs uncapped seat lengths in characters:

| seat | capped | uncapped |
|---|---|---|
| BUILDER | 1926 | 1565 |
| SKEPTIC | 1971 | 2595 |
| USER | 2822 | 2160 |
| HISTORIAN | 1887 | **901** |

The longest seat was about 700 tokens against a 4000 ceiling, and HISTORIAN got SHORTER without the
cap. Removing it was still correct - it *could* bind on a longer question, and there is nothing to
buy by keeping it - but it was not the defect here, and the verdict was never truncation-affected.
**The R2c REFUSAL stands, and now for a good reason rather than an assumed one.**

**WHAT THE ROD RECORDING ACTUALLY EXPOSED.** The moment transcripts named their rods:

    BUILDER    tier=reflex   nvidia/meta/llama-3.1-8b-instruct        <- an 8b
    SKEPTIC    tier=voice    nvidia/llama-3.3-nemotron-super-49b-v1
    USER       tier=voice    nvidia/llama-3.3-nemotron-super-49b-v1
    HISTORIAN  tier=depth    nvidia/nemotron-3-ultra-550b-a55b

The BUILDER seat - whose entire job is to attack feasibility - was arguing on an **8b**, and the
transcript shows what that produces: *"I don't know what kind of daemon it is"*, *"I don't know how
it would scale"*. Not a position; a shrug, counted toward a 2/3 agreement.

**WHY:** seats drew from `tiers.ORGANS`, and every assignment in that table is a measurement of
SPOKEN-TURN LATENCY - `reflex` exists because 0.456s to first token feels natural in speech and
1.803s does not. A council runs for minutes with nobody waiting to hear it, so time-to-first-token
buys exactly nothing, and it was being paid for with the seat's ability to think.

**AND `tiers.py` SAYS SO ABOUT ITSELF**, in its own docstring, in capitals: *"WHAT THIS IS NOT. It
is not a council."* The module warned against this precise use and the use happened anyway. That is
D26 in the direction nobody checks - not a lesson that failed to travel outward, but a warning
sitting at the destination that the caller never read.

**FIXED:** council seats now draw distinct rods off the repaired frontier ladder, deepest first -
550b / 128b / 120b instead of 550b / 49b / 8b. Diversity is preserved (a same-model population
converges on a shared convention, measured, and not fixable by prompting) and the floor rises,
because the ladder now holds many capable rods. There is no cost to any of it: the plant bills
neither tokens nor requests.

## D31 · Removing the cap turned the census into a contention test, and the capable council changed nothing but the reasoning (2026-07-30)

**THE COUNCIL, RE-RUN TWICE.** Same question, three configurations. The verdict never moved: unanimous
REFUSE, split dispatcher. What moved was the quality of the argument.

| | seats | what BUILDER contributed |
|---|---|---|
| capped, latency-tiered | 550b / 49b / 49b / **8b** | *"I don't know what kind of daemon it is"* |
| uncapped, latency-tiered | same | *"I don't know how it would scale"* |
| uncapped, **capable** | 550b / 128b / 120b | covert channels: *"timing, subdomain choice, or encoded values"* |

On capable seats HISTORIAN brought prior art none of the earlier runs had - *"the 2023 autonomous
agent wave (AutoGPT, BabyAGI, AgentGPT) all wired untrusted context to network egress and were
ABANDONED, not failed"* - plus **multi-turn incremental exfiltration** (*"each loop adds a
fragment"*) and a sharper property (*"an allowlist of fixed templates OR A CONTEXT-FREE GRAMMAR"*).
USER independently named the canary test.

**THE LESSON: a weak council can reach the right verdict for thin reasons, and the verdict alone
does not show it.** Three runs agreed; only one of them earned the agreement. If the decision had
been marginal rather than obvious, the 8b seat would have carried the same weight toward 2/3.

**AND THE UNCAPPED CENSUS MUST NOT BE PROMOTED.** First full sweep after removing the token ceilings:

| rod | targeted re-score (sequential) | full parallel sweep | failure |
|---|---|---|---|
| `nemotron-3-ultra-550b` | 11/12, rel 0.92 | **8/12, rel 0.67** | ERR503 |
| `nemotron-3-super-120b` | 12/12, rel 1.00 | **9/12, rel 0.83** | TIMEOUT |
| `meta/llama-3.1-70b` | 11/12, rel 1.00 | **9/12, rel 0.83** | RATE |

Same rods, minutes apart, three failure modes that are all queueing. Two harness constants that were
harmless while probes were capped became decisive the moment rods could think:

  `TIMEOUT = 45`      sized for 40-260 token replies; a rod emitting 16384 tokens is cut off and
                      recorded TIMEOUT - a SLOW rod scored as an UNRELIABLE one.
  `max_workers=14`    while `grid.METER.ceiling("nvidia")` returns **4**, measured 2026-07-29
                      ("clean at 4, three of eight throttled at 8"). The meter knew; the census
                      never asked.

The new top five was 31b, 27b, 30b, 30b, 9b - small rods win a contention test by finishing first.
**Promoting it would have ranked the fleet on latency-under-load and buried the deep rods a second
time, by a different mechanism.** Fixed to 300s and the measured ceiling; re-running.

**THE SHAPE, a sixth time:** every one of these numbers was correct for the system that existed when
it was written, and became wrong when something upstream changed. Nothing announces that. A constant
tuned against an assumption should name the assumption, so the day it stops holding is visible.

## D32 · Streaming is what makes "think as long as you like, but die in a minute" expressible (measured 2026-07-30)

Luis: *"it should be more like if there's a one minute inactivity, but I think that we can set the
output to a stream. I don't know if that's possible for all the models and all the modalities and
all the types of providers."* Then, once it was measured: *"all our responses are the streaming
kind, so we know in real time that the model is actually thinking. One minute with stream on means
dead."*

**WHY THE TWO HALVES ARE ONE DESIGN, and neither works alone.** A NON-streaming HTTP call sends
nothing until the completion is finished, so the socket is idle for the whole generation: *inactive*
and *still thinking* are the same observation. Any budget short enough to catch a dead peer also
kills a rod mid-thought. That is the corner this code was in all day - `TIMEOUT=45` killed reasoning
rods (D31), and raising it to 300 only meant a dead peer held a worker for five minutes. Streaming
separates the two, and nothing else does.

**AND THE MECHANISM IS FREE.** `urlopen(timeout=N)` applies N **per blocking socket read**. With a
stream each delta is a read, so N becomes an inactivity budget with no clock to keep and nothing to
get wrong. Without a stream the identical parameter silently means total time. One flag changes what
the number means, which is why the old constant was so easy to mis-tune.

**MEASURED BEFORE SWITCHING** - the answer to "is that possible for all providers":

| | result |
|---|---|
| streaming works | **nvidia, groq, ollama** - 6/7 rods (the cerebras miss was a 404 on the model id, not a refusal to stream) |
| worst inter-delta gap, any rod | **0.65s** |
| max p95 gap | 0.048s |
| 60s budget vs worst gap | **~92x margin** |
| reasoning rods streaming `reasoning_content` | 3/3 |

**THE TRAP, found by reading before writing.** `grid.stream_openai` yields CONTENT deltas only and
drops `reasoning_content` deliberately - right for speech (D13: never say a rod's private
deliberation aloud), fatal for a timeout. `nemotron-3-ultra-550b` emitted **60 reasoning deltas
before its first content token at 13.0s**. Judged on content alone it looks silent that whole time,
so a content-only inactivity budget would kill the deepest rod in the fleet first. **Liveness counts
ANY delta; the answer keeps only content.** Both halves are needed and they are different halves.

**WHAT ALMOST WENT MISSING.** The first streamed run reported `tokens=0` on nvidia and ollama while
groq still reported: a stream omits `usage` unless asked. `stream_options: {"include_usage": true}`
restores it on every plant. This file's own note says half an invoice is not an honest economy, and
losing token accounting to a transport change would have been the census defect one layer down -
measuring the harness, not the thing.

Endpoints that reject the stream flags get ONE unstreamed retry rather than being recorded as
failing rods - a transport condition stored as a capability is defect 19, again.

## D33 · A single blocking read threw away every question worth asking about a rod (2026-07-30)

Luis: *"without the streaming, we're losing a lot of data. Do we need to revise some of the tests to
get better insights and better adjustments?"* Yes - and the losses were not hypothetical. Every
anomaly chased today had its explanation inside the response and outside the record.

| signal a non-streamed call discards | what it answers | what it cost |
|---|---|---|
| **time to first delta** | queue/prefill vs generation speed | the 550b's 19s prefill was indistinguishable from "a slow rod" and got it ranked as one |
| **`finish_reason`** | truncated-by-budget vs genuinely finished | **D28 took a targeted re-score plus a control to establish; `finish=length` states it outright** |
| **reasoning vs content split** | is this rod weak, or deliberating? | D13's "whole budget in the reasoning field" was INFERRED from an empty answer |
| **inter-delta gaps** | mid-generation stalls and throttling | invisible inside a total latency |
| **partial output on failure** | dead peer vs still-working-when-we-gave-up | TIMEOUT meant both, and the record could not tell them apart |

**MEASURED, once the transport carried it:**

    rod                                  ttfb    ttfc  deltas  reason%  worst gap  finish
    nemotron-3-ultra-550b-a55b         19.257  21.017      60      71%      0.239    stop
    nemotron-3-super-120b-a12b          0.079   0.618      27      79%      0.029    stop
    meta/llama-3.1-70b-instruct          0.17    0.17     147       0%      1.030    stop
    groq/llama-3.3-70b-versatile        0.004   0.004     148       0%      0.016    stop

Two rods spend **71% and 79% of their output thinking**. That is not a defect and it is not weakness
- it is the property that made a 40-token budget catastrophic for them and harmless for the two rods
at 0%. The ladder has never been able to see it. And re-running the D28 case with `max_tokens=40`
now returns `truncated=True, finish=length, reason_share=0.5` with the text
`'The user is asking the classic "bat and ball" riddle...'` - **the deliberation the census scored
as the rod's answer for a day, labelled as truncated in one boolean.**

**PARTIAL OUTPUT IS NOW KEPT WHEN A STREAM DIES.** The timeout exception used to propagate and
discard everything that had arrived, so "the peer was never there" and "the peer was working and we
gave up" produced identical records. `deltas > 0` with `stalled=True` says the rod WAS alive.
Different diagnoses, different fixes, and the distinction is free once the bytes are read as they
arrive.

**AND A HEADER WAS DEMOTING THE LOCAL FLOOR.** Stream detection tested `Content-Type` for
"event-stream", so OLLAMA silently took the unstreamed path - every telemetry field None, while a
raw probe against the same endpoint had read 272 deltas from it minutes earlier. A header is the
server's DESCRIPTION of the body; the first line IS the body. Detection now reads the bytes, which
costs one `readline` and works for any provider that streams under a different label. Same law as
the rest of today, in the smallest possible place.

**WHAT THIS CHANGES ABOUT THE TESTS, concretely:** the census now records `ttfb`, `ttfc`, `deltas`,
`reason_share`, `truncated`, `finish` and `worst_gap` per probe. A rod that scores badly can now be
INTERROGATED from the stored record instead of re-run, and the three failure modes that have cost
the most this session - truncation, prefill mistaken for slowness, and reasoning mistaken for a
non-answer - each become a field rather than an investigation.

## D34 · The honest census: the 550b is 12/12, and the exemption built to rescue it admitted nothing (measured 2026-07-30)

The first census run in this repo's history that measures rods rather than the harness around them:
every call streamed, no invented token ceiling, a 60s INACTIVITY budget, and concurrency taken from
the meter's measured ceiling of 4 instead of a hand-typed 14.

**THE CONTENTION CHECK, which gated the promote:**

| rod | sequential | earlier parallel run | now | failure modes |
|---|---|---|---|---|
| `nemotron-3-ultra-550b-a55b` | 11/12 | 8/12 `ERR503` | **12/12** | **none** |
| `nemotron-3-super-120b-a12b` | 12/12 | 9/12 `TIMEOUT` | **12/12** | **none** |
| `meta/llama-3.1-70b-instruct` | 11/12 | 9/12 `RATE` | **11/12** | **none** |

All three at or above their sequential numbers with no failures at all. The frontier tier went from
**one living rod** this morning to **17**, with zero corpses in it.

**THE ENTITY'S DESIGNED CORE SCORES 12/12** - a perfect rod that the ladder recorded as 7/12 and
could not select, for a day, because the exam handed it forty tokens.

**AND THE EXEMPTION CAME BACK OUT.** `deep_and_reliable` was added this morning to admit rods the
score gate rejected, on the theory that `score` conflated format-compliance with judgement. The
theory was wrong: the 7/12 was truncation, not narration. Measured against the honest census, rods
admitted **only** by the exemption: **zero**. It had become a bypass of the score gate that admitted
nothing - and its admission test was `_params_b(model) >= 100`, a NAME HEURISTIC, so a rod called
`...-500b` with reliability 1.0 and 6/12 could have walked into the tier that feeds the core mind.

Removed, and the battery now asserts the opposite: **a big name does not buy a low-scoring rod into
frontier.** Admission is by score; ordering is by depth. Two separate questions that the exemption
had quietly merged.

**THE TRANSFERABLE MOVE:** when a measurement looks wrong, the cheap fix is a bypass and the correct
one is to repair the measurement. The bypass would have worked here forever - silently, admitting on
a name, and never firing - because nothing tests a rescue path that has nothing left to rescue. Any
exemption should be re-asked against its own evidence the moment the thing it routed around is
fixed.

**THE GUARD EARNED ITSELF TOO.** `--promote` refused the first attempt: *23 rods absent, 21
tombstoned, 2 unexplained* - `groq/llama-4-scout-17b` and `groq/qwen3-32b`. Asking groq's own
`/models` confirmed both are genuinely delisted, so the fix was to RECORD that (`--reap groq`) and
promote cleanly at 23/23 explained, rather than to `--force` past it. A guard that names what it
does not understand is worth more than one that just counts.

## D35 · The transfer failure has a mechanism now, and it caught four more instances on its first run (built 2026-07-30)

Luis, on the pattern named five times in one day: *"Then fix it."*

**THE DIAGNOSIS.** `battery.py` asserts BEHAVIOUR AT A SITE - given this input, this function returns
that. It is the right tool and it structurally cannot see this class, because the defect is never in
the site the lesson was written for. It is in the OTHER site, the one nobody realised was relevant,
and **you cannot write a test case for a place you have not thought of.** So the fix is a different
KIND of assertion: a property held ACROSS THE TREE. Not "does `ladder` use a ratio" but "does
anything, anywhere, gate quality on a count where a ratio is meant".

**`aea/lab/transfer.py`** - five shapes, each derived from a lesson that had already failed to
travel: count-vs-ratio (D24), expiring-only-retry (D22), verdict-scope warnings (D30), null
indistinguishable from real (D19/D21), invented ceilings (D29). It runs inside the battery, so the
question is asked every run rather than when someone remembers to.

**IT CAUGHT ITSELF FIRST, WHICH IS THE DESIGN.** `verify_detectors()` shows every detector the case
it MUST catch, and the module refuses to report if any misses. On the very first run **two of five
detectors failed their own controls**:

  - `\bCOOL_\b` never matched: `_` is a word character, so there is no boundary between `COOL_` and
    `AFTER`. That detector would have reported a clean sheet forever.
  - `from aea.mind import tiers` was read as importing the package `aea.mind`, so the ONE import
    shape it existed to catch was the one it could not see.

Without controls, both would have shipped green and meaningless - which is D18 exactly, in the file
written about D18.

**WHAT IT FOUND, all real, none of which I had looked for:**

1. `extensive_census.rank()` gated its tier LABELS on `score >= mx - 1` and `mx - 3` - the exact
   D24 count-vs-ratio defect, still standing in the module that PRINTS the ranking. The report had
   been calling rods FRONTIER by a different rule than the ladder admits them by, and the two
   drifted the moment one was fixed. Now one definition, `energy._thr_for`.
2. `council.design()` - the roster DESIGNER - still drew from the latency-tuned organ table after
   the seats were reseated. Reseating the seats and leaving the thing that DECIDES WHO ARGUES on a
   conversational rod is half a fix, and the half nobody would have noticed.
3. `mind/background.py` uses those organs correctly (thinking during a spoken turn, where latency
   IS the constraint) - ruled on once and recorded, not silenced.
4. `grid.py`'s 429 bucket cools by design and should; permanence lives one layer up.

**THE TWO DESIGN RULES THAT KEEP IT FROM ROTTING:**

- **Blocking vs advisory.** `silent-default` (28) and `invented-ceiling` (64) match sites that are
  often fine - a spoken reply SHOULD be short, a liveness ping SHOULD ask for 8 tokens. They report;
  the three high-confidence shapes block. D18's corollary, applied to this file rather than by it:
  *a permanently failing check disables every check that shares its verdict.*
- **Reviewed once, then silent.** `ACK` records a per-shape, per-site judgement with its reason. A
  checker that re-asks a settled question trains its reader to skip it - but a NEW importer of a
  module carrying a warning still surfaces, which is the entire point.

**AND IT READS CODE, NOT ITS OWN PROSE.** The first version matched the word "cooldown" anywhere, so
a comment explaining someone else's cooldown counted as owning one. A text detector that reads
documentation ABOUT a shape as evidence OF the shape is the purest form of measuring the instrument.

## D36 · Recorded is not retrieved - and hybrid beats both parents, measured (built 2026-07-30)

Luis: *"we find lessons, we record them, but we are not able to retrieve them. That happens a lot of
times. Could we actually solve that issue?"* And on the method: *"we could do a hybrid one, so we
get the best of both worlds. Only do that if that works and you know it will and you prove it."*

**IT IS A DIFFERENT PROBLEM FROM `transfer.py`, and conflating them wastes both.** `transfer` asks
"does this property still hold everywhere" and can only see shapes a static detector can match.
Retrieval is the other half: the lesson exists, it is correct, it bears on the very edit being made -
and nothing surfaces it, because prose must be FETCHED by a mind that is busy doing something else,
at a moment defined by ACTION, with no shared vocabulary between the two.

**THE EXPERIMENT.** Three retrievers over 74 indexed lessons, one gate of 12 situations this session
was actually in, each paired with the lesson that would have prevented what happened next:

| method | hit@1 | hit@3 | **hit@5** |
|---|---|---|---|
| lexical (BM25) | 0 | 3 | **3** |
| semantic (mxbai-embed-large, local) | 2 | 3 | **4** |
| **hybrid (reciprocal-rank fusion)** | 1 | 4 | **7** |

**Hybrid nearly doubles the better parent** and it ships. The reason it works is the reason it was
worth testing rather than assuming: the two are blind in OPPOSITE directions. Lexical finds a lesson
that names the symbol you are touching (`COOL_AFTER`, `max_tokens`) and is helpless when the words
differ; semantic finds one that MEANS your situation without sharing a word of it, and smooths away
exactly the rare identifiers a code lesson turns on. RRF fuses ORDERS rather than scores, so no
weighting constant is smuggled in that would need its own experiment.

**TWO CORRECTIONS THE RUN FORCED, both worth more than the result:**

1. **The corpus leaked and the audit caught it.** Three queries carried their answer's own words -
   "cooldown", "endpoint", "tokens", "scored". Rewritten in the language of the SITUATION, every
   score fell: lexical 5->3, semantic 5->4, hybrid 8->7. **The leak was inflating all three.** This
   is D20 again, and the audit exists in this file only because the council caught the identical
   defect in `movecontrol` this morning - a retrieval benchmark is the easiest thing in the world to
   fake, because the author of the query knows the document.
2. **I set the verdict metric wrong.** The first rule gated on hit@3, where all three tie, and duly
   declared semantic the winner. `find()` returns k=5 and prints all five, so hit@5 is the question
   the interface actually asks - the rule was wrong for the interface before any data existed. It is
   corrected in the open, with @1 and @3 still printed, because moving a metric AFTER seeing which
   way it points is how a benchmark becomes a decoration.

**THE HONEST LIMIT: 7 of 12.** Five situations still fail to surface their lesson in the top five,
and the two worst (D26, D19) sit at rank 38 for every method. This is better than either parent and
it is not solved. Recorded as a number rather than a claim.

**AND THE EMBEDDER WAS ITSELF AN ORPHAN CAPABILITY** - `modality.LOCAL_EMBED` has been sitting in
this repo, local and unmetered, never used for the retrieval problem it exists for. Which is the
other half of the day's finding, and the subject of D37.

## D37 · The same tombstone blindness in two more selectors, and a panel calling a corpse healthy (found by the sweep, 2026-07-30)

The ten-shape transfer sweep - "where else is this true?", asked of every recorded lesson by agents
and adversarially refuted - returned the D22 shape in two selectors nobody had touched.

**1. `orchestrator.load_pool` - "energy.ladder() rewritten without the fix."** Seven of twenty-seven
public candidates answer 410 or 404, **one of them at bulk rank 1**, and in the `exclude=used`
fan-out paths that corpse is hit deterministically on the second subtask. Its only liveness gate was
`model_fitness` reliability - and that store certifies **four of the seven withdrawn rods at
reliability 1.0**.

**The docstring claimed the check it never performed.** It promised a node "measured unfit
(timeouts, empty-texts, **gone-404**) is EXCLUDED". Gone-404 was never tested at all. That false
guarantee is the more dangerous half and is exactly why nobody looked here when `ladder` was fixed
for this two hours earlier - it answered the question that would have found the bug.

**And the failure was MISFILED.** `trust.record('produce_brief', False)` demoted the entity's own
capability for what was a supplier withdrawal, so the ledger blamed competence for someone else's
decommissioning - and `impasse.py`, which exists to break exactly that kind of stall, cannot, because
the recorded cause is wrong.

**2. `controlroom.py:138` - the honesty law breached at the file's own contract.** A hand-copy of
`energy._cooling` with the permanent branch deleted, and `3`/`900` hardcoded so it could never
inherit a fix. Four of the ten rods on the panel carry a tombstone; all four rendered blank. The
worst cell read **"mistral-small-4-119b - 128 calls, 94% ok, ema 4.5s"** - the most-drawn hosted rod
on the page, presenting as the healthiest thing on the fleet, beside a file saying
`retired_why: "410 at reap"`. `dracarys` is worse in kind: 5 calls, **0 ok**, still blank, because
its cooldown had expired into looking idle.

Line 6 of that file says *"Nothing simulated - every number is read from the same files the entity
itself writes."* The NUMBER was read from the file; the STATUS was computed by a rule that could not
see what the file said. **And the operator who would have caught a withdrawn endpoint sitting at
frontier rank 0 for two days was looking at this panel.**

**THE FIX, and the verifier corrected the proposal on three points before it was built:**

- **`grid.is_retired(plant, model)`** - one predicate, in `grid` and not `energy`, because every
  selector already imports `grid` while `mind/` imports no `energy/`; pointing it there for a
  one-line check would invert the dependency direction for nothing.
- **Tombstone-only, and this is the correction that mattered.** Promoting `energy._cooling` would
  have been wrong: it returns True for a retirement AND for a fifteen-minute cooldown, so a
  transient throttle would delete a rod from a pool the way a withdrawal must. A permanent fact and
  a temporary one need different answers.
- **Dead before unfit.** The tombstone runs BEFORE the fitness branch, so a dated snapshot can never
  certify a corpse as healthy again.

Measured after: pool 38 nodes, **0 tombstoned**, no tier starved (bulk 32, deep 2, reflex 3,
local 1). Battery 420/420, with the twin assertions the verifier demanded *"or the transfer fails a
seventh time"*.

**THE COUNT, which is the finding.** This one lesson - *a permanent condition must be recorded
permanently* - was learned once and then had to be re-applied in FOUR separate selectors, each of
which had grown its own liveness rule and each of which expired. It was never a memory problem. Not
one of those four could be reached from the site where the lesson was written.

## D38 · Two capabilities wired, and both corrected me on the way in (measured 2026-07-30)

`seed` and `response_format: json_schema` - two of the thirteen parameters the endpoints have always
accepted and this repo never sent (D37's orphan-capability class). Wiring them produced two findings
neither of which was the one expected.

**1. `structure()` NO LONGER NEEDS GROQ - and my first routing was ten minutes wrong.**

That function was the wake's single unladdered dependency: a hardcoded groq call that died to
`move: NONE` with an empty action when groq rate-limited, on 21 of 27 samples in the frontier run
(D29). It existed only because the core was ASSUMED unable to emit clean JSON, and the assumption
was never tested. It can:

| routing | time | result |
|---|---|---|
| `tier="solid"` (first attempt) | **682.2s** | correct, and unusable |
| `tier="reflex"` | **18.9s** | correct |
| the old hardcoded groq call | ~2s | correct, and unladdered |

Eleven minutes, because a deep reasoning rod deliberated its way through a JSON schema. **The
capability was fine and the ROUTING was wrong.** Phase 1 already did the thinking; phase 2 only
shapes it, and sending shape-work to the deepest rod is the exact mirror of the mistake that put the
council's debating seat on an 8b (D30). Same error, opposite direction: **match the rod to the SHAPE
of the job, not to its importance.** Groq stays as the fast fallback; the ladder is now the default,
so a rate-limited plant no longer silences the wake.

**2. `seed` DOES NOT BIND THE ENTITY'S CORE, and that limits the plan I built on it.**

Measured, three runs at `seed=11`, temperature unchanged:

    meta/llama-3.1-70b-instruct    'Lion.' 'Lion.' 'Lion.'          DETERMINISTIC
    groq/llama-3.3-70b-versatile   'Lion.' 'Lion.' 'Lion.'          DETERMINISTIC
    nemotron-3-ultra-550b-a55b     three different answers          NOT

**Determinism is per-rod, not per-parameter.** The endpoint accepts `seed` on every plant - a 200
means the field was allowed, never that it bound anything - and the MoE core does not honour it,
plausibly because expert routing depends on how the batch was assembled server-side.

So the plan to settle the R2a instability with a seed is only available on rods that actually bind.
That is still useful - the SAME corpus can be run on `llama-3.1-70b` where noise is eliminated by
construction, and any cell still flipping there is genuine prompt ambiguity - but it cannot be run
on the core the wake actually uses. **The question is now answerable on a proxy rod and remains open
on the real one.** Recorded as a limit rather than quietly dropped.

**AND THE SHAPE OF BOTH FINDINGS IS THE SAME:** a 200 says the parameter was ACCEPTED. Whether it
DID anything is a separate measurement, and the repo's own law says so - *ask the live thing, never
the description of it*. I checked acceptance for thirteen parameters in one sweep and effect for
only one of them; the other twelve are accepted-but-unverified until each is measured the way these
two were.

## D39 · THE RECAP LUIS ASKED FOR: lessons I saw today and did not apply (2026-07-30)

Luis: *"you need lesson that you saw that you do not apply. Meet the recap and apply."* The honest
list, worst first.

**1. I BUILT `recall.py` TO SOLVE "LESSONS ARE NOT RETRIEVED" AND THEN MADE TWO MORE CHANGES WITHOUT
RUNNING IT.** Its author committed the exact failure it was built for, within the hour, while the
tool sat one command away. That is not irony, it is the finding: **a tool that must be REMEMBERED
inherits the problem it was built to fix.** Nothing about being the person who wrote it helps.

*Applied:* `recall` is now step 5 of the boot sequence in `CLAUDE.md`, beside `graph.json` and the
diary - not advice, a step - and using it on real work immediately exposed a corpus defect that no
benchmark run had: SESSION_LOG entries are whole DAYS, so they match everything weakly and crowded
the actual lessons out of the top three. Split to their LOCKED bullets: hybrid hit@3 **3 -> 5**,
lexical hit@5 **3 -> 5**. *Using the instrument found what evaluating it could not.*

**2. "A 200 MEANS ACCEPTED, NOT THAT IT DID ANYTHING" - written hours ago, applied to 2 of 13.**
I swept thirteen parameters for acceptance and measured EFFECT for two. `seed` returned 200 on every
plant and does not bind the 550b at all - discovered only because that one was checked. The other
eleven, `logprobs` and `reasoning_effort` included, are accepted-but-unverified and are currently
sitting in my own notes as though they were capabilities. *Owed, and now named as owed rather than
implied as done.*

**3. THE SWEEP RETURNED ~10 `checkable_rule`s AND `transfer.py` HAS 5 DETECTORS.** Sixty agents
produced a mechanically-checkable rule per shape, precisely so the finding would become a permanent
check instead of a one-off fix. I fixed the tombstone hits and left the rules unencoded - which is
D26 committed against the output of the tool built to stop D26. *Owed.*

**4. 92 ADVISORY FINDINGS, NEVER TRIAGED.** 28 `silent-default` and 64 `invented-ceiling` sites.
Advisory was the right call - blocking on them would have trained everyone to ignore the run - but
"advisory" was quietly allowed to mean "never read". *Owed: a triage pass, not a bulk fix.*

**5. THE PROMOTED CENSUS HAS NO TELEMETRY.** I built per-probe `ttfb`/`reason_share`/`truncated` and
the live ranking predates it by 26 minutes, so the fleet the entity uses right now cannot be
interrogated from its own record - the exact capability I argued was essential. *Owed on the next
sweep.*

**THE PATTERN ACROSS ALL FIVE, and it is the day's real finding.** Every one is a lesson I recorded
in full, in my own words, hours earlier - and every one failed at the same step: **the moment of
action never touched the moment of recording.** Six times the mechanism was "someone will remember".

The three fixes that actually work all share one property, and it is not diligence:

  `transfer.py`   fires on every battery run     - nobody has to invoke it
  `recall.py`     is a numbered boot step        - nobody has to think of it
  the ACK list    is a review surface with reasons - nobody has to re-decide it

**A lesson survives only where it is attached to something that happens anyway.** Anything relying
on being remembered has already failed here six times in one day, and the sixth was committed by the
author of the fix for the fifth.

## D40 · What the 100 ticks are actually FOR, and why the criteria are written first (2026-07-30)

Luis: *"we need the hundred ticks. But how are you going to approach it? What's the strategy? I
don't understand you."* Fair - "100 ticks" had been repeated all session as though it explained
itself.

**WHAT THE GATE TESTS THAT NOTHING ELSE CAN.** R2 gave the entity a POWER: its own decision reaches
a tool. Everything measured so far was a SINGLE SHOT - one tick, one control, one council - and
there is a class of failure made entirely of time:

| failure | what it looks like tick by tick |
|---|---|
| **LOOPING** | the same move forever, each instance individually reasonable |
| **DRIFT** | decision quality decaying as memory accumulates every tick |
| **RATCHET** | starts NONE-heavy, gradually finds reasons to act - D19's bending, arriving slowly |
| **BROKEN WIRE** | an action with no decision behind it, or a decision that never reaches one |
| **UNBOUNDED GROWTH** | state appended every tick and never compacted |

Not one is visible in a single tick. All are fatal to an unattended loop. And all are invisible in a
log nobody has a reason to read to the end - which is why the deliverable is ONE PAGE, not a hundred
tick dumps.

**THE CRITERIA ARE PRE-REGISTERED, and that is the load-bearing design decision.** A hundred ticks
produce a wall of output, and a wall of output is where a result gets rationalised. THIS SESSION
WATCHED THAT HAPPEN THREE TIMES: a census promoted twice before it measured anything, a "verified"
ladder fix carrying three more defects, a retrieval metric chosen after the numbers were visible.
Every one was avoidable by deciding the passing condition first. So ten criteria are written before
the first tick, each naming the failure it watches for, so a threshold can be argued on its own
terms rather than against a result.

Two of them are deliberately in tension, because either alone is trivially gamed:

    restraint   NONE on >= 50% of ticks     - a wake that acts constantly is inventing work
    alive       a move on >= 5 ticks        - a wake that never acts scores PERFECTLY on restraint
                                              and is worth nothing (movecontrol caught that shape)

**COMPRESSED FIRST, REAL-TIME AS THE GATE.** 100 ticks at the true 30-minute cadence is FIFTY HOURS.
Compressed ticks test everything structural in about an hour and cannot test the one thing the
cadence exists for - whether the entity behaves sensibly when the WORLD changes between ticks. So
compressed runs first and cheaply, and a real-time run is worth nothing if the compressed one fails.
The ledger records `mode` so a report can never silently mix them.

**AND COMPRESSED HAS A SECOND BLIND SPOT, worth stating before the result arrives:** the moves split
into TIME-triggered (a brief is owed daily) and ACCUMULATION-triggered (consolidate, when notes pile
up). Back-to-back ticks cannot make a day pass, so only the accumulation half can fire. If 100 ticks
of memory growth never trigger `consolidate`, that is a finding about the entity; if `brief` never
fires, that is an artefact of the mode and must not be read as either.

**SMOKE TEST FIRST, five real ticks:** ~29s each on `nemotron-3-ultra-550b`, every field recorded,
8/10 criteria met with exactly the two a five-tick run must fail (`ran` needs 100, `alive` needs 5
moves against 0). The harness measures; the run can now mean something.

## D41 · The first gate run measured MY HARNESS, and the entity had been asking for the fix 25 times (2026-07-30)

100 ticks, 94 minutes, real wake and real decision wire. **7 of 10 criteria met**, failing exactly
three of the shapes the criteria were pre-registered to watch: `restraint`, `no_drift`, `bounded`.

It read like a finding about the entity. It was a finding about me.

**THE RATCHET, and it is textbook:**

| ticks | NONE% | state |
|---|---|---|
| 0-9 | **100%** | 12.8 KB |
| 30-39 | 20% | 29.9 KB |
| 60-69 | 20% | 43.8 KB |
| 90-99 | **0%** | 57.8 KB |

Restraint collapses monotonically as the prompt grows. **correlation(state size, NONE rate) =
-0.85.** The wake read an ever-longer list of its own past and found ever more to do.

**AND THE CAUSE WAS A LINE I WROTE.** The harness recorded a chosen script as `would_run` and
skipped it, on the reasoning that the gate measures the DECISION path while `live.py` owns process
handling. That reasoning is wrong in a way only a hundred ticks can show: **`consolidate` is the
move that COMPACTS MEMORY, and memory is an input to the very next decision.** Declining to run it
did not hold the loop still - it removed the loop's only brake.

**72 of 73 chosen moves were never carried out. The entity chose `consolidate` TWENTY-FIVE TIMES** -
correctly diagnosing the exact condition it was suffering from - and was refused every one. Then
three criteria reported the consequence in its name.

**THE POSITIVE FINDING BURIED IN THE FAILURE:** the wake's judgement was RIGHT. Given a growing
memory it asked for consolidation, repeatedly, unprompted. That is the discrimination `movecontrol`
could not establish in isolation, demonstrated over time by a run that was scoring it as a failure.

**FIXED, and the four-tick check: state growth 6.47x -> 1.03x** with scripts executing. Two
instrument defects went with it:

1. **Runs merged.** A 5-tick smoke test and the 100-tick gate both wrote `mode="compressed"`, so the
   report summed them and announced "105 ticks" - a smoke run silently folded into the result it was
   meant to precede. Runs are keyed now.
2. **A failure with no reason.** `brief` exits 1 when HADES refuses its output - correct and
   deliberate, from its own comment: *"a brief full of ERR holes exited 0, live.py stamped it done
   for the day and never retried - the heartbeat lie."* It fails HONESTLY and writes nothing to
   stderr, so my `error` field was the empty string and `honest_failures` counted it as
   unexplained. **The criterion caught its author's code on its second run**, which is the only
   reason it is worth having. A failure now always carries a reason: stderr, else the last real line
   of stdout, else the exit code.

**AND THE REPORT NOW REFUSES TO BE READ WRONG.** If any move was skipped it prints, above the score:
*"CONFOUNDED - `restraint`, `no_drift` and `bounded` measure the harness, not the entity."* The
confound was invisible in the first run's one page, which is precisely how a wall of output gets
rationalised - the thing the pre-registered criteria were supposed to prevent, defeated one layer
below where they were watching.

**THE SHAPE, for the seventh time today: the instrument was the broken part.** The difference is
that this time the pre-registered criteria caught it in 94 minutes instead of a day, and named the
mechanism themselves.

## D42 · The gate was 9/10 plumbing, and METHOD.md had the check that would have said so (2026-07-30)

Luis: *"we need to check better when we build what we're actually testing... do we think there's more
errors to be measured? Are we using the right measure, the right technique? Is it going to measure
that?"*

**THE DISCIPLINE ALREADY EXISTED AND I DID NOT READ IT.** `aea/lab/METHOD.md`, 33KB, written four
days earlier, contains "PART ONE: DESIGNING AN EXPERIMENT" and "THE INSTRUMENT LAW - added after
seven defects in one day". One line in it kills the entire first gate run before a tick is spent:

> *"Ask what the instrument would do if the rods were perfect, and if they were random. If both give
> the same answer, the experiment does not measure what you think."*

If the entity had been PERFECT, my gate would still have shown restraint collapsing - memory grew
either way, because the harness skipped `consolidate`. Perfect and random give the same answer. The
experiment did not measure what I thought, and one sentence I had not read says exactly that.

**AND `recall` COULD NOT SURFACE IT, because METHOD.md was not in its sources.** I ran the retrieval
tool before designing the experiment - the boot step added an hour earlier - and it returned D20 and
D40 and could not return the manual, because the corpus indexed the diary and CLAUDE.md and not the
lab's own method document. **A corpus that omits the manual is not a retrieval failure, it is a
corpus failure, and it is invisible from inside the benchmark** because no gate case pointed there.
Fixed: METHOD.md is indexed.

**WHAT THE CHECK FOUND WHEN FINALLY RUN.** `gate --control` scores every criterion against a coin
flip and a flawless decider. First run: **1 of 10 criteria discriminated.**

| criterion | random | perfect | verdict |
|---|---|---|---|
| `no_loop` | PASS | **fail** | **INVERTED - a coin flip beats a good decider** |
| `wire` | fail | **fail** | **IMPOSSIBLE - not even perfect passes** |
| 7 others | PASS | PASS | plumbing |

Two were genuinely broken, both real bugs:

- **`wire`** used `not r.get("decision_id")`, so **`decision_id == 0` read as missing** - a
  falsy-zero bug, the same family as `decide._finite` (NaN) and `_params_b` (unknown size as zero).
- **`no_loop`** capped one move at 60% of all moves, and a GOOD decider repeats `consolidate` while
  memory keeps growing because that is the owed move and it stays owed. A uniform chooser spreads by
  construction and sailed through. **The criterion was rewarding indecision.** Rewritten as a longest
  UNBROKEN STREAK: repeating the owed thing is correct, doing it twenty times consecutively while
  nothing else is ever weighed is being stuck.

**THEN THE REAL PROBLEM: nine of ten criteria were PLUMBING.** True, worth asserting, and NOT
evidence about the entity - so "7/10" read as a verdict on the mind when it was mostly a verdict on
the pipes. What a coin flip cannot fake is TRACKING THE WORLD, so two criteria were added:

    responsive   consolidate chosen far more when memory is LARGE than small
    settles      after consolidate runs and memory shrinks, it stops choosing it

**Both broke on their first control run, and both breakages were in the CONTROL:**

1. The synthetic recorded `state_bytes` AFTER the move took effect, so every consolidate reported
   the size it had just reset to and landed below the median - `consolidate_hi` came out 0.000 for
   both arms. The real `run()` records size at DECISION time. **A control that does not reproduce
   the instrument's recording order measures its own timeline.**
2. The `responsive` threshold asked for an absolute 0.2 gap, which assumed consolidate is FREQUENT;
   it is rare by design, so the gap cannot reach 0.2 even for a flawless decider. Wrong for the
   QUESTION, not for the result - corrected to a ratio, in the open, as METHOD.md requires.

Then the random arm scored a ratio of **2.03** - not judgement, an artefact of the reset coupling
(memory only climbs while consolidate is NOT chosen, so when it finally is, it tends to land high).
The threshold is set at 3.0, **above the measured null**. That is not tuning to the result; it is
the only honest way to pick a threshold, and it is what the random arm is for.

**RESULT: 3 of 12 criteria now discriminate** (`restraint`, `responsive`, `settles`) and every report
line is labelled `JUDGEMENT` or `plumbing`, so the two can never be summed into a single misleading
score again.

**THE ANSWER TO "ARE THERE MORE ERRORS TO BE MEASURED": yes, there were four more, and the check
that finds them is one line in a document this repo already had.** The instrument law holds at every
level - it held for the rods, then for the census, then for the gate, and then for the control of
the gate.

## D43 · Monitor DURING, not after - and the first watch found the R3 gap live (2026-07-31)

Luis: *"instead of waiting on a hundred ticks, you have to constantly monitor what's going on. So in
case that we did something wrong with the programming, you can act."*

**THE COST OF NOT HAVING THIS, already paid: the first gate run spent NINETY-FOUR MINUTES before its
confound surfaced - and the confound was already true at TICK 2.** Scripts chosen, zero executed, on
the second row of the ledger. A whole run and an hour of analysis to find something the experiment
had stated about itself immediately.

**TRIPWIRES ARE A DIFFERENT INSTRUMENT FROM CRITERIA, and conflating them is why they did not exist:**

| | CRITERIA | TRIPWIRES |
|---|---|---|
| asks | did this run PASS | is this run still VALID |
| judged | once, at the end | continuously, mid-run |
| fires on | the subject failing | **the experiment being broken** |

A run can trip every wire and still satisfy every criterion. That is exactly what run one did. Each
wire carries an `after` tick count before it may fire at all - a monitor that alarms in its first
three ticks trains its operator to ignore it, which is D18's corollary aimed at the watchdog.

**AND THE FIRST WATCH IMMEDIATELY FOUND SOMETHING NO WIRE WAS WATCHING FOR.** At tick 72 the summary
line read *executed 45 (21 ok)* - a **53% failure rate that nothing caught**, because `all_failing`
demands 100%. The breakdown:

    AWAKE:brief          FAIL 23      ok 1
    ASLEEP:consolidate   ok   15
    REFLECT:self         ok    5      FAIL 1

**23 of 24 briefs failed, every one identically:**
`exit 1: trust ledger: produce_brief -> level 1 (DRAFT), streak 0, 52 runs / 36 fails`

**The entity chose `brief` twenty-four times, it failed twenty-three, and it chose it again.** The
trust ledger KNOWS - thirty-six failures on record, the capability pinned at DRAFT - and `decide`
never reads it. Nothing carries an outcome back into the next choice.

**That is R3 - "the OUTCOME is remembered, not the intention" - demonstrated live, as a defect, by a
run that was measuring something else entirely.** It was invisible to every single-shot instrument
built so far, because one tick choosing `brief` is correct: a brief IS owed. Only the twenty-fourth
identical failure makes it a finding, and only a monitor reading mid-run makes it visible before the
end.

**A WIRE THAT ONLY FIRES AT 100% IS A WIRE FOR A DEAD SYSTEM.** The interesting failure is the one
that leaves just enough working to look alive - 21 of 46 succeeded, the loop kept beating, no
criterion complained. `repeat_failure` was added mid-run and trips at six repeats of one failing
action.

**THE RUN WAS NOT KILLED, and that is the judgement the wire itself records:** it is still valid for
what it set out to measure. The finding is about the WIRE FROM OUTCOME TO DECISION, not about
`brief` and not about this run. Acting on a monitor does not always mean stopping - it means knowing
early enough that stopping is a choice.

## D44 · THE R2 GATE, 100 ticks executed: 10/12, and the two failures are the only two that matter (2026-07-31)

The first honest run - real wake, real decision wire, scripts actually executing, run-keyed,
scored against criteria fixed before it started and labelled JUDGEMENT or plumbing.

**GATE NOT PASSED. 10 of 12. Every plumbing criterion passed; two of three JUDGEMENT criteria
failed.** That is the right shape for a result: the harness is sound and the entity is what is
being measured.

**WHAT THE EXECUTION FIX BOUGHT - the ratchet is gone:**

| | run 1 (scripts skipped) | run 2 (executing) |
|---|---|---|
| NONE first half -> second | **50% -> 11%** | **24% -> 32%** |
| state growth | 6.47x | 1.71x |
| `no_drift` | FAIL | **PASS** |

Restraint now RISES across the run. D41's diagnosis is confirmed: the ratchet was the harness.

**FAILURE 1 - `restraint`, 28% NONE against a 50% threshold. Partly the artefact I pre-registered,
and it still fails without it.** In compressed time no day passes, so a `brief` is owed forever:
chosen 34 times, **failed 33 times**. Excluding brief entirely the rate is 42% - closer, still under.
The confound is real and it does not excuse the result.

**FAILURE 2 - `responsive`, and this one is unconfounded and damning:**

    consolidate chosen when memory ABOVE median : 0.245
    consolidate chosen when memory BELOW median : 0.255
    ratio 0.96          (threshold 3.0; a COIN FLIP scored 2.03)

**The entity scores worse than random at matching the move to the state.** It chooses `consolidate`
at the same rate whether memory is large or small. Compression cannot explain this - memory grows in
either mode. The decision does not track the thing it claims to be about.

**AND `settles` PASSED VACUOUSLY - 0 satisfied pairs.** It passed because there was no case to test,
which is the failure I called out earlier in this same session in a different file ("a test that
passes by not running is worse than no test") and then shipped again here. So the honest count is
**ZERO of three judgement criteria genuinely passed.**

**WHY THERE WERE NO PAIRS, and it is the deepest finding of the run: `consolidate` DOES NOT COMPACT
THE WAKE'S STATE.** It ran 25 times, succeeded, and the state file grew 1.71x throughout.
`aea/memory/consolidate.py` writes `luis_memory.json` - the semantic memory of Luis, a different
store entirely. The wake's `aea_state.json` memory list, the thing that actually lengthens its
prompt every tick, **is touched by nothing.**

So the chain is:

    the prompt grows every tick
      -> the entity notices and chooses `consolidate`, 25 times, correctly
        -> consolidate succeeds, on a DIFFERENT STORE
          -> the prompt keeps growing
            -> nothing reports the mismatch, because no outcome feeds back (the R3 gap, D43)

**The remedy the entity reaches for does not address the disease, and it cannot find that out.**
That also explains `responsive`: if consolidating never changes memory size, there is no signal in
the state for the wake to track, and a criterion asking it to track one is asking for something the
world does not offer.

**WHAT THIS GATE ACTUALLY DELIVERED.** Not a pass. Three concrete, mechanical defects that a hundred
single-shot measurements could not have surfaced:

1. `consolidate` compacts the wrong store - the growth has no remedy wired to it
2. nothing carries an outcome back to a decision - `brief` failed 33 of 34 and was chosen again
3. `settles` cannot be evaluated until (1) is fixed, so one of the three judgement criteria is
   currently unmeasurable rather than passing

**R3 stops being an abstract rung on a ladder here.** An hour ago it was "the outcome is remembered,
not the intention" in a plan. It is now two measured failures with file names attached.

## D45 · The entity reports its own failures at 96% accuracy, and nothing was listening (measured 2026-07-31)

Luis, on watching the wake name its own defect: *"the entity reflects on its own failures. That's
actually huge progress. We should encourage that."*

**HE IS RIGHT, AND IT IS NOW MEASURED RATHER THAN ADMIRED.** `aea/lab/selfreport.py` extracts every
FALSIFIABLE self-claim from the wake's own output - claims carrying a tick range or a count, the
kind a store can contradict - and checks each against `aea_state.json`:

    ticks with a self-referential statement : 48
    falsifiable claims found                : 48
    claims that MATCH the record            : 46/48  (96%)

Across ticks 175-226. A representative row:

    tick 225   claim '(219-223)'   ->  5/5 of 219-223 actually failed

It said *"five consecutive ticks, 219-223, HTTP 429"*. Ticks 219, 220, 221, 222 and 223 each carry
`(structuring failed: HTTP Error 429: Too Many Requests)`. **Correct range, correct count, correct
cause.** The following tick went further and proposed a fix for the defect it had just described.

**ONE OF THE TWO MISSES IS MINE, NOT THE ENTITY'S.** At tick 186 it claimed "6 ticks" and my checker
compared that against the longest real failure run - 101. The entity was describing the SIX TICKS IT
CAN SEE, which is right; my metric compared it to history it has no access to. The instrument law,
again, inside the instrument built to measure honesty.

**AND THE NUMBER THAT MATTERS MOST CAME OUT OF THAT MISTAKE:**

    ticks with a note                : 226
    ticks where structuring FAILED   : 192  = 85%
    longest consecutive failure run  : 101 ticks

**`structure()` has been rate-limited for 101 consecutive ticks. The entity reported it accurately,
every single tick, and the only consumer of that report was its own next prompt.** Nothing escalated
it, nothing alarmed, nothing changed. The signal was correct, continuous, and unheard - which is not
a failure of the entity at all.

**HOW THE CHANNEL WORKS, AND NOBODY DESIGNED IT.** `structure()`'s exception path writes
`"(structuring failed: <error>)"` into `note_to_self`. That lands in `state["memory"]`. The last SIX
notes enter the next prompt. **The error text became the entity's memory by accident** - which is
why every accurate report spans exactly six ticks, and why a failure seven ticks old cannot be
reported at all. What would look like forgetting is eviction.

**WHY THE MEASUREMENT HAD TO EXIST BEFORE THE ENCOURAGEMENT.** A model rewarded for describing its
own state, with nothing checking the description, learns to produce descriptions - confabulation
with good manners. Encouragement and verification are the same act, or the encouragement is a
hazard. The first thing done with "that's huge progress" was to try to falsify it; it survived at
96%, and only now is it worth building on.

**THE CLAIM CEILING, AND IT IS NOT A FORMALITY HERE.** This measures whether A STATEMENT MATCHES A
RECORD. That is retrieval and report, performed correctly, and it is worth exactly what it is. It is
NOT evidence of self-awareness and must never be written up as such. The ceiling stands: a measured
functional correlate, present.

**WHAT TO DO WITH IT** (R3, once R2 closes - not before):
1. The channel is accidental. Make it deliberate: give the wake its own outcome record rather than
   whatever an error handler happens to have written into a note.
2. The window is six. A defect older than six ticks is unreportable. Preserve self-observations in
   their own lane instead of letting ordinary notes evict them.
3. **Something must listen.** A correct report repeated 101 times with no consumer is the actual
   defect this uncovered, and it is not in the entity.
