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
   its edges. Never re-scan the tree; that's what burns tokens. Refresh: `python aea/build_graph.py`.
2. **`diary/SESSION_LOG.md`** — the latest entry: current state, what's `LOCKED` (do not re-litigate),
   and the exact `NEXT` task. Build from `NEXT`; don't re-decide what's under `LOCKED`.
3. **`diary/DISCOVERIES.md`** — *why* the plan is what it is (D1–D8 + the shortest path). Inherit the
   reasoning, not just the result. The raw, undistilled sparks these grew from live one step upstream
   in **`diary/REFLECTIONS.md`** (Luis's realizations, verbatim) — read it to catch the current frontier.
4. The laws in §3 below. Then `GAME_PLAN.md` + `design/` on demand (read, don't re-plan).

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
aea/       ALL runtime Python, one package, flat imports:
             controlroom.py (server) · grid.py (metered model grid = the game's energy)
             bench_core.py (THE BENCH: compose real models into a machine, run it)
             aea.py (the entity's heartbeat/tick) · agent_tools.py (its hands = real tool-calling)
             brief/hades/autonomy/energy/talk/speak/trust/pulse/... (the organs)
             build_graph.py (regenerates graph.json — deterministic, no LLM tokens)
state/     ALL runtime state (grid_state, journey_save = the sacred save, self, heartbeat, memory...).
             Resolved by grid.STATE. Private stores are gitignored, never committed.
web/       front-end: world.html (mission loop), game/ (the bench UI), tracker/game.html, three.js libs. Served via grid.WEB
design/    the design book (~40 chapters) + design/concepts/ sheets. Entry: design/INDEX.md
docs/      AEA research/planning notes + specs (pre-game)
archive/   dead prototypes / scratch / orphaned data — kept, not deleted
voice/     local TTS/STT tooling (weights gitignored — downloaded, not source)
```

**The path model (why it holds together):** `aea/grid.py` finds `ROOT` by walking up to `design/`/`.git`,
then sets `STATE = ROOT/state`, `WEB = ROOT/web`, and loads `.env` (keys) from `ROOT`. Code runs from
`aea/` while state, web, and keys resolve to the repo root. **Never hardcode a state path — always go
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
   `python aea/build_graph.py` so the graph stays true. Add a durable finding to `diary/DISCOVERIES.md`.
3. Commit only when Luis asks. Privacy-scan the diff first (no employer paths / secrets). Never `--force`
   or skip hooks unless told.

The next real move is always in the diary's `NEXT`. As of the last entry that is **THE MERGE** — unite
the mission loop (`web/world.html`) and the bench (`aea/bench_core.py` + `web/game/`) into one program,
then light the first Minimal Viable NPC. Confirm against the diary; it wins over this paragraph.
