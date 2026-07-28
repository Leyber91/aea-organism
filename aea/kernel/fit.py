"""fit.py - ONE PLACE THAT ANSWERS "WHICH ROD FOR THIS JOB", AND SAYS WHY NOT FOR ALL THE OTHERS.

An audit of this repo on 2026-07-28 found TWENTY-ONE systems touching model budgets or selection, and
SIX functions that pick a model - `grid.Router.pick`, `orchestrator.pick`, `energy.ladder`/`draw`,
`swarm.pick_varied`, `seats.pick_rod`, and a hardcoded ladder in `organs/converse.py`. None of them
calls another. They rank on four different keys: cheapest-plant-first, lowest-latency, highest-score,
and random-among-the-top-eight.

THIS FILE IS NOT THE SEVENTH. It is written to be the one the others delegate to, and it starts by
replacing `seats.pick_rod` outright. Adding a selector without removing one would make the exact
problem worse, and saying so is cheaper than discovering it later.

WHAT A SELECTOR MUST DO THAT NONE OF THE SIX DOES: state the requirement, then refuse.

    a NEED says what the job requires        suites, tools, zone, locality
    `fit()` returns rods that satisfy ALL    with the reason each survivor survived
    `why_not()` returns the rejects          with the reason each one died
    nothing matches -> REFUSE                never a fallback to "closest available"

The fallback is not hypothetical. `orchestrator.pick` returns `cands[0]` even when every candidate
failed the budget check - the meter is consulted and then overruled, which is worse than not
consulting it, because the log says it was checked. And `seats.pick_rod` ranked on measured latency
alone, which would have seated the fastest rod in the fuel table for tool work: a rod that cannot
call a tool at all, because it emits a JSON blob that looks like a call, as prose.

DECLARED VERSUS OBSERVED, AND THE FOUR PLACES THEY DISAGREE. `conflicts()` compares the hardcoded
limits in `grid.PLANTS` against what the plants actually said in their own headers via `lab/pace`.
The audit found four live disagreements, including cerebras at 5 rpm in one file and 30 in another,
and nvidia's in-flight ceiling enforced as 20 by the meter and 8 by the lab's own semaphore. A
constant that disagrees with a measurement is not a second opinion; it is a stale one, and the
purpose of this function is that the next disagreement is found by running something rather than by
reading everything.

  python -m aea.kernel.fit                 what would be chosen for each standard need, and why
  python -m aea.kernel.fit --conflicts     declared limits vs what the plants actually reported
"""
from __future__ import annotations

import os
import sys

from aea.kernel import grid, unstick
from aea.lab import pace

FUELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "lab", "organisms", "fuels.json")

# The suites the fleet measures, plus the one hands measures. A need names what it requires from
# this list and nothing outside it - a requirement that cannot be checked is a preference.
SUITES = ("reach", "format", "arith", "carry", "code")


class NoFit(LookupError):
    """Nothing satisfies the need. The message carries the count that died at each gate, because
    "no rod available" is useless and "all 162 died at the zone gate" is a fix."""


class Need:
    """WHAT THE JOB REQUIRES, stated before anything is chosen.

    Every field is checkable against a measurement that already exists. `tools` reads the probe in
    `state/tool_rods.json`; `suites` reads the fleet results in `fuels.json`; `zone` reads the
    privacy boundary in `unstick`. There is deliberately no field for "good at reasoning" - there is
    no measurement of that here, and a requirement nothing can check is how selectors end up ranking
    on name recognition.
    """

    def __init__(self, what: str, zone: str = "public", suites=(), tools: bool = False,
                 budget: bool = True, exclude=(), calls: int = 1, tokens_each: int = 550):
        bad = [s for s in suites if s not in SUITES]
        if bad:
            raise ValueError("no such suite(s) %s; measured suites are %s" % (bad, list(SUITES)))
        self.what, self.zone, self.suites = what, zone, tuple(suites)
        self.tools, self.budget = bool(tools), bool(budget)
        # WHY A SELECTOR NEEDS AN EXCLUDE LIST: A MEASUREMENT CAN GO STALE.
        # `gpt-oss:120b-cloud` passed the tool probe and then began returning empty replies forty
        # minutes later - a hosted quota exhausting as a 200 rather than a 429. Every gate here reads
        # a stored measurement, so every gate would keep choosing it. The thing that NOTICED is the
        # trust ledger and the impasse loop; this is where that live knowledge re-enters selection.
        self.exclude = set(exclude)
        # THE SHAPE OF THE JOB, WHICH IS WHAT DECIDES WHICH WALL YOU HIT.
        # One call and three thousand calls are different questions for the same rod, and a rod that
        # is fastest per token can still be the one that cannot deliver: cerebras runs at ~2000 tok/s
        # and serves five requests a minute, so it is the quickest fuel here and unusable for
        # anything that is many small calls. Speed and capacity are different axes and ranking on
        # the first is how a plan gets started that could never finish.
        self.calls, self.tokens_each = int(calls), int(tokens_each)

    def __repr__(self):
        return ("Need(%r, zone=%s, suites=%s, tools=%s)"
                % (self.what, self.zone, list(self.suites) or "-", self.tools))


