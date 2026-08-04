# THE STRUCTURE CONVERSATION

*The engineering contract between a model's output and code that has to trust it. Written 2026-08-02
after R4a closed. Every number here was measured on this machine; nothing is quoted from a vendor
page. Read it before starting a rung, and hold the conversation in section 8 for that rung.*

The one-line version: **the model proposes, structure decides, code executes, the record survives
the crash.** Each clause is a section below.

---

## 0 · THE PRINCIPLE, AND THE THREE RELATIONS THE LADDER ACTUALLY HAS

*Added 2026-08-03, during R5's contract. Luis: "we have to make sure that our logic model - that's
where it should have started from the very beginning - to have the logic sound. The logic more than
the code, more than anything." He is right that there is one, and it was not invented for this note:
it is EXTRACTED from laws this repo already paid for, one at a time, without noticing they were one
law.*

### The principle

> **A SYSTEM MAY ONLY ASSERT WHAT SOMETHING OUTSIDE IT COULD HAVE REFUTED.**

Six rules already in force here, and every one is this sentence in a different costume:

```
the entity        a hypothesis reality is permitted to kill                          R5
the instruments   every check gets a positive control, or it does not count
the bounds        a planted breach must FLIP the verdict - constructible, exercised
the rungs         a rung does not count until measured, and the measurement can say NO
the record        absent -> a dash, never a guess. Invalid means not used. Fail closed
the numbers       computed from what is ENFORCED, never from what was OBSERVED
```

**It generates the ordering by itself.** External refutation needs reach (R4b); reach is only safe
behind a closed argument language (R2); an argument language needs the decision to arrive intact
(R1.5, R1); all of it needs something that keeps running (R0). **The ladder is what this sentence
looks like when you unfold it** - which is why the logic retrofits cleanly onto rungs that were
derived empirically.

**AND THAT FIT IS CORROBORATION, NOT EVIDENCE. Corrected 2026-08-03.** The first version called it
"EVIDENCE THE ORDERING WAS RIGHT", which is the exact move this file names as a fallacy 190 lines
below: *if the principle generates the ladder the fit appears; the fit appeared; therefore the
principle generates the ladder* is affirming the consequent. The fit was also **retrodicted onto a
ladder that already existed**, so it carried no risk of failing to appear. Its honest status is the
one this file's own vocabulary mandates - **CORROBORATED, not yet dead, and nothing downstream may
treat it as true.** Which specifically means the derivation is not a licence to renumber the shipped
ladder; see the status note at the end of the walked ladder below.

It also decides a question that had been open: **the drive is not a rung**, because *wanting* is not
a thing anything outside the system could refute. It is an axis off the ladder, permanently visible
and permanently closed.

**AND THE HONEST WARNING THAT COMES WITH IT.** The rungs that are PROVEN are the ones built against
a defect that had already cost something. The rungs designed from theory - R7, R8, R9 - are the ones
that moved twice in a single conversation on 2026-08-03. So this principle's job is to gate the
UNBUILT half. Applying it backwards, as a reason to re-derive what already measures, is
infrastructure-as-avoidance wearing the best costume it has ever had.

### The derivation - the whole ladder from the one sentence

*Written as a DERIVATION rather than a description, because that makes it a test: if the principle
generates the ladder, the chain closes; where it fails to reach a rung, that rung is not doing
logical work. One rung failed. See the note at the end.*

A system may only assert what something outside it could have refuted. Everything else here follows
from taking that sentence seriously and asking, at each step, what it presupposes.

**Downward, the sentence has no slack in it.** Refutation from outside requires that the system can
reach outside; that is R4b. But reaching outside means composing a request, and a request composed
inside a context that already holds untrusted text is itself the way data escapes - so reach is
admissible only if nothing the system wrote can become the address. That is R2's bound, rehearsed
locally at R4a, where the source is SELECTED from a closed table rather than written. Composing
anything at all presupposes that the decision survived the passage from the part that thinks to the
part that acts, and survived it legibly, because a misheard decision produces an act nobody can
attribute: R1.5, and R1 beneath it. And all of it presupposes something that keeps running when
nobody is watching, or every number above describes a session rather than a system: R0. Remove any
one of these and the principle stops being checkable.

