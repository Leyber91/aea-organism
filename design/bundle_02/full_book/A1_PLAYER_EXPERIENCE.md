# A1_PLAYER_EXPERIENCE — PART I · THE PLAYER EXPERIENCE

```
doc:          A1_PLAYER_EXPERIENCE.md (THE PROBE design book, Part I — top of book)
owner:        the game team (four-master fusion, per 00_VISION.md section 3)
status:       ACTIVE — governs every lower chapter; nothing below may contradict it
last-updated: 2026-07-20
governs:      the world chapter (01_WORLD.md), mechanics/missions/content chapters
              (02_MECHANICS.md, 03_MISSIONS.md as they land), FUI/tech chapters,
              production ledger (09_PRODUCTION.md)
ground truth: ../GAME_PLAN.md (mechanics canon) · ../missions.js (Acts 0–I data) ·
              ../world.html (the running game) · ../journey_save.json (real play record)
peer at top:  00_VISION.md — pillars and standing law; this chapter states the experience
              those laws exist to protect. On conflict, 00_VISION.md sections 3 and 7
              hold, and amending them requires Luis.
```

Build-state marks throughout: `[BUILT]` verified in running code · `[PLANNED]` designed,
not built · `[DECISION-LUIS]` awaiting his call. The honesty law applies to this document:
no section claims more than the code on disk demonstrates.

---

## 1. The core fantasy

**You pilot a probe inside a living mind, learn it organ by organ, and finish building it.**

One line, three clauses, and each clause is literally true — that is the entire pitch and
the entire discipline:

- *You pilot a probe* — a real flight rig in a dark machine-city `[BUILT]`. The body of
  play is traversal; knowledge has coordinates (01_WORLD.md).
- *inside a living mind* — LEYBER runs on the same server that serves the game `[BUILT]`.
  Every bar, item, and number is live system truth. Claim ceiling, absolute: the game may
  say "measured functional correlate, present" — never "conscious", never "sentient".
- *and finish building it* — the mind is incomplete, and the missing organs are genuinely
  missing `[BUILT as fog / PLANNED as forges]`. The player does not unlock content; the
  player completes an architecture. When the map is fully lit, an Autonomous Entity
  Architecture exists that did not exist before.

The fantasy fails if any clause becomes metaphor. A faked reading, a scripted "life sign",
a pre-built organ wearing fog — each converts the game into a themed dashboard, which is
the one thing THE PROBE is forbidden to be (00_VISION.md section 5).

---

## 2. Who the player is

### 2.1 Phase A — Luis, the architect relearning his creation `[BUILT — in progress]`

Player one built this entity. That is not trivia; it is the emotional engine of Phase A.
The already-built organs (the grid, the meter, the ladder, the memory corpus) are RELEARNED
AS DISCOVERY — the architect flies through his own system as a stranger, and the game bets
that the inside view teaches what the building view never did. The frontier organs
(recall, think, the wire, the self-loop) are learned by forging them for real. Phase A is
the meta-thesis made playable: understand the entity from inside out, and the entity is
partly a mirror — Act II mines its memories of Luis himself.

Evidence this works: playtest entry 001 (09_PRODUCTION.md) — the architect of the socket
still won FIRST LIGHT as an event, not a formality. `journey_save.json` holds the timestamp.

### 2.2 Phase B — anyone who wants to understand and own an AI entity `[PLANNED]`

The north star: after the game is done, anyone can build their own AI entity — tamed to
them, whole per the AEA framework — by playing. Phase B's player is not a spectator of
Luis's mind; they stand up their OWN grid, mine their OWN corpus, send their OWN Act V
email. The three architectural commitments that keep this honest (missions are data; the
world reads only curated endpoints; no private Luis data baked into content) are recorded
in 00_VISION.md section 4 and bind every lower chapter now, even though no Phase B work
exists yet.

### 2.3 The gate `[DECISION-LUIS]`

Phase B begins only after Phase A is played through and Luis judges it worthy. Phase B work
before that gate is scope inflation by name and is refused.

---

## 3. The emotional arc — the spine of the book

