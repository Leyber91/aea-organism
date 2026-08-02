# CLAUDE.md — THE PROBE (aea-city). The introduction. Read this first, every session.

You are landing cold on a game that is being built inside a **real autonomous AI entity** running on
this machine. THE PROBE: the player flies a probe through the living entity and composes real AI
parts — models, organs, loops — into small machines that **actually run** (every DO beat is an HTTP
call to `localhost`). The spine of the whole thing is the **honesty law**: every bar, number, and
event is live system truth. A fabricated resource is a worse failure than an ugly one.

The thesis (one line, LOCKED): *Wire living proofs of a mind, each more complete than the last, until
you hold the whole one — and it keeps running after you close the tab.*

---

## THIS FILE IS THE MAP AND THE METHOD — NOT THE STATE

Read this once at the start of a session and you know **how to work here and where everything is**.
That does not change, so this file does not need updating. The things that *do* change — what shipped,
what's next, what's locked — live in `diary/SESSION_LOG.md`. **If you catch yourself wanting to write
progress into this file, you have the wrong file open. Update the diary.** The only time this file
changes is when the *methodology* or the *repo shape* genuinely changes.

---

## 0 · BOOT SEQUENCE (every session starts here)

1. **`graph.json`** — the master orchestrator graph. Enter at root `THE_PROBE`, follow one `contains`
   edge into the subgraph you need (`code` / `plan` / `discoveries` / `references`), pull that node +
   its edges. Never re-scan the tree; that's what burns tokens. Refresh: `python -m aea.tooling.build_graph`.
2. **`diary/SESSION_LOG.md`** — the latest entry: current state, what's `LOCKED` (do not re-litigate),
   and the exact `NEXT` task. Build from `NEXT`; don't re-decide what's under `LOCKED`.
3. **`diary/OPEN_LOOPS.md`** - THE PENDING WORK. Every step carries a verdict (FINISH/LATER/KILL)
   and names three things: the WIRING, the CODE, and the MILESTONE the assembled entity can
   demonstrate the moment it lands. Its machine-side twins are `aea/lab/vital.py` (what RAN and what
   CHANGED at runtime) and `aea/tooling/assembly.py` (what is reachable, statically) - when the file
   and the manifests disagree, the manifests are the truth.
