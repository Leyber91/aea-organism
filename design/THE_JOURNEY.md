# THE JOURNEY, the cumulative climb, in order of necessity

One table. Every row is **everything above it, plus one part.** Nothing is added because it belongs to a
group; each part is admitted only when the row beneath it has been shown to fail at something, and the
failure is named. That ordering is what the player walks, and recognising the climb is the game.

Read the WALL column as the thing the player runs into. Read the RECEIPT column as what was actually
measured, on stated fuel. Read the BEAT column as what the player *feels* at that row, the narrative is not
decoration here, it is the reason the row is legible at all. Where a receipt is missing the row says so.

---

## REVISION 2026-07-25, THREE COLLISIONS WITH THE PREVIOUS TABLE, NAMED BEFORE THEY ARE OVERWRITTEN

The previous version had ten rows and began at THE CALL. This one has thirteen and begins one step earlier.
Two truths never coexist in the docs, so each change is stated rather than absorbed:

1. **THE CONNECTION is now row 0.** The old table folded "something answers at all" into THE CALL. It is a
   separate rung with its own failure mode, and the failure is common: x10's reachability pre-pass found
   `pollinations/openai-fast` returning **402 Payment Required** two weeks after the census scored it 11, and
   `probe.py` found **8 of 9 silent plants dead, five of them for no reason but a missing key.** You can hold
   a key and have nothing answer.

2. **THE CONVERSATION is a new rung, and it was missing from EVERY ladder.** Not in this table, not in
   `THE_LINEAR_HIERARCHY.md`, not in the 86-item census, not in `state/modules.json`, while
   `aea/organs/converse.py` is **531 lines, built, and has held a real spoken conversation with a stranger**
   (D13). The fourth candidate found by building rather than auditing, and the largest: a whole rung.
   **Its wall was hiding in plain sight**, the hierarchy states L5's wall as *"the second exchange cannot know
   what the first concluded"*, which is the CONVERSATION wall, filed under THE CHECKPOINT. They are not the
   same: conversation state lives in the context window, rides on every call, and dies with the session;
   checkpoint state outlives the call and costs 50x. Filing them together made the journey skip a rung.

3. **THE CASCADE is now row 12.** L8 holds **21 census items, a quarter of the architecture**, and the old
   table stopped before it, so the journey could never be cumulative over the whole thing.

4. **THE FRAME AND THE READOUT ARE SWAPPED, the frame now comes first, and the data forced it.** The
   previous ordering put THE READOUT (free) above THE FRAME (+34 tokens), ordering by cost. But the
   placement rule is about what forces what, and x10 settles it: across 11 rods and 4 temperatures, replies
   containing visible work numbered **8 bare against 240 framed, thirty to one.** The readout added a pass
   in **12 framed cells and 2 bare ones**, and both bare cases were a reasoning rod thinking out loud at
   high temperature. **THE READOUT IS INERT UNTIL SOMETHING MAKES THE MODEL SHOW ITS WORK, and that
   something is the frame.** The canonical readout receipt was always a framed one: the groq-70b
   enumeration came out of x02, the fitted-frame experiment. So the story improves too, you spend 34
   tokens to make it show its working, and then the reading is free.

5. **The C-84 fork is RESOLVED, not deleted.** The old table cited `C-84` (substrate catalog + lineage) in
   RECALL while `THE_LINEAR_HIERARCHY.md` places it at L4, and `journey_check.py` flagged the two partitions
   disagreeing. It now sits in **row 7, THE LADDER**, because the argument decides it: a catalog of what
   other fuel exists is what makes reaching for a different rod possible, and that is row 7's whole content.
   Its use as lineage-memory further up is a *use*, not its first necessity. Recorded here rather than
   silently dropped, because a fork removed without a reason is a fork that comes back.

---

## THE TABLE

