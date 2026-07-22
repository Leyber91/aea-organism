# FIRST_LIGHT_INTEGRATION.md — the exact real calls for the seam (BUILD reference, not design)

Engineering map from a 5-reader substrate scout (2026-07-22). Read this before writing `aea/gameapi.py` +
wiring the client — it is the exact contract, so the seam calls the REAL organs and never fabricates.
Pairs with `design/CLEAN_ARCHITECTURE.md`. (This is a code map; it is NOT new design corpus.)

## The seam (gameapi.py): ThreadingHTTPServer on **127.0.0.1 only** (privacy, non-negotiable). ALL replies
are HTTP 200 + JSON body — errors/refusals ride inside the body (`ok`/`refused`/`error`), never 4xx/5xx.
Import the PRESERVED organs (`bench_core, grid, energy, controlroom` logic); never reimplement them.

## COMPOSE → IGNITE → RUN-OR-FAIL — use THE BENCH (the truer model)
- **POST `/game/ignite` `{spec, task:'t-01'}`** → `out = bench_core.start_run({'spec':spec,'task':'t-01'})`.
  Returns INSTANTLY (threaded; **one run at a time** — a 2nd ignite while live is *refused*, not queued).
  `out['ok']` → `{run_id}`. `'refused' in out` → `{ok:false, refused: out['refused']}` (honesty law, verbatim).
  `'error' in out` → infra failure. (Optionally `bench_core.validate_spec(spec)` for a compose-time verdict,
  no run minted.)
- **GET `/game/run?id=`** → `bench_core.run_status(id)` (reads `state/bench_runs.json` = truth every call;
  poll ~300ms). Returns `{status:'running'|'done'|'halted'|'lost', links:[{seq,part,ms,ok,receipt}],
  open_link, construct, task, zone, parts, total_ms, run_ok, pass, axes:{latency_ms, tokens, ok, zone},
  halted_at, receipt, last_ms, best_ms}`. **`halted` = the visible blue fail** (`halted_at` = which part);
  `lost` = CARRIER LOST (silent). Pass the dict through largely as-is.

### The construct spec (client → seam; from DEFAULT_CONSTRUCT)
```
{construct_version:'0.1.0', id:'c-01', parts:['tap','scorer'], wiring:[['tap','scorer']],
 rods:{default:{tier:'local'}}, policies:{}, zone:'private'}   # zone REQUIRED: private|sensitive|public
```
- FIREABLE = `tap, scaffold, governor, ladder, scorer`. Real entry points: **tap→`energy.draw` (the ONLY
  token burn)**, scaffold→`bench_core.scaffold`, governor→`grid.METER.can_spend`, ladder→`energy.ladder`,
  scorer→`bench_core.score`. **BRAIN = `tap`** (its tier picks model class; zone routes rods). Min ignitable = `tap+scorer`.
- **SPEC LAW** (validate_spec enforces, else refused): `parts[0]` MUST be `tap`; if `scorer` present it MUST
  be last; no dupes; every part BUILT+fireable in `state/modules.json` (confirm that file exists).
- Only `scaffold.template` policy is honored; any other policy key is refused as a fake lever.
- P0 ships ONE task `t-01` (prompt pinned: "Reply with exactly one line: PROBE ONLINE"). **No player free
  prompt yet** — a custom prompt needs a new TASKS entry (unwired). Flag for the "wonder before mechanism" beat.

## The MVO (BRAIN + LOOP) — the smallest real thing
- **BRAIN = `energy.draw(prompt, tier='frontier'|'local', zone='private')`** → `{ok, text, plant, model,
  latency, tried[]}`. Never raises; **empty text from a live rod = FAILURE** (honest). `ok=False` →
  `{ok:false, text:'', plant:None, ...}` → dash / blue-fail, no fabrication. (`aea.core(prompt)` is the thin wrapper.)
- Show WHICH rod burns BEFORE ignite (no tokens): `energy.ladder(tier,zone)[0]` → `(plant,model)` = the
  honest "BRAIN = <model>" label.
- **LOOP has NO bench part** — the one place the game's model and the engine diverge. The MVO heartbeat =
  `aea.main`'s skeleton `for i in range(n): ...; time.sleep(3)`, but with the tick body reduced to a single
  `energy.draw()` call. **BYPASS `aea.tick`/`sense`/`structure`/`hades`** (they add 2 live fetches + 2 extra
  model calls; and need `state/aea_seed.md`). LOOP is a seam/client concept wrapping repeated draws.

