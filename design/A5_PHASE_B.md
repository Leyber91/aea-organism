# A5_PHASE_B — PART VII: THE GAME FOR EVERYONE

```
Book:          THE PROBE — design book, top-of-book chapter (PART VII)
Status:        PLANNED — GATED. Zero build hours until the gate in section 1 opens.
Last updated:  2026-07-20
Governs:       the product path. Lower chapters (01_WORLD.md, 02_MECHANICS.md, 03_MISSIONS.md,
               04_FUI.md, 05_TECH.md, 06_ROADMAP.md, 09_PRODUCTION.md) derive Phase B
               obligations from THIS chapter; none may start Phase B work on their own.
Inherits:      00_VISION.md (root vision; section 4 two-phase audience, section 6.2 win
               condition) and the sibling top-of-book PARTs I–VI of this A-series.
Ground truth:  ../GAME_PLAN.md (mechanics canon) · ../grid.py (PLANTS, ZONES, Meter, key())
               · ../missions.js · ../world.html · ../controlroom.py
Laws in force: honesty law (every number is live system truth; claim ceiling = "measured
               functional correlate, present"; never "conscious", never "sentient") ·
               two-ink FUI (amber = live/fired only, blue-gray = structure) · no emoji.
```

Build-state marks: `[BUILT]` verified in running code · `[PLANNED]` designed, not built ·
`[DECISION-LUIS]` awaiting his call.

---

## 1. The gate — read this before anything else in this chapter

`[DECISION-LUIS — the gate is his call, not a team call]`

Phase B receives **zero build hours** until two conditions hold, in order:

1. **Phase A is played.** Luis, player one, has piloted THE PROBE through Act VI — the
   journey playable and played, THE SEND passed, the self-loop closed (00_VISION.md §6.1).
2. **Luis judges it worthy.** An explicit go, on the record in 09_PRODUCTION.md §6 — not
   drift, not "while we're here".

