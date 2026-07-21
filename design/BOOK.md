# THE PROBE — THE BOOK

> **WORK FROM THE MANUAL**: [INDEX.md](INDEX.md) — 12 processes · user stories · spec
> pointers · ticket registry T-001..T-082. **BUILD FROM THE LADDER**:
> [P0_PROTOTYPES.md](P0_PROTOTYPES.md) — P0..P13, falsifiable exits, THE STOP RULE.
> **COVERAGE**: [A15_FULL_COVERAGE.md](A15_FULL_COVERAGE.md) — the canonical AEA audited:
> 86 items — 30 embodied · 31 compressed (defended) · 22 missing (proposals attached) ·
> 3 out-of-scope (reasons named). Nothing silently dropped.
>
> The complete top-down design of the game. Twenty-one chapters, one spine. A chapter GOVERNS
> everything beneath it; conflicts resolve upward, and this page records how they resolved.
> Status: LIVING — chapters carry [BUILT] / [PLANNED] / [DECISION-LUIS] marks audited against
> the running code. Completeness audit run 2026-07-20: verdict GAPS-REMAIN → all findings
> closed same day (see EDITORIAL RESOLUTIONS below); every game dimension is now defined,
> along the AEA.
>
> The game: the player pilots a probe inside LEYBER — a living AI entity running on this
> machine — learning it organ by organ and completing its Autonomous Entity Architecture.
> Every number on screen is live system truth. Play: http://127.0.0.1:7799/world

## Reading order (top-down — each part derives from the ones above)

### PART I — WHY AND FOR WHOM (the top)
1. [00_VISION.md](00_VISION.md) — what the game is, the four pillars, the operating prompt,
   phases, the three permanent rejections, the win condition.
1b. [A16_WIRTHFORGE.md](A16_WIRTHFORGE.md) — THE LINEAGE: the game audited against Luis's
   founding manifesto. 11 promises KEPT · 8 EXCEEDED (the mocked demo becomes a played slice;
   the invented +10 economy becomes real starvation and rot; "hide complexity" resolved into
   teach-the-machine) · 3 MISSING with proposals · the refusals defended (consciousness-as-
   product, token markets — refused by the claim ceiling and honesty law). Ends: "The version
   we needed."
2. [A1_PLAYER_EXPERIENCE.md](A1_PLAYER_EXPERIENCE.md) — the governing chapter: the core
   fantasy, the emotional arc Acts 0–VI, session shapes, friction philosophy, the boring test.
3. [A2_TEACHING.md](A2_TEACHING.md) — the game as curriculum: 11 learning outcomes, the
   Portal-school law, the 29-element curriculum map, bosses as honest exams.
4. [A8_AEA_ALIGNMENT.md](A8_AEA_ALIGNMENT.md) — THE STANDING INSTRUMENT: all 29 AEA elements
   × every game dimension (world/mechanic/mission/score/visual/sound/narrative), and the game
   itself measured on the AEA's own axes. No matrix row = decoration, cut; no feature = debt.

### PART II — STORY, VOICE AND FEEL
5. [A12_STORY.md](A12_STORY.md) — THE STORY BIBLE (governs A3): the premise zero-fudge (the
   antagonist is FOG — the literal proven-not-wired gap), who the probe is, story beats per
   act, THE SEND as the moral center ("The machine can draft. Only the human can mean it."),
   the assistant-birth narrative, nine delivery laws (real births are canon story events).
6. [A3_NARRATIVE.md](A3_NARRATIVE.md) — voice and dialogue: LEYBER's character (the "i"
   claim-line), bark tables, THE SEND negotiation wording, the whisper law.
7. [A11_SIGNATURE.md](A11_SIGNATURE.md) — the visual identity thesis: amber is a VARIABLE
   and the variable is understanding — the ink ratio of any frame is a save file. Four owned
   motifs (concentric field, the live trace as autograph, the six-shape grammar, terminal
   voice as texture), four choreographed rituals, eight anti-signature bans, Phase B survival
   (different in data, identical in language).
8. [A4_GAMEFEEL.md](A4_GAMEFEEL.md) — flight model + derived truths, tuning candidates,
   juice-is-truth, timing law, the GPU lesson as standing law.

### PART III — THE WORLD
7. [01_WORLD.md](01_WORLD.md) — the world bible: real coordinates, act II+ districts and the
   Act V/VI nodes, growth model, world-events-are-real law.