def _tool_rods() -> dict:
    doc = grid.load_json(os.path.join(grid.STATE, "tool_rods.json"), {"rods": {}})
    return doc.get("rods") or {}


def _judge(need: Need) -> list:
    """Every rod, with a verdict and a reason. The rejects are kept - that is the whole point.

    Gates run in a fixed order and the FIRST failure is the reason recorded, so "why was nothing
    available" has a single answer per rod rather than a list of complaints.
    """
    rods = (grid.load_json(FUELS, {"rods": {}}).get("rods") or {})
    tools = _tool_rods()
    allowed = unstick.plants_for(need.zone)
    out = []

    for r in rods.values():
        rod, plant = r["rod"], r.get("plant")
        t = r.get("tested") or {}
        verdict = None

        if rod in need.exclude:
            verdict = ("excluded", "excluded by the caller; it is failing right now")
        elif allowed is not None and plant not in allowed:
            verdict = ("zone", "%s may not serve the %s zone" % (plant, need.zone))
        elif allowed is not None and not unstick.is_local(rod):
            verdict = ("locality", "hosted model behind a local plant name; the %s zone keeps data "
                                   "on this machine" % need.zone)
        elif not (t.get("reach") or {}).get("pass"):
            verdict = ("reach", "never answered when measured")
        elif need.tools and rod not in tools:
            verdict = ("unmeasured", "tool-calling has not been measured for this rod")
        elif need.tools and not tools[rod].get("pass"):
            verdict = ("tools", "measured: %s" % tools[rod].get("result"))
        else:
            for s in need.suites:
                if not (t.get(s) or {}).get("pass"):
                    verdict = ("suite", "fails the %s suite" % s)
                    break

        cap = None
        if verdict is None and need.budget:
            ok, wait, why = grid.METER.can_spend(plant, r.get("model") or rod.split("/", 1)[1])
            if not ok:
                verdict = ("budget", "%s (retry in %ss)" % (why, int(wait or 0)))

        # CAPACITY IS THE LAST GATE AND IT IS ABOUT THE JOB, NOT THE ROD. Everything above asks
        # "is this rod capable"; this asks "can this fuel deliver a job of this shape before the
        # walls stop it". A rod can pass every capability gate and still be unable to finish.
        if verdict is None:
            cap = binds(rod, need.calls, need.tokens_each)
            if cap.get("ok") is False:
                verdict = ("capacity", cap["why"])

        tps = (t.get("reach") or {}).get("tps") or 0
        secs = (tools.get(rod) or {}).get("seconds")
        out.append({"rod": rod, "plant": plant, "tps": tps, "tool_seconds": secs,
                    "hours": (cap or {}).get("hours"), "bound_by": (cap or {}).get("bound_by"),
                    "ok": verdict is None,
                    "gate": verdict[0] if verdict else None,
                    "why": verdict[1] if verdict else
                    ("satisfies every requirement; %s" % (cap or {}).get("why", "single call"))})
    return out


