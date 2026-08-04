"""sensors.py - THE SIGNALS NOTHING ELSE COMPUTES, AND WHAT EACH ONE CANNOT SEE.

    python -m aea.tooling.sensors            every derived signal, once
    python -m aea.tooling.sensors --json     the same, as data

WHY THIS EXISTS. Luis, 2026-08-03: *"if you cannot see what's happening, it means that you need to
establish another checkpoint to actually measure everything that is going on... discovering that you
need more data sensors is okay."*

THE FAILURE THAT PROVED HIM RIGHT, measured the same hour. Ticks 535-540 chose
`what_to_try bad_response` SIX TIMES RUNNING. Every existing instrument read healthy:

    impasse       watches CAPABILITIES for failures - none of these failed
    outcomes      recorded `ok` six times, correctly
    R1            counted each as the wake differing from the fallback - it did
    the ledger    recorded the tool ran and returned in 0.01s - it did

A loop producing nothing was FEEDING the rung that measures deliberation, and the only reason it
was noticed is that a human read six log lines in a row and recognised a word. That is not a
measurement, it is an accident, and the next one will not be noticed.

THE SHAPE OF WHAT IS MISSING, and it is one thing at one altitude - the same one the handoff names
as open on the tool side:

    did the call COMPLETE          measured (hands ledger, `outcome`)
    is the CAPABILITY failing      measured (impasse, over the trust ledger)
    DID IT DO ITS JOB              NOT MEASURED - and every gap here lives at this altitude

A tool that returns a captcha page reads `ran`. A move that returns a cached answer reads `ok`. A
mind that reaches the same conclusion six times reads as six healthy decisions. In all three the
call completed and the capability is fine and nothing moved.

WHAT EACH SENSOR CANNOT SEE IS PRINTED BESIDE IT. A sensor whose blind spot is undeclared is the
next thing to be trusted for something it never measured, which is D51 in one sentence.
"""
from __future__ import annotations

import collections
import json
import os
import sys
import time

from aea.kernel import grid


def _rows(name: str, limit: int = None) -> tuple:
    """(rows, why-not). Absent, unreadable and empty are three different facts."""
    p = os.path.join(grid.STATE, name)
    if not os.path.exists(p):
        return [], "%s does not exist" % name
    out = []
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    except Exception as e:
        return [], "%s unreadable (%s)" % (name, type(e).__name__)
    if limit:
        out = out[-limit:]
    return out, ("" if out else "%s is empty" % name)


