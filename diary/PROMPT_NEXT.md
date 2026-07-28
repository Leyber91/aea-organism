# PROMPT FOR THE NEXT SESSION

*Paste the block below as the first message. Everything after it is for a human, not for the prompt.*

---

```
Read these before doing anything, in this order:

  diary/HANDOFF_2026-07-29.md   the last session: eleven instrument defects, what every rod
                                actually does, the dev/qa/prod ladder, what is still unwired
  design/THE_LAWS.md            43 laws, each paid for by a real failure. They bind you.
  diary/DISCOVERIES.md          D18 is the one that governs this session
  diary/OPEN_LOOPS.md           every open item carries FINISH / LATER / KILL

Then run these so you are looking at the live state rather than at a description of it:

  python -m aea.tooling.selfcheck
  python -m aea.tooling.xray
  python -m aea.energy.rodprobe --show

THE RULE THAT GOVERNS THIS SESSION, and it was measured rather than argued: THE INSTRUMENT IS
WRONG MORE OFTEN THAN THE MODEL. Eleven instrument defects in one session against almost no
model behaving unexpectedly, and six of the eleven were in code written to CHECK something.
Before believing any finding, ask what would have to be true of the INSTRUMENT for it to be
false, and test that first. Every one of the eleven was caught by pointing the tool at a case
whose answer was already known. A detector that has never been shown a positive it must catch
has not been tested, it has only been run.

THE JOB: OUTBOUND CAPABILITIES. An autonomous entity that cannot reach the world cannot help
anyone. In priority order, and Luis set this order:

1 INTERNET. hands.web_fetch and json_get exist, are permission-gated at the call site, and are
  now reachable from the wake through brief. Extend from two hardcoded fetches to real search.
  Law B3: a read tool IS an outbound channel the moment the model writes the address.
2 VOICE. aea/organs/converse.py is 531 lines, verified running end to end: the mind answers in
  1.49s and VOICE synthesis is the bottleneck at 14.7s of a 16.2s turn. It is unwired. Audio
  never leaves the machine; only transcript text does.
3 RAG. Retrieval over design/ (3.4 MB, 196 files), NOT over code where the AST is exact. Six
  hosted embedders are measured and working; nemotron-3-embed-1b is best (2048 dims, margin
  0.528, 0.6s). But ZONES permits `local` only in the sensitive zone, so anything private needs
  a local embedder. torch is installed CPU-only; a CUDA build is a decision, not a default.

BEFORE ANY OF IT, three things that are cheap and that everything else rests on:
  - fix the discriminator's INPUTS before wiring kernel/fit.py (421 lines). The tool-calling
    census undercounts and 59 of 86 model cards are unread. Wiring fit on bad data makes bad
    selection authoritative.
  - re-read those 59 cards across SIX ROTATED READERS. One reader at eight workers destroyed
    the last run with 429s.
  - decide the outbound boundary deliberately. send_outbound and spend_money are FORBIDDEN with
    no implementation at all.

HOW TO WORK HERE.

Be a filter, not a mirror. Name failure points before validating strengths. Disagreement is
wanted and only counts with a measurement; contrarianism without evidence gets discounted.

Verify, do not claim. "Done" means it RAN: the gate returned 5 green checks, the screenshot was
read, the test printed. Report failures with the output.

At the SECOND repetition, extract it. Sixteen throwaway probes in one session were fifteen
copies of one module; aea/energy/rodprobe.py is now that module, so use it.

Never test a regex or a path through a shell heredoc. The Bash tool eats backslashes and it
made the same diagnosis wrong twice. Write it to a real file and run the file.

"No timeout" means a generous INACTIVITY budget (rodprobe.IDLE = 300s), never timeout=None.
None hung two experiments for 28 and 64 minutes on one second of CPU each.

Drop to the primitive when a tool fails on a source. WebFetch times out on build.nvidia.com;
a plain urllib GET with a browser User-Agent returns 200 and the whole page.

No emoji anywhere. No em dashes, ever, in chat or code or docs. No negative parallelism
("it's not X, it's Y"). These are recorded rules that keep getting broken; scan before sending.

Nothing is committed until Luis asks. Privacy-scan first. state/journey_save.json is sacred.
Known-good is 44525f3 - roll back to that, never to "the last commit".
```

---

## HOW TO INTERPRET THE HANDOFF (for the human)

**Section 1 is the load-bearing part.** Eleven instrument defects in a table. If a new session
proposes trusting a stored number, that table is the argument for re-measuring it first.

**Section 2 is the only place the rod facts are written down in prose.** The machine-readable
version is `state/rods.json` via `rodprobe.facts(rod)`, and it wins on conflict.

**Section 3 is what Luis authorised.** dev/qa/prod with declared blind spots. The important detail
is that a proposal cannot edit its own judge and there is deliberately no `promote()`. If a future
session wants to add one, that is a conversation with Luis, never a refactor.

**The critique in section 6 is the part most likely to be skipped.** In particular: a model squad
approving its own proposals is not independence, and x11 already measured that councils tie their
best member at 5x the cost. Models propose. The gate approves.

**What is deliberately NOT in the next session:** the board's visual work (E12 sections 4 and 6),
wiring the remaining 30 unwired modules, and the 43 unmeasured models. All real, all deferred by
Luis in favour of outbound capability.
