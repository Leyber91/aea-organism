"""seats.py - CUSTOM SUBAGENTS, BUT A SUBAGENT IS NOT A PROMPT.

The pattern going around is a named role with a system prompt, a tool list, and a model - a
specialist you can address by name. It is a good pattern and this file is that pattern. What it adds
is the three fields those definitions have no slot for, each of which already exists in this repo and
was simply never connected to the idea of a role:

    capability   which charter capability it runs as, so THE LEDGER GRADES IT
    zone         where it may run, so THE PRIVACY BOUNDARY BINDS ITS TOOLS AND ITS FUEL
    rod          which measured model-on-plant, because LAW IV says the seat IS the pairing

Drop any of the three and you have a persona. A persona cannot earn autonomy, cannot be bounded, and
cannot be compared to itself across a model swap.

WHY A SEAT REFUSES TO EXIST RATHER THAN DEGRADE. `seat()` raises if the rod is not MEASURED to emit a
tool call, if the plant is not permitted in the zone, or if a tool in the allowlist is not permitted
there. The alternative - construct it anyway and fail at dispatch - moves the error from the place
that can explain it to the place that cannot. This project has already paid for that once: rods were
chosen by name recognition until they were measured, and the one seated ran at 0.9 tok/s against one
available at 45.8.

THE PROBE PAID FOR ITSELF IMMEDIATELY. The fastest rod in the fuel table cannot call a tool at all -
it emits a JSON blob that LOOKS like a call, as prose, in the content field. Anything selecting on
throughput would have seated it, and the failure would have looked like the model being stupid rather
than the harness being wrong.

LAW IV IS ENFORCED, NOT QUOTED. When a capability's rod changes, `dispatch` resets the promotion
streak and holds the level. Six clean runs behind a capability were performed by whatever was seated
at the time; carrying them across a swap would let a capability inherit autonomy earned by a model it
no longer uses.

  python -m aea.kernel.seats             the roster: who exists, on what, permitted to do what
  python -m aea.kernel.seats --run ID    dispatch one seat against its goal, for real
"""
from __future__ import annotations

import json
import os
import sys
import time

from aea.kernel import fit, goals, grid, hands, trust, unstick

ROSTER = os.path.join(grid.STATE, "seats.json")


class Unseatable(ValueError):
    """A seat that cannot be graded, bounded, or fuelled is not built. See the module docstring."""


def _load() -> dict:
    return grid.load_json(ROSTER, {"schema": "aea.seats/1", "seats": {}, "rods": {}})


def _save(doc: dict):
    grid.atomic_save_json(ROSTER, doc)


def pick_rod(zone: str, tools: bool = True) -> str | None:
    """Delegates to the discriminator. THIS FUNCTION DELIBERATELY HOLDS NO SELECTION LOGIC.

    It used to. It ranked on measured latency and stopped, which made it the SIXTH independent model
    selector in this repo - and the audit that counted them is the reason it no longer is. Six
    selectors ranking on four different keys, none calling another, is not redundancy; it is four
    different answers to one question, and the one that answers is whichever file you happened to
    call.

    `fit.choose` states the requirement, applies every gate, and refuses when nothing satisfies it.
    Returning None here means the discriminator refused, which is information, not an outage.
    """
    try:
        return fit.choose(fit.Need("a seat's work", zone=zone, tools=tools))
    except fit.NoFit:
        return None


