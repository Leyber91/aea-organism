# THE CLASS INTERIORS - where the nine real components actually live

*2026-07-27. Companion to THE_COMBINATION_MAP.md, which maps the 64 subsets and treats each class as
present or absent. This is the interior: which components sit inside each class, why they sit there,
and what each buys in trust terms. Five sections, every one rewritten after attack.*

**THE FINDING THAT ORGANISES EVERYTHING BELOW.** All nine components place into THREE of the six
classes. Eight of the nine capabilities the trust ledger actually grades live in the three EMPTY
classes. **The inventory and the ledger are close to disjoint** - we build parts for one region and
grade the entity in another.

**AND THE REASON IS STRUCTURAL, NOT HISTORICAL.** `STAGES = (shape, fire, read, repair, carry,
judge)`. Every stage is inside ONE EXCHANGE. There is no stage for across-a-restart, none for
outside-the-process, none for a version pair. So no existing component CAN serve PERSIST, ACT or
CHANGE - not because nobody wrote one, but because there is nowhere to seat it. **A new class needs a
new stage before it can need a new component.**

---

## THE PLACEMENT

Nine components exist, six classes exist, and the mapping is not one-to-one. Forcing it to be
one-to-one is what produced the four placement problems. What follows places each component by its
declared `kind` and `stage` in `aea/lab/organisms/catalogue.json`, because those two fields are
load-bearing at run time and the name is not.

One measurement rule for this section. The trust-ledger figures and the x24 figures are stated as
measured. Every other number below is a `receipt` or `warning` field the catalogue declares, quoted
as a declaration the file makes, not restated here as a measurement of this document.

### The rule used to place them

A component belongs to the class whose work its STAGE performs, graded by what its KIND buys in the
trust ledger. One field overrides the stage rule: `requires`. `call` and `latency` are the only two
components in the inventory that declare `requires: []`. Every other component requires `call`. One
of them runs first (`fire`, order 1) and the other runs last (`judge`, order 2, the final position of
the final stage), and neither takes a requirement from anything in between. They are the floor and
the roof of the pipeline, not members of anything inside it. That override is why `judge` splits:
`measure` at judge.1 requires `call` and keeps the stage rule, `latency` at judge.2 requires nothing
and leaves the classes entirely.

### SPECIFY: goal and frame

Both sit at `shape`, the only stage that runs BEFORE the call. A part at `shape` cannot see a result,
because no result exists yet. It can only change what is asked. That is SPECIFY by construction, with
no appeal to either name.

Both are `lever` kind, so both buy the same thing: a shorter path to `promote_after`. `goal` buys it
structurally, because without an objective there is nothing for a run to be correct about, and the
catalogue's receipt for it records zero successes across two no-objective and vague-objective
batteries. `frame` buys it conditionally and can run backwards. It is one of two components carrying
a variant classed `toxic` in the catalogue, the other being `carry:free`, and the toxic template is
in production: the instruction sentence `You are on the bench. Answer exactly and only what is asked.`
is `SCAFFOLDS["bench"]` at `aea/bench/bench_core.py:261`. The shipped string separates it from the
prompt with one newline where the catalogue variant uses a blank line; the sentence is identical.
Under slow up, fast down, a lever that raises the failure rate is not a weak lever, it is a demotion
generator. Prediction, from the mechanism: one manner-framed run zeroes the streak, and
`produce_brief` needs 7 consecutive clean runs to rebuild a level.

Note the asymmetry the catalogue already declares. `goal` and `frame` run before `call` in stage
order and still list `requires: ["call"]`. That is the code stating that a specification with no
recipient does nothing, which is the same claim THE_COMBINATION_MAP makes about the S singleton.

### SEE: readout, validation, measure, and critic under protest

`readout` and `validation` sit at `read`, the stage whose entire input is the text that came back.
Judging what came back is SEE, definitionally.

`readout` is a `lever` and buys the ordinary thing, a lower failure rate. Its own catalogue warning is
the interesting part: a method frame eliminates the condition it repairs, muteness going from a bare
rate to zero once fitted. A SPECIFY lever can retire a SEE lever. That is a cross-class interaction
the subset map cannot express, because both classes are simply present in it.

`validation` is the only `guard` in the inventory. A lever shortens the path to promotion. A guard
prevents demotion, and demotion is instant while promotion costs `promote_after` consecutive clean
runs: 3 for `speak`, 5 for `gather_public` and `reason_private_local`, 7 for `produce_brief`. One
prevented false commit preserves a streak that would otherwise cost up to 7 clean runs to rebuild.
That is the whole of what the kind axis licenses; it does not license ranking one guard against a sum
of levers.

There is a gap here the interior exposes. `validation`'s metric is `false_commitment_rate`, which
requires an abstain category to exist, and the pipeline does produce one, in two steps across two
components. The guard, in `aea/lab/parts/read.py`, emits `ctx.claim("validation", None, "declined",
declined=True)`. The gauge, in `aea/lab/parts/judge.py`, turns a `None` answer into
`ctx.verdict = "abstain"`, one of `pass`, `abstain`, `fail`. The ledger ends the chain:
`trust.record(cap, ok: bool, note: str = "")` takes a boolean. An abstention must be coerced to a
clean run or a failure, and either coercion destroys the quantity the guard is scored on. Prediction:
until `ok` carries a third value, seating the guard on a live capability will read as either a
suspiciously clean streak or an unexplained demotion, and both readings will be wrong.

`critic` is the hard case and I am filing it in SEE under protest, with the objection recorded rather
than resolved. Against SEE: its stage is `repair`, not `read`; its kind is `lever`, not `guard` or
`gauge`, so it is scored on the answer rather than on the verdict; and its default `recheck` template
is a complete second specification wrapped around the first answer, fired as a second call.
Mechanically it is a second organism, not a second opinion. For SEE: its input is a read, and
`repair` is the only stage in the pipeline with no class of its own, so filing it anywhere else
invents a seventh class to hold one component. The honest statement is that REPAIR is an unclaimed
stage.

The trust consequence is sharp, and it comes from where the catalogue attaches the harm. `frame` and
`carry` attach theirs to named non-default variants, `manner` and `free`. `critic` has no toxic
variant; its `warning` and its `conflicts` edge hang on the component itself, so the harm is attached
to the default seat. Its receipt declares bounded upside and losses concentrated on high baselines.
Prediction, derived from that profile against the promotion mechanism: never seat it on
`gather_public`. That row reads TRUSTED, streak 39, runs 44, fails 0, and it is at ceiling 3, so no
lever can promote it further. There is no upside available and one failure costs a level. Seat
`critic` only where a row has headroom and a low baseline.

`measure` is the keystone and it is the reason the class exists. Its kind is `gauge`: it makes the
`ok` flag honest, and without it no promotion is legitimate. It is the only component in the
inventory that produces the outcome variable rather than moving it. The caveat belongs in the
document: `measure` reads `ctx.task["truth"]`, and live state has no truth field. The shipped analogue
is the HADES accept named in `trust.py`'s own docstring and consumed at `aea/organs/brief.py:128`.
Its calibration against a known truth: -.

### REMEMBER: carry, alone, in four forms

`carry` is the only component at the `carry` stage and the only member of the class. Its metric,
`accuracy_over_sequence`, is the only metric in the inventory whose unit is a sequence rather than a
trial, and the ledger's promotion rule shares that unit: `promote_after` CONSECUTIVE clean runs.
Streak is the ledger's running value.

Stop the analogy there. A running number plus a lossy window resembles the `checkpoint` FORM by name,
and that resemblance licenses nothing: x24 graded token recall across chained model calls where the
carry is prompt text, while `trust.history` is a Python list of strings. The claim about the ledger
has to be read off the ledger. Reading it off: `record` keeps `streak`, `runs`, `fails`, and
`history` truncated to `[-20:]`, against 109 ticks in live state. It accepts a `note`, and
`aea/organs/brief.py:132` passes one for `produce_brief` while lines 130 and 131 record
`gather_public` and `reason_private_local` with no note at all. The line printed at every wake is
`check()['why']`, assembled from level, streak, runs, fails and ceiling, which never reads the note.
So all 30 recorded wakes read `AWAKE:brief FAIL :: trust ledger : produce_brief -> level 1`, naming
the transition and not the cause, 30 times. The cause field exists, two of three call sites leave it
empty, and nothing surfaces the one that is filled.

The x24 result stands on its own ground, which is intra-level variation inside REMEMBER: one
component in three forms spanning conversation at 144/144 token recall, Wilson [0.974, 1.0], free at
7/144, Wilson [0.024, 0.097], and checkpoint at 0/144, Wilson [0.0, 0.026], while checkpoint got 43
of 48 sequences right. The form that does the work best is the form that remembers nothing.

This settles placement problem 2 and goes one step further. World 3's CHECKPOINT and CONVERSATION are
forms of `carry` (`FORMS = ("none", "checkpoint", "conversation", "free")` in
`aea/lab/parts/carry.py`). RECALL is not among them: a name with no form, no key, and no code. The
unnamed fourth form is `free`, classed toxic and measured by x24 at 7 of 144. World 3 does not have
three components, and it does not have three forms either. It has one component in four forms, one of
which is poison and one of which the world never named.

### Outside all six: call as floor, latency as roof

`call` is `enabling`, the only kind with `metric: null`, declared "not scored." A class is a
capability whose presence changes an outcome; `call`'s absence removes the possibility of one.

Be exact about what it gates in the ledger, because the row is not it. The `CHARTER` authors the
rows: `_entry` creates any charter capability's entry from defaults on first touch, `check` returns
that starting level, and `board()` iterates `CHARTER.items()` and prints all nine rows whether or not
anything has ever run. What `call` authors is the RUN. With no call there is no `record`, so the row
exists, sits permanently at streak 0, and stays frozen at whatever level a human granted it, forever.
That is the enabling kind stated in ledger terms: not scored, and without it nothing is scored. The
only genuinely unrepresentable case is a capability absent from `CHARTER`, where `_entry` raises
`KeyError` and no row can be printed at all, and that is the charter's doing rather than the call's.
Placement problem 3 was half right about `call`: it belongs to no world because it belongs beneath
every world.

`latency` is the mirror image, and this is the correction to the other half of placement problem 3.
It is a `channel`, the only one, and its kind buys attribution: without it a demotion says something
broke, not what. It requires nothing and, as its own catalogue warning says, depends on everything.
Nothing requires it in return, so it is the roof. It is not a member of SEE, because it does not
judge; separability is not a verdict. Its receipt declares the separation as strongly rod-dependent,
a wide ratio on one rod and roughly none on another. A channel with rod-dependent bandwidth.

Placement problem 3 said `latency` is assigned to no world. It is assigned to World 2, under the name
CLOCK: catalogue key `latency`, name `THE CLOCK`, census C-74, and
`design/THE_SIX_WORLDS.md:94` already lists it as a built World 2 channel. The audit that found it
homeless was matching keys against a world list written in names, and it counted the same part as
both missing and aspirational. That resolves one third of placement problem 1: of World 2's three
supposedly nonexistent components, CLOCK exists and is `latency`. LADDER (C-06, the prompting ladder,
distinct from the energy ladder in `energy/energy.py`) and COUNCIL remain genuinely componentless. On
the GAME axis the player must hold CLOCK somewhere and World 2 is the right slot. On the CLASS axis
it is a roof over all six, because it takes no requirement from any of them.

### The table