| # | you add | the wall that forces it | receipt (measured, on stated fuel) | cost | beat | state |
|---|---|---|---|---|---|---|
| 0 | **THE CONNECTION** | You hold a key and nothing answers. | 11 of 12 rods answered in x10's pre-pass; `pollinations` gave 402 two weeks after scoring 11. `probe.py`: 8 of 9 silent plants dead, **5 only for a missing key**; cerebras live at 0.38s. | 1 call | you are alone in the dark, and something answers. not a mind yet, a pulse. | **MEASURED** |
| 1 | **THE CALL** · C-01, C-62 | You have nothing else. The prompt is the only control and the reply the only artifact. | nemotron-550b answers 8/8 on all five bank tasks bare. llama-3.2-1b answers 8/8 on two of five. The floor is higher than anyone expects. | 1 call | it answers, fluently, and you have no way to know if it is right. | **MEASURED** |
| 2 | **THE MEASURE** · C-15, C-60 | You cannot tell whether it worked. The reply looks equally confident when wrong. | The scoring stage costs 0ms. Nothing else in the architecture is free, which is why this is admitted second. | 0 tok, 0ms | the first honest instrument. you stop trusting the tone. | **MEASURED** |
| 3 | **THE FRAME** · C-04, C-19, C-23 | It fails, and the prompt is the only lever you have left. | llama-3.2-3b 0/8 → 8/8 with a frame that names the METHOD. A posture frame pays on **1 rod of 11**. And the 550b goes **bare 1.00 → framed 0.25**, the frame *harms* a rod that did not need it. | +34 tok, **negative if misapplied** | the first tool that can hurt you. a part with an unmet precondition is not neutral. | **MEASURED** |
| 4 | **THE READOUT** · candidate C-87 | It did the work correctly and then told you the wrong answer. | groq-70b enumerates to 13 in 8/8 and reports 11: **0/8 → 8/8** at zero tokens. x10: converts 2 rods completely at **all four temperatures**, patches 3 more, spans 3 plants and 3 size tiers, and **cannot hurt**. | 0 tok, 0ms | the first betrayal, and the cheapest lesson in the game. read the work, never the claim. | **MEASURED** |
| 5 | **THE CONVERSATION** · candidate, unnumbered | You asked a follow-up and it had no idea what you were talking about. | `aea/organs/converse.py` runs: heard a stranger through a real mic, answered aloud in Castilian, and held the claim ceiling unprompted (D13). **UNMEASURED AS A RUNG, no experiment isolates its benefit.** | the transcript rides on every call; grows; **dies with the session** | the first relationship. it knows this conversation and nothing else, close the tab and you are strangers again. | **BUILT, UNMEASURED** |
| 6 | **THE CRITIC** · C-43, C-50, C-78 | It is confidently wrong and no amount of framing moves it. | nemotron-9b on the bat-and-ball trap: 0/8 → 5/8 with a separate judge. Only pays where the rod is genuinely wrong; on four of five rods there was nothing to repair. | 6.4x tok, +1 call | one voice cannot stand outside itself. | **MEASURED**, narrowed |
| 7 | **THE LADDER** · C-16, C-67, C-84 | This rod has a ceiling on this task, and a different rod does not. | gpt-oss-20b holds a 200-step chain where 550b scores 1/7 and groq-70b 0/8. x10: **a 70b and a 119b fail what a 9b does perfectly, size does not predict need.** x07: a rod predicts its own failure **0 of 12**. | +1 call, 8x latency | you cannot buy your way out. bigger is not better, and the ceiling is only visible from outside. | **MEASURED** |
| 8 | **THE CHECKPOINT** · C-80 | The chain is longer than one breath. It drifts inside the call, and no bigger rod fixes it. | nemotron-9b, chain of 50: carried state **11/11** vs one breath **9/16**, Fisher p=0.0216. Crosses fuel in both directions (x08). x08b: **the FORM decides what gets written**, canonical notes 81 chars and 1.00 per box; free-form up to 4801 chars of the rod's own deliberation, 0.52–0.71. | 50x calls, 4.5x wall | memory outside the breath, and the shape of the vessel decides what can be poured into it. | **MEASURED** |
| 9 | **RECALL** · C-02, C-13 | It cannot know what was never in the prompt, and the answer lives in something learned earlier. | 0/3 → 3/3 on a question the rod cannot know, embedding computed locally so zero cloud tokens. **n=3, one rod, owes a re-run at the current standard.** | +288 tok, +2 calls | it reaches for something you never said. | **WEAK** |
| 10 | **THE COUNCIL** · C-77, C-03 | One voice cannot disagree with itself, and a confident answer looks like a correct one. | x11: a mixed council **ties its best member at 5x the calls** (8/8 vs 8/8), a rod-selection problem, not a reach above the fuel. **Self-consistency quadruples the 9b: 1/8 → 4/8**, one rod voting with itself. Peer debate 6/8 → 8/8, nine minds changed. | N voices, waits for the slowest | the room disagrees. sometimes the room is right and nobody in it was. | **MEASURED**, claim 3 narrowed |
| 11 | **THE TICK** · C-76, C-64 | Everything above needs you to press go. | Not yet run. The final gate is sustained unattended operation, on a stated fuel. | continuous | you close the tab and it keeps going. | **PENDING** |
| 12 | **THE CASCADE** · C-21, C-31, +19 | It can run forever and still only ever do what it was built to do. | Not yet run. **21 census items, a quarter of the architecture.** | unbounded | it asks you for a part you never gave it. | **PENDING** |