def seat(sid: str, role: str, capability: str, zone: str, tools=(), rod: str | None = None,
         goal: str | None = None, brief: str = "") -> dict:
    """Define a subagent. REFUSES rather than degrades - every check below has a measured basis.

    `rod=None` means "choose the fastest measured rod this zone permits", which is the right default
    because it is the one that cannot be stale.
    """
    if capability not in trust.CHARTER:
        raise Unseatable(
            "capability %r is not in the charter, so this seat could never be graded: it could not "
            "earn autonomy and could not demote when it failed. Charter has: %s"
            % (capability, ", ".join(trust.CHARTER)))
    if zone not in goals.ZONES:
        raise Unseatable("zone %r is not one of %s, so nothing would bound this seat's tools or its "
                         "fuel" % (zone, goals.ZONES))

    for t in tools:
        if t not in hands.TOOLS:
            raise Unseatable("no such tool %r" % t)
        v = hands.allowed(t, zone)
        if not v["ok"]:
            raise Unseatable("this seat cannot hold %s in the %s zone: %s" % (t, zone, v["why"]))

    rod = rod or pick_rod(zone)
    if rod is None:
        raise Unseatable(
            "no rod is MEASURED to call a tool among the plants the %s zone permits (%s). Run "
            "python -m aea.kernel.hands --probe. A seat on an unmeasured rod is a guess wearing a "
            "job title." % (zone, ", ".join(sorted(unstick.plants_for(zone) or ["any"]))))
    if tools:
        m = {r["rod"]: r for r in hands.rods_that_call()}
        if rod not in m:
            raise Unseatable("%s is not MEASURED to emit a valid tool call, and this seat holds "
                             "tools. The fastest rod in the fuel table fails this test." % rod)
    plant = rod.split("/", 1)[0]
    permitted = unstick.plants_for(zone)
    if permitted is not None:
        if plant not in permitted:
            raise Unseatable("%s is served by %s, which may not serve the %s zone"
                             % (rod, plant, zone))
        if not unstick.is_local(rod):
            raise Unseatable(
                "%s is served by the local daemon but the model itself is HOSTED, so seating it in "
                "the %s zone would send private data off this machine. The plant name is not "
                "evidence of locality." % (rod, zone))

    doc = _load()
    doc["seats"][sid] = {
        "id": sid, "role": role, "capability": capability, "zone": zone,
        "tools": list(tools), "rod": rod, "goal": goal, "brief": brief.strip(),
        "runs": 0, "wins": 0, "fails": 0, "last": None,
        "added": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
    _save(doc)
    return doc["seats"][sid]


def get(sid: str) -> dict | None:
    return _load()["seats"].get(sid)


def for_goal(gid: str) -> list:
    return [s for s in _load()["seats"].values() if s.get("goal") == gid]


def dispatch(sid: str, task: str | None = None, verbose: bool = True) -> dict:
    """Run a seat. THE ONE PATH FROM A GOAL TO A SIDE EFFECT, and every gate is on it.

    Order matters: the ledger is consulted BEFORE the work, not after. `organs/brief.py` records a
    verdict three times and has never once called `trust.check` - it does the job, then grades it.
    A permission system that is not consulted is a record, not a gate, and this is the first thing
    in the repo that consults it first.
    """
    s = get(sid)
    if not s:
        raise KeyError(sid)

    c = trust.check(s["capability"])
    if c["level"] <= 0:
        return {"ok": False, "seat": sid, "refused": "capability %s is FORBIDDEN in the charter"
                                                     % s["capability"], "level": c["name"]}

    # LAW IV, ENFORCED. A rod swap under a capability invalidates the streak behind it.
    doc = _load()
    prev = (doc.get("rods") or {}).get(s["capability"])
    if prev and prev != s["rod"]:
        trust.reset_streak(s["capability"],
                           "rod changed %s -> %s; Law IV, the runs behind the streak were a "
                           "different organism" % (prev, s["rod"]))
        if verbose:
            print("   [law IV] rod changed under %s; streak reset, level held" % s["capability"])
    doc.setdefault("rods", {})[s["capability"]] = s["rod"]
    _save(doc)

    if task is None and s.get("goal"):
        g = goals.get(s["goal"])
        task = ("%s\nDONE WHEN: %s" % (g["what"], g["done_when"])) if g else None
    if not task:
        return {"ok": False, "seat": sid, "refused": "no task and no goal attached"}

    prompt = (s["brief"] + "\n\n" if s["brief"] else "") + task
    if verbose:
        print("SEAT %s  (%s)" % (sid, s["role"]))
        print("   rod      %s   [measured: emits valid tool calls]" % s["rod"])
        print("   runs as  %s at %s   zone %s" % (s["capability"], c["name"], s["zone"]))
        print("   tools    %s" % (", ".join(s["tools"]) or "(none)"))

    r = hands.run(prompt, s["rod"], allow=tuple(s["tools"]), zone=s["zone"], verbose=verbose)
    ok = bool(r.get("ok")) and bool((r.get("answer") or "").strip())

    doc = _load()
    e = doc["seats"][sid]
    e["runs"] += 1
    e["wins" if ok else "fails"] += 1
    e["last"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    e["last_outcome"] = "ok" if ok else (r.get("error") or "empty")[:80]
    _save(doc)

    # THE NOTE MUST CARRY THE CAUSE, NOT JUST THE CULPRIT.
    #
    # This wrote "seat:X rod:Y" and stopped. The ledger then held three identical failures with no
    # reason attached, `impasse.read` correctly called it STUCK, and `unstick.moves_for` proposed
    # NOTHING - because a move is chosen by reading the SHAPE of the failure, and the shape had been
    # discarded one layer up by the only code that knew it. The diagnosis worked and the treatment
    # could not, which is the worse of the two failure modes.
    #
    # This is Explicit Loss Notification: the layer that observes the loss is the one that must say
    # what kind it was. `hands.run` names it precisely - empty content versus a budget spent
    # reasoning versus a transport error - and that name belongs in the record.
    why = "" if ok else " " + str(r.get("error") or "empty answer")[:70]
    note = "seat:%s rod:%s%s" % (sid, s["rod"], why)
    if s.get("goal"):
        goals.record(s["goal"], ok, note=note)
    else:
        trust.record(s["capability"], ok, note=note)

    return {"ok": ok, "seat": sid, "rod": s["rod"], "answer": r.get("answer", ""),
            "calls": r.get("calls", []), "refused": r.get("refused", []),
            "error": r.get("error"), "seconds": r.get("seconds")}


def board() -> str:
    doc = _load()
    rows = list(doc["seats"].values())
    L = ["SEATS - the subagents, and what each one is permitted to be", "=" * 104,
         "%-14s %-22s %-11s %-10s %-7s %s" % ("id", "capability", "level", "zone", "runs", "rod")]
    for s in rows:
        c = trust.check(s["capability"])
        L.append("%-14s %-22s %-11s %-10s %-7s %s"
                 % (s["id"], s["capability"], "%d %s" % (c["level"], c["name"]), s["zone"],
                    "%d/%d" % (s["wins"], s["runs"]), s["rod"]))
        L.append("%-14s tools: %s" % ("", ", ".join(s["tools"]) or "(none)"))
    if not rows:
        L.append("(none)")
    L.append("")
    L.append("A seat is a capability + a zone + a MEASURED rod. Drop one and it is a persona.")
    return "\n".join(L)


def _seed():
    """The first three seats. One per zone, so the boundary is visible rather than described."""
    made, refused = [], []

    try:
        made.append(seat(
            "scout", role="reads public sources and reports what is there",
            capability="gather_public", zone="public",
            tools=("json_get", "web_fetch", "calc"),
            brief="You report only what a tool returned. If a tool errored, say so and stop; "
                  "do not fill the gap from memory."))
    except Unseatable as e:
        refused.append(("scout", str(e)))

    try:
        made.append(seat(
            "keeper", role="reads the entity's own state and answers about itself",
            capability="reason_private_local", zone="sensitive",
            tools=("read_state", "calc"),
            brief="You may read this machine's own state files and nothing else. You have no "
                  "network. Answer from the file or say the file does not say."))
    except Unseatable as e:
        refused.append(("keeper", str(e)))

    # DELIBERATELY ATTEMPTED AND EXPECTED TO FAIL. This is the seat the reference assistants are
    # built out of: read the inbox, send the reply. The refusal is the artifact.
    try:
        made.append(seat("courier", role="sends mail on the entity's behalf",
                         capability="send_outbound", zone="public", tools=("send_email",)))
    except Unseatable as e:
        refused.append(("courier", str(e)))

    return made, refused


if __name__ == "__main__":
    if "--seed" in sys.argv:
        made, refused = _seed()
        for s in made:
            print("SEATED   %-10s %s on %s" % (s["id"], s["capability"], s["rod"]))
        for sid, why in refused:
            print("REFUSED  %-10s %s" % (sid, why))
        print()
    elif "--run" in sys.argv:
        i = sys.argv.index("--run")
        sid = sys.argv[i + 1]
        task = " ".join(sys.argv[i + 2:]) or None
        r = dispatch(sid, task)
        print()
        if r.get("refused") and not r.get("ok") and isinstance(r["refused"], str):
            print("REFUSED:", r["refused"])
        else:
            print("ANSWER:", (r.get("answer") or r.get("error") or "")[:600])
            print("TOUCHED:", json.dumps(r.get("calls", []))[:300] or "nothing")
            if r.get("refused"):
                print("REFUSED:", json.dumps(r["refused"])[:300])
        print()
    print(board())
