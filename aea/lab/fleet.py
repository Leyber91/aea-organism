"""fleet.py - TEST EVERY ROD, WITH THE TEST IT CAN ACTUALLY SIT.

WHY THIS REPLACES THE FIRST PROBE, AND IT IS A DEFECT OF MINE RATHER THAN OF THE PLANTS. The first
pass sent ONE arithmetic question to all 103 nvidia models and recorded 60 of them as `not-served`.
They are served. `nemotron-3-embed-1b`, `nv-embed-v1`, `arctic-embed-l` and `nv-embedcode-7b-v1` are
EMBEDDING models and the call went to /chat/completions. `magpie-tts-zeroshot` is speech.
`bevformer` and `streampetr` are 3D perception. `esmfold` predicts protein structure. Asking a
protein folder to add two numbers and recording the 404 as a property of the model is the same
mistake as measuring a capability on a task whose precondition does not hold - the oldest void class
in this lab, committed again by me at fleet scale.

SO CLASSIFY FIRST, THEN TEST. A rod is routed to the endpoint and the suite its modality allows, and
a rod whose modality this lab has no suite for is recorded as UNTESTED-BY-DESIGN rather than as
failing.

THE SUITES ARE CHOSEN FOR WHAT THE GAME WILL NEED, NOT FOR WHAT IS EASY TO SCORE:

  reach      it answers at all, how fast, and how many tokens per second
  format     it obeys `ANSWER: <n>`. Parse failure ran at 0.40 on one seated rod and was scored as
             wrong answers for the whole of chapter I
  arith      a two-operand sum. The floor
  carry      four dependent steps. The single thing the 16-step chain experiments actually need
  code       IT WRITES A PYTHON FUNCTION THAT IS EXECUTED AGAINST TEST CASES. Worlds 5 and 6 are
             HAND/ACT and APPRENTICE/CHANGE, where the entity edits its own code. A rod that cannot
             produce a runnable function cannot be seated there, and nothing in this lab has ever
             measured that

CONCURRENCY IS PER MODEL BECAUSE THE BUDGET IS PER MODEL. Measured: nvidia serves ~40 requests per
minute PER MODEL, and two groq models on one key report reset windows six hours apart. So N models
tested at once is N calls against N separate buckets. The fleet is tested wide, never deep - one
model's suite runs serially inside its own bucket while every other model runs in parallel.

  python -m aea.lab.fleet --classify            what each rod is, and which suite it can sit
  python -m aea.lab.fleet --test nvidia         run every applicable suite, wide
  python -m aea.lab.fleet                       the library, as it stands
"""
from __future__ import annotations

import concurrent.futures as _f
import json
import re
import sys
import time

from aea.kernel import grid
from aea.lab import fuels

# --- CLASSIFICATION. Name-based, declared honestly as a heuristic, and every rod records which
# --- rule matched so a misclassification is visible rather than buried.
CLASSES = [
    ("embedding", r"(embed|embedcode)", "/embeddings"),
    ("rerank", r"(rerank|ranking)", "/ranking"),
    ("speech", r"(tts|voice|speech|magpie|studio.voice|noise.removal|riva)", None),
    ("vision-video", r"(cosmos|streampetr|bevformer|sparsedrive|synthetic-video|speaker)", None),
    ("biology", r"(esm2|esmfold)", None),
    ("safety", r"(guard|safety|gliner|content-safety)", "/chat/completions"),
    ("vision-language", r"(vision|-vl\b|paligemma|nemotron-nano-12b-v2-vl|omni)", "/chat/completions"),
    ("chat", r".*", "/chat/completions"),
]

# Suites a class may sit. A rod is never scored on a suite its modality forbids.
ALLOWED = {
    "chat": ["reach", "format", "arith", "carry", "code"],
    "vision-language": ["reach", "format", "arith", "carry", "code"],
    "safety": ["reach"],
    "embedding": ["reach"],
    "rerank": ["reach"],
    "speech": [], "vision-video": [], "biology": [],
}

