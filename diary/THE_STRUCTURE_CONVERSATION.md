# THE STRUCTURE CONVERSATION

*The engineering contract between a model's output and code that has to trust it. Written 2026-08-02
after R4a closed. Every number here was measured on this machine; nothing is quoted from a vendor
page. Read it before starting a rung, and hold the conversation in section 8 for that rung.*

The one-line version: **the model proposes, structure decides, code executes, the record survives
the crash.** Each clause is a section below.

---

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
