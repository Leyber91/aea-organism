# PROMPT FOR THE NEXT SESSION

*Paste the block below as the first message. Everything after it explains why it is written that way,
and is for a human, not for the prompt.*

---

```
Read these four files before doing anything, in this order:

  diary/HANDOFF_2026-07-28.md   the whole of the last session: what was built, what
                                every failure taught, what is pending with a verdict
  design/THE_LAWS.md            43 laws, each paid for by a real failure. They bind you.
  design/E12_BOARD_SPEC.md      the design specification. Every value resolved, no ranges.
  diary/OPEN_LOOPS.md           the work, each item carrying FINISH / LATER / KILL

Then run `python -m aea.tooling.selfcheck` and `python -m aea.tooling.xray` so you are
looking at the live state rather than at the handoff's description of it. The handoff is
a point-in-time record; the code is the truth.

THE TWO JOBS, in order.

FIRST: the interface does not read as an instrument. Luis's verdict, verbatim: "It doesn't
read JARVIS. Not futuristic, no live vibes. It's just very plain. And you need to make it
readable." Sections 4 (atmosphere: grain, vignette, glow, depth cueing) and 6 (the full
12-column layout at 1700x1000, which solves the dead space) of E12_BOARD_SPEC.md are
UNIMPLEMENTED. That is where the gap is. Implement the spec in the order its section 8
gives, screenshot after each change, and READ the PNG before claiming anything. The spec
exists because taste already failed twice; follow its numbers rather than your judgement.

SECOND: 88 of 110 modules cannot be reached by any wake. hands, seats, fit, goals,
crystal, shadow, laws, xray, selfcheck and heal are all built, tested and connected to
nothing. Wire them into aea/loop/live.py the way impasse and unstick now are. An entity
whose kernel is orphaned is a library, not an entity.

HOW TO WORK HERE.

Be a filter, not a mirror. Name failure points before validating strengths. Disagreement
is wanted and only counts when you bring a measurement; contrarianism without evidence
should be discounted, and Luis will discount it.

Verify, do not claim. "Done" means it ran: the server returned 200, the screenshot was
read, the test printed. Report failures with the output.

Measure before you believe. If something looks 100x better, prove it, then go. The word
"know" has to mean measured. Every false finding this project has produced came from its
own instrument, not from a model behaving unexpectedly.

No emoji anywhere. No em dashes, ever, in chat or code or docs; use a comma, a colon, or
two sentences. No negative parallelism ("it's not X, it's Y"). These are recorded rules
that were broken twice in the last session; scan your drafts before sending.

Nothing is committed until Luis asks. Privacy-scan first: no keys, no absolute paths, no
employer strings. The sacred save state/journey_save.json is never touched.

Kill the listener PID before restarting controlroom.py or route edits will not load.
```

---

## HOW TO INTERPRET THE HANDOFF (for the human)

**It is a record, not a specification.** Section 1's status column will be stale the moment anything
is wired in. Run `xray` first; if its numbers disagree with the handoff, the handoff is wrong.

**Section 3 is the load-bearing part.** The laws are not style preferences. Each one has a failure
attached and the failure is the argument. If a new session proposes something that violates one,
the correct response is to point at the cost that was paid, not to re-litigate.

**Section 5 is the open wound.** It contains measured numbers (ΔL\* below the JND, 2.5% ink coverage,
twelve font sizes at unreadable ratios) that explain *mechanically* why the board feels flat. Anyone
who tries to fix it by taste will fail the same way twice. The spec is the answer; it exists because
taste already lost.

**Section 7 is there so the next session does not have to relearn how to talk to you.** It is the
part most likely to be skipped and the part that costs the most when it is.

**The order of the <REDACTED-CIRCUMSTANCE> is deliberate and arguable.** The interface is first because it is what
Luis actually asked for last and because the board is how the next session will see its own progress.
The wiring is second because it is larger. If the next session wants to invert them, that is a
reasonable call, and it should say so out loud rather than drift into the easier one — which is
exactly what happened last session, where nine modules got built and none got connected.
