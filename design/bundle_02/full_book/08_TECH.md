# 08_TECH — THE PROBE technical architecture

    owner: the game team
    status: LIVE — describes the running build, not an aspiration
    last-updated: 2026-07-20
    ground truth: world.html · controlroom.py · missions.js · aea_elements.js · journey_save.json
    corpus siblings referenced by filename (update if a sibling lands under another name):
    01_VISION.md (premise + honesty law) · 03_MISSIONS.md (beat grammar) · 04_WORLD.md (field layout)
    05_UI.md (BINDING UI SPEC v1.0, two-ink law) · 06_AEA_MAP.md (codex/rings) · 07_COMMS.md (the channel)
    repo companions: GAME_PLAN.md (ASCENT v2 acts) · AEA_PROOF_PLAN.md (taxonomy) · AUTONOMY_BATTERY.md

Every section is tagged [BUILT] (verified in code on this date), [PLANNED] (designed, not
built), or [DECISION-LUIS] (awaiting his call). Every number below was read from the files,
not remembered.

---

## 1. The stack [BUILT]

One HTML file is the whole game client: `world.html` (~1120 lines, no build step, no
framework, no bundler). It is served by the entity's own server and runs in a plain browser.

**three.js r128, GLOBAL build.** `three.min.js` on disk carries `REVISION="128"`. Everything
attaches to `window.THREE`. The post-processing addons are the classic `examples/js` style:
IIFEs that assign `THREE.EffectComposer`, `THREE.Pass`, etc. There are NO ES modules, NO
import maps, NO CDN.

**Law: no newer APIs.** r128 predates the modern module-only three.js. Code written for this
game must use only r128 API surface (e.g. `THREE.FogExp2`, `MeshStandardMaterial`,
`sRGB`-era color handling, `ACESFilmicToneMapping`). Do not paste snippets from current
three.js docs — `outputColorSpace`, `addons/` imports, and post-r150 idioms will silently
break or throw. `window.onerror` paints failures into the `#err` strip; a blank strip after
boot is the smoke test.

**The three-stack on disk (8 files):**

| file | role | loaded by world.html |
|---|---|---|
| `three.min.js` | r128 core, global | yes — FIRST |
| `CopyShader.js` | bloom dependency | yes |
| `LuminosityHighPassShader.js` | bloom dependency | yes |
| `EffectComposer.js` | defines `THREE.Pass` base + composer | yes |
| `ShaderPass.js` | extends `THREE.Pass` | yes |
| `RenderPass.js` | extends `THREE.Pass` | yes |
| `UnrealBloomPass.js` | the bloom | yes — LAST of the chain |
| `OrbitControls.js` | sibling views (/city, /mind) only | NO |

**Load order law** (world.html lines 296-304, do not reorder):

    three.min.js -> missions.js -> aea_elements.js ->
    CopyShader -> LuminosityHighPassShader -> EffectComposer ->
    ShaderPass -> RenderPass -> UnrealBloomPass

`ShaderPass`, `RenderPass`, `UnrealBloomPass` all extend `THREE.Pass`, which is DEFINED in
`EffectComposer.js` — composer must precede the passes. `UnrealBloomPass` constructs
`CopyShader` and `LuminosityHighPassShader` materials — the shaders must precede it. The
data files (`missions.js`, `aea_elements.js`) are plain scripts that set `window.MISSIONS`
and `window.AEA`; the engine reads them at boot, so they load before the main inline script.

**Composer chain** (world.html line 359-364): `RenderPass -> UnrealBloomPass(res, 0.65,
0.4, 0.5)` (strength, radius, threshold). The whole composer is built inside `try/catch`;
on any failure the game falls back to `renderer.render()` — the game must remain playable
with bloom dead. Film/Vignette/Gamma passes are NOT on disk; CSS carries that texture
(see Deviations, section 7).

## 2. The server contract — controlroom.py [BUILT]

`python controlroom.py` = `ThreadingHTTPServer` hard-bound to `127.0.0.1:7799`. Local only,
by construction — the bind address is a literal, not a config. THE PROBE is served at
`GET /world`; it calls back into the same origin for everything.

### 2.1 Game-facing GET endpoints

