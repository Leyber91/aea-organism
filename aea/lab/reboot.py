"""reboot.py - RE-RUN THE EXPERIMENTS WHOSE EVIDENCE CANNOT BE READ.

THE ORDER MATTERS AND IT IS THE WHOLE POINT: THE STORAGE WAS FIXED FIRST. Re-running an experiment
before fixing what it stores reproduces the problem at full cost. Two changes had to land before a
single call here was worth spending:

  fire.py    `raw` was ctx.text[-320:]. Now the whole reply. That slice is the root of four recorded
             defects and it also collapses every `distinct_replies` count in the lab, because two
             replies differing only in their opening were counted as one.
  chain.py   the trace row stored `chars` and no text at all, so no chain experiment could ever be
             re-read. Now it stores the reply.

WHAT THIS DOES NOT DO. It does not re-derive a published finding and quietly replace it. Each run
lands as a NEW run id beside the old one, with its own design fingerprint. The old run keeps its
rows. If the number moves, that movement is itself the finding and it is visible as a diff rather
than as a silent correction.

THE SITE REBUILDS AFTER EVERY EXPERIMENT, so a section appears the moment its evidence exists rather
than at the end of the batch.

  python -m aea.lab.reboot                 everything that cannot be re-scored, in priority order
  python -m aea.lab.reboot x21 x22         only these
  python -m aea.lab.reboot --list          what would run, and why
"""
from __future__ import annotations

import os
import subprocess
import sys
import time

from aea.kernel import grid
from aea.lab import site

# PRIORITY IS NOT ALPHABETICAL. These three carry World 3's entire bestiary and all three stored
# nothing: `Sistens oneris` came out of x21, the capacity ladder out of x22, inheritance out of x23b.
# A finding with no readable evidence underneath a drawn creature is the exact shape of the failure
# this project keeps catching.
PRIORITY = ["x21_the_carry_battery", "x22_the_capacity_ladder",
            "x23b_inheritance_across_plants", "x23_inheritance"]


def module_exists(experiment):
    return os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "%s.py" % experiment))


def plan(only=None):
    """What needs re-running, in the order it should happen, with the reason attached."""
    ix = site.build()
    todo = []
    for x in ix["experiments"]:
        if x["status"] == "COMPLETE":
            continue
        if only and not any(x["id"].startswith(o) for o in only):
            continue
        if not module_exists(x["id"]):
            todo.append({"id": x["id"], "runnable": False,
                         "why": "no module named %s.py - this run id came from a variant or a "
                                "manual invocation and cannot be rebooted" % x["id"]})
            continue
        todo.append({"id": x["id"], "runnable": True, "regime": x["regime"],
                     "why": ("stored nothing; can never be re-read"
                             if x["regime"] == "NONE" else
                             "stored only the last 320 characters of each reply")})
    rank = {e: i for i, e in enumerate(PRIORITY)}
    todo.sort(key=lambda t: (rank.get(t["id"], 99), t["id"]))
    return todo


def progress_path():
    return os.path.join(grid.STATE, "lab", "reboot.json")


def run(only=None, timeout=5400):
    todo = plan(only)
    runnable = [t for t in todo if t["runnable"]]
    doc = {"started": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
           "planned": todo, "done": []}
    grid.atomic_save_json(progress_path(), doc)

    print("REBOOT - %d experiments, storage fixed first\n" % len(runnable), flush=True)
    for t in todo:
        if not t["runnable"]:
            print("  SKIP %-34s %s" % (t["id"], t["why"]), flush=True)
    print("", flush=True)

    for i, t in enumerate(runnable, 1):
        e = t["id"]
        print("[%d/%d] %s  (%s)" % (i, len(runnable), e, t["why"]), flush=True)
        t0 = time.time()
        try:
            p = subprocess.run([sys.executable, "-u", "-m", "aea.lab.%s" % e],
                               cwd=grid.ROOT, capture_output=True, text=True, timeout=timeout)
            ok, err = p.returncode == 0, (p.stderr or "")[-600:]
            tail = [ln for ln in (p.stdout or "").splitlines() if ln.strip()][-3:]
        except subprocess.TimeoutExpired:
            ok, err, tail = False, "timed out after %ds" % timeout, []
        except Exception as ex:
            ok, err, tail = False, "%s: %s" % (type(ex).__name__, ex), []

        # THE SITE IS REBUILT HERE, not at the end. Its section exists the moment the evidence does.
        ix = site.build()
        after = next((x for x in ix["experiments"] if x["id"] == e), {})
        rec = {"id": e, "ok": ok, "seconds": round(time.time() - t0),
               "regime_before": t.get("regime"), "regime_after": after.get("regime"),
               "replies_after": after.get("replies"), "error": None if ok else err}
        doc["done"].append(rec)
        doc["updated"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
        grid.atomic_save_json(progress_path(), doc)

        print("      %s  %ds  %s -> %s  (%s replies)"
              % ("ok" if ok else "FAILED", rec["seconds"], rec["regime_before"],
                 rec["regime_after"], rec["replies_after"] or 0), flush=True)
        for ln in tail:
            print("      | %s" % ln[:150], flush=True)
        if not ok:
            print("      | %s" % err.replace("\n", " ")[:220], flush=True)

    fixed = [d for d in doc["done"] if d["regime_after"] == "FULL"]
    print("\n%d of %d now store full replies and are re-scorable."
          % (len(fixed), len(runnable)), flush=True)
    still = [d["id"] for d in doc["done"] if d["regime_after"] != "FULL"]
    if still:
        print("STILL NOT RE-SCORABLE: %s" % ", ".join(still), flush=True)
        print("These store no records at all, which is a change to the experiment rather than to "
              "the parts. Named rather than left looking done.", flush=True)
    return doc


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--list" in sys.argv:
        for t in plan(args or None):
            print("%-34s %-9s %s" % (t["id"], "RUN" if t["runnable"] else "SKIP", t["why"]))
    else:
        run(args or None)
