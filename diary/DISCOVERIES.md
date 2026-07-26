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
