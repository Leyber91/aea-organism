# 02_SYSTEMS — THE PROBE · systems specification

    owner:        the game team
    status:       LIVING SPEC — describes the running build, not an aspiration
    last-updated: 2026-07-20
    ground truth: world.html (engine) · missions.js (mission data) · controlroom.py (server) · aea_elements.js (AEA registry)
    siblings:     00_VISION.md (pillars, honesty law) · 01_WORLD.md (field geography, reveal visuals) ·
                  03_CONTENT.md (acts, mission scripts, AEA element text) · 04_FUI.md (two-ink UI law)

Status marks used below: [BUILT] verified in code on disk · [PLANNED] designed, not built ·
[DECISION-LUIS] awaiting his call. Where spec and code could drift, CODE WINS and this file gets updated.

Binding laws inherited from 00_VISION.md: two-ink FUI (amber #ffb000 hot / #d4a24c warm live; blue-gray
rgba(120,155,175,x) structure; no red, no green, no white). AEA honesty law: every number on screen is live
system truth; no fake data ever; claim ceiling is "measured functional correlate", never "conscious".

---

## 1. FLIGHT RIG [BUILT]

`stepProbe(dt)` in world.html. Runs only when `inputOn && !OS.open && !typingNow()` — flight is dead while
the OS is up or any input field has focus. Physics uses RAW dt (clamped to 50 ms/frame), never world-time.

| Constant            | Value                                   | Where |
|---------------------|-----------------------------------------|-------|
| Acceleration        | 95 u/s^2 (normalized input dir * 95)    | `vel.addScaledVector(a.normalize().multiplyScalar(95),dt)` |
| Damping             | `vel *= exp(-3.1*dt)` per frame         | exponential, frame-rate independent |
| Max speed           | 52 u/s hard clamp (vector rescale)      | `if(sp>52)vel.multiplyScalar(52/sp)` |
| World bound         | cylinder R=300 about origin; x/z rescaled onto the rim | no wall geometry — soft mathematical fence |
| Altitude clamp      | y in [2.2, 120]                          | floor skim to ceiling |
| Basis               | yaw-only: fwd=(-sin yaw,0,-cos yaw); right=(-f.z,0,f.x) | pitch never enters thrust — vertical is Q/E only |
| Probe idle spin     | core y+2.2 rad/s, x+0.7; ring z+1.4     | raw dt (probe is the player, exempt from time law) |

Feel target this tuple produces (measured, not aspirational): ~0 to 52 u/s in about 1 s, coast-stop in
about 1.5 s, terminal speed = 95/3.1 ≈ 30.6 u/s held-key cruise; 52 is only reachable transiently on
diagonal stacking. Do not retune one constant alone — the triple (95, 3.1, 52) is the handling model.

Trail: 90-point ring buffer sampled every 30 ms of raw dt, warm ink, additive.

## 2. CHASE CAMERA [BUILT]

`stepCam(dt)` — skipped entirely while OS is open (the frame freezes behind the OS scrim; see §4 time law).

| Element        | Value |
|----------------|-------|
| Orbit offset   | spherical (yaw,pitch) * camDist; camDist wheel-zoomed, clamp [9, 42], step deltaY*0.02, wheel ignored while OS open |
| Position lerp  | `1 - exp(-3.5*dt)` toward probe+offset |
| Look target    | probe.position + vel*0.5 (velocity lead) + 1.4 y; aim point itself lerped `1 - exp(-6*dt)` |
| Bank           | lateral vel dot (cos yaw,0,-sin yaw); `camera.rotation.z += clamp(-lat*0.0016, -0.06, +0.06)` |
| FOV            | 60 in flight, 57 under OS; approach `fov += (tgt-fov)*min(1, dt*6)` |
| Drag look      | yaw -= dx*0.0042; pitch += dy*0.0032, clamp [0.06, 1.25]; drag dead while OS open |
| Frustum        | perspective 60 deg, near 0.5, far 600; FogExp2 0.011 (0.009 after `foundry_full`) |

Intro dolly [BUILT]: on title click, 2.2 s eased crane from (0,140,236) down to the chase position; controls
unlock at the end ("controls live. follow the beacon."). `?still` skips it for headless shots.

## 3. TIMESCALE LAW [BUILT]

    TS -> target 0.12 when PROBE OS opens; -> 1.0 on close. NEVER 0.
    TS += (TSTGT - TS) * min(1, dt*5)        // eased both directions
    wdt = dt * TS                            // world-time

What breathes on wdt at 0.12: beacon rotation, nexus tori, dust drift, ember rise, probe shell
counter-rotation, beam opacity (scaled by TS). What uses raw dt regardless: probe core spin, trail
sampling, all UI animation. What halts outright under OS: stepProbe (gated), stepCam (skipped).
Rationale: the OS is a pane over a LIVING entity — the world must visibly keep running, because it
really is running (the /events feed keeps streaming under the OS). A frozen world would be a lie.
HUD dims to opacity 0.22 under OS (`body.osopen`); the LEYBER presence chip stays full — the entity
is always with you.