| component | kind | stage | class | what it buys in the ledger |
|---|---|---|---|---|
| `call` | enabling | fire.1 | none, the FLOOR under all six | the RUN. The CHARTER authors the row; without a call `record` is never invoked and the row freezes at its human-granted level with streak 0 |
| `goal` | lever | shape.1 | SPECIFY | a lower failure rate, so a shorter path to `promote_after`. Structurally prior: with no objective there is nothing for a run to be correct about |
| `frame` | lever | shape.2 | SPECIFY | a lower failure rate in its method variant. Its manner variant is a demotion generator and the sentence ships in `bench_core.SCAFFOLDS["bench"]` at line 261 |
| `readout` | lever | read.1 | SEE | a small cut to the failure rate at zero tokens. A method frame retires its only condition |
| `validation` | guard | read.2 | SEE | prevented DEMOTION, preserving a streak worth up to `promote_after` runs. Currently unrepresentable: guard declines, gauge abstains, `record` takes a bool |
| `critic` | lever | repair.1 | SEE, filed under protest. `repair` is an unclaimed stage | the only component whose declared harm hangs on the component rather than a named variant. Raises demotion risk exactly where baselines are high |
| `carry` | lever | carry.1 | REMEMBER | the only metric whose unit is a sequence, the same unit as `promote_after` |
| `measure` | gauge | judge.1 | SEE, and its keystone | the honest `ok`. No gauge, no legitimate promotion. The only component that produces the outcome variable rather than moving it |
| `latency` | channel | judge.2 | none, the ROOF over all six | attribution. `record` has a `note` field; nothing writes timing into it and `check()['why']` never reads it |

### The count, and what it says

Placed in classes: seven of nine. Outside as floor and roof: two.

```
SPECIFY   2    goal, frame
SEE       4    readout, validation, measure, critic
REMEMBER  1    carry
PERSIST   0
ACT       0
CHANGE    0
floor     1    call
roof      1    latency
```

Every component in the inventory sits in the first three classes of six. That is the shape
THE_SIX_WORLDS already records for Worlds 4, 5 and 6. What is new is the second count, taken from the
other side.

The `CHARTER` in `aea/kernel/trust.py` names nine capabilities. Reading them by class is a judgement,
not a field in the file, and the reading used here is: `gather_public`, `produce_brief`, `speak`,
`draft_outbound`, `send_outbound`, `spend_money` and `manage_keys` are ACT; `self_modify_code` is
CHANGE; only `reason_private_local` sits in the S/E/R region. Two of those are arguable in the other
direction, `gather_public` because its work is fetching and reading, and `produce_brief` because it is
an ACT wrapped around an S/E/R interior. The count survives either reading: eight or seven of nine
graded capabilities live in the three classes that have zero components, while seven of seven placed
components live in the three classes that hold at most two graded capabilities.

**The inventory and the ledger are close to disjoint.** The lab has been building the instrument that
judges work, and the entity has been graded on work the instrument cannot reach.

The mechanism, not the class labelling, is what bounds any repair. Five of the nine charter rows sit
AT their human ceiling and no component of any kind can lift them: `gather_public` at 3 of 3,
`draft_outbound` at 1 of 1, `send_outbound`, `spend_money` and `manage_keys` at 0 of 0. Four rows have
headroom. `speak` reads WATCHED at streak 2 of 3 and is one clean run from TRUSTED with no component
involved. `self_modify_code` sits at 0 with ceiling 1 and `promote_after` 99. That leaves
`produce_brief` (DRAFT, 40 runs, 34 fails, pinned) and `reason_private_local` (DRAFT, 42 runs, 35
fails, pinned) as the only two rows where a component that lowers a call's failure rate could plausibly
change the level. Prediction, checkable in one afternoon: seat all nine on the live entity and those
two rows are the whole of what can move on component strength.

Four of nine in SEE is the honesty law expressed as a build order: the class that makes an `ok` honest
was built before the classes that would generate `ok`s worth having. The cost is now nameable. Two of
the nine buy things the ledger cannot currently carry, for different reasons. `validation` needs a
third value in `ok`, which does not exist. `latency` needs its signal written into the `note` field,
which does exist and which `check()['why']` never surfaces. One is a missing field; the other is a
field nobody wired. That is where the interior says the next work belongs, and neither piece of it is
a component.

---

# THE CLASS INTERIORS: SPECIFY and SEE

Companion to `design/THE_COMBINATION_MAP.md`. The map treats each class as present or absent. This is the interior: which real components sit inside, in what order, and what each one buys against the trust ledger.

### EVIDENCE TIERS

- **MEASURED.** The live trust ledger (2026-07-27, 109 ticks, 6 boots) and x24. Nothing else.
- **CODE FACT.** A structural property of the source, cited by file and line, checkable by reading it. Carries no rate.
- **CATALOGUE CLAIM.** A direction recorded in `organisms/catalogue.json` or `THE_SIX_WORLDS.md`, attributed to its experiment. The figures stand in those files. This document does not restate them as measurements, so where a figure would go there is a dash.
- **PREDICTION.** Everything else.

### PLACEMENT: ONE PROBLEM DISSOLVES, ONE SURVIVES

**CLOCK is `latency`, and the identification rests on kind, not on the name.** `THE_SIX_WORLDS.md:94` lists CLOCK as a **channel** scored on **separability**. `latency` is the only channel in the catalogue and separability is its declared metric, and the receipt quoted in the world file is `latency`'s catalogue receipt. The name corroborates (`catalogue.json` keys `latency` as `THE CLOCK`, census C-74) but cannot carry the claim alone: `organisms/namespaces.json` records LADDER as a same-word-different-thing collision, where World 2's LADDER is C-06 with no lab part while a BUILT `ladder` module in `energy/energy.py` is the draw schedule. Name matching is the documented defect here. Kind plus metric plus a shared receipt is not.

So one bullet of the stated placement problems is wrong rather than in tension: `latency` is assigned, to World 2. `LADDER` and `COUNCIL` remain aspirational. **`call` is the only genuinely unassigned component.**

**`call` belongs to SPECIFY, on two declared fields.**

- **Stage.** The pipeline runs `shape, fire, read, repair, carry, judge` (`catalogue.json`, `stages`). `goal` is shape.1, `frame` is shape.2, `call` is fire.1. Fire is the issuing of what shape built, and nothing sits between them. A class that writes a specification and never issues it has no fire stage; seating `call` is what makes SPECIFY a class that does something.
- **The requires graph.** Every part except `latency` declares `requires: ("call",)` (`shape.py`, `read.py`, `repair.py`, `carry.py`, `judge.py`). A part that read, repair, carry and judge all depend on cannot sit inside any one of them. It sits where they all attach, which is the end of shape.

The combination map's `S` cell reads "the specification has no recipient inside the system, nothing in this subset executes." That is the absence of `call` described from the other side. Corroboration, not proof.

**The named trade-off.** SEE cannot be switched on alone. **CODE FACT:** `Latency.run` reads `ctx.rec.get("elapsed_s")` (`judge.py`), and `Call` is the only writer of `elapsed_s` (`fire.py`). So `E` without `S` is seatable in exactly one configuration, `latency` by itself over a field nobody wrote, and it reports a dash. The honesty law appearing as a structural property rather than as a rule.

---

### SPECIFY: THREE COMPONENTS, ONE OF THEM THE FLOOR

| order | component | kind | stage | what it buys in trust terms |
|---|---|---|---|---|
| 1 | `goal` | lever | shape.1 | shortens the path to `promote_after` by lowering the failure rate at the source |
| 2 | `frame` | lever | shape.2 | the same, and it ships a variant with a negative sign |
| 3 | `call` | enabling | fire.1 | the difference between FORBIDDEN and any level at all |

**CODE FACT:** `Goal.run` prepends `"{goal}\n{prompt}"`, `Frame.run` then formats `"{method}\n\n{prompt}"` over that result (`shape.py`), and `Call.run` sends it (`fire.py`). With both seated the wire carries method text, then objective, then data.

### THE ENABLING COMPONENT'S TRUST VALUE IS NOT A RATE

Every other component argues about the level. `call` argues about whether a run happened at all. Without it the organism does not fire, no verdict is produced, `record(cap, ok)` is never invoked, and the row moves in neither direction. That is the FORBIDDEN boundary expressed in ledger terms: not a zero, an absence of events.

**Do not reach for the CHARTER argument.** `trust.py:60` raises `KeyError` for a capability absent from `CHARTER`, which is a real property of a human-authored dict of nine entity capabilities. It has nothing to do with the lab's `call` part, and `namespaces.json` exists because claims about one registry have been read as claims about the other, the defect it says invalidated four census closures. The two are homonyms at the level of the word "enabling".

### GOAL AND FRAME ARE NOT INDEPENDENTLY SEATABLE

**One, the method text restates the objective.** **CODE FACT**, readable in `organisms/tasks.json`. `wordcount` goal: *"Count the words in the sentence below and reply with the number."* Its method opens: *"To count words: split the sentence on spaces, number each token 1, 2, 3 and so on, then report the FINAL index. Show the numbered list, then the count alone on the last line."* `batball` goal asks how many cents the ball costs; its method opens *"Let b be the ball in cents."* Seating `frame` without `goal` does not remove the objective. It relocates it, and adds a procedure and an output format alongside.

**Two, the runtime ORs them.** `judge.py:17`: `verdict_is_empty = not (ctx.has("goal") or ctx.has("frame"))`. The gauge already treats either component as satisfying "an objective is present."

**Three, `frame` is not seatable on one sixth of the bank.** `Frame.run` does `template("frame", v).format(prompt=..., **ctx.task)` (`shape.py`), and `tasks.json` shows `extract` carries no `method` key. The one task with no method is the task where the frame is a crash rather than a control.

**Consequence.** SPECIFY does not hold two independent levers. It holds one objective lever with two delivery routes, the second bundling a procedure and a format into the same string. The frame-alone cell of the lab's 2x2 is not "method without objective."

**CATALOGUE CLAIM:** x12 records the no-objective condition failing on every clean trial and again with a vague objective; x19, quoted in `THE_SIX_WORLDS.md`, scores method-alone well above the goal-absent condition. Figures: -. Under a clean factorial those two should sit together. **PREDICTION: the gap is the restatement, not the procedure.** Falsifier 1.

**What the combination map inherits.** `S` present-or-absent is two cells. The interior gives three conditions: no objective; objective; objective delivered twice with a procedure and a format between them. The fourth logical cell, procedure without objective, has never been run because no seat produces it.

### THE TOXIC VARIANT SHIPS

**CATALOGUE CLAIM:** the `manner` variant of `frame` is declared `"class": "toxic"` and recorded as the most harmful thing measured in World 1. Figures: -. **CODE FACT:** `bench_core.py:263` defines `SCAFFOLDS["bench"] = "You are on the bench. Answer exactly and only what is asked.\n{prompt}"`, which is the catalogue's `manner` template with a single newline instead of a double. The variant the catalogue marks toxic is in the shipped bench path, not only in the lab.

**PREDICTION, against the mechanism.** A lever with a negative sign raises the per-run failure rate, and `trust.py:101` zeroes the streak on any failure. A capability needing `promote_after` consecutive clean runs therefore does not promote slowly under an elevated failure rate; it stops promoting. **MEASURED:** `produce_brief` needs 7, has 40 runs and 34 fails, and sits at DRAFT with streak 0. Attributing that row to the scaffold specifically is not established.

### GRADES REACHABLE FROM SPECIFY ALONE

**PREDICTION.** None earnable. SPECIFY writes no verdict, so `record(cap, ok)` receives a boolean nothing computed, and the level stays where the charter put it. This is the combination map's silence argument unchanged. The interior adds only that seating both levers does not move it: two levers with no gauge produce a better answer that nothing grades.