| endpoint | shape (verified) | game use |
|---|---|---|
| `/state` | `{t, identity{name,born,voice}, life{alive_since,wakes,ticks,last_brief,recent[],log[]}, memory{sessions,memories}, mind{turns[]}, energy{plants[],rods[],census{frontier,generated}}, trust{cap:{level,streak,runs,fails}}, brief[]}` — `plants[]` rows: `{plant,privacy,rpd,tokens,rpm_now,rpm_cap,rpd_cap,throttled[]}` | plant lights, HUD tick/ingots, survey + meter missions, throttle asserts |
| `/events?since=<epoch>` | array of pulse records `{t,organ,action,detail,ok}` | the bottom-left live feed (poll 1.6s) |
| `/autonomy` | `autonomy.score()` -> `{class, passing, total, ...}` or `{error}` | HUD `class` + `tests` counters (poll 6s) |
| `/roster` | `{fitness_top[{rod,fit,lat,tier}], fitness_generated, candidates, excluded[]}` | MODELS tab: lived fitness per specimen |
| `/api/schema` | raw `schema.json` bytes (code contracts, no secrets) | THE ASCENT board (`/game`); PROBE Act II+ codex deep-dives [PLANNED] |
| `/api/journey` | current `journey_save.json`: `{done{},reveals[],models[],updated}` | `loadSave()` at boot |

`/journal`, `/skills`, `/chains`, `/decisions` exist for the dashboard; the game does not
call them today. They are same-origin and read-only — free to adopt in later acts.

### 2.2 Game-facing POST endpoints

| endpoint | request | response | law |
|---|---|---|---|
| `/api/node/run` | `{node:"channel", plant, model, prompt}` or `{node:"energy", prompt, tier?, zone?}` | `{ok, node, elapsed, pure:{...}}` — `pure` is the RAW provider/router dict (`ok, latency, text, tokens, tried[], plant, model, status, error`) | allowlist is exactly `channel` and `energy`. Read-safe draws only, never an effector. The board shows the true API response, not a mock. |
| `/api/journey` | `{mission, done:true, reveals[], models[]}` or `{reset:true}` | `{ok, ...merged save}` | file-locked atomic merge; per-POST caps `reveals[:20]`, `models[:30]`; server stamps `done[mid]` with local time |
| `/talk` | `{text, zone:"private"\|"local", speak?}` | `{reply, ok, rod, latency, zone, memories[], events[]}` | serialized by a lock (one exchange at a time). Every exchange writes a chain record to `chains.jsonl` and spawns an async watcher verdict (Law 3) — accept/redo logged, never blocking the reply. `zone:"local"` maps to sensitive -> local rod only. |
| `/do` | `{cmd}` where cmd in `brief, consolidate, status, play, stop, tick` | `{ok, out}` | the motor cortex allowlist. Nothing arbitrary executes. The PROBE client does not call `/do` yet — Act II field missions (mine a corpus slice, run a tick) will [PLANNED]. |

COMMS prepends mission context to `/talk` text: `"[in the field · mission M1.3 THE METER ·
act I] "`. The entity answers from its real state; the receipt line (`RX 1.42s · MODEL x ·
MEM 3 RECALLED`) is built from the response fields, never invented.

### 2.3 The static allowlist law [BUILT]

`_static_path()` serves ONLY: (a) a FLAT basename — `os.path.basename()` strips any
traversal; (b) an extension in `_CTYPES`: `.js .css .png .svg .woff2 .map .ico .wav .mp3`.

Consequence, and the law it encodes: **`.py`, `.md`, and every state `.json` are
unreachable over the socket.** `luis_memory.json`, `grid_state.json`, `aea_state.json`,
`talk_state.json`, `.env`, the source organs — none can be fetched, ever. `.json` is
deliberately absent from the allowlist; state that the game needs crosses only through the
typed endpoints above, which shape and bound what leaves disk. Any future asset need
(fonts, audio files) must fit the existing extensions or amend `_CTYPES` consciously — the
amendment is a security review, not a convenience edit.

## 3. Data files [BUILT]

**`missions.js`** — `window.MISSIONS`, data ONLY (the engine lives in world.html). Acts 0-I
authored: `M0.1, M1.1-M1.5`. Beat kinds: `brief | learn | do | observe | prove`. `do`
actions are typed (`node_channel, survey, channel_multi, meter_load, node_energy, drill`)
and every one resolves to a real endpoint call; `prove` asserts (`last_ok_text,
plants_online, multi_served, no_throttle, drill_clean`) verify against live responses or
fresh `/state` reads — a mission cannot pass on a dead server. `rewards.reveals` are the
world-lighting keys (section below). Terminal voice: lowercase, terse. See 03_MISSIONS.md.