4. **`diary/DISCOVERIES.md`** — *why* the plan is what it is (D1–D8 + the shortest path). Inherit the
   reasoning, not just the result. The raw, undistilled sparks these grew from live one step upstream
   in **`diary/REFLECTIONS.md`** (Luis's realizations, verbatim) — read it to catch the current frontier.
5. **`diary/THE_STRUCTURE_CONVERSATION.md`** - the engineering contract for any rung: how structure
   is obtained and validated, the write-ahead ordering, the four memory stores, and the SEVEN
   QUESTIONS to answer in writing before building a rung. Hold that conversation first.
6. The laws in §3 below. Then `GAME_PLAN.md` + `design/` on demand (read, don't re-plan).
7. **Before any non-trivial change, ASK: `python -m aea.lab.recall "what you are about to do"`.**
   Hybrid lexical+semantic over every recorded lesson, MEASURED at 7/12 hit@5 against a gate of this
   repo's own defects (lexical alone 3, semantic alone 4). It is one command and it costs seconds.
   *Why this is a boot step and not advice:* the recurring failure here has never been forgetting -
   it is that a lesson written as prose must be RETRIEVED, by a mind doing something else, at a
   moment defined by action, with no shared vocabulary between the two. Six lessons were re-learned
   in a single day while being correctly recorded within arm's reach of the defect. And the author
   of `recall.py` shipped it and then made two more changes without running it, which is the whole
   argument for putting it in the boot sequence instead of trusting anyone to remember.
   Its companion is `python -m aea.lab.transfer` - the same question asked mechanically ACROSS the
   tree, and it runs inside the battery so it cannot be skipped.

**Run it:** `python controlroom.py` → serves the game + the entity's live endpoints on `:7799`.

---

## 1 · WHERE EVERYTHING IS (the map)

```
controlroom.py     run shim -> aea/controlroom.py
graph.json         the knowledge-graph — read FIRST (refresh: python aea/build_graph.py)
CLAUDE.md          this file (the introduction; stable)
README.md / GAME_PLAN.md

diary/     the handoff system. SESSION_LOG (state) · REFLECTIONS (Luis's raw sparks, mess-first) · DISCOVERIES (distilled reasoning) · README (protocol) · REORG_PLAN
references/ pointer map to authoritative sources (AEA framework, site voice, visual spec) — pointers, privacy-guarded
aea/       ALL runtime Python — 10 domain subpackages, inward-only deps (imports are `from aea.<pkg> import <mod>`):
             kernel/  grid (metered model grid + Meter + ROOT/STATE/WEB paths) · pulse · trust · tracelog
             mind/    orchestrator · swarm · hades · pathfinder · relay
             energy/  energy (the draw/ladder) · capacity · capability_census · extensive_census · model_fitness · probe · gauntlet
             memory/  consolidate · index_codex · memory      bench/  bench_core (THE BENCH: compose+run real models)
             io/      speak · listen · agent_tools (HANDS) · notify
             organs/  autonomy · brief · talk · telegram_bridge · reflect
             loop/    aea (heartbeat/tick) · live        server/  controlroom (the server)
             tooling/ build_graph (regenerates graph.json, deterministic) · export_city
                      page/    THE PUBLISHED ORGANISM, one job per module: sources · graph · layout ·
                               marks · axes · climb · style · panels · template · render · guard.
                               `publish.py` is the run shim; the command did not move. Split proved
                               byte-identical against the monolith at the same tree state.
state/     ALL runtime state (grid_state, journey_save = the sacred save, self, heartbeat, memory...).
             Resolved by grid.STATE. Private stores are gitignored, never committed.
web/       front-end: world.html (mission loop), game/ (the bench UI), tracker/game.html, three.js libs. Served via grid.WEB
design/    the design book (~40 chapters) + design/concepts/ sheets. Entry: design/INDEX.md
docs/      AEA research/planning notes + specs (pre-game)
archive/   dead prototypes / scratch / orphaned data — kept, not deleted
voice/     local TTS/STT tooling (weights gitignored — downloaded, not source)
```

**The path model (why it holds together):** `aea/kernel/grid.py` finds `ROOT` by walking up to
`design/`/`.git`, then sets `STATE = ROOT/state`, `WEB = ROOT/web`, and loads `.env` (keys) from `ROOT`.
Code runs from the `aea/` subpackages while state, web, and keys resolve to the repo root; the entity's
own subprocess spawns run as `python -m aea.<pkg>.<mod>` at cwd=repo-root. **Never hardcode a state path — always go
through `grid.STATE` / `grid.load_json` / `grid.atomic_save_json`.** A missed write-site silently
splits or resets state (that is discovery D8, learned the hard way).

---

## 2 · HOW TO WORK HERE (the crystallized lessons — earned across every prior Claude session with Luis)

These are not preferences; they are corrections that already cost time once. (Sources: the global
operating rules' field-lessons layer, the PORTFOLIO project rules, `LUIS_FILTER`, `LAB_EXPERIENCE_STANDARD`.)

- **Be the filter, not the mirror.** Critical thought partner and senior engineer. If the logic is
  flawed, say so first — name failure points *before* validating strengths. Devil's advocate is standing.
- **Completion over planning.** The recorded failure mode is "brilliant strategy, zero artifacts."
  This repo already carries ~110:1 words-to-code (D7). No new design chapters, no new concept sheets,
  no new acts until an act *ships*. When tempted to re-plan, read the diary's `NEXT` and execute it.
- **Verify, don't claim.** "Done" means it *ran* — server restarted, endpoint returned 200, screenshot
  read — not "it compiles in my head." Report failures plainly with the output.
- **Show, don't tell.** Decisions move on screenshots, not prose. Build it, render it, read the PNG,
  put it in front of Luis. Present the artifact, not a description of the artifact.
- **His messages bundle 3–5 asks.** Enumerate them; answer every one or explicitly defer it. A dropped
  thread costs more trust than a wrong answer.
- **Capture his sparks before acting.** When Luis puts a realization / vision-shift through, write it to
  `diary/REFLECTIONS.md` first (dated, in his words) — mess-first. Distil it into a discovery later,
  rested. Losing the spark to fast execution is the failure this file prevents.
- **Dissatisfaction is structural until proven cosmetic.** "Feels off" has always meant form,
  composition, framerate, motion — never missing decoration. Diagnose at architecture level first.
- **"What do you think?" = one opinionated recommendation** with reasons and a named trade-off. Never
  a menu. Ambiguity in execution mode → make the best-judgment call and build it; correcting a
  completed attempt beats approving a plan.
- **Run the gauntlet on your own output before showing it.** Ask "would Luis ship this or push for
  more?" — then apply the predictable pushes yourself and present only the surviving version.
- **Expert-hat protocol (STANDING).** Start a build under the operating role in `GAME_PLAN` / the plan:
  a fusion of a Duskers-class diegetic director, a Bruno-Simon three.js artist, a Territory-Studio FUI
  designer, and a Portal-school learning designer — above all four, the honesty law.
- **Name avoidance out loud.** Infrastructure-as-avoidance, scope inflation, polish instead of
  capability — if the shiny thing delays shipping, name what it costs against the income clock and stop.
- **The income clock is real.** On ties, the move that earns or that ships a playable act beats the one
  that polishes. Name the trade when scope competes with the clock.
- **Batch the exploration into a script; never a dozen live calls.** Law W1 applies to the assistant
  too. When an investigation needs more than about three lookups, stop and write ONE script that
  answers every open question in a single pass, then read one output. Fifteen small greps cost more
  tokens, take longer, and lose the intermediate results the moment the context compacts, while a
  script is re-runnable, diffable, and can be promoted into `aea/tooling/` once something calls it.
  Same rule for verification: a probe with a control beats three ad-hoc checks. *Named by Luis,
  2026-07-28, against a session that made a dozen greps where one survey would have done.*
- **Never test a regex or a path through a shell heredoc.** The Bash tool eats backslashes, so a
  pattern that works reports as broken and a broken one can report as fine. Write the test to a real
  file and run the file. *Paid for:* a privacy-guard diagnosis that was wrong twice before the shell
  was taken out of the loop.
- **A tool failing on a source is not the source being closed. Drop to the primitive.** A convenience
  tool has its own limits, and those limits are not the world's. When one fails, ask what it was doing
  underneath and do that directly: a raw GET with a browser User-Agent, the provider's own list
  endpoint, the file on disk. *Paid for:* `WebFetch` timed out twice on `build.nvidia.com` and it was
  nearly recorded as "the page cannot be read"; a plain `urllib` GET with a desktop UA returned 200
  and 200KB of server-rendered payload carrying every parameter the docs omitted. Corollary: an
  authoritative list is almost always an API call away, so derive the set from the provider
  (`/v1/models` returned 102 ids) rather than asking a human to paste links.
- **"No timeout" means a generous INACTIVITY budget, never `timeout=None`.** A rod that thinks for
  minutes must survive; a socket whose peer vanished must not hang the run. `None` gives urllib no
  read deadline at all, so a peer that stops sending without closing blocks forever. *Paid for:* two
  experiments sat 28 and 64 minutes on one second of CPU each, produced nothing, and were killed.
  Use ~300s per read, which is five times the worst latency ever measured here.
- **Every recorded failure has FOUR parts, and the fourth is the one that stops recurrence.** The
  rule, the failure that paid for it, **how it should have been built**, and **why the knowledge
  that would have prevented it was present and not applied**. Parts 1-3 make the next attempt
  cheaper; only part 4 stops the same mistake arriving in a new costume, because almost nothing here
  fails from not knowing. *Named by Luis, 2026-07-29,* across two messages while `scout.py` failed:
  first "add how you would have done it, so the next path starts from a silhouette", then "why you
  got to this point and didn't avoid it before - that is crucial". The honest answer that time: the
  author had quoted law B2 in that file's own docstring, had built the control because of M4, and
  had written D18 the day before. The knowledge was applied to the schema and not to the six-word
  category list, because **attention follows effort rather than risk** (law M9). Deliberately
  re-read the cheap part.
- **The SECOND time you write it, extract it. Not the tenth.** W1 governs your own process, and the
  trigger is repetition, not volume. *Paid for:* sixteen scratchpad probes in one session, each
  re-implementing the same untimed POST, the same reasoning/content parse, the same per-model
  parameter lookup, the same concurrent map and the same result table. That is fifteen copies of one
  module. When a script is about to repeat a block you already wrote today, stop and promote the
  block; when a finding is about to be re-derived, write it where it is loaded at boot. The same
  applies to lessons: a rule learned twice and recorded zero times will be learned a third time.
- **Ask the live thing, never the description of it.** Documentation describes the product; the
  endpoint describes what you actually have. Both matter and they disagree constantly: NVIDIA's docs
  document `nvext.max_thinking_tokens` and `reasoning_budget` that the hosted endpoint ignores or
  rejects, a model card can list a rod the endpoint 404s, and a catalogue entry is not a served
  model. Read the doc for the parameter NAME, then measure the behaviour. *Named by Luis, 2026-07-28.*

---

## 3 · THE LAWS THAT DO NOT BEND

- **Honesty law.** Every bar/item/event/number is live system truth from a real endpoint. No simulated
  outcome, no cosmetic particle disconnected from a real event, no invented number. Absent value → a
  dash, never a guess. The game may only be beautiful in ways the truth permits.
- **Claim ceiling.** Never assert the entity is "conscious / sentient / self-aware." The ceiling is
  "measured functional correlate, present." The *player* supplies "it's alive"; the game never asserts it.
  A "proof" is a receipt (it ran), never a claim.
- **Two-ink visual law.** Void field + structure grey; amber (`#ffb000`/`#d4a24c`) is the **fired/active
  state only** — sparse, bright, earned. Exact spec: `design/E2_VISUAL_DIRECTION.md` +
  `design/E8_FIDELITY_LAW.md`. Every experience earns **one wow moment + one honesty tag**. IBM Plex Mono,
  tabular-nums so numbers never jitter. Respect `prefers-reduced-motion`.
- **The boring test gates shipping.** If a stranger would call it a dashboard, it does not ship. Reading
  is not playing.
- **The sacred save.** `state/journey_save.json` (M0.1/M1.1 real progress) is never reset or overwritten
  carelessly. It survives every refactor.
- **Privacy guard (absolute).** Never write into anything committed/pushed: employer or client names,
  NDA / multi-employment references, compensation, absolute filesystem paths (this repo's parent tree
  contains an employer folder name), or personal identifiers. Privacy-scan before any push. The only real
  URL is `github.com/Leyber91`. This is why `data.js` and `index_codex.py` were excluded from the backup.
- **No emoji. Anywhere.** Not in code, UI, copy, commits, or conversation.

---

## 4 · RUN + VERIFY

- **Run:** `python controlroom.py` (root shim → `aea/controlroom.py`, `:7799`). Routes load at import —
  kill the running PID before restarting, or route edits won't take.
- **Headless screenshots need software GL:** Chrome `--use-angle=swiftshader` (WebGL will not paint
  otherwise). Serve over `http://` from a local copy, not `file://`, for anything using ES modules;
  OneDrive can serve stale bytes — robocopy to local temp first. Shoot, then **Read the PNG** before
  reporting. Render first, decide on the screenshot.
- **The decisive test is Luis piloting it in his browser** — flight feel, mission flow, the boring test.
  His go/no-go gates the next slice.

---

## 5 · END OF SESSION (the one ritual that keeps handoff alive)

1. Append one entry to **`diary/SESSION_LOG.md`**: `DID` / `LOCKED` (only if a new lock landed) / `NEXT`.
   This is the single source of "current state." (This file, `CLAUDE.md`, stays as-is.)
2. If the repo *shape* changed (files added/moved, endpoints, new design docs, new discovery), run
   `python -m aea.tooling.build_graph` so the graph stays true. Add a durable finding to `diary/DISCOVERIES.md`.
3. Commit only when Luis asks. Privacy-scan the diff first (no employer paths / secrets). Never `--force`
   or skip hooks unless told.

The next real move is always in the diary's `NEXT`. As of the last entry that is **THE MERGE** — unite
the mission loop (`web/world.html`) and the bench (`aea/bench_core.py` + `web/game/`) into one program,
then light the first Minimal Viable NPC. Confirm against the diary; it wins over this paragraph.