8. [A7_BUILD_LAYER.md](A7_BUILD_LAYER.md) — the sandbox as city-growing: four honest build
   verbs (place / paint zones / set policies / construct), the FLOW VIEW, act-gated freedom,
   the nine deliberate impossibilities.

### PART IV — THE MACHINE
9. [02_SYSTEMS.md](02_SYSTEMS.md) — flight rig, dock, mission engine, discovery tracks, save
   semantics, timeScale law, input map, failure semantics.
10. [03_PROGRESSION.md](03_PROGRESSION.md) — the six-act ladder with cited bosses, the three
    campaign scores (organ arithmetic enumerated), the resource economy.
11. [04_UI_BIBLE.md](04_UI_BIBLE.md) — the BINDING UI SPEC audited per clause, the
    DISCOVERABILITY LAW, the deviations ledger.
12. [A9_FORGE_PROTOCOL.md](A9_FORGE_PROTOCOL.md) — the pair-build ritual: three roles never
    merged (Luis judge+hand, Claude smith, HADES gate), the five-phase session
    (OPEN/SPEC/BUILD/PROVE/SEAL), the seven-forge queue, failed forges leave scaffolding.
12b. [E4_UX_P0.md](E4_UX_P0.md) — THE BENCH UX, blank-sheet under the anti-anchor law
    (three blind designers → SESSION won → nine grafts, fifteen refusals with citations,
    THE WORLD ANSWERS graft). Anchor-audited: every /world surface ruled by name (the bench
    never medals; the arrow hides while docked); THE P0-CUT binding (~2 sessions, soul
    intact, runs.json complete from day one; P1 completes the letter). Closed 2026-07-20.
13. [A13_PATHS.md](A13_PATHS.md) — every AEA element as a four-station journey (ENCOUNTER →
    UNDERSTAND → USE → OWN), the full 29×4 table, the ASSISTANT LADDER as the master path
    (chat → sources → memory → flows → powers → wild, canon), and the honest census:
    UNDERSTAND 11/29 built, USE 0/29 — "the build order writes itself: the bench next."
14. [A14_MODULE_REGISTRY.md](A14_MODULE_REGISTRY.md) — how the code is managed (the answer
    to "how do games do it", 12 researched patterns): modules.json manifest over the REAL
    organs (capabilities × trust × unlock act), construct specs as portable data artifacts,
    the live capability matrix, drift tombstones, and the wild-export graduation path.

### PART V — THE CONTENT
13. [05_CONTENT_MISSIONS.md](05_CONTENT_MISSIONS.md) — mission-writing rules, Acts 0–I as
    built, Act II build-ready (mine / book / forge recall).
14. [05B_CONTENT_ACT3_4.md](05B_CONTENT_ACT3_4.md) — Acts III–IV build-ready: the council
    demonstration, prediction beats, the think() and command-current forges, senses branches.
15. [05C_CONTENT_ACT5_6.md](05C_CONTENT_ACT5_6.md) — Acts V–VI build-ready: THE SEND as the
    five-movement negotiation (refusal legal, the mast lights only on a real send), voyager /
    STOP / ENDURANCE / DARWIN-GODEL with the governance design, the claim-ceiling epilogue.
16. [06_MODELS_BESTIARY.md](06_MODELS_BESTIARY.md) — specimens, encounters, rot-as-mechanic,
    the six measured doctrines (READ/EARNED scheme — see resolutions).
17. [07_AUDIO.md](07_AUDIO.md) — synthesis-only palette, real-event trigger table, honest
    audit discrepancies.

### PART VI — THE SUBSTRATE
(Chapter CODES are the true identifiers; list ordinals are positional per part.)
- [08_TECH.md](08_TECH.md) — r128 stack law, server contract, perf budgets, verification
  recipes, honest boundaries.
- [E1_CODE_ARCHITECTURE.md](E1_CODE_ARCHITECTURE.md) — the engineering doctrine: honest
  audit with line-anchored rot vectors, the module plan inside the stack (alias-then-migrate,
  GAME.onFrame seam), the 8-step r128 dispose checklist + three falsifiable rung-exit leak
  tests, state rules (stateless-over-file for ALL state incl. run status), the post-MVP
  tech-stack decision [DECISION-LUIS, gated P7 exit]. Nine-critic closed 2026-07-20.