**Upward, reach is not enough.** A system that looks outside and changes course has not been refuted
- it has been STEERED, and being steered by third-party text is the failure every rung below was
built to prevent. Refutation requires a claim that PREDATES the evidence, which is R5, and which is
why R5 is a hinge rather than a step: it is the first place the principle is applied to the entity
itself rather than to its instruments. A claim that predates evidence has to come from somewhere,
and the only honest source is the record of what has already happened - R3. So R3 supplies the
claim, R4 supplies the reach, R5 supplies the commitment that makes the arrival of evidence mean
anything, and no one of the three is sufficient alone.

**Above the hinge the principle turns inward and the certainty falls.** Refutations accumulate, and
the pattern across them is new content with no external referent - the system's own generalisation,
defeasible by construction. That is R6, and it is admissible only because R5 installed something
outside the system that cannot be edited from within it. A generalisation is worth no more than its
premises, so when a premise dies its conclusions must be withdrawn: that is RETRACTION, and it is
what lineage is actually for - not an audit trail, the index of what to take back. Withdrawing a
conclusion drawn by a rule eventually requires the rules themselves to be nameable objects rather
than the code the system is made of; and only then may a rule be changed at all, judged necessarily
from a level the change cannot reach. **That level is the hashed artefact R5 put on disk. The top of
the ladder does not rest on the rung beneath it - it rests on the hinge.**

**WHAT THE DERIVATION FOUND BY OMISSION, which is why it was worth writing.** The chain reaches R0,
R1, R1.5, R2, R3, R4a, R4b, R5, R6, retraction, legibility and R9 - and **never once needs the
council.** An adversarial review does not fall out of the principle, and the reason is exact: **a
council is outside the MODEL but inside the SYSTEM.** It reduces correlated error, which is
valuable, but it cannot ground an assertion, because nothing inside the system can be the thing
outside it that could have refuted. So the council is a RELIABILITY mechanism, not a logical rung -
the same status the drive now has, and arrived at by the same test.

This is also the derivation of a law this repo already earned the expensive way: **a council may
WRITE a gate, it may never BE one.** That was learned by watching a gate become unfalsifiable. It is
now a consequence of the principle rather than a scar.

### THE LADDER, WALKED - and it reads in both directions

*Each rung carries a BECAUSE and a THEREFORE. Read the `because` clauses downward and you get the
presupposition chain - what must already be true. Read the `therefore` clauses upward and you get
the construction chain - what each rung hands to the next. One text, two directions, and neither is
a summary of the other.*

**R0 · THE LOOP SURVIVES**
BECAUSE nothing is beneath it; this is the floor. A measurement of a system that runs only while
watched is a measurement of the watching.
THEREFORE something persists between decisions, so what it decides can be heard by something else.

**R1 · THE DECISION IS READ**
BECAUSE there must be something that keeps running, or there is nothing for a decision to be heard by.
THEREFORE the part that thinks reaches the part that acts - which makes a MISHEARING possible, and
therefore worth detecting.

**R1.5 · THE DECISION IS PARSED**
BECAUSE a decision must be read before the way it is understood can matter.
THEREFORE what arrives is either the decision or a recorded failure to understand it, and an act can
be attributed to one or the other.

**R2 · THE DECISION IS A TOOL CALL**
BECAUSE an act can only be attributed if the decision reached the actor intact.
THEREFORE the system acts in the world - and because nothing it wrote may become an argument, acting
cannot itself become a channel out.

**R3 · THE OUTCOME IS REMEMBERED**
BECAUSE there must be acts before there can be outcomes.
THEREFORE it holds a record of what HAPPENED rather than what was meant - the only honest material
from which a claim about itself can later be generated.

**R4a · PERCEPTION IS A CHOICE**
BECAUSE choosing where to look means nothing until a record exists that could make one place worth
more than another.
THEREFORE what it examines is its own, SELECTED from a closed table, so that choosing never becomes
writing.

**R4b · PERCEPTION REACHES THE WORLD**
BECAUSE local choice is the rehearsal, and the bound that makes selection safe is the same bound
that makes reach admissible.
THEREFORE something can leave the machine - and because the request is itself the escape, the bound
here stops being a proof and becomes a rate.

**R5 · RESEARCH  — THE HINGE**
BECAUSE a claim can be refuted from outside only if the outside can be reached (R4b), and generated
honestly only from a record of what already happened (R3). *And R4b needs R5 in return, for a reason
to fire at all - this is the fixed point, and the only one on the ladder.*
THEREFORE the outside can change its direction only by killing something it said first, and the
DEATH - never the content of a page - is what moves it. **This is the first object in the system that
nothing inside the system can forge.**

