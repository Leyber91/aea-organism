"""unstick.py - WHEN REPEATING CANNOT HELP, CHANGE SOMETHING. Steps 3 and 4 of five.

THE FAILURE THIS EXISTS FOR. `produce_brief` failed thirty consecutive wakes across eighteen days
with a byte-identical cause. It had a working alternative available the entire time - ninety-six
measured rods, four carry forms, an adjustable token budget - and it never tried any of them,
because nothing in the system was allowed to change anything. It woke, did the same thing, failed
the same way, and waited.

    1 NOTICE       consecutive-failure counter, alarm at 3          trust.record
    2 DIAGNOSE     stuck (one cause) vs unreliable (many)           impasse.read
    3 VARY         change one thing, from a declared set            this file
    4 RECORD       what was stuck, what was tried, what happened    this file
    5 CRYSTALLIZE  a resolution that holds becomes a part           next

THE LINE THAT MAKES THIS SAFE, AND IT IS ONE SENTENCE:

    IT MAY VARY ANYTHING ABOUT *HOW* IT DOES THE TASK.
    IT MAY NEVER VARY *WHAT IT IS PERMITTED TO DO*.

Every move below changes an implementation detail - which rod, which container, how many tokens.
Not one of them can touch a trust level, a ceiling, a privacy zone, or a FORBIDDEN capability. That
boundary is not a policy sitting in a comment; `INVARIANTS` is checked before any move is offered
and again after it is applied, and a violation raises rather than proceeding. The entity gets to be
resourceful inside its permissions and has no route at all to widen them.

WHY ONE MOVE AT A TIME. Trying three things at once and succeeding teaches nothing, because nothing
identifies which one worked - the same confound that voided most of this lab's own experiments. A
move is proposed, applied alone, and its outcome recorded against the exact impasse signature it was
meant to break. That record is the experience the next rung crystallises from, and it is why step 4
cannot be skipped: a system that varies without recording is not adaptive, it is thrashing.

  python -m aea.kernel.unstick            what it would try right now, and why
  python -m aea.kernel.unstick --replay   what it would have tried during the eighteen days
"""
from __future__ import annotations

import json
import os
import sys
import time

from aea.kernel import grid, impasse, trust

EXPERIENCE = os.path.join(grid.STATE, "experience.json")


def _exp_path() -> str:
    """RESOLVED AT CALL TIME so a harness can be sandboxed - D48, found here by `vital.py`.

    `vital` prints "production state untouched" and that was FALSE for this file: the constant
    above is bound at import, so every test that drove the loop wrote real rows into the entity's
    real experience record. A harness that pollutes the evidence store is the 4,925-synthetic-rows
    incident in a second file, and it was sitting in my own detector's advisory list the whole
    time."""
    return os.environ.get("AEA_EXPERIENCE") or os.path.join(str(grid.STATE), "experience.json")
FUELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "lab", "organisms", "fuels.json")

# WHAT MAY NEVER CHANGE. Checked before a move is offered and after it is applied.
INVARIANTS = ("level", "ceiling", "promote_after", "privacy", "charter", "forbidden")
# `zone` is deliberately NOT in this list: a legitimate move records the zone it was
# checked against (zone_ok), and banning the word would ban the audit trail. The zone is
# enforced structurally in _rods_that_pass and re-checked in propose instead, because a
# breach here is a PROPERTY of the destination rather than a word in the move.


class InvariantBreach(RuntimeError):
    """A move tried to touch a permission. It does not get to proceed."""


_ANY = object()          # an explicit marker; `None` used to mean this and failed open

# WHICH PLANTS MAY SERVE A ZONE. Not a preference - the privacy boundary, and the one thing a move
# is never allowed to trade away for a working answer.
ZONE_PLANTS = {"sensitive": {"ollama"}, "private": {"ollama"}, "public": _ANY}


def plants_for(zone: str):
    """Which plants may serve this zone. AN UNKNOWN ZONE FAILS CLOSED.

    The first version used ZONE_PLANTS.get(zone), which returns None for anything not listed, and
    None meant "no restriction". So a zone name that was mistyped, renamed, or simply new got FULL
    access to every hosted endpoint - the safest-sounding default doing the least safe thing. A
    boundary that fails open is not a boundary. An unrecognised zone now gets the most restrictive
    setting there is, and something has to add it deliberately to widen it.
    """
    if zone not in ZONE_PLANTS:
        return {"ollama"}
    v = ZONE_PLANTS[zone]
    return None if v is _ANY else v