def move_runs(window: int = 40) -> dict:
    """REPETITION IN THE DECISION STREAM. The signal that had no sensor.

    CANNOT SEE: whether a repeated move is WRONG. Repeating `read_state` while genuinely working
    through different files is healthy; repeating `what_to_try` against one unchanged situation is
    not. This reports the run length and the variety, and judging them is a separate question that
    needs the outcome dimension below."""
    # THE MIND'S OWN STREAM FIRST, BECAUSE IT CARRIES THE ARGUMENT.
    #
    # THE DEFECT, found by watching it fail twice within ten ticks. This read `r1_decisions.jsonl`,
    # which records the BODY's view of the decision - `LOOK:read_state`, `AWAKE:brief` - with the
    # argument stripped. So it could not tell these apart:
    #
    #     read_your_state ladder.json  ->  read_your_state grid_state.json     working through state
    #     read_your_state ladder.json  ->  read_your_state ladder.json         the repetition pattern
    #
    # Both read `LOOK:read_state x2`. It reported healthy investigation as a streak, and then
    # reported a real consecutive repeat of ladder.json as `AWAKE:brief x1 in a row` - wrong in
    # both directions, which is the signature of measuring the wrong object rather than measuring
    # badly.
    #
    # `state["moves"]` is the mind's own list, move AND argument, written at commit. It was added
    # the same morning and read by nothing - a store with a writer and no reader, which is the R1
    # defect, reintroduced by the author who had just written that sentence into a docstring.
    #
    # The body stream stays as the fallback: it is longer-lived (400 rows against 40) so it still
    # carries the historical `longest_ever`, and if the mind has not ticked since the field was
    # added there is something rather than nothing.
    src = "state.moves (mind, with argument)"
    moves = []
    try:
        st = json.load(open(os.path.join(grid.STATE, "aea_state.json"),
                            encoding="utf-8", errors="replace"))
        moves = [str(m) for m in (st.get("moves") or [])]
    except Exception:
        moves = []
    rows, why = _rows("r1_decisions.jsonl", 400)
    body_moves = [str(r.get("wake") or "") for r in rows if r.get("wake")]
    if not moves:
        src, moves = "r1_decisions (body, argument stripped)", body_moves
    if not moves:
        return dict(ok=False, why=why or "no decisions recorded in either stream", streak=0)
    tail = moves[-window:]
    streak, last = 0, moves[-1]
    for m in reversed(moves):
        if m != last:
            break
        streak += 1
    longest, run, prev = 0, 0, None
    for m in moves:
        run = run + 1 if m == prev else 1
        prev = m
        longest = max(longest, run)
    # `longest_ever` comes from the BODY stream when it is longer, because `state["moves"]` is
    # capped at 40 and the historical record lives in r1_decisions. Reported with its source so a
    # reader can never mistake a 40-entry window for the whole history.
    b_longest, b_run, b_prev = 0, 0, None
    for m in body_moves:
        b_run = b_run + 1 if m == b_prev else 1
        b_prev = m
        b_longest = max(b_longest, b_run)
    return dict(ok=True, why="", source=src, current_move=last, streak=streak,
                longest_ever=max(longest, b_longest),
                longest_in_this_stream=longest, body_stream_longest=b_longest,
                distinct_in_window=len(set(tail)), window=len(tail),
                spread={k: v for k, v in collections.Counter(tail).most_common(6)},
                repeating=bool(streak >= 3),
                note=("the same move %d times running" % streak) if streak >= 3 else "")


def prompt_identity(window: int = 20) -> dict:
    """IS THE MIND SEEING THE SAME WORLD EACH TICK? `sensed.jsonl` stores a prompt sha per tick.

    A mind fed a byte-identical prompt has no way to reach a different conclusion, so an identical
    move is not stubbornness - it is arithmetic. This separates those two explanations, and until
    now nothing did.

    CANNOT SEE: whether a CHANGED prompt changed in a way that matters. Two prompts differing only
    in a timestamp hash differently and are the same situation."""
    rows, why = _rows("sensed.jsonl", 400)
    shas = [r.get("prompt_sha") for r in rows if r.get("prompt_sha")]
    if not shas:
        return dict(ok=False, why=why or "no prompt_sha recorded")
    tail = shas[-window:]
    c = collections.Counter(tail)
    top, n = c.most_common(1)[0]
    return dict(ok=True, why="", window=len(tail), distinct=len(c),
                most_repeated=n, all_identical=bool(len(c) == 1),
                note=("%d of the last %d prompts were byte-identical" % (n, len(tail))
                      if n > 1 else "every recent prompt differed"))


def outward_experiment(since_iso: str = "2026-08-03 08:47:00 UTC") -> dict:
    """CLOSED 2026-08-04 - see the wrapper below. The original docstring follows."""
    d = _closed_or_none()
    if d is not None:
        return d
    return _outward_experiment_live(since_iso)


def _closed_or_none():
    """A closed experiment returns its RECORDED result, not a fresh recomputation.

    It froze at 6 outward for fifteen consecutive checks while decisions climbed 131 to 142, and it
    was read out every five minutes as though it were live. A counter that cannot change its answer
    is reporting history, and a panel that recomputes settled history invites it to be read as news -
    which is the same defect as a docstring that outlives its function, in the other direction."""
    import os as _os
    p = _os.path.join(grid.STATE, "outward_experiment_closed.json")
    if not _os.path.exists(p):
        return None
    try:
        doc = grid.load_json(p, {}) or {}
    except Exception:
        return None
    f = dict(doc.get("final") or {})
    f["closed"] = doc.get("closed")
    f["verdict"] = "CLOSED %s - %s" % (str(doc.get("closed"))[:10], str(doc.get("result"))[:150])
    return f