**R6 · REFLECTION**
BECAUSE a generalisation needs refutations to generalise over, and needs something unforgeable to be
anchored to.
THEREFORE it holds claims that were in neither its record nor the world - its own, defeasible by
construction, carrying both lineage and the taint of whatever third-party bytes they descend from.

**R7 · RETRACTION**
BECAUSE there must be derived claims before there is anything to withdraw, and deaths before there
is a reason to.
THEREFORE nothing outlives its grounds - which is what makes lineage load-bearing rather than
decorative, and what stops one undetected contradiction from making everything derivable.

**R8 · THE RULES ARE NAMEABLE**
BECAUSE you cannot withdraw what a rule produced without being able to say which rule produced it.
THEREFORE the protocol is an object the system can denote - READ, never written, because on this
ladder the reader always precedes the writer.

**R9 · IT EVOLVES ITS OWN PROTOCOL**
BECAUSE a rule can be changed safely only by something that can name it, evaluate what it produced,
and take back what depended on it.
THEREFORE it changes a rule it runs by - having stated beforehand what the change should improve and
what would count as the change having failed - judged from a level the change cannot reach. **That
level is R5's artefact. The ladder closes on its hinge, not on its top.**

**The two readings, each in one line.**

```
DOWNWARD  assert only what could be refuted -> requires reach -> requires a closed argument
          language -> requires a decision that arrives intact -> requires something that runs
UPWARD    survive -> be heard -> be understood -> act -> remember -> choose where to look ->
          reach outside -> be wrong on purpose -> generalise -> take it back -> name your own
          rules -> change them
```

**AND WHAT THE DERIVATION DOES NOT REACH.** *The council* - outside the model, inside the system; it
lowers correlated error and cannot ground an assertion. *The drive* - wanting is not a thing anything
outside the system could refute. The proposal is that both are axes beside the ladder rather than
steps on it. **The upper ladder is not more capability. It is more restraint.**

> **STATUS OF R7, R8, R9 ABOVE: PROPOSAL, NOT ADOPTED. Corrected 2026-08-03.**
> `aea/tooling/ladder.py` still declares **R7 = THE COUNCIL ON ITS OWN PLANS** and **R8 = THE
> DRIVE**; `state/ladder.json` carries the same, and `climb.py` renders those titles to the
> published page. So the walked ladder above and the shipped ladder are **two different ladders**,
> and the first version of this section said the council and the drive had been "removed by the
> derivation rather than by preference" - past tense, accomplished. **Nothing had been removed.**
>
> Found by three independent lenses in an adversarial pass, and it is the only finding against this
> section that survived every attempt to refute it. It is also the worst kind of error for this
> file to contain: **asserting a change that never happened, in the document about only asserting
> what could be refuted.** Adopting the renumbering is a decision that changes the published page
> and it has not been taken.

### The three relations

The ladder was being read as one kind of edge. It has three, and conflating them is what made "are
the rungs cumulative?" unanswerable:

```
PRESUPPOSITION   N is impossible without N-1        a strict order    R0->R1->R1.5->R2->R3
USE              N consumes N-1's output            a weaker edge     R3->R4a
MUTUAL           N and M are only true TOGETHER     a FIXED POINT     R4b <-> R5
```

So the ladder is **a directed graph whose CONDENSATION is a DAG**, with one non-trivial strongly
connected component, `{R4b, R5}`. It is not a staircase and not a partial order, because a cycle
violates antisymmetry.

**Two corrections, 2026-08-03, both from the adversarial pass, and the second is the one that
matters.** The first version said "a DAG with one strongly connected component" - which is
self-contradictory, since a DAG has no component larger than one, and it was the single sentence a
reader would quote. Fixed above.

The second is sharper: **the cycle may be an artefact of bundling.** `R5_CONTRACT.md` splits R5 into
R5a / R5b / R5c on §8's own no-bundling law, and `ladder.py` records R4b as already split in
practice - conditions 1 and 2 hold, only 3 is open. Take both splits seriously and the edges are
`R4b-BOUND -> R5a -> R5b -> R5c -> R4b-POWER`, which is **acyclic**. So the claim that *some
capabilities cannot be reached in sequence, only together* is **CORROBORATED, not established** -
it may dissolve the moment question 1 is applied to both endpoints. The bootstrap discipline below
holds either way, because it is about seeds and their removal rather than about cycles.

