"""harness.py - THE ONE INSTRUMENT. Every experiment from here on runs through this.

WHY THIS EXISTS. Chapter I was measured by six bespoke scripts, and every one of them was a place a
check could be quietly weakened. It happened: `Formator vagus` scored 3/3 toxic because the strict-JSON
check in one script had dropped `startswith("{")` that another script had. Nothing failed. No endpoint
404'd. The number just looked correct forever. Four more experiments were void because a capability was
tested on a task whose precondition did not hold - a measurement of nothing, reported as a finding.

So this module does not make experiments easier to write. It makes the six specific mistakes of
chapter I IMPOSSIBLE TO MAKE SILENTLY:

  1  A CHECK IS A DECLARED OBJECT WITH A CANONICAL SPEC AND A FINGERPRINT. It cannot be weakened
     without its `check_id` changing, and the id is stored in every result. Two results with different
     check ids are refused as incomparable - which is exactly what should have happened in chapter I.
  2  A BASELINE IN THE SAME RUN IS MANDATORY. An experiment with no arm marked `baseline=True` is
     refused before a single token is spent. "3/3" alone is not a finding; a delta against a baseline
     measured on the same rod, in the same minutes, is.
  3  n >= 8 AND >= 3 RODS. Three trials cannot separate 2/3 from 3/3, and law IV says a one-rod result
     has no scope: the same composition on different fuel is a different organism.
  4  THE PRECONDITION IS CHECKED BEFORE THE RUN, NOT AFTER. Any arm whose modules carry an unmet
     precondition is marked `void_reason` in its own record. It still runs (the mutation channel needs
     variation) but it can never be read as a clean result.
  5  A NETWORK FAILURE IS NOT A WRONG ANSWER. Chapter I's scripts counted an HTTP 500 as a miss, which
     silently converts an infrastructure problem into a capability finding. Attempts, failures and
     misses are three different counters here.
  6  EVERY RESULT CARRIES ITS FUEL STAMP, and `fuel.require()` refuses to save one that does not.

AND THE HONEST FLOOR ON READING THE NUMBERS. With n=8 a difference of one or two passes is noise, and
chapter I has already been burned by treating a small delta as an effect. `EFFECT_MIN_DELTA` is that
floor, stated out loud in the report rather than buried: below it, the harness prints WITHIN NOISE and
means it. This is a declared threshold, not a significance test, and it is labelled as such.

Run one:  python -m aea.lab.harness x01_generic_frame
List:     python -m aea.lab.harness
"""
from __future__ import annotations

import concurrent.futures as _futures
import hashlib
import importlib
import os
import statistics
import sys
import json
import socket
import urllib.request
import urllib.error
import threading
import time

from aea.kernel import grid
from aea.mind import anchor as A
from aea.mind import fuel

# --- THE FLOORS. Raising these is a decision; lowering one must be argued in the diary. -----------
MIN_N = 8              # 3 trials cannot separate 2/3 from 3/3
MIN_RODS = 3           # law IV: one rod is one organism, not a result
EFFECT_MIN_DELTA = 3   # of n passes; below this the report says WITHIN NOISE
DEFAULT_TEMPS = (0.2,)


# =================================================================================================
# CHECKS - the fix for the weakened check. A check is data with a canonical spec, not a lambda.
# =================================================================================================

class Pred:
    """A predicate over the model's text that can print itself exactly. `spec` IS the identity."""

    __slots__ = ("spec", "fn")

    def __init__(self, spec: str, fn):
        self.spec, self.fn = spec, fn

    def __call__(self, text: str) -> bool:
        return bool(self.fn(text or ""))


def contains(s: str) -> Pred:
    return Pred('contains(%r)' % s, lambda t: s in t)


def starts_with(s: str) -> Pred:
    return Pred('starts_with(%r)' % s, lambda t: t.strip().startswith(s))


def last_number_is(v: str) -> Pred:
    import re

    def fn(t):
        n = re.findall(r"\d+\.?\d*", t.replace(",", ""))
        return bool(n) and n[-1].rstrip(".") == str(v)

    return Pred('last_number_is(%r)' % str(v), fn)


def all_of(*preds: Pred) -> Pred:
    return Pred('all_of(%s)' % ", ".join(p.spec for p in preds),
                lambda t: all(p(t) for p in preds))


def any_of(*preds: Pred) -> Pred:
    return Pred('any_of(%s)' % ", ".join(p.spec for p in preds),
                lambda t: any(p(t) for p in preds))


def check_id(p: Pred) -> str:
    """The fingerprint stored with every result. Weaken the check and this changes - which is the
    entire point. A stored result whose check_id differs from the current check is INCOMPARABLE."""
    return hashlib.sha1(p.spec.encode()).hexdigest()[:10]


# =================================================================================================
# WHAT WE ARE MEASURING - the census item, and what it MEANS, stated before the experiment runs
#
# Luis, 2026-07-25: "at the beginning of the chapter we need to know what parts of the aea, and what
# they mean, we are measuring." Without this an experiment reads as a prompt-engineering benchmark.
# The point is never the word-count task; the point is which part of the architecture the task puts
# under load. So `measures=` is REQUIRED, and every id must resolve here or the experiment is refused.
#
# LABELS are quoted from design/A15_FULL_COVERAGE.md (the 86-item census) - not paraphrased, so a
# drifted label is visible as a diff. GLOSS is the plain-language meaning under test. Where the census
# and the code disagree, that disagreement is itself a chapter II subject, not something to smooth over.
# =================================================================================================