def _outward_experiment_live(since_iso: str = "2026-08-03 08:47:00 UTC") -> dict:
    """THE EXPERIMENT COUNTER, and it was being kept by hand in a chat window.

    The claim R5 rests on: the entity will not choose to look outside until it holds a question it
    cannot settle from its own state. The nudge line that made `look_outward` reachable was removed
    2026-08-03; every decision after that is unprompted evidence. This counts them.

    CANNOT SEE: whether a decision was GENUINELY unprompted. It trusts the removal timestamp. If
    another line in the prompt is doing the nudge's job, this counter cannot tell - which is why
    `prompt_identity` and the surviving budget line are reported beside it rather than hidden."""
    try:
        cut = time.mktime(time.strptime(since_iso, "%Y-%m-%d %H:%M:%S UTC")) - time.timezone
    except Exception:
        return dict(ok=False, why="could not parse the cutoff %r" % since_iso)
    dec, _ = _rows("r1_decisions.jsonl")
    after = [r for r in dec if float(r.get("at") or 0) >= cut]
    lo = [r for r in after if "look_outward" in str(r.get("wake") or "")]
    hands, _ = _rows("hands_ledger.jsonl")
    counted = [r for r in hands
               if r.get("tool") == "look_outward" and r.get("src") == "wake"
               and r.get("outcome") == "ran" and float(r.get("at") or 0) >= cut]
    n = len(after)

    # THE VERDICT IS A PROBABILITY, NOT A PRONOUNCEMENT - and the first version pronounced.
    #
    # THE DEFECT, caught the moment it fired 2026-08-03. The cutoff was `n < 20`, chosen by feel,
    # and at n=20 with zero looks it printed "R5 is required". That claim does not survive its own
    # arithmetic: the measured base rate of `look_outward` is 2 in 228 wake decisions = 0.88%, so
    # under the NULL hypothesis that nothing changed,
    #
    #     P(zero in 20)  = 0.9912^20  = 0.84     <- the observation is unsurprising either way
    #     P(zero in 100) = 0.9912^100 = 0.41
    #     P(zero in 300) = 0.9912^300 = 0.07     <- only here does a zero carry information
    #
    # So a threshold of 20 converts noise into a conclusion, which is exactly what this sensor was
    # built to stop me doing by hand. It now reports the probability beside the count and refuses to
    # use the word "required" until that probability is small.
    #
    # THE BASE RATE IS ITSELF SOFT: those 2 look_outward choices happened WITH the nudge in the
    # prompt, so it is an upper bound on the unprompted rate rather than an estimate of it. Stated
    # because a null built from contaminated data is a null that flatters whoever chose it.
    BASE_RATE = 2.0 / 228.0
    p_null = (1.0 - BASE_RATE) ** n if n else 1.0
    if lo:
        verdict = ("%d outward looks in %d decisions - it does NOT need R5 to choose this"
                   % (len(lo), n))
    elif p_null > 0.25:
        verdict = ("zero in %d - but P(zero | rate unchanged) = %.2f, so this says NOTHING yet "
                   "(need ~300)" % (n, p_null))
    elif p_null > 0.10:
        verdict = ("zero in %d - P(zero | rate unchanged) = %.2f. Suggestive, not conclusive"
                   % (n, p_null))
    else:
        verdict = ("ZERO outward looks in %d unprompted decisions, P = %.3f under the unchanged "
                   "rate - R5 is required" % (n, p_null))
    return dict(ok=True, why="", since=since_iso, decisions=n, outward_chosen=len(lo),
                dispatches_that_ran=len(counted), p_null=round(p_null, 4),
                base_rate=round(BASE_RATE, 5), verdict=verdict)


