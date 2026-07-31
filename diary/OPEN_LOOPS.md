# OPEN LOOPS - the pending steps, what each needs, and what the entity can DO when it lands

*Rewritten 2026-07-31. The 2026-07-28 version is superseded (its FINISH list is done: the kernel is
wired, the tree is committed, `known_good` earned at `44525f3`). Its RULE survives and is the reason
this file works at all.*

**THE RULE:** every entry has a verdict - `FINISH`, `LATER`, or `KILL`. An entry with no verdict is
the disease this file treats. A `LATER` still `LATER` in a month becomes a `KILL`.

**AND THE ADDITION LUIS ASKED FOR, 2026-07-31:** every step names three things, because "done" has
meant three different things on three different days -

    WIRING     what connects to what, and who calls it
    CODE       what has to be written or changed
    MILESTONE  what the ASSEMBLED entity can demonstrably do the moment it lands

A step whose milestone nobody can demonstrate is not a step, it is an intention.

---

## MEASURED RIGHT NOW - every number here is one command away, regenerate before trusting it

    python -m aea.lab.transfer      invented-ceiling 80 · silent-default 31 · unredirectable 7
                                    BLOCKING 0 · advisory 118
    trust.check                     gather_public TRUSTED · produce_brief DRAFT (demoted by its own
                                    80/97 failure rate - nobody had said that out loud) ·
                                    vary_own_knob DRAFT (granted and revoked 2026-07-31) ·
                                    self_modify_code FORBIDDEN
    knobs                           declared: depth, max_tokens, public_max_tokens
                                    proposable: carry.form, max_tokens, read.precedence
                                    APPLIABLE: max_tokens ONLY
    state/hands_ledger.jsonl        38 rows, 11 src=wake     (R2-REACH needs >=20 across >=3 tools)
    state/outcomes.jsonl            1 row
    state/experience.json           4 attempts
    state/crystal.json              0 parts
    python -m aea.lab.vital         6 steps declared - runtime: what RAN and what CHANGED
    python -m aea.tooling.assembly  5 steps declared - static: EVERY DECLARED STEP IS WIRED

---

## THE FLOW THAT GOT US HERE

R2 "nearly done" for a day -> the fleet was broken (1 living frontier rod, not 17) -> **RUNG = POWER
+ BOUND**, and only power had ever been gated -> the containment bound bought structurally in 15
seconds -> that bound RETRACTED for a wrong denominator and re-earned at 0.6% -> R3 designed,
refuted, cut from a platform down to four edits -> R3 wired end to end and the loop ran once -> the
ceiling sweep: the D29 fix had landed on one of three doors, and `hades` was judging a brief on its
first 1600 characters -> the grant, and its withdrawal when a hard audit found three of my safety
claims false -> `vital.py` and the ten QUALITIES, because static reachability cannot see a function
that runs and does nothing.

**The day in one line: the ladder moved one rung and the instruments moved five.**

---

# FINISH - everything else is blocked behind these, in this order

### 1. THE RATCHET · the one thing
The audit's answer to *why do small things pile up*: **a detection that changes no number and fails
no command is indistinguishable from no detection.** `transfer` finds 118 advisory findings right
now and nothing anywhere records that it was 118, so the 119th is invisible by construction.

- **WIRING** `aea/tooling/selfcheck.py` gains ONE invariant that runs `aea.lab.transfer` and compares
  per-shape counts against a committed `state/transfer_baseline.json`. Then the wake's action table
  (`aea/loop/live.py`, beside consolidate) gains `["-m","aea.tooling.selfcheck","--json"]`.
- **CODE** ~40 lines. Baseline today's counts. Any shape RISING turns `ALL INVARIANTS HOLD` into a
  failure. Deliberately NOT `blocking=True`: a check that always fails stops being read, and a
  ratchet tolerates the 80 we have chosen to live with while making the 81st a hard stop.
- **MILESTONE** *The entity runs its own verification, and the verdict is produced by the machine
  rather than by a human remembering.* Measured today: `battery`, `transfer`, `selfcheck`, `vital`,
  `assembly` and all four test files have ZERO non-prose callers, `.claude/settings.json` has zero
  hooks, and CLAUDE.md's claim that transfer "runs inside the battery so it cannot be skipped" is
  false in effect - the battery is never run either.
- **VERIFY** inject one `max_tokens=256` into a scratch module inside the tree, confirm selfcheck
  goes RED, remove it, confirm GREEN. A ratchet unproven against a deliberate violation is one more
  unrun test.

### 2. THE HANDOFF STOPS LYING · text only, zero runtime risk
`diary/SESSION_LOG.md` says `vary_own_knob` is GRANTED at ceiling 2 and revoked by lowering `level`.
Both false since `b397d93`. CLAUDE.md makes that file the single source of current state, so this is
the loudest false claim in the repo.

- **WIRING** none. **CODE** append the revoke entry; correct the lever to the CEILING; replace the
  LOCKED line "No invented ceiling anywhere on a model path" with the measured 80 / 118.
- **MILESTONE** *A cold reader who reads only the diary is not misled about what the entity may do.*