CODE_TASK = (
    "Write a Python function `f(xs)` that takes a list of integers and returns the sum of the "
    "values that are strictly greater than 10. Reply with the function only, inside a single "
    "```python code block. No explanation."
)
CODE_CASES = [([1, 11, 20, 3], 31), ([], 0), ([10, 10], 0), ([-5, 100], 100)]

CARRY_OPS = [("add 47", 47), ("subtract 128", -128), ("add 356", 356), ("subtract 61", -61)]
CARRY_START = 60122


def classify(model):
    m = model.lower()
    for name, pat, endpoint in CLASSES:
        if re.search(pat, m):
            return {"class": name, "endpoint": endpoint, "matched": pat,
                    "suites": ALLOWED.get(name, [])}
    return {"class": "chat", "endpoint": "/chat/completions", "matched": "fallback",
            "suites": ALLOWED["chat"]}


def _post(plant, path, body, timeout=90):
    import urllib.error
    import urllib.request
    cap = grid.PLANTS.get(plant) or {}
    h = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea-grid/0.1"}
    if cap.get("auth"):
        k = grid.key(cap["auth"])
        if not k:
            return None, "no-key", 0.0
        h["Authorization"] = "Bearer " + k
    t0 = time.time()
    try:
        req = urllib.request.Request(cap["base"].rstrip("/") + path,
                                     data=json.dumps(body).encode(), headers=h)
        return json.load(urllib.request.urlopen(req, timeout=timeout)), None, time.time() - t0
    except urllib.error.HTTPError as e:
        return None, "http-%d" % e.code, time.time() - t0
    except Exception as e:
        return None, type(e).__name__, time.time() - t0


def _chat(plant, model, prompt, max_tokens=600, timeout=90):
    # A LOCAL MODEL MAY HAVE TO BE LOADED FROM DISK BEFORE IT CAN ANSWER. A hosted rod is warm; an
    # ollama model that is not resident costs a multi-second swap first, and a 90s ceiling turns
    # "cold" into "incapable". PLANT_TIMEOUT raises the floor for plants that pay that cost.
    timeout = max(timeout, PLANT_TIMEOUT.get(plant, 0))
    doc, err, dt = _post(plant, "/chat/completions",
                         {"model": model, "temperature": 0.2, "max_tokens": max_tokens,
                          "messages": [{"role": "user", "content": prompt}]}, timeout)
    if err:
        return {"ok": False, "error": err, "seconds": round(dt, 2)}
    ch = ((doc.get("choices") or [{}])[0]) or {}
    msg = ch.get("message") or {}
    u = doc.get("usage") or {}
    return {"ok": True, "seconds": round(dt, 2), "content": msg.get("content") or "",
            # THE SPLIT. Kept apart here, never concatenated, because the streaming reader in
            # harness.py merges them and that is why every gpt-oss reply opens "The user says".
            "reasoning": msg.get("reasoning_content") or msg.get("reasoning") or "",
            "finish": ch.get("finish_reason"), "truncated": ch.get("finish_reason") == "length",
            "tok_out": u.get("completion_tokens"), "tok_in": u.get("prompt_tokens"),
            "tps": round((u.get("completion_tokens") or 0) / dt, 1) if dt else None}


def suite_reach(plant, model):
    r = _chat(plant, model, "Reply with the single word: ready", max_tokens=32, timeout=60)
    return {"pass": bool(r.get("ok")), "seconds": r.get("seconds"), "tps": r.get("tps"),
            "split_reasoning": bool(r.get("reasoning")), "error": r.get("error")}


def suite_format(plant, model):
    r = _chat(plant, model, "What is 4817 plus 2996? End with a final line of exactly: "
                            "ANSWER: <the integer>", max_tokens=500)
    if not r.get("ok"):
        return {"pass": False, "error": r.get("error")}
    a = re.findall(r"(?im)^\s*ANSWER:\s*(-?\d{1,9})\s*$", r["content"])
    return {"pass": bool(a), "correct": bool(a) and int(a[-1]) == 7813,
            "truncated": r.get("truncated"), "seconds": r.get("seconds"), "tps": r.get("tps")}


