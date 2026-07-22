# ROOT REORG — the exact, mapped refactor (execute first, with the server running)

**Why this is a checklist and not a file-move:** the entity finds its own state through a path
model — `HERE = dirname(abspath(__file__))` (grid.py:30), 75 calls through `grid.load_json` /
`atomic_save_json` (bare filenames, working-directory-relative), 5 direct opens anchored to `HERE`,
and 3 subprocess calls with `cwd=HERE`. Moving any file without rewiring this splits or resets
state. grid.py's own note: *"continuity lives in the files."* So this is done as ONE coherent
change, tested, not as loose moves. **It is fully git-recoverable (`bc825ce`, pushed to AEA_GAME) —
if a state write goes wrong, `git checkout HEAD -- state/` restores it.**

## Target root (from ~90 loose files to this)

```
README.md  SESSION_LOG.md  GAME_PLAN.md  REORG_PLAN.md  .gitignore
runtime/   all the .py (server + entity organs) — co-located so flat imports keep working
state/     all runtime .json / .jsonl (grid_state, journey_save, self, heartbeat, events…)
web/       world.html tracker.html game.html + three.js libs + aea_elements.js + missions.js + game/
design/  docs/  archive/  voice/
```

## The precise changes (every site mapped 2026-07-22)

### 1. State layer — grid.py
- Add: `STATE_DIR = os.path.join(HERE, "state")`; `os.makedirs(STATE_DIR, exist_ok=True)`.
- Add resolver `_state(p)`: if `os.path.dirname(p) == ""` return `os.path.join(STATE_DIR, p)` else `p`.
- Apply `_state(path)` at the top of **`atomic_save_json`**, **`load_json`**, **`file_lock`** — so
  `.tmp` / `.lock` / `.corrupt` derivations (which happen after) also land in `state/`.

### 2. The 5 direct opens → route to `state/`
- `autonomy.py:36` `heartbeat.json` · `autonomy.py:41` `self.json` — change `os.path.join(HERE, x)` → `os.path.join(HERE, "state", x)`.
- `brief.py:19` `private_today.json` — change to `grid.load_json("private_today.json", {})`.
- `controlroom.py:333` `schema.json` · `controlroom.py:390` `tickets.json` — `os.path.join(HERE, "state", x)`.

### 3. jsonl / bounded-json append writers → route to `state/`
Locate and route each (they append, so a miss = a split log): `events.jsonl` (pulse.py),
`chains.jsonl` (controlroom.py:28 helper), `bench_runs.json` (bench_core.py:57 idiom),
`decisions.jsonl`, `reflections.jsonl`, `brief_trace.jsonl`. Prefer routing through `grid._state`.

### 4. Python → `runtime/`
- `git mv *.py runtime/` (all together → flat imports still resolve; they're co-located).
- Run entry: add a 3-line root `controlroom.py` shim (`import runpath; runtime/controlroom`) OR
  document `python runtime/controlroom.py`. `HERE` becomes `.../runtime`; `STATE_DIR = HERE/../state`
  or an explicit repo-root anchor — pick ONE anchor and use it everywhere.
- `controlroom.py:621/626/657` subprocess `cwd=HERE` → set cwd to the repo root so subprocessed
  `brief/consolidate/live` read the SAME state dir as the server.

### 5. Web → `web/`
- `git mv world.html tracker.html game.html *.js game/ web/`.
- Server static base → `web/`. `game/index.html` uses absolute `/CopyShader.js`, `/aea_elements.js`
  — either keep the server mapping `/x.js` → `web/x.js`, or rewrite those refs. `world.html` uses
  relative refs → unchanged (moves with the libs).

## TEST after the change (do not skip)
1. `python -m py_compile runtime/*.py` — all compile.
2. `python runtime/controlroom.py --port 7800 --no-open` — starts clean.
3. `curl :7800/world` `curl :7800/api/tickets` `curl :7800/state` — all 200 with real data.
4. Trigger a write: `curl :7800/api/journey` (save) and one tick — then **confirm NO new `.json`
   appeared at repo root** (all writes went to `state/`) and `state/journey_save.json` still holds
   `M0.1` + `M1.1`. If a stray file appears at root, that's the missed write site — fix it.
5. Only then commit.

**Rule:** never runs blind. If any step can't be verified, `git checkout` and stop — the mapped
sites above make the retry mechanical.