def fit(need: Need, limit: int = 5) -> list:
    """Rods that satisfy the need, best first. RAISES NoFit rather than returning a near-miss.

    Ranked on measured tool latency when the need is tool work (that is the number that was actually
    measured for that job) and on measured throughput otherwise. Not on plant rank, not on model
    size, not at random.
    """
    rows = _judge(need)
    good = [r for r in rows if r["ok"]]
    if not good:
        counts = {}
        for r in rows:
            counts[r["gate"]] = counts.get(r["gate"], 0) + 1
        raise NoFit("nothing fits %r. Of %d rods: %s"
                    % (need, len(rows),
                       ", ".join("%d died at %s" % (v, k) for k, v in sorted(counts.items(),
                                                                            key=lambda x: -x[1]))))
    if need.tools:
        good.sort(key=lambda r: (r["tool_seconds"] if r["tool_seconds"] is not None else 999))
    else:
        good.sort(key=lambda r: -r["tps"])
    return good[:limit]


def why_not(need: Need, limit: int = 8) -> list:
    """The rejects and the gate each died at. A selector that cannot say why is the thing this repo
    already has six of."""
    return [r for r in _judge(need) if not r["ok"]][:limit]


def choose(need: Need) -> str:
    """The single rod, or raise. The one call a caller should need."""
    return fit(need, limit=1)[0]["rod"]


# ---------------------------------------------------------------------------------------------
# DECLARED VERSUS OBSERVED
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# FUEL CAPACITY IS NOT A NUMBER. It is a set of walls with different units, windows and SCOPES,
# and which one you hit depends on the shape of the job.
# ---------------------------------------------------------------------------------------------
#
# `grid.PLANTS` gives every plant the same three columns - rpm, rpd, tpd - and fills the gaps with
# None meaning unlimited. That schema is why cerebras reads "declared UNLIMITED" against a real
# 2400/day wall: the table has no way to say "this plant is not limited on this axis" as distinct
# from "nobody has looked". The plants do not have the same shape:
#
#   nvidia    requests/min, PER MODEL, independent buckets. No token period cap observed.
#             The real per-call ceiling is the CONTEXT WINDOW, not a budget.
#   groq      tokens/min AND requests/day, both PER MODEL and DIFFERENT PER MODEL
#             (8b-instant: 6000 tok/min, 14400/day. 70b-versatile: 12000 tok/min, 1000/day.)
#   cerebras  requests/min 5, /hour 150, /day 2400, plus 30000 tok/min. Four walls, org-scoped.
#   ollama    no period limit at all. Binds on CONCURRENCY (one model resident) and WALL CLOCK.
#
# SCOPE is the field nothing in this repo had, and its absence is a live bug: `Meter._roll` buckets
# `rpd` per PLANT while `_win` buckets `rpm` per (plant, model), inside the same `can_spend` call.
# So groq's per-model 14400/day is charged against a shared 1000.

PER_MODEL = "per model"        # independent bucket for each model on the plant
PER_PLANT = "per plant"        # one shared bucket, org-wide

# Which axes each plant is actually limited on, and at what SCOPE. Absence from this table is not
# "unlimited" - `capacity()` reports it as UNKNOWN, which is the distinction the flat schema lost.
SCOPES = {
    "nvidia":   {"req_min": PER_MODEL},
    "groq":     {"req_min": PER_MODEL, "req_day": PER_MODEL, "tok_min": PER_MODEL},
    "cerebras": {"req_min": PER_PLANT, "req_day": PER_PLANT, "tok_min": PER_PLANT},
    "ollama":   {"concurrency": PER_PLANT},
}

# The one plant whose cost is TIME rather than quota. Ollama holds ONE model resident, so calls
# serialise and a second model evicts the first (~37s cold load, ~2s warm - measured, METHOD).
LOCAL_CONCURRENCY = 1