def suite_arith(plant, model):
    r = _chat(plant, model, "Compute 60122 - 128 + 356. Reply with only the integer.", max_tokens=300)
    if not r.get("ok"):
        return {"pass": False, "error": r.get("error")}
    n = re.findall(r"-?\d+", (r["content"] or "").replace(",", ""))
    return {"pass": bool(n) and int(n[-1]) == 60350, "seconds": r.get("seconds")}


def suite_carry(plant, model):
    """FOUR DEPENDENT STEPS, which is the thing every chain experiment in this lab actually needs.
    Each step is a separate call carrying only a stated running value, so this measures the rod's
    tolerance for a sequence rather than its arithmetic."""
    v, hits = CARRY_START, 0
    for i, (op, delta) in enumerate(CARRY_OPS, 1):
        r = _chat(plant, model,
                  "The running value is %d.\n\nStep %d: %s\nReply with only the resulting integer."
                  % (v, i, op), max_tokens=300)
        if not r.get("ok"):
            return {"pass": False, "steps_hit": hits, "of": len(CARRY_OPS), "error": r.get("error")}
        n = re.findall(r"-?\d+", (r["content"] or "").replace(",", ""))
        want = v + delta
        got = int(n[-1]) if n else None
        if got == want:
            hits += 1
        v = want          # the truth carries forward, never the rod's answer: one slip is one miss
    return {"pass": hits == len(CARRY_OPS), "steps_hit": hits, "of": len(CARRY_OPS)}


def suite_code(plant, model):
    """IT WRITES A FUNCTION AND WE RUN IT. Worlds 5 and 6 are ACT and CHANGE - the entity editing
    its own code - and nothing in this lab has ever measured whether a rod can produce something
    executable. The code runs in a bare namespace with a hard cap on what it can reach."""
    r = _chat(plant, model, CODE_TASK, max_tokens=700)
    if not r.get("ok"):
        return {"pass": False, "error": r.get("error")}
    body = r["content"] or ""
    m = re.search(r"```(?:python)?\s*(.+?)```", body, re.S)
    src = (m.group(1) if m else body).strip()
    if "def f" not in src:
        return {"pass": False, "reason": "no function named f", "seconds": r.get("seconds")}
    ns = {"__builtins__": {"sum": sum, "len": len, "range": range, "int": int, "list": list}}
    try:
        exec(compile(src, "<rod>", "exec"), ns)          # noqa: S102 - the measurement IS execution
        fn = ns.get("f")
        if not callable(fn):
            return {"pass": False, "reason": "f is not callable"}
        passed = sum(1 for xs, want in CODE_CASES if fn(list(xs)) == want)
    except Exception as e:
        return {"pass": False, "reason": "%s: %s" % (type(e).__name__, str(e)[:80]),
                "seconds": r.get("seconds")}
    return {"pass": passed == len(CODE_CASES), "cases": passed, "of": len(CODE_CASES),
            "seconds": r.get("seconds"), "tps": r.get("tps")}


SUITES = {"reach": suite_reach, "format": suite_format, "arith": suite_arith,
          "carry": suite_carry, "code": suite_code}


def test_rod(plant, model, suites):
    """One rod's whole suite, SERIALLY inside its own rate bucket. Wide, never deep."""
    out, t0 = {}, time.time()
    for s in suites:
        out[s] = SUITES[s](plant, model)
        if s == "reach" and not out[s]["pass"]:
            out["_stopped"] = "unreachable; remaining suites not attempted"
            break
    out["_seconds"] = round(time.time() - t0, 1)
    return out


# ONE LOCAL SERVER IS NOT NINETY-SIX INDEPENDENT BUCKETS. nvidia serves ~40 requests per
# minute PER MODEL from separate infrastructure, so testing it wide costs the same as testing one
# rod twice. ollama is one process on one GPU: it holds a couple of models resident and swaps the
# rest from disk, so fourteen concurrent probes queue behind each other and every one times out.
# Measured 2026-07-28: all 14 local models returned at exactly 60.0s, which is the shape of a
# timeout rather than of a capability. The budget is per PLANT here, not per model.
PLANT_WORKERS = {"ollama": 1}
PLANT_TIMEOUT = {"ollama": 240}


