# NEXT SESSION — kickoff prompt (design the codebase from scratch)

Paste the block below into a fresh conversation opened in this repo (`aea-city`). `CLAUDE.md` auto-loads
here and routes the session. This prompt makes its FIRST act be a complete, from-scratch codebase-design
presentation — clean, modular, OOP, subfoldered, size-capped — with a hard "don't code until Luis approves"
gate. Written 2026-07-22 at session close; supersedes the earlier "extend the architecture" framing.

---

```
You are taking over THE PROBE (this repo, aea-city). The current code is FUNCTIONAL but poorly organized —
flat, monolithic, forked. We are DESIGNING THE CODEBASE ORGANIZATION FROM SCRATCH: the FUNCTIONALITY is
preserved (ported), the STRUCTURE is redesigned clean from first principles. Do NOT write code yet — design
the ideal structure, present it, and I approve it before any code.

STEP 1 — INHERIT THE EXPERIENCE (only the CODE ORGANIZATION starts fresh, not the thinking). Read:
  graph.json → the "START HERE" entry atop diary/SESSION_LOG.md → design/CLEAN_ARCHITECTURE.md (current
  thinking — improve on it, not gospel) → design/FIRST_LIGHT_INTEGRATION.md (the real substrate calls) →
  DISCOVERIES D1–D12 (D12 = the expert-panel verdict + the HOLD-THE-LINE list) → design/FIELD_GUIDE.html
  (the target). Honor the standing "anti-anchor" conviction in REFLECTIONS.md: derive the design from the
  game's laws and the player, NOT from the shape of the old build.

STEP 2 — DESIGN THE CODEBASE FROM SCRATCH, to the scale of the finished game (all three modes, the world,
the pokedex, the acts, Phase B). Present, for my review:
  - THE IDEAL FILE TREE — folders and subfolders (and sub-subfolders where a domain earns it), every file
    with a one-line responsibility, designed clean from first principles — NOT a lightly-edited copy of the
    current layout.
  - PER FILE, ITS CLASS: NEW (design + write fresh) · PORT (carry real working logic out of a legacy file
    into a clean module) · KEEP (leave a working piece untouched and design around it).
  - ALL DEPENDENCIES — runtime (Python: confirm stdlib-only from the real code; the client's vendored
    three.js r128 + bloom chain, no build step; the .env keys) + the internal module import graph
    (dependencies point INWARD; no cycles).
  - THE ARCHITECTURE — the layers/rings, the boundaries, the client↔server data contract, and the single
    place the honesty law + claim ceiling are enforced.
  - FUNCTIONALITY MAP — each game system (compose→ignite→receipt, pokedex, world/map, the three modes,
    energy/carrying-capacity, the acts, Phase B) → the exact files that implement it → the build order.
  - THE MIGRATION PLAN — for every PORT/KEEP, which legacy file it comes from and what changes.

ENGINEERING STANDARD (the design MUST satisfy all of these):
  1. ONE REFERENCE POINT, THEN SUBFOLDERS. The root holds only the entry point(s) + config + a README that
     is the map. NO loose code files at root — every module lives in a named domain subfolder.
  2. SIZE CAP. Target <=300 lines per file; hard ceiling 500. Anything larger is split BY RESPONSIBILITY.
     The current monoliths (controlroom.py ~689 lines, world.html ~78KB) are the anti-pattern to dissolve.
  3. MODULAR OOP, single responsibility. Cohesive classes with one clear job; explicit interfaces;
     composition over inheritance; no god-objects, no logic buried in a 30-branch dispatch. Group by
     DOMAIN/feature, not by generic "utils".
  4. DEPENDENCY DIRECTION points inward: client → seam → substrate. The substrate imports nothing outward;
     zero circular imports; the seam is the only thing that knows about both sides.
  5. THE HONESTY FIREWALL — one class/module is the sole boundary where the honesty law + claim ceiling
     live: absent→null→dash, refusal→{ok:false, refused:'clause'}, errors are RECEIPTS (HTTP 200 + body),
     never exceptions across the wire, never a fabricated value. Nothing bypasses it.
  6. CONFIG & CONTENT AS DATA, not code. Curated model allowlists, tiers, parts, entity types/tiers,
     missions, specimens → JSON/config files. Adding content = editing data (an extensibility seam), never
     a hardcoded catalog inside a method (the current CURATED dict buried in a handler is the anti-pattern).
  7. TYPED + SELF-DOCUMENTING. Python type hints; JS JSDoc (or TS if a no-build path exists). Every file
     opens with a one-line responsibility + its NEW/PORT/KEEP class.
  8. CLIENT = NATIVE ES MODULES (import/export) — real modularity with NO build step (browsers load them
     over http). three.js r128 stays a global script; the game code is proper modules, not one window.GAME
     global with IIFEs. Evaluate this vs the current pattern and recommend.
  9. HONEST TEST LANE. Test real behavior via the unlimited local hearth (ollama) + REPLAYED real recorded
     traces (a measured record, not a mock) — never fake outputs. Add a contract test the client and seam
     both check the /game/* shapes against.
  10. ATOMIC, LOCKED STATE + ONE EVENT BUS. State writes stay atomic + file-locked (the existing idiom);
      all events flow through one observable bus/trace so the run is legible.
  Add any further best-practices or innovative structure you can defend — but every one must serve the
  honesty law and the size/modularity rules above, never decorate.

THE ONE HARD BOUNDARY (the moat, not a preference): the game's power is that a REAL autonomous AI actually
runs — real metered model calls, a real execution engine, real token draws, a measured autonomy battery,
real memory, the sacred save. That real BEHAVIOR is the honesty law and it is expensive to make true.
"From scratch" is the STRUCTURE, not the behavior. The entity's real integrations are PORT or KEEP, never
faked or rebuilt-from-nothing. If you reorganize the entity into new classes, treat it as careful surgery —
its state is live (see D8) — and stage + test each move. Present the trade (reorganize the entity vs
keep-and-wrap it) with a recommendation.

STEP 3 — STOP. Show me the full design. Write NO code until I approve the structure. On approval, the first
build is FIRST LIGHT (compose→ignite→run-or-fail; see design/FIRST_LIGHT_INTEGRATION.md).

GUARDRAILS: honesty law + claim ceiling (never "conscious/sentient") · the SACRED save
state/journey_save.json is never reset · no employer names, filesystem paths, or secrets in anything
committed · NO emoji · design first, present, get my approval, THEN code — the exit is first light.
```