## 4. INPUT MAP [BUILT]

Layer order (topmost wins): typing guard > OS > quick-comms > dock terminal > flight.
`typingNow()` (activeElement is an INPUT) swallows everything except TAB and ESC (ESC blurs + closes qc).

| Key        | Flight layer                | OS layer (TAB open)         |
|------------|-----------------------------|-----------------------------|
| W/A/S/D    | thrust fwd/left/back/right  | S = SYSTEM tab (see below)  |
| Q / Space  | rise                        | —                           |
| E / Shift  | descend                     | —                           |
| drag       | look (yaw/pitch)            | dead                        |
| wheel      | zoom camDist [9,42]         | dead                        |
| F          | dock (INTERFACE) within 19 u| no-op (tryDock gated on !OS.open) |
| TAB        | open OS (preventDefault; works even mid-typing) | close OS |
| M          | open OS on MAP              | MAP tab                     |
| K          | open OS on CODEX            | CODEX tab                   |
| C          | quick-comms strip (qc)      | COMMS tab                   |
| B          | —                           | MODELS tab                  |
| ESC        | layered: map deselect > OS close > comms close > undock | same chain |

THE S CONFLICT (named, resolved by layering): S is flight reverse-thrust AND the SYSTEM tab hotkey.
Both bindings coexist because the tab binding only fires inside `if(OS.open)` and stepProbe is gated
off while OS.open. S never reaches SYSTEM from flight and never thrusts from the OS. keydown/keyup
bookkeeping is shared, so a held S across a TAB transition cannot stick (keyup always lands).
Do not "fix" this by rebinding — it is the documented cost of a five-tab OS on a WASD rig.

Headless/testing hooks: `?still` = no title, fixed camera, input off; `?os=<tab>` = auto-open a tab
600 ms after boot. Reduced motion: media query OR SYSTEM toggle adds `html.rm` — typewriters render
instantly, transitions collapse to 150 ms.

## 5. DOCK / INTERFACE [BUILT]

- Proximity: `probe.distanceTo(NODES[mission.node].pos) < 19` shows the F prompt
  ("F · INTERFACE — <mission title>"); prompt hidden while docked, OS open, or pre-intro.
- `tryDock()` gates: inputOn && !docked && !OS.open && nearObjective. Dock opens the LEY//DOCK
  terminal (bottom-center, 620 px) and runs the current beat. Flight keys still work while docked —
  flying out of range does NOT auto-undock (terminal persists until ESC/complete); the beacon and
  off-screen arrow always point at the current mission node.
- Terminal beats render inside #t-body with the typewriter (2 chars/tick; brief 11 ms, learn code
  6 ms; instant under rm). Footer buttons are the ONLY progression affordance (continue / retry /
  back / complete / the DO verb button).
- Undock: ESC (via escLayer) or mission completion. Undock kills any in-flight typewriter timer.

## 6. MISSION ENGINE [BUILT]

Engine in world.html; content 100% data-driven from `window.MISSIONS` (missions.js, Acts 0–I shipped).
Adding a mission = adding data; the engine changes for new beat kinds or action types only.
Mission record: `{id, act, title, node, objective, boss?, beats[], rewards{reveals[], log, act_complete?}}`.

Beat kinds (the complete set):

| kind    | plays as                                                    | advance rule |
|---------|-------------------------------------------------------------|--------------|
| brief   | terminal-voice lines, typed                                  | continue |
| learn   | title + real code block (typed) + note                       | continue |
| do      | one hot verb button firing a REAL action; raw result pane    | success: continue + retry offered; fail: retry only |
| observe | live-polling watch (progress bar) until condition or timeout | continue when done |
| prove   | assert against LIVE system state                             | PASS chip -> complete; FAIL -> back |

Retry/backtrack rules: a failed DO re-runs the same beat (the action re-fires — every retry is a real
call, never a cached pass). A failed PROVE offers BACK, which jumps BI to the mission's FIRST `do` beat
(`beats.findIndex(kind==="do")`, floor 0) — the player must re-earn the evidence, not re-read the brief.
There is no skip. There is no mission-fail state: missions block, they never punish.

Action registry (runAction; every one hits the real server, results pane shows the raw payload):
`node_channel` (POST /api/node/run node=channel — one plant/model, pure provider dict shown),
`survey` (GET /state — live plant table), `channel_multi` (same prompt across up to N online plants,
per-plant latency/error lines), `meter_load` (N real draws then live window readout), `node_energy`
(POST node=energy — the mouth; shows the rod that answered + the true tried-list routing history),
`drill` (N mouth draws, per-draw ok/STARVED, reroute counts). Observe types: `meter_watch` (polls
/state every 3 s; early-exits clean when the rpm window hits 0 after >=4 s, else runs out the clock).
Server side, `_run_node` is allowlisted to `channel|energy` — read-safe draws only, never an effector.