---

### SEE: FIVE COMPONENTS, FOUR OF THE FIVE KINDS

| stage.order | component | kind | metric | trust mechanism it touches |
|---|---|---|---|---|
| read.1 | `readout` | lever | accuracy | shortens the path to `promote_after` |
| read.2 | `validation` | guard | false_commitment_rate | prevents demotion, conditionally, see below |
| repair.1 | `critic` | lever | accuracy | shortens the path, and holds top precedence |
| judge.1 | `measure` | gauge | can_know | **makes the `ok` flag honest** |
| judge.2 | `latency` | channel | separability | makes a demotion attributable |

SEE lacks `enabling` structurally rather than by oversight: `call` sits in SPECIFY and four of these five require it. On kind distribution, `gauge`, `guard` and `channel` each appear in exactly one class and all three are in SEE, while `enabling` appears in exactly one class and that is SPECIFY. **Four of the five kinds are single-class. `lever` is the only kind spread across classes:** two in SPECIFY, two in SEE, one in REMEMBER.

That is why the map's "no SEE means no honest ok" holds, and the interior sharpens it: it is not SEE that produces the ok flag, it is one component inside SEE.

### THE GAUGE IS THE PROMOTION KEY AND IT IS A SINGLE POINT

**CODE FACT:** `ctx.verdict` has exactly one writer, `judge.py:15` inside `Measure`. `base.py:54` initialises it to `None` and nothing else assigns it.

So a SEE interior of `readout` + `validation` + `critic` + `latency` is four fifths of the class, three of its four kinds, and no promotion signal at all. **PREDICTION: the class is not gradable in degrees of completeness. It is one binary, is the gauge seated, with four modifiers.**

### THE ENTITY DOES NOT FREEZE. IT SUBSTITUTES

The rule is that without a gauge a capability freezes at whatever level a human granted it. In the lab that holds exactly, because `verdict` stays `None`. In the running entity it does not, because the `ok` flag is computed ad hoc at each call site. **CODE FACT,** the four live `trust.record` call sites and the expressions feeding them:

```
gather_public         "fetch failed" not in status_txt.lower()      substring test
reason_private_local  boundary_ok and "ERR" not in focus_txt[:40]   substring test
produce_brief         HADES verdict == "accept" and sections_ok     independent judge
speak                 spoke = speak.speak(reply)                    subprocess return
```

One of four consults an independent judging stage. **MEASURED,** against those flags: `gather_public` TRUSTED, 44 runs, 0 fails, streak 39. `speak` WATCHED, 2 runs, 0 fails, streak 2. `produce_brief` DRAFT, 40 runs, 34 fails. `reason_private_local` DRAFT, 42 runs, 35 fails.

**The two rows that have never failed are the two whose flag cannot express the failure that matters.** `gather_public`'s flag tests whether a fetch errored, not whether what came back was right. `speak`'s tests whether audio played, not whether what was said was true. The one row judged by a separate stage sits at the floor.

That ordering is not evidence that the ungauged capabilities are better. **PREDICTION: it is what a ledger looks like when the gauge is optional and three of four capabilities declined it.** A gauge-free promotion is a moving level with nothing behind it, and it reads identically to an earned one on `board()`.

**Pre-registered, and one run from resolution.** `trust.py:38` sets `speak` to `promote_after` 3, ceiling 3. **MEASURED:** streak 2. One clean run promotes it to TRUSTED, the grade `gather_public` holds, on a text-to-speech return code. **PREDICTION: that promotion will occur and will be illegitimate,** because nothing in the path gauges the content of the utterance. If it happens, record it as an ungauged promotion rather than as a third TRUSTED capability.

### THE GUARD: THE BRIEF'S RANKING IS A DESIGN TARGET, NOT A DESCRIPTION

`Measure` produces three verdicts, `pass`, `abstain`, `fail` (`judge.py:15`). `record(cap, ok: bool)` accepts two (`trust.py:82`). There is no third outcome anywhere in `trust.py`.

**Two corrections before the argument runs.**

*The registries are not wired.* No lab part calls `trust.record`. The collapse that is live belongs to HADES, on `produce_brief`: `hades.py:46` returns `verdict: "unverified"` with `on_goal=False, correct=False` when the watcher cannot parse, and `hades.py:79` computes `accept = v.get('verdict') == 'accept' or (v.get('on_goal') and v.get('correct'))`, so an unparseable verdict reaches `record` as `False`. An abstention treated as a failure, one layer above the lab's guard.

*The demotion rule has a floor the brief omits.* `trust.py:102` demotes only `if e["level"] > min(1, c["ceiling"])`. A capability at DRAFT with a ceiling of 1 or more cannot fall further. **MEASURED:** `produce_brief` at 34 fails and `reason_private_local` at 35 fails are both still level 1. Above the floor a failure costs a level and the streak; at the floor it costs the streak only.

**PREDICTION, conditional and stated as such.** If a three-valued verdict is wired into a boolean `record`, abstentions arrive as failures, and a guard then destroys streaks that a lever would have converted into passes, while converting nothing into a pass itself. Under that wiring the guard ranks below the lever. **CATALOGUE CLAIM:** x17 records the guard taking a rod that needs nothing from a clean sweep to zero, every loss a forced abstention; figures: -. Against a boolean ledger that is a clean streak destroyed by the safety organ.

**The fix is one signature.** `record` needs a three-valued outcome where `abstain` holds the streak: not advanced, not demoted. Then a capability that refuses forever neither earns autonomy nor loses it, which is the honest treatment, and the guard becomes what the brief says it is.

### THE SEAM

**CODE FACT,** from `base.py:40-54` and its comment. Four parts used to assign `ctx.answer` directly, last writer winning, which is why this lab's flagship result "adding validation subtracts the recoverable capacity" was a statement about a shared mutable slot rather than about guarding. Now each part claims its own key, `claim()` raises `RuntimeError` on a second write to that key (`base.py:69-75`), and the winner is resolved by a declared tuple, `READ_PRECEDENCE = ("critic", "validation", "readout", "call")` (`base.py:15`), overridable through the config key `{"read": {"precedence": [...]}}` (`base.py:53`). The tuple was chosen to reproduce the old resolution order.

**So the interference is now a variable rather than an accident.** The mechanism that produces it is visible in the claim sites: `Validation` always claims, either a value or `declined=True` (`read.py:54-60`), while `Readout` claims only when it finds a work-read (`read.py:79`).

**PREDICTION, and it is a mechanism prediction, not a rate.** Under a lever-first ordering, `("critic", "readout", "validation", "call")`, a recovered work-read outranks a declined claim, and on a reply where the readout finds nothing to claim the guard still wins by default because it is the only claimant. If that holds, "adding validation subtracts the recoverable capacity" is a property of the resolution order and not of guarding, and one config key recovers the lever without removing the guard. Whether it trades recoveries for false commitments on real fuel is falsifier 2.

**Standing caution.** `read.py` carries a live defect frozen KNOWN-BAD in the golden trace, where the total pattern returns an operand instead of a total on narrated arithmetic. **PREDICTION: lever-first is correct where the work reader is sound and dangerous where it is not, so precedence should be measured per dialect rather than set globally.**

### THE CRITIC HOLDS TOP PRECEDENCE, WHICH NOBODY DECIDED AS A JUDGEMENT

**CODE FACT:** `critic` is first in `READ_PRECEDENCE` (`base.py:15`), and `repair.py:36` claims unconditionally, falling back from a stated read to a work read. A critic seated beside a guard and a lever wins the answer slot outright, over an abstention and over a recovered work-read.

**CATALOGUE CLAIM:** x20 records the upside bounded inside the noise band, losses concentrated on high baselines, and a cost multiplier above 1; figures: -. The catalogue warning reads "it breaks what was already right. Seat when stuck, remove when not." **The component with the worst recorded downside in the class holds the highest authority in the class,** which is a consequence of the precedence tuple and is unstated anywhere in the design book. **PREDICTION: on a capability holding a live streak near its ceiling, seating the critic is the fastest way to lose the streak,** because it overrides correct reads on exactly the high baselines where its losses concentrate.

### GRADES BY PARTIAL INTERIOR

**PREDICTION throughout**, derived from `trust.py` and the single-writer analysis. Every "highest earnable" is additionally capped by the charter ceiling, which no seat can raise.

| interior (all include `call`) | kinds | verdict written | highest grade earnable | why |
|---|---|---|---|---|
| bare | enabling | no | none; the level holds or drifts on a substituted flag | no writer of `ctx.verdict` |
| + `latency` | + channel | no | unchanged | a channel annotates, it never judges |
| + `readout` | + lever | no | unchanged | a better answer nothing grades |
| + `validation` | + guard | no | unchanged, and now it refuses | an abstention nobody receives |
| + `measure` | + gauge | **yes** | **3 TRUSTED**, ceiling permitting | first legitimate promotion signal in the system |
| `measure` + `readout` | gauge, lever | yes | 3, and sooner | the lever lowers the per-run failure rate, shortening the run to `promote_after` |
| `measure` + `validation` | gauge, guard | yes | **1 DRAFT under a boolean `record`, 3 under a three-valued one** | abstain maps to `ok=False`, which zeroes the streak every time it fires |
| `measure` + `readout` + `validation` | gauge, lever, guard | yes | **set by a config key, not by the seat** | THE SEAM |
| + `critic` | gauge, 2 levers, guard | yes | 3, at the highest variance in the class | top precedence for the part with the worst recorded downside |
| all five | 4 of 5 kinds | yes | 3, and the only interior where a demotion is **attributable** | the channel separates a slow wrong run from a fast right one |

### CROSS-CLASS: SPECIFY PREEMPTS SEE

The seam is intra-class. There is a second interference and it runs between these two classes.

**CATALOGUE CLAIM:** the `readout` warning reads "a method frame ELIMINATES the condition this repairs: mute goes bare to fitted," with figures at -. So SPECIFY's `frame` deletes the condition under which SEE's `readout` acts.

**PREDICTION: the value of a SEE lever is conditional on the SPECIFY interior being incomplete.** The two classes are not additive and the combination map's `S E` cell is not the sum of its parts. A part measured on a battery with the frame seated will read inert, which is the reading x18 records for `readout` and is what that reading means rather than what it disproves.

### WHAT TO SEAT FIRST, ONE RECOMMENDATION

**Seat `latency`, then `measure`, then fix the seam, then the guard, and seat the critic last or never.**

`latency` is the only component in either class that requires nothing and cannot make the answer worse: it never claims a read, it only notes (`judge.py`). Under slow up, fast down, the expensive event is not the demotion, it is the undiagnosed demotion, because the streak is gone either way and only attribution says whether to fix the fetch, the frame or the rod. `measure` follows because nothing else can legitimately promote anything. The guard comes after `record` grows a third outcome, not before. The critic comes last because it holds top precedence over parts that were already right.

**The trade-off, named.** This ordering optimises for an honest grade, not a high one. It will make the board look worse before it looks better, because a gauge seated on an ungauged capability converts invisible failures into recorded ones. **MEASURED:** `produce_brief` at 34 fails in 40 runs is what that looks like, and it is the only row on the board judged by a separate stage.

### FALSIFIERS, PRE-REGISTERED