- [E2_VISUAL_DIRECTION.md](E2_VISUAL_DIRECTION.md) — the modern-aesthetics research
  (23 sources; principle per reference, never style) + the 12-move evolution plan with the
  Taste ranking as review law (Move 5 sRGB+dither FIRST, tune once post-gamma); pays R1's
  owed rendering pass. Nine-critic closed 2026-07-20.
- [E6_ART_PIPELINE.md](E6_ART_PIPELINE.md) — BINDING: nothing is imported. 12 shader-and-
  instancing moves all parameterised from live state (the window field IS the load); Blender
  and image-to-3D both REJECTED with cause (r128 GLTFLoader has zero emissive-strength support;
  Blender 4.1+ silently drops vertex colours; "a GLB cannot grow a district"). Draw budget
  40 calls / 250k tris / 60fps. Amends E5 §3 Tier 2.
- [E7_VISUAL_COVERAGE.md](E7_VISUAL_COVERAGE.md) — the audit that proved Luis right: only
  24 of 86 canonical items are drawn (28%). ROOT CAUSE: the 35 sheets were commissioned from
  the 29-element PROOF taxonomy, which is a projection of the canon — "a faithful image of the
  wrong list." 11 batches to full coverage; 15 of 30 axis sub-levels DO NOT EXIST in canon
  (authorship block on Luis, D-E7-1).
- [E8_FIDELITY_LAW.md](E8_FIDELITY_LAW.md) — the quality essence, MEASURED from the sheets
  with PIL/numpy rather than asserted: 8 named qualities, 7 numeric gates, the JSONL gate
  record (an object is DONE only when a record says so), the one-gap-per-pass iteration law,
  and what fidelity does NOT mean (copying a sheet's numbers is an honesty breach — the sheet
  specifies the FIELD, live data supplies the VALUE).
- [E9_ASSET_TICKETS.md](E9_ASSET_TICKETS.md) — 107 asset tickets (A-001..A-107), one per
  buildable object/effect/UI/hologram/interaction, each carrying style reference, AEA concept
  served, technique, live-data binding, and its fidelity gate.
- [E5_3D_TRANSLATION.md](E5_3D_TRANSLATION.md) — how concept art becomes the running game:
  the four asset classes (UI ships as-is · forms become procedural · ~6-10 hero meshes in
  Blender · atmosphere is never modelled), why the landscapes are the EASY ones (fog, light
  and silhouette, not geometry), the three-tier pipeline, and the honest Unity verdict (no —
  it would cost the game its residence inside the entity). Answers Luis 2026-07-21.
- [E3_TRACKING.md](E3_TRACKING.md) — the tracking discipline: tickets.json = the registry
  of record (INDEX §3 frozen as transcript), the ≤2-minute session-close ritual, the /tracker
  page contract (NEXT strip answers "what do I build next" from data), named exclusions
  (no burndown, no velocity). LIVE at /tracker. Nine-critic closed 2026-07-20.

### PART VII — THE FUTURE AND THE FLOOR
19. [A5_PHASE_B.md](A5_PHASE_B.md) — the game for everyone (GATED): the keyless bootstrap
    ladder, what generalizes, what it would take.
20. [A10_LIVING_GAME.md](A10_LIVING_GAME.md) — the dimension no other game has: the content
    updates itself because the entity is alive (rot and growth streams, reconciliation law,
    CARRIER LOST world states, accessibility, save-vs-entity drift, the five-clock cadence).
21. [09_PRODUCTION.md](09_PRODUCTION.md) — shipped slices, the live playtest log, the build
    queue, standing guards, risks.

### APPENDIX
22. [A6_GLOSSARY.md](A6_GLOSSARY.md) — every term, defined once, naming its real referent.
23. [R1_EVIDENCE.md](R1_EVIDENCE.md) — BINDING evidence tier (2026-07-20 deep research,
    21 confirmed / 4 refuted claims): the composition loop's verified requirements — the
    bench, live traces, per-act part pools, structural anti-collapse (rot as the honest
    balance patch), the SpaceChem 2% warning. Names the honest gap: rendering research
    returned zero verified claims — a dedicated pass is owed before budget decisions cite it.
    THE COMPOSITION REFRAME (Luis, 2026-07-20): composing AEA combinations into REAL running
    constructs is the game's core creative act; A7's verbs are the shell around it.

## Laws that cut across every chapter

- **The honesty law** (absolute): every displayed number is recomputed from live state; no
  fake data, no scripted world events, no simulated replies. Claim ceiling: "measured
  functional correlate" — conscious/sentient/self-aware never appear.