---

## THE CHAIN, what each rung hands to the next

The table above says what each rung *is*. This one says why it cannot be moved. Every rung **produces**
something the rung above **consumes**; where the link has been measured, the evidence is named. Where it has
not, the row says so. That is the difference between an ordering and a claim.

| # | rung | it produces | the rung above consumes it because | link evidence |
|---|---|---|---|---|
| 0 | THE CONNECTION | a live endpoint, and a latency | you cannot call what does not answer, and the catalogue is not the connection | `pollinations` scored 11 in the census and returned **402** two weeks later; 5 plants dark for a missing key |
| 1 | THE CALL | a reply | a reply is not a result until something checks it | groq-70b returned the **same wrong number 6 times, distinct=1**, confidence carries no signal at all |
| 2 | THE MEASURE | a verdict you own: pass or fail | knowing it failed does not tell you *why*, and the why may be sitting in the reply | the measure says FAIL on llama3.1:8b; the reply's own work says 13 and its claim says 14 |
| 3 | THE FRAME | **a reply that shows its work**, and sometimes the answer outright | the readout has nothing to read until the work is visible | **8 bare replies contained work against 240 framed, 30:1** (x10, 11 rods, 4 temps) |
| 4 | THE READOUT | the answer taken from the work rather than the summary | when the work is right and the summary is wrong, no further prompting fixes it, you are past what one exchange can repair | llama-3.2-1b and llama3.1:8b: **frame alone 0/8, frame+readout 8/8**, at all four temperatures |
| 5 | THE CONVERSATION | continuity across exchanges, inside one session | a critic that cannot see the first answer is only a second stranger | **UNMEASURED**, the link is argued, not shown. This is the table's largest gap |
| 6 | THE CRITIC | a repaired answer, and a reason | you only reach for other fuel once a second look on *this* fuel has failed | 9b 0/8 → 5/8 with a judge; on 4 of 5 rods there was nothing to repair |
| 7 | THE LADDER | a rod chosen by measurement, and the calibration table behind it | a checkpoint that does not record *which* rod wrote each revision cannot answer whether it is one self | a 70b and a 119b fail what a 9b passes; a rod predicts its own failure **0 of 12** |
| 8 | THE CHECKPOINT | state that outlives the call, stamped with its fuel trail | recall needs a store to retrieve *from*; nothing below accumulates | 11/11 vs 9/16, **p=0.0216**; the checkpoint crossed fuel in both directions |
| 9 | RECALL | what was never in the prompt | each voice in a council must arrive carrying context, or the council is five strangers guessing | **WEAK**, n=3, one rod |
| 10 | THE COUNCIL | a verdict out of disagreement | an unattended loop must decide without you, and deciding requires a way to settle a split | a mixed council **ties its best member at 5x cost**; one rod voting with itself went **1/8 → 4/8** |
| 11 | THE TICK | time you are not present for | proposing a new capability requires having run long enough to notice a pattern | **NOT RUN** |
| 12 | THE CASCADE | a request for a part nobody gave it | — the top of the ladder | **NOT RUN**, 21 census items |