def run(plant, workers=None, only_class=None):
    workers = workers or PLANT_WORKERS.get(plant, 14)
    doc = fuels.load()
    rods = [r for r in doc["rods"].values() if r["plant"] == plant]
    for r in rods:
        r["kind"] = classify(r["model"])
    todo = [r for r in rods if r["kind"]["suites"] and
            (not only_class or r["kind"]["class"] == only_class)]
    skipped = [r for r in rods if not r["kind"]["suites"]]
    fuels.save(doc)

    print("  %d rods on %s: %d testable, %d UNTESTED-BY-DESIGN (%s)\n"
          % (len(rods), plant, len(todo), len(skipped),
             ", ".join(sorted({r["kind"]["class"] for r in skipped})) or "-"), flush=True)
    print("  %d models at a time - the budget is per model, so this is wide not deep\n"
          % workers, flush=True)

    done = 0
    with _f.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(test_rod, plant, r["model"], r["kind"]["suites"]): r for r in todo}
        for fut in _f.as_completed(futs):
            r = futs[fut]
            try:
                res = fut.result()
            except Exception as e:
                res = {"_error": str(e)[:120]}
            r["tested"] = res
            done += 1
            if done % 8 == 0:
                fuels.save(doc)
            got = [k for k, v in res.items() if not k.startswith("_") and v.get("pass")]
            print("    %-44s %-15s %-38s %ss"
                  % (r["model"][:43], r["kind"]["class"],
                     ("PASS " + "+".join(got)) if got else "no suite passed",
                     res.get("_seconds")), flush=True)
    fuels.save(doc)
    return doc


def render():
    doc = fuels.load()
    rods = [r for r in doc["rods"].values() if r.get("tested")]
    if not rods:
        return "no rod has been tested yet. run: python -m aea.lab.fleet --test nvidia"
    L = ["%d rods tested\n" % len(rods)]
    L.append("%-44s %-14s %-6s %-7s %-7s %-7s %-7s %s"
             % ("ROD", "CLASS", "REACH", "FORMAT", "ARITH", "CARRY", "CODE", "TOK/S"))

    def mark(t, k):
        v = t.get(k)
        return "-" if v is None else ("yes" if v.get("pass") else "no")
    for r in sorted(rods, key=lambda x: -(((x["tested"].get("reach") or {}).get("tps")) or 0)):
        t = r["tested"]
        L.append("%-44s %-14s %-6s %-7s %-7s %-7s %-7s %s"
                 % (r["model"][:43], r["kind"]["class"], mark(t, "reach"), mark(t, "format"),
                    mark(t, "arith"), mark(t, "carry"), mark(t, "code"),
                    (t.get("reach") or {}).get("tps") or "-"))
    coders = [r for r in rods if (r["tested"].get("code") or {}).get("pass")]
    L.append("")
    L.append("%d rods write a function that RUNS and passes every case. Worlds 5 and 6 need these "
             "and this is the first time the lab has known which they are." % len(coders))
    return "\n".join(L)


if __name__ == "__main__":
    if "--classify" in sys.argv:
        doc = fuels.load()
        seen = {}
        for r in doc["rods"].values():
            k = classify(r["model"])
            r["kind"] = k
            seen.setdefault("%s/%s" % (r["plant"], k["class"]), []).append(r["model"])
        fuels.save(doc)
        for k in sorted(seen):
            print("%-26s %3d   %s" % (k, len(seen[k]), ", ".join(x[:26] for x in seen[k][:3])))
    elif "--test" in sys.argv:
        i = sys.argv.index("--test")
        run(sys.argv[i + 1] if len(sys.argv) > i + 1 else "nvidia")
        print("\n" + render())
    else:
        print(render())