### How a mutual pair is built, and the discipline that keeps it honest

A cycle has no bottom, so it cannot be built in stages. It is reached by **iteration to convergence**:
seed a weak version of one side by hand, use it to build the other, then remove the seed and check
the pair still holds. That is bootstrapping to a fixed point, and **it already happened here** - the
line at `aea/loop/aea.py:368` (*"your record holds NOTHING from outside this machine"*) was a
hand-written weak stand-in for R5's output, placed so R4b could move at all.

**D52 was not the error of placing the seed. It was reading the seed as the answer.** Which gives the
rule, and it generalises to every future cycle:

> **EVERY BOOTSTRAP MUST BE LABELLED AS SCAFFOLDING AND MUST BE REMOVABLE, AND THE RUNG DOES NOT
> COUNT UNTIL IT HOLDS WITHOUT IT.**

### What the logic lens changed the day it arrived

Four things, none cosmetic, all in `diary/R5_CONTRACT.md`:

- **"Survives" is not a conclusion.** *If H then P; P; therefore H* is affirming the consequent. Only
  refutation is valid (modus tollens), which is the formal reason R5's gate demands a DEATH. The
  status is **CORROBORATED** - not yet dead - and nothing downstream may treat it as true.
- **Duhem-Quine.** You never refute a hypothesis, only a CONJUNCTION. A hypothesis row must name what
  it **holds fixed**, or a death is unattributable and the gate counts noise.
- **Retraction is a missing rung.** R6 derives from claims, R5 kills claims, and nothing withdraws a
  conclusion whose premise died. That is AGM belief revision, and it reframes provenance: **lineage
  is the retraction index, not an audit trail.** Also here: an undetected contradiction is unbounded
  corruption, because from a contradiction anything follows.
- **Tarski is why R5 must precede R9.** *"A system that edits its own code can edit the thing that
  judges the edit"* is the undefinability of truth in a self-referential system. The escape is a
  hierarchy of levels, and **R5's hashed artefact is the first object at a level the entity cannot
  reach.**

## 1 · HOW TO GET THE JSON OUT

Measured 2026-08-02: three models x four enforcement modes, twelve live calls, no token ceiling,
`reasoning_content` read separately from `content`.

| model | kind | none | json_object | json_schema | nvext guided |
|---|---|---|---|---|---|
| nemotron-3-nano-30b-a3b | reasoning | VALID | **wrong shape** | VALID | VALID |
| gpt-oss-20b | mixed | VALID | VALID | VALID | VALID |
| llama-3.3-70b-instruct | plain | VALID | VALID | VALID | VALID |

**Eleven of twelve valid on the first try, clean - no fence stripping, no brace hunting.**

Four things that follow, and the fourth is the only one that matters:

- **A prompt showing the exact object is enough.** The `none` column is VALID on all three models.
  Enforcement is not required to get structure; it raises the hit rate.
- **`json_object` is not schema enforcement.** It guarantees the reply is JSON, not that it is *your*
  JSON. The single miss is exactly that: clean JSON, wrong shape.
- **Never send a token ceiling.** The first version of this measurement used `max_tokens=400` and
  reported "provider enforcement does not work". It was measuring its own truncation. The same cut
  was live in `hands.probe_tools`, where a rod that spends ~1,400 characters reasoning was graded
  `no_call: cannot call tools`. Omit the field entirely - absence lets the plant apply its own
  maximum, whereas a bigger number is a newer guess about somebody else's model.
- **THEREFORE: enforcement is a bonus and never the contract.** n=1 per cell. A thing that works
  once is not a thing that works. The failure arrives at 1-in-50 and it arrives as **wrong shape,
  not unparseable** - which a naive `json.loads` check waves straight through. Only our own
  validator makes structure a rule.

Reasoning models file their thinking in `reasoning_content`. Read it separately or you will parse
the thinking and call the model broken.

## 2 · HOW TO USE IT - THE VALIDATOR

Three stages, and they are three because they fail differently.

