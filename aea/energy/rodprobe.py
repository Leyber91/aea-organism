"""rodprobe.py - ONE HARNESS FOR ASKING A ROD ANYTHING, AND ONE STORE FOR WHAT IT ANSWERED.

WHY THIS EXISTS. In one session, sixteen throwaway probes were written and every one of them
re-implemented the same four things: an untimed POST, the reasoning-versus-content parse, the
per-model parameter lookup, and a concurrent map with a result table. That is fifteen copies of one
module, and law W1 says a behaviour you repeat that a machine could do belongs to the machine.

AND THE MEASUREMENTS WENT NOWHERE. Six stores holding 148KB of real findings, and not one line of
this repo read any of them. A measurement nothing reads is a measurement that will be taken again.
So this file also owns `state/rods.json`, the single place a rod fact lives, and `grid.own_params`
and `grid.think_off` read it before falling back to their literal tables.

  python -m aea.energy.rodprobe --consolidate   fold the scattered stores into state/rods.json
  python -m aea.energy.rodprobe --show          what is known about every rod, one line each

THE TRANSPORT RULE. `timeout=None` is an INACTIVITY budget rather than a deadline, so a rod gets as
long as it needs. Luis, 2026-07-25: a slow rod scored as unreliable is the same class of error as
counting an outage as a wrong answer. Every probe in this file inherits that.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from aea.kernel import grid

STORE = os.path.join(grid.STATE, "rods.json")

# the scattered stores this folds together, and which key each one contributes
SOURCES = {
    "nvidia_catalog.json":    ("models", "id", ("state", "seconds", "context", "commercial")),
    "nvidia_kinds.json":      ("models", "id", ("kind", "params_b", "endpoints", "local_worth")),
    "nvidia_owncall.json":    ("models", "id", ("published", "endpoint", "think_marks")),
    "nvidia_battery.json":    ("models", "id", ("state", "detail", "secs")),
    "orchestrator_test.json": ("models", "id", ("modes", "tool")),
    "dialogue_test.json":     ("models", "id", ("recall", "held_constraint", "used_result")),
}


# --------------------------------------------------------------------------- the transport
IDLE = 300      # seconds of SILENCE tolerated on one socket read, not a deadline on the exchange


def ask(plant: str, path: str, body: dict, key: str = None, timeout=IDLE,
        wait: bool = True) -> tuple:
    """One request THROUGH THE METER, on an INACTIVITY budget. Returns (parsed, seconds, error).

    NOT `timeout=None`. THAT IS NOT PATIENCE, IT IS A HANG. Luis's rule is that a slow rod must
    never be cut off, and `None` was the wrong way to obey it: urllib applies the value per blocking
    socket operation, so None means a peer that stops sending WITHOUT CLOSING blocks the thread
    forever. MEASURED 2026-07-28: two experiments sat for 28 and 64 minutes on ~1s of CPU each,
    produced nothing, and had to be killed. IDLE=300 lets a reasoner think five minutes between
    bytes, which is far beyond the 66s worst case ever observed here, and still ends a dead socket.


    GOING AROUND THE METER IS HOW YOU CAUSE THE 429 YOU THEN RECORD AS A ROD DEFECT. Every probe
    written today posted with raw urllib and earned exactly that: eight workers on one reader
    against a ceiling the Meter already knew. `grid.METER` measured the real limit on 2026-07-25 and
    it is CONCURRENCY PER ROD (~25, guarded at 20), not the published 40 rpm and not shared across
    the plant, so spreading across rods costs nothing and saturating one costs everything.

    `wait=True` sleeps until a slot frees rather than failing, because a rate limit is our problem
    and a rod must never be scored for it. An HTTP error returns as a STRING rather than raising,
    for the same reason.
    """
    model = body.get("model") or ""
    base = grid.PLANTS[plant]["base"] if plant in grid.PLANTS else plant
    key = key or (grid.key(grid.PLANTS[plant]["auth"]) if plant in grid.PLANTS else None)
    metered = plant in grid.PLANTS
    t0 = time.time()

    if metered:
        # try_enter CHECKS AND CLAIMS ATOMICALLY. can_spend-then-enter is a check-then-act race that
        # measured 15 x 429 out of 30 concurrent calls: every thread read inflight=0 before any of
        # them had claimed. The budget checks (rpd, tokens/day, 429 cooldown) still come from
        # can_spend, which is not racy because those counters are not claimed per request.
        claimed = False
        for _ in range(240):                       # ~20 minutes of patience, then say so honestly
            ok, wait_s, why = grid.METER.can_spend(plant, model)
            if ok and grid.METER.try_enter(plant, model):
                claimed = True
                break
            if not wait:
                return None, round(time.time() - t0, 1), "metered: %s" % (why if not ok
                                                                          else "rod saturated")
            time.sleep(min(5.0, wait_s or 0.35))
        if not claimed:
            return None, round(time.time() - t0, 1), "metered: never freed"
    try:
        data = json.dumps(body).encode()
        head = {"Content-Type": "application/json", "Accept": "application/json"}
        if key:
            head["Authorization"] = "Bearer " + key
        # PLANTS bases already carry their version segment, so `/v1` + `/v1/chat/completions`
        # builds `/v1/v1/...` and returns a bare "404 page not found" that reads exactly like a
        # missing model. Caught by a load test that was looking for something else entirely.
        url = base.rstrip("/")
        seg = path.lstrip("/").split("/")[0]
        req = urllib.request.Request(
            url + (path[len(seg) + 1:] if url.endswith("/" + seg) else path), data, head)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
        if metered:
            grid.METER.record(plant, model,
                              tokens=((d.get("usage") or {}).get("total_tokens") or 0))
        return d, round(time.time() - t0, 1), None
    except urllib.error.HTTPError as e:
        body_txt = e.read()[:160].decode("utf-8", "replace").replace("\n", " ")
        if metered and e.code == 429:
            grid.METER.mark_throttled(plant, model)   # OUR fault, recorded against the bucket
        return None, round(time.time() - t0, 1), "HTTP%d %s" % (e.code, body_txt)
    except Exception as e:
        return None, round(time.time() - t0, 1), "%s %s" % (type(e).__name__, str(e)[:110])
    finally:
        if metered:
            grid.METER.leave(plant, model)            # ALWAYS: a leaked slot shrinks the rod forever


def reply_of(d: dict) -> tuple:
    """(content, reasoning, message). THREE FIELD NAMES, NOT TWO - nvidia uses reasoning_content,
    others use reasoning, and some rods inline the trace in content behind a </think>. Reading only
    one blanks an entire arm, which grid.py already learned the hard way."""
    m = ((d.get("choices") or [{}])[0].get("message")) or {}
    think = m.get("reasoning_content") or m.get("reasoning") or ""
    content = m.get("content") or ""
    if "</think>" in content:
        think = think or content.split("</think>")[0]
        content = content.split("</think>")[-1]
    return content.strip(), think, m


def body_for(model: str, messages: list, **over) -> dict:
    """A request built on THIS model's published parameters. The repo's whole measurement history
    was taken at temperature=0.2/max_tokens=256 while the owners publish 0.2-1.0 and 1024-20480,
    so a probe that ignores them is measuring our defaults rather than the rod."""
    body = dict(grid.own_params(model) or {})
    body.setdefault("max_tokens", 1024)
    body.update(model=model, messages=messages)
    body.update(over)
    return body


def sweep(items, fn, workers: int = 10) -> list:
    """Run fn over items concurrently and keep the order. Failures come back as dicts rather than
    raising, so one dead rod never voids the sweep."""
    def guard(x):
        try:
            return fn(x)
        except Exception as e:
            return {"item": str(x)[:60], "error": "%s %s" % (type(e).__name__, str(e)[:90])}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(guard, items))


# --------------------------------------------------------------------------- the real ceiling
CEILING = os.path.join(grid.STATE, "plant_ceiling.json")


def calibrate(plant: str, model: str, steps=(1, 2, 4, 8, 16, 24), tokens: int = 4) -> dict:
    """FIND THE CONCURRENCY A ROD ACTUALLY TOLERATES, instead of trusting a constant.

    `PLANTS["nvidia"]["max_inflight"] = 20` rests on a 2026-07-25 measurement (50 concurrent -> 25
    ok / 25 rejected). On 2026-07-28 that did not reproduce: 30 concurrent yielded 15-17 x 429 even
    through an atomic claim, some after waiting a full minute for a legitimately free slot. A stale
    ceiling is worse than no ceiling, because it is trusted.

    Ramps concurrency and records the LARGEST step that returned zero 429s. Deliberately small
    outputs: this measures admission, not generation. Writes state/plant_ceiling.json so the answer
    is a measurement with a date rather than a number in the source.
    """
    body = lambda: dict(model=model, messages=[{"role": "user", "content": "Say OK."}],
                        max_tokens=tokens)
    rows, best = [], 0
    for n in steps:
        def one(_):
            # wait=False: this MEASURES the endpoint's admission, so our own queueing must not hide
            # it. A calibration that waits for a slot measures the meter, not the plant.
            d, s, e = ask(plant, "/v1/chat/completions", body(), wait=False)
            return e
        errs = sweep(range(n), one, workers=n)
        throttled = sum(1 for e in errs if e and "429" in str(e))
        other = sum(1 for e in errs if e and "429" not in str(e))
        rows.append({"concurrency": n, "throttled": throttled, "other_errors": other,
                     "ok": n - throttled - other})
        if throttled == 0 and other == 0:
            best = n
        else:
            break                                  # the first step that rejects IS the ceiling
        time.sleep(3)                              # let the window drain before the next step
    doc = grid.load_json(CEILING, {"schema": "aea.plant_ceiling/1", "plants": {}})
    doc["plants"][plant] = {"measured_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                            "on_model": model, "clean_at": best,
                            "declared_max_inflight": grid.PLANTS.get(plant, {}).get("max_inflight"),
                            "ramp": rows}
    grid.atomic_save_json(CEILING, doc, indent=1)
    return doc["plants"][plant]


# --------------------------------------------------------------------------- the store
def load() -> dict:
    return grid.load_json(STORE, {"schema": "aea.rods/1", "rods": {}}).get("rods", {})


def facts(rod: str) -> dict:
    """Everything measured about one rod, or {} when nothing is. Never a guess."""
    return load().get(rod, {})


def consolidate() -> dict:
    """Fold every scattered probe store into one keyed record. Merges rather than overwrites, so
    running one probe alone cannot silently drop the other eight."""
    out = load()
    for fname, (listkey, idkey, fields) in SOURCES.items():
        doc = grid.load_json(os.path.join(grid.STATE, fname), {})
        for row in doc.get(listkey) or []:
            rid = row.get(idkey)
            if not rid:
                continue
            rec = out.setdefault(rid, {"id": rid})
            for f in fields:
                if row.get(f) not in (None, "", [], {}):
                    rec[f if f != "state" else fname.split(".")[0] + "_state"] = row[f]
    grid.atomic_save_json(STORE, {"schema": "aea.rods/1",
                                  "generated": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                                  "rods": out}, indent=1)
    return out


def render(rods: dict) -> str:
    L = ["RODS - every measured fact, in one place (%d rods)" % len(rods), "=" * 108,
         "%-46s %-9s %-7s %-9s %-22s %s" % ("rod", "kind", "ctx", "served", "own params", "tools")]
    for rid, r in sorted(rods.items()):
        pub = r.get("published") or {}
        tool = ((r.get("tool") or {}).get("state")) or "-"
        L.append("%-46s %-9s %-7s %-9s %-22s %s"
                 % (rid[:45], r.get("kind") or "-", r.get("context") or "-",
                    r.get("nvidia_catalog_state") or "-",
                    ("t=%s p=%s m=%s" % (pub.get("temperature"), pub.get("top_p"),
                                         pub.get("max_tokens"))) if pub else "-", tool))
    known = sum(1 for r in rods.values() if r.get("published"))
    L += ["", "%d of %d carry their owner's published parameters. The rest fall back to house "
              "defaults, and that difference is recorded rather than hidden." % (known, len(rods))]
    return "\n".join(L)


if __name__ == "__main__":
    if "--consolidate" in sys.argv:
        rods = consolidate()
        print("consolidated %d rods into %s" % (len(rods), STORE))
    else:
        rods = load()
        if not rods:
            rods = consolidate()
    print(render(rods))
