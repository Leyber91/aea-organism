"""pace.py - THE PLANTS PUBLISH THEIR LIMITS. READ THEM INSTEAD OF GUESSING.

WHAT WAS WRONG, AND IT COST A DAY OF WALL CLOCK. The lab paced itself with a fixed per-plant
semaphore of `max_inflight // 2` and exponential backoff on 429. Both halves are blind. The semaphore
is a number somebody typed; the backoff only learns after a request has already been refused. So the
lab was simultaneously TOO SLOW on a plant with capacity and TOO FAST on a plant without, and it
could not tell which was which.

Every OpenAI-compatible plant answers with its exact remaining budget on EVERY response:

    groq        x-ratelimit-limit-tokens 6000        reset-tokens 5.14s
    cerebras    x-ratelimit-limit-requests-minute 5  limit-requests-hour 150

MEASURED 2026-07-27, AND THIS IS WHY IT MATTERS. Cerebras allows FIVE REQUESTS PER MINUTE. x24's
cerebras cells are 4 containers x 48 sequences x 16 steps = 3072 calls, which is TWENTY HOURS at that
rate. It was never going to finish, and nothing in the lab could say so before starting. Worse, the
run does not fail cleanly: `call_gated` burns its five retries in backoff and returns not-ok, the
sequence is recorded as incomplete, and a RATE LIMIT is written into the archive as a CAPABILITY
result. That already happened once and was misread as a context ceiling.

SO THE FIX IS TWO THINGS, AND THE SECOND MATTERS MORE THAN THE FIRST.

  1 PACE PROACTIVELY. A token bucket per plant, refilled from the headers the plant just sent. Wait
    before being refused rather than after.

  2 REFUSE AN IMPOSSIBLE PLAN BEFORE SPENDING ANYTHING. This is the harness's own discipline applied
    one layer down: it already refuses an experiment with no baseline or with n below the floor. An
    experiment that needs more calls than the plant will serve in a working day is equally unrunnable,
    and it should say so in the first second rather than in the ninth hour.

  python -m aea.lab.pace                     what each plant will currently serve
  python -m aea.lab.pace groq 3072 550       can this plan run? how long?
"""
from __future__ import annotations

import atexit
import os
import re
import sys
import threading
import time

from aea.kernel import grid

_DUR = re.compile(r"(?:(\d+(?:\.\d+)?)h)?(?:(\d+(?:\.\d+)?)m)?(?:(\d+(?:\.\d+)?)s)?$")
_LOCK = threading.Lock()

# WHERE OBSERVED LIMITS LIVE, AND WHY THEY HAVE TO LIVE SOMEWHERE.
#
# `_STATE` was an in-memory dict and nothing else. This module is the ONLY thing in the repo that
# reads a plant's real limits from the plant itself - every other number anywhere is a hand-written
# constant - and it discarded every one of them at process exit. `python -m aea.lab.pace` printed
# "no call observed yet" while the harness in another process held a full picture, and neither could
# see the other. Ground truth that does not outlive the call that produced it is not a source of
# truth; it is a log line.
_PATH = os.path.join(grid.STATE, "pace_observed.json")
_SAVE_EVERY = 5.0                # seconds; observe() is called on every response
_last_save = 0.0


def _read_disk() -> dict:
    return (grid.load_json(_PATH, {"schema": "aea.pace/1", "plants": {}}) or {}).get("plants", {})


def _flush_at_exit():
    """THE THROTTLE NEEDS AN ESCAPE HATCH AND THIS IS IT.

    Without it, `_SAVE_EVERY` silently ate every observation after the first: a probe reading three
    plants in under a second persisted plant one and dropped plants two and three, then exited. The
    conflict report duly said cerebras was UNOBSERVED while `pace.render()` in the same run had just
    printed its live 5/min. A throttle with no flush is not a throttle, it is a filter.
    """
    _persist(force=True)


_STATE: dict = _read_disk()


