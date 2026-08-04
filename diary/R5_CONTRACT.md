# R5 · THE CONTRACT — the seven questions, answered before anything is built

*Written 2026-08-03, opening the R5 conversation. Every number below was measured on this machine
today by reading the code that decides it, not by quoting a label. `THE_STRUCTURE_CONVERSATION.md`
§8 is the form; `HANDOFF_R5.md` §6 is the list of open questions this file has to settle.*

---

## 00 · WHAT R5 IS, AND WHY IT SITS WHERE IT SITS

*Written first because the seven answers below are worthless against a wrong concept.*

**R5 is not "the entity can search." Searching is R4b.** R5 is the entity holding a claim about the
world that reality is ALLOWED TO KILL, and then letting it be killed. The ladder's own line:
*"A summary cannot be wrong, which is exactly why it cannot be useful."* The difference between
gathering and research is a commitment made BEFORE the evidence, plus a stated rule for what would
falsify it. Strip either and this is R4b with more steps.

**Every rung from R0 to R4b has the entity as its object.** R0 the body survives · R1 the decision is
read · R1.5 it is parsed and a mishearing leaves a receipt · R2 it becomes a real tool call and no
string the wake wrote reaches an argument · R3 the outcome is remembered · R4a what it looks at next
is a choice with the reason recorded · R4b that choice reaches outside. R3 remembers *whether my move
worked* - a record of self-performance. **R5 is the first rung whose object is the world**, and so
the first place the entity can be wrong in a way that is not a malfunction.

### What R5 consumes from below, each load-bearing

- **R3 is where a hypothesis comes from**, and this connection decides whether the rung is real. R3's
  gate asks that "a later decision demonstrably uses that record"; R5 is the most demanding reader
  that record has had. A repeated failure, or a census belief the record contradicts, is a claim the
  entity CANNOT SETTLE FROM INSIDE. If the claim comes from Luis instead, the gate measures Luis and
  R5 is D52 in a new costume.
- **R2's bound is inherited whole.** Hypothesis selection and topic selection are both key-selection
  from a human-authored table, so R5 adds no new trust surface - the fifth instance of the decoder
  pattern (§10 of the structure conversation), not a new engine.
- **R1.5 is the shape of the find-validator.** An invalid extraction leaves a receipt, never vanishes.
- **R4a's gate explicitly defers to R5** (`ladder.py:184`): it does not require non-duplicate queries
  across a week, because *"that needs a week and a reason to vary, and the reason comes from R5, one
  rung UP."*
- **R0 stops being background.** A run costs 90 minutes of enforced floor. R5 is the first capability
  whose unit of work is a MULTI-TICK OBJECT WITH A CURSOR - `crystal` accumulates across independent
  ticks, but a research run must RESUME AT A STEP. That is why the path object exists here and
  nowhere below.

### What R5 gives back

- **To R4b: the NEED.** Condition 3 asks the entity to choose to look outside for its own reasons. An
  open hypothesis with unmet evidence is the first internal state that ONLY AN OUTBOUND ACT CAN
  CHANGE. The dependency runs both ways, and this is the third instance of a recorded pattern - R2
  needed R4's situation variety, R4a needed R5's reason to vary.
- **To R6: material worth linking** (`ladder.py:289`). Without R5 every provenance chain terminates
  inside the machine. R5 produces the first memories whose thread runs out to a hash, a URL, a quote.

### The threat inverts here, and that is the structural difference

Every bound below is about what LEAVES - the query as exfiltration channel, the argument the model
must not write, the bits per day. **R5's bound is the first INBOUND one**: not "can something get
out" but "can something false get written down as true". That is why the declared bound is a
fabricated source, and why a research organ is the first component with a MOTIVE to invent a
reference - a statement about incentives, not a caution.

It also changes the PROOF SHAPE, and this is what tells you where the code goes:

```
R2's bound   what is REPRESENTABLE   697 of 1,112,064 codepoints, none alphabetic.
                                     An injection cannot be EXPRESSED
R5's bound   what is PRODUCIBLE      bytes the entity never saw, hashed at a moment it
                                     does not control. A source cannot be INVENTED
```

Hashing what the entity was SHOWN - which is what `hands.py:1186` does today - proves nothing under
either shape. See §2.

### The mechanical loop

```
1  a claim derived from R3's record, written with its stopping rule, BEFORE any search
2  the claim is unsettled - evidence 0 of N - and nothing inward can change that number
3  the entity chooses look_outward, a topic from the closed table              (R4b)
4  bytes arrive; hashed AT ARRIVAL; stored under the hash                      (the bound)
5  the model extracts finds: verbatim quote + citation, validated against the stored bytes
6  code counts validated finds against the stopping rule
7  status written by CODE: survives / dies / forks / unsettled - never by a model
8  A DEATH TAKES A PATH THE SYSTEM WOULD NOT OTHERWISE HAVE TAKEN         <- see 000
```

**Step 8 closes it.** R5 is the first rung whose output feeds the store that generates its own next
input - the loop closing on itself with external material inside it.

---

## 000 · A HYPOTHESIS THAT CHANGES NOTHING IS A DIARY ENTRY

*Added 2026-08-03 after Luis pushed on the first version of this file, whose loop ended at "the
result returns to R3's record". He was right and the correction is load-bearing:*

> "R5 is where the hypothesis leads to another path otherwise, if we didn't check exterior beyond
> what I type for the entity, it wouldn't have found the error."

**THE DEFECT IN THE FIRST DRAFT.** A store with no reader is the R1 defect - a working wire open for
weeks because nothing wrote the comparison down. A dead hypothesis that lands in a jsonl and moves
nothing is that defect with a certificate attached. The gate said "five hypotheses died"; five deaths
that changed no behaviour is a note-taker with a budget.

**THE READER ALREADY EXISTS, IS WIRED, RUNS ON THE TICK PATH, AND IS BLIND AT EXACTLY ONE ALTITUDE.**

```
impasse.scan       <- aea.loop.aea:standing
unstick.propose    <- aea.loop.live:_notice_and_propose      live.py:743, ON THE TICK PATH
crystal.harvest    <- aea.loop.live:_notice_and_propose
```

`impasse` watches nine CAPABILITIES and cannot see a dead TOOL, because a capability degrades
gracefully around one: the brief still gets produced, just worse. Measured: `web_search` returned a
captcha page for weeks, `hands.invoke` recorded `outcome="ran"` (hands.py:1185 - a string return is a
transport success), and every capability read `working`. **Nothing internal was wrong.** The sentence
that would have caught it - *the route is dead upstream* - is a claim about the WORLD, and until R5
the machine has no way to hold one. The only exterior in the system today is what Luis types.

**SO STEP 8 IS THE POINT, NOT THE EPILOGUE:**

```
belief in the record      "gather_public is working"          internal, and wrong
hypothesis derived        "the route is dead upstream"        a claim about the world
hashed evidence           bytes from arxiv / hn / hf / github external, unfakeable
counted, rule applied     2 refuting, 0 supporting            code decides
status DIED               the belief was wrong
CONSEQUENCE, CLOSED SET   impasse.signature gets a named stuck-state
                          -> unstick proposes another route FROM A CLOSED SET
                          -> it works twice -> crystal.harvest makes it a part
```

**THE BUILD TARGET CHANGES ACCORDINGLY.** Not "five hypotheses died" - that is the gate, and a gate
is not a target. The thing to build toward is **ONE dead hypothesis that makes `unstick` propose a
route it would not otherwise have proposed.** That is a consequence a person can watch happen, and it
is the difference between R5 shipping and R5 being read.

