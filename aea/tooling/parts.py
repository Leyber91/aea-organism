"""parts.py - ONE PANEL PER PART, AND EACH ONE MEASURES THE ACTION RATHER THAN THE CODE.

    python -m aea.tooling.parts            every part, demonstrated or not
    python -m aea.tooling.parts --json     the same, as data

WHY THIS EXISTS. Luis, 2026-08-03: *"it faces demonstrating one action, so we have to find out how
to measure that action. Otherwise, how do we know that it's actually doing that?"* and *"what cannot
be measured cannot be demonstrated."*

THE FAILURE THAT PROVED THE NEED, an hour earlier and committed by the author of this file.
`vital.py` runs the organism in a COLD SANDBOX and reported `knobs:set 0 calls`, `unstick:propose
0 calls`. I read that and told Luis the entity had never changed its own configuration. Production
said: **KNOB APPLIED eighteen times, unstick.propose seventy-nine times, and knobs.json holds three
entries the entity wrote itself.** A sandbox result asserted as a fact about the running system.

SO EVERY PART HERE DECLARES THREE THINGS AND THE THIRD IS THE ONE THAT MATTERS:

    ACTION      what this part DOES, in one sentence. Not what it is
    EVIDENCE    the specific store, field or log line that exists ONLY IF the action happened
    VERDICT     DEMONSTRATED (with a count and a timestamp) / NEVER / UNMEASURED

`UNMEASURED` IS A FIRST-CLASS VERDICT, and refusing to have it is how a dashboard lies. A part whose
action leaves no trace is not passing and is not failing - it is unobservable, and saying so is the
only honest thing a panel can do. Three parts below are UNMEASURED and they are named, because a
green board with a silent hole in it is worse than a board that admits the hole.

AND THE EVIDENCE IS PRODUCTION, NEVER A SANDBOX. Every count comes from the live record: the hands
ledger, the outcome record, the wake spawn ledger, the artefact store, the entity's own log. What a
function does in a fresh temp directory is a different question with a different instrument, and
conflating the two is the mistake this file was written after.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

from aea.kernel import grid


def _jsonl(name: str) -> tuple:
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
    return out, ("" if out else "%s is empty" % name)


def _log() -> tuple:
    p = os.path.join(grid.STATE, "live.log")
    if not os.path.exists(p):
        return "", "live.log does not exist"
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read(), ""
    except Exception as e:
        return "", "live.log unreadable (%s)" % type(e).__name__


def _when(ts) -> str:
    try:
        return time.strftime("%m-%d %H:%M", time.localtime(float(ts)))
    except Exception:
        return "-"


def _from_log(pattern: str, label: str) -> dict:
    """Count a LOG LINE that only appears when the action ran. The log is the entity's own voice."""
    txt, why = _log()
    if why:
        return dict(count=None, last="-", why=why)
    hits = re.findall(r"^(\S+ \S+ \S+)\s+.*" + pattern, txt, re.M)
    n = len(re.findall(pattern, txt))
    return dict(count=n, last=(hits[-1] if hits else "-"), why="")


def _from_rows(rows, pred, tsfield="at") -> dict:
    hits = [r for r in rows if pred(r)]
    last = "-"
    if hits:
        last = _when(hits[-1].get(tsfield) or hits[-1].get("t") or 0)
    return dict(count=len(hits), last=last, why="")