def _persist(force: bool = False):
    """Merge this process's observations into the shared file, newest-wins per plant.

    Read-modify-write under the same file lock the ledger uses, because two processes observing two
    plants at once must not erase each other. Throttled, since a lab run calls observe() thousands
    of times and the file is not the point of the run.
    """
    global _last_save
    now = time.time()
    if not force and now - _last_save < _SAVE_EVERY:
        return
    _last_save = now
    try:
        with grid.file_lock(_PATH):
            doc = grid.load_json(_PATH, {"schema": "aea.pace/1", "plants": {}})
            disk = doc.setdefault("plants", {})
            for plant, mine in _STATE.items():
                if (mine.get("at") or 0) >= ((disk.get(plant) or {}).get("at") or 0):
                    disk[plant] = dict(mine)
            doc["updated"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
            grid.atomic_save_json(_PATH, doc)
    except Exception:
        pass                      # observing must never break the call that produced the headers


atexit.register(_flush_at_exit)

# A plan needing longer than this is refused rather than started. Not a technical limit - a decision
# about what is worth a working day, stated out loud so it can be argued with.
MAX_PLAN_HOURS = 6.0


def parse_duration(s):
    """Plants write resets as `34m24s`, `5.14s`, `24.25s`. Seconds out, or None."""
    if not s:
        return None
    m = _DUR.match(str(s).strip())
    if not m or not any(m.groups()):
        return None
    h, mi, se = (float(x) if x else 0.0 for x in m.groups())
    return h * 3600 + mi * 60 + se


def observe(plant, headers, model=None):
    """Update what is known from the response just sent. Never invents a limit: a header that is
    absent leaves that field None, and None means unknown, not unlimited.

    RECORDED UNDER THE ROD AS WELL AS THE PLANT, BECAUSE THE QUOTA IS OFTEN NOT THE PLANT'S.
    This keyed by plant alone, and groq is the counter-example that breaks it: `llama-3.1-8b-instant`
    publishes 14400 requests/day and 6000 tokens/min, while `llama-3.3-70b-versatile` on the SAME
    plant publishes 1000/day and 12000 tokens/min. Collapsed to one per-plant record, the last model
    to answer overwrote the others and every reader got a confident number belonging to a different
    model - the 70b's 1000/day wall reported as 14400.

    The plant-level record is kept too: cerebras really is org-scoped, so for that plant the plant
    key is the true one. Which key to trust is a property of the plant, and `fit.SCOPES` says which.
    """
    if not headers:
        return
    h = {str(k).lower(): v for k, v in dict(headers).items()}
    keys = [plant] + (["%s/%s" % (plant, model)] if model else [])

    def num(*names):
        for n in names:
            if n in h:
                try:
                    return float(str(h[n]).strip())
                except ValueError:
                    pass
        return None

    with _LOCK:
        for bucket in keys:
            s = _STATE.setdefault(bucket, {})
            s["at"] = time.time()
            if model:
                s["model"] = model
            for key, names in (
                ("req_limit_min", ("x-ratelimit-limit-requests-minute",)),
                ("req_left_min", ("x-ratelimit-remaining-requests-minute",)),
                ("req_limit_hour", ("x-ratelimit-limit-requests-hour",)),
                ("req_left_hour", ("x-ratelimit-remaining-requests-hour",)),
                ("req_limit", ("x-ratelimit-limit-requests", "x-ratelimit-limit-requests-day")),
                ("req_left", ("x-ratelimit-remaining-requests",
                              "x-ratelimit-remaining-requests-day")),
                ("tok_limit", ("x-ratelimit-limit-tokens", "x-ratelimit-limit-tokens-minute")),
                ("tok_left", ("x-ratelimit-remaining-tokens",
                              "x-ratelimit-remaining-tokens-minute")),
            ):
                v = num(*names)
                if v is not None:
                    s[key] = v
            for key, names in (("req_reset", ("x-ratelimit-reset-requests",)),
                               ("tok_reset", ("x-ratelimit-reset-tokens",))):
                d = parse_duration(h.get(names[0]))
                if d is not None:
                    s[key] = d
    _persist()


def known(plant=None):
    with _LOCK:
        return dict(_STATE.get(plant, {})) if plant else {k: dict(v) for k, v in _STATE.items()}


def per_minute(plant):
    """Calls per minute this plant will serve, as far as anything is known. None when unknown -
    and unknown is reported as unknown rather than defaulted to a comfortable number."""
    s = known(plant)
    if not s:
        return None
    if s.get("req_limit_min"):
        return s["req_limit_min"]
    if s.get("req_limit_hour"):
        return s["req_limit_hour"] / 60.0
    return None


def tokens_per_minute(plant):
    s = known(plant)
    lim, reset = s.get("tok_limit"), s.get("tok_reset")
    if not lim:
        return None
    # A token limit whose window resets in seconds is a per-minute bucket. Where the window is not
    # stated, the per-minute reading is the honest one to assume and it is labelled as an assumption.
    return lim if (reset is None or reset <= 70) else lim


def day_budget(plant):
    """Requests left today, if the plant says. THE DAILY CAP IS THE ONE THAT BITES SILENTLY.

    Measured 2026-07-27, and it happened live while this file was being written:
    groq/llama-3.3-70b-versatile publishes a limit of 1000 requests per DAY - not per minute - and
    resets on a rolling ~7h window. Two runs drawing on it at once took it to 721 remaining while
    x24 still needed roughly 1700. The cells that ran past the wall came back `correct 0/48` with
    6 probes out of 288, beside 37/48 and 144/144 on an unthrottled rod running the SAME container.

    Nothing in the run could tell those apart. A per-minute limit announces itself as slowness; a
    daily cap announces itself as a rod that suddenly cannot do the task, which is indistinguishable
    from a finding. This is the reason to check before the run and not after.
    """
    s = known(plant)
    left = s.get("req_left")
    lim = s.get("req_limit")
    if left is None:
        return None
    return {"remaining": left, "limit": lim, "resets_in_s": s.get("req_reset")}


def afford(plant, calls):
    """Can today's remaining budget cover this many calls? Answered before the first one is spent."""
    b = day_budget(plant)
    if not b:
        return {"known": False, "verdict": "no daily budget observed for %s - make one call so the "
                                           "headers can be read" % plant}
    ok = b["remaining"] >= calls
    return {"known": True, "ok": ok, "remaining": b["remaining"], "needs": calls,
            "verdict": ("%d of %d remaining today, enough" % (b["remaining"], b["limit"] or 0) if ok
                        else "REFUSED - needs %d calls, %d left today, resets in %s. Running past "
                             "this writes exhaustion into the archive as a capability result: the "
                             "cells past the wall come back at zero and look exactly like a rod "
                             "that cannot do the task."
                             % (calls, b["remaining"],
                                ("%.0f min" % (b["resets_in_s"] / 60) if b.get("resets_in_s")
                                 else "unknown")))}


def feasibility(plant, calls, tokens_each=None):
    """Can this plan run, and how long will it take? Answered BEFORE anything is spent.

    Returns `hours=None` when the plant publishes no limit we have seen. That is not permission -
    it is an admission, and the caller is told so rather than being given a reassuring number.
    """
    rpm = per_minute(plant)
    tpm = tokens_per_minute(plant) if tokens_each else None
    limits = []
    if rpm:
        limits.append(("requests", calls / rpm / 60.0))
    if tpm and tokens_each:
        limits.append(("tokens", (calls * tokens_each) / tpm / 60.0))
    if not limits:
        return {"plant": plant, "calls": calls, "hours": None, "bound_by": None,
                "verdict": "UNKNOWN - no published limit has been observed for this plant. Make one "
                           "call first so the headers can be read, then ask again."}
    bound, hours = max(limits, key=lambda x: x[1])
    ok = hours <= MAX_PLAN_HOURS
    return {"plant": plant, "calls": calls, "hours": round(hours, 2), "bound_by": bound,
            "per_minute": rpm, "tokens_per_minute": tpm, "ok": ok,
            "verdict": ("runnable in %.1f h, bound by %s" % (hours, bound) if ok else
                        "REFUSED - %.1f h against a ceiling of %.0f h, bound by %s. Cut the cell "
                        "count, shorten the chain, or move this arm to another plant. A run that "
                        "cannot finish writes rate limits into the archive as capability results."
                        % (hours, MAX_PLAN_HOURS, bound))}


def plan(plants_calls, tokens_each=550):
    """Feasibility for a whole experiment: {plant: n_calls}. The slowest plant is the run."""
    rows = [feasibility(p, n, tokens_each) for p, n in plants_calls.items()]
    known_h = [r["hours"] for r in rows if r["hours"] is not None]
    return {"rows": rows, "wall_clock_hours": max(known_h) if known_h else None,
            "refused": [r for r in rows if r.get("ok") is False],
            "unknown": [r["plant"] for r in rows if r["hours"] is None]}


def wait(plant, tokens=550):
    """Block until this plant can take another call. Proactive: the sleep happens BEFORE the request
    rather than after a 429, so a refusal is never written into the reliability figures as the rod's
    fault. Returns the seconds waited, which is worth recording."""
    rpm = per_minute(plant)
    if not rpm:
        return 0.0
    gap = 60.0 / rpm
    with _LOCK:
        s = _STATE.setdefault(plant, {})
        nxt = s.get("_next", 0.0)
        now = time.time()
        start = max(now, nxt)
        s["_next"] = start + gap
    d = start - time.time()
    if d > 0:
        time.sleep(d)
        return round(d, 2)
    return 0.0


def render():
    L = ["%-11s %-14s %-14s %-13s %s"
         % ("PLANT", "REQ/MIN", "TOKENS/MIN", "OBSERVED", "NOTE")]
    for p in sorted(grid.PLANTS):
        s = known(p)
        if not s:
            L.append("%-11s %-14s %-14s %-13s %s"
                     % (p, "-", "-", "never", "no call observed yet; unknown, not unlimited"))
            continue
        L.append("%-11s %-14s %-14s %-13s %s"
                 % (p, per_minute(p) or "-", tokens_per_minute(p) or "-",
                    "%.0fs ago" % (time.time() - s["at"]),
                    "day cap %s" % int(s["req_limit"]) if s.get("req_limit") else ""))
    return "\n".join(L)


def probe(plant, model):
    """One cheap call, purely to read the headers. The only honest way to learn a limit."""
    from aea.lab import harness as H
    r = H.call_gated(plant, model, [{"role": "user", "content": "hi"}], max_tokens=4, tries=1)
    return r


if __name__ == "__main__":
    # `python -m aea.lab.pace` imports this file TWICE - once as __main__ and once as
    # aea.lab.pace when harness does `from aea.lab import pace`. Two module objects, two _STATE
    # dicts, and the CLI reads the one the harness never wrote to. Use the package copy for
    # everything below so the CLI sees what the wire sees.
    from aea.lab import pace as P

    RODS = {"groq": "llama-3.1-8b-instant", "cerebras": "gpt-oss-120b",
            "nvidia": "openai/gpt-oss-20b"}
    if len(sys.argv) >= 3:
        p, n = sys.argv[1], int(sys.argv[2])
        t = int(sys.argv[3]) if len(sys.argv) > 3 else 550
        P.probe(p, RODS.get(p, "llama-3.1-8b-instant"))
        print("%s  %d calls at ~%d tokens" % (p, n, t))
        print("  %s" % P.feasibility(p, n, t)["verdict"])
    else:
        for p, m in RODS.items():
            P.probe(p, m)
        print(P.render())