### 3. THE REFUSAL CARRIES ITS REASON
`_apply_knob` returns a bare `bool`, so a refused apply and a silently-broken applier leave
byte-identical durable state: `applied=False, refused=""`. That shape is in production
`heartbeat.json` at this moment, and the next tick writes it into experience as `note="refused: "`.

- **WIRING** `live._apply_knob` -> `hb["_r3_pending"]` -> `unstick.record` -> `experience.json`.
- **CODE** return `(ok, reason)`; store both; rewrite `move["to"]` to the value that LANDED, so the
  graded row records what happened rather than what was asked.
- **MILESTONE** *Every refusal in the entity's own record names why* - the honesty law reaching the
  one store R3 grades from.

### 4. THE MENU MATCHES THE TABLE
1 of 3 proposable knobs is appliable. `depth` and `public_max_tokens` were built, wired and verified
today and **nothing can ever propose them** - the same class as the four wrong-object edits with the
ends swapped: a reader that nothing can write.

- **WIRING** `unstick.moves_for` already filters by `appliable`; add proposers for `depth` (slow /
  unverified signature) and `public_max_tokens` (empty), and take the BLOCKED branch that already
  exists in `live.py` when the filtered menu is empty, with a pulse on it.
- **CODE** ~20 lines in `unstick.py`.
- **MILESTONE** *The entity has more than one thing it can actually try, and when it has none it
  says BLOCKED once instead of proposing the impossible forever.* Today the loop walls at ~tick 6.

### 5. R2a-REACH · the last open half of R2
11 wake rows against a required 20, across 2 tools against 3, in 1 situation against 8.

- **WIRING** the wake's own decision -> `decide.choose` -> `hands.invoke` -> the ledger, across
  genuinely distinct situations.
- **CODE** seed states where a tool IS the owed move - a self-map question, an unread state file, an
  arithmetic need - so the `WHEN` conditions are reachable rather than waited for.
- **MILESTONE** *R2 CLOSES.* WIRE true + BOUND 0.6% + REACH >=20 invocations / >=3 tools / >=8
  situations, every one traceable decision -> argument -> result -> record.

---

# LATER - real, evidenced, and not before the five above

- **The outcomes gate is a FUNCTION, not a property of the store.** REPRODUCED: `outcomes.write`
  correctly refuses an ungated row, then `grid.append_jsonl(outcomes._path(), row)` writes the same
  row and `read()` returns it indistinguishably. Fix: validate on the way OUT, or make the row carry
  something only `write` can produce.
- **`shadow.PROTECTED` reaches nothing at runtime.** Three callers, all inside `shadow.py`, and
  `protected("aea/kernel/../kernel/knobs.py")` is False. It is a property of the proposal pipeline,
  not of the filesystem - and I described it as stronger than it is.
- **`grid.load_json` on a `.jsonl` file QUARANTINES IT.** It found `hands_ledger.jsonl`
  unparseable, renamed it, and returned the default - destroying 38 rows including 11 of R2's own
  evidence, from one line in a survey script. Recovered only because quarantine renames rather than
  deletes. Fix: refuse to quarantine a path ending `.jsonl`, or give jsonl its own loader.
- **`state/xray.json` goes stale by design** - written only under `--json`, and it is the gate's
  no-new-orphans baseline. Fixed once this morning, stale again by afternoon.
- **677 `[:N]` slices in the tree and no detector for them.** Today's diff removed 23 and added 44.
  A verbatim truncation control driven through all six detectors fired none of them.
- **`dispatch.py`** - built, canary-gated, unwired. Required by R4 AND R5, so it is early work
  rather than deferrable work.
- **The eleven disagreeing constants** from `heal.py` - `TEMP` at 0.0 and 0.2 across 14 files.
  Real, cheap, unglamorous. Survives from the 2026-07-28 list.
- **R4-R9** - hazards named in `THE_RUNGS_RECAP.md`. R4 IS the design a council refused three times,
  unless it goes through the split dispatcher. R8 and R9 stay closed: no writable bound exists yet.

---

# KILL

- **Adding criteria to prove a rung.** The suite went 10 to 12 while three of them pointed at
  nothing real. The gate already names what to STOP measuring; adding is the reflex to resist.
- **Declaring a knob to unblock a proposal.** A knob with no reader is a false outcome record by
  construction. `carry.form` and `read.precedence` stay undeclared until an organ reads them.
- **Re-granting `vary_own_knob` before steps 2, 3 and 4.** Its own charter comment names those three
  as preconditions. The re-grant is raising BOTH level and ceiling to 2; nothing less does it.

---

## THE STANDARD ANY OF THIS IS MEASURED AGAINST

`aea/lab/QUALITIES.md` - ten angles, not two: RUNS · EFFECT · CORRECT · HONEST · BOUNDED · STABLE ·
ISOLATED · ATTRIBUTED · REVERSIBLE · DEGRADES. Eight of the ten were violated on the day it was
written. *A quality with no probe is an opinion, and presence is the weakest angle - it is the one
everyone builds.*

The machine-side twins of this file are `aea/lab/vital.py` (what RAN and what CHANGED, at runtime)
and `aea/tooling/assembly.py` (what is reachable, statically). **When this file and those manifests
disagree, they are the truth and this file is stale.**
