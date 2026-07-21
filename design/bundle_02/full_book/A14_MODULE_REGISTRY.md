# A14_MODULE_REGISTRY — THE MODULE REGISTRY

```
doc:          A14_MODULE_REGISTRY.md (THE PROBE design book — the code-management chapter)
owner:        the game team (four-master fusion, per 00_VISION.md section 3)
status:       ACTIVE as design — answers Luis's architecture question of 2026-07-20;
              the manifest itself is [PLANNED], its substrate is largely [BUILT]
last-updated: 2026-07-20
governs:      how modules are declared, gated, composed, accounted, and exported; binds
              the construct spec format for the bench (R1_EVIDENCE.md composition reframe)
              and the export bundle of A5_PHASE_B.md
ground truth: ../controlroom.py (ORGANS_DOC, /skills, allowlists) · ../trust.py (CHARTER,
              check/record) · ../grid.py (key(), PLANTS, atomic stores) · ../energy.py
              (tiers, zones, cooling) · ../agent_tools.py · ../memory.py ·
              ../index_codex.py · ../telegram_bridge.py · ../reflect.py
siblings:     A9_FORGE_PROTOCOL.md (how modules come to exist) · A7_BUILD_LAYER.md
              (policies, the no-fake-lever law) · A10_LIVING_GAME.md (drift, tombstones) ·
              A5_PHASE_B.md (the wild) · 02_SYSTEMS.md (engine, save) · 03_PROGRESSION.md
              (acts, bosses) · R1_EVIDENCE.md (the bench). On conflict, 00_VISION.md and
              A1_PLAYER_EXPERIENCE.md hold.
laws:         honesty law absolute — every number is live truth; claim ceiling "measured
              functional correlate". Two-ink FUI (amber #ffb000/#d4a24c live only ·
              blue-gray structure). NO emoji. THE ASSISTANT LADDER is canon (Luis,
              2026-07-20): Act 0 chat, one keyless model · Act I token sources · Act II
              memory/RAG · Act III flows · Act IV powers to the exterior · Act V-VI the wild.
```

Build-state marks: `[BUILT]` verified in code on disk this date · `[PLANNED]` designed,
not built · `[DECISION-LUIS]` awaiting his call.

---

## 0. The question this chapter answers

Luis, 2026-07-20: *"we will have predefined all the modules and their capabilities on
output as the game progresses — how do we account for that? How do games do it?"*

The question has three parts and this chapter answers all three: (1) where the definitive
list of modules and their capabilities LIVES (section 2 — the manifest), (2) how the game
knows at any moment what the assembled assistant can and cannot do (section 4 — the live
capability matrix), (3) how a finished assistant leaves the game and runs in the wild
(section 5 — the graduation bundle). The industry answer comes first, because thirty years
of shipped games already converged on the shape, and THE PROBE's code — built before this
chapter existed — independently converged on half of it.

---

## 1. HOW GAMES DO IT — the converged patterns

Twelve named patterns from the 2026-07-20 industry research, each with its source. The
synthesis after the table is what THE PROBE actually adopts.

