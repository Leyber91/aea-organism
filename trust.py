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

import grid, pulse              # durable persistence + the nervous signal

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "trust_ledger.json")

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
    """May the entity do this right now? Returns {allowed, level, name, why}."""
    state = _load()
    e = _entry(state, cap)
    lvl = e["level"]
    return {
        "allowed": lvl >= 2,                      # autonomous action needs WATCHED or better
        "draft_only": lvl == 1,
        "level": lvl, "name": LEVEL_NAMES[lvl],
        "why": f"{cap}: level {lvl} ({LEVEL_NAMES[lvl]}), streak {e['streak']}, "
               f"{e['runs']} runs / {e['fails']} fails; ceiling {CHARTER[cap]['ceiling']}",
    }


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
            if e["level"] > min(1, c["ceiling"]):     # fast down, but never below DRAFT unless charter says 0
                e["level"] -= 1
            e["history"].append(f"{stamp} FAIL -> {LEVEL_NAMES[e['level']]} {note}".strip())
        e["history"] = e["history"][-20:]
        _save(state)
        pulse.emit("trust", "record", f"{cap} {'ok' if ok else 'FAIL'} -> {LEVEL_NAMES[e['level']]} streak {e['streak']}", ok=ok)
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