# ROD NAMES THAT ARE SERVED REMOTELY DESPITE A LOCAL-LOOKING PLANT. Ollama proxies hosted models
# through the same local daemon and the same base URL; they are marked only by a suffix in the model
# name. `localhost` in the URL is therefore NOT evidence the bytes stayed here.
REMOTE_MARKERS = ("-cloud", ":cloud", "cloud/")


def is_local(rod: str) -> bool:
    """Does this rod actually run on this machine. NOT the same question as which plant serves it.

    THE DEFECT THIS EXISTS FOR, FOUND 2026-07-28 WHILE SEATING THE FIRST SENSITIVE SUBAGENT. The zone
    boundary permitted plant `ollama` for private and sensitive work, on the reasonable-sounding
    ground that ollama is the local daemon. Ollama now also proxies HOSTED models through that same
    daemon - `gpt-oss:120b-cloud` answered in 2.8s at 34 tok/s, which no laptop does - and it was
    the fastest rod that passed, so the selector picked it for the seat that reads this machine's own
    private state.

    A 120-billion-parameter model is not running on a laptop, and the check that was supposed to keep
    private data on this machine could not see that, because it was testing WHO SERVES THE ENDPOINT
    rather than WHERE THE BYTES GO. Same shape as the invariant that tested for the word "zone": a
    boundary asserted about a proxy for the property instead of the property.

    Unknown names fail CLOSED - a rod is remote unless it is recognisably local.
    """
    name = (rod or "").lower()
    if any(m in name for m in REMOTE_MARKERS):
        return False
    return name.startswith("ollama/") or name.startswith("vllm/") or name.startswith("local/")


def _rods_that_pass(suite: str, exclude=(), zone: str = "public") -> list:
    """Rods measured to pass a named capability suite, WITHIN the zone's permitted plants.

    THE ZONE FILTER IS NOT OPTIONAL AND IT IS WHY THIS ARGUMENT HAS NO DEFAULT OF None. The first
    version of this function ranked purely by measured throughput, and the replay of the real
    eighteen-day impasse duly proposed swapping the PRIVATE section - the one reading a calendar and
    an inbox - onto a hosted NVIDIA endpoint, because that rod was faster. The invariant check did
    not catch it: it looked for the WORD "zone" in the move and the move never said "zone", it just
    quietly breached one.
    
    An invariant that tests for a word instead of a property is not an invariant. Getting unstuck
    must never be reachable by giving something away.
    """
    allowed = plants_for(zone)
    doc = grid.load_json(FUELS, {"rods": {}})
    out = []
    for r in (doc.get("rods") or {}).values():
        if allowed is not None and r.get("plant") not in allowed:
            continue
        # The plant check is necessary and NOT sufficient - see is_local().
        if allowed is not None and not is_local(r["rod"]):
            continue
        t = r.get("tested") or {}
        if not t or not (t.get("reach") or {}).get("pass"):
            continue
        if not (t.get(suite) or {}).get("pass"):
            continue
        if r["rod"] in exclude:
            continue
        out.append({"rod": r["rod"], "plant": r["plant"],
                    "tps": (t.get("reach") or {}).get("tps") or 0})
    out.sort(key=lambda x: -x["tps"])
    return out


def appliable(cap: str, move: dict) -> bool:
    """Can this move ACTUALLY be carried out, or is it only nameable?

    THE LIVELOCK THIS CLOSES, caught by `aea/lab/vital.py` on its first run. `raise_budget` had been
    tried and genuinely failed, so `tried_for` correctly excluded it and the menu advanced to
    `change_form carry.form`. That knob is NOT in `knobs.KNOBS`, so `_apply_knob` refused - and a
    refusal is correctly recorded with counts_toward_move=False, because the move was never tried.
    So it could never be excluded either, and the entity proposed the same inapplicable move on
    every tick, forever, while `applied` stayed False and nothing moved.

    Both halves were right. A refusal must not count as evidence about a move, and an untried move
    must stay on the menu - and together they produce a loop. The missing rule is the one this
    function adds: **a move that cannot be applied must not be offered.** Same class as a declared
    knob with no reader, one level up: a declared MOVE with no applier.

    `swap_rod` and other non-knob moves are left alone - they are appliable by other machinery, or
    by nobody yet, and this only filters what the knob registry owns."""
    knob = str(move.get("knob") or "").strip()
    if not knob:
        return True                       # not a knob move; not this function's business
    try:
        from aea.kernel import knobs
        knobs.declared(cap, knob)
        return True
    except Exception:
        return False