| pattern | source | one-line mechanism |
|---|---|---|
| **Prototype registry** (everything-is-data, staged assembly) | Factorio `data.raw` data lifecycle | boot builds ONE central table of prototypes in three passes; the engine instantiates gameplay exclusively from it; missing fields default-or-hard-error by name |
| **Registered / pool / equipped** (three-state unlock) | Slay the Spire unlock system + BaseMod registry | full library compiled from day one; score raises unlock levels moving cards into the DRAW POOL; the deck is a third, separate set |
| **Whole-graph-as-versioned-JSON, build-as-pointer-set** | Path of Exile passive tree JSON (grindinggear/skilltree-export) | the entire tree ships as one versioned JSON; a build is nothing but allocated node IDs — tiny, diffable, meaningless without the tree |
| **Lock-and-key over a dependency DAG** | Metroidvania design analyses (gamedeveloper.com) + runevision's procedural progression graphs | abilities rewire movement EVERYWHERE, not one door; generators machine-verify reachability on the graph |
| **Tech tree = prerequisite predicate** | Civilization-lineage tech trees | the engine stores no "what unlocks next"; it evaluates one pure predicate at request time: prerequisites met AND cost paid |
| **Server-authoritative entitlements, dark-shipped features** | LaunchDarkly entitlements · Microsoft GDK service-to-service query · NeoForge feature flags | code ships dark in the client; the authority is a service queried at point of use; unlock state = rows in a store the client cannot forge |
| **Capability manifest + runtime escalation** | Chrome extension permission model (`manifest.json`, `chrome.permissions`) | minimum permissions declared at install; optional ones escalated at runtime with the user as consent surface; an API not in the manifest does not exist |
| **Sandboxed containers, injected capability set** | Roblox Script Capabilities · Factorio Lua sandbox RCE analysis | the execution context holds exactly the granted callables; the documented lesson: remove eval/loadstring-class hatches entirely |
| **Hierarchical permission nodes** | Bukkit permission nodes (`bukkit.command.kick`) | dotted namespace, parent grants children, explicit per-node overrides; the namespace is the schema; greppable at thousand-capability scale |
| **Format versioning + save migrations** | Factorio migrations · Minecraft `pack_format` | content renames ship migrations so earned progress SURVIVES; incompatible versions refuse loudly, never half-run |
| **Acts as spec files** | TIS-100 SPECIFICATION EDITOR (Lua puzzle specs) | campaign and player content share one data format; the engine hosts the spec, the spec never touches the engine |
| **Text-encoded export with a clear-check gate** | Mindustry base64 schematics · TIS-100 plain-text saves · Mario Maker upload-after-clear | the artifact is compact text referencing a shared engine everyone has; nothing publishes until the creator clears it themselves |

Three separations recur across all twelve, and they are the chapter's spine:

1. **Registry, pool, loadout are three different persisted sets** (Slay the Spire, PoE,
   Factorio). What exists / what you earned / what is slotted right now. Games that merge
   any two of these ship bugs where players equip what they never earned or lose what they
   did.
2. **Permission is a predicate evaluated at call time, never a flag set at unlock time**
   (Civ trees, GDK entitlements, Chrome runtime permissions). A demotion instantly
   re-locks everything downstream with zero bookkeeping.
3. **The creation and the engine are separate artifacts** (PoE builds, Mindustry blobs,
   TIS-100 saves). The export is pointers plus config; the engine is shared substrate.
   That split is what makes creations tiny, portable, and honest.

---

## 2. THE PROBE'S ANSWER — the MODULE MANIFEST

### 2.1 The answer in one law

**One registry file — `modules.json` `[PLANNED]` — declares every real organ and what it
can do. The game reads the manifest to know what EXISTS. The save records what is
UNLOCKED. The trust ledger decides what may FIRE, per call. The code itself is never
generated by the game — modules are forged in pair sessions (A9_FORGE_PROTOCOL.md) and
then REGISTERED.**

This is Factorio's prototype-registry discipline applied to organs instead of items: acts
never create capability code; they only flip permission state on pre-registered entries.
A forge session's SEAL phase (A9 section 3.5) gains a sixth ledger: the manifest entry
flips `FORGE-PENDING` to `BUILT` in the same commit that lands the organ. A module absent
from the manifest does not exist to the game — the Chrome-manifest law — with one
deliberate divergence: THE PROBE's forbidden axes (send, spend, keys) ARE declared, at
level 0, because trust.py's design is that the entity can always answer *"why am I allowed
— or not allowed — to do this?"* Absence would be silence; declared-FORBIDDEN is
inspectable refusal. `[BUILT]` in the CHARTER today.

### 2.2 What already exists — the substrate is half-built

The manifest is not invented from nothing; it consolidates three real, currently-separate
declarations:

- `ORGANS_DOC` in ../controlroom.py `[BUILT]` — a hardcoded (name, file, status) list of
  17 organs, served on `/skills`. It is a prose registry: no capabilities, no gating.
- `CHARTER` in ../trust.py `[BUILT]` — nine capabilities with start level, ceiling, and
  promotion cost. Its guard is already manifest-grade law: an unknown capability raises
  `KeyError("add it to the CHARTER deliberately, never implicitly")`.