**`aea_elements.js`** — `window.AEA`: the codex. 29 elements (5 axes, 10 seeds, 3 verbs,
4 mechanics mirroring seeds 3/4/5/7, 4 ops, 3 principles), ring geometry (core r70; rings
150/250/360/470 in a 1000-viewBox), `links {from,to,by}` drawn only after mission `by`
completes, `discovers` map (mission -> element ids), and 6 combination doctrines with
measured evidence strings. Every element carries a `proof` naming the real script that
proved it. See 06_AEA_MAP.md.

**`journey_save.json`** — the save of record, SERVER-side so progress survives any browser:

    { "done":    { "M0.1": "2026-07-20 13:23", ... },   // mission id -> completion stamp
      "reveals": [ "plant_pollinations", ... ],          // world-lighting keys, append-only
      "models":  [ "pollinations/openai-fast", ... ],    // specimen bestiary (real encounters)
      "updated": "..." }

Semantics: `done` gates mission progression (`MI = first not-done`); `reveals` are
idempotent lighting/fog mutations replayed at every boot (`applyReveal(r, silent=true)`);
`models` records only rods that actually answered (`encounter()` fires on `ok` responses,
including every hop of a `tried[]` reroute). Reset is a deliberate two-step: hold-to-wipe
UI (600ms hold) -> `POST {reset:true}` -> reload. Two localStorage keys exist and are
cosmetic only, never authoritative: `probe_viewed` (map NEW pips), `probe_comms` (comms
transcript, last 40 lines).

## 4. Performance budgets [BUILT]

| budget | value | where enforced |
|---|---|---|
| frame target | 60 fps on Luis's machine | design law; verify by eye + feed cadence |
| pixel ratio | `Math.min(devicePixelRatio, 2)` | world.html renderer setup |
| particles | dust 800 (camera-wrap box) + embers 180 (foundry) | `DUSTN=800`, `EMBN=180`; plus 1200 static stars, 90-point trail |
| post passes | exactly 2 (Render + Bloom) | composer chain |
| draw horizon | camera far 600 · sky r400 · world clamp r300 · FogExp2 0.011 (0.009 after `foundry_full`) | scene setup |
| polling | `/events` 1.6s · `/state`+`/autonomy` 6s · comms ticker 100ms only while waiting | pollEvents/pollTracks |
| time scale | PROBE OS open -> TS 0.12, never 0 (world breathes) | animate loop |
| lights | hemisphere + probe point light — exactly two | scene setup (§5 of the UI spec) |

**Single-WebGL-context law.** THE PROBE opens in ITS OWN window/tab, never inside a
dashboard iframe. Dashboard iframes spend GPU contexts from the browser's small per-process
pool; burning them churns the context pool and kills sibling canvases (the LUMEN lesson,
learned the hard way on luisblanco.dev). One game, one window, one context, one composer.

## 5. Verification recipes [BUILT — hard-won]

**Headless screenshot** (the only honest "it renders" evidence):

    chrome --headless=new --disable-gpu-sandbox --use-angle=swiftshader
           --window-size=1600,900 --virtual-time-budget=9000
           --screenshot=<out.png> "http://127.0.0.1:7799/world?still&os=<tab>"

- `?still` — skips the title screen, disables input, parks the camera at a fixed vantage
  (64,22,128 looking at 100,6,76). Deterministic frames.
- `?os=map|models|codex|comms|sys` — opens the PROBE OS on that tab at t+600ms.
- swiftshader is REQUIRED headless; without it the WebGL canvas is black.

**The save-race lesson (world.html:582).** Under `--virtual-time-budget`, virtual time
fires the `?os=` timer BEFORE the `/api/journey` fetch resolves — the OS renders an empty
save, then the save lands. Fix, in code: `loadSave()` ends with `if(OS.open) osTab(OS.tab)`
— re-render the open tab on save arrival. Any future async boot data must follow the same
pattern: render immediately, re-render on arrival. Never assume fetch-before-timer.