def tool_outcomes(window: int = 200) -> dict:
    """DID THE TOOL DO ITS JOB - the altitude between `ran` and `the capability is failing`.

    `hands.invoke` records `ran` whenever an implementation returns a string. `web_search` returning
    "NO RESULTS from any route" is a string. So a dead route reads as a successful call, which is
    exactly how it stayed dead for weeks with every capability reporting `working`.

    This looks at what came BACK, not at whether the call completed. The markers are the ones the
    tools themselves emit, so this reads their own vocabulary rather than guessing at meaning.

    CANNOT SEE: a tool that returns a plausible WRONG answer. Nothing here can - that needs a
    reference to compare against, which is what R5's artefact store is for."""
    rows, why = _rows("hands_ledger.jsonl", 4000)
    if not rows:
        return dict(ok=False, why=why or "no ledger rows")
    tail = rows[-window:]

    # THE FIRST VERSION OF THIS SENSOR WAS BLIND, and it is worth leaving the reason in place.
    #
    # It looked for phrases like "no results" in the row's REASON field - which `hands._ledger`
    # only writes on a refusal or a raise. A successful-but-empty call leaves that field blank, so
    # the sensor reported `barren 0` for every tool including `web_search`, which is the exact
    # capability whose weeks-long silence motivated this whole altitude. A sensor that reads a
    # field the phenomenon never writes to is `return True` wearing a number.
    #
    # WHAT THE LEDGER ACTUALLY HAS: `result_chars`, written on every successful invoke. A
    # `web_search` with real hits runs to thousands of characters; "NO RESULTS from any route
    # (arxiv:0, hn:0...)" is about a hundred. So SIZE is the observable, and the threshold is per
    # tool because "short" means different things to `calc` and to a page fetch.
    #
    # STILL A FLOOR, NOT A RATE. A tool returning a long, confident, WRONG answer is invisible
    # here and to everything else in this repo - that needs an external reference to compare
    # against, which is precisely what R5's artefact store is being built to provide.
    FLOOR = {"web_search": 400, "web_fetch": 400, "look_outward": 400, "json_get": 1,
             "read_state": 60, "self_map": 60, "my_record": 40, "what_to_try": 40,
             "list_tools": 60, "calc": 1}
    DEFAULT_FLOOR = 20
    per = collections.defaultdict(lambda: dict(calls=0, ran=0, barren=0, raised=0, refused=0,
                                               unmeasured=0))
    for r in tail:
        name = str(r.get("tool") or "?")
        t = per[name]
        t["calls"] += 1
        oc = str(r.get("outcome") or "")
        if oc == "ran":
            t["ran"] += 1
            n = r.get("result_chars")
            if not isinstance(n, (int, float)):
                # A ROW WITHOUT A LENGTH IS NOT A HEALTHY ROW, it is one this sensor cannot judge.
                # Counted separately so "no barren calls" can never mean "no rows carried the field".
                t["unmeasured"] += 1
            elif n < FLOOR.get(name, DEFAULT_FLOOR):
                t["barren"] += 1
        elif oc == "raised":
            t["raised"] += 1
        elif oc == "refused":
            t["refused"] += 1
    out = []
    for name, t in sorted(per.items(), key=lambda kv: -kv[1]["calls"]):
        judged = t["ran"] - t["unmeasured"]
        out.append(dict(tool=name, **t, floor=FLOOR.get(name, DEFAULT_FLOOR),
                        barren_rate=(round(100.0 * t["barren"] / judged, 1) if judged else None)))
    return dict(ok=True, why="", window=len(tail), tools=out,
                note="`barren` = completed and returned less than this tool's floor in characters. "
                     "`unmeasured` = the row carried no result_chars, so it could not be judged - "
                     "reported rather than counted as healthy. A long WRONG answer is invisible "
                     "here and needs an external reference (R5).")