```
extract   clean -> fenced(```) -> braces{...}      record WHICH rescue worked
shape     required keys present, right types       a parse is not a shape
bound     decide.parse + hands.allowed             the certified boundary, unchanged
```

**Record which rescue worked.** "The reply was clean" and "a fence had to be stripped" are different
facts about a rod, and the second one predicts the first failure.

**The bound stage is free.** `decide.parse` already certifies the argument language: of 1,112,064
codepoints it admits 697, none of them alphabetic. A step that passes it has exactly the authority a
single move has - which is why a *path* of N validated steps needs no new trust surface. This is the
whole reason the design is affordable.

**Fail closed.** Wrong shape is not close enough. On invalid: retry K times **feeding the validation
error back**, then decline the tick with a reason. Declining is a recorded state; guessing is not.

Measured 2026-08-02: **nothing anywhere in this repo retries on an invalid parse.** A reply that does
not parse is a lost tick - no second ask, no error fed back. That is the artefact this section
describes and it does not exist yet.

## 3 · WHERE THE CODE MANAGES IT

`aea/kernel/grid.py` is the single choke point - eight call sites, and it **already carries
`response_format`, `json_schema`, `nvext` and `tools` plumbing that nothing uses.**

The validator goes there, once. Not at each call site. Law W1 applied to ourselves: the second time
you write it, extract it - and there are already sixteen scratchpad probes that each re-implemented
the same untimed POST and the same parse.

## 4 · THE WHOLE PROCESS

```
path = load()                             # survives a crash, because R0 works
while not path.done and len(path.steps) < BUDGET:
    append(step, result); save(path)      # WRITE-AHEAD - before any thinking
    reply  = ask(model, prompt(path))     # the model sees every prior result. No ceiling
    step   = validate(reply)              # section 2. Fails closed
    if not step: step = retry(K, error_fed_back) or decline_tick()
    result = hands.invoke(step)           # the certified boundary