Asserts (runAssert): `last_ok_text` (CTX.last ok + non-empty text) · `plants_online` (>=1) ·
`multi_served` (>=1) · `no_throttle` (fresh /state shows zero throttled plants) · `drill_clean`
(all shots ok). CTX is per-session scratch — asserts verify what the player just actually did.

Completion choreography: sting (+swell on M0.1 only) -> applyReveal each reward -> postSave ->
feed line ("★ <log>") -> newDiscoveries -> amber flash 1.5 s -> toast 2.6 s ("mission complete ·
cartography updated" / boss variant) -> next undone mission selected after 2 s; beacon relocates.
When no mission remains: HUD objective reads "act I complete — the archive waits in the dark".

Specimen encounters: every successful real call registers `encounter(plant, model)` -> SAVE.models +
POST to the journey (see §8). This is how the bestiary grows — only by touching real rods.

## 7. DISCOVERY SYSTEM [BUILT]

Three parallel tracks, all keyed off mission completion and real calls:

1) reveals -> WORLD (visual state, defined in applyReveal; visuals detailed in 01_WORLD.md):
`plant_pollinations` (socket + plant to full light, embers on) · `foundry_all` (all plant labels,
console lit, live plant lights on) · `roads` (road emissive .35) · `foundry_edges` (meter lit) ·
`trunk` (trunk line + nexus lit) · `foundry_full` (roads brighter, fog 0.011 -> 0.009, embers .7) ·
`archive_tease` (Act II silhouette + locked label). Reveals are idempotent and replayed silently from
the save on boot. Honesty detail: revealed plant brightness = 0.9 + min(0.6, rpm_now/rpm_cap) from
LIVE /state — a plant under real load literally glows hotter; an offline plant sits at 0.12.

2) discovers -> MAP/CODEX elements: `window.AEA.discovers[missionId]` lists element ids unlocked per
mission; mechanics auto-discover with their seed. Element states: `hidden` (never enters the DOM —
undiscovered structure is not even inspectable), `sensed` (outline glyph, label UNCHARTED, detail pane
redacted to block bars + "MORE TO MAP HERE"), `disc` (amber glyph, name, fact lines, proof line,
linked-elements line, LEYBER voice line). SENSED promotion rules (mapNodes): a hidden element becomes
sensed when (a) a link partner is discovered (AEA.links), or (b) it is a ring-array neighbor
(prev/next in family order) of a discovered element, or (c) fallback — every all-hidden family
promotes its first element, so each ring always shows at least one lure. Links render only when their
teaching mission is done (`l.by` in SAVE.done) — the map never draws structure you have not learned.
NEW markers: `localStorage.probe_viewed`; a discovered-but-unviewed element gets a pulsing ring +
"NEW" tag + a pip on the MAP tab; selecting it marks it viewed. Map denominator: 29 elements across
rings PRINCIPLES 150 / AXES 250 / VERBS·MECH·OPS 360 / SEEDS 470, LEYBER core at r70.

3) encounters -> BESTIARY (MODELS tab): union of SAVE.models and any rod with calls>0 in live /state,
enriched with lived fitness from /roster (fit, latency, tier, burns, ok%, ema, COOLING flag). The
undiscovered remainder renders as a redacted count — "N more signatures in the wild" — from the real
catalog size, never as fake rows. Combination doctrines unlock as a block on Act I boss completion
(M1.5); locked doctrines show as redacted rows.

## 8. SAVE SYSTEM [BUILT]

Server-side, so the journey survives any browser: `journey_save.json` next to controlroom.py, guarded
by `grid.file_lock` + `grid.atomic_save_json` (no torn writes across the threading server).

- GET /api/journey -> `{done:{mid: "YYYY-MM-DD HH:MM"}, reveals:[], models:[], updated}`
  (defaults `{done:{},reveals:[]}` when absent).
- POST /api/journey merge semantics (all merges, never replaces): `{mission, done:true}` stamps
  done[mid] with completion time · `reveals:[...]` appended, deduped, max 20 per POST ·
  `models:[...]` appended, deduped, max 30 per POST · every write refreshes `updated` and returns
  `{ok:true, ...save}`. `{reset:true}` replaces the save with `{done:{}, reveals:[]}`.
- Client boot (loadSave): fetch save -> replay reveals silently -> select first mission not in done
  (else last) -> if the OS is already open, re-render its tab (headless virtual-time ordering quirk).