**TODAY'S GPU LESSON (2026-07-20).** swiftshader UNDERSELLS bloom: the software rasterizer
renders emissives dimmer and the UnrealBloom halo tighter than real hardware. A scene tuned
hot until swiftshader screenshots look right will BLOW OUT on the real GPU. Law: tune
emissive intensities conservatively against swiftshader shots, then verify the final grade
on real hardware before calling a lighting change done. Headless shots prove geometry,
layout, and state wiring — they are NOT the color-grade ground truth.

## 6. Deviations ledger

Deliberate departures, named so they never get "fixed" by accident:

| deviation | why | tag |
|---|---|---|
| Film/Vignette/Gamma passes absent from disk; CSS `#vig` (radial vignette) + `#scan` (scanlines, 0.03) carry the texture | fewer passes, fewer files, same read; named in code (world.html:359) | [BUILT] |
| Composer wrapped in try/catch -> plain-render fallback | bloom is garnish; the game must run without it | [BUILT] |
| IBM Plex Mono loaded from fonts.googleapis.com — the ONE external network dependency; falls back to Consolas/monospace offline | `.woff2` is already in the static allowlist; self-hosting is a 10-minute close | [DECISION-LUIS] self-host the font and go fully offline? |
| Audio is oscillator-only (WebAudio) — zero audio assets | keeps the client one file + the stack lean; `.wav/.mp3` allowlist entries exist for sibling views | [BUILT] |
| `OrbitControls.js` on disk but unused by the game | serves /city and /mind; do not delete | [BUILT] |
| `--dump-dom` and DOM-based headless assertions | not used; screenshot-only verification (dump-dom is unreliable in this environment) | [BUILT] practice |

## 7. Honest boundaries — what the game may NEVER fetch or serve

These are laws, not defaults. They inherit from the AEA honesty law (01_VISION.md) and the
privacy boundary proven in `brief.py`.

1. **Never served:** `.py` source, `.md` docs, any state `.json`, `.env`, keys. Enforced
   structurally by the extension allowlist + flat-basename rule (section 2.3), not by a
   deny-list that can rot.
2. **Never bound beyond loopback.** `127.0.0.1` is a literal. Exposing the port (tunnel,
   0.0.0.0, port-forward) is out of contract — the server assumes a trusted single user.
3. **Never a direct external call from the client.** The game speaks only to its own origin
   (plus the flagged font fetch). Every model draw crosses `/api/node/run`, which allowlists
   `channel` and `energy` and returns the raw truth. The client holds zero keys.
4. **Never an effector from the UI.** `/api/node/run` runs read-safe draws only; `/do` runs
   six named commands. There is no path from a browser input to arbitrary execution.
5. **Never a fake number.** Every HUD value binds to a live endpoint field; failures render
   AS failures (CARRIER LOST, STARVED, FAIL, COOLING) — the fail states are content, not
   errors to hide. No mission can pass against a mock.
6. **Never above the claim ceiling.** "Measured functional correlate" is the highest claim
   any screen makes; "conscious" appears nowhere, including flavor text. The SYSTEM tab
   renders the clause verbatim.
7. **Two-ink FUI is law** (05_UI.md): amber `#ffb000` hot / `#d4a24c` warm for the live and
   the earned; blue-gray `rgba(120,155,175,x)` for structure. No red, no green, no white,
   no emoji, three type sizes, one panel recipe.
8. **Sensitive zone stays local.** `/talk` with `zone:"local"` routes to the local rod only,
   and its watcher verdict also runs local. Private data never leaves the machine — proven
   behavior, inherited by the game unchanged.

## 8. Open items

- [PLANNED] Act II field missions wire `/do consolidate` + `/do tick` into DO beats
  (server side already allowlisted; client actions not yet authored) — GAME_PLAN.md §4.
- [PLANNED] `/api/schema` consumption inside THE PROBE (codex deep-dives reading the real
  code-contract graph; today only /game uses it).
- [PLANNED] Act II world: THE ARCHIVE geometry exists only as the locked tease
  (`archive_tease` reveal).
- [DECISION-LUIS] Self-host IBM Plex Mono (section 6) — closes the last external fetch.
- [DECISION-LUIS] Phase B posture: before anyone else runs THE PROBE against their own AEA,
  re-audit sections 2.3 and 7 as a hostile-user threat model (today's contract assumes
  player one is the machine's owner).
