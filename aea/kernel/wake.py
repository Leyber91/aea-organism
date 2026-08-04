"""wake.py - THE ENTITY COMPUTES WHEN IT NEXT THINKS, AND SOMETHING DUMB EXECUTES IT.

    python -m aea.kernel.wake              the wake budget, and what it permits right now

THE DEFECT THIS EXISTS TO CLOSE, and it is the oldest one on the ladder. Measured 2026-08-03:

    aea/server/controlroom.py:699   spawns  aea.loop.live      the ACTING loop
                                    spawns  aea.loop.aea       NOTHING. No call site anywhere

`aea.loop.aea` - the DELIBERATING loop, the thing every rung from R1 upward is actually about - has
no spawner. Its `main()` takes N_TICKS as a positional argument: it is a CLI a person drives. And
the record agrees. `r1_decisions.jsonl`, `perception.jsonl` and `sensed.jsonl` all stop at the same
instant, which is a human standing up, not a rhythm.

SO R0 IS PROVEN FOR THE WRONG LOOP. Its 246.9 unattended hours certified a BODY. Every rung above it
is measured on an entity whose mind a human breathes for, and two rungs are blocked by exactly that:
R4b's condition 3 cannot accumulate occasions, and R5's gate - five research runs, each spanning
multiple ticks across 90+ minutes of enforced egress floor - would require a person at the keyboard
for most of a day.

A CRON JOB IS NOT AN OSCILLATOR. Biology's clock is endogenous: it free-runs in constant darkness,
and light shifts its phase without causing it. If the OS decides when the entity lives, the human
has only moved into a config file. So the entity COMPUTES the number - `hb["next_wake_s"]` - and
this module clamps it and something dumb executes it. When the entity has not computed one, the
fallback fires AND IS RECORDED AS THE FALLBACK, because a silent default reads as a decision.

WHAT IS CLAMPED, all of it from on-disk state so a restart cannot reset it:

    FLOOR_S       the entity may not think more often than this, whatever it asks for
    CEILING_S     nor less often, or a wake that never comes is indistinguishable from a dead loop
    PER_DAY       a budget on wakes in a rolling 24h window. The entity cannot raise it: it is a
                  constant in this file and changing it is a diff
    STOP          `state/STOP` - the SAME file egress checks, so one kill halts thinking and
                  reaching together, and it survives the entity's own next scheduled wake

WHY THIS DUPLICATES `egress.py`'s SHAPE INSTEAD OF SHARING CODE WITH IT. Law W1 says the second time
you write it, extract it - and the right call here is the opposite one. `egress` is R4b's CERTIFIED
condition 2; its numbers are published and its bound is measured. Refactoring a certified module so
an uncertified one can share its helpers puts the certificate at risk to save forty lines, and the
two budgets do not mean the same thing: egress bounds HOW MUCH CAN LEAVE, this bounds HOW OFTEN IT
THINKS. Same shape, different claim. If a third one appears, extract then.

WHAT THIS DELIBERATELY DOES NOT DO. §5 of THE_STRUCTURE_CONVERSATION asks for the wake to be spawned
"when it has nothing to react to" - thinking is worth most exactly then. That condition is NOT built
here: this spawns on the entity's own clamped cadence, and reactivity is not consulted. Saying so,
because a partial implementation described as a whole one is the defect class this repo keeps
paying for.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

from aea.kernel import grid

STORE = "wake_budget.json"
LEDGER = "wake_spawns.jsonl"
STOP_FILE = "STOP"                       # the same file egress checks - one kill stops both

# THE THREE NUMBERS THE CLAMP RESTS ON. Deliberately wide at the top and tight at the bottom: a
# minute is the fastest a mind here has any reason to run, an hour is slow enough that a stuck
# entity is obvious.
#
# RAISED 2026-08-03 FROM 24/day AND A 3600s FALLBACK, on Luis's instruction to gather more data,
# and the numbers are measured rather than picked. `grid.PLANTS` gives nvidia **rpm 40 and NO daily
# cap**; the meter shows 13 requests and 5,933 tokens spent today, about 456 tokens a call. At 96
# wakes a day and roughly three model calls per wake tick that is ~288 calls and ~130k tokens
# daily - two orders of magnitude inside a limit that is per-MINUTE and never per-day.
#
# SO THE BINDING CONSTRAINT WAS NEVER THE FLEET. It was this file, and it was set conservatively by
# an author who had not looked up the limits. That is worth naming: a clamp chosen for caution and
# left unmeasured is indistinguishable from a clamp chosen for a reason.
#
# EGRESS IS DELIBERATELY UNCHANGED at 12/day behind an 1800s floor. It is R4b's certified condition
# 2 and the source of a published figure (27.86 bits/day). More thinking does not buy more
# reaching, and it must not: the two budgets bound different things, and only one of them is a
# claim on a page.
#
# RAISED AGAIN 2026-08-03 to a 300s cadence and 288/day, on Luis's ask to make it move every five
# minutes. 288 wakes at ~3 model calls each is ~864 calls and ~394k tokens a day, against nvidia's
# 40-per-MINUTE limit and no daily cap - 0.6 calls a minute, which is 1.5% of the ceiling.
#
# THE POINT IS NOT SPEED, IT IS SAMPLE SIZE. The claim this whole session rests on - that the entity
# will not look outward until R5 gives it a reason - currently rests on n=2 wake decisions after the
# nudge was removed. At 288 opportunities a day that becomes a real measurement inside 24 hours. A
# zero at n=288 is evidence; a zero at n=2 is an anecdote.
FLOOR_S = 60.0
CEILING_S = 3600.0
PER_DAY = 288
FALLBACK_S = 300.0                       # used when the entity computed nothing. RECORDED as such


def _path() -> str:
    """Resolved at CALL time. A path bound at import cannot be sandboxed by a test (D48)."""
    return os.environ.get("AEA_WAKE_BUDGET") or os.path.join(grid.STATE, STORE)


def _ledger_path() -> str:
    return os.environ.get("AEA_WAKE_LEDGER") or os.path.join(grid.STATE, LEDGER)


def _stop_path() -> str:
    return os.environ.get("AEA_EGRESS_STOP") or os.path.join(grid.STATE, STOP_FILE)


def _load() -> tuple:
    """(ledger, why-it-is-empty). NEVER a bare {} - absent and corrupt are opposite facts.

    Absent means nothing has been spent. Corrupt means SPENDS MAY HAVE BEEN LOST, so the ceiling
    cannot be enforced against a count that may be wrong. Same reasoning as `egress._load`, which
    was caught by the defect ratchet the moment it shipped with a silent default."""
    p = _path()
    if not os.path.exists(p):
        return {}, "no ledger yet - nothing has been spent"
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        return {}, "LEDGER UNREADABLE (%s) - spends may have been lost" % type(e).__name__
    if not isinstance(d, dict):
        return {}, "LEDGER IS NOT AN OBJECT (%s) - spends may have been lost" % type(d).__name__
    return d, ""


def _window(d: dict, now: float) -> list:
    return [t for t in (d.get("at") or []) if isinstance(t, (int, float)) and now - t < 86400.0]


def interval_for(hb: dict = None) -> dict:
    """How long until the next wake, and WHO DECIDED - the entity or the fallback.

    Returns the decision as a record rather than a number, because "the entity chose 900s" and "the
    entity chose nothing and got the default" are different facts about a mind, and a bare integer
    cannot tell them apart. That distinction is the whole difference between an endogenous clock and
    a cron job with extra words."""
    raw = (hb or {}).get("next_wake_s")
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return dict(seconds=FALLBACK_S, by="fallback", asked=None, clamped=False,
                    why="the entity computed no next_wake_s" if raw is None
                        else "next_wake_s was %r, not a number" % (raw,))
    asked = float(raw)
    sec = max(FLOOR_S, min(CEILING_S, asked))
    return dict(seconds=sec, by="entity", asked=asked, clamped=(sec != asked),
                why="" if sec == asked else "clamped from %.0fs into [%.0f, %.0f]"
                    % (asked, FLOOR_S, CEILING_S))


def fuel(tier: str = "frontier", zone: str = "private", meter=None, order: str = "depth") -> dict:
    """IS THERE A ROD THAT CAN ACTUALLY BE SPENT AGAINST RIGHT NOW - asked of the live meter.

    Named by Luis 2026-08-03: the wake "needs to be aware of the models available, and what the
    request permits". He is right, and the failure it prevents is specific. `aea.loop.aea` opens
    with `energy.ladder("frontier", "private")` and thinks with whatever sits at the top. If every
    NVIDIA rod on that ladder is in a 429 cooldown, saturated in-flight, or out of requests-per-day,
    the wake still starts, still burns one of PER_DAY, and produces a tick that could not think -
    which then lands in the record as the ENTITY failing rather than as the fleet being empty.

    Measured on this machine the same day: `groq/llama-3.3-70b-versatile` sat at 33 consecutive
    failures and cooled; `nvidia/mistralai/mistral-small-4-119b` was retired after 8; a crystallised
    path in `state/paths.json` still pointed at the cooled rod. A fleet is not a constant.

    THE QUESTION IS ASKED OF `Meter.can_spend`, NOT OF A CENSUS. The census says what a rod CAN do;
    the meter says what this account may do in the next second - rpm, rpd, tokens/day, monthly
    calls, in-flight saturation, 429 cooldown. Documentation describes the product, the endpoint
    describes what you actually have, and a rate limit is the endpoint's opinion.

    Returns the whole picture rather than a bool: which rod is available, and for every rod that is
    not, WHY and for how long. A refusal that cannot say which limit bit is a refusal nobody can act
    on at four in the morning.

    `order` DEFAULTS TO "depth" BECAUSE THAT IS WHAT THE WAKE ACTUALLY ASKS FOR. This shipped
    calling `energy.ladder(tier, zone)` with the default ordering while `aea.loop.aea:core` calls
    `energy.draw(..., order="depth")` - so the availability check ranked by score and answered about
    a rod the wake would never take. Measured 2026-08-04: the console printed
    `FUEL nvidia/nemotron-3-nano-30b-a3b` for hours while every one of the last 19 wakes ran on
    `nemotron-3-ultra-550b-a55b`, and it was read out as the entity's rod three times before anyone
    checked the record. D28's defect a second time - score ordering puts a nano ahead of a 550b -
    and here it corrupted the refusal too, not only the label: with score ordering this returns
    "there is fuel" whenever the nano is spendable, including when every rod the wake would actually
    reach for is in a 429 cooldown. A liveness check must ask the question the caller will ask."""
    try:
        from aea.energy import energy
        rods = energy.ladder(tier, zone, order=order)
    except Exception as e:
        # FAIL OPEN HERE, DELIBERATELY, AND ONLY HERE. If the ladder itself cannot be computed we do
        # not know that there is no fuel - we know we cannot see. Refusing every wake on a broken
        # census would let one unreadable file silently stop the mind, which is a worse failure than
        # one wasted tick, and it would look exactly like an entity that chose to stop thinking.
        return dict(ok=True, rod=None, checked=0, blind=True,
                    why="ladder unavailable (%s: %s) - not treated as empty"
                        % (type(e).__name__, str(e)[:70]), rods=[])
    m = meter or grid.Meter()
    seen = []
    for plant, model in rods[:8]:
        try:
            ok, wait, reason = m.can_spend(plant, model)
        except Exception as e:
            ok, wait, reason = False, None, "%s: %s" % (type(e).__name__, str(e)[:40])
        seen.append(dict(plant=plant, model=model, ok=bool(ok), wait=wait, why=reason))
        if ok:
            return dict(ok=True, rod=(plant, model), checked=len(seen), blind=False,
                        why="", rods=seen)
    return dict(ok=False, rod=None, checked=len(seen), blind=False, rods=seen,
                why=("no rod can be spent against: "
                     + "; ".join("%s/%s %s" % (r["plant"], r["model"].rsplit("/", 1)[-1], r["why"])
                                 for r in seen[:4])) if seen else "the ladder is empty")


def allow(now: float = None, hb: dict = None, check_fuel: bool = True) -> tuple:
    """(ok, why). REFUSES rather than delays - a refusal is a recorded event, a delay is not."""
    now = time.time() if now is None else now
    if os.path.exists(_stop_path()):
        return False, "state/STOP exists - thinking is halted and this survives a restart"
    d, why = _load()
    if why.startswith("LEDGER"):
        return False, why
    recent = _window(d, now)
    last = max(recent) if recent else None
    if last is not None:
        need = interval_for(hb)["seconds"]
        if (now - last) < min(need, CEILING_S):
            return False, ("interval: %.0fs since the last wake, %.0fs required"
                           % (now - last, need))
        if (now - last) < FLOOR_S:
            return False, "floor: %.0fs since the last wake, %.0fs required" % (now - last, FLOOR_S)
    if len(recent) >= PER_DAY:
        return False, "ceiling: %d wakes in the last 24h, %d permitted" % (len(recent), PER_DAY)
    # THE FUEL CHECK IS LAST, because it is the only one that costs a network-shaped lookup and the
    # cheap refusals should short-circuit it. It is also the only one that can be waived
    # (`check_fuel=False`) - by tests, never by the entity, which cannot reach this argument.
    if check_fuel:
        f = fuel()
        if not f["ok"]:
            return False, "no fuel: %s" % f["why"]
    return True, ""


def spend(decision: dict, now: float = None) -> dict:
    """Record a wake. Written BEFORE the process is spawned, never after.

    Write-ahead, for the reason every other ledger here is: a crash between the spawn and the record
    must COST the budget rather than refund it. Optimistic accounting on an act that has already
    happened turns a ceiling into a suggestion."""
    now = time.time() if now is None else now
    d, _why = _load()
    at = _window(d, now) + [now]
    d["at"] = sorted(at)[-(PER_DAY * 4):]
    d["last_iso"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now))
    d["last_by"] = decision.get("by")
    grid.atomic_save_json(_path(), d, indent=1)
    grid.append_jsonl(_ledger_path(), dict(
        at=now, iso=d["last_iso"], by=decision.get("by"), seconds=decision.get("seconds"),
        asked=decision.get("asked"), clamped=decision.get("clamped"), why=decision.get("why", "")))
    return d


def spawn(ticks: int = 1, hb: dict = None, now: float = None, runner=None,
          check_fuel: bool = True) -> dict:
    """Start ONE wake, if the clamp permits. Returns what happened, always with a reason.

    `runner` is injected so a test can prove the gate without starting a process - the same seam
    `dispatch.run` uses for `invoke`, and for the same reason: a control that cannot exercise the
    real path is not a control.

    THE SPAWN IS DETACHED AND ITS OUTPUT GOES TO A LOG, matching how `controlroom` starts `live`.
    A wake that inherits this process's stdout would interleave two loops' output into one stream
    and make the record unreadable, which is how a log stops being evidence."""
    now = time.time() if now is None else now
    decision = interval_for(hb)
    ok, why = allow(now, hb, check_fuel=check_fuel)
    if not ok:
        return dict(spawned=False, why=why, decision=decision)
    spend(decision, now)                                    # write-ahead
    if runner is None:
        def runner(n):
            logp = os.path.join(grid.STATE, "wake.log")
            logf = open(logp, "ab")
            return subprocess.Popen(
                [sys.executable, "-m", "aea.loop.aea", str(n)],
                cwd=grid.ROOT, stdout=logf, stderr=logf,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    try:
        p = runner(int(ticks))
    except Exception as e:
        return dict(spawned=False, why="spawn failed: %s: %s" % (type(e).__name__, str(e)[:90]),
                    decision=decision, budget_spent=True)
    return dict(spawned=True, why="", decision=decision,
                pid=getattr(p, "pid", None), ticks=int(ticks))


def state(now: float = None, hb: dict = None) -> dict:
    now = time.time() if now is None else now
    d, load_why = _load()
    recent = _window(d, now)
    ok, why = allow(now, hb)
    last = max(recent) if recent else None
    return dict(floor_seconds=FLOOR_S, ceiling_seconds=CEILING_S, per_day=PER_DAY,
                fallback_seconds=FALLBACK_S,
                decision=interval_for(hb), spent_24h=len(recent),
                remaining=max(0, PER_DAY - len(recent)),
                seconds_since_last=(round(now - last, 1) if last else None),
                permitted_now=ok, refused_because=why or None,
                ledger=load_why or "ok", stop_present=os.path.exists(_stop_path()))


def selftest() -> list:
    """Every check gets a control on the defect class it claims to cover, or it does not count."""
    import tempfile
    out = []

    def chk(n, ok, d=""):
        out.append((n, bool(ok), d))

    with tempfile.TemporaryDirectory() as td:
        keep = {k: os.environ.get(k) for k in
                ("AEA_WAKE_BUDGET", "AEA_WAKE_LEDGER", "AEA_EGRESS_STOP")}
        os.environ["AEA_WAKE_BUDGET"] = os.path.join(td, "wake_budget.json")
        os.environ["AEA_WAKE_LEDGER"] = os.path.join(td, "wake_spawns.jsonl")
        os.environ["AEA_EGRESS_STOP"] = os.path.join(td, "STOP")
        spawned = []

        def fake(n):
            spawned.append(n)
            return type("P", (), {"pid": 4242})()

        try:
            d = interval_for({"next_wake_s": 900})
            chk("the entity's own number is used", d["seconds"] == 900 and d["by"] == "entity")
            chk("CONTROL an absent number falls back, and SAYS so",
                interval_for({})["by"] == "fallback")
            chk("CONTROL a non-number falls back",
                interval_for({"next_wake_s": "soon"})["by"] == "fallback")
            chk("CONTROL True is not a number", interval_for({"next_wake_s": True})["by"] == "fallback")
            lo = interval_for({"next_wake_s": 1})
            hi = interval_for({"next_wake_s": 99999})
            chk("CONTROL below the floor is clamped UP", lo["seconds"] == FLOOR_S and lo["clamped"])
            chk("CONTROL above the ceiling is clamped DOWN",
                hi["seconds"] == CEILING_S and hi["clamped"])

            t0 = 1_000_000.0
            # `check_fuel=False` throughout the CLAMP checks: they are about the budget, and asking
            # the live meter would make a rate limit somewhere else decide whether this suite is
            # green. The fuel gate gets its own controls below, against a fake meter.
            r = spawn(1, hb={"next_wake_s": 60}, now=t0, runner=fake, check_fuel=False)
            chk("a permitted wake spawns", r["spawned"] and spawned == [1])
            r2 = spawn(1, hb={"next_wake_s": 60}, now=t0 + 5, runner=fake, check_fuel=False)
            chk("CONTROL a wake inside the interval is REFUSED",
                not r2["spawned"] and "interval" in (r2["why"] or ""))
            r3 = spawn(1, hb={"next_wake_s": 60}, now=t0 + 61, runner=fake, check_fuel=False)
            chk("...and permitted once the interval has passed", r3["spawned"])

            open(os.environ["AEA_EGRESS_STOP"], "w").write("halt")
            r4 = spawn(1, hb={"next_wake_s": 60}, now=t0 + 100000, runner=fake, check_fuel=False)
            chk("CONTROL state/STOP refuses a wake", not r4["spawned"] and "STOP" in r4["why"])
            os.remove(os.environ["AEA_EGRESS_STOP"])

            base = 2_000_000.0
            for i in range(PER_DAY + 3):
                spawn(1, hb={"next_wake_s": 60}, now=base + i * 61.0, runner=fake, check_fuel=False)
            st = state(now=base + (PER_DAY + 3) * 61.0)
            chk("CONTROL the daily ceiling holds", st["spent_24h"] <= PER_DAY,
                "spent %s of %s" % (st["spent_24h"], PER_DAY))

            # ---- THE FUEL GATE, against a fake meter so no live rate limit decides this suite ----
            class _AllThrottled:
                def can_spend(self, plant, model, est_tokens=800):
                    return (False, 42.0, "throttled (429 cooldown)")

            class _OneFree:
                def __init__(self):
                    self.n = 0

                def can_spend(self, plant, model, est_tokens=800):
                    self.n += 1
                    return (self.n >= 2, 0.0, "ok" if self.n >= 2 else "rpm")

            f_bad = fuel(meter=_AllThrottled())
            chk("CONTROL an exhausted fleet reports no fuel", not f_bad["ok"] and not f_bad["blind"])
            chk("...and the refusal NAMES which limit bit", "throttled" in (f_bad["why"] or ""))
            f_ok = fuel(meter=_OneFree())
            chk("a fleet with one live rod reports fuel", f_ok["ok"] and f_ok["rod"] is not None)
            chk("...and it names the rod it would use", bool(f_ok["rod"]))

            with open(os.environ["AEA_WAKE_BUDGET"], "w") as f:
                f.write("{ not json")
            chk("CONTROL a corrupt budget refuses rather than resets",
                not allow(now=base + 10**6, check_fuel=False)[0])
        finally:
            for k, v in keep.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    return out


if __name__ == "__main__":
    hb = grid.load_json(os.path.join(grid.STATE, "heartbeat.json"), {}) or {}
    s = state(hb=hb)
    if "--json" in sys.argv:
        print(json.dumps(dict(state=s, selftest=[dict(check=n, ok=o, detail=d)
                                                 for n, o, d in selftest()]), indent=1))
        sys.exit(0)
    print("=" * 92)
    print("THE WAKE BUDGET - the entity computes when it next thinks; this clamps it")
    print("=" * 92)
    d = s["decision"]
    print("  next wake in           %.0fs   decided by %s%s" % (
        d["seconds"], d["by"], ("  (%s)" % d["why"]) if d["why"] else ""))
    print("  clamp                  floor %.0fs, ceiling %.0fs, %d per day"
          % (s["floor_seconds"], s["ceiling_seconds"], s["per_day"]))
    print("  spent in the last 24h  %d of %d" % (s["spent_24h"], s["per_day"]))
    print("  seconds since last     %s" % s["seconds_since_last"])
    print("  permitted right now    %s%s" % (s["permitted_now"],
                                             "" if s["permitted_now"]
                                             else "  (%s)" % s["refused_because"]))
    print("  state/STOP present     %s" % s["stop_present"])
    print()
    res = selftest()
    for n, ok, det in res:
        print("  %-52s %s%s" % (n, "ok" if ok else "FAIL", ("   " + det) if det and not ok else ""))
    bad = [n for n, ok, _ in res if not ok]
    print()
    print("  %d of %d checks pass%s" % (len(res) - len(bad), len(res),
                                        "" if not bad else "   FAILING: " + ", ".join(bad)))
    sys.exit(1 if bad else 0)