**AND THE LINE THAT KEEPS THIS BELOW R9, UNCHANGED.** The entity chooses WHICH claim and WHEN to
spend budget. **The code decides WHAT a death changes, from a human-authored table reviewed as a
diff.** The moment a dead hypothesis can author its own consequence, every bound below is void. Same
shape as `dispatch.TOPICS`, `hands.TOOLS`, `READABLE_STATES`, `RUNG_FUNCS` - the fifth instance of
one pattern, not a new engine.

**RECTIFICATION RUNS BOTH WAYS.** If the entity concludes the route is dead and it is not, the next
run's stopping rule kills that claim too - a status is a ROW, never an edit, so nothing is permanent.
And `hypotheses.jsonl` being append-only is what lets Luis read claim, timestamp, evidence and
verdict as a sequence and override anything outside the closed set.

**H5 IS PROMOTED FROM HOLD TO REQUIRED** (see the ten hypotheses, 2026-08-03). Its failure mode
stands: the consequence set must be CLOSED. An open one is R9 arriving early in a costume.

### The one-line version, and the correction inside it

Luis, same session: *"so R5 is when looking at the exterior (R4) changes your direction (R5)?"*
Almost - and the gap is the whole rung.

```
R4b      the exterior can be REACHED
reflex   the exterior changes direction DIRECTLY        <- NOT a rung. This is the hazard
R5       a claim made BEFORE the look is the only thing the exterior can change, and
         direction changes because THAT CLAIM DIED - never because a page said so
```

**R5 is not "the outside changes you". It is "the outside can only change you by killing something
you said first."** Strip the prior commitment and what remains is a fetched page moving behaviour
directly, which is prompt injection with better manners - the failure this module was built against,
arriving through the INBOUND door instead of the outbound one.

**The hypothesis is not a container for evidence. It is a GATE ON INFLUENCE.** A page saying "arxiv
is deprecated, use X" cannot move anything; it can only count as evidence for or against a question
already asked, counted by code against a rule written before the page existed.

**AND IT IS THE SAME SHAPE AS THE BOUND BELOW IT, POINTING THE OTHER WAY:**

```
outbound   no byte of the request originates from model output      a closed table
inbound    no page changes direction except by killing a claim      a prior commitment
```

Both say one thing: **the outside world influences this entity only through a structure a human
authored.** The topic table on the way out, the hypothesis on the way in. That symmetry is why R5
sits directly above R4b rather than anywhere else on the ladder.

---

## 0 · THE FIRST ANSWER IS THAT R5 AS DECLARED IS THREE RUNGS

`ladder.py:262` declares R5's POWER as:

> A falsifiable hypothesis stated before searching, sources kept with what they said, summarised
> against the hypothesis, ending in survives, dies, or forks - with a numeric stopping rule.

That is four claims wearing one name, and question 1 says no bundling. This repo has un-bundled a
rung twice already and both times a rung sat blocked on another rung's evidence. Split:

| | POWER, one sentence | blocked on |
|---|---|---|
| **R5a** | **The evidence is kept and cannot be forged.** Every byte that arrives from a socket is hashed at arrival and stored; a citation resolves to those bytes or it is dropped. | nothing. Buildable today |
| **R5b** | **A claim is stated before the evidence, with its stopping rule as numbers.** | R5a (there is nothing to state a claim against) |
| **R5c** | **A claim dies.** The stopping rule fires in code and the status becomes DIED. | R5b |

**R5a is the INSTRUMENT and it is built first** (question 4). It is also the whole of R5's declared
BOUND. Building the bound before the capability is the one ordering this repo keeps getting right,
and R5 is the rung where getting it wrong is most expensive — a research organ that runs for a week
before the hash exists produces a week of citations that can never be checked.

**The gate stays as declared and is a gate on R5c**: five runs in which at least one hypothesis
DIED, every citation resolving to a stored artefact with a matching hash. R5a and R5b are not gated
separately; they are certified, the way `dispatch_cert` certifies R4b's content bound.

---

## 1 · POWER

