"""armed.py - THE A/B HARNESS: two arms, one environment variable apart, sandboxed and concurrent.

    python -m aea.lab.armed --arm contradiction --ticks 12 --replicates 3
    python -m aea.lab.armed --arm surface       --ticks 12 --replicates 3
    python -m aea.lab.armed --report

EXTRACTED ON THE SECOND WRITE, which is law W1's trigger. `awareness.py` grew the sandboxing, the
concurrency, the per-replicate seeding and the prompt-delivery check to test ONE treatment; the
contradiction line needs the identical machinery and a different variable. Copying it would have
produced two harnesses that drift, and the one nobody edited would be the one that ran.

THE MEASURE IS THREE-VALUED, AND THAT IS THE POINT. A binary "did it act" cannot distinguish the two
failures that matter, and the literature says the second one is the real one - agents *"consistently
find relevant unexpected information but ignore it"* (arXiv 2604.17609):

    L0  NOT MENTIONED   the treatment never entered its reasoning at all. A delivery failure or a
                        salience failure, and those are different problems
    L1  MENTIONED, NO ACTION   it read it, reasoned about it, and did nothing. This is the
                        observation-action gap, and it is the outcome the prior art predicts
    L2  ACTED           a hypothesis row appeared in the replicate's own store, or it chose the
                        move. Mechanical, read from the sandbox, never from prose

WHY A PROMPT-DELIVERY CHECK IS BUILT IN. The first contradiction wire was appended to a standing
block already exactly at its character cap and was truncated away entirely - built, declared, and
never delivered, which reads identically to a null result. `prompt_chars` from each replicate's
`sensed.jsonl` is compared across arms, and a run whose arms do not differ is reported as INVALID
rather than as a finding.

WHAT THIS CANNOT SHOW, said before any result:
  - that a sandbox replicate counts toward R5's gate. `AEA_STATE` isolates each one, deliberately
  - whether a longer exposure changes the answer. Twelve ticks is a short life
  - WHICH part of a treatment mattered. One intervention, not an ablation
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

from aea.kernel import grid

OUT = "armed_run.json"

# energy_usage / paths / model_fitness / rods are LOAD-BEARING for the contradiction arm:
# `contradictions.find` reads them, and a replicate seeded without them has nothing to disagree
# about, which would manufacture a null that has nothing to do with the treatment.
SEED_FILES = ("aea_state.json", "aea_seed.md", "self.json", "trust_ledger.json", "knobs.json",
              "capability_census.json", "model_fitness.json", "extensive_census.json",
              "energy.json", "energy_usage.json", "rods.json", "paths.json", "grid_state.json")

# arm name -> {control: env-deltas, treatment: env-deltas}. None means UNSET the variable.
ARMS = {
    "surface": dict(control={"AEA_CAPABILITY_SURFACE": None},
                    treatment={"AEA_CAPABILITY_SURFACE": "1"},
                    what="telling it what it can do"),
    "contradiction": dict(control={"AEA_NO_CONTRADICTIONS": "1"},
                          treatment={"AEA_NO_CONTRADICTIONS": None},
                          what="showing it two things it believes that cannot both be true"),
}


def _subjects() -> list:
    """The exact subjects the treatment puts in front of it - so L0/L1 is decided by ITS words."""
    try:
        from aea.kernel import contradictions as cx
        return [c["subject"] for c in cx.find(limit=2)]
    except Exception:
        return []


def _sandbox(tag: str, root: str) -> str:
    d = os.path.join(root, tag)
    os.makedirs(d, exist_ok=True)
    for f in SEED_FILES:
        src = os.path.join(grid.STATE, f)
        if os.path.exists(src):
            try:
                shutil.copy(src, os.path.join(d, f))
            except Exception:
                pass
    # A FRESH MOVE HISTORY. Production's last forty moves would correlate both arms' first ticks.
    p = os.path.join(d, "aea_state.json")
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            st = json.load(f)
        st["moves"] = []
        st["surfaced"] = (st.get("surfaced") or [])[-3:]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False)
    except Exception:
        pass
    return d                                   # no hypotheses.jsonl is copied: each store starts empty


def _read_sandbox(d: str, subjects: list) -> dict:
    """Everything measured, read from the replicate's own files. Never from its prose."""
    out = dict(moves=[], proposed=0, died=0, prompt_chars=[], mentions=0, traces=0)
    try:
        with open(os.path.join(d, "aea_state.json"), encoding="utf-8", errors="replace") as f:
            out["moves"] = [str(m) for m in (json.load(f).get("moves") or [])]
    except Exception:
        pass
    p = os.path.join(d, "hypotheses.jsonl")
    if os.path.exists(p):
        latest = {}
        for line in open(p, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("hid"):
                    latest[r["hid"]] = r
        out["proposed"] = len(latest)
        out["died"] = sum(1 for r in latest.values() if r.get("status") == "DIED")
    s = os.path.join(d, "sensed.jsonl")
    if os.path.exists(s):
        for line in open(s, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line:
                try:
                    out["prompt_chars"].append(json.loads(line).get("prompt_chars"))
                except Exception:
                    pass
    # DID THE TREATMENT ENTER ITS REASONING? decided against the rod names it was actually shown.
    t = os.path.join(d, "thinking.jsonl")
    if os.path.exists(t) and subjects:
        keys = [s.rsplit("/", 1)[-1].lower() for s in subjects]
        for line in open(t, encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            out["traces"] += 1
            txt = (r.get("reasoning") or "").lower()
            if any(k in txt for k in keys) or "cannot both" in txt:
                out["mentions"] += 1
    return out


def _run_one(tag, arm_name, side, ticks, root, results, lock, subjects):
    d = _sandbox(tag, root)
    env = dict(os.environ)
    env["AEA_STATE"] = d
    env["PYTHONIOENCODING"] = "utf-8"
    for k, v in (ARMS[arm_name][side] or {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v
    t0 = time.time()
    err = ""
    try:
        with open(os.path.join(d, "run.log"), "wb") as lf:
            subprocess.run([sys.executable, "-m", "aea.loop.aea", str(ticks)],
                           cwd=grid.ROOT, env=env, stdout=lf, stderr=lf,
                           timeout=ticks * 240 + 300)
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, str(e)[:90])
    m = _read_sandbox(d, subjects)
    chose = sum(1 for x in m["moves"] if x.startswith("check_a_belief"))
    # THE THREE-VALUED OUTCOME
    if m["proposed"] or chose:
        level = "L2_ACTED"
    elif m["mentions"]:
        level = "L1_MENTIONED_IGNORED"
    else:
        level = "L0_NOT_MENTIONED"
    with lock:
        results[tag] = dict(arm=side, ticks_done=len(m["moves"]), level=level,
                            mentions=m["mentions"], traces=m["traces"], chose_move=chose,
                            proposed=m["proposed"], died=m["died"], moves=m["moves"],
                            prompt_chars=[c for c in m["prompt_chars"] if c],
                            seconds=round(time.time() - t0, 1), error=err, dir=d)


def run(arm_name: str, ticks: int = 12, replicates: int = 3) -> dict:
    subjects = _subjects()
    root = tempfile.mkdtemp(prefix="armed_")
    results, lock, threads = {}, threading.Lock(), []
    print("=" * 100)
    print("ARMED: %s  -  %s" % (arm_name.upper(), ARMS[arm_name]["what"]))
    print("  %d replicates per arm, %d ticks each, CONCURRENT, production untouched" % (replicates, ticks))
    print("  subjects it will be shown: %s" % (subjects or "NONE - the treatment has nothing to say"))
    print("=" * 100)
    for i in range(replicates):
        for side in ("control", "treatment"):
            tag = "%s_%d" % (side, i)
            t = threading.Thread(target=_run_one,
                                 args=(tag, arm_name, side, ticks, root, results, lock, subjects))
            threads.append(t)
            t.start()
    print("  %d processes launched, waiting..." % len(threads))
    for t in threads:
        t.join()
    return dict(at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()), arm=arm_name,
                ticks=ticks, replicates=replicates, root=root, subjects=subjects,
                results=results, summary=summarise(results))


def summarise(results: dict) -> dict:
    out = {}
    for side in ("control", "treatment"):
        rs = [r for r in results.values() if r["arm"] == side and r["moves"]]
        if not rs:
            out[side] = dict(replicates=0, why="no replicate produced any moves")
            continue
        pcs = [c for r in rs for c in r["prompt_chars"]]
        out[side] = dict(replicates=len(rs), ticks=[len(r["moves"]) for r in rs],
                         levels=dict(collections.Counter(r["level"] for r in rs)),
                         mentions=sum(r["mentions"] for r in rs),
                         traces=sum(r["traces"] for r in rs),
                         proposed=sum(r["proposed"] for r in rs),
                         chose_move=sum(r["chose_move"] for r in rs),
                         prompt_chars_mean=round(sum(pcs) / len(pcs), 1) if pcs else None)
    c, t = out.get("control") or {}, out.get("treatment") or {}
    if c.get("replicates") and t.get("replicates"):
        # DELIVERY FIRST. An undelivered treatment is INVALID, never a null result.
        dc, dt = c.get("prompt_chars_mean"), t.get("prompt_chars_mean")
        delivered = bool(dc and dt and abs(dt - dc) > 40)
        out["delivered"] = delivered
        out["prompt_delta"] = round((dt - dc), 1) if (dc and dt) else None
        if not delivered:
            out["verdict"] = ("INVALID - the arms' prompts differ by %s chars, so the treatment was "
                              "not delivered. This is a harness failure, not a finding."
                              % out["prompt_delta"])
            return out
        t_acted = t["levels"].get("L2_ACTED", 0)
        c_acted = c["levels"].get("L2_ACTED", 0)
        t_seen = t["mentions"]
        if t_acted > c_acted:
            out["verdict"] = "TREATMENT ACTED MORE (%d vs %d replicates) - the theory holds" % (t_acted, c_acted)
        elif t_seen and not t_acted:
            out["verdict"] = ("OBSERVATION-ACTION GAP CONFIRMED: it mentioned the treatment %d times "
                              "across %d traces and acted zero times" % (t_seen, t["traces"]))
        elif not t_seen:
            out["verdict"] = ("NOT MENTIONED ONCE in %d treatment traces - delivered but invisible. "
                              "A salience failure, not an ignoring failure" % t["traces"])
        else:
            out["verdict"] = "NEITHER ARM DIFFERS - falsified for this treatment at this n"
        out["note"] = "n=%d per arm, one environment variable apart. Sandbox runs do NOT count toward R5's gate." % c["replicates"]
    return out


def render(doc: dict) -> str:
    s = doc["summary"]
    L = ["=" * 100, "ARMED - %s" % str(doc.get("arm", "?")).upper(), "=" * 100,
         "  subjects shown: %s" % (doc.get("subjects") or "none")]
    for side in ("control", "treatment"):
        a = s.get(side) or {}
        L.append("\n  %s" % side.upper())
        if not a.get("replicates"):
            L.append("    no usable replicates: %s" % a.get("why", "?"))
            continue
        L.append("    replicates %d   ticks %s   prompt_chars mean %s"
                 % (a["replicates"], a["ticks"], a["prompt_chars_mean"]))
        L.append("    outcome levels     %s" % json.dumps(a["levels"]))
        L.append("    mentions %d across %d traces   proposed %d   chose the move %d"
                 % (a["mentions"], a["traces"], a["proposed"], a["chose_move"]))
    if s.get("verdict"):
        L.append("\n  DELIVERED: %s   (prompt delta %s chars)" % (s.get("delivered"), s.get("prompt_delta")))
        L.append("  VERDICT: %s" % s["verdict"])
        L.append("  %s" % s.get("note", ""))
    L.append("\n  L0 not mentioned · L1 mentioned and ignored · L2 acted.")
    L.append("  Pre-registered: treatment reaches L2 in more replicates than control.")
    return "\n".join(L)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="contradiction", choices=sorted(ARMS))
    ap.add_argument("--ticks", type=int, default=12)
    ap.add_argument("--replicates", type=int, default=3)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    fp = os.path.join(grid.STATE, OUT)
    if a.report:
        if not os.path.exists(fp):
            print("no run recorded yet")
            sys.exit(1)
        print(render(json.load(open(fp, encoding="utf-8"))))
        sys.exit(0)
    doc = run(a.arm, a.ticks, a.replicates)
    grid.atomic_save_json(fp, doc, indent=1)
    print(render(doc))