def survey() -> list:
    """Every part, with the evidence its action actually happened. Production only."""
    hands, hands_why = _jsonl("hands_ledger.jsonl")
    outcomes, out_why = _jsonl("outcomes.jsonl")
    decisions, dec_why = _jsonl("r1_decisions.jsonl")
    percept, per_why = _jsonl("perception.jsonl")
    wakes, wake_why = _jsonl("wake_spawns.jsonl")
    arte, arte_why = _jsonl("artefacts.jsonl")
    refl, refl_why = _jsonl("reflections.jsonl")

    P = []

    def add(part, action, evidence, res, note=""):
        if res.get("why"):
            verdict = "UNMEASURED"
        elif res.get("count") is None:
            verdict = "UNMEASURED"
        elif res["count"] > 0:
            verdict = "DEMONSTRATED"
        else:
            verdict = "NEVER"
        P.append(dict(part=part, action=action, evidence=evidence, verdict=verdict,
                      count=res.get("count"), last=res.get("last", "-"),
                      why=res.get("why", ""), note=note))

    # ---- the two loops --------------------------------------------------------------------------
    hb = grid.load_json(os.path.join(grid.STATE, "heartbeat.json"), {}) or {}
    add("loop.live", "acts on a tick without a person present",
        "heartbeat.total_ticks", dict(count=int(hb.get("total_ticks") or 0),
                                      last=_when(os.path.getmtime(os.path.join(grid.STATE, "heartbeat.json")))
                                      if os.path.exists(os.path.join(grid.STATE, "heartbeat.json")) else "-"))
    try:
        mind = json.load(open(os.path.join(grid.STATE, "aea_state.json"),
                              encoding="utf-8", errors="replace"))
    except Exception as e:
        mind = {}
    add("loop.aea", "deliberates and commits a decision",
        "aea_state.tick + surfaced[]", dict(count=int(mind.get("tick") or 0),
                                            last=_when(((mind.get("surfaced") or [{}])[-1] or {}).get("at"))))

    # ---- the kernel -----------------------------------------------------------------------------
    add("kernel.wake", "SPAWNS the mind, on a cadence the entity computes",
        "wake_spawns.jsonl", _from_rows(wakes, lambda r: True))
    add("kernel.decide", "turns the wake's prose into a validated move",
        "r1_decisions.jsonl (wake != fallback)",
        _from_rows(decisions, lambda r: r.get("differed") is True))
    add("kernel.hands", "runs a real tool behind the zone gate",
        "hands_ledger.jsonl outcome=ran", _from_rows(hands, lambda r: r.get("outcome") == "ran"))
    add("kernel.hands (refusal)", "REFUSES a tool the zone forbids",
        "hands_ledger.jsonl outcome=refused",
        _from_rows(hands, lambda r: r.get("outcome") == "refused"),
        "a gate with no exercised refusal is `return True`")
    add("kernel.dispatch", "puts a literal query and allowlisted URLs on the wire",
        "hands_ledger look_outward + outcome=ran",
        _from_rows(hands, lambda r: r.get("tool") == "look_outward" and r.get("outcome") == "ran"))
    add("kernel.egress", "REFUSES a dispatch outside the floor or ceiling",
        "live.log 'egress refused'", _from_log(r"egress refused", "egress"))
    add("kernel.artefacts", "hashes bytes AT ARRIVAL and stores them under their digest",
        "artefacts.jsonl with sha256", _from_rows(arte, lambda r: bool(r.get("sha256"))))
    add("kernel.outcomes", "records what happened, not what was meant",
        "outcomes.jsonl", _from_rows(outcomes, lambda r: True))
    add("kernel.outcomes (suppress)", "STOPS re-choosing what its record says keeps failing",
        "live.log 'HELD BACK'", _from_log(r"HELD BACK", "suppress"))
    add("kernel.impasse", "names a capability as stuck, from its own record",
        "live.log 'STUCK:'", _from_log(r"STUCK:", "impasse"))
    add("kernel.unstick", "proposes another route from a CLOSED set",
        "live.log 'PROPOSED:'", _from_log(r"PROPOSED:", "unstick"))
    add("kernel.knobs", "CHANGES ITS OWN CONFIGURATION",
        "live.log 'KNOB APPLIED' + knobs.json", _from_log(r"KNOB APPLIED", "knobs"))
    add("kernel.crystal", "turns a route that worked TWICE into a reusable part",
        "crystal.json parts", dict(count=len((grid.load_json("crystal.json", {}) or {}).get("parts") or {}),
                                   last="-"),
        "requires something to work twice; nothing has yet")
    add("kernel.trust", "REFUSES a capability the ladder has not granted",
        "live.log 'NOT APPLIED'", _from_log(r"NOT APPLIED", "trust"))
    add("kernel.perceive", "chooses what to look at, and records WHY",
        "perception.jsonl src=wake",
        _from_rows(percept, lambda r: r.get("src") == "wake" and r.get("why_from") == "wake"))

    # ---- organs ---------------------------------------------------------------------------------
    add("organs.reflect", "poses a question to itself and answers it",
        "reflections.jsonl", _from_rows(refl, lambda r: True, tsfield="t"))
    add("organs.brief", "produces the daily brief",
        "live.log 'AWAKE:brief  ok'", _from_log(r"AWAKE:brief\s+ok", "brief"))
    add("memory.consolidate", "turns closed episodes into semantic memory",
        "live.log 'ASLEEP:consolidate  ok'", _from_log(r"ASLEEP:consolidate\s+ok", "consolidate"))
    hades, hades_why = _jsonl("hades.jsonl")
    add("mind.hades", "judges the wake's output and can say REDO",
        "hades.jsonl", _from_rows(hades, lambda r: True) if hades
        else dict(count=None, last="-",
                  why=(hades_why or "hades.jsonl absent") + " - the store was added 2026-08-04; "
                      "it fills from the next wake tick onward"))
    add("mind.hades (redo)", "DISAGREES with the wake and sends it back",
        "hades.jsonl verdict=redo",
        _from_rows(hades, lambda r: "redo" in str(r.get("verdict") or "").lower()) if hades
        else dict(count=None, last="-", why="no hades.jsonl yet"),
        "a judge that never disagrees is `return accept`")

    # ---- the parts with no observable action ----------------------------------------------------
    add("kernel.grid (meter)", "refuses a rod that is rate-limited or out of budget",
        "no store records a REFUSED draw", dict(count=None, last="-",
                                                why="grid.Meter.can_spend returns a reason and "
                                                    "nothing persists the refusals"))
    add("mind.orchestrator", "routes a hard problem to a swarm",
        "no store records a swarm invocation", dict(count=None, last="-",
                                                   why="no swarm ledger exists"))
    return P