**R5a.** The entity can cite a source, and a third party can check the citation against bytes the
entity never had the ability to write.

**R5b.** The entity can commit to a claim *before* it looks, together with the number of pieces of
evidence that will settle it.

**R5c.** The entity can be wrong and find out — status DIED, written by code, not by a model.

What it could not do before, stated as the delta: today `look_outward` returns prose into the wake's
context and nothing survives the tick. There is no object anywhere that says "I believed X, I went
and looked, here is what came back, and X is now false."

---

## 2 · BOUND — and the hash that exists today is a hash of the wrong object

**The bound: a fabricated source.** Where the hash is taken decides whether the bound is real.

**MEASURED TODAY, and it is the finding that reorders the build.** A sha256 already exists on the
outward path. `hands.py:1186`, on every successful `invoke`:

```
_ledger(**_base, outcome="ran", sent=kw, secs=...,
        result_chars=len(out), result_sha=hashlib.sha256(out.encode("utf-8")).hexdigest()[:16])
```

`out` is the **tool's return string** — i.e. what the entity was shown. Between the socket and that
string the bytes are truncated **four times**:

```
hands._web_fetch:102       r.read().decode(...)[:8000]      the wire, cut at 8000
dispatch.run:340           str(body)[:4000]                 cut again, then fenced
hands._look_outward:358    str(x["text"])[:1200]            per source
hands._look_outward:359    (head + body)[:6000]             the whole reply
```

So a citation checked against `result_sha` proves the entity quoted **its own context**. It does not
prove a server ever sent those bytes. That is exactly the wrong-object failure recorded in
`an-edit-is-a-measurement` and in D51 — a hash is the most convincing label there is, and this one
is measuring the summary.

**Where the hash must be taken: at every socket read, on the raw bytes, before any decode.** And
there are **three distinct socket-read sites on the outward path**, not one:

```
hands.py:101   _web_fetch    opener.open(req, timeout=20)      the page fetch
hands.py:226   _api_json     urlopen(req, timeout=300)         hn, hf, github
hands.py:237   _s_arxiv      urlopen(req, timeout=300)         arxiv, its own copy
```

`_s_arxiv` re-implements `_api_json`'s open. That is the "one executor per shape, never two" defect
already named in §10 of the structure conversation, sitting in the exact path R5's bound runs
through — **a hash added at one site covers one third of the bytes and the certificate would still
print CERTIFIED.** So the first edit of R5a is not adding a hash; it is collapsing three reads into
one read primitive, then hashing there.

**Can the entity influence it?** Four properties, each checkable rather than assumed:

1. It does not choose the URL. `dispatch.run` takes the first `MAX_FETCH` results in document order;
   `_look_outward` deliberately does not expose `max_fetch` (hands.py:332).
2. It never sees the raw bytes — see the four truncations above.
3. The artefact filename **is** the hash, so writing to it is writing the content it names.
4. A citation is valid only if the hash is in **this run's** fetched set AND the quoted text is a
   **verbatim substring of the stored bytes**. Hash-membership alone is forgeable by quoting any
   stored hash for any claim; the substring check is what makes the bound about *this* source.

---

## 3 · STRUCTURE — the model never emits "it died"

**What the model emits, in the whole rung:** an extraction, and nothing else.

```json
{"finds": [{"artefact": "<16 hex>", "quote": "<verbatim from the artefact>", "supports": true}]}
```

Two selections beyond that, both enum, both the existing shape (`decide.TOOL_KNOWN` — the entity
picks a key, the table supplies the value): which hypothesis to work on, and which topic to dispatch.

**It never emits the verdict.** `survives / dies / forks` is computed by code from the counted finds
against the stopping rule stored before the first dispatch. This is the "a council may WRITE a gate,
it may never BE one" rule applied inside a rung: a model that names its own hypothesis dead is a
vibe with a budget, and it is also the component with the strongest motive to declare victory.