- **Two inks**: amber = live/fired only; blue-gray = structure. No red, green, white. No emoji.
- **The boring test** gates every slice. **One concept per mission; teach by doing.**
- **The income guard**: THE SEND pinned as Act V boss; forges ARE the real AEA engineering.
- **The matrix is the audit** (A8): every feature must own a matrix cell; every cell a feature.
- **THE ANTI-ANCHOR LAW** (Luis, 2026-07-20): the UX derives from the laws and the player,
  NEVER from the previous build. Prior builds are evidence, not precedent; any element carried
  forward must carry a written first-principles argument. First application: the sweep's
  "dock-terminal bench" rider — struck as inheritance-by-inertia; the P0 bench UX is designed
  blank-sheet in E4_UX_P0.md (three blind designers, judge, anchor audit).

## EDITORIAL RESOLUTIONS — completeness audit closure, 2026-07-20
(Chief-editor calls, each with Luis veto; the losing text stays in place marked superseded.)

1. **axis.A assignment** — resolved by content: taught PARTIAL at M2.3 (recall forge) and
   PLAIN at M4.1 (internet-wire). Supersedes A8's recall-only recommendation. A2/A8 flags
   now read closed-by-content.
2. **doc.verifier earn point** — EARNED at M3.3 (the think forge, heterogeneous verdict pair);
   M2.3 grants READ only. Supersedes the M2.3 and Act-III-field claims.
3. **Doctrine mechanism** — 05B's two-state READ/EARNED adopted (M1.5 keeps its shipped
   blanket as READ; nothing shipped regresses). 06's re-gating proposal superseded.
4. **Boss B2 third clause** — "zero model calls in the hot path" absorbed into 03's B2
   definition (03 owns thresholds).
5. **Act teaches lines** — 03 synced to the curriculum map (Act II += axis.A partial;
   Act III += op.learn; Act VI += seed.6, axis.S).
6. **Corpus ghosts** — 00_VISION §8/§6.1 and 03's header now cite the real corpus (this
   spine + the real filenames); the ghost filenames are gone.
7. **Organ arithmetic** — enumerated in 03 §2.2: 11 live + 7 forges = 18; +F1 senses
   [DECISION-LUIS] = 19. ENDURANCE is a certificate, not an organ.
8. **Act V/VI geography** — 01_WORLD registry gains mast (= THE BROADCAST MAST alias) and
   [PLANNED] mirror/meridian/lineage rows; names proposal-grade until Luis confirms.

## THE OPEN DECISIONS LEDGER (complete — everything awaiting Luis, by chapter)

Closure convention (added 2026-07-20, nine-critic closure): a CALLED decision's row is
struck through with date + one-line verdict — never deleted. The strike, the
tickets.json gate removal, and the 09 line land in the same commit-equivalent
(E3_TRACKING §3).