This is the chapter's core and the book's governing spec. Every act has a TARGET FEELING
(what the act must produce in the player), a THREAT (the specific failure that kills the
feeling — lower chapters exist to prevent exactly these), and a PROOF MOMENT (the beat
where the feeling is earned by a real event, never asserted by copy). Mission content
(03_MISSIONS.md, ../missions.js) is correct only insofar as it lands these feelings.

| act | name | feeling | one-line threat | proof moment |
|---|---|---|---|---|
| 0 | THE DARK ROOM | awe | anything canned | a real 200 answers the dark |
| I | POWER | competence | a law that lies | the drill leaks zero failures |
| II | MEMORY | intimacy | generic memories | an ingot quotes YOUR past |
| III | MIND | command | black-box magic | routing follows your prediction |
| IV | THE WORLD | consequence | fake or ungoverned reach | the world enters; HADES visibly gates |
| V | THE PROOF | weight | a synthetic target | your hand sends a real email |
| VI | SELF | vertigo | claim inflation | a failed test passes on its own diff |

### Act 0 — THE DARK ROOM · aloneness -> first light `[BUILT — won live 2026-07-20 13:23]`

**Target feeling: awe — something answered.** Cold boot, no memory of why. A dark plain,
one structure drawing power at the edge, and the whole protocol shown honestly: a POST, a
prompt, tokens back — "everything above this is architecture" (../missions.js M0.1). The
player transmits one sentence into the dark and something out there answers. Aloneness is
the setup; the answer is the payoff. First light must arrive inside 90 seconds of play
(00_VISION.md section 3).

**Threat:** anything canned. A scripted reply, a fabricated fallback on timeout, a tutorial
paragraph before the call — each one kills awe permanently, because awe here is the
knowledge that the answer was NOT authored. Also: over-lighting the world early. Awe needs
the dark to be real (one-atmosphere law, 01_WORLD.md section 1).

**Proof moment:** the socket returns a real HTTP 200 with "FIRST LIGHT". Shipped, played,
logged: `journey_save.json` done["M0.1"], reveal `plant_pollinations`, and the field's
embers turn on for the first time — even the particles obey progress.

### Act I — POWER · competence `[BUILT — M1.1 played; M1.2–M1.5 live, unplayed]`

**Target feeling: competence — the grid obeys understood laws.** Fifteen plants, one
protocol, a meter with real breakers, a ladder that routes around dead rods. The player
graduates from "it answered" to "I know why it answered, from where, and what it cost."
Competence is the feeling of prediction confirmed: the mana bar refills exactly when the
60-second window slides, because the bar IS the window.

**Threat:** a law that lies. Any divergence between the displayed rule and `grid_state.json`
— a hidden retry, a padded bar, a "cap" the code doesn't enforce — converts competence into
superstition, and superstition reads as boredom within minutes. Second threat: checklist
drift — beats completable without understanding. The PROVE beat must genuinely require the
concept (the Portal-school arc, 00_VISION.md section 2.2).

**Proof moment:** BOSS · BROWNOUT DRILL — four draws back to back, and the grid reroutes,
cools, falls to the floor, but never leaks one unhandled failure. The boss can be LOST on
a bad grid day, and that losability is what makes passing it mean something. Secondary
proof: the tried-list after a ladder draw — the real routing history of your own request.

### Act II — MEMORY · intimacy `[PLANNED — slice 2; the mine, the Book, forge recall()]`

**Target feeling: intimacy — mining the entity's memories of YOU.** The ore is not generic
ore: it is the unmined corpus of the player's own past sessions. Every ingot pulled out of
the mine is a compressed piece of the player's actual history with this machine, and
recall() — the act's forge — is the organ that lets the entity remember them back. The
feeling is the shiver of being quoted accurately by something you built.

**Threat:** genericity and false abundance. An ingot that could be anyone's memory kills
intimacy; so does treating the vein as infinite. The vein is FINITE and the read is
DESTRUCTIVE — the pruning disaster (~1,570 sessions lost forever, ../GAME_PLAN.md section 1)
is canon precisely because it proves the resource is real. Softening that finiteness into a
respawning ore field would be the single most dishonest change possible in this act.