def capacity(rod: str) -> dict:
    """Every wall this rod is subject to, each labelled with its unit, scope and SOURCE.

    Source precedence is OBSERVED > DECLARED, and both are reported rather than merged, because a
    header is one moment and a constant carries a dated provenance note. Anything nobody has looked
    at is `None` with source `unknown` - never silently `unlimited`. That distinction is the whole
    reason this function exists: the flat table could not express it, and twice now a boundary has
    failed open because "no value" was read as "no limit".
    """
    plant, model = rod.split("/", 1)
    cap = grid.PLANTS.get(plant) or {}
    scope = SCOPES.get(plant, {})

    # READ THE BUCKET THE QUOTA ACTUALLY LIVES IN. Where the plant scopes per model, the per-plant
    # record is another model's number wearing this one's name; where it scopes per plant (cerebras
    # is org-bucketed) the plant record is the true one. Falling back to the plant record is honest
    # only because the source label travels with the value.
    per_model = pace.known("%s/%s" % (plant, model)) or {}
    obs = per_model if per_model else (pace.known(plant) or {})
    obs_scope = "observed per model" if per_model else "observed per plant"
    rods = (grid.load_json(FUELS, {"rods": {}}).get("rods") or {})
    r = rods.get(rod) or {}
    tps = ((r.get("tested") or {}).get("reach") or {}).get("tps")
    ctx = (r.get("declared") or {}).get("context")

    def wall(axis, observed, declared):
        if observed is not None:
            want = scope.get(axis, "unknown")
            mismatch = (want == PER_MODEL and not per_model)
            return {"limit": observed, "source": obs_scope, "scope": want,
                    **({"warn": "this plant scopes %s PER MODEL and the only observation is "
                                "plant-wide, so this number may belong to a different model. Make "
                                "one call on this rod to correct it." % axis} if mismatch else {})}
        if declared is not None:
            return {"limit": declared, "source": "declared", "scope": scope.get(axis, "unknown")}
        return {"limit": None, "source": "unknown",
                "scope": scope.get(axis, "unknown"),
                "note": "nobody has looked; this is NOT a statement that it is unlimited"}

    out = {
        "rod": rod, "plant": plant, "local": unstick.is_local(rod),
        "req_min": wall("req_min", obs.get("req_limit_min"), cap.get("rpm")),
        "req_day": wall("req_day", obs.get("req_limit"), cap.get("rpd")),
        "tok_min": wall("tok_min", obs.get("tok_limit"), None),
        "tok_day": wall("tok_day", None, cap.get("tpd")),
        "context": {"limit": ctx, "source": "declared" if ctx else "unknown",
                    "scope": "per call",
                    "note": "the per-CALL ceiling; not a budget that refills"},
        "concurrency": {"limit": LOCAL_CONCURRENCY if unstick.is_local(rod)
                        else cap.get("max_inflight"),
                        "source": "measured" if unstick.is_local(rod) else "declared",
                        "scope": scope.get("concurrency", "per model")},
        "tok_s": tps,
    }
    return out


def binds(rod: str, calls: int, tokens_each: int = 550) -> dict:
    """WHICH WALL THIS JOB HITS FIRST, and how long it takes to get there.

    This is the question a selector actually has to answer and none of the six could: not "is this
    rod good" but "can this FUEL deliver a job of THIS SHAPE". Many small calls bind on requests per
    minute; few large calls bind on tokens per minute or on the context window; local work binds on
    wall clock, because ollama serialises.

    An axis nobody has measured is listed under `unknown` and explicitly does NOT count as passable.
    """
    c = capacity(rod)
    walls, unknown = [], []

    per_call = tokens_each
    ctx = c["context"]["limit"]
    if ctx and per_call > ctx:
        return {"rod": rod, "ok": False, "bound_by": "context",
                "why": "%d tokens per call exceeds this rod's %d-token context window; no amount of "
                       "waiting fixes a call that does not fit" % (per_call, ctx)}

    if c["local"]:
        # No quota. The cost is time, and calls serialise behind one resident model.
        if c["tok_s"]:
            hours = (calls * per_call) / float(c["tok_s"]) / 3600.0
            walls.append(("wall clock (local, serialised)", hours))
        else:
            unknown.append("throughput never measured for this local rod")
    else:
        rm = c["req_min"]["limit"]
        walls.append(("requests/min", calls / float(rm) / 60.0)) if rm else \
            unknown.append("requests/min")
        tm = c["tok_min"]["limit"]
        walls.append(("tokens/min", (calls * per_call) / float(tm) / 60.0)) if tm else \
            unknown.append("tokens/min")
        rd = c["req_day"]["limit"]
        if rd and calls > rd:
            return {"rod": rod, "ok": False, "bound_by": "requests/day",
                    "why": "%d calls against a %s cap of %d per day (%s). Running past a daily wall "
                           "writes exhaustion into the record as a capability result - the cells "
                           "past it come back at zero and look exactly like a rod that cannot do "
                           "the task." % (calls, c["req_day"]["scope"], int(rd),
                                          c["req_day"]["source"])}

    if not walls:
        return {"rod": rod, "ok": None, "bound_by": None, "unknown": unknown,
                "why": "no limit has been observed or declared on any axis for this rod. That is an "
                       "admission, not permission - make one call so the headers can be read."}

    bound, hours = max(walls, key=lambda x: x[1])
    ok = hours <= pace.MAX_PLAN_HOURS
    return {"rod": rod, "ok": ok, "bound_by": bound, "hours": round(hours, 2),
            "unknown": unknown, "walls": [(n, round(h, 2)) for n, h in walls],
            "why": ("%d calls x %d tok: %.2f h, bound by %s" % (calls, per_call, hours, bound)
                    if ok else
                    "REFUSED - %.1f h against a %.0f h ceiling, bound by %s"
                    % (hours, pace.MAX_PLAN_HOURS, bound))}