```

**The path grows one validated step at a time and the whole loop re-runs with the longer path.** It
is not plan-then-execute: a plan written before step 2 ran is stale by step 3. Each step is chosen
after seeing what actually happened, which makes it both more flexible and strictly safer.

**Nothing re-executes.** Results live in the record and are re-read. This is what an IDE agent does -
the transcript is the memo; each turn appends `(call, result)` and re-sends the accumulated whole.
Provider prompt caching is an optimisation on top of that, not the mechanism. The saving is not
tokens, it is **side effects and time**: a tool that ran must not run twice, and a 40-second call
must not be paid again.

**The path is data, never a program.** Only the wake writes steps. It cannot extend itself at
execution time. That single line is what keeps this out of R9, and it belongs in the module docstring
rather than in a design note - `render.py` had its gate as a comment and nothing enforced it.

## 5 · HOW IT REACTIVATES

The defect found 2026-08-02, and it invalidates less than it re-frames: **`controlroom.py:699`
spawns `aea.loop.live` detached, and nothing anywhere spawns `aea.loop.aea`.** The body runs
unattended; the mind runs when a person types. R0's 246.9 hours certified a body whose mind had
spoken once. Measured rhythm across 88 wakes: median gap 2.1 minutes, 38 of 87 under two minutes,
longest **14,814 minutes** - bursts when a human sat down, not a rhythm.

Three pieces, in order:

1. **`live` spawns the wake when it has nothing to react to.** One missing call site. Thinking is
   worth most exactly when there is nothing left to react to.
2. **`hb["next_wake_s"]`, computed by the entity from state it already keeps.** The sleep-pressure
   signal exists and is unused: 107 briefs seen against 22 consolidated.
3. **Clamped.** Floor 60s, a wakes-per-day budget the entity cannot raise, and `state/STOP` checked
   before each wake so a kill survives the entity's own next scheduled run.

**A cron job is not an oscillator.** Biology's clock is endogenous - it free-runs in constant
darkness; light shifts its phase but does not cause it. If the OS decides when the entity lives, the
human has only moved into a config file. The entity must compute the number; something dumb may
execute it.

## 6 · WHAT MEMORY IS KEPT

Four stores, four lifetimes. Confusing them is how a rung ends up measuring the wrong thing.

| store | holds | lives | written by | read by |
|---|---|---|---|---|
| `path.json` | this inquiry's steps + results | until the question closes | the loop | the next prompt |
| `outcomes.jsonl` | what worked and failed, per move | forever | `_record_outcome` | the suppressor |
| `perception.jsonl` | what it chose to look at, and why | forever | the wake path only | R4a's gate |
| consolidated memory | the semantic store | forever | `ASLEEP:consolidate` | the seed |

**Every store needs a named writer AND a named reader.** A store with no reader is the R1 defect - a
working wire nobody could see, open for weeks. A store with no writer is worse, because it reads as
zero rather than as absent. Check both when adding one.

**Provenance fails closed.** `perception.jsonl` counts a row only when `src == "wake"` AND
`why_from == "wake"`. The first version stored `decide.explain`'s note - *"the wake chose
what_to_try (1s ago)"* - and the gate counted nine reasons of which none was a reason. Where the
value came from is a *fact*; sniffing boilerplate by wording would be a guess.

## 7 · CHECKPOINTS

- **Save before thinking.** Write-ahead. Think-then-save means a crash between execution and
  persistence re-runs the step, which for a side-effecting tool is doing it twice for real.
- **Mark carried-out before dispatch, not after.** Already the pattern: `decide.choose` sets
  `hb["_last_decision"]` at choose time. Before this existed, one decision was handed to the acting
  loop on every tick for ninety minutes and executed every time - 54 ledger rows against 26
  decisions, which read from outside as an entity repeating itself.
- **Resumption has three cases, and the third is the one people get wrong.** On boot: a path whose
  last step has a result continues; a path with no open step is done; **a step written with NO
  result crashed mid-execution - do not re-run it.** Mark the result `unknown` and let the next step
  be chosen knowing that. Re-running is how a crash becomes a duplicate purchase.
- **A cap of any kind must be logged.** If a loop stops at a budget, `log()` what was dropped. Silent
  truncation reads as completion.

## 8 · THE CONVERSATION TO HOLD ON EVERY RUNG

Seven questions. Answer them in writing before building, and the answers go in the rung's entry.

1. **POWER** - what can it do that it could not do before? One sentence, no bundling. Twice this
   repo has had to un-bundle a rung: R2 carried situation-variety that R4 produces, and R2 carried
   FALLBACK that belongs to R3. Both times one rung was blocked on another rung's evidence.
2. **BOUND** - what must remain impossible, and where is that enforced *in code*? A rung is POWER
   plus BOUND wearing one name, and only POWER was ever gated.
3. **STRUCTURE** - what does the model emit, against what schema, and what happens when it is
   invalid? "Invalid means not used" is the only acceptable answer.
4. **INSTRUMENT** - what artefact records this happening, and **is it built before the capability?**
   From outside, "the wire has never fired" and "nobody is writing it down" are identical.
5. **GATE** - is it satisfiable by the entity ALONE? Does it need a capability produced by a rung
   ABOVE it? If the entity has to make the world cooperate, the gate measures the world.
6. **CONTROL** - what input makes this check say NO, and is that input exercised? A check with no
   exercised negative case is `return True`.
7. **MEMORY** - what is kept, who writes it, who reads it, how long does it live?

### The standing checks, each earned

- **A mechanism present and not connected is the defect class of this repo.** Four instances in one
  day: a heartbeat key read three times and assigned nowhere; a frozen check defined and never
  called; a publishing gate written as a comment; a CLI flag accepted, documented, and never read.
  Each was found by a different accident. All four now have a frozen check with a control.
- **Never cap tokens.** It has produced two false findings, one of them in the measurement that
  proved the rule.
- **Ask the live thing, never the description of it.** Docs describe a product; the endpoint
  describes what you have.
- **Never anchor a source edit on a token that can appear in data.** Four patches in one session
  anchored on `if __name__ == "__main__":`; the fourth landed inside a triple-quoted fixture and the
  suite printed 108 green rows for a function that existed only as characters in a string. Anchor on
  the last occurrence and assert with `ast` that the name landed at module level.
- **Every check gets a positive control on the defect class it claims to cover, or it does not
  count.**

### Where the rungs stand

R0, R1, R1.5, R2, R3, R4a **proven**. R4b shut behind `dispatch` running dry plus a reconvened
council. R5-R9 future.

The honest asterisk on R4a: its eight occasions were caused by a script alternating the two loops by
hand. Section 5 is what removes the asterisk, and it is the next thing built.

---

## 9 · REACHING CONTENT: WHICH LOCKS, AND WHEN

*Added 2026-08-02 after `web_search` was found dead. Luis: "Don't go to the hard locks. Go to what's
open, and that's the key. But if something that is on a hard lock we need it, we need to get a way
through it - probably the latest stages."*

**THE PRIORITY: FIND DOORS THAT ARE OPEN, DO NOT GET BETTER AT PICKING LOCKS.** Measured 2026-08-02:
`lite.duckduckgo.com` HTTP 202 challenge page, `html.duckduckgo.com` the same, `www.mojeek.com`
HTTP 200 with `<title>Captcha</title>`. Both general engines refuse a non-browser client. Meanwhile
`export.arxiv.org`, `hn.algolia.com` and `huggingface.co` returned 200 with real results in under
two seconds, keyless. The open door was faster, more reliable, and STRICTLY SAFER for the rung above
- results come from an allowlisted domain by construction rather than by a filter applied after.

"Hard lock" is four different things and they have four different answers:

| lock | a way through | stage |
|---|---|---|
| bot detection / captcha | defeating detection | **NOT BUILT.** Also the least necessary - a site that captchas an automated client almost always publishes a feed or an API that does not |
| authentication we are entitled to | a credential, used properly | **NOW**, under the constraint below |
| paywall / licence | paying, or an institutional route | a business decision, not a rung |
| JS-rendered content | a headless browser | **LATER STAGE. Own bound, own council** |

**THE CREDENTIAL CONSTRAINT, AND IT IS NOT NEGOTIABLE.** An authenticated route is normal API usage,
not evasion - but the credential lives CODE-SIDE ONLY and never enters the entity's context. `.env`
at ROOT holds 16 live provider credentials and the wake has no measured read path to them; that
property must survive every route we add. The entity chooses a topic NAME, code attaches the header.
Same shape as `plan()`: the entity picks the key, the table supplies the value.

Concrete and outstanding: unauthenticated `api.github.com` returned 504 with 0 results and is what
starves `local_inference`, the one dispatch topic still producing nothing. A token fixes it,
code-side.

**WHY THE BROWSER IS A LATER STAGE, stated as a property rather than as caution.** A headless browser
executes third-party JavaScript, so THE PAGE issues outbound requests nobody here authored -
beacons, third-party fetches, anything. R4b's claim - "no byte of the outbound request originates
from model output" - stops being the relevant sentence, not because the model writes bytes but
because the page does. Any certificate built on that claim is void the moment a browser is in the
path. It needs its own bound and its own council, and it is a real capability worth having later.

**AND THE EVOLUTION TRIGGER IS THE ENTITY, NOT A SELF-HEALING SCRAPER.** Luis, same session: *"the
tools need to evolve, but the trigger needs to be the autonomous entity architecture."* Correct - and
the machinery already exists here AND IS WIRED AND WORKING, which is not what this section said an
hour ago.

**RETRACTION, and it was in this file.** The first version of this section said the three organs were
"reachable and silent", with "empty stores after 280 ticks", implying a wire that never fires. That
was read off `EXTRACTED` in the provenance table plus the size of `crystal.json`. EXTRACTED means A
STATIC CALL SITE EXISTS - it is not a claim that the function runs, and I published it as one. That
is the same error as certifying dispatch's BOUND and assuming its POWER, one hour later, in the
document written to prevent it.

MEASURED instead of inferred:

    impasse.scan       <- aea.loop.aea:standing
    unstick.propose    <- aea.loop.live:_notice_and_propose      live.py:743, ON THE TICK PATH
    unstick.record     <- aea.loop.live:_notice_and_propose
    crystal.harvest    <- aea.loop.live:_notice_and_propose
    crystal.applicable <- aea.loop.aea:standing, live:_notice_and_propose
    crystal.carry_out  <- aea.loop.live:_notice_and_propose

    organ functions with no caller anywhere: 0

And `impasse.scan()` over the real 140KB outcome record judges nine capabilities and finds one
genuinely stuck - `produce_brief`, "3 of the last 4 failures share one cause" - with the other eight
correctly `working`. `_notice_and_propose`'s own docstring records that it was built to close exactly
the CLI-only gap this section claimed was still open.

Nothing has crystallised because `crystal.harvest` requires something that worked TWICE and nothing
has yet. That is the design behaving correctly, not a wire that never fires.

**THE REAL GAP IS NARROWER AND IT IS AN ALTITUDE PROBLEM.** `impasse` watches nine CAPABILITIES -
gather_public, produce_brief, send_outbound and so on. "web_search returns a captcha page" is not one
of them, and cannot become one, because a capability degrades gracefully around a dead tool: the
brief still gets produced, just worse. So a tool can be dead for weeks with every capability reading
`working`.

Underneath that sits the recording level: the hands ledger carries `outcome` on all 146 rows
(`ran 125 / refused 11 / raised 10`) and it is TRANSPORT-level. `web_search` returning
"NO RESULTS (14313 bytes but nothing parsed)" was recorded as `ran`, successfully, for weeks.

So the missing piece is one dimension at one altitude - **did the TOOL do its job**, distinct from
*did the call complete* and from *is the CAPABILITY failing* - fed into the loop that already runs:

    tool returns nothing usable  ->  impasse.signature   a named stuck-state
    impasse recorded             ->  unstick.propose     another route, from a CLOSED set
    that route works twice       ->  crystal.harvest     it becomes a part
    part applies next time       ->  crystal.applicable  learning, and measurable

**What must never be in that loop:** a model-GENERATED parser or URL shape that then executes. The
entity selecting an untried technique from a human-authored set is R4-shaped and safe; the entity
writing the technique is R9 and voids every bound below it.


---

## 10 · THE PROCESS DECODER - AND WHY IT IS ALREADY HALF HERE

*Luis, 2026-08-02: "spaghetti code is not [maintainable]. It's not flexible enough, because the code
has to allow for this flexibility to be possible. So I figured the best will be like a reader that
there is JSON files - like a decoder of processes, and it executes the paths."*

**THE DIAGNOSIS IS CORRECT AND IT IS MEASURED.** 177 modules, 33 reachable from a wake, 133
orphaned. One function in nine is alive. That is the shape of a codebase that grew by addition
rather than by composition, and it is exactly what a process-decoder answers.

**AND THE PATTERN IS ALREADY THE REPO'S ARCHITECTURE, four times over, unnamed:**

| the declaration | the executor | who may write the declaration |
|---|---|---|
| `dispatch.TOPICS` - 5 topics, literal queries | `dispatch.run` | a human edit, reviewed as a diff |
| `hands.TOOLS` - 11 tools, impl per name | `hands.invoke` | a human edit |
| `hands.READABLE_STATES` - 16 filenames | `_read_state` | a human edit |
| `ladder.RUNG_FUNCS` / `RUNG_STANDBY` | `verify_funcs` | a human edit |

Every one is the same move: **the entity selects a KEY, the table supplies the VALUE, one executor
walks it.** That is the process decoder, and R2's whole certified bound rests on it - of 1,112,064
codepoints the argument language admits 697, none alphabetic, precisely because nothing the model
writes ever becomes a path.

**SO THE WORK IS NOT TO BUILD A DECODER. IT IS TO NAME THE PATTERN AND STOP DEVIATING FROM IT.**
Adding a framework layer to a tree with 133 orphaned modules adds a 134th. The repo does not need a
new engine; it needs the four tables above to be recognisably one idea, so the fifth is written that
way without being told.

**THE LINE THAT DECIDES WHETHER A DECODER IS SAFE, and it is the only one that matters:**

    declaration HUMAN-AUTHORED + executor in code   ->  this is R2/R4-shaped. Certified. Safe.
    declaration MODEL-GENERATED + executed          ->  this is R9. Voids every bound below it.

A JSON file that describes a process is data. The same file emitted by a model and then executed is
a program the model wrote, and the review surface stops being a diff. `dispatch.py`'s docstring
already states the test: *the entity chooses WHEN and WHICH, never WHAT in its own words. Adding a
topic is a human edit to this file, and that is the point - the review surface is a diff, not a
prompt.*

**WHAT FLEXIBILITY ACTUALLY REQUIRES**, since the complaint is that the code must permit it:

- **one executor per shape, never two.** `run` composing through `dry` was this: two copies of one
  URL regex, byte-identical, one edit from disagreeing, and only one of them measured
- **the declaration carries its own evidence.** `RUNG_FUNCS` names functions AND `verify_funcs`
  grades them by what reaches them; a table that cannot be checked against the tree goes stale
  silently
- **a missing reader must be visible.** `climb._evidence` renders *"measured, but this page has no
  reader for R4b yet"* rather than a dash - the gap announces itself instead of looking like absence
- **every store needs a named writer AND reader.** `dispatch_power.json` was written and read by
  nobody for an hour, which is the same defect as `funcs_check`, found the same day

**THE NEXT STEP THAT IS ACTUALLY THIS, and it is small.** The path object in section 4 is a process
declaration with a cursor, executed by one loop, every step validated by `decide.parse`. Build that
and the decoder exists - as the fifth instance of a pattern already here, rather than as a framework
sitting above four things that already work.