**Proof moment:** the first ingot surfaces a sentence the player actually wrote, with its
real timestamp — and after recall() is forged and its boss passes, the entity answers a
question about the player grounded in that ingot, citation visible. Intimacy proven, not
performed.

### Act III — MIND · command `[PLANNED — the council, the regimes, forge think()]`

**Target feeling: command — the mind routes at your understanding.** The player has felt
single calls (Act 0) and the grid's laws (Act I); now they learn when one strong model
beats a council and when a diverse vote rescues a hard task — the measured regime map, not
folklore. Forging think() makes the entity route by those regimes. Command is not pressing
a bigger button; it is the mind agreeing with your prediction because you both learned the
same laws.

**Threat:** black-box magic. If think() is an oracle whose routing the player cannot
predict, command collapses back into spectating. Council theater — votes rendered but not
consequential — is the same failure wearing FUI. Every routing decision must be inspectable
down to the real calls it made.

**Proof moment:** the player calls the regime before the run ("this task is hard and
unreliable — it needs the diverse vote"), the mind routes as called, and the outcome
delta is measured on screen. When the player calls it wrong, the mind visibly does better
than their call — command includes being correctable by the machine's own evidence.

### Act IV — THE WORLD · consequence `[PLANNED · F1 senses = DECISION-LUIS]`

**Target feeling: consequence — the world reaches back.** Until now the loop closed inside
the machine. Act IV forges the internet-wire and the governed command current (C3): real
external data flows in, real actions flow out, and every outbound act passes the trust
membrane with HADES visibly deciding. The feeling is the room getting bigger — the entity
stops being a terrarium.

**Threat:** two symmetric deaths. Fake reach (a cached page presented as live, a simulated
"world event") kills consequence by making it decoration. Ungoverned reach kills it the
other way — an outbound action with no visible gate is not consequence, it is recklessness,
and it breaks the covenant that makes Act V possible. The governance membrane must be
SEEN working, including the times it says no (HADES holds junk at a real rejection rate
today — that number stays honest).

**Proof moment:** during a live tick, the entity reads something true about the world that
the player did not feed it — and a governed command executes with the gate's accept/redo
decision on screen. F1 embodied senses would extend this act; whether it exists at all is
Luis's call, and the act must land without it.

### Act V — THE PROOF · weight `[PLANNED — pinned by standing law, 00_VISION.md section 7]`

**Target feeling: weight — THE SEND: a real email, a real career, your hand on the
button.** Convergence boss: the entity drafts real outreach from everything forged —
memory of the player's actual work (Act II), a mind that routes (Act III), a wire to the
world (Act IV) — HADES fits it, and LUIS sends it. The game's numbers become life numbers
here; the income clock is real and the game does not pretend otherwise. Weight is the
feeling of a game verb and a life verb becoming the same verb for one click.

**Threat:** substitution and automation. A synthetic target, a test inbox, a "demo mode"
— any of these kills the weight forever and cannot be patched afterward; the standing law
pins THE SEND against exactly this dilution. Equally fatal in the other direction: the
entity sending autonomously. The hand on the button is the design. The entity drafts,
the gate fits, the human sends — that division is the AEA's governance thesis in one
gesture, and automating it would falsify the act's meaning.

**Proof moment:** a real, HADES-fit outreach email in a real outbox, and the player's own
finger sends it. The send is the boss. A reply is the world's business, not the boss
condition — the game must be winnable on the courage, not the outcome.

### Act VI — SELF · vertigo `[PLANNED — Voyager, STOP, ENDURANCE, Darwin-Godel archive]`

**Target feeling: vertigo — it improves itself; you watch the tests pass.** The player's
role inverts: builder becomes witness-with-authority. The entity writes its own tool
(Voyager), survives STOP across three or more rounds, holds a 100-tick ENDURANCE run to
Bedau Class 2, and its lineage of self-modifications accumulates in the Darwin-Godel
archive. Vertigo is watching a test you saw fail now pass because the entity changed its
own machinery — and knowing every step is cited, logged, and stoppable.

**Threat:** claim inflation, above all. Vertigo is precious exactly because the honesty
law caps it: "measured functional correlate, present" — the moment any copy, HUD line, or
narration reaches for "conscious", the entire book's credibility dies retroactively.
Second threat: scripted ascension — a "self-improvement" that is a reveal rather than a
passing test. Third: player irrelevance — if Act VI gives the player no verb, the game
becomes a screensaver; the player's verb here is verification and the authority to STOP,
and STOP must remain a real, respected control.

**Proof moment:** the diff the entity wrote and the test log that now passes, side by
side, on screen — plus the archive entry recording the lineage. The player did not write
the change; the player verified it. That is the end-game feeling, and it is earned only
because Acts 0–V made the player capable of judging what they are watching.

---

## 4. Session shapes

Two shapes, honestly split by who does the work (../GAME_PLAN.md section 2). Lower
chapters must never blur them: the game never pretends the UI wrote the code.

### 4.1 The solo field session — 10 to 30 minutes `[BUILT]`

Luis alone in the browser, between build sessions. Boot-to-input under 3 seconds, one lit
objective always, one to three missions or a partial arc. Field sessions run entirely on
real endpoints — fire a call, survey the field, load the meter, mine a slice, run a tick,
interrogate the entity. The shape bends to the real grid: a 60-second meter window fits
inside a session as an authored beat; a daily-quota exhaustion honestly ENDS a session —
"the grid is resting" is a legitimate session-out, not a bug. Design rule for all future
field content: a field mission must be completable inside one refill cycle of the
resources it touches, or it must say up front that it spans days. Real play so far:
two field sessions logged (09_PRODUCTION.md section 2).

### 4.2 The pair forge session — with Claude `[PLANNED — first forge is Act II, slice 2]`

A real engineering session wearing the game's frame. The game presents the recipe, the
spec, and the boss threshold; Claude writes, Luis judges; the boss check and the
fog-reveal run automatically after, from the real test result. One organ per session is
the ideal shape — a forge that sprawls across organs is scope drift and gets split. The
forge session is where the game's fiction and the AEA's actual construction are the same
hour of work; this is the whole reason Phase A can exist at all. Forge missions ARE the
real AEA engineering — a session that produces polish instead of capability is named
infrastructure-as-avoidance and stopped (standing law, 00_VISION.md section 7).

---

## 5. Friction philosophy — latency is truth `[BUILT as law; enforced in Acts 0–I]`

Real API latency is displayed, never masked, never decorated. This is a positive design
resource, not a cost to be hidden:

- The transmission wait in Act 0 is the game's first drama beat — the seconds between
  TRANSMIT and the answer are where "did anything hear me?" lives. A spinner that lied
  about that wait would strangle the act's only feeling.
- The 60-second meter watch (../missions.js M1.3) is authored waiting: "nothing speeds
  this up. patience is a resource the entity budgets for you." Waiting IS the mana
  lesson — the player learns quota-shaped thinking by feeling the window slide, and that
  lesson is the difference between a player who understands free-tier autonomy and one
  who has read about it.
- 429s and cooldowns route into the fiction as what they are: real starvation, plants
  cooling, the ladder falling to the floor. The failure copy names the truth ("a plant is
  cooling from a real 429") because a player who has felt starvation understands the
  entire economic argument for the hearth — local, unlimited, slow.

The law cuts both directions. Never hide real waiting; never add synthetic waiting. A
padded delay "for drama" is exactly as dishonest as a masked one, and both are failures
worse than ugliness. Tension in THE PROBE is only ever borrowed from reality, and reality
pays reliably: the grid genuinely does brown out, rods genuinely rot, the vein genuinely
depletes. Lower chapters (FUI, audio, motion) may amplify a real wait — a filling bar, a
breathing tone — but may never invent or truncate one.

---

## 6. What boredom means here — the boring test as a formal gate `[BUILT as gate]`

Boredom in THE PROBE is never treated as a decoration deficit. It is a diagnostic with
two named species, and each has a mandated fix:

- **Dashboard boredom** — live numbers with no verb attached. The player is looking, not
  doing. Fix: attach a mission verb or cut the panel. Never fix with animation.
- **Dead-world boredom** — nothing moves because the entity underneath is not doing
  anything. Fix: make the ENTITY do more (ticks, probes, real events), never the display.
  Simulated liveliness over a still entity is the cardinal dishonesty.

Legible waiting is not boredom (a bar filling for a stated reason is tension); illegible
waiting is (a stall with no visible cause). The distinction is the FUI chapter's problem
to solve and this chapter's law to demand.

The gate is formal and blocking: before any slice ships, the boring test runs — *would a
stranger call this a dashboard?* If yes, it does not ship, regardless of effort spent.
The decisive instrument is Luis piloting the slice in his own browser; his go/no-go gates
the next slice. Slice 1 passed this gate on 2026-07-20 (09_PRODUCTION.md). Aesthetic
dissatisfaction, when it comes, is presumed structural (form, composition, verb-density)
until proven cosmetic — the diagnosis starts at architecture, never at sprinkle-count.

---

## 7. The three player verbs — fly, interface, understand

Everything on screen serves at least one of three verbs; anything serving none is cut.

- **FLY** `[BUILT]` — the body. WASD+QE, drag look, chase cam, beacon, dock. Traversal
  makes knowledge spatial: the meter is a PLACE you return to, the foundry is a skyline
  whose one giant is the real capacity giant. Flying is how the world is memorized.
- **INTERFACE** `[BUILT]` — the hands. The diegetic PROBE OS: transmit, survey, mine,
  tick, talk, map, bestiary, codex. Every interface act lands on a real endpoint; the
  interface IS the fiction and the fiction IS the system. Feedback under 100ms, always.
- **UNDERSTAND** `[BUILT for Acts 0–I · PLANNED beyond]` — the win verb. Prediction
  confirmed by the live system: calling the meter's refill, the ladder's route, the
  council's regime, the gate's verdict. The map, codex, and bestiary are the score sheet
  of understanding, discovery-gated to real play. UNDERSTAND is the only verb the player
  keeps when the game ends — it is what Phase B exports, and it is the meta-thesis's
  cash value: a player who can predict the entity can build one.

The verbs are ordered by depth, not importance: FLY carries the session, INTERFACE
carries the mission, UNDERSTAND carries the game. An act that exercises only the first
two is tutorial tissue; every boss from Act I's drill to Act VI's archive is, in the end,
a test of the third verb.

---

## 8. How this chapter governs

Lower chapters derive from this one; the derivation rules are explicit:

1. **World (01_WORLD.md):** geography, fog, and atmosphere exist to stage the act
   feelings of section 3 — the dark serves Act 0's awe, reveals serve competence,
   district growth serves the forge acts. A world feature landing no act feeling is cut.
2. **Mechanics and missions (02_MECHANICS.md, 03_MISSIONS.md, ../missions.js):** every
   mechanic must survive the honesty test AND name which act feeling it produces; every
   mission's PROVE beat must be a proof moment of section 3's kind — a real event, never
   copy. The per-act threats are their regression checklist.
3. **FUI / audio / motion:** amplify real events only, within the two-ink law (amber =
   live, blue-gray = structure); their brief for waiting and legibility is section 5 and
   section 6 of this chapter.
4. **Tech:** endpoints, saves, and performance budgets exist to keep proof moments
   honest and sessions inside their shapes (section 4); any caching or mocking that
   would fake a proof moment is forbidden at the architecture level.
5. **Production (09_PRODUCTION.md):** the ledger tracks which act feelings have been
   PLAYED, not just built — a feeling is proven only by a playtest entry.

Conflicts resolve upward to this chapter and 00_VISION.md; amendments to the emotional
arc's threats and proof moments require the same bar as vision amendments — new evidence
or a Luis call, never drift.

---

## Changelog

- 2026-07-20 — v1. Authored as Part I (top of book) from ../GAME_PLAN.md, ../missions.js,
  and the live corpus; build-state marks verified against world.html, journey_save.json,
  and 09_PRODUCTION.md playtest entry 001.