def conflicts() -> list:
    """Hardcoded limits in `grid.PLANTS` against what the plants themselves reported.

    REPORTS, NEVER OVERWRITES. A header is one plant's answer at one moment and a constant carries a
    dated provenance note someone earned; silently preferring either would destroy evidence. The
    output is a disagreement to resolve by hand, which is the correct amount of automation for a
    number that governs whether the system is allowed to make a request.
    """
    seen = pace.known()
    out = []
    for plant, cap in grid.PLANTS.items():
        obs = seen.get(plant) or {}
        if not obs:
            out.append({"plant": plant, "field": "-", "declared": cap.get("rpm"), "observed": None,
                        "verdict": "UNOBSERVED - no call from this process tree has read its headers"})
            continue
        pairs = [("rpm", cap.get("rpm"), obs.get("req_limit_min")),
                 ("rpd", cap.get("rpd"), obs.get("req_limit"))]
        for field, dec, ob in pairs:
            if ob is None:
                continue
            if dec is None:
                out.append({"plant": plant, "field": field, "declared": "UNLIMITED", "observed": ob,
                            "verdict": "DECLARED UNLIMITED, PLANT DISAGREES"})
            elif abs(float(dec) - float(ob)) > 0.5:
                out.append({"plant": plant, "field": field, "declared": dec, "observed": ob,
                            "verdict": "CONFLICT"})
    return out


NEEDS = (
    Need("read a public API and report the number", zone="public", tools=True),
    Need("read this machine's own state, privately", zone="sensitive", tools=True),
    Need("carry a value across steps of a chain", zone="public", suites=("carry",)),
    Need("write code that runs", zone="public", suites=("code",)),
    Need("reason over private data with no tools", zone="private"),
)


def render() -> str:
    L = ["THE DISCRIMINATOR - one requirement in, one rod out, and the reason for every reject",
         "=" * 100]
    for n in NEEDS:
        L.append("")
        L.append("NEED  %s" % n.what)
        L.append("      zone=%s  tools=%s  suites=%s" % (n.zone, n.tools, list(n.suites) or "-"))
        try:
            for i, r in enumerate(fit(n, limit=3)):
                mark = "->" if i == 0 else "  "
                L.append("   %s %-46s %-9s %s" % (mark, r["rod"], r["plant"], r["why"]))
        except NoFit as e:
            L.append("   REFUSED  %s" % e)
        for r in why_not(n, limit=3):
            L.append("      x  %-46s %-10s %s" % (r["rod"], r["gate"], r["why"][:44]))
    return "\n".join(L)


if __name__ == "__main__":
    if "--conflicts" in sys.argv:
        rows = conflicts()
        print("DECLARED (grid.PLANTS, hardcoded) vs OBSERVED (the plant's own headers)")
        print("=" * 92)
        print("%-12s %-8s %-14s %-14s %s" % ("plant", "field", "declared", "observed", "verdict"))
        for r in rows:
            print("%-12s %-8s %-14s %-14s %s"
                  % (r["plant"], r["field"], r["declared"], r["observed"], r["verdict"]))
        print()
        print("Reported, never overwritten. A header is one moment; a constant carries a dated")
        print("provenance note. Resolving them is a human decision about what may be requested.")
        print()
    print(render())
