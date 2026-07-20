# E3_TRACKING — THE TRACKING DISCIPLINE

```
doc:          E3_TRACKING.md (THE PROBE design book — how ticket state moves, and the
              one page that renders it)
owner:        the game team
status:       ACTIVE — governs every status flip in tickets.json from 2026-07-20 on
last-updated: 2026-07-20
governs:      tickets.json (root — THE REGISTRY OF RECORD for every machine field:
              rows, status, rung, order, depends, gate, size, note) · tracker.html
              (root, served at /tracker) — and nothing else; INDEX.md §3 is a frozen
              2026-07-20 transcript (rows are no longer struck there; on any
              disagreement tickets.json wins), 09_PRODUCTION.md remains the log of
              record — edited 2026-07-20 (nine-critic closure)
reads:        INDEX.md §3–§4 (registry + session loop) · P0_PROTOTYPES.md (rungs +
              P0 SPEC ADDENDUM) · 09_PRODUCTION.md (ledger, guards)
laws:         honesty law absolute — every count on the tracker computed from the data,
              never typed · two-ink FUI (amber #ffb000/#d4a24c live · blue-gray
              structure) · NO emoji · marks [BUILT] / [PLANNED] / [DECISION-LUIS]
```

---

## 1. What exists

Three artifacts, no more:

- **tickets.json** [BUILT] — the registry of record. INDEX §3's T-001..T-082 transcribed to data, plus
  the four P0 SPEC ADDENDUM rows (ids `P0A-*`; two already DONE by the 2026-07-20
  final-sweep closure: the claim-ceiling string sweep and the /api/node/run channel
  constraint). A header block carries the P0–P13 rung ladder (title + exit criterion
  per rung, compressed from P0_PROTOTYPES.md — on any disagreement that chapter wins).
  Gate strings are verbatim from INDEX §3; `rung` is set only where the ladder names
  the work — `null` means not yet placed, and placement happens when a rung opens,
  never by guess. `order` (integer) is the in-rung build order, placed when a rung
  opens with the same discipline as `rung` (P0 seeded 2026-07-20 per P0_PROTOTYPES:
  T-066 first). Spanning tickets (T-026, T-027, T-029) carry the span in `note`.
- **tracker.html** [BUILT] — served at `/tracker` by controlroom.py; reads
  `/api/tickets` (tickets.json verbatim) and `/api/journey` (act/mission truth from
  the live save). Renders the RUNG RAIL (P0–P13, done/total per rung, current rung
  amber), the BOARD (tickets grouped by the twelve processes, filterable by rung and
  status), and the LEDGER strip (open [DECISION-LUIS] gate refs plus named holds,
  each with the tickets it blocks). The page opens ON the current rung ("all" is one
  click away), tops the board with a NEXT strip (the current rung's ready-and-ungated
  open tickets in `order`, computed at load), sorts visible tickets ready-first then
  by `order`, dims blocked rows with a computed "waits on T-xxx" chip, and renders the
  data file's `updated` stamp in the header — all computed, nothing typed.
- **This chapter** — the discipline. It is short because the discipline is small.

## 2. The state machine — who moves a ticket, and when

`open → doing → done → verified`. Four states, no substates, no percent.

- **open** — transcribed from INDEX §3, untouched. The default; 84 of 86 rows start here.
- **doing** — OPTIONAL, and it carries information in exactly one case: parking a
  genuinely mid-flight L ticket at session CLOSE. That flip requires a dated resume
  note ("doing since YYYY-MM-DD — <state>, resume at <step>"). The open -> done direct
  flip is legal and is the normal path; nobody hand-edits a status just to start
  working. More than two tickets flipped in one session is the scope alarm, not
  progress. — edited 2026-07-20 (nine-critic closure: mandatory open-flips rot solo)
- **done** — the change exists in code on disk and ran once. Compiling in your head
  does not count; neither does prose.
- **verified** — seen per INDEX §4 step 5: screenshot, live assert, or Luis's eyes —
  and anything touching emissive/bloom/tone-mapping on BOTH pipelines (risk R2).
  Only `verified` closes a ticket, with the evidence named in `note`.

**Who moves it: the session.** The human-plus-pair unit doing the work flips the field
by editing tickets.json — never the tracker page, never a background process, never
"cleanup". A flip without a session behind it is a lie in the data, which is the one
crime the honesty law does not forgive. Every status flip's note carries the date.

**The single-source rule (2026-07-20):** tickets.json is the registry of record for
every machine field — rows, status, rung, order, depends, gate, size, note. INDEX §3
is a frozen 2026-07-20 transcript: rows are NOT struck there, new tickets get NO
counterpart row there, and on any disagreement tickets.json wins. (Closure note: one
review proposed keeping INDEX §3 as a re-swept derived view; the freeze is the more
restrictive rule and wins — one registry, zero sync debt.)

## 3. The session-close ritual — one commit-equivalent

When a session ends, these land TOGETHER or not at all:

1. **tickets.json** — every status the session changed, with `note` naming evidence
   AND the date where the flip was to `done`, `verified`, or `doing` (parked).