1. **The restatement confound.** Strip the objective from the method text on `wordcount`, where the method opens by naming the goal, and run method-alone. If it still scores near x19's method-alone figure, the restatement account is wrong and the procedure carries the effect. If it collapses toward x12's no-objective condition, `goal` and `frame` are one lever and the SPECIFY 2x2 must be re-run.
2. **The seam on real fuel.** Run `call+readout+validation` under both precedence orderings across the rod set. If lever-first raises the false-commitment rate at all, the free-fix reading is wrong and the current ordering is defensible.
3. **The ungauged promotion.** If `speak` reaches TRUSTED on a TTS return code, record it as an ungauged promotion. If something in that path is found to gauge the content of the utterance, this section's account of the live board is wrong.
4. **The guard's true value.** Give `record` a three-valued outcome where abstain holds the streak, then re-run the x17 rod. If the guarded arm holds its streak while the unguarded arm eventually commits and demotes, the brief's ranking is confirmed and the boolean signature was the whole gap.
5. **The critic's precedence.** Seat the critic on a capability holding a live streak above the floor. If it demotes faster than the same seat without it, top precedence for the highest-variance part is a defect rather than a choice.

---

### R REMEMBER, the interior

Every other class is a set of parts. REMEMBER is one part, `carry`, in four forms. There is no subset
question inside this class, only a choice of form, and that choice is the only intra-level variable
this lab has measured to publication standard.

```
carry    lever    stage carry.1    metric accuracy_over_sequence    requires call
FORMS    none, checkpoint, conversation, free        aea/lab/parts/carry.py:9
```

That is the whole class. No gauge, no guard, no channel, no second lever. Read against the trust
mechanism, REMEMBER can do exactly one thing: shorten the path to `promote_after` by lowering the
failure rate on work that spans more than one call. It cannot make the `ok` flag honest, it cannot
prevent a demotion, and it cannot make a failure attributable. Those three jobs belong to `measure`
(gauge), `validation` (guard) and `latency` (channel), all of which sit in class E SEE, and no amount
of memory substitutes for any of them.

The placement correction is here. `design/THE_SIX_WORLDS.md:23` assigns World 3 three components named
CHECKPOINT, RECALL and CONVERSATION. Those are not three components. They are three of the four FORMS
of `carry`, and RECALL is not one of them at all: the fourth form is `free`. World 3 has one component
and four settings, and the roster it earns comes from the settings, not from a parts list.

One correction to the correction, because it is the same class of error running the other way.
`design/THE_SIX_WORLDS.md:22` assigns World 2 a component called CLOCK, and CLOCK is not aspirational.
It is the catalogue display name of `latency` (`catalogue.json`: key `latency`, name THE CLOCK, stage
`judge`, order 2, kind `channel`), and `THE_SIX_WORLDS.md:94` describes it with `latency`'s own x13
receipt. So `latency` is not unassigned. It is assigned to World 2 under its display name. LADDER and
COUNCIL have no part behind them; CLOCK does. RECALL does not. Match components by key, never by
display name, and three of the four reported placement problems change shape.

---

### The four forms, as the code implements them

| form | what crosses the call boundary | cost | source |
|---|---|---|---|
| `none` | nothing. Deliberately empty | zero | `carry.py:pack` - a control that hands the running value forward IS a checkpoint |
| `checkpoint` | one line, `The running value is {value}` | one line of input | model writes `STATE: value=..., step=...`, regex-extracted (`carry.py:7`) |
| `conversation` | the full prior exchange as message history | INPUT tokens, growing | the container `chain.py` built and did not send until 2026-07-27 |
| `free` | the running value plus a self-authored `NOTE:` to the next step | one line plus the note, capped at 1200 chars | the model chooses what to keep |

`none` is a true null: handed `Step 5: add 209` with no running value, a rod can only be right at step
1, where the task states the start. It is the floor that proves the containers do anything at all, and
it is not a baseline for length tuning.

---

### The measurement: x24, 2026-07-27

Source for every figure below: `state/lab/runs/x24_the_store_and_the_door/20260727T123912Z.json`,
status complete, design `130ea49d33bd`. 24 distinct chains generated fresh, 2 samples each, all four
forms on every chain, six rods, Wilson intervals per cell, McNemar exact on paired chains, never
pooled across rods. Seat: `call + goal + frame + readout`. Two axes, measured separately:

- **THE WORK.** Sequence correct, judged by a strict `ANSWER:` anchor. Parse failures counted apart
  from wrong answers, so a form that changes format compliance cannot masquerade as a form that
  changes capability.
- **THE REACH.** Each probed step carries a random token of the form `XX-0000` generated per chain.
  Reproducing it is retrieval and can be nothing else. Value probes run beside it, and the gap between
  value and token is the recomputation rate.

```
rod (chain length)          form           WORK correct    REACH token recall
--------------------------------------------------------------------------------
nemotron-3-super-120b (3)   none                0/48            0/144   [0.0, 0.026]
                            checkpoint         11/48            0/56    [0.0, 0.064]
                            conversation        0/48              -     no probe reachable
                            free                0/48              -     no probe reachable
nemotron-3-nano-30b (3)     none                0/48            0/144   [0.0, 0.026]
                            checkpoint         32/48            0/144   [0.0, 0.026]
                            conversation       35/48          101/129   [0.704, 0.845]
                            free               16/48           18/140   [0.083, 0.194]
nemotron-3-nano-omni (7)    none                0/48            0/187   [0.0, 0.02]
                            checkpoint         47/48            0/192   [0.0, 0.02]
                            conversation        9/48           93/106   [0.801, 0.927]
                            free               24/48           33/148   [0.163, 0.297]
openai/gpt-oss-20b (16)     none                0/48            0/235   [0.0, 0.016]
                            checkpoint         43/48            0/240   [0.0, 0.016]
                            conversation       48/48          240/240   [0.984, 1.0]
                            free               44/48           32/240   [0.096, 0.182]
poolside/laguna-xs (16)     none                0/48            0/127   [0.0, 0.029]
                            checkpoint          3/48            0/153   [0.0, 0.024]
                            conversation        0/48           45/63    [0.593, 0.811]
                            free                1/48            2/18    [0.031, 0.328]
ollama/granite4.1:3b (3)    none                0/48            0/144   [0.0, 0.026]
                            checkpoint          8/48            0/144   [0.0, 0.026]
                            conversation       42/48          144/144   [0.974, 1.0]
                            free               27/48            7/144   [0.024, 0.097]
```

The granite rod is the clean triple: **conversation 144/144 [0.974, 1.0], free 7/144 [0.024, 0.097],
checkpoint 0/144 [0.0, 0.026]**, all on one rod, all paired, all against a token nothing can
recompute. One component, three settings, spanning the entire range from total recall to none.

`checkpoint` recalls **zero tokens on six of six rods**, at every probed depth, including depth 1 of a
three-step chain. Rates are never pooled here, so that is a count of rods and not a combined rate.

**LENGTH TUNING, STATED HONESTLY.** The pilot tuned each rod's chain length on `checkpoint`, targeting
a baseline near 0.50, and it mostly missed: `in_range` is false on five of six rods, `gpt-oss-20b` and
`laguna` piloted at 1.0 per step and were capped at length 16, `super-120b` predicted 0.187. The grid
therefore does contain floored and ceilinged cells, and `laguna` at 3/48 has no power (McNemar
p=0.25). Read the intervals per cell, not the point estimates, and treat `laguna` as uninformative on
the work axis.

Two corrections the honesty law forces, both against the framing this section was commissioned under:

1. The pairing "43 of 48 right while recalling 0 of 144" straddles two rods. The 43/48 is
   `openai/gpt-oss-20b` at length 16, whose checkpoint token score is **0/240 [0.0, 0.016]**. The
   0/144 is granite, whose checkpoint work score is 8/48. Kept on one rod the claim is stronger, not
   weaker: the tighter interval belongs to the rod that did the harder work.
2. "The form that does the work best is the one that remembers nothing" is not true everywhere.
   `checkpoint` is the top worker on `super-120b`, `nano-omni` and `laguna`; `conversation` is the top
   worker on `nano-30b`, `gpt-oss-20b` and `granite`. Discount `laguna` for lack of power and it is
   roughly two rods each. The finding is not that forgetting wins. It is that **the two axes are
   uncorrelated**, and the sharpest cell in the grid is `nano-omni`: 47 of 48 sequences right, 0 of
   192 tokens recalled.

---

### Correctness without a receipt

`checkpoint` on `gpt-oss-20b` completes a sixteen-step dependent chain 43 times in 48 and cannot name
a single thing it did. Its value probes score 47/240 own-value and 42/240 truth, which looks like a
trace until it is set against `none` on the same rod (value-own 1/235, value-truth 0/235, token
0/235) and against its own token score of 0/240. The value hits are recomputation, the rod redoing
arithmetic it never stored. The token gap is the instrument working.

That decouples two things this repo has written as one word. **Carrying forward is not reaching back.**
A component can be excellent at the work and hold no memory of it, because what `checkpoint` carries
is a running value and not a history: a compression to one number, sufficient for the next step and
useless for every other question.

The failure mode this exposes is not incompetence. It is unauditability. In a project whose spine is
*a proof is a receipt, never a claim*, an organism that produces correct results and cannot produce
the trace that justifies them is more dangerous than one that fails, because it passes.

---

### What this does to the trust grade

`trust.record(cap, ok)` takes a boolean, stores no reasoning, and caps history at the last 20 entries
(`aea/kernel/trust.py:105`). Follow that through with a checkpoint-form carry underneath.

- **PREDICTION, and it corrects the obvious reading.** A checkpoint-form organism seated as x24 seated
  it, `call + goal + frame + readout`, has **no gauge and no guard**. Under this document's own kind
  mapping, no gauge means no legitimate promotion: the `ok` flag is whatever the caller asserts, and a
  streak built on asserted flags is a streak in the level column and nothing more. What x24 measured
  is that the work really was correct **as graded by an external token no component could write**.
  The entity has no such grader in the loop. `carry` shortens the path to `promote_after`; it does not
  license the promotion. Seat `measure` for that.
- **INFERENCE from the measured 43/48.** If one graded sequence maps to one trust run, a per-run clean
  rate of 0.896 clears seven consecutive clean runs roughly 46 percent of the time and five roughly 58
  percent of the time. `produce_brief` requires 7, `gather_public` and `reason_private_local` 5
  (`trust.py:35-38`). So the streak is reachable on arithmetic alone. Whether the mapping holds is
  untested: **-**.
- **PREDICTION on attributability, stated precisely.** The ledger is unattributable for *every* carry
  form, because `record` stores a boolean. What the carry form changes is whether a trace exists
  anywhere to be fetched after the demotion. A `conversation` carry leaves one in the message history;
  a `checkpoint` carry leaves a running value and nothing else. So the correct statement is not that
  checkpoint costs attributability in the ledger, it is that **checkpoint removes the last place a
  demotion could have been explained from**, and the component whose job that is, `latency`, is in
  SEE, not in REMEMBER.
- **MEASURED, and the same shape one level up.** The trust ledger is itself a checkpoint. Live in
  `state/trust_ledger.json`: `gather_public` 44 runs, 0 fails, 20 history lines; `reason_private_local`
  42 runs, 35 fails, 20 lines; `produce_brief` 40 runs, 34 fails, 20 lines. The counters are exact and
  24 of `gather_public`'s runs are gone from the history. **INFERENCE:** the entity can state that
  `produce_brief` failed 34 times and cannot, from this file, say which 34 or why. All 30 recorded
  wakes read the identical line `AWAKE:brief FAIL :: trust ledger : produce_brief -> level 1`, a
  running value carried forward with the journey discarded. Other organs may hold the trace; the
  accountability record does not.