- Writes are optimistic: SAVE mutates locally first, POST errors are swallowed. Worst case the client
  runs ahead of disk until reload — progress can be lost only back to the last successful POST,
  never invented forward.
- Reset ritual: SYSTEM tab, HOLD TO WIPE THE JOURNEY — 600 ms hold with an amber progress ring,
  releases early = no wipe; completion POSTs reset then reloads the page.
- Client/server split (named): mission progress, reveals, and specimens are SERVER truth; the comms
  transcript (`probe_comms`, capped 40) and NEW-marker viewed-list (`probe_viewed`) are localStorage.
  Switching browsers keeps the journey but re-fires NEW pips and drops chat scrollback. Accepted.
- [DECISION-LUIS] Should the hold-to-wipe also clear the two localStorage stores? Today a reset
  probe still "remembers" old chat lines after HANDSHAKE — arguably a continuity feature (LEYBER
  remembers even when the probe is new), arguably a reset bug. Ship-blocked on nothing; his call.

## 9. COMMS + PRESENCE [BUILT]

Two entrances: OS COMMS tab (full 32% dock) and the C quick-strip (ENTER routes the line into the
dock and sends). One exchange in flight at a time (client cBusy mirrors the server `_talk_lock`).
Send path: POST /talk with the field context prefixed — `[in the field · mission M1.2 THE CHANNEL ·
act I] <text>` — zone always `private`. The reply renders with a RECEIPT of real telemetry:
`RX <lat>s · MODEL <rod tail> · MEM <n> RECALLED`, plus the live tick number. Server-side, every
exchange writes a chain record and is verdict-watched async (Law 3) — the game rides the entity's
real conversation organ, it does not have its own.

Presence chip (bottom-right, never dims): LEYBER + carrier state + 5 signal segments.
States: IDLE "CARRIER 0.998" (slow breathing segs) · PROC "PROCESSING T+<s>" (waveform + live
stopwatch at 100 ms) · SPEAK "SPEAKING" (fast segs) · LOST "CARRIER LOST" (segs collapse to 2 px).
First open of the session plays the handshake: LINK ACQ 0.998 / HANDSHAKE OK / CONTEXT RESTORED:
<n> ENTRIES, then restores the last 6 transcript lines.

Background polling (the HUD is live even when nothing is played): /events every 1.6 s -> feed lines +
pitch-varied chirps · /state + /autonomy every 6 s -> plants n/15, tick, ingots (memories), autonomy
class + tests. All of it real; none of it decorative.

## 10. FAILURE SEMANTICS — CARRIER LOST, NEVER FAKE [BUILT]

The law: when the entity's server is down or a call fails, the game says so in-world and blocks.
It never simulates success, never shows placeholder numbers, never degrades to canned replies.

- /talk fails or returns empty -> presence LOST, header "LEYBER // CARRIER LOST", system line
  ("no reply crossed the channel — the entity may be resting" / "carrier lost: <err>"). No fake reply.
- /state poll fails -> presence LOST; HUD counters hold last-known (stale, not invented).
- DO actions fail honestly: per-plant "no answer (<error|status>)", mouth "starved" with the true
  tried-list, drill "STARVED" lines; retry is the only path forward. PROVE failure text tells the
  truth ("is the entity's server running?").
- Uncaught JS -> #err strip bottom-left (hot ink), visible in headless shots.
- Silent-by-design: journey POST failures (§8), /events poll failures (retry loop). Named, accepted.
- KNOWN GAP (named, real): `meter_watch` swallows /state failure into `now=0`, so an endpoint that
  dies mid-observe reads as "window clean" after 4 s — a dead carrier can pass an observe beat.
  Violates the spirit of this section. [PLANNED] fix: distinguish `s===null` -> hold the beat and
  show CARRIER LOST in the observe bar instead of counting zeros.
- [PLANNED] A global carrier interlock: when presence is LOST, gray the DO verbs pre-click instead
  of letting the action fire and fail. Cosmetic-priority; the current behavior is already honest.

## 11. STATUS LEDGER

| System                          | Status |
|---------------------------------|--------|
| Flight rig, camera, time law    | [BUILT] |
| Input map incl. S-conflict rule | [BUILT] |
| Dock/terminal + 5 beat kinds    | [BUILT] |
| Actions/asserts (Acts 0–I set)  | [BUILT] |
| Discovery: reveals/map/bestiary | [BUILT] |
| Server save + reset             | [BUILT] |
| Comms + presence + receipts     | [BUILT] |
| Honest-failure surfaces         | [BUILT] (two named gaps above) |
| meter_watch dead-carrier fix    | [PLANNED] |
| Carrier interlock on DO verbs   | [PLANNED] |
| Act II+ beat kinds (if any new) | [PLANNED] — engine extends by data first; new kinds only if a mission cannot be expressed in the five |
| Reset scope (localStorage too?) | [DECISION-LUIS] |