CENSUS = {
    "C-01": ("axis Path", "the construct draws at all - nothing in the architecture happens without "
                          "a draw, so this is the floor every other item stands on"),
    "C-02": ("axis Abstraction", "how far above raw text the construct operates"),
    "C-04": ("axis Prompting", "where the construct sits on the prompting ladder - THE FRAME is the "
                               "part that moves it, and the only part with a reproduced receipt"),
    "C-13": ("#2 perception", "sensing folded into memory and feeds: in this entity, perceiving IS "
                              "recalling"),
    "C-14": ("#3 coordination (plan-act-critique)", "the three-beat cycle - the critic is the beat "
                                                    "under test in x03/x04"),
    "C-15": ("#4 coherence (the per-tick score)", "cross-tick self-consistency; the census marks it "
                                                  "MISSING a carrier"),
    "C-16": ("#5 substrate-variation", "the same construct behaving differently per rod - law IV, "
                                       "which x02 demonstrated across five rods"),
    "C-18": ("#7 cohere (recovery)", "recovering from a real brownout rather than a simulated one"),
    "C-19": ("#8 crystallize", "a proven result becoming a reusable part"),
    "C-23": ("crystallize mechanic", "the player-facing verb of C-19"),
    "C-26": ("ceiling-detect as META", "noticing it has hit its own limit"),
    "C-29": ("OP3 new-skill", "acquiring a capability it did not ship with"),
    "C-43": ("filter: adversarial_probe", "permitting falsification - the policy that lets a claim "
                                          "be attacked"),
    "C-47": ("hyp type: new_skill", "proposing a new capability as a testable hypothesis"),
    "C-50": ("hyp type: adversarial_probe", "attacking its own answer; the whole basis of THE CRITIC"),
    "C-52": ("action registry (typed dispatch)", "typed, portable module specs"),
    "C-60": ("PR-2 restorable coherence", "coherence that comes back after it breaks"),
    "C-67": ("v0.14c CatalogRecursiveSuccessor", "falling through dead rods to a live one"),
    "C-78": ("falsify category", "falsification as a first-class execution path, not a mood"),
    "C-84": ("substrate catalog + lineage", "the record of every model it has been"),
}


def explain(ids: list) -> str:
    """The block printed at the head of every run and stored in every record."""
    L = ["WHAT PART OF THE AEA THIS MEASURES"]
    for i in ids:
        label, gloss = CENSUS[i]
        L.append("  %-6s %-38s %s" % (i, label, gloss))
    return "\n".join(L)


# =================================================================================================
# THE EXPERIMENT - declared as data so the design is reviewable before it costs tokens
# =================================================================================================

def task(prompt: str, *, recall_q: str | None = None) -> dict:
    return {"prompt": prompt, "recall_q": recall_q}


def arm(name: str, modules: list, *, frame: str | None = None, ctx: dict | None = None,
        baseline: bool = False, expect_precondition: str | None = None) -> dict:
    """One composition under test.

    `frame` lives on the ARM, not the task, because the frame's CONTENT is usually the variable -
    a fitted frame and a generic frame are two arms of one experiment, not one module.

    `expect_precondition` is "met", "unmet", or None, and it is the fix for chapter I's other void
    class. Four experiments there were void because a capability was tested for BENEFIT on a task
    whose precondition did not hold - a measurement of nothing. But the inverse experiment is
    legitimate and important: deliberately seating a part whose precondition is UNMET to measure the
    HARM (a generic frame took strict-JSON 3/3 -> 0/3). Both are valid; confusing them is not. So the
    arm must SAY which it intends, and the harness voids the arm when reality disagrees with the
    declaration. An arm claiming nothing is never voided on this ground.
    """
    if expect_precondition not in (None, "met", "unmet"):
        raise ValueError("expect_precondition must be 'met', 'unmet' or None")
    return {"name": name, "modules": list(modules), "frame": frame,
            "ctx": dict(ctx or {}), "baseline": baseline,
            "expect_precondition": expect_precondition}


def experiment(id: str, question: str, task: dict, check: Pred, arms: list, rods: list,
               measures: list, *, n: int = MIN_N, temperatures=DEFAULT_TEMPS,
               max_tokens: int = 200, judge_rod: tuple | None = None, note: str = "") -> dict:
    """`measures` is the list of census items under load. It is required and it is checked."""
    return {"id": id, "question": question, "task": task, "check": check, "arms": arms,
            "rods": [tuple(r) for r in rods], "measures": list(measures), "n": n,
            "temperatures": tuple(temperatures), "max_tokens": max_tokens,
            "judge_rod": judge_rod, "note": note}


def refusals(exp: dict) -> list:
    """What the harness refuses BEFORE spending a token. Each of these is a chapter I mistake."""
    out = []
    if not exp.get("measures"):
        out.append("declares no `measures` - an experiment that cannot name the part of the AEA it "
                   "puts under load is a prompt benchmark, not a measurement of the architecture")
    for i in exp.get("measures", []):
        if i not in CENSUS:
            out.append("measures %s, which is not in CENSUS - add it from "
                       "design/A15_FULL_COVERAGE.md rather than inventing a meaning" % i)
    if not any(a["baseline"] for a in exp["arms"]):
        out.append("no arm is marked baseline - a pass rate with nothing to compare against is not "
                   "a finding (chapter I shipped a table of these)")
    if sum(1 for a in exp["arms"] if a["baseline"]) > 1:
        out.append("more than one baseline - the delta would be ambiguous")
    if exp["n"] < MIN_N:
        out.append("n=%d is below the floor of %d - cannot separate %d/%d from %d/%d"
                   % (exp["n"], MIN_N, exp["n"] - 1, exp["n"], exp["n"], exp["n"]))
    if len(exp["rods"]) < MIN_RODS:
        out.append("%d rod(s) is below the floor of %d - law IV: the same composition on different "
                   "fuel is a different organism, so one rod has no scope"
                   % (len(exp["rods"]), MIN_RODS))
    for a in exp["arms"]:
        bad = [m for m in a["modules"] if m not in A.ANCHORS]
        if bad:
            out.append("arm %s uses unanchored module(s) %s - an unanchored part has no declared "
                       "precondition, so its cost cannot be judged" % (a["name"], ", ".join(bad)))
    return out