def render(parts=None) -> str:
    parts = parts or survey()
    order = {"DEMONSTRATED": 0, "NEVER": 1, "UNMEASURED": 2}
    L = ["=" * 108,
         "THE PARTS - each one measured by its ACTION, from the production record",
         "=" * 108,
         "  %-24s %-13s %8s  %-12s %s" % ("part", "verdict", "count", "last", "the action")]
    for p in sorted(parts, key=lambda x: (order.get(x["verdict"], 3), x["part"])):
        L.append("  %-24s %-13s %8s  %-12s %s"
                 % (p["part"], p["verdict"],
                    "-" if p["count"] is None else p["count"], p["last"], p["action"][:52]))
        if p["verdict"] == "UNMEASURED" and p["why"]:
            L.append("  %-24s %s" % ("", "why: " + p["why"][:88]))
        elif p["note"] and p["verdict"] != "DEMONSTRATED":
            L.append("  %-24s %s" % ("", p["note"][:88]))
    d = len([p for p in parts if p["verdict"] == "DEMONSTRATED"])
    n = len([p for p in parts if p["verdict"] == "NEVER"])
    u = len([p for p in parts if p["verdict"] == "UNMEASURED"])
    L.append("")
    L.append("  %d DEMONSTRATED   %d NEVER   %d UNMEASURED   of %d parts" % (d, n, u, len(parts)))
    L.append("")
    L.append("  UNMEASURED is not a pass. A part whose action leaves no trace cannot be")
    L.append("  demonstrated, and a board that hides that is worse than one that admits it.")
    return "\n".join(L)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ps = survey()
    if "--json" in sys.argv:
        print(json.dumps(ps, indent=1, default=str))
        sys.exit(0)
    print(render(ps))