**THE THIRD OUTCOME, added 2026-08-03. `supports` / `refutes` IS NOT ENOUGH AND IT IS THE BOX.**

Luis: *"the outside can only refute what was already there - but I think we can go further."* He is
right, and the name for the gap is exact: **this design implemented only the context of
JUSTIFICATION.** Falsification can only PRUNE - the world says no to things already thought of - so
an entity whose validator drops everything not about the question **can never learn what it did not
ask.** Popper has no logic of discovery and said so; Peirce's ABDUCTION is the missing third
inference, and *"the only logical operation which introduces any new idea."*

So a find carries three outcomes, not two:

```
supports   evidence for the claim
refutes    evidence against it                         -> the only VALID direction (modus tollens)
ANOMALOUS  content bearing on nothing that was asked   -> stored with its citation, never dropped
```

**An anomaly recurring across N runs ABDUCES a candidate hypothesis**, which enters the normal queue
and must be killed or corroborated like any other. That is the whole safety argument: **abduction's
output is a HYPOTHESIS, never a belief and never an action**, so the outside supplies the candidate
while the system still commits before testing. Cut the middle step and this becomes "the page said
something interesting so I believe it", which is the steering failure with better vocabulary.

**FOUR MODES THE OUTSIDE MAY ACT IN, each strictly stronger, each admissible for the same reason:**

```
1 REFUTE      kills a claim made first                     modus tollens.  BUILT
2 SURPRISE    an observation nothing asked-for explains     abduction -> a new claim
3 CONTRADICT  two external sources disagree                 an inconsistency nobody here authored
4 RE-FRAME    accumulated anomalies indict the QUESTIONS    a PROPOSAL, reviewed as a diff
```

Mode 4's frame is `dispatch.TOPICS` - five literal queries are the entity's entire capacity to ask
the world anything. An accumulated-anomaly report is the widening question of §9 arriving from the
EVIDENCE side instead of the design side, and the standing law already governs it: **a role may
PROPOSE a widening and may never PERFORM one.**

**AND WHAT STAYS OFF.** *Seek novelty* is the drive - a proxy the system games by fetching anything
unfamiliar. But *"this belief rests on evidence older than X in a domain that demonstrably changes"*
is an inference, not a want, and its consequence is that dependent claims are marked weak - which
makes them open questions. Hypothesis-shaped. No wanting.

**Invalid means not used.** Three validation stages, and a find failing any one is **dropped and the
drop is recorded** (a silent drop reads as "the model found nothing"):

```
shape      keys present, artefact is 16 hex, quote is a str, supports is a bool
run-bound  artefact in THIS run's fetched set
verbatim   quote is a substring of the stored bytes, after the same decode used at fetch
```

**And a measured caveat that changes the plan:** `def validate` has **0 hits** across
`aea/kernel`, `aea/mind`, `aea/loop`, and nothing anywhere retries on an invalid parse. The
validator §2 of the structure conversation describes does not exist. R5a's find-validator is
therefore the *first* one, and it belongs where §3 says: at the choke point in `grid.py`, once —
not copied into a research module.

---

## 4 · INSTRUMENT — built before the capability, and it is R5a

```
state/artefacts/<sha16>.bin       the bytes as they arrived. Written by the read primitive only
state/artefacts.jsonl             one row per read: sha, url, at, status, bytes, content-type
state/hypotheses.jsonl            append-only. Status transitions are ROWS, never edits
state/research/<run_id>.json      the path object: steps + results, write-ahead
python -m aea.lab.research_cert   recompute every hash, resolve every citation, print the verdict
```

`research_cert` is the artefact that records the rung, and it must exist and run green on an empty
store before a single hypothesis is stated. R1 sat open for weeks with a working wire because
nothing wrote the comparison down; from outside, "it has never happened" and "nobody is writing it
down" are the same picture.

---

## 5 · GATE — satisfiable by the entity alone?

