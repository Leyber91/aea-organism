"""fuels.py - OUR OWN CATALOGUE OF RODS, AND OUR OWN BENCHMARK OF THEM.

WHAT WAS THERE INSTEAD. `aea/mind/fuel.py` holds `KNOWN`, a hand-typed dict of about twelve rods
whose `size` and `family` are read off the model NAME - "3b" because the string says 3b. One plant
alone serves 102 models. So the lab has been choosing rods from a list somebody remembered, and
describing them with properties nobody measured.

THREE TIERS, AND THEY ARE NEVER MIXED. This is the honesty law applied to the fleet:

  DECLARED   what the plant's own /models endpoint says. Free, and it is a claim, not a measurement.
  PROBED     what one cheap call showed: reachable, latency, whether it emits reasoning as its
             visible text, whether it obeys a format instruction. Costs one call per rod.
  MEASURED   what this rod actually did in a recorded experiment - accuracy, per-step chain
             tolerance, parse compliance. Costs a run, and only the archive can supply it.

A rod with no MEASURED block is not "average". It is unmeasured, and it renders as such. That
distinction is the entire point: Law IV says a capability score is a property of a MODULE-ON-A-FUEL
pairing, so a fleet list without measurements is a menu, not a benchmark.

WHY THE PROBE ASKS WHAT IT ASKS. Every field is a defect this lab already paid for:
  reasoning_visible   two rods emitted chain-of-thought AS their reply text and every read broke
  obeys_format        parse-failure ran at 0.40 on one rod and was scored as wrong answers
  first_byte_s        a reasoning rod thinking for minutes and a dead socket look identical

  python -m aea.lab.fuels --discover      pull every plant's catalogue (no model calls)
  python -m aea.lab.fuels --probe groq    one cheap call per rod on that plant
  python -m aea.lab.fuels                 show what is known, and what is not
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request

from aea.kernel import grid

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "organisms", "fuels.json")
SCHEMA = "aea.lab.fuels/1"

# The probe. One question with a checkable answer and a format demand, so a single cheap call
# reports reachability, latency, whether the rod narrates its reasoning, and whether it complies.
PROBE_Q = ("What is 4817 plus 2996? Show the addition on one line, then end your reply with a final "
           "line of exactly: ANSWER: <the integer>")
PROBE_TRUTH = 7813


def load():
    return grid.load_json(PATH, {"schema": SCHEMA, "rods": {}})


def save(doc):
    doc["updated"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    grid.atomic_save_json(PATH, doc)


def discover(plants=None):
    """DECLARED tier. Ask each plant what it serves. No model calls, so this is free and it is also
    the only tier that can be trusted to be complete."""
    doc = load()
    for plant in (plants or list(grid.PLANTS)):
        cap = grid.PLANTS.get(plant) or {}
        if not cap.get("base"):
            continue
        headers = {"User-Agent": "Mozilla/5.0 aea-grid/0.1"}
        if cap.get("auth"):
            k = grid.key(cap["auth"])
            if not k:
                continue
            headers["Authorization"] = "Bearer " + k
        try:
            req = urllib.request.Request(cap["base"].rstrip("/") + "/models", headers=headers)
            data = json.load(urllib.request.urlopen(req, timeout=25))
        except Exception as e:
            print("  %-11s catalogue unreachable: %s" % (plant, str(e)[:60]))
            continue
        models = data.get("data") or data.get("models") or []
        for m in models:
            mid = m.get("id") or m.get("name")
            if not mid:
                continue
            rod = "%s/%s" % (plant, mid)
            r = doc["rods"].setdefault(rod, {"rod": rod, "plant": plant, "model": mid})
            r["declared"] = {"owned_by": m.get("owned_by"), "created": m.get("created"),
                             "context": m.get("context_window") or m.get("max_context_length"),
                             "seen": time.strftime("%Y-%m-%d", time.gmtime())}
        print("  %-11s %d models declared" % (plant, len(models)))
    save(doc)
    return doc


def probe_one(plant, model, max_tokens=400, timeout=90):
    """PROBED tier. One unstreamed call, read at the JSON level so nothing is inferred.

    EVERY FIELD IS A DEFECT THIS LAB ALREADY PAID FOR, and one of them was found while writing it:

      reasoning_content   SOME RODS RETURN REASONING IN A SEPARATE FIELD. `openai/gpt-oss-20b` puts
                          its chain of thought in `message.reasoning_content` and its answer in
                          `message.content`. The streaming reader in harness.py does
                          `content or reasoning_content or reasoning`, so on any chunk where content
                          is empty it appends REASONING INTO THE REPLY TEXT. That is why every
                          gpt-oss reply in this archive opens "The user says...". The two fields are
                          recorded separately here so a rod that needs the split is known BEFORE it
                          is seated, not after its numbers look strange.
      finish_reason       `length` means truncated. Defect 1 was a truncation scored as a capability
                          difference; this is the field that would have caught it, unread until now.
      status_class        a 410 Gone and a wrong answer are not the same event. The declared
                          catalogue lists models the plant no longer serves.
      tokens_per_second   the only honest way to plan a long run; latency alone hides a slow decoder.
    """
    import json as _json
    import re
    import urllib.error
    import urllib.request
    cap = grid.PLANTS.get(plant) or {}
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea-grid/0.1"}
    if cap.get("auth"):
        k = grid.key(cap["auth"])
        if not k:
            return {"reachable": False, "error": "no key", "status_class": "no-key"}
        headers["Authorization"] = "Bearer " + k
    body = _json.dumps({"model": model, "temperature": 0.2, "max_tokens": max_tokens,
                        "messages": [{"role": "user", "content": PROBE_Q}]}).encode()
    t0 = time.time()
    try:
        req = urllib.request.Request(cap["base"].rstrip("/") + "/chat/completions",
                                     data=body, headers=headers)
        resp = urllib.request.urlopen(req, timeout=timeout)
        doc = _json.load(resp)
        from aea.lab import pace
        pace.observe(plant, resp.headers, model=model)
    except urllib.error.HTTPError as e:
        return {"reachable": False, "http": e.code, "seconds": round(time.time() - t0, 2),
                "status_class": {404: "not-served", 410: "withdrawn", 401: "unauthorised",
                                 429: "rate-limited"}.get(e.code, "http-error"),
                "error": (e.read().decode("utf-8", "ignore")[:160] if hasattr(e, "read") else ""),
                "at": time.strftime("%Y-%m-%d", time.gmtime())}
    except Exception as e:
        return {"reachable": False, "seconds": round(time.time() - t0, 2),
                "status_class": "transport", "error": "%s: %s" % (type(e).__name__, str(e)[:120]),
                "at": time.strftime("%Y-%m-%d", time.gmtime())}

    dt = round(time.time() - t0, 2)
    ch = ((doc.get("choices") or [{}])[0]) or {}
    msg = ch.get("message") or {}
    content = msg.get("content") or ""
    reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
    usage = doc.get("usage") or {}
    out = usage.get("completion_tokens")
    anchored = re.findall(r"(?im)^\s*ANSWER:\s*(-?\d{1,9})\s*$", content)
    return {
        "reachable": True, "status_class": "ok", "seconds": dt,
        "finish_reason": ch.get("finish_reason"),
        "truncated": ch.get("finish_reason") == "length",
        "tok_in": usage.get("prompt_tokens"), "tok_out": out,
        "tokens_per_second": round(out / dt, 1) if (out and dt) else None,
        # THE SPLIT THAT BREAKS THE READER. Recorded per rod, before it is ever seated.
        "separate_reasoning_field": bool(reasoning),
        "reasoning_chars": len(reasoning), "content_chars": len(content),
        "obeys_format": bool(anchored),
        "correct": bool(anchored) and int(anchored[-1]) == PROBE_TRUTH,
        "reply": content[:400],
        "at": time.strftime("%Y-%m-%d", time.gmtime()),
    }


def probe(plant, limit=None, contains=None, workers=12):
    """Probe every rod on a plant, CONCURRENTLY ACROSS MODELS.

    The concurrency is safe and it is the whole reason this is cheap: rate limits on these plants
    are PER MODEL, measured 2026-07-27 - two groq models on one key report reset windows 31 minutes
    and 6h51m apart, and nvidia serves 40 calls per minute per model. So one call each to 102
    different models is one call against 102 separate buckets, not 102 against one. Probing the
    whole catalogue costs about as much as probing a single rod twice.
    """
    import concurrent.futures as _f
    doc = load()
    rods = [r for r in doc["rods"].values() if r["plant"] == plant
            and (not contains or contains in r["model"])]
    rods = rods[:limit] if limit else rods
    print("  probing %d rods on %s, %d at a time (per-model buckets)\n" % (len(rods), plant, workers))
    done = 0
    with _f.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(probe_one, plant, r["model"]): r for r in rods}
        for fut in _f.as_completed(futs):
            r = futs[fut]
            try:
                p = fut.result()
            except Exception as e:
                p = {"reachable": False, "status_class": "probe-error", "error": str(e)[:120]}
            r["probed"] = p
            done += 1
            if done % 10 == 0:
                save(doc)
            print("    %-44s %-11s %6ss %6s tok/s  fmt=%-5s ok=%-5s %s"
                  % (r["model"][:43], p.get("status_class"), p.get("seconds", "-"),
                     p.get("tokens_per_second") or "-", p.get("obeys_format"), p.get("correct"),
                     "SPLIT-REASONING" if p.get("separate_reasoning_field") else
                     ("TRUNCATED" if p.get("truncated") else "")), flush=True)
    save(doc)
    return doc


def harvest():
    """MEASURED tier. Pull every per-rod result the archive already holds. Costs nothing: these
    calls were bought once and the numbers are sitting in the run files unread."""
    doc = load()
    d = os.path.join(grid.STATE, "lab", "runs")
    seen = {}
    for e in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        p = os.path.join(d, e)
        fs = sorted(f for f in os.listdir(p) if f.endswith(".json"))
        if not fs:
            continue
        run = grid.load_json(os.path.join(p, fs[-1]), {}) or {}
        for row in run.get("rows", []):
            rod = row.get("rod")
            if not rod or not isinstance(rod, str) or "/" not in rod:
                continue
            s = seen.setdefault(rod, {"experiments": [], "cells": 0})
            if e not in s["experiments"]:
                s["experiments"].append(e)
            s["cells"] += 1
            for key, field in (("correct", "sequence_correct"),
                               ("per_step_descriptive", "per_step"),
                               ("parse_fail_steps", "parse_fail"),
                               ("token_retrieval", "token_retrieval")):
                v = row.get(key)
                if isinstance(v, dict) and v.get("rate") is not None:
                    s.setdefault(field, []).append(v["rate"])
            if row.get("kind") == "pilot" and row.get("per_step_accuracy") is not None:
                s.setdefault("pilot_per_step", []).append(row["per_step_accuracy"])
                s["chain_length_tolerated"] = row.get("length_chosen")
    for rod, s in seen.items():
        r = doc["rods"].setdefault(rod, {"rod": rod, "plant": rod.split("/")[0],
                                         "model": rod.split("/", 1)[1]})
        m = {"experiments": s["experiments"], "cells": s["cells"]}
        for f in ("sequence_correct", "per_step", "parse_fail", "token_retrieval",
                  "pilot_per_step"):
            if s.get(f):
                m[f] = {"mean": round(sum(s[f]) / len(s[f]), 3), "n_cells": len(s[f])}
        if s.get("chain_length_tolerated"):
            m["chain_length_tolerated"] = s["chain_length_tolerated"]
        r["measured"] = m
    save(doc)
    return doc


def render(doc=None):
    doc = doc or load()
    rods = list(doc["rods"].values())
    meas = [r for r in rods if r.get("measured")]
    prob = [r for r in rods if r.get("probed")]
    L = ["%d rods declared across %d plants" % (len(rods), len({r["plant"] for r in rods})),
         "%d probed, %d measured in a real experiment" % (len(prob), len(meas)), ""]
    L.append("%-44s %-9s %-9s %-9s %-6s %s"
             % ("ROD", "PROBED", "FORMAT", "PER-STEP", "LEN", "EXPERIMENTS"))
    for r in sorted(meas, key=lambda x: -(x["measured"].get("cells") or 0)):
        m, p = r["measured"], r.get("probed") or {}
        ps = m.get("pilot_per_step") or m.get("per_step") or {}
        L.append("%-44s %-9s %-9s %-9s %-6s %s"
                 % (r["rod"][:43],
                    ("%ss" % p.get("seconds")) if p else "-",
                    str(p.get("obeys_format")) if p else "-",
                    ("%.3f" % ps["mean"]) if ps.get("mean") is not None else "-",
                    m.get("chain_length_tolerated") or "-",
                    ",".join(x.split("_")[0] for x in m["experiments"][:5])))
    unmeasured = len(rods) - len(meas)
    L.append("")
    L.append("%d rods are DECLARED and never measured. Unmeasured is not average; a rod with no "
             "run behind it has no capability claim at all." % unmeasured)
    return "\n".join(L)


if __name__ == "__main__":
    if "--discover" in sys.argv:
        print("DECLARED tier - asking each plant what it serves\n")
        discover()
        print("\n" + render())
    elif "--probe" in sys.argv:
        i = sys.argv.index("--probe")
        plant = sys.argv[i + 1] if len(sys.argv) > i + 1 else "groq"
        lim = int(sys.argv[i + 2]) if len(sys.argv) > i + 2 else None
        print("PROBED tier - one cheap call per rod on %s\n" % plant)
        probe(plant, limit=lim)
    else:
        harvest()
        print(render())
