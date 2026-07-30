# THE LOGIC AS IT ACTUALLY IS - read line by line, 2026-07-30

*Luis: "we need to deeply analyze how the logic is right now at the moment, everything. And then we
proceed with the final wiring."*

*This is that reading. Not the architecture as designed across 677,800 words - the code as it runs.*

---

## THE FINDING, IN ONE SENTENCE

> **There are two loops. One of them thinks and cannot act. The other acts and cannot think. They
> are not connected to each other, and neither of them has ever touched a tool.**

That is the whole wiring problem, and it is far smaller than "113 dormant modules".

---

## LOOP A - `aea/loop/aea.py`, "the wake". 134 lines.

What one `tick()` does, exactly:

```
1  sense()          fetch two HARDCODED urls: his github repos, and HN "AI agent" stories
2  build a prompt   the seed (who Luis is) + the last SIX memories + that world state
3  core()           ONE llm call. reasons in prose about what matters now
4  structure()      a SECOND llm call. turns the prose into
                    { matters_now, changed, ACTION, note_to_self }
5  remember         append note_to_self to state["memory"], append the rest to state["surfaced"]
6  hades.watch()    a watcher renders a verdict on the output
7  return
```

`main()` runs N ticks with `time.sleep(3)` between them and exits. It is not a daemon.

**IT DECIDES AN ACTION EVERY SINGLE TICK. THE ACTION IS A STRING. NOTHING READS IT.**

Verified: `surfaced` and `aea_state.json` appear nowhere else in the tree except a comment in
`shadow.py` and a privacy exclusion in `controlroom.py`. The entity's decision about what to do
today is written to a JSON file and printed to a terminal nobody is watching.

It is a deliberative organ with no motor pathway. It cannot even reach the two URLs it senses from
by choice - `sense()` is fixed.

---

## LOOP B - `aea/loop/live.py`, "the live loop". 327 lines.

This one genuinely runs, has a heartbeat, survives signals, and executes things. Its decision
function is 24 lines:

```python
def choose_action(hb) -> (name, argv, timeout):
    if today's brief is undone and not stuck:  return "AWAKE:brief",       [-m aea.organs.brief]
    if the corpus has unconsolidated items:    return "ASLEEP:consolidate", [-m aea.memory.consolidate]
    if reflect.py exists on disk:              return "REFLECT:self",       [-m aea.organs.reflect]
    return "IDLE", [], 0
```

**That is the entire action selection of the autonomous entity: an if/elif ladder over three
scripts, in fixed priority order.** No model is consulted. Nothing is weighed. The entity has no
say in what it does next.

To its credit it is a *good* if/elif ladder - the docstring records a real measured failure, where
a brief that failed for an external reason re-ran byte-identically forty-eight times a day and
starved every branch below it, with twelve identical trust-ledger entries as the receipt. That fix
is exactly right. It is still a ladder.

---

## THE TABLE

| | LOOP A · the wake | LOOP B · live |
|---|---|---|
| deliberates | **yes** - full reasoning about what matters | no - `if/elif` |
| acts | **no** - writes a string nobody reads | **yes** - runs one of 3 scripts |
| chooses what to sense | no - two fixed URLs | no |
| persists | memory across ticks | heartbeat |
| calls `hands.invoke` | **never** | **never** |
| runs unattended | no - N ticks then exits | **yes** |

**Neither loop has ever called a tool.** The nine gated tools - `calc`, `web_fetch`, `json_get`,
`read_state`, `web_search`, `self_map`, `list_tools`, `send_email`, `spend` - are reachable only
from `converse.py`, which is itself only reachable when a person types a command.

So the entity, running on its own: can think, can run three scripts, and **cannot look anything up,
cannot read its own state through its own hands, cannot send anything, cannot spend anything.**

---

## WHAT THIS MEANS FOR THE WIRING

The gap is not 113 modules. It is **one missing pathway and one hardcoded function**:

**WIRE 1 - the wake's decision must reach the live loop's hands.**
`choose_action` consults `aea_state.json` before falling through to its ladder. The ladder stays as
the floor - it is what the entity does when it has no better idea, which is the correct default and
already battle-tested. The deliberation stops being decoration the moment one branch reads it.

**WIRE 2 - the wake's `action` must be expressible as a tool call, not prose.**
Today it is a sentence. It has to be able to name one of nine tools and its arguments, validated
against `hands.schema()` before anything runs. That is the difference between an intention and an
instruction.

**WIRE 3 - `sense()` must be able to ask.**
Two hardcoded URLs is not perception, it is a fixed input. With `web_search` reachable, what the
entity looks at becomes something it decides - which is also the first half of the research organ
that does not exist.

Each of those three is a small function. Together they take the entity from *"produces an opinion
about what should happen"* to *"does one thing on purpose and writes down what happened"* - and
every one of the 113 dormant modules is behind that same door, because they are all invoked the
same way.

---

## THE HONEST CAUTION

The reason the wake was never wired is not laziness, and it should be said before it is wired.

`hands` includes `send_email` and `spend`. The moment loop A's decision can reach loop B's
execution, an unattended process that reasons freely about what matters can send mail and spend
money. Every containment mechanism this repo has - zones, the trust ledger, the announced URL, the
honesty guards, HADES watching each tick - was built for exactly that moment and **none of them has
ever been tested with a live wire behind it.**

Wire 1 and 2 should land with the tool allow-list restricted to the read-only five
(`calc`, `read_state`, `list_tools`, `self_map`, `web_search`) and `send_email`/`spend` left out
until the loop has run for a week and the ledger has been read.