def deliberation_cost(window: int = 12) -> dict:
    """WHAT THE MIND IS SPENDING TO REACH ITS CONCLUSIONS.

    Rising latency against an unchanged move is the signature of a mind working harder to arrive
    at the same place - which no other instrument reports.

    CANNOT SEE: the reasoning itself. Only `wake.log` holds that, and only as prose."""
    p = os.path.join(grid.STATE, "wake.log")
    if not os.path.exists(p):
        return dict(ok=False, why="state/wake.log does not exist")
    import re
    secs = []
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.search(r"^--- TICK (\d+)\s+\(core: (.+?), ([\d.]+)s\) ---", line)
                if m:
                    secs.append((int(m.group(1)), m.group(2), float(m.group(3))))
    except Exception as e:
        return dict(ok=False, why="wake.log unreadable (%s)" % type(e).__name__)
    if not secs:
        return dict(ok=False, why="no completed ticks in wake.log yet")
    tail = secs[-window:]
    vals = [s for _, _, s in tail]
    return dict(ok=True, why="", ticks=len(tail),
                last=tail[-1][2], mean=round(sum(vals) / len(vals), 1),
                min=min(vals), max=max(vals),
                rod=tail[-1][1],
                recent=[dict(tick=t, secs=s) for t, _, s in tail[-6:]])


def all_signals() -> dict:
    return dict(at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                move_runs=move_runs(), prompt_identity=prompt_identity(),
                outward_experiment=outward_experiment(), tool_outcomes=tool_outcomes(),
                deliberation_cost=deliberation_cost())


def render(s: dict = None) -> str:
    s = s or all_signals()
    L = ["=" * 96, "SENSORS - the signals nothing else computes, %s" % s["at"], "=" * 96]
    m = s["move_runs"]
    L.append("\n  MOVE REPETITION")
    if m.get("ok"):
        L.append("    current       %s" % m["current_move"])
        L.append("    streak        %d   longest ever %d   distinct in last %d: %d"
                 % (m["streak"], m["longest_ever"], m["window"], m["distinct_in_window"]))
        if m["note"]:
            L.append("    >> %s" % m["note"])
        L.append("    spread        %s" % m["spread"])
    else:
        L.append("    unavailable: %s" % m.get("why"))

    p = s["prompt_identity"]
    L.append("\n  IS IT SEEING THE SAME WORLD")
    L.append("    %s" % (p.get("note") if p.get("ok") else "unavailable: " + str(p.get("why"))))

    e = s["outward_experiment"]
    L.append("\n  THE OUTWARD EXPERIMENT  (since the nudge was removed)")
    if e.get("ok"):
        L.append("    decisions %d   outward chosen %d   dispatches that ran %d"
                 % (e["decisions"], e["outward_chosen"], e["dispatches_that_ran"]))
        L.append("    >> %s" % e["verdict"])
    else:
        L.append("    unavailable: %s" % e.get("why"))

    d = s["deliberation_cost"]
    L.append("\n  DELIBERATION COST")
    if d.get("ok"):
        L.append("    last %.1fs   mean %.1fs   range %.1f-%.1f   rod %s"
                 % (d["last"], d["mean"], d["min"], d["max"], d["rod"]))
        L.append("    recent %s" % ", ".join("t%d:%.0fs" % (r["tick"], r["secs"]) for r in d["recent"]))
    else:
        L.append("    unavailable: %s" % d.get("why"))

    t = s["tool_outcomes"]
    L.append("\n  DID THE TOOL DO ITS JOB  (last %s calls)" % t.get("window"))
    if t.get("ok"):
        L.append("    %-15s %6s %5s %11s %7s %8s %6s"
                 % ("tool", "calls", "ran", "barren", "raised", "refused", "unmeas"))
        for r in t["tools"][:9]:
            L.append("    %-15s %6d %5d %11s %7d %8d %6d"
                     % (r["tool"], r["calls"], r["ran"],
                        ("%d (%s%%)" % (r["barren"], r["barren_rate"])) if r["barren"] else "0",
                        r["raised"], r["refused"], r["unmeasured"]))
        L.append("    note: %s" % t["note"][:150])
    else:
        L.append("    unavailable: %s" % t.get("why"))
    return "\n".join(L)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if "--json" in sys.argv:
        print(json.dumps(all_signals(), indent=1, default=str))
        sys.exit(0)
    print(render())
