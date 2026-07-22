"""live.py - THE CONTINUOUS LIFE. The entity that is always alive, even when it sleeps.

Luis's model: the computer is not always on - that is fine. When it runs, the entity is AWAKE and
serves; when the machine is off, the process dies but its state is on disk - ASLEEP, still alive -
and it resumes on the next wake. Continuity lives in the files, not in the process.

TWO MODES, like a real nervous system:
  AWAKE  - if today's brief isn't done, produce it (serve Luis).
  ASLEEP - otherwise consolidate the transcript backlog (episodic -> semantic memory), a slice per
           tick, until the whole corpus is learned. Idle time becomes memory. Runs on LOCAL power.

It NEVER dies on an error (a bad tick is logged and the loop continues), writes a HEARTBEAT every
tick so its aliveness is visible, and RESUMES from heartbeat.json across restarts (proves it
survived sleep). Heavy work is delegated to the proven scripts as subprocesses, so a crash in one
can never take down the life.

  python live.py                          # run forever, 30-min ticks (production)
  python live.py --interval 1 --ticks 2   # bounded demo (prove heartbeat + restart-resume)
  python live.py --status                 # print the heartbeat and exit
"""
from __future__ import annotations
import json, os, sys, time, subprocess, signal
from datetime import datetime, timezone

import grid, pulse             # durable persistence + the nervous signal (the brain view watches)

HERE = os.path.dirname(os.path.abspath(__file__))
HEARTBEAT = os.path.join(grid.STATE, "heartbeat.json")
LOG = os.path.join(HERE, "live.log")
PIDLOCK = os.path.join(HERE, "live.instance")
PY = sys.executable
CONSOLIDATE_SLICE = 3          # sessions learned per idle (sleep) tick

_stop = {"now": False}
def _on_signal(*_):            # a clean sleep, not a crash: mark asleep and exit
    _stop["now"] = True


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def load_hb() -> dict:
    return grid.load_json(HEARTBEAT, {"alive_since": now_iso(), "boot_count": 0, "total_ticks": 0,
                                      "last_brief_date": None, "consolidated_sessions": 0, "history": []})

def save_hb(hb: dict):
    grid.atomic_save_json(HEARTBEAT, hb, indent=2)     # kill-safe (review 2026-07-10)

def log(msg: str):
    line = f"{now_iso()}  {msg}"
    try:
        open(LOG, "a", encoding="utf-8").write(line + "\n")
    except Exception:
        pass
    print(line)


def run_script(args: list[str], timeout: int) -> tuple[bool, str]:
    """Delegate heavy work to a proven script; isolate its failure from the life."""
    try:
        r = subprocess.run([PY] + args, cwd=HERE, capture_output=True, text=True, timeout=timeout)
        tail = (r.stdout or r.stderr or "").strip().splitlines()
        return r.returncode == 0, (tail[-1] if tail else "")
    except subprocess.TimeoutExpired:
        return False, f"timeout>{timeout}s"
    except Exception as e:
        return False, str(e)[:80]


def corpus_state() -> tuple[int, int]:
    """(consolidated-AND-existing, total) across ALL projects (2026-07-19: the old single-project
    count + ghost-processed ids made the loop believe 'nothing owed' while today's sessions sat
    unmined). Counts only the intersection of processed ids with files that still exist."""
    try:
        import consolidate, glob
        total = len(glob.glob(os.path.join(consolidate.PROJECTS_ROOT, "*", "*.jsonl")))
        meta = grid.load_json(consolidate.META, None)
        if meta is not None:
            return meta.get("processed", 0), total
        return len(consolidate.load_store().get("processed", [])), total
    except Exception:
        return 0, 0


def choose_action(hb: dict) -> tuple[str, list[str], int]:
    """AWAKE if today's brief is undone, else ASLEEP (consolidate) if backlog remains, else IDLE."""
    if hb.get("last_brief_date") != today():
        return "AWAKE:brief", ["brief.py"], 240
    done, total = corpus_state()
    if total and done < total:
        return "ASLEEP:consolidate", ["consolidate.py", "--limit", str(CONSOLIDATE_SLICE)], 600
    # NOT resting: t6 the reflection tick - self-originate ONE task (the autonomy organ, gated by HADES).
    # This is the wire from an internal goal to an action - what makes the self a loop, not a document.
    if os.path.exists(os.path.join(HERE, "reflect.py")):
        return "REFLECT:self", ["reflect.py", "--once"], 240
    return "IDLE", [], 0