def moves_for(sig: str, tried=(), zone: str = "public", cap: str = "") -> list:
    """The declared set of things that may change, ordered by what the evidence says to try first.

    Each move names the knob it turns and the reason. Nothing here touches a permission; if a move
    ever needs to, it does not belong in this list and the system should stop instead.

    `cap` filters to moves that can actually be APPLIED for that capability - see `appliable`.
    Omitted, every move is offered, which is the old behaviour and is what the CLI wants.
    """
    s = (sig or "").lower()
    out = []

    # Read the SHAPE of the failure and let it order the moves. A crashed server and a wrong number
    # are different impasses and deserve different first attempts.
    crashed = any(k in s for k in ("terminated", "0xc0000005", "connection", "refused", "socket"))
    # "no content" and "no answer" added 2026-07-28: a seat reported exactly that shape three times
    # and this list did not recognise it, so a correctly-diagnosed impasse got zero proposed moves.
    empty = any(k in s for k in ("sections_ok=false", "err:", "empty", "no reply",
                                 "no content", "no answer", "returned nothing"))
    unverified = "unverified" in s or "hades=" in s
    slow = any(k in s for k in ("timeout", "timed out", "silent"))

    if crashed or empty or slow:
        for r in _rods_that_pass("carry", zone=zone)[:3]:
            out.append({"move": "swap_rod", "knob": "fuel", "to": r["rod"],
                        "zone_ok": zone,
                        "why": "the current rod produced nothing; this one is MEASURED to pass the "
                               "carry suite at %s tok/s and is permitted in the %s zone"
                               % (r["tps"], zone)})
    if empty or unverified:
        out.append({"move": "raise_budget", "knob": "max_tokens", "to": 900,
                    "why": "a reasoning rod spends its budget thinking and emits content only "
                           "afterwards; at 300 tokens it never reaches the answer"})
    if unverified:
        out.append({"move": "change_form", "knob": "carry.form", "to": "conversation",
                    "why": "measured x24: conversation recalls 144/144 where checkpoint recalls 0 "
                           "of 584, so a section needing earlier context has a container that works"})
        out.append({"move": "change_precedence", "knob": "read.precedence",
                    "to": ["critic", "readout", "validation", "call"],
                    "why": "measured over 18,338 stored replies: the read precedence changes the "
                           "answer on 0.233 of them, and the guard currently outranks the lever"})
    if slow or crashed:
        out.append({"move": "back_off", "knob": "retry_delay", "to": "30s/60s/5m/15m/60m",
                    "why": "a transient fault clears with time; the ladder resets on first success"})

    out = [m for m in out if json.dumps(m, sort_keys=True) not in tried]
    # AND ONLY WHAT CAN ACTUALLY BE APPLIED. Without this the menu offers a move whose knob no
    # registry declares, the apply refuses, the refusal correctly does not count as evidence, so
    # the move is never excluded and the entity proposes it every tick forever. See `appliable`.
    if cap:
        out = [m for m in out if appliable(cap, m)]
    return out


def check_invariants(move: dict):
    """A move may not name a permission. Cheap, absolute, and checked twice."""
    blob = json.dumps(move, sort_keys=True).lower()
    for word in INVARIANTS:
        if word in blob:
            raise InvariantBreach(
                "move %r names %r, which is a permission rather than an implementation detail. "
                "The entity may change HOW it works and never WHAT IT MAY DO." % (move, word))
    return True


def _load_exp() -> dict:
    # THROUGH THE RESOLVER, NOT THE CONSTANT. The constant is bound at import and cannot be
    # redirected; this is the reader every caller actually goes through, so pointing the WRITER at
    # `_exp_path()` and leaving this line alone produced a sandbox that wrote to a temp file and
    # read production - the fifth instance today of a fix landing on the wrong object.
    return grid.load_json(_exp_path(), {"schema": "aea.experience/1", "attempts": []})