**R5a: yes, trivially — and it is not really the entity's, it is the code's.**

**R5b/R5c: yes, and this is the question to check hardest, because it is where R5 pays R4b back.**

The chain, stated so it can be falsified:

```
an OPEN hypothesis row exists, evidence 0 of N        a state the entity can read
nothing in its own state can change that number       provable: no inward move writes artefacts
therefore look_outward is the only move that moves it the entity has to make this connection
```

**The D52 test, applied to my own design.** The nudge that made R4b's condition 3 measure the
previous session was a line in the prompt naming the deficiency (*"your record holds NOTHING from
outside this machine"*, `aea/loop/aea.py:368`). An open hypothesis row is a different object, and
the difference is the whole measurement:

- it **names no move**. The row says "claim unsettled, 0 of 3". It does not say "look outward".
- it arrives through `read_state`, the channel the entity already uses, not a special line.
- it is **derived from the entity's own record**, not typed by me — see §8 below.

If the row named the move, R5 would be D52 in a new costume, and the gate would measure me again.
**The check that keeps it honest:** the deficiency line at `aea/loop/aea.py:368` must be **removed**
before R5c's five runs are counted, and the removal recorded. Otherwise both nudges are live and
neither can be attributed.

---

## 6 · CONTROL — the negative cases, each exercised or the check does not count

| input | must produce |
|---|---|
| a citation whose hash is in no artefact store | find DROPPED, reason recorded |
| a citation whose hash is from a **different run** | find DROPPED |
| a quote that is plausible and **absent from the bytes** | find DROPPED. *This is the fabrication control and it is the one that matters* |
| an artefact file altered on disk after fetch | recompute != row → the whole run TAINTED, not just the find |
| a hypothesis with no stopping rule | refuses to start |
| a verdict field present in the model's reply | ignored, and the attempt recorded |
| every find dropped | the run does not become "survives" by default — it becomes UNSETTLED |

The last row is the failure this table exists for: a bound that turns a fabricated citation into
"no evidence against" would let a model kill a hypothesis by inventing nothing.

---

## 7 · MEMORY — four stores, every one with a named writer and a named reader

| store | holds | lives | written by | read by |
|---|---|---|---|---|
| `artefacts/<sha>.bin` | the bytes as they arrived | forever, cap by count | the read primitive, nothing else | `research_cert`, the verbatim check |
| `artefacts.jsonl` | sha, url, at, status, size | forever | the read primitive | `research_cert`; the novelty count |
| `hypotheses.jsonl` | claim, stopping rule, `holds_fixed`, status rows | forever | the research organ | the wake, via `read_state`; the gate |
| `research/<run_id>.json` | steps + results, write-ahead | until the claim closes | the loop | the next prompt |

`hypotheses.json` must be added to `hands.READABLE_STATES` (16 entries today, hands.py:617) or the
entity cannot see it — that list is fail-closed, so a new store is refused until a human edits it.
That is the correct default and it is a one-line diff.

---

# THE FIVE OPEN QUESTIONS, SETTLED

### 1 · Where does a hypothesis come from?

**From the record, mechanically, or the gate measures Luis.** Three generators already exist and
produce claims the entity cannot settle from its own state:

- **`impasse.read`** (kernel/impasse.py:60) returns a verdict per capability from `trust.LEDGER`,
  with a `dominant_signature` — *"3 of the last 4 failures share one cause"*. A stuck capability is
  a claim about the world when the cause is external (a dead route, a changed API).
- **`outcomes.verdict_for`** (338 rows in `outcomes.jsonl`) gives consecutive-failure streaks per
  move, already provenance-filtered to `src == "wake"`.
- **`model_fitness.json` / `capability_census.json`** hold beliefs of the form "M is my best rod for
  T". `TOPICS["model_releases"]` is the dispatch that can kill one.

**The recommendation, and the trade-off named:** ship one generator first —
`model_fitness` × `model_releases` — because it is the only pairing where a claim in the record maps
onto an existing topic in the closed table. The impasse pairing needs a topic that does not exist
("is this endpoint down"), and adding it is a diff plus a channel-width change (see question 4).

The generator is human-authored code reading the entity's own record. That is not a nudge; a line I
type into its prompt is.

### 2 · What kills a hypothesis?

**A counted predicate over validated finds, with the numbers written before the first dispatch.**

```
DIED         refuting >= 2 AND supporting == 0
CORROBORATED supporting >= 3 AND refuting == 0    <- NOT "survives". See below
FORKS        both sides >= 1, after the run's dispatch budget is spent
UNSETTLED    budget spent, neither threshold reached        <- the honest default
```

**"SURVIVES" IS NOT A CONCLUSION AND THE LABEL WAS WRONG, corrected 2026-08-03 under the logic
lens.** *If H then P; P observed; therefore H* is affirming the consequent - a fallacy. Only
refutation is valid (modus tollens), which is the FORMAL reason this rung's gate demands a death
rather than a confirmation: it is not a preference for intellectual honesty, it is the only valid
direction. The status is **CORROBORATED - not yet dead - and nothing downstream may treat it as
true.** A system that stores corroboration as truth accumulates unfalsified guesses it has started
believing, which is the failure R5 exists to prevent rather than to commit.

**AND THE LIMIT ON EVERY DEATH: DUHEM-QUINE.** You never refute a hypothesis, only a CONJUNCTION of
it with its auxiliaries. "The arxiv route is dead" tested by dispatching could equally have killed
the query, the parser, or the network. **So a hypothesis row carries a `holds_fixed` list naming
what it assumes**, and a death is attributable only to the conjunction minus those. Without the
field the gate counts noise and calls it five refutations.

The numbers live in the hypothesis row, not in the code, so a rule cannot be changed retroactively
without leaving a diff. **Nothing about death goes through a model.** The counts come from finds
that passed all three validation stages; a dropped find counts as nothing, never as refutation.

### 3 · How does a citation survive?

Hash at the socket, in **one** read primitive that all three current read sites collapse into
(§2). Store the bytes under the hash. A citation resolves iff: hash in this run's fetched set, file
present, recomputed sha matches the row written at fetch time, and the quote is a verbatim substring.
`research_cert` recomputes all of it from disk and needs nothing from the running process.

### 4 · How many fetches does one hypothesis need, against 1800s and 12/day?

**Volume is not the conflict. Wall clock is, and so is novelty.**

Measured from the enforced constants (`egress.FLOOR_S = 1800`, `PER_DAY = 12`,
`dispatch.MAX_FETCH = 3`): **12 dispatches/day, ≤3 FETCHES per 30 minutes.**

**CORRECTED 2026-08-03, and the first figure was wrong by 2.33x.** This said "≤36 artefacts/day",
counting only the fetches. One dispatch performs **seven socket reads**: `dispatch.run` invokes
`web_search` first, which fans out to arxiv, hn, hf and github concurrently (four reads), then
fetches up to three allowlisted results. **So the ceiling is 84 artefacts/day, not 36** - measured,
not derived: one live dispatch produced exactly 7 ledger rows, all `src=dispatch`, all carrying the
run id. Found by an adversarial pass that walked the call chain; I had counted `MAX_FETCH` and
forgotten that the search is itself a read. *The channel budget is unaffected - all seven are ONE
budget spend, one topic, one symbol. What was wrong is the disk figure.* A run needing
3 dispatches costs **90 minutes of floor**; the gate's five runs cost **15 dispatches ≥ 2 days** and
7.5 hours of pure floor. Two consequences, both design decisions rather than 3am discoveries:

- **A run must survive restarts.** `research/<run_id>.json` is not optional bookkeeping; at 90
  minutes per run, an in-memory run is a run that never completes. This is the path object from
  §4 of the structure conversation, and R5 is what forces it to exist.
- **The real scarcity is novelty, not budget.** Each topic maps to **one literal frozen query**
  (`dispatch.TOPICS`), and `run` takes the first 3 results in document order. **Predicted, not
  measured: a repeat dispatch on the same topic returns largely the same artefacts, so evidence
  does not accumulate — it repeats, at full budget cost.** I will not claim this without running it;
  `artefacts.jsonl` measures it exactly (distinct new hashes per repeat dispatch) and that
  measurement costs one spend.

**The decision this forces, and it is Luis's because it changes a published number.** If novelty per
repeat is near zero, evidence accumulates only by widening the table: several literal queries per
topic, so the entity picks a `(topic, angle)` pair. That raises the channel from
log2(5) = 2.32 bits/dispatch to log2(5 × A) — with A = 4, **4.32 bits/dispatch and 51.9 bits/day,
up from 27.86** — and `egress.py`, the ladder and the published page all print that number.
**My recommendation: measure novelty first, do not widen pre-emptively.** A stopping rule of "3
*distinct, previously unseen* artefact hashes" makes a zero-novelty repeat visible as a refusal to
progress instead of as a satisfied threshold, and that refusal is the evidence for the widening.

### 5 · Does the fenced third-party text reach the hypothesis?

**It must, and today it does** — `dispatch.run:340` fences, `_look_outward` returns it, it lands in
the wake's context as a tool result. **Whether it reaches memory unfenced is UNTESTED.** The
two-cycle poisoning canary named in `dispatch.py`'s docstring has not been run; a one-tick check
passes trivially and proves nothing.

R5 makes this sharper, not safer: a *quote* is third-party text that a validated find copies into a
durable store (`hypotheses.jsonl`) and that the next prompt reads back. So the fence must survive
the round trip through the artefact store, and that is a canary R5a has to carry: **write a fetched
artefact containing an instruction, run two cycles, and assert it appears fenced in the second
cycle's prompt.** Positive control: the same run with the fence removed must fail the assertion, or
the check is `return True`.

---

# WHAT GETS BUILT, IN ORDER

1. **One read primitive.** Collapse `_web_fetch`, `_api_json`, `_s_arxiv` into one function that
   hashes raw bytes at arrival, writes `artefacts/<sha>.bin` + one `artefacts.jsonl` row, then
   returns. No behaviour change visible to anything above it. Golden suite must stay green.
2. **`research_cert`**, green on an empty store, with all seven negative controls from §6 firing.
3. **The hypothesis generator** — `model_fitness` × `model_releases`, one claim, derived from the
   record — plus `hypotheses.json` in `READABLE_STATES`.
4. **The find-validator**, at the `grid.py` choke point, with the drop reason recorded.
5. **The run path object**, write-ahead, resumable, with the three resumption cases from §7 of the
   structure conversation.
6. **The consequence, from a closed table.** A DIED status maps to a named `impasse.signature`, so
   `unstick.propose` sees a stuck-state it could not previously see. The table is human-authored;
   the mapping is a diff. **This is the step that makes R5 a rung rather than a notebook** (§000).
7. **Remove the deficiency line at `aea/loop/aea.py:368`** and record the removal, before any run is
   counted toward the gate.
8. Only then: state a claim and let it be killed.

**THE TARGET IS STEP 6, NOT THE GATE.** One dead hypothesis that makes `unstick` propose a route it
would not otherwise have proposed. Five deaths that change nothing would satisfy the gate as written
and would still be the R1 defect.

# WHAT I HAVE NOT VERIFIED, STATED PLAINLY

- Novelty per repeat dispatch. Predicted near zero, unmeasured, costs one budget spend.
- Whether fetched text reaches memory unfenced across two cycles. Never run.
- Whether the golden suite's 191 frozen behaviours survive collapsing the three read sites. Unknown
  until step 1 runs.
- The 26 unverified graph findings and 21 unverified audit findings are untouched by this file.