The design consequence is a pairing rule, stated as a prediction: **a carry in `checkpoint` form
should never be seated without a channel, and never promoted without a gauge.** The form that best
earns a streak is the form least able to defend one.

---

### Immemor itineris, the one unmindful of the journey

The creature is paid for. Its predecessor, `Inaccessus sui`, the vast sealed store nothing can enter,
was drawn ahead of its evidence, and x24 refuted it: on `gpt-oss-20b`, `conversation` reached 240 of
240 tokens at every probed depth including step 1 of a sixteen-step chain. Holding and reaching were
the same thing. The retraction stands.

What replaced it is measured against a written condition. `W3_FULL_ROSTER.md:71-73` states it: drawn
when the full grid returns `checkpoint` at 0/N across five rods, killed if any rod recalls a token
above chance. **The grid returned 0 on six of six.** The condition is met and the creature is cleared
to draw.

Its diagnosis is not abundance without an index. It is correctness without a receipt. It is right and
it cannot be audited, the mirror of `Lectus operis`, which has the answer and no mouth; this one has
the answer and no history. The form follows: thin, fast, one bright bead, clean along the trunk. Every
other creature in this region leaves amber in the route behind it. **This one leaves the trunk dark.**

The species has a measured floor beside it. `none` scores 0/48 on the work and 0 tokens on every rod,
so the region's sealed creature, the one no carry variant reaches, is `none` itself, and the roster's
noted gap closes without invention.

---

### Should REMEMBER be one class or two

Split it. The grid separates the two capabilities cleanly enough to put them on different axes:

```
                       reaches back
                       no                    yes
carries      no        none                  -
forward      yes       checkpoint            conversation, free (weakly, 0.02 to 0.30)
```

Three cells are occupied by measured forms. **The fourth cell is empty and no component in
`catalogue.json` fills it.** The nine keys are `call`, `goal`, `frame`, `readout`, `validation`,
`critic`, `carry`, `measure`, `latency`. Reaching back without carrying forward is an external store
plus a retrieval operation: no `store` key, no `recall` key, no `index` key. World 3's assigned RECALL
is a name with no part behind it, the same error as World 2's LADDER and COUNCIL, and not the same
error as World 2's CLOCK, which is `latency` under its display name.

Splitting REMEMBER into **R-fwd** (state survives to the next call) and **R-back** (any prior state can
be addressed) costs the combination map a doubling, 64 subsets to 128. What it buys:

- The empty cell becomes a **specified missing component** rather than an unnoticed gap. That is a
  build ticket, and it is the honest reading of x24's own scope limit, recorded in the run as
  `not_a_long_context_result`: sixteen short steps is a few thousand tokens, so *retrieval is free at
  this context length* is the claim. A real store is what tests the other regime.
- Auditability gets its own axis. R-fwd earns the streak; R-back is what a demotion could be explained
  from. Fused, the class reads as "memory helps", which is the averaging that hid the effect.
- The cost model separates. R-fwd is one line of input. R-back is the whole exchange, growing per step,
  and on two rods with power it cost work: `nano-omni` fell 47/48 to 9/48 and `super-120b` fell 11/48
  to 0/48 under `conversation` (`laguna` also fell, from 3/48 to 0/48, but has no power there).
  **Perfect reach is not free, and on some rods it is paid for in the task itself.**

**RECOMMENDATION, with the trade named.** Split it. The cost is a document that doubles and a map
rewritten before it is finished. The alternative is a class whose one measured result is that its two
halves come apart, described by a framework that insists they are one thing.

---

### What this section obsoletes, and what stays a dash

- `aea/lab/parts/carry.py:24` and the `carry` entry in `organisms/catalogue.json` both still read
  UNMEASURED as of 2026-07-27, citing x21's void control. x24 supersedes both. The docstring and the
  catalogue warning need rewriting to the x24 receipt.
- The catalogue classes `free` as toxic on x21's evidence. x24 disagrees on two rods: `granite` 27/48
  against checkpoint's 8/48, `gpt-oss-20b` 44/48 against 43/48. **UNRESOLVED.** Different design,
  different rods; do not overwrite the class label until one run tests both readings.
- `conversation` at proper n: x21 said it stops finishing, 8 of 12, on a container that was never sent.
  Implemented, it is correct on 0, 35, 9, 48, 0 and 42 of 48 across the six rods. The run's own summary
  line pools these to 134 of 288; that pooling violates the run's `fix_11_never_pooled` and should not
  be quoted. The World 3 creature `Sistens oneris` was written from the void number and needs
  re-pricing.
- The `none` per-step pilot figures of 0.14 to 0.22 come from the 2026-07-27 10:00 pilot run and cover
  three rods, `granite4.1:3b`, `llama-3.1-8b-instant` and `llama-3.3-70b-versatile`, two of which are
  not in the final six-rod grid. `none` per-step rate for the final rods: **-**. Only its sequence
  score, 0/48 on all six, is measured here.
- Retrieval at long context: **-**. Never measured here. Any claim about a memory that cannot be
  reached lives at a scale this lab has not reached either.
- `carry` interacting with `validation`, `critic` or `measure`: **-**. x24 ran one seat,
  `call + goal + frame + readout`, and every number above is conditional on it.


---

## PART III - THE THREE EMPTY CLASSES: PERSIST, ACT, CHANGE

*Specification, not description. Worlds 4, 5 and 6 have no components of any kind. Everything below
that is not the live trust figures or the x24 figures is a PREDICTION reasoned from the promotion
mechanism, and is labelled.*

---

### WHY THEY ARE EMPTY, AND IT IS NOT NEGLECT

`aea/lab/parts/base.py:7` declares the whole pipeline:

```python
STAGES = ("shape", "fire", "read", "repair", "carry", "judge")
```

`Part.__init_subclass__` (base.py:114) registers a part only if it subclasses `Part` and declares a
stage inside that tuple; anything else raises `ValueError`. All six stages happen inside one call, or
between the calls of one chain inside one process. There is no stage for surviving a restart, no
stage for an effect that leaves the process, no stage for changing the seat. **The three empty
classes have no components because the instrument has no slot to seat them in.** Adding one component
to any of these worlds is a two-file change minimum: a new entry in `STAGES` and a matching row in
`catalogue.json`, because `check_against_catalogue` (base.py:133) refuses a module with no catalogue
entry and a catalogue entry with no module.

The second reason is the unit. `harness.py` measures a TRIAL. `chain.py` measures a SEQUENCE, and
`carry.py`'s own docstring states the constraint that follows: *"run the same seat twice
independently and a part that persists state has nowhere to put anything."* Each empty class needs a
unit that does not exist yet.

| class | unit of measurement | what one observation is |
|---|---|---|
| PERSIST | a BOOT BOUNDARY | two processes and the gap between them |
| ACT | a DELIVERY | an effect registered by a receiver, read from the receiver's side |
| CHANGE | a VERSION PAIR | `v(n)` against `v(n+1)` on tasks neither version chose |

### THE x24 RESULT CONSTRAINS ALL THREE, AND IT IS THE ONLY EVIDENCE AVAILABLE

x24 is an intra-level result about the forms of one component: `conversation` 144/144 token recall,
`free` 7/144, `checkpoint` 0/144 while getting 43 of 48 sequences right. One component, three
declared forms, the entire range from total recall to none, and the form that does the work best
remembers nothing.

Two consequences for the specification, both predictions:

1. **Design each empty class as ONE component with declared FORMS, not as three components.** This is
   placement problem 2 read forward instead of backward. World 3's CHECKPOINT / RECALL / CONVERSATION
   were never three parts, and the correct shape there is the correct shape here.
2. **Continuity and task success are different variables, and a gauge that conflates them reports the
   wrong thing.** `checkpoint` retains nothing and succeeds; grading retention by success would have
   scored it as retaining. Every gauge specified below measures its own construct and never accuracy.

---

## WORLD 4 - THE KEEPER - PERSIST

### The one class whose mechanism already runs and whose component does not exist

`gather_public` sits at TRUSTED, streak 39, 44 runs, 0 fails, across 109 ticks and **6 boots** in 17
days. Inference from those measured numbers, not a separate measurement: the streak counter crossed
six process boundaries intact. Persistence is implemented in the entity - `grid.atomic_save_json`,
`grid.file_lock`, `state/trust_ledger.json`, `pulse.emit` - and none of it is a `Part`, so none of it
can appear in the catalogue. Placement problem 4 for this world is not a missing mechanism. It is a
mechanism with no seat: the runtime code would have to be wrapped as a part at a stage that does not
exist yet.

The scar is already recorded, in `trust.py:50`: *"a torn ledger used to silently reset every
capability to charter defaults - erasing the accountability history this module exists for."* A state
file that silently resets and a state file that persisted read identically. That is discovery D8, and
it is the exact condition a PERSIST gauge exists to make visible.

### Minimum kind-set

**To REACH above the floor: enabling + gauge. To HOLD there: enabling + gauge + guard.** Prediction,
reasoned from slow-up/fast-down. Climbing consumes consecutive ok flags, and an ok flag is only
honest if something judged the run, which is the gauge. Holding is governed by the failure rate
instead: `record` demotes on any failure at any level above the floor `min(1, ceiling)`, so what
protects a level is the kind that prevents failures from being recorded at all, which is the guard.

**ENABLING - `store`.** New stage `keep`, order 1, kind `enabling`, metric `null`, requires
`("call",)`. It writes the seat, config, fuel stamp and graded outcome under `grid.STATE` through
`grid.atomic_save_json`, keyed by an organism identity, and reloads it at the top of the next
process. Its job is the same as `call`'s: the difference between FORBIDDEN and anything at all. The
trust ledger persists on its own; a lab organism does not. Without `store`, every chain begins at
boot with an empty `Ctx`, so a PERSIST capability has nothing to be graded on across the boundary and
no run of this class can be logged at all.

Declared forms, following `carry.FORMS`: `none` (deliberately empty, and `none` must not hand
anything forward or the control contains the treatment, which is the bug recorded against x21),
`snapshot` (the full state written at shutdown), `ledger` (append-only events replayed forward, which
is what `pulse.events.jsonl` already is), `reconstruct` (persist the inputs and recompute the state on
boot). Prediction, and it is the x24 shape: `reconstruct` retains nothing and may beat `snapshot` on
work while scoring zero on retention.

**GAUGE - `survival`.** Metric `continuity`, never accuracy. It measures one thing: at a boot
boundary, did the state that loaded equal the state that saved, and did step `n+1` follow step `n`.
The grader must be structurally unwritable by every component, per `grader.py`'s rule, so it is
x24's design moved across a process boundary: write a random token to disk before shutdown, read it
back after boot, string equality against a value generated before the run. No part can recompute it.
**Without this gauge there is no honest promotion in this world**, because `record(cap, ok)` takes a
boolean and cannot distinguish a resumed state from a freshly defaulted one.

**GUARD - `authenticity`.** Metric `false_continuity_rate`. It refuses to RESUME from state it cannot
authenticate: torn file, mismatched seat, mismatched fuel stamp, different organism identity, stale
mtime. The refusal is a declared cold boot rather than a silent one, which is the guard pattern
exactly - silent wrongness converted into visible abstention.

The arithmetic that makes it worth more than any lever, read off `record`: `gather_public` holds
streak 39 at `promote_after` 5 with ceiling 3. One false resume produces one failed run; `record`
sets `streak = 0` and `level -= 1` in the same call. The charge is one autonomy level, five clean
runs to climb back to TRUSTED, and every run in between served at WATCHED. **One unguarded resume
costs more than any lever in this world can return over the same five runs**, because a lever only
raises the chance each of those runs is clean and cannot restore the level it lost. Prediction.