## Guard the awe-beat on the LOCAL HEARTH
- `PLANTS['ollama']` = local, keyless, `rpm=None/rpd=None` → **unbrownoutable** (`can_spend` always
  `(True,0,'ok')`). Use `tier='local'` for the first-light chord so a 429 can never starve it. Its only
  failure = ollama daemon down (→ honest blue-fail). Verify installed tags with `ollama list` (LOCAL_FLOOR
  tags may differ), or trust `tier='local'` to walk the floor.
- The rpm=4 keyless SOCKET = `PLANTS['pollinations']` (privacy='none' → `zone='public'` only; ~1 req/15s,
  serialize). Reserve it for the Act-I scarcity LESSON, never the keystone.

## The read endpoints (re-home from `controlroom.py`; call the SAME functions)
- **GET `/game/state`** → `controlroom.state()` → `{identity, life, memory, energy:{plants[{plant,privacy,
  rpd,tokens,rpm_now,rpm_cap,rpd_cap,throttled}], rods[{rod,calls,ok,ema_latency,cooling}], census},
  trust, brief[]}`. The client's `refreshGrid()` reads `energy.plants` (looks up `pollinations`
  rpm_now/rpm_cap, rpd_cap; counts non-cooling `rods`).
- **GET `/game/catalogue`** → `controlroom.roster()` (`fitness_top`, `candidates`).
- **GET `/game/events`** → `controlroom.journal()` (or `pulse.tail`).
- **GET `/game/schema`** → `state/schema.json` (the fog map).
- **GET+POST `/game/save`** → `controlroom._journey` — **the SACRED save** `journey_save.json`
  `{done, reveals, models}`. Merge under `grid.file_lock`; never reset unasked.
- EXCLUDE from the seam: `_do` play/stop/tick (spawn OS processes) — not read-safe.

## Client wiring (`web/game/`) — mostly REPOINTING, not building
- `bench.js` already does compose→ignite→poll→render **inline** (`specNow / fire / schedulePoll /
  normalizeRun / applyStatus`). **"run:link has no listener" is a red herring** — bench.js never touches
  `GAME.bus`; the flow is inline function calls. Don't hunt for a listener.
- **FIRST LIGHT = repoint THREE fetch sites:** `fire()` POST `/api/construct/run` → `/game/ignite`;
  `schedulePoll()` GET `/api/construct/run?id=` → `/game/run?id=`; `refreshGrid()` GET `/state` → `/game/state`.
- **Change the refusal read:** bench reads `j.error`; the seam returns `{ok:false, refused:'clause'}` → read
  `j.refused` (or have the seam also echo `error`).
- Optionally add `core/api.js` (the only server-talker) after `engine.js` in `index.html`'s `<script>` list
  + inline init (before `BENCH.init`). For the minimal slice, repointing bench's inline `api()` calls is enough.
- Client tolerances: run_id accepted as `j.run_id || j.run.run_id`; `normalizeRun` reads `j.run.*` or flat
  `j.*`; per-link `L.ms` is server `perf_counter` (never client-invented); dash-law already enforced
  client-side (`chipStat`='—' when grid falsy; header 'CARRIER LOST' on fetch fail). `?still` disables the
  network for headless verify; `?still&bench=1` force-docks the plate.

## HANDS (later — flagged, NOT in BRAIN+LOOP first light)
BRAIN (`energy.draw`) and HANDS (`agent_tools.chat/run_agent`) are **separate code paths**: agent_tools
bypasses the Meter + ladder, hardcodes `nvidia / meta/llama-3.3-70b-instruct`, temp 0.1, and RAISES on error.
`energy.draw` has **no `tools` param**. Attaching HANDS = adopting agent_tools' loop (unmetered) OR extending
`draw()` to pass tools — real work, not a config flag.

## Honesty guarantees already native (formalize, don't reinvent)
Refusal → `{ok:false, refused:'clause'}`. Absent → null → dash (`grid.load_json(path,default)`; **`tokens`
is permanently `None` at P0 → render a dash, never 0**; any `None` cap = dash, never ∞). Curated allowlist —
the client may NEVER pass an arbitrary model string. `grid.call_openai` does NOT meter — if used directly,
`METER.can_spend` before + `METER.record` after (+ `mark_throttled` on 429); prefer `energy.draw`.