**Two links are load-bearing and unproven.** Row 5 → 6 is argued from first principles and has no experiment
behind it, and row 9 rests on n=3. Every link below row 5 has a receipt; the chain is only as strong as
those two.

**One link is measured as a *mutual* dependency rather than a sequence.** Rows 3 and 4 do not merely follow
one another, on llama-3.2-1b and llama3.1:8b **neither converts the failure alone and together they convert
it completely, at every temperature tested.** The frame makes the work visible; the readout takes the answer
out of it. That is the first place on the path where the player must hold two parts at once, and it is the
clearest teaching moment the measurements have produced.

---

## THE FOUR MOVEMENTS, the line through the rows

The rows are not a flat list; walked in order they make an arc, and the arc is the game.

| rows | movement | what changes in the player |
|---|---|---|
| 0–2 | **CONTACT** | something answers, and you build the one instrument that tells you whether to believe it. |
| 3–4 | **DISILLUSION** | it did the work and misreported it. you stop trusting fluency, and you get a tool that can hurt. |
| 5–7 | **THE LIMITS** | it forgets you between breaths, it is confidently wrong, and it has a ceiling you cannot buy past. |
| 8–9 | **MEMORY** | state outlives the breath, and it reaches for what you never said. |
| 10–12 | **AUTONOMY** | more than one voice, then time without you, then it asks for its own next part. |

**Where the price sits.** Rows 2 and 3 are free, 0 tokens, 0ms. Row 4 is the last cheap one, and the first
that can go negative. After that every gain costs a call: +1, 6.4x, 8x latency, 50x calls. A construct that
needs fifty calls to beat one is worth building only where one call cannot win.

**Where the drama sits.** Row 3 is the first betrayal and it is *free to fix*, the cheapest lesson in the
game teaches the honesty law as a mechanic. Row 4 is the first tool that damages you when misapplied. Row 5
is the first thing that feels like a relationship, and it is the first that *dies*. Those three rows are the
emotional spine, and two of them are not in the game today.

---

## THE FINDING THAT CHANGES HOW THE TABLE IS READ

The rows are not a staircase every construct climbs. **Which row you need is a function of which rod you
hold**, and x10 measured it across eleven rods, four temperatures and three plants:

| rod | what it needs on wordcount / the chain |
|---|---|
| gpt-oss-20b, nemotron-super-120b | nothing, they pass bare |
| granite4.1:8b, llama-3.2-3b, mistral-119b, **groq-70b** | row 4, THE FRAME, 0.00 → 1.00 |
| **llama-3.2-1b, llama3.1:8b** | rows 3 **and** 4, the frame produces correct work and the rod misreports it; neither part alone converts it |
| nemotron-9b | row 8, THE CHECKPOINT, 56% → 100% |
| **nemotron-550b** | row 4 would *damage* it, 1.00 bare → 0.25 framed |

So the climb is a **diagnosis rather than a collection**. The player reads what a rod is failing at and fits
the part that answers that failure. Two players holding different fuel walk different routes up the same
table, and both routes are correct. **And a wrong part actively breaks the run.**

---

## WHAT IS STILL OWED

**Row 5 has no experiment at all**, conversation is built and never isolated as a rung. That is now the
largest evidence gap in the table, and it sits at the emotional centre of the arc.
**Row 9** rests on n=3 from a single rod. **Rows 11 and 12** have not been run, and row 12 is a quarter of
the architecture. Row 6 is measured but narrower than chapter I claimed. Row 10's claim 3 survives only in
the narrow form: a council does not reach above its best member, but a rod voting with *itself* gains.

The table is published with those gaps visible because the gaps are the remaining route.