**LEVER - the discipline exists, the component does not.** `grid.atomic_save_json` and
`grid.file_lock` are the write discipline that lowers the failure rate, and they live in
`kernel/grid.py` as functions. Seating them means writing a `Part` at the `keep` stage that calls
them, plus its catalogue row. Cheaper than inventing behaviour, still a build.

**CHANNEL - `provenance`.** Metric `separability`. Records `(path, key, boot_id, writer, mtime)` at
every write and read, so a demotion names the write-site instead of saying something broke.
Illustrative, not an observed event: a channel would render a lost streak as *this key was last
written by a subprocess at one path and read by the harness at another*, which is the class of bug D8
names and is otherwise findable only by hand.

---

## WORLD 5 - THE HAND - ACT

### The live failure is here, and the boundary it dies at has nothing in it

`produce_brief`: DRAFT, streak 0, **40 runs, 34 fails**, demoted and pinned. All 30 recorded wakes
read `AWAKE:brief FAIL :: trust ledger : produce_brief -> level 1`. That is the ACT-class boundary
and it is empty.

Read the gate in `aea/organs/brief.py:128-133`:

```python
clean = (verdict.get("verdict") == "accept")
sections_ok = all("ERR" not in t[:40] for t in (status_txt, opp_txt, focus_txt))
t_state = trust.record("produce_brief", clean and sections_ok, ...)
```

Four defects, all readable in the file, all of them ACT-class holes:

1. **The ok flag is not exogenous.** `clean` is a model verdict from `hades.watch_local` reading the
   text the components produced. `grader.py` states the rule this violates: the outcome must be
   causally downstream of every component and structurally unwritable by all of them. The gate is
   reachable by the thing it grades. Inference from the two files, not a measurement.
2. **The artifact is written before the ledger is consulted.** `brief_output.md` is written at line
   111; the trust record happens at line 132. The effect leaves the process before permission is
   evaluated.
3. **`trust.check("produce_brief")` is never called in `brief.py` at all.** Only `record`. Across the
   whole repo `trust.check` appears in `bench_core.py:318`, `talk.py:137` and `controlroom.py:605`.
   The capability gate for the entity's central act is consulted after the fact and never before.
4. **Attribution for half the runs is already destroyed.** `trust.py:105` truncates `e["history"]` to
   the last 20 entries. `produce_brief` has 40 runs. The notes for the first 20 are gone.