- `window.AEA` / aea_elements.js `[BUILT]` — the teaching-side registry (codex elements,
  discovers/links). Engine truth and teaching truth must not fork: the UNCHARTED SIGNAL
  boot diff (A10_LIVING_GAME.md section 2.3) is the reconciliation surface.

Namespace note, to prevent a real confusion: `capability_census.json` measures MODEL
capabilities (the six-probe census of rods). The manifest declares ORGAN capabilities.
Same word, different layer; the glossary (A6_GLOSSARY.md) gets both entries.

### 2.3 The manifest schema `[PLANNED]`

Every entry declares eight facts. Two worked entries, one built, one pending:

```json
{ "manifest_version": "0.1.0",
  "modules": {
    "speak": {
      "file": "speak.py",
      "status": "BUILT",
      "capabilities": ["speak-local"],
      "trust": { "capability": "speak", "min_level": "WATCHED" },
      "unlock_act": "I",
      "bench_part": true,
      "config": { "cloud_ok": "bool — forced false in sensitive zone" }
    },
    "recall": {
      "file": "recall.py",
      "status": "FORGE-PENDING",
      "forge": { "queue": 1, "boss": "B2", "spec": "05_CONTENT_MISSIONS.md section 4" },
      "capabilities": ["recall"],
      "trust": { "capability": "reason_private_local", "min_level": "WATCHED" },
      "unlock_act": "II",
      "bench_part": true,
      "config": { "k": "int 1..8", "zone": "private | sensitive" }
    } } }
```