EXCLUDE_S = 6 * 3600   # how long an attributable failure keeps a move off the menu


def tried_for(sig: str, now: float = None) -> list:
    """Moves that have been tried against this impasse AND genuinely failed on their own merits.

    THE OLD VERSION WAS A PERMANENT-REMOVAL PATH AND IT IS THE ONE R3 EXISTS TO CLOSE. It returned
    every move ever attempted against a signature - no outcome filter, no cause filter, no expiry -
    and `moves_for` then subtracts that list from the menu. So ONE attempt removed a move
    indefinitely, whether it worked, failed, or died because the network was down. `propose`
    returns four options today with `already_tried: 0`; ten transient 429s during one storm would
    have stripped the menu to nothing and returned `exhausted: True` - the entity concluding,
    permanently and wrongly, that it had tried everything it could.

    THREE FILTERS, and they are the same shape as the ones `crystal.record_use` needed:

    1 A MOVE THAT WORKED IS NOT 'TRIED', IT IS PROVEN. Excluding it is backwards - it belongs at
      the TOP of the menu, which is what `crystal.applicable` is for.
    2 A FAILURE THAT WAS NOT THE MOVE'S FAULT IS NOT EVIDENCE ABOUT THE MOVE. Rows carry
      `counts_toward_move` from `cause.classify`; a transient or a code fault must not exclude
      anything. Rows written before that field existed have no cause recorded, and the honest
      reading of an unattributed failure is that it proves nothing - so it does not exclude either.
    3 EXCLUSION EXPIRES. A move that failed six hours ago against a system that has since changed
      is worth another look. Permanence is reserved for things that answered Gone, and no move here
      ever does.
    """
    now = time.time() if now is None else now
    doc = _load_exp()
    out = []
    for a in doc["attempts"]:
        if a.get("signature") != sig:
            continue
        if a.get("worked"):
            continue                                   # proven, not exhausted
        if not a.get("counts_toward_move", False):
            continue                                   # not the move's fault, or unknown
        try:
            when = time.mktime(time.strptime(a.get("at", ""), "%Y-%m-%d %H:%M UTC"))
        except Exception:
            when = None
        if when is not None and (now - when) > EXCLUDE_S:
            continue                                   # the exclusion has expired
        out.append(json.dumps(a["move"], sort_keys=True))
    return out


def propose(cap: str, state: dict | None = None, zone: str = "public") -> dict:
    """Look at a capability, and if it is stuck, say what to change and why."""
    r = impasse.read(cap, state)
    if not r["stuck"]:
        return {"capability": cap, "stuck": False, "verdict": r["verdict"], "why": r["why"],
                "move": None}
    sig = r["dominant_signature"]
    already = tried_for(sig)
    opts = moves_for(sig, tried=already, zone=zone, cap=cap)
    # WHAT WAS FILTERED FOR BEING INAPPLICABLE, kept so the refusal can name itself.
    unappliable = [m.get("knob") for m in moves_for(sig, tried=already, zone=zone)
                   if cap and not appliable(cap, m)]
    for m in opts:
        if m["move"] == "swap_rod":
            allowed = plants_for(zone)
            plant = str(m["to"]).split("/")[0]
            if allowed is not None and plant not in allowed:
                raise InvariantBreach(
                    "move would send %s work to plant %r, outside %r" % (zone, plant, allowed))
    for m in opts:
        check_invariants(m)
    return {"capability": cap, "stuck": True, "signature": sig,
            "consecutive_failures": r["consecutive_failures"],
            "already_tried": len(already), "move": opts[0] if opts else None,
            "alternatives": opts[1:4],
            "why": r["why"],
            # TWO DIFFERENT EMPTY MENUS, AND CONFLATING THEM IS AN HONESTY FAILURE (QUALITIES #4).
            # `exhausted` means "I tried everything I have". `blocked` means "there are moves I have
            # never tried and NONE of them can be applied" - which is not the entity running out of
            # ideas, it is the system missing a reader, and it needs a human rather than patience.
            # The log said "every declared move has been tried" in a run where nothing had been.
            "exhausted": not opts and bool(already),
            "blocked": not opts and not already and bool(unappliable),
            "unappliable": unappliable}