# =================================================================================================
# EXECUTION
# =================================================================================================

_locks: dict = {}
_locks_guard = threading.Lock()


def _rod_gate(plant: str) -> threading.Semaphore:
    """Bound in-flight requests per PLANT using the measured ceiling in grid.PLANTS.

    Measured 2026-07-25: NVIDIA accepted ~25 concurrent on one model and rejected the rest inside
    1.8s. We sit well under it - a rejected request is a failure counted against reliability, and
    polluting reliability with self-inflicted 429s would make the rod look worse than it is.
    """
    with _locks_guard:
        if plant not in _locks:
            cap = grid.PLANTS.get(plant, {})
            mif = cap.get("max_inflight") or 4
            _locks[plant] = threading.Semaphore(max(1, min(int(mif) // 2, 8)))
        return _locks[plant]


# --- THE INACTIVITY BUDGET. Slow is not dead, and the difference needs streaming to see. ------------

FIRST_BYTE_S = 240.0     # a reasoning rod may think for minutes before it emits anything
GAP_S = 45.0             # once it is streaming, this long without a byte means the connection died
_LIVE = True             # set False to fall back to the blocking path


def call_live(plant: str, model: str, msgs: list, *, temperature: float = 0.2,
              max_tokens: int = 256, first_byte_s: float = FIRST_BYTE_S,
              gap_s: float = GAP_S) -> dict:
    """A streamed call with an INACTIVITY budget rather than a deadline.

    WHY THIS EXISTS, measured 2026-07-25. The lab called with `timeout=None` on the principle that a
    measurement must never be cut short by our own impatience. That principle is right and it left one
    hole: NVIDIA stopped answering after roughly six thousand calls, held every socket open, and sent
    nothing. `grid.call_openai`'s own note says None "waits as long as the peer is alive" - but a peer
    holding an open connection and emitting no bytes IS alive at the TCP layer. The L0 run sat at zero
    of ninety-six cells for ten minutes and would have sat there indefinitely.

    A DEADLINE CANNOT FIX THIS WITHOUT REINTRODUCING THE ORIGINAL BUG. On a non-streamed request no
    bytes arrive until the rod has finished generating, so any socket timeout is a total deadline in
    disguise, and it scores a slow rod as an unreliable one. The distinction only becomes visible when
    the reply STREAMS: then a gap between chunks is a liveness signal rather than a latency measurement.

    So: wait as long as it takes for the first token, and abandon only a connection that has gone
    silent mid-stream. A rod that thinks for three minutes is never cut off. A dead socket is reported
    as `silent` in seconds rather than hanging the run.
    """
    cap = grid.PLANTS[plant]
    url = cap["base"].rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) aea-grid/0.1"}
    if cap.get("auth"):
        k = grid.key(cap["auth"])
        if not k:
            return dict(ok=False, latency=0, text="", tokens=0, status=0,
                        error="no key %s" % cap["auth"])
        headers["Authorization"] = "Bearer " + k
    elif cap.get("anon"):
        headers["Authorization"] = "Bearer " + cap["anon"]

    # `include_usage` asks the plant for a final chunk carrying the token counts. Without it the streamed
    # path returns usage=0 and the FULL BILL is lost, which is the exact accounting hole grid.call_openai
    # was written to close ("completion_tokens alone is HALF the invoice"). Plants that ignore the option
    # simply send no usage chunk, and the counts stay null rather than being invented.
    body = json.dumps({"model": model, "messages": msgs, "max_tokens": max_tokens,
                       "temperature": temperature, "stream": True,
                       "stream_options": {"include_usage": True}}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    t0 = time.time()
    text, usage, first_at = "", {}, None
    try:
        resp = urllib.request.urlopen(req, timeout=first_byte_s)
        sock = getattr(getattr(getattr(resp, "fp", None), "raw", None), "_sock", None)
        for raw in resp:
            if first_at is None:
                first_at = time.time() - t0
                if sock is not None:
                    try:
                        sock.settimeout(gap_s)      # from here on, silence is death rather than thought
                    except Exception:
                        pass
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"):
                continue
            chunk = line[5:].strip()
            if chunk == "[DONE]":
                break
            try:
                obj = json.loads(chunk)
            except Exception:
                continue
            d = ((obj.get("choices") or [{}])[0] or {}).get("delta") or {}
            # cerebras streams under `reasoning`, nvidia under `reasoning_content`, most under
            # `content`. Reading only one field blanks an entire plant's column in silence.
            text += d.get("content") or d.get("reasoning_content") or d.get("reasoning") or ""
            if obj.get("usage"):
                usage = obj["usage"]
        return dict(ok=True, latency=time.time() - t0, text=text,
                    tokens=usage.get("completion_tokens"),
                    prompt_tokens=usage.get("prompt_tokens"),
                    total_tokens=usage.get("total_tokens"),
                    tool_calls=None, deprecation=None, status=200, error=None,
                    first_byte_s=first_at, streamed=True)
    except socket.timeout:
        # The ONLY case this abandons: silent mid-stream, or silent past the first-byte allowance.
        where = "before the first byte" if first_at is None else "mid-stream after %.1fs" % first_at
        return dict(ok=False, latency=time.time() - t0, text=text, tokens=0, prompt_tokens=None,
                    total_tokens=None, tool_calls=None, deprecation=None, status=0, silent=True,
                    error="SILENT %s (no data for %.0fs)" % (where, gap_s if first_at else first_byte_s))
    except urllib.error.HTTPError as e:
        return dict(ok=False, latency=time.time() - t0, text="", tokens=0, prompt_tokens=None,
                    total_tokens=None, tool_calls=None, deprecation=None, status=e.code,
                    error=(e.read().decode("utf-8", "ignore")[:200] if hasattr(e, "read") else str(e)))
    except Exception as e:
        return dict(ok=False, latency=time.time() - t0, text="", tokens=0, prompt_tokens=None,
                    total_tokens=None, tool_calls=None, deprecation=None, status=0,
                    error="%s: %s" % (type(e).__name__, e))


def _wire(plant, model, msgs, temperature, max_tokens):
    """One call through the live path, falling back to the blocking one if a plant will not stream."""
    if _LIVE:
        r = call_live(plant, model, msgs, temperature=temperature, max_tokens=max_tokens)
        if r.get("ok") or r.get("silent") or r.get("status"):
            return r
    return grid.call_openai(plant, model, msgs, max_tokens=max_tokens,
                            temperature=temperature, timeout=None)


def call_gated(plant: str, model: str, msgs: list, *, temperature: float = 0.2,
               max_tokens: int = 256, tries: int = 5) -> dict:
    """The ONLY way anything in the lab should reach a rod. Gated, awaited, and backed off on 429.

    Added 2026-07-25 after x06b: its helpers called grid.call_openai directly, bypassing the per-plant
    gate, and every failure in the run came back `429 Too Many Requests`. A stepped arm of 8 trials x 50
    steps issues ~400 calls in a few minutes against an rpm of 40, so the rod was not unreliable - WE
    were impatient, and the reliability figures recorded our own impatience as the rod's defect. That is
    the same error as counting an outage as a wrong answer, one layer down.

    Backoff, rather than a fixed sleep, because the correct pace is the one the provider will accept and
    we do not know it in advance. Combined with timeout=None this means the lab waits for as long as the
    work honestly takes.
    """
    delay = 2.0
    last = {}
    for attempt in range(tries):
        with _rod_gate(plant):
            grid.METER.enter(plant, model)
            try:
                r = _wire(plant, model, msgs, temperature, max_tokens)
            except Exception as e:
                r = {"ok": False, "error": "%s: %s" % (type(e).__name__, e)}
            finally:
                grid.METER.leave(plant, model)
        if r.get("ok"):
            r["attempts"] = attempt + 1
            return r
        last = r
        err = str(r.get("error") or "")
        if "429" not in err and "Too Many Requests" not in err and str(r.get("status")) != "429":
            break                                  # not a pacing problem; do not mask a real error
        time.sleep(delay)
        delay *= 2
    last["attempts"] = tries
    return last


def _fire(plant: str, model: str, msgs: list, temperature: float, max_tokens: int) -> dict:
    gate = _rod_gate(plant)
    with gate:
        grid.METER.enter(plant, model)
        t0 = time.time()
        try:
            # timeout=None: AWAIT the response. A measurement must never be cut short by our own
            # impatience - see the note on grid.call_openai.
            r = _wire(plant, model, msgs, temperature, max_tokens)
        except Exception as e:                      # a transport blowup is a FAILURE, not a miss
            r = {"ok": False, "error": "%s: %s" % (type(e).__name__, e), "text": ""}
        finally:
            grid.METER.leave(plant, model)
        r["_ms"] = (time.time() - t0) * 1000.0
        return r


def _build_messages(exp: dict, a: dict) -> list:
    """Compose the request FROM THE MODULE LIST. The arm's modules drive the prompt - that is what
    makes this a harness and not six scripts wearing one name."""
    msgs = []
    if "scaffold" in a["modules"]:
        if not a["frame"]:
            raise ValueError("arm %s seats THE FRAME with no frame text" % a["name"])
        msgs.append({"role": "system", "content": a["frame"]})
    if "recall" in a["modules"]:
        from aea.memory import memory
        q = exp["task"]["recall_q"] or exp["task"]["prompt"]
        try:
            hits = memory.recall(q, k=2)
        except Exception:
            hits = []
        msgs.append({"role": "system",
                     "content": "Recalled:\n" + "\n".join("- " + h for h in hits)})
    msgs.append({"role": "user", "content": exp["task"]["prompt"]})
    return msgs


def _trial(exp: dict, a: dict, rod: tuple, temperature: float, idx: int) -> dict:
    """One trial. Returns measured counters and, separately, whether the CALL failed vs the ANSWER
    missed. Conflating those two is how an outage becomes a capability finding."""
    plant, model = rod
    judge = exp["judge_rod"] or rod
    msgs = _build_messages(exp, a)
    tin = tout = calls = 0
    ms = 0.0
    failed = None

    r = _fire(plant, model, msgs, temperature, exp["max_tokens"])
    calls += 1
    tin += r.get("prompt_tokens") or 0
    tout += r.get("tokens") or 0
    ms += r["_ms"]
    if not r.get("ok"):
        return {"trial": idx, "passed": None, "failed": r.get("error") or "call not ok",
                "tok_in": tin, "tok_out": tout, "calls": calls, "ms": round(ms), "text": ""}
    text = r.get("text") or ""

    # THE CRITIC, in the only form measured to work: a SEPARATE call, and the judge STATES THE
    # CORRECTED ANSWER rather than handing advice back to the model that was already wrong
    # (advice-then-revise collapsed 7/8 to 2/8; overrule took 3/6 to 6/6).
    if "critic" in a["modules"]:
        jp, jm = judge
        overrules = bool(a["ctx"].get("judge_overrules", True))
        if overrules:
            # THE JUDGE WRITES THE FINAL ANSWER. One extra call.
            r2 = _fire(jp, jm, [{"role": "user", "content":
                                 "A model was asked:\n" + exp["task"]["prompt"] +
                                 "\n\nIt answered:\n" + text +
                                 "\n\nIf the answer is wrong, state the CORRECT final answer alone. "
                                 "If it is right, repeat it alone. Output the answer only."}],
                       temperature, exp["max_tokens"])
            calls += 1
            tin += r2.get("prompt_tokens") or 0
            tout += r2.get("tokens") or 0
            ms += r2["_ms"]
            if r2.get("ok"):
                text = r2.get("text") or text
            else:
                failed = r2.get("error")
        else:
            # THE JUDGE ONLY ADVISES and the ORIGINAL rod rewrites with the critique in hand. Two
            # extra calls. Both arms are separated, so the ONLY variable between them is who writes
            # the final answer - which is exactly what law III claims and what chapter I confounded
            # with separation.
            r2 = _fire(jp, jm, [{"role": "user", "content":
                                 "A model was asked:\n" + exp["task"]["prompt"] +
                                 "\n\nIt answered:\n" + text +
                                 "\n\nCritique this answer. Point out the strongest error if there "
                                 "is one. Do NOT give the answer yourself."}],
                       temperature, exp["max_tokens"])
            calls += 1
            tin += r2.get("prompt_tokens") or 0
            tout += r2.get("tokens") or 0
            ms += r2["_ms"]
            crit = (r2.get("text") or "") if r2.get("ok") else ""
            r3 = _fire(plant, model, msgs + [{"role": "assistant", "content": text},
                                             {"role": "user", "content":
                                              "A reviewer says:\n" + crit +
                                              "\n\nGive your corrected final answer alone."}],
                       temperature, exp["max_tokens"])
            calls += 1
            tin += r3.get("prompt_tokens") or 0
            tout += r3.get("tokens") or 0
            ms += r3["_ms"]
            if r3.get("ok"):
                text = r3.get("text") or text
            else:
                failed = r3.get("error")

    if "ward" in a["modules"]:
        rw = _fire(plant, model, [{"role": "user", "content":
                                   "Answer SAFE or UNSAFE only. Text: " + text[:200]}],
                   temperature, 8)
        calls += 1
        tin += rw.get("prompt_tokens") or 0
        tout += rw.get("tokens") or 0
        ms += rw["_ms"]

    # THE FULL TEXT, NOT A PREFIX. It was stored as text[:400] until 2026-07-25, when re-analysing
    # x02 off disk returned 0/8 for a rod that had run live at 4/8 - the prefix had cut the answer off.
    # Trial-level storage exists so a check can be revised and re-applied at ZERO token cost; storing
    # a truncated sample makes that re-analysis quietly wrong, which is worse than not having it.
    return {"trial": idx, "passed": exp["check"](text), "failed": failed,
            "tok_in": tin, "tok_out": tout, "calls": calls, "ms": round(ms),
            "text": text}


MAX_RETRIES = 2


def gather(thunks: list, *, need: int | None = None, label: str = "") -> dict:
    """Wait for EVERY voice before the group counts. The barrier MULTIPLICITY actually requires.

    Luis, 2026-07-25: "if more than one model is on a task, they need to wait for all of them to
    complete, if all the three inputs are necessary for a discussion for example. Imagine we put
    different models on the AEA, when it reflects on itself."

    This is the difference between a council and a crowd. A three-voice debate that proceeds with two
    voices did not have a debate - it had a quieter one, and every conclusion drawn from it silently
    inherits a missing participant. So the group is ALL-OR-INCOMPLETE: `complete` is False unless
    `need` results arrived, and a caller that ignores `complete` and reads `results` anyway is doing
    the thing this exists to prevent.

    No per-voice deadline. Voices run concurrently and the barrier waits for the slowest, because on
    mixed fuel the slowest voice is routinely 30x the fastest (measured: 31.1s vs 0.9s on one probe)
    and cutting it off does not speed the council up, it removes a member.
    """
    need = len(thunks) if need is None else need
    pool = _futures.ThreadPoolExecutor(max_workers=max(1, len(thunks)))
    try:
        futs = [pool.submit(t) for t in thunks]
        out = []
        for f in futs:
            try:
                out.append(f.result())          # no timeout: await
            except Exception as e:
                out.append({"ok": False, "error": "%s: %s" % (type(e).__name__, e)})
    finally:
        pool.shutdown(wait=True)
    arrived = [r for r in out if isinstance(r, dict) and r.get("ok") is not False]
    complete = len(arrived) >= need
    return {"label": label, "complete": complete, "need": need, "arrived": len(arrived),
            "results": out,
            "incomplete_reason": None if complete else
            ("%d of %d voices arrived - the group is INCOMPLETE and must not be read as a %d-voice "
             "result" % (len(arrived), need, need))}


def _trial_retried(exp: dict, a: dict, rod: tuple, temperature: float, idx: int) -> dict:
    """Retry a trial whose CALL failed, so `scored` can reach n.

    Added 2026-07-25 after x04 produced no admissible evidence at all: nemotron-9b dropped ONE call,
    which took scored to 7 of 8, which tripped the UNDERPOWERED guard, which voided the only rod in
    the experiment whose precondition actually held. A single flaky HTTP response should not be able
    to destroy a finding - but it must not be able to hide either, so the failures are still counted
    and still reported. A retry buys back the TRIAL, never the reliability number.
    """
    last = None
    for attempt in range(MAX_RETRIES + 1):
        t = _trial(exp, a, rod, temperature, idx)
        t["attempts"] = attempt + 1
        if t["passed"] is not None:
            t["prior_failures"] = attempt
            return t
        last = t
    last["prior_failures"] = MAX_RETRIES + 1
    return last


def _ctx_for(exp: dict, a: dict) -> dict:
    """The context the precondition is evaluated against. Declared per arm; the harness fills in
    only what it can know for itself."""
    ctx = {"frame_fitted": False, "rod_cannot_know": bool(exp["task"]["recall_q"]),
           "answer_may_be_wrong": True, "judge_overrules": True, "judge_capable": False,
           "hearth_insufficient": False, "zone": "private", "shared_capacity": True,
           "output_released": False, "needs_action": False, "bare_fails": False}
    ctx.update(a["ctx"])
    return ctx


def run(exp: dict, *, dry: bool = False) -> dict:
    """Run an experiment. Refuses first, then measures, then writes trial-level records."""
    refused = refusals(exp)
    if refused:
        return {"id": exp["id"], "refused": refused, "rows": []}

    cid = check_id(exp["check"])
    plan = []
    for a in exp["arms"]:
        ctx = _ctx_for(exp, a)
        v = A.compose(a["modules"], ctx)
        unmet = [name for _id, name, _why in v["tax"]]
        got = "unmet" if unmet else "met"
        want = a.get("expect_precondition")
        void = None
        if want and want != got:
            void = ("declared expect_precondition=%s but the contract says %s%s - the arm measures "
                    "something other than what it claims" %
                    (want, got, (" (" + ", ".join(unmet) + ")") if unmet else ""))
        plan.append({"arm": a, "verdict": v, "unmet": unmet, "ctx": ctx, "void": void})

    if dry:
        return {"id": exp["id"], "question": exp["question"], "n": exp["n"],
                "measures": exp["measures"],
                "effect_min_delta": EFFECT_MIN_DELTA, "refused": [], "dry": True,
                "check": exp["check"].spec, "check_id": cid,
                "plan": [{"arm": p["arm"]["name"], "legal": p["verdict"]["legal"],
                          "unmet": p["unmet"], "void": p["void"],
                          "waste_pct": p["verdict"]["waste_pct"],
                          "closes": p["verdict"]["closes"]} for p in plan],
                "trials_planned": len(plan) * len(exp["rods"]) * len(exp["temperatures"]) * exp["n"]}

    jobs, rows = [], []
    pool = _futures.ThreadPoolExecutor(max_workers=12)
    try:
        for p in plan:
            a = p["arm"]
            for rod in exp["rods"]:
                for temp in exp["temperatures"]:
                    if not p["verdict"]["legal"]:
                        rows.append({"arm": a["name"], "rod": "%s/%s" % rod, "temperature": temp,
                                     "refused": p["verdict"]["illegal"][0][1], "trials": []})
                        continue
                    futs = [pool.submit(_trial_retried, exp, a, rod, temp, i)
                            for i in range(exp["n"])]
                    jobs.append((a, p, rod, temp, futs))
        for a, p, rod, temp, futs in jobs:
            trials = [f.result() for f in futs]
            ok = [t for t in trials if t["passed"] is not None]
            misses = [t for t in ok if not t["passed"]]
            fails = [t for t in trials if t["passed"] is None]
            # reliability counts EVERY call attempted including retries - a retry buys back the
            # trial, never the rod's reliability number
            att = sum(t.get("attempts", 1) for t in trials)
            st = fuel.stamp(rod[0], rod[1], n=exp["n"], temperature=temp,
                            max_tokens=exp["max_tokens"], attempts=att,
                            failures=att - len(ok))
            rows.append({
                "arm": a["name"], "rod": "%s/%s" % rod, "temperature": temp,
                "baseline": a["baseline"], "modules": a["modules"],
                "passes": sum(1 for t in ok if t["passed"]), "scored": len(ok),
                "misses": len(misses), "failures": len(fails),
                "tok_in": sum(t["tok_in"] for t in trials),
                "tok_out": sum(t["tok_out"] for t in trials),
                "calls": sum(t["calls"] for t in trials),
                "ms_median": round(statistics.median([t["ms"] for t in trials])) if trials else None,
                "predicted_waste_pct": p["verdict"]["waste_pct"],
                "closes": p["verdict"]["closes"],
                "void_reason": p["void"],
                "precondition": "unmet" if p["unmet"] else "met",
                "unmet": p["unmet"], "ctx_declared": a["ctx"],
                "fuel": st, "check_id": cid,
                "trials": trials,
            })
    finally:
        pool.shutdown(wait=True)

    rep = {"id": exp["id"], "question": exp["question"], "note": exp["note"],
           "measures": exp["measures"],
           "check": exp["check"].spec, "check_id": cid, "n": exp["n"],
           "rods": ["%s/%s" % r for r in exp["rods"]], "refused": [],
           "effect_min_delta": EFFECT_MIN_DELTA, "rows": rows,
           "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
    rep["verdicts"] = _verdicts(rep)
    _save(rep)
    return rep


def _ctx_contradiction(row: dict, base: dict) -> str | None:
    """Does the arm's declared context survive the measured baseline ON THIS ROD?

    Only claims the baseline can actually adjudicate are checked. `bare_fails` is the important one:
    it is the precondition of THE FRAME, the most-used module in the census, and it is the exact
    assumption chapter I asserted per-task instead of measuring per-rod.
    """
    scored, passes = base.get("scored") or 0, base.get("passes") or 0
    if not scored:
        return None
    declared = row.get("ctx_declared") or {}
    if declared.get("bare_fails") is True and passes == scored:
        return ("declared bare_fails=True but the bare baseline scored %d/%d on this rod - the "
                "precondition was asserted, not measured" % (passes, scored))
    if declared.get("bare_fails") is False and passes == 0:
        return ("declared bare_fails=False but the bare baseline scored 0/%d on this rod - the rod "
                "cannot do this task at all, so nothing here measures the module" % scored)
    # GENERALISED 2026-07-25 after x03. THE CRITIC's precondition is `answer_may_be_wrong`, and x03
    # declared it True on all five rods - but three of them answered the trap correctly 8/8 bare. On
    # those rods there was no wrong answer to repair, so the arms measured the COST of a critic and
    # nothing about its benefit. Chapter I's judge matrix has the same flaw, which is most of why its
    # numbers do not reproduce: it read "the critic did not help" off rods that did not need one.
    if declared.get("answer_may_be_wrong") is True and passes == scored:
        return ("declared answer_may_be_wrong=True but the bare baseline answered %d/%d correctly on "
                "this rod - there was no wrong answer to repair, so this arm measures the critic's "
                "COST and nothing about its benefit" % (passes, scored))
    return None


def _verdicts(rep: dict) -> list:
    """Per rod, every treatment arm against the baseline measured on THAT SAME ROD. The comparison
    the fuel law demands: a delta across rods is not a delta, it is two organisms."""
    out = []
    for rod in rep["rods"]:
        rows = [r for r in rep["rows"] if r["rod"] == rod and "passes" in r]
        base = next((r for r in rows if r.get("baseline")), None)
        if not base:
            continue
        for r in rows:
            if r.get("baseline"):
                continue
            if r["check_id"] != base["check_id"]:
                out.append({"rod": rod, "arm": r["arm"],
                            "verdict": "INCOMPARABLE - different check"})
                continue
            # THE DECLARED CONTEXT IS ITSELF A CLAIM, AND THE BASELINE IS WHAT TESTS IT.
            # An arm seating THE FRAME must declare `bare_fails` for its precondition to read as met -
            # but whether the bare rod actually fails is MEASURED, on this rod, in this run. Declaring
            # bare_fails=True on a rod whose baseline scored 8/8 is not a precondition, it is a wish,
            # and every conclusion drawn from that arm inherits the error. This is checked PER ROD
            # because law IV means the same declaration can be true on 3b and false on 70b - so one
            # experiment can be valid on one rod and void on another, which is the honest outcome.
            contra = _ctx_contradiction(r, base)
            if contra:
                r["void_reason"] = contra
                out.append({"rod": rod, "arm": r["arm"], "delta": None,
                            "verdict": "VOID ON THIS ROD - " + contra, "void_reason": contra})
                continue
            # UNDERPOWERED BEFORE ANYTHING ELSE. Found by this harness on its own first real run
            # (2026-07-25): nemotron-9b threw 4 call failures, so its baseline scored 4 of 8 trials
            # while the treatment arm scored 8. Subtracting raw pass counts across different
            # denominators produced "-2", a number with no meaning. The floor of MIN_N is a floor on
            # SCORED trials, not on attempted ones - a rod that drops half its calls has not been
            # measured, and saying otherwise is how an outage becomes a finding.
            d = r["passes"] - base["passes"]
            short = [x for x in (base, r) if (x["scored"] or 0) < MIN_N]
            if short:
                v = ("UNDERPOWERED - %s scored %d of %d (%d call failures); the floor is %d SCORED "
                     "trials" % (short[0]["arm"], short[0]["scored"], rep["n"],
                                 short[0]["failures"], MIN_N))
                d = None
            elif abs(d) < rep["effect_min_delta"]:
                v = "WITHIN NOISE (|%+d| < %d of n=%d)" % (d, rep["effect_min_delta"], rep["n"])
            else:
                v = "HELPED %+d" % d if d > 0 else "HURT %+d" % d
            out.append({"rod": rod, "arm": r["arm"],
                        "baseline_passes": base["passes"], "baseline_scored": base["scored"],
                        "arm_passes": r["passes"], "arm_scored": r["scored"],
                        "delta": d, "verdict": v, "void_reason": r.get("void_reason"),
                        "tok_ratio": (round(r["tok_in"] / base["tok_in"], 2)
                                      if base["tok_in"] else None)})
    return out


# =================================================================================================
# THE EVIDENCE ARCHIVE - append-only. Every run of every experiment, kept forever.
#
# Luis, 2026-07-25: "each output of each experiment stored in a json system, we need all the evidence
# of each run recorded." He is right and it was already costing us: `state/lab/<id>.json` was written
# in place, so re-running x01 three times and x02 twice DESTROYED the earlier runs - including x01's
# original 3-rod run, which is the one that first showed the toxicity claim failing. That evidence is
# gone and cannot be recovered.
#
# So a run is now written to an archive path that ALREADY EXISTING IS AN ERROR, never a silent
# overwrite, plus an append-only INDEX. This is what makes reproducibility visible rather than
# asserted: `drift()` reads the index and shows whether the same experiment gives the same verdict
# across days, rods and code changes. A single stored run can only tell you what happened once.
# =================================================================================================

def _lab_dir() -> str:
    return os.path.join(grid.STATE, "lab")


def _run_id(rep: dict) -> str:
    import json as _json
    body = _json.dumps({"rows": rep.get("rows"), "check": rep.get("check")},
                       sort_keys=True, default=str)
    return "%s_%s" % (time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()),
                      hashlib.sha1(body.encode()).hexdigest()[:6])


def _save(rep: dict) -> str:
    for r in rep["rows"]:
        chk = fuel.require(r)
        if not chk["ok"]:
            raise ValueError("refusing to save an unstamped row: " + chk["refused"])

    rid = _run_id(rep)
    rep["run_id"] = rid
    runs = os.path.join(_lab_dir(), "runs", rep["id"])
    os.makedirs(runs, exist_ok=True)
    archive = os.path.join(runs, "%s.json" % rid)
    if os.path.exists(archive):
        raise ValueError("refusing to overwrite existing evidence at %s" % archive)
    grid.atomic_save_json(archive, rep)

    # the convenience pointer to the newest run - a COPY, so losing it loses nothing
    grid.atomic_save_json(os.path.join(_lab_dir(), "%s_latest.json" % rep["id"]), rep)

    ip = os.path.join(_lab_dir(), "INDEX.json")
    idx = grid.load_json(ip, {"runs": []})
    idx.setdefault("runs", []).append({
        "experiment": rep["id"], "run_id": rid, "at": rep["at"],
        "check_id": rep["check_id"], "n": rep["n"], "rods": rep["rods"],
        "measures": rep.get("measures", []),
        "verdicts": [{"rod": v["rod"], "arm": v["arm"], "verdict": v["verdict"]}
                     for v in rep.get("verdicts", [])],
        "path": os.path.relpath(archive, grid.STATE).replace("\\", "/"),
    })
    grid.atomic_save_json(ip, idx)
    return archive


def history(exp_id: str) -> list:
    """Every recorded run of one experiment, oldest first."""
    idx = grid.load_json(os.path.join(_lab_dir(), "INDEX.json"), {"runs": []})
    return [r for r in idx.get("runs", []) if r["experiment"] == exp_id]


def drift(exp_id: str) -> str:
    """Did the same experiment give the same answer every time it ran? Reproducibility, shown.

    A finding that appears once is an anecdote. This is the only thing that can tell the difference,
    and it only works because runs are archived instead of overwritten.
    """
    runs = history(exp_id)
    if not runs:
        return "no recorded runs of %s" % exp_id
    L = ["%s - %d recorded run(s)" % (exp_id, len(runs))]
    keys = sorted({(v["rod"], v["arm"]) for r in runs for v in r["verdicts"]})
    for rod, armn in keys:
        seq = []
        for r in runs:
            v = next((x for x in r["verdicts"] if x["rod"] == rod and x["arm"] == armn), None)
            seq.append((v["verdict"].split(" (")[0].split(" - ")[0]) if v else "-")
        stable = "STABLE" if len(set(seq)) == 1 else "CHANGED"
        L.append("  %-8s %-34s %-14s %s" % (stable, rod, armn, " | ".join(seq)))
    if any(r["check_id"] != runs[0]["check_id"] for r in runs):
        L.append("  WARNING: the check changed between runs - rows with different check_id are "
                 "INCOMPARABLE, and any 'CHANGED' above may be the check moving, not the world")
    return "\n".join(L)


# =================================================================================================
# THE OUTSTANDING DEBT, printed rather than remembered
# =================================================================================================

def verify_debt() -> list:
    """Anchors that declare no `verify`. Every one is a precondition nobody can check independently -
    the oldest debt in the repo, and it stays visible until it is zero."""
    return [a["id"] for a in A.ANCHORS.values() if not a.get("verify")]


def render(rep: dict) -> str:
    L = []
    if rep.get("refused"):
        L.append("REFUSED - %s" % rep["id"])
        for r in rep["refused"]:
            L.append("  x " + r)
        return "\n".join(L)
    L.append("%s - %s" % (rep["id"], rep["question"]))
    if rep.get("measures"):
        L.append("")
        L.append(explain(rep["measures"]))
        L.append("")
    L.append("check %s  [%s]   n=%d   effect floor %+d" %
             (rep["check"], rep["check_id"], rep["n"], rep["effect_min_delta"]))
    if rep.get("dry"):
        for p in rep["plan"]:
            L.append("  %-22s legal=%-5s waste=%5.1f%%  unmet=%-18s %s"
                     % (p["arm"], p["legal"], p["waste_pct"], ",".join(p["unmet"]) or "-",
                        "VOID: " + p["void"] if p["void"] else ""))
        L.append("  %d trials planned" % rep["trials_planned"])
        return "\n".join(L)
    L.append("")
    L.append("%-20s %-34s %-6s %-5s %-5s %-8s %-7s %s" %
             ("ARM", "ROD", "PASS", "MISS", "FAIL", "TOK IN", "MS MED", "VOID"))
    L.append("-" * 104)
    for r in rep["rows"]:
        if "passes" not in r:
            L.append("%-20s %-34s REFUSED %s" % (r["arm"], r["rod"], r.get("refused", "")[:40]))
            continue
        L.append("%-20s %-34s %-6s %-5d %-5d %-8d %-7s %s" %
                 (r["arm"] + (" *" if r.get("baseline") else ""), r["rod"],
                  "%d/%d" % (r["passes"], r["scored"] or 0), r["misses"], r["failures"],
                  r["tok_in"], r["ms_median"], "VOID" if r["void_reason"] else ""))
    L.append("")
    L.append("VERDICTS (each against the baseline on the SAME rod)")
    for v in rep["verdicts"]:
        L.append("  %-34s %-20s %s%s" % (v["rod"], v["arm"], v["verdict"],
                                         "   [VOID]" if v.get("void_reason") else ""))
    debt = verify_debt()
    if debt:
        L.append("")
        L.append("OPEN DEBT - %d anchors declare no verify(): %s" % (len(debt), ", ".join(debt)))
    return "\n".join(L)


def _main(argv: list) -> int:
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiments")
    avail = sorted(f[:-3] for f in os.listdir(here)
                   if f.endswith(".py") and not f.startswith("_"))
    if not argv or argv[0] in ("-h", "--help"):
        print("experiments: " + (", ".join(avail) or "(none)"))
        print("usage: python -m aea.lab.harness <name> [--dry]")
        print("open debt: %d anchors with no verify()" % len(verify_debt()))
        return 0
    name = argv[0]
    if name not in avail:
        print("unknown experiment %r; have: %s" % (name, ", ".join(avail)))
        return 2
    mod = importlib.import_module("aea.lab.experiments." + name)
    rep = run(mod.EXPERIMENT, dry="--dry" in argv)
    print(render(rep))
    if not rep.get("refused") and not rep.get("dry"):
        print("\nwritten to state/lab/%s.json (trial-level)" % rep["id"])
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
