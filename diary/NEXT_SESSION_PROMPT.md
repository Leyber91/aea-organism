# NEXT SESSION — kickoff prompt (build first light on the clean package)

Paste the block below into a fresh conversation opened in this repo (`aea-city`). `CLAUDE.md` auto-loads
here and routes the session. **Superseded the earlier "design the codebase from scratch" prompt: the aea/
subfoldering is now DONE** (10 domain subpackages, verified, committed `aa926ad` — see `SESSION_LOG` later·8),
so the next artifact is CODE — first light. Written 2026-07-22.

---

```
You are continuing THE PROBE (this repo, aea-city). A major structural step is DONE; the next artifact
is CODE — first light. Orient, confirm the current state, then build. Do not re-design what's built.

STEP 1 — ORIENT (read, in order):
  graph.json  ->  the "later·8" and "START HERE" entries atop diary/SESSION_LOG.md  ->
  design/CLEAN_ARCHITECTURE.html (the codebase design; read its STATUS banner)  ->
  design/FIRST_LIGHT_INTEGRATION.md (the exact real seam calls)  ->  DISCOVERIES D9-D12
  (D12 = the expert-panel verdict + the HOLD-THE-LINE list).

STEP 2 — CURRENT STATE (decided/done — do NOT redo):
  - The aea/ substrate is now 10 domain subpackages: kernel/ mind/ energy/ memory/ bench/ io/ organs/
    loop/ server/ tooling/ (DONE, verified end-to-end, committed aa926ad). Imports are
    `from aea.<pkg> import <mod>`. Run: `python controlroom.py` (shim -> `python -m aea.server.controlroom`,
    :7799). The entity's real behavior is UNCHANGED and PRESERVED — never rewrite it.
  - This SUPERSEDES CLEAN_ARCHITECTURE's "KEEP-AND-WRAP the flat entity" trade — the entity is already clean.
  - The four gate questions are resolved: entity subfoldered (done); client = native ES modules (approved);
    controlroom dissolves into a seam package (aea/gameapi/ or aea/seam/) + a thin admin.py (the plan, NOT
    yet built); GO for first light.

STEP 3 — BUILD FIRST LIGHT (the compose->ignite->run-or-fail verb; follow FIRST_LIGHT_INTEGRATION.md):
  - The honest seam: stand up the gameapi package — the honesty firewall (absent->dash, refusal->
    {ok:false,refused}, receipts-not-exceptions) wrapping the REAL organs: bench_core.start_run /
    run_status behind /game/ignite + /game/run, controlroom.state() behind /game/state. Call the real
    organs; never reimplement them.
  - The client: core/api.js (the only server-talker) + repoint web/game/js/bench.js's three fetches
    (fire / schedulePoll / refreshGrid) at /game/*, and switch the refusal read to j.refused.
  - Guard the awe-beat on the UNLIMITED local hearth (ollama), never the rpm=4 socket.
  - First light = a composed creature (BRAIN + LOOP) ignites, wakes on its own tick, draws a real token,
    prints its thought — OR fails visibly in blue. Verify on a swiftshader screenshot (serve over http).
  - STOP and show Luis the screenshot before building anything more.

GUARDRAILS: honesty law + claim ceiling (never "conscious/sentient") · the SACRED save
state/journey_save.json is NEVER reset · no employer names / filesystem paths / secrets in anything
committed · NO emoji · the entity (aea/) is PRESERVED · commit locally, do not push without Luis's word ·
the exit of first light is a working screenshot, not more docs.
```