Any Phase B task attempted before that gate is scope inflation by definition and is refused
by name (00_VISION.md §4; 09_PRODUCTION.md §4: "a tutorial for others written before player
one finishes is fiction"). This chapter exists so that when the gate opens, the path is
already designed and no re-planning session is needed — design on paper now, hours later.
The three architectural commitments that keep the door open cost nothing and are already
law: missions are data; the world reads only curated endpoints; no private Luis data is
baked into game content (00_VISION.md §4, all three `[BUILT]` in slice 1).

---

## 2. The promise

`[PLANNED — the product's one-sentence contract]`

**Finish the game and you have built your own AI entity with the AEA's properties.**

Not watched one being built. Not read about one. Built one — on your machine, from your
keys, out of your corpus — because THE PROBE never hid the machine: every organ was seen
as real code (the learn-beat reveal), every resource limit was felt as real starvation,
every threshold was a citation you watched pass or fail (00_VISION.md §6.2). The entity
you finish with is not LEYBER; it is yours, tamed to you, and it keeps running when the
game is closed, because it was never a game object in the first place.

The promise has a hard ceiling, and the ceiling is the product's spine, not a disclaimer:
what you finish with is an autonomous entity whose properties are **measured functional
correlates** — cited, falsifiable, re-runnable on your own logs. The game never promises,
implies, or markets "conscious", "sentient", or "your own mind". A teaching product at
this boundary that inflates the claim destroys the one thing it sells: that every number
on screen is true. The honesty law is the brand.

And the promise is falsifiable, which is why Phase A gates it: Luis finishing the game is
the first demonstration that the AEA can be learned from inside (00_VISION.md §6.2). If
player one cannot get there, strangers cannot, and the promise is not made.

---

## 3. The bootstrap ladder — already real for a stranger

`[BUILT — the capacity mechanism below exists today in ../grid.py; the missions that
climb it are PLANNED]`

The reason Phase B is credible and not a pivot: the energy grid was built stateless over
files from the start, and its bottom rungs require nothing a stranger does not already
have. `grid.py` skips any plant whose key is absent (`PLANTS[plant]["auth"] and not
key(...)` — the plant simply is not routed to), so an empty `.env` does not error; it
produces a smaller, honest grid. Capacity growth is literal file state, which makes it a
progression system for free (GAME_PLAN.md §1, capacity row). The ladder, bottom up:

### Rung 0 — first light, zero accounts `[BUILT — mechanism]`
Act 0's socket is **pollinations**: keyless (`auth=None` in PLANTS), 1 request per 15
seconds, public-zone only. Anyone on earth with a browser and this repo gets a real model
answering from the dark with **zero accounts, zero keys, zero payment instruments**. This
is the whole acquisition funnel in one mechanic: the player's first real call inside 90
seconds of play, before any signup friction exists. It is deliberately meager — 4 rpm and
no privacy — so the game's first lesson is scarcity, and the first desire is the next rung.

### Rung 1 — the private hearth `[BUILT — mechanism]`
**Local ollama**: `privacy="local"`, unlimited rpm/rpd, slow, yours. This rung changes the
entity's nature, not just its capacity: in the zone law (`ZONES` in grid.py), the
`sensitive` zone admits **only** local. A stranger's private corpus — the ore they will
mine in Act II — can be worked without one byte leaving their machine, not as a promise
but as routing law the game teaches as a mission. The hearth is why "tamed to them" is
honest: personal memory lives at home.

### Rung 2 and up — keys as capacity, one plant at a time `[BUILT — mechanism]`
Every free key minted is a plant coming online, and the numbers are real per-plant
physics from PLANTS: NVIDIA (one key, ~121 models, 40 rpm each — the single biggest
unlock), groq (speed), cerebras (batch lane, verified 5 rpm), sambanova, ovh (400 rpm
with token, EU), cloudflare (10k neurons/day), then the trains-on-data public zone
(gemini, mistral, openrouter, zai). The Meter's sliding windows and daily quotas make
each new key a visible, felt increase — mana pools appearing on the HUD because they
appeared in `.env`. Progression IS onboarding; there is no separate tutorial economy.

The ladder is also the privacy curriculum: rung 0 teaches "public means public", rung 1
teaches the sensitive zone, rung 2 teaches the no-train / trains distinction plant by
plant. A player who tops the ladder has learned real operational judgment about where
data may flow — which is the product's actual teaching claim, made mechanical.

---

## 4. Yours and his — what generalizes, what does not

`[PLANNED — the separation contract; partially BUILT via slice-1 commitments]`

| Layer | Phase B status | Why |
|---|---|---|
| Engine: `world.html` probe rig, mission engine, HUD, WebAudio, save protocol | **Generalizes as-is** | Reads only curated endpoints; any AEA-shaped server backs it (00_VISION.md §4, commitment 2) |
| Content: `missions.js` acts, beats, teaches-map, boss thresholds | **Generalizes with hardening (§5)** | Missions are data; citations and thresholds are universal, not Luis-shaped |
| The map: districts-as-organs, fog, growth on forge (01_WORLD.md) | **Generalizes** | The geography is the AEA schema, and the schema is the curriculum |
| Grid machinery: `grid.py` PLANTS/Meter/zones, fitness, autonomy battery, HADES | **Generalizes** | Stateless-over-files; keys and state are the player's own |
| `luis_memory.json` — the ingots | **LUIS-ONLY. Never ships.** | A new player starts at zero ingots and mines **their own** corpus |
| The corpus vein — Luis's sessions | **LUIS-ONLY.** | The player's vein is their own session archive, notes, exports — their life in text. Mining it is the point |
| The codex — Luis-authored entries and personal context | **LUIS-ONLY at the personal layer; the AEA framework layer generalizes** | Requires server-side filtering before any distribution (§5, B-3) |
| LEYBER itself — its memory, class history, tick log | **LUIS-ONLY.** | LEYBER is player one's entity. Each player's completed entity is **theirs** — same architecture, different being |

The identity rule, stated once and binding on all lower chapters: **the AEA generalizes;
the entity does not.** Phase B ships an architecture and a journey, never a copy of
LEYBER. Two players who both finish have built two different entities, each tamed to its
builder, because the ore, the hearth, and the keys were theirs. The world bible already
carries the matching law: the world can only ever show a stranger's entity as truthfully
as it shows LEYBER (01_WORLD.md, phase note).

Empty-state corollary (binding on 03_MISSIONS.md and 05_TECH.md): every screen and
mission must boot honest on a **zero entity** — no ingots, no fitness history, no tick
log, one keyless plant. Where there is no truth to show, the game shows nothing or the
darkness — never a placeholder number (00_VISION.md §5).

---

## 5. What Phase B needs built

`[PLANNED — sized on paper only; no hours until section 1 opens]`

- **B-0 — Setup mission zero: stand up the server.** The one mission that runs outside
  the game: install python, clone, run `controlroom.py`, install ollama, pull one small
  model, open `/world`. Framed diegetically — before you can pilot the probe, you build
  the dark room — but engineered as installer-grade bootstrap (one script, hard version
  pins, a self-check endpoint the mission's PROVE beat asserts against). This mission's
  failure rate decides the product's support burden (§7, R-B1); it gets the most design
  attention of anything in Phase B.
- **B-1 — Key-onboarding missions.** One mission per plant rung: acquire the free key
  (authored walkthrough of the provider's real signup), drop it in `.env`, and PROVE
  with a live call routed through the new plant — the mana pool appears because the
  capacity did. Teaches the plant's privacy class as part of the same beat. Content rots
  with provider policy (§7, R-B2) and is therefore data-driven like all missions.
- **B-2 — Content hardening.** Strip every Luis-default from mission asserts; rebalance
  Act thresholds for cold-start grids (a boss tuned against 29 fit models must not be a
  wall on a 2-plant grid); full empty-state pass per §4; corpus-adapter step so a
  stranger can point the mine at their own archive formats.
- **B-3 — Server-side codex filtering.** A curation layer on the codex and memory
  endpoints: the AEA framework layer serves; the personal layer never leaves the server
  by construction (an allowlist of servable entries, not a blocklist of secrets). Zone
  routing already enforces this for model calls `[BUILT]`; B-3 extends the same law to
  content reads. Ships with a leak test in CI, not a promise.
- **B-4 — Distribution decision.** `[DECISION-LUIS]` Repo-clone open source · packaged
  release · hosted demo of the *game* over a sandbox entity (a player's real entity can
  never be hosted by us — their keys and corpus stay on their machine, which is the
  product's privacy spine, so "hosted full product" is a different product and is out of
  scope for this chapter). Licensing and pricing ride on this call. Default if unmade:
  no distribution; Phase B artifacts stay in-repo.

Build order when the gate opens: B-0 -> B-2 -> B-1 -> B-3 -> B-4, because a stranger who
cannot boot never reaches a key mission, and nothing distributes before the leak test
exists. Sequencing detail belongs to 06_ROADMAP.md and 09_PRODUCTION.md, derived from
this list.

---

## 6. Why this chapter exists in the income arc — stated plainly

`[PLANNED — positioning only; no revenue is promised here]`

Phase B is a **teaching product at the boundary of AI systems and human understanding** —
the AI Systems Architect's flagship artifact. The public identity claims an
engineer-translator who shows people that the thing they feared was offering them
something; Phase B is that claim made playable: a stranger goes from fear-of-the-black-box
to having built one they understand, organ by organ, with every claim cited and every
limit felt. Anti-evangelism is structural — the product persuades by mechanism, never by
hype, because the honesty law forbids the hype.

What this chapter deliberately does **not** do: promise revenue, set prices, or forecast
adoption. Those are downstream of evidence that does not exist yet — Phase A finished,
the promise demonstrated on player one, B-4 decided. What can be said without inflation:
the artifact is the portfolio's spine either way (a completed, honest, novel product at
exactly the professed boundary), and the income clock is served **first** by THE SEND at
Act V — which is Phase A, is pinned, and no Phase B ambition may delay it (09_PRODUCTION.md
§4). Phase B compounds the identity; it does not jump the queue.

---

## 7. Risks

`[PLANNED — named now so the gate-opening session starts with eyes open; extends the
Phase A risk table in 09_PRODUCTION.md §5]`

| id | risk | why it is real | mitigation |
|---|---|---|---|
| R-B1 | **Support burden.** Every player runs their own server, python env, ollama install, and key set — every environment failure becomes a ticket addressed to one person who already runs <REDACTED-CIRCUMSTANCE>. | The measured session budget is the scarcest resource in this workspace (09_PRODUCTION.md R4). | B-0 is engineered installer-grade with a self-check the game itself reads; distribution choice (B-4) is made partly on support cost; the boring-but-honest fallback is narrowing the supported platform list rather than absorbing tickets. |
| R-B2 | **Key churn.** Free tiers are geology in motion: llm7 refuted after research said free (removed 2026-06-26), github models retiring, cerebras verified down to 5 rpm. Onboarding missions describing a signup flow rot without any code changing. | The PLANTS table in grid.py is itself a changelog of dead and downgraded rungs. | Key missions are data (B-1) and versioned per provider; the game's PROVE beat already fails honestly when a plant is gone; the ladder needs redundancy per rung, never a single mandatory provider. |
| R-B3 | **Model rot changes content balance.** Phase A already recorded this (09_PRODUCTION.md R3: pool 44 -> 29, perfect 7 -> 2 in one sweep); Phase B multiplies it by every player's grid, each rotting differently. A mission tuned on Luis's grid can be a wall or a triviality on a stranger's. | Rot is a design pillar, not an edge case (GAME_PLAN.md §1, item durability). | Asserts written against the player's own live survey, not absolute counts (B-2); missions fail honestly naming the real cause; rot itself stays in the curriculum — it is a lesson, not a bug, and the content must treat it as one. |
| R-B4 | **Privacy leak through content.** A single Luis-personal codex entry or memory shard reaching a distributed build is irreversible once indexed. | The public/private boundary is a standing high-cost rule for this workspace. | B-3 allowlist-by-construction plus an automated leak test gating every release; distribution (B-4) blocked until it exists. |
| R-B5 | **Promise inflation.** The market rewards "build your own JARVIS" copy; the product's claim ceiling forbids it, and one inflated line poisons the honesty brand that is the moat. | Every adjacent product in this space markets past its truth; the pressure is constant. | Section 2 is binding copy law for store pages, READMEs, and posts; the anonymize/claims lint runs on all public text; the ceiling phrase — measured functional correlate, present — appears verbatim in the product's own description. |

---

## 8. Governance

This chapter is top-of-book: when it conflicts with a lower chapter on any Phase B
matter, this chapter wins until explicitly amended. It may not itself contradict
00_VISION.md or the sibling PARTs I–VI; conflicts resolve upward, and amendments to the
gate (§1), the promise ceiling (§2), or the identity rule (§4) require Luis. The next
action on this chapter is **nothing** — that is the design. It sits ready until the
Phase A gate opens, and its readiness is what makes "worthy" a decision instead of
another planning session.

---

## Changelog

- 2026-07-20 — v1. Authored from ../GAME_PLAN.md, ../grid.py (PLANTS/ZONES/Meter/key
  verified on disk), 00_VISION.md §4/§6.2, 01_WORLD.md phase note, 09_PRODUCTION.md
  §4–§6. All Phase B work marked PLANNED and gated; no build hours consumed.
