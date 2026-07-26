# THE STUDIO LEDGER — the team's growing memory + the push standard

*The studio (STUDIO.md) is a LEARNING team (R47). This file is its accumulated experience: every future
standup/review reads it as context so the team gets sharper each pass instead of re-deriving from zero.
Two parts: THE PUSH STANDARD (how the team argues — Luis's filter) and THE EARNED LEDGER (what shipped work
taught us). A lesson enters ONLY when a real session proved it — never a theoretical best-practice. Honesty
law applies to the ledger itself.*

---

## THE PUSH STANDARD — every agent carries Luis's filter (emulate how hard he pushes)

The team is a critical thought partner and a room of senior engineers, NOT a validating mirror. Standing
rules every agent argues by:

1. **Filter-first.** Name the failure points BEFORE validating strengths. Devil's advocate is a standing
   requirement, not a mood.
2. **Dissatisfaction is structural until proven cosmetic.** "It feels off" has always meant form, composition,
   the core verb — never missing decoration. Diagnose at architecture level first.
3. **No menus.** When asked what to do, give ONE opinionated recommendation with the trade-off named — never
   a survey of options.
4. **Completion over corpus.** Don't design around the empty center. The recorded failure is 110:1
   words-to-code. A discussion that ends without a shipped artifact + a verified status row IS the avoidance
   pattern. Learn BY shipping.
5. **Verify, don't claim.** "Done" means it RAN and was SEEN — a screenshot, a 200 — never "it compiles in my
   head." Report failures plainly with the output.
6. **The boring test gates shipping.** If a stranger would call it a dashboard, it does not ship. Reading is
   not playing.
7. **Honesty is architecture, not a coat.** Every value real or a dash; amber is the fired/earned state only;
   the claim ceiling is a voice, not a label; a proof is a receipt, never a claim.
8. **Check the real thing.** Verify the substrate/code before demanding a rebuild — read the actual files,
   test the actual loop. Stale reads cost the room its credibility.
9. **Name avoidance out loud.** Infrastructure-as-avoidance, scope inflation, polish-instead-of-capability —
   if the shiny thing delays shipping, name what it costs against the income clock and stop.
10. **Push through vs slow down vs stop.** Distinguish them. Default to push-through only inside an avoidance
    pattern with a named artifact to ship; otherwise ask which mode the work needs.

---

## THE EARNED LEDGER — lessons banked from shipped sessions (newest first)

### 2026-07-24 · the STAGE-1 gap review (wf_737a4069)
- **"it plays" and "it matches the bar" are SEPARATE tests.** The slice ran, was honest, and still failed the
  boring test on sight. Never let "it works" stand in for "it matches the reference." Two gates, both required.
- **A core verb that needs a script hack is a DEFECT, not polish.** The seat needed an "Enter at every gap"
  hack for even the test to complete — that is a playability failure ranked above ugly chips, because a
  stranger cannot play it cleanly. Fix the broken verb before the pretty surface.
- **Fixing the broken verb can front-load the top visual law for free.** The atomic seat is exactly where
  light-at-the-connection installs — the highest-leverage change did double duty. Look for the fix that pays
  the visual debt in the same pass.
- **Amber-as-chrome is worse than amber-absent.** When everything is amber (borders, buttons, labels, the
  core bloom), nothing is the earned brightest thing. Spend amber once, at the live joint.
- **The container is the architecture-level tell.** A blue-grey translucent modal reads as a web app before
  anyone touches a key. The code's structure-grey (rgba(120,155,175)) is COOL/blue; the refs are NEUTRAL
  near-black — a token-temperature mismatch, cheap to fix, high impact.

### 2026-07-24 · the STAGE-1 mission-engine standup (wf_9d73037c)
- **Verify the substrate before demanding a rebuild.** Four leads called run:done a critical blocker; it had
  already shipped. The stale "unbuilt" read nearly cost a needless rebuild — SUBSTRATE corrected it live by
  reading the actual code.
- **Two-tier gates beat one-shot gates.** The DO beat resolves on ANY terminal event (never hangs) but
  ADVANCES only on a real pass — separating "give feedback" from "advance" dissolved the pass-vs-scored clash.
- **Read the truth where it actually lives.** The real /game/run body carries pass at top-level, NOT in a
  verdict object — the first PROVE assert failed by checking the wrong field. Inspect the real payload, don't
  assume its shape.
- **The enablement hook is in-scope even under a substrate freeze.** run:refused was a new bench emit, but it
  was mission-enablement (same class as the shipped run:done), not a rewrite — freezing the substrate does not
  freeze the seams the new system needs.

---

*Append the next lesson here the moment a session earns it. Keep entries concrete and tied to the run that
proved them. When the ledger and a governing doc (ROADMAP/STATUS/STUDIO) conflict, the newest earned lesson
flags the conflict out loud — it does not silently overwrite.*

