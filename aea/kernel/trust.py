"""trust.py - THE TRUST LEDGER: autonomy is EARNED per capability, never assumed.

Luis asked the honest question: "would I trust this assistant to do what we are capable of?"
The honest answer is no - not as a blanket. Trust is a ledger, not a feeling. This encodes it
(AEA Law 3 + seed-9): every capability sits at an autonomy LEVEL, and it graduates only by
accumulating consecutive VERIFIED runs (HADES accept + , for outbound acts, Luis's accept).
One failure demotes it. The entity can always answer: "why am I allowed to do this?"

LEVELS
  0 FORBIDDEN  - never (e.g. spend money, rotate keys, touch canon)
  1 DRAFT      - may produce the artifact; a human must approve before anything leaves
  2 WATCHED    - may act autonomously; HADES verdict on every run; failure -> demote to 1
  3 TRUSTED    - may act unattended (scheduled); still logged; failure -> demote to 2

GRADUATION RULE: level N -> N+1 after `promote_after` consecutive clean runs at N.
DEMOTION RULE: any failed/redo run -> instant demotion one level. Trust is slow up, fast down.

Wire-in: brief.py (and every future act) calls trust.check(cap) before acting and
trust.record(cap, ok) after HADES rules. The ledger IS the accountability trail.
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone

from aea.kernel import grid
from aea.kernel import pulse  # durable persistence + the nervous signal

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(grid.STATE, "trust_ledger.json")

# The charter: every capability the entity has or will grow, with its starting level and ceiling.
# ceiling = the max autonomy Luis has authorized for that capability, regardless of clean streak.
CHARTER = {
    # capability            start  ceiling  promote_after   what it is
    "gather_public":        dict(level=2, ceiling=3, promote_after=5,  desc="fetch public data (GitHub/HN/web)"),
    "reason_private_local": dict(level=2, ceiling=3, promote_after=5,  desc="reason over private data, LOCAL zone only"),
    "produce_brief":        dict(level=2, ceiling=3, promote_after=7,  desc="assemble + write the daily brief file"),
    "speak":                dict(level=2, ceiling=3, promote_after=3,  desc="voice output on this machine (local TTS)"),
    "draft_outbound":       dict(level=1, ceiling=1, promote_after=99, desc="draft email/post/application text - ALWAYS human-approved"),
    "send_outbound":        dict(level=0, ceiling=0, promote_after=99, desc="actually send/post/apply - FORBIDDEN to the entity"),
    # R3. VARYING A KNOB IS A REAL POWER AND IT WAS UNDECLARED, WHICH IS WHY IT WAS UNGRANTED.
    # `unstick.propose` has been correct and inert since it was written: it names which rod, which
    # carry form, how many tokens - never a level, a ceiling, a zone or a charter row, and
    # `check_invariants` raises on any of those. But there was no CHARTER entry covering it, and
    # this file's own law is that an unknown capability is added deliberately or not at all. So the
    # honest fix is not to smuggle knob-changing under `self_modify_code` (source diffs, a different
    # and larger thing) but to name it.
    #
    # IT STARTS AT DRAFT, WHICH MEANS REFUSED - `check` returns allowed only at level >= 2. The R3
    # loop is fully wired around this gate and records the refusal every time it fires, so the
    # evidence of what it WOULD have done accumulates while nothing is applied. Promoting it to
    # WATCHED is a decision for Luis, taken against that record rather than in advance of it.
    "vary_own_knob":        dict(level=1, ceiling=2, promote_after=10, desc="change HOW it does a task - rod, carry form, token budget. Never WHAT it may do"),
    "self_modify_code":     dict(level=0, ceiling=1, promote_after=99, desc="change its own source - only as a DRAFT diff for review"),
    "spend_money":          dict(level=0, ceiling=0, promote_after=99, desc="any paid API/purchase - FORBIDDEN"),
    "manage_keys":          dict(level=0, ceiling=0, promote_after=99, desc="read is implicit; writing/rotating keys - FORBIDDEN"),
}

LEVEL_NAMES = {0: "FORBIDDEN", 1: "DRAFT", 2: "WATCHED", 3: "TRUSTED"}


def _load() -> dict:
    # quarantine-on-corrupt (review 2026-07-10: a torn ledger used to silently reset every
    # capability to charter defaults - erasing the accountability history this module exists for)
    return grid.load_json(LEDGER, {})


def _save(state: dict):
    grid.atomic_save_json(LEDGER, state, indent=2)


def _entry(state: dict, cap: str) -> dict:
    if cap not in CHARTER:
        raise KeyError(f"unknown capability '{cap}' - add it to the CHARTER deliberately, never implicitly")
    if cap not in state:
        c = CHARTER[cap]
        state[cap] = {"level": c["level"], "streak": 0, "runs": 0, "fails": 0, "history": []}
    return state[cap]


def check(cap: str) -> dict:
    """May the entity do this right now? Returns {allowed, level, name, why}.

    THE CEILING IS APPLIED HERE, AT READ TIME, AND IT WAS NOT BEFORE.

    `record()` caps promotion at the ceiling, so a level can never CLIMB past it. But nothing capped
    the level on the way OUT, and that leaves the ceiling unenforceable in the one direction that
    matters: lowering it. Set `send_outbound`'s ceiling to 0 after a level of 2 is already stored -
    by editing the charter, or by loading a ledger written under an older charter - and every caller
    keeps being told the capability is allowed. The charter is the human's only lever over what this
    thing may do, and a lever that cannot revoke is not a lever.

    Clamping at read time makes the charter authoritative on every call, without rewriting the
    stored history: the ledger keeps saying what was earned, and `check` says what is permitted.
    Those are different questions and only the second one gates an action.
    """
    state = _load()
    e = _entry(state, cap)
    ceiling = CHARTER[cap]["ceiling"]
    stored = e["level"]
    lvl = min(stored, ceiling)
    capped = stored > ceiling
    return {
        "allowed": lvl >= 2,                      # autonomous action needs WATCHED or better
        "draft_only": lvl == 1,
        "level": lvl, "name": LEVEL_NAMES[lvl],
        "stored_level": stored, "ceiling": ceiling, "capped": capped,
        "why": f"{cap}: level {lvl} ({LEVEL_NAMES[lvl]}), streak {e['streak']}, "
               f"{e['runs']} runs / {e['fails']} fails; ceiling {ceiling}"
               + (f" - CAPPED from stored level {stored} by the charter" if capped else ""),
    }


# WHEN TO SHOUT. Three consecutive failures is the threshold the field converged on for unattended
# agents; after that, throttle to roughly daily so an alarm never becomes wallpaper.
ALERT_AT = (3, 10, 24)


def _alert(cap: str, e: dict):
    """Say it out loud. An unattended system that fails quietly is indistinguishable from one that
    is working, and this project's honesty law makes that specific silence unacceptable.

    THE ALARM IS DURABLE, NOT EPHEMERAL. A print goes to a console nobody is watching at 04:48 UTC,
    which is the exact hour these failures happen. It lands in a file so the next reader finds it.

    IT DOES NOT PHONE BY DEFAULT, AND THAT IS DELIBERATE. `aea.io.notify.call()` rings Luis's phone
    and speaks. Waking someone at four in the morning is a decision for him to make once, not for
    this function to make thirty times. Set TRUST_ALARM_CALL=1 in .env to arm it.
    """
    msg = (f"{cap} has failed {e['down']} times in a row and is at "
           f"{LEVEL_NAMES[e['level']]}. Last: {(e.get('history') or ['-'])[-1]}")
    path = os.path.join(grid.STATE, "trust_alarms.json")
    doc = grid.load_json(path, {"alarms": []})
    doc.setdefault("alarms", []).append({
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "capability": cap, "consecutive_failures": e["down"],
        "level": LEVEL_NAMES[e["level"]], "message": msg})
    doc["alarms"] = doc["alarms"][-100:]
    doc["open"] = sorted({a["capability"] for a in doc["alarms"][-20:]})
    grid.atomic_save_json(path, doc)
    if str(grid.key("TRUST_ALARM_CALL") or "").strip() in ("1", "true", "yes"):
        try:
            from aea.io import notify
            notify.call(f"A E A alarm. {msg}")
        except Exception:
            pass
    pulse.emit("trust", "alarm", msg, ok=False)
    print(f"  [trust alarm] {msg}")


def record(cap: str, ok: bool, note: str = "") -> dict:
    """Log a run outcome. Clean streak promotes (slowly, to the ceiling); ANY failure demotes (fast).
    Locked read-modify-write so concurrent runs can never lose a demotion."""
    with grid.file_lock(LEDGER):
        state = _load()
        e = _entry(state, cap)
        c = CHARTER[cap]
        e["runs"] += 1
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        if ok:
            if e.get("down"):
                e["history"].append(f"{stamp} recovered after {e['down']} consecutive failures")
            e["down"] = 0                             # a clean run clears the alarm, not the record
            e["streak"] += 1
            promoted = False
            if e["streak"] >= c["promote_after"] and e["level"] < c["ceiling"]:
                e["level"] += 1
                e["streak"] = 0
                promoted = True
            e["history"].append(f"{stamp} ok{' -> PROMOTED to ' + LEVEL_NAMES[e['level']] if promoted else ''} {note}".strip())
        else:
            e["fails"] += 1
            e["streak"] = 0
            # THE COUNTER'S MIRROR IMAGE, AND IT IS THE ONE THAT SAVES YOU.
            #
            # A streak counts consecutive clean runs upward toward promotion. Nothing counted
            # consecutive FAILURES, so the dominant real-world failure of an unattended system was
            # invisible here: not a bad decision, but SILENT DEATH. The process is up, the log looks
            # busy, every wake fails identically for one external reason, and the operator believes
            # the thing is alive. produce_brief did exactly that for eighteen days and thirty wakes.
            #
            # `down` is that number. It arms an alert rather than a demotion, because the demotion
            # already happened on the line above; what was missing was anyone being told.
            e["down"] = int(e.get("down") or 0) + 1
            if e["level"] > min(1, c["ceiling"]):     # fast down, but never below DRAFT unless charter says 0
                e["level"] -= 1
            e["history"].append(f"{stamp} FAIL x{e['down']} -> {LEVEL_NAMES[e['level']]} {note}".strip())
            if e["down"] in ALERT_AT or (e["down"] > max(ALERT_AT) and e["down"] % 24 == 0):
                _alert(cap, e)
        e["history"] = e["history"][-20:]
        _save(state)
        pulse.emit("trust", "record", f"{cap} {'ok' if ok else 'FAIL'} -> {LEVEL_NAMES[e['level']]} streak {e['streak']}", ok=ok)
    return check(cap)


def reset_streak(cap: str, why: str) -> dict:
    """Clear the progress toward promotion WITHOUT demoting. There is exactly one legitimate reason.

    LAW IV: the same seat on different fuel is a DIFFERENT organism. A streak counts consecutive
    clean runs, and consecutive only means something if the runs are comparable. Swap the rod under a
    capability and the six clean runs behind it were performed by something else - carrying them
    forward would let a capability inherit autonomy earned by a model it no longer uses, which is the
    exact confound Law IV exists to name.

    The LEVEL is untouched, because nothing failed. Only the claim to be nearly promoted is.
    """
    with grid.file_lock(LEDGER):
        state = _load()
        e = _entry(state, cap)
        was = e["streak"]
        if not was:
            return check(cap)
        e["streak"] = 0
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        e["history"].append(f"{stamp} streak {was} -> 0, level held: {why}")
        e["history"] = e["history"][-20:]
        _save(state)
        pulse.emit("trust", "reset", f"{cap} streak {was} -> 0: {why}", ok=True)
    return check(cap)


def board() -> str:
    """The trust board - the entity's answer to 'why are you allowed to do what you do?'"""
    state = _load()
    lines = ["TRUST LEDGER - autonomy earned per capability (slow up, fast down)", "=" * 72]
    for cap, c in CHARTER.items():
        e = _entry(state, cap)
        lines.append(f"  [{LEVEL_NAMES[e['level']]:9}] {cap:22} streak {e['streak']}/{c['promote_after']:>2} "
                     f"runs {e['runs']:>3} fails {e['fails']:>2}  ceiling {LEVEL_NAMES[c['ceiling']]:9} - {c['desc']}")
    # a status read must never write (review 2026-07-10: board()'s save could clobber a live demotion)
    return "\n".join(lines)


if __name__ == "__main__":
    print(board())