def tick(hb: dict, demo: bool):
    hb["total_ticks"] += 1
    action, args, tmo = choose_action(hb)
    if demo and action.startswith("AWAKE"):        # keep the demo cheap: skip the 60s brief, do a memory slice
        action, args, tmo = "ASLEEP:consolidate(demo)", ["consolidate.py", "--limit", "1"], 300
    if not args:
        log(f"tick {hb['total_ticks']}  IDLE (corpus fully consolidated; nothing owed) - resting")
        return
    log(f"tick {hb['total_ticks']}  {action}  -> running {' '.join(args)}")
    pulse.emit("life", "tick", f"#{hb['total_ticks']} {action}")
    ok, tail = run_script(args, tmo)
    pulse.emit("life", "tick-done", f"#{hb['total_ticks']} {action} {'ok' if ok else 'FAIL'}", ok=ok)
    if action.startswith("AWAKE"):
        if ok:
            hb["last_brief_date"] = today()
    done, total = corpus_state()
    hb["consolidated_sessions"] = done
    hb["history"] = (hb.get("history", []) + [f"{now_iso()} {action} {'ok' if ok else 'FAIL'} :: {tail[:80]}"])[-30:]
    log(f"tick {hb['total_ticks']}  {action}  {'ok' if ok else 'FAIL'}  ({tail[:70]})  | corpus {done}/{total}")


def main():
    a = sys.argv
    if "--status" in a:
        hb = load_hb()
        done, total = corpus_state()
        print(json.dumps({k: hb.get(k) for k in
              ("alive_since", "boot_count", "total_ticks", "last_brief_date", "consolidated_sessions")}, indent=2))
        print(f"corpus consolidated: {done}/{total}")
        print("recent:"); [print("  " + h) for h in hb.get("history", [])[-6:]]
        return

    interval = int(a[a.index("--interval") + 1]) if "--interval" in a else 1800
    max_ticks = int(a[a.index("--ticks") + 1]) if "--ticks" in a else None
    demo = "--demo" in a or max_ticks is not None
    signal.signal(signal.SIGINT, _on_signal)
    try:
        signal.signal(signal.SIGTERM, _on_signal)
    except Exception:
        pass

    # SINGLE-INSTANCE guard (review 2026-07-10): two lives racing the same heartbeat/brief was
    # silent double-work. The lock handle is held for the process lifetime; the OS releases it
    # on any death, so there is no stale-lock problem.
    _instance = open(PIDLOCK, "a+b")
    try:
        import msvcrt
        _instance.seek(0); msvcrt.locking(_instance.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        print("another live.py is already running - this one yields."); return
    except ImportError:
        pass

    hb = load_hb()
    hb["boot_count"] += 1                            # every start = a WAKE; proves survival across sleep
    save_hb(hb)
    log(f"=== WAKE #{hb['boot_count']} ===  alive since {hb['alive_since']} | "
        f"resuming at tick {hb['total_ticks']} | interval {interval}s"
        + (f" | {max_ticks} ticks then sleep" if max_ticks else " | forever"))

    n = 0
    while not _stop["now"]:
        try:
            tick(hb, demo)
        except Exception as e:
            log(f"tick error (survived): {e}")       # the life never dies on a bad tick
        save_hb(hb)                                   # persist EVERY tick -> asleep-still-alive
        n += 1
        if max_ticks and n >= max_ticks:
            break
        for _ in range(interval):                     # responsive sleep so a stop is a clean sleep
            if _stop["now"]:
                break
            time.sleep(1)

    log(f"=== SLEEP ===  ran {n} ticks this wake; total {hb['total_ticks']}; state persisted. Still alive on disk.")


if __name__ == "__main__":
    main()
