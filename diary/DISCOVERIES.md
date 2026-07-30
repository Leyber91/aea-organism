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