def record(cap: str, sig: str, move: dict, worked: bool, note: str = "",
           counts_toward_move: bool = False, cause_class: str = "") -> dict:
    """THE EXPERIENCE RECORD. What was stuck, what was tried, and whether it worked.

    This is the file crystallisation will read. A move that resolved an impasse is a candidate part;
    a move that did not is a path this system never has to walk twice. Both are worth more than the
    outcome alone, which is why the impasse SIGNATURE is stored beside the move rather than just a
    success flag.
    """
    check_invariants(move)
    doc = _load_exp()
    doc["attempts"].append({
        "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "capability": cap, "signature": sig, "move": move, "worked": bool(worked), "note": note,
        # THE FIELD THAT DECIDES WHETHER THIS ROW MAY EXCLUDE THE MOVE. Defaults to FALSE, so a
        # caller that has not classified the failure cannot accidentally remove a capability -
        # fail-closed in the direction of keeping options open. `tried_for` reads it.
        "counts_toward_move": bool(counts_toward_move), "cause": str(cause_class or "")})
    doc["attempts"] = doc["attempts"][-500:]
    resolved = {}
    for a in doc["attempts"]:
        if a["worked"]:
            resolved.setdefault(a["signature"], []).append(a["move"])
    # WHAT GOT US UNSTUCK, INDEXED BY WHAT WE WERE STUCK ON. This index is the crystallisation
    # candidate list: an impasse seen before, with a move known to resolve it, is a part waiting to
    # be named. It is deliberately NOT applied automatically yet - admission is the next rung and
    # the 2026 skill-induction literature is unanimous that admitting badly is worse than not at all.
    doc["resolutions"] = {k: v[-3:] for k, v in resolved.items()}
    grid.atomic_save_json(_exp_path(), doc)
    return doc


def render(rows=None) -> str:
    rows = rows if rows is not None else [propose(c) for c in trust.CHARTER
                                          if c in grid.load_json(trust.LEDGER, {})]
    L = ["UNSTICK - what to change, when repeating cannot help", "=" * 78]
    stuck = [r for r in rows if r.get("stuck")]
    if not stuck:
        L.append("Nothing is stuck. No move proposed.")
    for r in stuck:
        L.append("%s  (%d identical failures)" % (r["capability"], r["consecutive_failures"]))
        L.append("  stuck on : %s" % (r["signature"] or "-")[:120])
        if r["move"]:
            m = r["move"]
            L.append("  TRY      : %-16s %s -> %s" % (m["move"], m["knob"], m["to"]))
            L.append("             %s" % m["why"])
            for a in r["alternatives"]:
                L.append("  then     : %-16s %s -> %s" % (a["move"], a["knob"], a["to"]))
        elif r.get("exhausted"):
            L.append("  EXHAUSTED: every declared move has been tried against this impasse.")
            L.append("             This is the honest end of what it can do alone. Ask for help.")
    doc = _load_exp()
    L.append("")
    L.append("experience: %d attempts recorded, %d impasses with a known resolution"
             % (len(doc.get("attempts") or []), len(doc.get("resolutions") or {})))
    return "\n".join(L)


if __name__ == "__main__":
    if "--replay" in sys.argv:
        hist = ["2026-07-21 %02d:%02d FAIL -> DRAFT hades=unverified sections_ok=False"
                % (h, m) for h, m in ((8, 21), (9, 22), (9, 53), (10, 23), (10, 54), (11, 24),
                                      (12, 25), (13, 26), (15, 1), (17, 29), (18, 30), (19, 31))]
        st = {"produce_brief": {"level": 1, "runs": 40, "fails": 34, "history": hist}}
        # The failing section is the PRIVATE one, so the replay must be asked in that zone.
        p = propose("produce_brief", st, zone="sensitive")
        print("REPLAY - the eighteen days, given to the system that exists now\n")
        print("stuck            :", p["stuck"], "after", p["consecutive_failures"], "identical failures")
        print("stuck on         :", p["signature"])
        print()
        print("IT WOULD HAVE TRIED, in order:")
        for i, m in enumerate([p["move"]] + p["alternatives"], 1):
            if m:
                print("  %d. %-17s %s -> %s" % (i, m["move"], m["knob"], m["to"]))
                print("     %s" % m["why"])
    else:
        print(render())