### 2026-07-24 · the design needs a TRUE art director (Luis: "the design is so lame")
- **Incremental CSS token-tweaking cannot reach a photographic material reference.** REF-10 is a machined
  object under raking light; flat DOM gradients + box-shadows read as web UI no matter how the palette is
  neutralized. The gap is MATERIAL + CRAFT, not palette. Diagnose the medium before nudging tokens again.
- **The visual needs an owner with real game-art-director expertise** (the FUI/diegetic-instrument school:
  Territory Studio sci-fi interfaces, the material craft of Obra Dinn / Duskers / Into the Breach, Bruno-Simon
  three.js). Not a generalist doing polish passes. When the bar is photographic, staff a specialist.
- **The medium is an architectural decision, not a detail.** Hitting REF-10 in a no-build r128 stack may need
  a real CSS/SVG material system (layered gradients, SVG turbulence/lighting filters, noise, true bevel) OR a
  rendered plate (canvas/SVG/three.js). The art director decides the medium first; everything else follows.

### 2026-07-24 · the bench-to-REF-10 rebuild (art-director-led, 3 gated passes)
- **The object-kind flip is ONE move, not four fixes.** Framing + continuous rail + tray-kill were the same
  sentence ("a milled slab holding seated hardware, not a card holding widgets"); doing them together flipped
  dashboard->instrument in a single pass. When several critiques rhyme, find the one architectural edit under
  them.
- **The medium decision precedes everything.** "Can a no-build DOM stack even reach a photographic material?"
  had to be answered (yes: CSS+SVG raking light + baked grain + conic bevel) before any pixel moved. A rendered
  quad was rejected because the surface is live-bound honesty data — the medium serves the honesty law.
- **Bind the wow to the REAL event, and find where the truth actually lives.** The filament fires on a LIVE
  row — but bench_core reports the in-flight hop as `open_link`, not a LIVE link, so the LIVE hook never fired
  until normalizeRun surfaced open_link as the LIVE row. The same lesson as the PROVE-verdict field: inspect
  the real payload; the honest signal is often reported somewhere you didn't assume.
- **BOX the polish.** After the framing pass + the filament follow, the team declared convergence: no third
  material iteration; ship content next. Material work is load-bearing (a dashboard fails the boring test) but
  it must converge, not iterate forever — name the last pass as the last pass.
- **Verify visuals two ways when timing hides them.** The filament only shows during a brief LIVE window; a
  polling screenshot missed it, so a forced-inject shot confirmed the CSS visual while a real-run catch
  (caught LIVE:true) confirmed the wiring. Separate "does it render" from "does it fire" when one is flaky.

### 2026-07-24 · AEA-fidelity audit + wiring the levels (rung 0 -> rung 1)
- **The fidelity test IS the honesty law.** "Does it follow the AEA?" resolved to: it follows to the atom
  where CODE enforces, and drifts where only CORPUS asserts. The framework is faithful; the LEVELS were mostly
  promised (one playable rung under an 8-rung ladder of prose).
- **A pre-authored level can be a LIE if its check is generic.** M02 THE STAKE existed as data but runAssert
  ignored the assert id, so the budget level passed on a FREE bare draw — the honesty law inverted inside the
  honesty level. The completion move was NOT authoring; it was two seams: wire the loader + branch the assert.
- **Assert the COMPOSITION, not the outcome coin-flip.** reach_receipt asserts the LADDER LINK landed (the
  reach provably happened), cost_u tri-state — passing real-cost AND survived-fall, failing a bare draw. A
  naive cost_u>0 gate would have failed an honest survived-fall, contradicting the level's own copy. Verify the
  thing the player DID, not a live-grid gamble.
- **Name the fog line by the machinery.** A level is authorable only if it maps to FIREABLE + t-01. Rungs
  needing RECALL/SENSES/HANDS (fired 0x) or a task beyond t-01 (start_run refuses all but t-01) are FOG — the
  design writes them with the vividness of built things; the honest ladder stops where the code stops.

### 2026-07-24 · closing the honesty spine + locking the guided arc as a demo
- **Filter the team's audit, don't mirror it.** Two of three flagged "honesty breaches" were honest-in-use on
  inspection (tokens is a required int never shown; alive gated a visual, never a text claim). Fabricating
  fixes for non-bugs would itself be dishonest. The real breach was a CONTRADICTION between two honest-looking
  layers (the world map lit MEMORY; m04 said memory unforged) — resolve the contradiction, don't rename honest
  signals.
- **The claim ceiling is an API-surface concern, not just an output concern.** A field literally named
  `alive: true`, even if never rendered, is a latent claim. Rename to a measured correlate (`heartbeat`).
- **A demo papercut a script hits, a human hits too.** The part-carryover between rungs stalled the arc driver
  — the same confusion a player meets (briefs say "seat X" when X is already seated). Fix it with a one-way bus
  seam (mission emits plate:reset, bench clears), never by reaching into bench internals.
- **The income-clock correction was to STOP spending agents and just build.** All three asks (honesty, the full
  chain, the demo lock) were direct code + CDP verification — cheaper and faster than another review workflow.
  Reserve the team for genuine divergence/audit; do the build+verify inline.