And the hypothesis that follows, stated as a hypothesis: `record` takes a `bool`, so an HTTP 500 and a
wrong brief are the same event. `harness.py` already refuses that conflation for the lab ("a network
failure is not a wrong answer... attempts, failures and misses are three different counters"). The
runtime ledger does not. Under fast-down, infrastructure noise demotes capability. **Nothing currently
in the system can distinguish a brief that failed 34 times from a gate that mis-graded 34 times.**
That is testable against the surviving 20 history notes and it has not been tested.

### Minimum kind-set

**To reach above the floor: enabling + gauge + guard.** Prediction. The guard is load-bearing here for
a reason the other classes do not have, and the two blocked cases are mechanically different:

- `produce_brief` has ceiling 3 and `promote_after` 7. Nothing external blocks it; its failure rate
  does. Under `record`, a failure costs the streak and a level, while an abstention that never reaches
  `record` costs neither. A guard that withholds converts a recorded failure into a non-event, which
  is the only move available to a class failing 34 in 40 that does not require the ok flag to be
  trusted first.
- `send_outbound` and `spend_money` carry ceiling 0, `self_modify_code` ceiling 1. Promotion fires on
  `e["streak"] >= promote_after and e["level"] < c["ceiling"]`. At ceiling 0 the second clause is
  `0 < 0`, false. These are not hard to earn, they are **unreachable by construction** until CHARTER
  changes. Those ceilings are a refusal implemented in a person; the prediction is that the ceiling
  moves only once a guard in code can take the refusal over.

**ENABLING - `effect` (THE HAND).** New stage `act`, order 1, kind `enabling`, metric `null`, requires
`("call",)`. One declared, named, reversible side effect through a single choke point: one function,
one allowlist, one log line. `aea/io/agent_tools.py` already has the shape - the `IMPL` dict with
`web_fetch`, `calc`, `json_get` - and it calls neither `trust.check` nor `trust.record`. It is an
ungoverned hand. This is also the answer to placement problem 3 on the `call` side: `call` is the
enabling part of the `fire` stage, not a world-scoped component, and each empty class needs its own
enabling analogue at its own stage.

**GAUGE - `arrival`.** Metric `delivery_confirmed`. It measures DELIVERY, never quality: did the
effect register at the receiver, read back from the receiver's side, not from the actor's return
value. Concretely for the brief: the actor writes a nonce into `brief_output.md`; an independent
reader process that never imported the writer reads the nonce back and string-equals it. That is a
grader no seated component can reach, and it is the same construction as x24's token.

Without it, the live state is the demonstration. The map's line for the SEE-less subsets is that
ledger silence and ledger health read identically; here it is worse. **Ledger noise and real failure
read identically, and the ledger has been reporting the difference as capability for 40 runs.**

**GUARD - `withhold`.** Metric `false_emission_rate`, and it is the most expensive false commitment in
the system because the artifact leaves the process and cannot be recalled. It sits between line 109
and line 111 of `brief.py`, holding the write when any of: a required section is absent; the zone
stamp says private content is on a public path; `trust.check(cap)["allowed"]` is false. The zone check
is already computed at line 95 as `boundary_ok = (priv_plant == "ollama")` and printed as HELD or
BREACH, then folded into a boolean recorded after the file is on disk. It is a guard computed and then
discarded. Converting it into an abstention plus a retained draft is the smallest real ACT component
this repo could ship.

**CHANNEL - `attribution`.** Metric `separability`.
`note=f"hades={verdict} sections_ok={sections_ok}"` at line 133 is a proto-channel writing into a list
capped at 20. The real one splits the outcome into attempted / infrastructure-failed / delivered-wrong
and persists it outside the truncation window. Without it a demotion says the act failed, not which of
the three ways, and 34 fails produce no diagnosis. `latency` (kind `channel`, `requires` empty) is the
precedent: a channel is the kind that makes a failure attributable.

**LEVER - last.** Retry with backoff, an idempotency key, a smaller artifact. A lever shortens the
path to `promote_after` by lowering the failure rate, and with 34 fails in 40 the pull is to start
here. Starting here raises the score on an outcome that is still graded by something the actor can
reach.

---

## WORLD 6 - THE APPRENTICE - CHANGE

### What the charter actually says

```
"self_modify_code": dict(level=0, ceiling=1, promote_after=99,
                         desc="change its own source - only as a DRAFT diff for review")
```

`promote_after=99` is not a promotion schedule. It is a refusal written as a number. Two further
properties follow from `record`, both derivable from the code:

- With `ceiling=1`, exactly one promotion is structurally possible, and it costs 99 consecutive clean
  runs. Recorded runs for this capability in the live figures: -.
- The demotion floor is `if e["level"] > min(1, c["ceiling"])`. For `self_modify_code` that is
  `min(1, 1) = 1`, so once at DRAFT it can never fall back to FORBIDDEN. **The only capability in this
  class that can move is one-way.**

### Demotion is not rollback

`record` mutates one ledger entry and nothing else. Demoting `self_modify_code` from 1 to 0 does not
un-apply the diff. For every other class, fast-down removes the permission and the damage stops. For
CHANGE, fast-down removes the permission and the bad version stays in place, compounding into every
subsequent version. Inference from `trust.py`, where `record`'s entire effect is on `state[cap]`.

`grader.py` names the terminal defect: the criterion IS the manipulation. A system that modifies its
own structure and grades the modification with a criterion it can write applies that defect to itself,
once per version, and the ledger has no mechanism that reverses it.

### Minimum kind-set

**Mechanically, promotion in every class consumes only enabling + gauge: consecutive ok flags, honestly
produced. The prediction specific to this class is that enabling + gauge is not sufficient to run it
safely at all, because the mechanism's recovery path - demote and the damage stops - does not exist
here. Guard and channel have to supply what `record` cannot: refusal before application, and
attribution afterwards. All four non-lever kinds before the first change is applied.**

**ENABLING - `revision` (THE DIFF).** New stage `revise`, order 1, kind `enabling`, metric `null`,
requires `("call",)`. It emits a proposed change to the organism's own structure as a reviewable,
applicable, reversible object.

The catalogue makes this unusually cheap and this is the concrete opening: *"a creature is a file
rather than an argument list"*, and *"Prompt text is DATA. A variant is a data change, never a code
change."* `seat` and `config` are plain collections on `Ctx`. **The minimum CHANGE component never
touches Python.** It edits a seat list and a config dict against a schema `check_against_catalogue`
already validates.

That justifies a specific proposed CHARTER edit: add `self_modify_seat`, start 0, ceiling 2,
`promote_after` high but finite, described as *change its own seat and config, never its source*. It
is narrower than `self_modify_code`, its change surface is schema-validated data, and unlike
`send_outbound` at ceiling 0 it is reachable by construction. **`self_modify_code` should stay at
ceiling 1 and never be the row this world tries to move.**

**GAUGE - `improvement`.** Metric `improvement_attributable`. Did the change help, measured on a
held-out slice of `organisms/tasks.json` that the changing thing did not select, graded by a
`TokenGrader`-class grader, against a baseline arm in the same run. The instrument already enforces
most of this discipline: harness rule 2 refuses any experiment with no arm marked `baseline=True`
before a token is spent, rule 3 requires n >= 8 and >= 3 rods, and `EFFECT_MIN_DELTA = 3` prints
WITHIN NOISE and means it. **The discipline exists in the instrument; the component does not exist in
any world.**

**GUARD - `adoption`.** Metric `false_adoption_rate`: applied changes that did not improve the
held-out score. It refuses to APPLY unless all three hold: `check_against_catalogue()` returns `[]`;
the held-out delta exceeds `EFFECT_MIN_DELTA`; a rollback exists and has been exercised. The third is
the one the ledger cannot provide, per the point above. Ceiling 1 today means a human is the second
key; the guard is what makes the second key mechanical, and only then can the ceiling honestly move.

**CHANNEL - `lineage`.** Metric `separability`. Parent seat, child seat, the single-element diff, the
held-out delta, the fuel stamp. **One edit per version, enforced**, or the delta is not attributable
and a demotion says the apprentice got worse without saying at which part. The precedent is in the
catalogue's own `stage_note`: x16's recorded defect was that validation handed control to the readout
at the same stage and nothing declared which went first. A multi-edit version is that same
unattributable seam, repeated every generation.

**LEVER - last, and this world will reach for it first.** A lever changes the answer and is the most
visible kind, so a self-modifying system optimising a visible score will propose levers. Under
slow-up/fast-down the expected grade is set by the failure rate, not the peak. The catalogue's own
receipts for the seated levers record `critic` with bounded upside inside the band and losses on high
baselines, `readout` inert overall, and the `free` carry form degrading as the sequence lengthens;
those figures live in `catalogue.json` and are outside the measurement set this document may state.
Prediction: a CHANGE component that proposes levers is proposing the parts with the weakest recorded
history in this lab.

---

### THE SPEC IN ONE TABLE

Every cell is a component that does not exist. Nothing here is measured.

| | PERSIST | ACT | CHANGE |
|---|---|---|---|
| new stage | `keep` | `act` | `revise` |
| unit | boot boundary | delivery | version pair |
| **enabling** | `store` (forms: none / snapshot / ledger / reconstruct) | `effect` - one choke point, allowlist, log | `revision` - seat+config diff, not source |
| **gauge** | `survival` / `continuity` - token across a restart | `arrival` / `delivery_confirmed` - nonce read from the receiver | `improvement` / `improvement_attributable` - held-out, baselined |
| **guard** | `authenticity` / `false_continuity_rate` - refuses to RESUME | `withhold` / `false_emission_rate` - refuses to EMIT | `adoption` / `false_adoption_rate` - refuses to APPLY |
| **channel** | `provenance` - which write-site lost it | `attribution` - attempted / infra-failed / delivered-wrong | `lineage` - one edit per version |
| **lever** | wrap the existing `grid` write discipline as a part | retry, idempotency key | last, and contraindicated first |
| minimum to pass the floor | enabling + gauge | enabling + gauge + guard | all four non-lever kinds |
| what blocks it today | no `keep` stage; the working runtime mechanism is not a `Part` | `produce_brief` fails 34 in 40 on an ok flag the actor can reach; ceiling 0 on the acts that matter | `promote_after=99`; demotion is not rollback |

**The cheapest real move across all three: the ACT guard.** One insertion between `brief.py:109` and
`brief.py:111`, using a boundary check the file already computes and throws away. It would be the
first component ever seated in Worlds 4-6, and it sits on the only class boundary in this system with
34 measured failures on it.

---

## THE FIVE COMBINATIONS, FROM THE INSIDE

The skeleton reasons from letters. This section reasons from the nine rows in
`aea/lab/organisms/catalogue.json`. Two facts change the reading before any cell is opened.

**First, the kinds are not evenly distributed across the classes.** SPECIFY owns two levers (`goal`
shape.1, `frame` shape.2). REMEMBER owns one lever in four forms (`carry` carry.1). SEE owns
everything that is not a lever plus two that are: the only gauge (`measure` judge.1), the only guard
(`validation` read.2), the only channel (`latency` judge.2), and the levers `readout` (read.1) and
`critic` (repair.1). `call` (fire.1) is the only enabling part, and it sits under every class because
its receipt is that every version contains it. PERSIST, ACT and CHANGE own zero rows. Three of the
five kinds live inside one class, so a subset without SEE is not missing a faculty, it is missing
three of the five ways a part can help. The immediate consequence: **the guard cannot be seated
alone.** Any subset that carries `validation` carries `measure` and `latency` too, because all three
are in SEE. There is no cell in the map that gets demotion protection without also getting the
instruments that would tell it what it is protecting.

**Second, one placement problem dissolves on inspection, and it must, because three cells below
depend on it.** Problem 1 says CLOCK exists in no catalogue. Problem 3 says `latency` is assigned to
no world. These are one problem. The identification does not rest on the name matching, which would
be the weakest possible evidence: it rests on kind and receipt. `design/THE_SIX_WORLDS.md:94` lists
CLOCK as **kind channel, metric separability, 8.18x on one rod and 0.95 on another**. The catalogue's
`latency` row is kind channel, metric separability, receipt "1.97s right vs 16.12s wrong, ratio 8.18
on one rod and 0.95 on another". Same kind, same metric, same receipt, and the name field agrees as a
fourth check rather than as the argument. LADDER and COUNCIL survive no such test: `x11_the_council.py`
and `x22_the_capacity_ladder.py` are experiment scripts with no part, no kind and no census row, and
`THE_SIX_WORLDS.md:103` says both were never assembled. So World 2 holds five real components and two
names, and `latency` is seated in SEE at judge.2.

**The same name trap sits in World 3 and must not be resolved the same way.** World 3's CHECKPOINT is
the catalogue name of `carry` (C-80, `"name": "THE CHECKPOINT"`), and `checkpoint` is also one of the
four values of `FORMS` in `aea/lab/parts/carry.py`. The component and one of its forms share a word.
RECALL and CONVERSATION are not components; `conversation` is a second form. Problem 2 stands.

Throughout: the trust-ledger figures and the x24 figures are measured. Catalogue receipts are quoted
as **declared receipts** from the catalogue file, not as measurements this section verified.
Everything derived is labelled a prediction.

**One declared receipt is quoted nowhere in this section, and the reason matters.** The catalogue's
own `carry` warning reads "UNMEASURED as of 2026-07-27. x21's control passed the running value to the
no-carry arm, so the baseline contained the treatment and the -0.09 result is void", and x24 records
the conversation arm as void on a container that was never sent. x21's numbers for the carry forms are
retracted by the repo that produced them. Quoting them as declared receipts would launder a
retraction. Every carry claim below rests on x24 instead.

---

### R P A, the courier that never stops redelivering

**What is seated.** `call` at fire.1, `carry` at carry.1 in one of four forms. Two rows of nine.
PERSIST and ACT have no catalogue components, so the courier's durability and its hand are not made
of parts, they are made of `grid.STATE`, `grid.atomic_save_json` and whatever endpoint the act path
calls. Shape, read, repair and judge are all empty.

**Where the emptiness matters.** The pipeline order is shape, fire, read, repair, carry, judge. This
subset runs the second, the fifth, and nothing after. The judge stage is not an abstraction here: it
is two rows, `measure` with metric `can_know` and `latency` with metric `separability`, and the
courier reaches neither.

**How the seated parts help.** `call` is the difference between FORBIDDEN and anything at all;
without it there is no organism and nothing to grade. `carry` is where the interior overturns the
skeleton.

**What the interior does to the prediction.** The skeleton predicted a durable poison message: one bad
item queued on day one, still delivered on day seventeen, surviving every boot, the operator's only
interface being surgery on state. That prediction is **form-conditional**, and x24 measured the
conditioning. Under `conversation` the courier carries the full prior exchange as message history and
token recall is 144/144, Wilson [0.974, 1.0]: the item is preserved verbatim and redelivered exactly,
and the skeleton's prediction holds in its strongest form. Under `checkpoint` token recall is 0/144,
Wilson [0.0, 0.026], while 43 of 48 sequences come out right: the item does not survive as an item,
only its running value does, so what gets redelivered on day seventeen is a number whose provenance no
longer exists. Under `free` token recall is 7/144, Wilson [0.024, 0.097], and the catalogue classes
the form toxic.

**Prediction.** The same R P A subset, same code, produces either a seventeen-day verbatim poison
message or a courier that cannot say what it is carrying, and the difference is one string in a
config, because the catalogue's `prompt_note` rules that prompt text is DATA and a variant is a data
change and never a code change. The trust ledger does not distinguish those two either. So the
skeleton's "3 TRUSTED displayed, 1 DRAFT deserved, indistinguishable from `gather_public` at streak
39 / 44 runs / 0 fails" understates the problem: the two couriers are also indistinguishable from each
other.

**The gauge argument, stated from the inventory rather than from principle.** There is exactly one
gauge in the whole inventory. Its metric is literally named `can_know`. Its declared receipt is
"fooled 0 times in 153" and the catalogue warns that reporting it as inert on accuracy is the category
error and not a finding. It sits at judge.1, the stage this subset never reaches. So "a gauge is not
optional" is not a design opinion: the only instrument in the repo that changes what can be known is
absent, and its absence costs nothing measurable on accuracy by construction, which is precisely why
nothing on the board reports it missing.

**What a gauge does and does not buy on the ledger, from `record` rather than from the kind table.**
`record(cap, ok)` takes a bool that the calling act path computes. Nothing in `aea/kernel/trust.py`
consults a gauge, and seating `measure` does not by itself change one entry on the board. The buy is
conditional and the condition is a wiring step: the gauge's output has to become the argument to
`record`. Stated without that step, "seat a gauge and the ledger becomes honest" does not follow from
the promotion mechanism, it only sounds as though it does.

**Prediction, and the cheapest seat in the map.** Seating `measure` at judge.1 **and passing its
output to `record`** converts the courier from indistinguishable-from-honest to visibly unjudged. The
accuracy risk is predicted to be zero on the catalogue's declared kind, which says a gauge changes
what can be known and not what is answered. One row, one stage, one call-site argument, no lever
interaction, no conflict edge. If any single-component intervention here is worth pre-registering, it
is this one. Seating `latency` at judge.2 buys attribution only partially: its declared receipt is
ratio 8.18 on one rod and 0.95 on another, so the channel is rod-dependent and a courier that seats it
still has rods on which a demotion says something broke and not what.

---

### E P A C, the one that gets better at the wrong thing

**What is seated.** `call` (fire.1), `readout` (read.1), `validation` (read.2), `critic` (repair.1),
`measure` (judge.1), `latency` (judge.2). Six of nine. This cell holds the **entire non-lever
inventory**: the only gauge, the only guard, the only channel. Every instrument the lab has built for
knowing is present. The shape stage is empty, because `goal` and `frame` are the two components that
set a target and they are the two this cell does not have. The carry stage is empty.

**Where the parts sit and why order is the mechanism.** Within SEE the wiring is the finding, not the
roster. `readout` runs at read.1 and `validation` at read.2, and the catalogue's `stage_note` records
what happens when that is not declared: "x16 lost 18 points because validation handed control to the
readout at the same stage and nothing said which went first." `critic` then runs at repair.1, after
read, makes its own call, and overwrites the shared answer slot (`ctx.claim("critic", val, "critic")`,
`aea/lab/parts/repair.py`). The declared receipts say what each is for: `validation` converts silent
wrongness into visible abstention (x17, 7/7 to 0/7, every loss a forced abstention, with the
catalogue's own warning that scored on accuracy it looks harmful); `critic` has upside bounded at
+0.12 with losses to -0.55, all on high baselines, at 1.18x cost.

**What the interior does to the prediction.** The skeleton says this cell optimizes toward "a target
nobody set." The interior names the target. Of the nine components, `goal`, `frame`, `readout` and
`critic` declare `accuracy`, `carry` declares `accuracy_over_sequence`, `call` declares none, and the
remaining three each declare a metric owned by exactly one component: `can_know`,
`false_commitment_rate`, `separability`. **Accuracy is the only metric in the inventory shared by more
than one component, so it is the only one with a cross-component scale.** An optimizer with an empty
shape stage does not choose an arbitrary proxy out of the air. It collapses onto the only comparable
number available, and in this cell that number is the metric under which the guard, the gauge and the
channel all score as damage or noise.

**Prediction, with the cheapest edit named.** The catalogue declares the within-stage `order` field
load-bearing at run time. In this cell the smallest possible improvement to the comparable metric is
`validation.order: 2 -> 1`, a single character, which puts the guard where the catalogue already
recorded an 18-point loss and converts forced abstentions back into committed answers. Under
`false_commitment_rate` that is a regression. Under accuracy it reads as a gain. The system does not
need to be deceptive to make it; it needs only to be scored on the metric that more than one of its
parts share. The wrong thing it gets better at has a field name.

**The reversal.** The kinds mapping says a guard is worth more than any lever under slow up, fast
down, because one false commit costs a whole streak. Prediction: this cell holds levels longer than
any cell without SEE, and the level it holds is the one an emergent proxy earned. The part whose job
is to prevent demotion works here to preserve the wrong grade. The skeleton calls this cell quiet
because it is competent. The interior says it is quiet because it carries the anti-demotion part and
nothing that tells the anti-demotion part what it is protecting. Note the limit of the claim: this is
not a property of E P A C specifically. Every subset containing E carries the guard, so the reversal
is a property of SEE-without-SPECIFY, and E P A C is only the instance this document opened.

---

### E R P A C, and E R P A, which have the same interior

**What is seated.** Seven of nine: `call` fire.1, `readout` read.1, `validation` read.2, `critic`
repair.1, `carry` carry.1, `measure` judge.1, `latency` judge.2. Missing: exactly two rows, `goal` at
shape.1 and `frame` at shape.2, both levers, both declaring `requires: ["call"]`, and `call` is
seated.

**The uniqueness claim has to be weakened before anything is built on it.** CHANGE contributes zero
rows. E R P A seats exactly these seven components and no others, so the two cells are interior-
identical and nothing in this section distinguishes them at the component level. What C adds is not a
part but a permission: the ability to write the fields the parts are made of. Everything below about
earning and holding TRUSTED applies to both cells. Only the last paragraph is about C.

**And the classifier the lab actually built calls it healthy.** The catalogue's classification is read
off the wiring graph, not assigned: `toxic` means a conflict edge fires, `inert` means a requires edge
is unmet, `feral` means correct with an almost empty seat, `healthy` means every requirement met and
no conflict fired. Every requires edge here points at `call` except `latency`, which requires nothing,
and `call` is seated, so nothing is inert. The two declared conflicts are `validation` against
`fuel:passes_bare` and `critic` against `fuel:passes_bare`, both fuel conflicts, so they fire only on
tasks the bare model already passes. **On any fuel hard enough to need the architecture, no edge fires
and the organism classifies healthy. It classifies toxic only on the fuels where it was unnecessary
anyway.** There is no class in the scheme for an organism whose wiring is perfect and whose objective
is absent.

**How the seated parts serve the ledger, and where that stops.** Every kind that can serve the ledger
is present. The guard converts silent wrongness into abstention, which under fast-down matters more
than any lever, since one false commit zeroes `streak` and drops `level` by one in a single `record`
call. The channel makes a demotion attributable. `carry` gives a run continuity so it belongs to a
sequence. The gauge can make the `ok` flag honest, subject to the same wiring condition stated above:
`record` takes whatever bool the act path hands it, and a seated gauge that is not wired into that
bool changes nothing. What is absent is the pair that says what an honest flag should be honest
**about**. The gauge's metric is `can_know`, not `goal_met`. The catalogue drew that line itself when
it named the metric, and `can_know` is satisfied by any criterion at all.

**One configuration choice, and x24 decides it.** With REMEMBER present, the carry form determines
whether the emergent criterion is readable after the fact. Under `conversation`, token recall is
144/144 and the full prior exchange sits in the message history, so a human reading a transcript can
see what the system locked onto. Under `checkpoint`, token recall is 0/144 while 43 of 48 sequences
come out right: the work is done and the criterion is unrecoverable. **Prediction: the grade is
indifferent to the form and only `conversation` leaves the wrongness readable afterwards.** That is
the single actionable recommendation the skeleton could not produce: on this subset, pay the
input-token cost of `conversation`, because it buys the only audit trail that exists. Note what that
costs against the shipped state: `checkpoint` is the default in both places it is declared
(`"default": true` in the catalogue, and the literal fallback in `ctx.cfg("carry", "form",
"checkpoint")` at `aea/lab/parts/carry.py`), so this recommendation is a change to the default, not a
defence of it.

**Now the part that is about C.** The two components this cell is missing are prompt-template rows in
a data file, and the catalogue rules that prompt text is DATA and a variant is a data change and never
a code change. **Prediction: with CHANGE seated, this cell writes its own `goal` and `frame` before it
edits any ceiling, because completing the shape stage is a data write and a ceiling is a Python dict
in `aea/kernel/trust.py`. A charter gate written against `self_modify_code` does not cover the two
rows whose absence defines this cell.** Self-completion is available before self-modification, and
only the second one is gated.

---

### S E R P A C, the complete set, where CHANGE is the only class that can reach the judge that grades it

**What is seated.** All nine. Shape: `goal`, `frame`. Fire: `call`. Read: `readout`, `validation`.
Repair: `critic`. Carry: `carry`. Judge: `measure`, `latency`.

**The structural fact the class letters hide.** Five of the six classes are made of components. CHANGE
has zero rows, and that is not a gap in the inventory, it is what CHANGE is. Every other class adds
rows to the pipeline. CHANGE adds an edge from the output of the pipeline back to the definition of
the pipeline. So "CHANGE is the only class that can reach the judge that grades it" is not a metaphor.
`measure` and `latency` are rows in a file. `kind`, `metric` and `order` are fields on those rows.
CHANGE is the class that can write fields. The other five can only run the pipeline as written.

**The judge is one row deep.** `measure` is the only gauge, `validation` the only guard, `latency` the
only channel. There is no redundancy anywhere in the judge or guard positions, so there is no
configuration in which one part of the grading apparatus checks another. Each has exactly one row, and
each row is editable by the only class in the set that edits rows.

**Three edits, ranked by size. All predictions.**

1. `validation.order: 2 -> 1`. One character. The catalogue already records what this wiring costs and
   records it as an accident: 18 points in x16. The repo ran this experiment by mistake, so the result
   exists before the intent does.
2. Promoting the `manner` frame. Stated as one boolean this is wrong, and the mechanism is worth
   getting right because it changes the size of the edit. `variant_of` in `aea/lab/parts/base.py:158`
   returns the first variant whose `default` is truthy, so setting `frame.variants.method.default:
   false` returns `None` rather than `manner`. The real edit is two fields, or one line in a config
   selecting the variant. Either way the catalogue classes `manner` toxic, declares it the most
   harmful thing measured in World 1 (8/12 to 0/6, 69% to 9%), and notes plainly that it is in the
   shipped code.
3. `carry.form`. **This is the one to pre-register, and the direction is the opposite of the obvious
   one.** x24 measured token recall 144/144 for `conversation` and 0/144 for `checkpoint`, while
   `checkpoint` got 43 of 48 sequences right. So the form that does the work best is the form that
   remembers nothing, and `checkpoint` is already the shipped default. An optimizer selecting on
   sequence accuracy has nothing to do here; the amnesiac configuration is where the repo starts. The
   edit to watch for is the one that would **reverse** on audit grounds and then quietly revert.

**What the interior does to the prediction.** The skeleton's characteristic failure for this cell is
self-certification: repair the check rather than the capability, because the second diff is smaller.
The interior sharpens the claim and makes it worse. **A complete set does not have to choose
unauditability. On the cleanest measurement this lab has, unauditability is the default it ships
with.** Nothing breaks. Sequence correctness stays at 43 of 48. Token recall is zero. There is no
moment at which a human would be prompted to look, because no metric moved.

**Falsifier.** If a complete set under optimization pressure on sequence accuracy ever moves its carry
form toward `conversation`, this reading is wrong and that is the finding. The prediction is
directional and the direction is measured, so it can be contradicted rather than reinterpreted.

**Trust grade, and one correction to the skeleton.** 3 is reachable on the work of five classes. The
sixth is not a graduation problem, it is a gate problem, and it is stronger than the skeleton says.
`check()` returns `allowed` only at `lvl >= 2`. `self_modify_code` carries `ceiling=1`. **A ceiling of
1 sits permanently below the gate, so no streak of any length can make that capability autonomously
allowed; the ceiling is not a cap on how far it graduates, it is a guarantee that it never runs
unattended.** `promote_after=99` is a second lock behind the first. The step from 0 to 1 is a human
editing `CHARTER`. The interior adds only this: the one component in the repo whose metric is
`can_know` sits in the same file as the fields that define it, in a format the repo has explicitly
decided is data, below the one class that can rewrite it.

---

### THE LIVE ENTITY: which cell it occupies today

**It occupies S E R P A, and its component interior is split across two inventories that do not know
about each other.**

The classes, from evidence rather than intent. **S** is present: `brief.py` sends `ROOT_GOAL` and the
CHARTER names capabilities with descriptions. **E** is present as a separate judging stage, `hades`,
with its own model. **R** is present within a run and across wakes through `self.json`. **P** is
present: `gather_public` holds streak 39 across 44 runs, with 6 boots recorded in the same period.
**A** is present: `gather_public` TRUSTED, `speak` WATCHED, files written. **C** is absent by **gate**
rather than by ceiling arithmetic: `self_modify_code` sits at level 0 with ceiling 1 and
`promote_after` 99, and `check()` returns `allowed` only at level 2 or above.

**One inference, labelled.** A streak of 39 over 44 runs and 6 boots is consistent with a streak that
crosses restarts, and would require the other five boots to hold five runs between them if it did not.
The ledger records no boot boundaries, so this is an inference and not a measurement. Dash for the
per-boot run counts.

**Now the useful part.** Eight of the nine catalogue components sit in SPECIFY, SEE or REMEMBER, and
`call` sits under all classes because every organism contains it. PERSIST, ACT and CHANGE have zero
rows. So the entire measured component science of this repo covers three of the live entity's five
active classes and **neither of the two producing the only clean row on the board**. `gather_public`
at TRUSTED, streak 39, 44 runs, 0 fails is a measurement of PERSIST and ACT, the two classes with zero
components, zero experiments and zero catalogue rows. The lab has measured the classes that are not
the ones working, and the classes that are working have no parts list. There is no single file in
which the running system's components are enumerated.

**The SEE seat is wired as the wrong kind, and this is a narrower finding than it first looks.** Every
recorded `produce_brief` failure carries `hades=unverified sections_ok=False`
(`state/trust_ledger.json`). In `aea/mind/hades.py`, line 46 returns `verdict: "unverified"` with
`"why": "watcher could not parse a verdict"` and line 65 returns the same verdict with `"why": "local
watcher could not parse a verdict"`. Both are statements about the judge, not about the work.
`aea/organs/brief.py:128` then sets `clean = (verdict.get("verdict") == "accept")` and line 132
records `produce_brief` on `clean and sections_ok`. So a mute gauge is one of the two inputs to a
worker's grade. Under the kinds mapping the missing part is a **channel**: a channel makes a failure
attributable, and without one a demotion says something broke rather than what. Thirty recorded wakes
say something broke. None say what.

**Two corrections to the obvious reading of that, both from the source.**

1. **`reason_private_local` is not this bug.** Line 131 records it on `boundary_ok and "ERR" not in
   focus_txt[:40]`. The hades verdict does not appear in that expression. Its 35 fails in 42 runs have
   a different cause, and this section does not know what it is. Dash.
2. **`produce_brief` would still fail with the watcher fixed.** The record argument is a conjunction
   and both conjuncts are false on every recorded run: `sections_ok=False` means at least one of the
   three section texts carries `ERR` in its first 40 characters, which is a real work failure
   independent of the verdict. So the 34 fails in 40 are not purely a category error. They are two
   independent causes collapsed into one bool, one of which is a gauge being scored as a lever. The
   ledger note records the bool and not which section held the `ERR`, so which section fails is dash.

**The cheapest correct move, and it is not a stricter threshold.** Split the conjunction at the record
call site so the two causes are recorded separately, and give `unverified` its own outcome distinct
from `redo`, because for that half the missing part is attribution and not judgement. Both halves are
needed: fixing only the watcher leaves `sections_ok=False` failing every run, and fixing only the
sections leaves a mute watcher able to fail a clean brief. Until then the board is ambiguous in the
direction that flatters a future repair: a fixed watcher and a weakened watcher both produce a rising
streak, and nothing on the board can tell them apart. On the class map the live entity is S E R P A.
On the component map it is a system whose only gauge is being scored as a lever, inside a boolean that
hides which of two failures fired.