Capability TYPES are a closed vocabulary (typed verbs, extended only by book amendment):
`read-state` (own stores/endpoints) · `draw` (burn a rod through energy.draw — always
carries tier x zone) · `recall` (vector read over private embeddings, local by
construction) · `write-state` (own JSON through grid's atomic helpers) · `act-external`
(bytes leave the machine other than a plant draw) · `speak-local` · `listen-local` ·
`spawn-proc` (subprocess; today only the `/do` allowlist holds it).

### 2.4 The registry, transcribed from the real code

The v0 manifest content, honest per file on disk 2026-07-20. `INGREDIENT` is the third
status the code forced on us: a real file, proven in isolation, not wired into the live
mind — A9's proven-not-wired fog list, declared rather than hidden.

| id | file | capabilities | charter binding | act | bench part | status |
|---|---|---|---|---|---|---|
| grid | grid.py | read-state, write-state (meter) | substrate — ungated | 0 | no | BUILT |
| energy | energy.py | draw | zone law enforced in-module | 0 | no — the power bus every part draws through | BUILT |
| talk | talk.py | draw, recall | reason_private_local | 0 | yes | BUILT |
| brief | brief.py | draw, read-state, write-state | gather_public + reason_private_local + produce_brief | I | no | BUILT |
| speak | speak.py | speak-local | speak @ WATCHED (checked live in controlroom.py) | I | yes | BUILT |
| memory | memory.py | recall, write-state | reason_private_local | II | yes | BUILT |
| consolidate | consolidate.py | recall, write-state, destructive-read | reason_private_local | II | no — a mission verb, the mine | BUILT |
| index_codex | index_codex.py | recall | reason_private_local | II | yes | BUILT |
| recall | recall.py | recall | reason_private_local | II | yes | FORGE-PENDING (queue 1) |
| think | think.py | draw (council) | reason_private_local | III | yes | FORGE-PENDING (queue 2) |
| orchestrator / swarm / relay / pathfinder | *.py | draw | — | III | yes, after the think forge wires them | INGREDIENT |
| agent_tools | agent_tools.py | act-external (web_fetch, json_get), compute (calc) | gather_public @ WATCHED | IV | yes, after the wire forge (queue 3) | INGREDIENT |
| telegram_bridge | telegram_bridge.py | act-external (bound operator chat only), listen | NO CHARTER ROW — named gap, section 6 | IV | no | BUILT |
| reflect | reflect.py | draw, write-state | its own envelope: no internet, no effectors, no keys | — (the entity's, not the player's) | no | BUILT |
| hades / trust / pulse / tracelog | hades.py, trust.py, pulse.py, tracelog.py | verdict-draw / ledger / signal / trace | they ARE the law | — | no | BUILT |
| live | live.py | spawn-proc (scheduler) | substrate | — | no | BUILT (partial per ORGANS_DOC) |

Two structural facts the table encodes, both inherited law:

- **Substrate rows have no unlock act.** HADES, trust, the meter, pulse, tracelog are
  day-0 law of the entity; only the PLAYER'S surfaces unlock (A7_BUILD_LAYER.md section 4:
  gate the control surfaces, never the entity's behavior). They are also `bench_part: no`
  — a construct cannot slot the gate; the gate wraps every construct.
- **The three-state split is explicit** (the Slay the Spire pattern): REGISTERED = a row
  in modules.json (browsable in the codex, cold ink, from install) · UNLOCKED = the row's
  `unlock_act` appears in `journey_save.json` `done{}` (the pool) · SLOTTED = the module id
  appears in a construct spec (the loadout, section 3). Three files, three sets, never
  merged.

### 2.5 One audited hatch, named

Factorio's RCE lesson says injected surfaces must carry no eval-class hatches.
../agent_tools.py `calc()` uses `eval` — fenced to arithmetic by regex and scrubbed
builtins `[BUILT]`. It is the one eval in the organ population; the manifest marks it
`audited-hatch: calc` so it can never disappear from review. Any future module proposing
eval/exec/dynamic-import in an injected surface is refused at registration.

---

## 3. THE CONSTRUCT SPEC — the composition format

The composition reframe is canon (R1_EVIDENCE.md, Luis 2026-07-20): composing AEA
combinations into REAL running constructs is the game's core creative act. The construct
spec is that act's file format. `[PLANNED]`

```json
{ "construct_version": "0.1.0",
  "manifest_version": "0.1.0",
  "id": "morning-counsel",
  "parts":    ["recall", "think", "speak"],
  "rods":     { "think": { "tier": "frontier" }, "default": { "tier": "reflex" } },
  "wiring":   [["recall", "think"], ["think", "speak"]],
  "policies": { "recall": { "k": 4 }, "speak": { "cloud_ok": false } },
  "zone":     "private" }
```

The laws of the format, each stolen from a named pattern:

- **A construct is a pointer set** (the PoE build pattern). `parts` are module ids into
  the manifest; `rods` are tier requests into the energy ladder, never model names
  (energy.py's law: no organ may ever name a model — the construct inherits it; the ladder
  resolves tier to rod at draw time from live fitness). The spec is tiny, diffable,
  git-committable, and meaningless without the manifest it references — exactly right.
- **Validation is a pure re-walk** (PoE + runevision): every part REGISTERED, every part's
  `unlock_act` in the save, every part `bench_part: true`, every wiring edge between
  declared parts, every policy key inside the part's declared `config` surface, the
  construct's zone at least as strict as its strictest part. A spec that fails names the
  violated clause — never a generic lock.
- **The bench executes through the real router.** Running a construct walks the wiring and
  fires each part's real entry point through energy.draw / the organ's actual function,
  under the zone law, metered, HADES-watched, tracelogged. The bench is a harness, not an
  interpreter of game-flavored pseudo-code — there is no second execution engine to drift
  from the first.
- **Versioned and portable** (TIS-100 plain text): constructs live as files, survive in
  git, and are the unit of gifting and grading. Act III's flows curriculum is authored AS
  construct specs the player modifies — campaign content and player content share one
  format (the TIS-100 spec-file pattern), which is what keeps Phase B's community door
  open for free.
- `[DECISION-LUIS]` D-M3 — execution rights for constructs containing `act-external`
  parts: direct fire vs draft-and-approve. Recommendation: mirror A7's D-B3 split —
  direct for read-only external (web_fetch under gather_public), draft-and-approve for
  anything that writes to the world, and `send_outbound` stays FORBIDDEN at charter level
  regardless of any construct (a spec can never out-rank the ledger).

---

## 4. CAPABILITY ACCOUNTING — proving what it can do, live

### 4.1 The live capability matrix

The game's runtime answer to "what can the assistant do RIGHT NOW" is a pure function,
recomputed at render and — critically — re-evaluated at every call:

```
CAN(module, cap) =  manifest declares cap on module            (modules.json)
                 AND module.unlock_act in save.done            (journey_save.json — the pool)
                 AND trust.check(module.trust.capability).allowed   (the ledger, at THIS moment)
                 AND required plant online: auth is None or key present   (grid.key — .env truth)
                 AND file exists and non-empty on disk         (the forge_gate check, A9 3.1)
```

Manifest x trust ledger x keys present = the matrix. Rendered in the OS as a table
`[PLANNED]`: rows are modules, cells carry the verdict WITH the why-string —
trust.check() already returns one (`"speak: level 2 (WATCHED), streak 1, 4 runs / 0
fails; ceiling TRUSTED"`) `[BUILT]`. Two-ink discipline: a cell is amber only when every
conjunct holds this instant; every other state is structure ink plus a WORD naming the
failing conjunct (`LOCKED act III` / `DRAFT-ONLY` / `PLANT OFFLINE` / `FORBIDDEN` /
`LOST SIGNAL`) — never hue alone (A10 section 4.5).

### 4.2 Predicate at call time — the code already obeys the pattern

The Civ-tree and GDK-entitlement law — evaluate at point of use, never cache the grant —
is ALREADY the built behavior: brief.py calls `trust.check(cap)` before acting and
`trust.record(cap, ok)` after HADES rules; controlroom.py checks `trust.check("speak")`
before every TTS call `[BUILT]`. One failure demotes instantly (`record()`: fast down),
and because nothing downstream caches the old level, the demotion re-locks everything
that depends on it with zero bookkeeping. The manifest adds no new mechanism here; it
adds the DECLARATION that lets the game render, before the call, the same predicate the
organ will evaluate during it. Server-authoritative translates locally exactly as the
research fit predicted: only trust.record() writes the ledger, under `grid.file_lock`,
organs read it; no game surface can flip a level (the REINITIALIZE boundary, A10 3.4 —
wiping the journey empties the POOL, never the ledger; earned trust is the entity's
history, not the probe's).

### 4.3 Drift rules — when code changes under the manifest

The manifest is a claim about code, and CODE WINS (02_SYSTEMS.md header law). Drift is
handled with A10 section 5's tombstone discipline, applied to modules:

1. **A vanished module keeps its row.** File gone or import broken while the manifest
   still declares it: the row renders `LOST SIGNAL` in structure ink — a hole reads as
   fate, not as silent deletion. Constructs referencing it fail validation naming the
   tombstone. `[PLANNED]`
2. **No silent repair.** No code path prunes manifest rows or edits construct specs to
   match the present. Disagreement renders as disagreement, with provenance.
3. **Renames ship migrations** (the Factorio pattern): when a charter capability splits
   or a module id changes, a migration rewrites ledger and construct specs so EARNED
   TRUST SURVIVES — resetting a player's TRUSTED tiers on a refactor is the cardinal sin
   the pattern exists to prevent. `manifest_version` + a recorded applied-migrations list
   per store. `[PLANNED — machinery deferred until the first real rename, named
   deliberately: building it before one exists is scope inflation]`
4. **Version mismatch refuses loudly** (pack_format): a construct or export whose
   `manifest_version` is newer than the engine's refuses to load with the version named —
   never half-runs.

---

## 5. RUN IN THE WILD — the graduation architecture

Act V-VI of the assistant ladder ends with an assistant that leaves. Per A5_PHASE_B.md
this is GATED — zero build hours until Phase A is played and judged — but the export
shape is designed now so no forge builds against a dead end. `[PLANNED, gated]`

**The bundle is four things, and the split follows the artifact/engine separation:**

1. **The engine** — the organ files themselves, obtained by clone/install (A5's B-0
   setup mission: the bootstrap ladder from the keyless rung up). The engine is NEVER
   inside the export blob — Mindustry's schematic references the game everyone has; PoE's
   build references the tree everyone has. Same move.
2. **The manifest + the player's unlock state** — which modules are registered, which
   acts are done, which trust levels were earned. The wild runtime enforces the identical
   bounds with zero game context — the manifest is the contract; the game was just the UI
   for negotiating it (the Chrome-manifest fit, verbatim).
3. **The construct specs** — the assistant's actual composition, as section 3 text
   artifacts: magic-prefixed, versioned, pasteable, giftable (the Mindustry text-blob
   pattern).
4. **THEIR keys and THEIR memory — never Luis's.** Keys never serialize into any blob:
   the export records which plants a construct EXPECTS; the owner re-hydrates `.env`
   locally (keys travel by the player's hand or not at all). Memory stores travel as the
   player's own files. The A5 section 4 table is binding law here: `luis_memory.json`,
   the corpus vein, and LEYBER's own history NEVER ship. Two finishers have built two
   different entities.

**The clear-check gate, stolen from Mario Maker verbatim:** an assistant may only be
exported after it passes its own HADES acceptance run — the construct executes end-to-end
on the owner's machine, the gate verdicts it, and the trust ledger shows no FORBIDDEN
part and no DRAFT-level part slotted for autonomous fire. Nothing unproven graduates.
The ledger's final act is the clear-check; the export is signed with the manifest version
and the acceptance run's trace id, so a wild runtime can show WHY this assistant was fit
to leave. Mario Maker's insight is the honest one: the creator clearing their own level
is the only anti-garbage gate that cannot be faked by policy.

---

## 6. Engine deltas to manifest v0 — honestly scoped

In order; nothing here starts before its act needs it (one phase at a time).

1. **Author `modules.json`** — transcribe section 2.4; pure data authoring, no code.
   `[PLANNED — small]`
2. **`/api/manifest` endpoint** in controlroom.py — serve the file plus live per-row
   flags: file exists + non-empty (the forge_gate check), plant/key gating via
   `grid.key`, current ledger level per binding. `[PLANNED — small]`
3. **Retire the ORGANS_DOC hardcode** — `/skills` reads the manifest; one source of
   truth, delete the constant. `[PLANNED — small]`
4. **Charter additions, deliberately** — `notify_operator` for telegram_bridge (today it
   runs gated only by token presence and chat-binding, with NO ledger row — the one organ
   acting externally outside the charter; named gap, closes here); decide whether
   agent_tools' external reads stay under `gather_public` or split. CHARTER edits are
   governance, Luis-reviewed by trust.py's own law. `[PLANNED — small, DECISION-LUIS on
   the split]`
5. **Construct spec v0 + validator** — the schema and the pure re-walk of section 3;
   data + one function, no bench UI yet (the bench itself is R1/A7 scope, Act III).
   `[PLANNED — small]`
6. **The capability matrix pane** — the OS rendering of section 4.1, folded into the
   existing SYSTEM or codex surface before it earns its own tab (the boring test gates
   it). `[PLANNED — medium]`
7. **Migrations machinery** — explicitly deferred until the first real rename (section
   4.3, item 3). `[PLANNED — deferred, named]`
8. **Export** — zero hours until the A5 section 1 gate opens. The bundle spec above is
   the whole deliverable for now. `[PLANNED — gated]`

Open decisions ledger for this chapter:

| # | decision | recommendation |
|---|---|---|
| D-M1 | capability naming: keep flat CHARTER ids vs adopt dotted namespace (probe.tools.fs.write, Bukkit-style) | keep flat ids canonical; dotted aliases only when the ledger first needs a child override — the namespace pattern earns its complexity at hundreds of nodes, we have nine |
| D-M2 | manifest as modules.json vs registry.py | JSON — everything-is-data (Factorio), diffable, servable raw over /api/manifest with no import side effects |
| D-M3 | construct execution rights for act-external parts | split per A7 D-B3: direct for governed reads, draft-and-approve for world-writes; send_outbound stays charter-FORBIDDEN over any spec |

---

## Changelog

- 2026-07-20 — v1. Authored as the code-management chapter from Luis's registry question,
  the 12-pattern industry research (Factorio, Slay the Spire, PoE, Metroidvania DAGs, Civ
  trees, LaunchDarkly/GDK/NeoForge, Chrome manifests, Roblox capabilities, Bukkit nodes,
  Factorio migrations, TIS-100 specs, Mindustry/Mario Maker export), and the code on disk:
  controlroom.py ORGANS_DOC + /skills + allowlists, trust.py CHARTER + call-time checks,
  grid.py key()/PLANTS, energy.py tiers/zones, agent_tools.py's audited eval hatch,
  telegram_bridge.py's charter gap. Manifest [PLANNED]; its substrate marked [BUILT]
  where verified.