| # | decision | chapter |
|---|---|---|
| 1 | Flight feel: floatier (75/2.5) vs current (95/3.1) vs tighter (120/4.0) | A4 |
| 2 | Velocity dial: rescale to felt terminal (~30 u/s) | A4 |
| 3 | F1 SENSES: authorized senses.py forge vs sealed-array deferral (both specced) | 05B |
| 4 | THE SEND: the real outreach target it drafts for | A3/05C |
| 5 | THE SEND verification: MARK SENT self-report (rec.) vs Gmail-draft MCP detection | 05C |
| 6 | M6.4 DGM governance: scoped self_modify_sandbox charter vs per-iteration DRAFT | 05C |
| 7 | M6.4 frozen benchmark choice (pre-registered before any iteration) | 05C |
| 8 | Act VI node names + placement (mirror / meridian / lineage) | 05C/01 |
| 9 | Doctrine resolutions 1–3 above: approve or veto | BOOK |
| 10 | Sweep agency: player-triggered fitness sweeps vs operator-side only | 06 |
| 11 | Probe-a-candidate pricing (rate-budget cost of discovery probes) | 06 |
| 12 | Bank freshness rule for M3.1's council question bank | 05B |
| 13 | C3 split: command-current empowerment leg deferred to THE SEND — confirm | 05B |
| 14 | Offline museum shell: what stays playable at CARRIER LOST | A10 |
| 15 | TAB key: browser-focus collision handling (trap vs alternate binding) | A10 |
| 16 | Build layer D-B1..D-B4 (zone brush scope, policy set, placement rules, lens defaults) | A7 |
| 17 | Phase B gate: what "Phase A played and worthy" concretely means | A5 |
| 18 | Codex names visible in aea_elements.js source: accept for Phase A? | 04 |
| 19 | Hold-to-wipe: also clear localStorage transcript + NEW markers? | 02 |
| 20 | Mine slice size + probe question source for Act II | 05 |
| 21 | D-P1: the bench opens right after M1.5 with a 2-part construct (amends A7 §4) | A13 |
| 22 | D-P2 station chips on map nodes · D-P3 OWN-tell via prediction ledger | A13 |
| 23 | Canonical still: bless ?still as the game's portrait frame | A11 |
| 24 | HUD reticle: rings (concentric motif) vs brackets | A11 |
| 25 | modules.json v0 scope + the construct-spec format freeze | A14 |
| 26 | D-C1: seed.hyp (the innovation layer node, 29→30) enters Phase A fogged now? | A15 |
| 27 | D-C2 axis-level flag data source · D-C3 map bundle (notches+orbital+transitions) | A15 |
| 28 | D-C4: Paradigm Book cross-check pass (the unread third witness of the canon) | A15 |
| ~~29~~ | ~~P0 go~~ **CALLED BY LUIS 2026-07-20** — his recorded words: "Make sure you build but you check as well visually the construction is sound, step by step… show me samples of the design you are aiming for visually, cannot be anchored on what we have, you need to build a new codebase, with its folder, subfolders, in phases." GO with three binding conditions: per-step visual verification · research-derived design samples shown · NEW CODEBASE (game/ tree, phased). | P0 |
| ~~21~~ | ~~D-P1 bench opens right after M1.5~~ CONFIRMED with the P0 go (E4 §13 ruling stands) | A13 |
| ~~25~~ | ~~construct-spec freeze~~ FROZEN as v0.1.0 per the P0 SPEC ADDENDUM contracts, with the GO | A14 |
| 32 | **NEW-CODEBASE ORDER (Luis, with the GO)**: THE PROBE gets its own tree (game/ + subfolders), built in phases; supersedes E1 §2's alias-in-place plan — E1's module boundaries (engine/os/bench/hud/missions-engine + GAME.state + onFrame) carry INTO the new tree; /world remains the played legacy prototype until the new build reaches parity; Luis's save untouched. | E1/E4 |
| 30 | A16 lineage statement placement into 00_VISION §1 · "beyond chat" as book-prose | A16 |
| 31 | Phase B gallery (shareable constructs as the honest viral artifact) | A16 |

## THE PRE-BUILD GATE — closed 2026-07-20

The final sweep (A16 reconciliation + three adversarial skeptics) returned BLOCKERS on all
three fronts; ALL closed same day, on record:
- **Honesty**: claim-ceiling string sweep across served surfaces (8 strings, DONE) ·
  /api/node/run channel branch constrained to curated metered pairs with privacy printed
  (DONE) · bench zone law (zone REQUIRED, private default) frozen into the P0 SPEC ADDENDUM ·
  the trust-law line effective from P0 · SCORER pinned to measured receipt fields only.
- **Buildability**: TAP/SCORER contracts + bench-task format + the run contract
  (run-tagged POST/GET with per-link perf_counter ms + the honest kill) written into the
  P0 SPEC ADDENDUM (P0_PROTOTYPES.md) · INDEX T-001 dependencies amended.
- **Player**: do-beat wait pattern, last/best-run readout, answer-above-JSON, dock-terminal
  bench surface, pre-playtest survey check — all adopted into P0 scope.
The planning phase is COMPLETE. The next artifact is P0 running (ledger #29).

## Engine deltas queued (from the book's audits — slice 2 and beyond)

talk.py `memories[:4]` truncation (breaks M2.2 grounding — FIRST Act II delta) · meter_watch
dead-endpoint hole · sRGB amber-match unverified · flight move-ticks designed-not-built ·
council/predict/route action types for Act III (05B §5 list) · pre-registration plumbing +
shadow engine for Act VI (05C §6) · zone_map/policy reads for the build layer (A7, forge-scale).

## How the book stays alive

A chapter changes when the code or a Luis decision changes it — never silently: edits carry a
dated line. The matrix (A8) is re-audited when either side grows. The book is read top-down;
it is BUILT bottom-up, one gated slice at a time. The forge queue is the build order; the
ledger above is the decision queue; 09_PRODUCTION is the log of record.