2. **09_PRODUCTION.md** — the §1 slice entry / §2 playtest entry / §3 queue movement
   the flips correspond to. A ticket marked done without its 09 line did not happen
   (09's own change discipline, extended to the data file). At a rung exit, the 09
   ledger line also re-verifies E1's header ground-truth counts (wc + symbol grep).
3. **BOOK ledger** — if a [DECISION-LUIS] was called during the session, the row is
   STRUCK with date + one-line verdict (never deleted — the BOOK ledger's closure
   convention), the ledger line lands in the same breath, and any ticket the decision
   was gating loses its hold in tickets.json then, not later — strike, gate removal,
   and 09 line in the same commit-equivalent.
4. **The board renders.** Load /tracker once and see it render — a close where the
   board does not render did not close (verify-don't-claim, applied to the tracking
   file itself; the boot catch honestly renders nothing on a parse error).

One commit-equivalent is now LITERAL: the repo is a local git repository (initialized
2026-07-20, nine-critic closure) and a session close is one commit — a reader at any
point in history sees data, log, and ledger agreeing, and a tickets.json typo has a
revert path. Never flip the data in one sitting and write the log in another.
— edited 2026-07-20 (nine-critic closure)

## 4. The tracker page contract

- **Read-only, v0.** The page renders; it never writes. Status changes happen in the
  data file per §2–§3. If a write UI is ever proposed, it goes to the BOOK first as
  new scope — the discipline above is the feature, not a missing one.
- **Counts computed, never typed.** Every number on the page — rail counts, board
  group counts, header scores, ledger totals — is computed from tickets.json at load.
  A hardcoded count anywhere on the page is a bug of the honesty-law class.
- **Current rung = the lowest rung with a mapped ticket not yet VERIFIED.** Decided
  2026-07-20 (nine-critic closure): bare `done` does NOT release a rung — a rung whose
  tickets are all done-but-unverified stays current, because attention moving on while
  verification is owed is the exact verify-don't-claim hole. The rule is printed in
  the page footer. Rungs with no mapped tickets show 0/0 and cannot be current — the
  rail does not pretend to know what has not been placed.
- **One glance returns the next ticket, not just a rung name.** The page opens
  filtered to the current rung; the NEXT strip lists that rung's ready-and-ungated
  open tickets in `order`; blocked rows are dimmed with a computed "waits on T-xxx"
  chip; the header renders the data file's `updated` stamp. All computed from
  tickets.json at load — the contract line for every one of these views.
- **Honest failure.** If `/api/tickets` is unreadable the board says so and renders
  nothing; if `/api/journey` is unreachable the journey panel reads CARRIER LOST.
  Nothing is substituted, cached, or invented.
- Two-ink throughout: amber only for the current rung, done/verified state, and
  fired filters; everything structural stays blue-gray. NO emoji.

## 5. What deliberately does NOT exist

- **Burndown charts.** A burndown is a forecast wearing a chart. Nothing on a PROBE
  surface may show a number that is not measured truth; a projected completion date
  is not measured truth. The rung ladder's exit criteria are the only "when".
- **Velocity.** Velocity measures sessions against estimates nobody pre-registered,
  and invites optimizing the metric instead of the artifact — the exact failure the
  bench's multi-objective records exist to prevent in the game (R1 finding 8). We do
  not install in the studio the pathology we designed out of the product.
- **Estimates beyond S/M/L.** INDEX §3.0's convention is the ceiling. Hour-grain
  estimates are false precision on work whose honest unit is the session, and they
  feed the re-planning trap (09 §4): precise-looking plans invite re-planning instead
  of executing.
- **Percent-complete bars.** A percent implies equal units; tickets are S to L and a
  pair forge is not three checkboxes. Counts only — done/total, computed.
- **Assignees, due dates, sprints.** One team, one queue (09 §3 / the P0–P13 ladder),
  one calendar law (the income clock). A second scheduling system would be a second
  world, and the book bans second worlds.

Decisions with no build shape yet (#10, #14, #18, #23, #24, the mute hotkey, D-B2)
remain non-tickets per INDEX §3.0 — they enter tickets.json only when called, as new
rows, in the same commit-equivalent as the BOOK ledger line that calls them.

---

## Changelog

- 2026-07-20 — v1. Authored with the tracking system's first ship: tickets.json
  (registry as data), tracker.html (/tracker, read-only), the two controlroom.py
  routes (/api/tickets, /tracker). Statuses seeded all-open except the two addendum
  sweep closures marked done with notes.
- 2026-07-20 — nine-critic closure (Solo-Dev Pragmatist, Data Auditor, Producer).
  Single registry: tickets.json is the registry of record; INDEX §3 frozen as a
  transcript, the strike clause deleted here and in INDEX §4 step 6. `doing` made
  optional (park-at-close only, dated resume note); every flip's note carries the
  date. Ritual gains step 4 (the board renders) and the rung-exit ground-truth
  re-verify; git init makes the commit-equivalent literal. BOOK ledger closure
  convention named in step 3. Current rung redefined: bare done does not release a
  rung (the restrictive side of the Producer's fork, chosen deliberately). Tracker
  contract gains open-on-current-rung, the NEXT strip, ready-first ordering with
  waits-on chips, the `updated` stamp, and the `order` convention.
