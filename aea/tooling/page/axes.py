"""axes.py - THE TWO AXES AS SERIES: what arrives at each step, and the words for it.

BY CALL HOP and BY RUNG answer different questions and neither replaces the other. Hop depth says
WHAT CALLS WHAT and covers every reachable function; rung says WHAT CAPABILITY THIS IS PART OF and
covers a fifth of them. Both are true, and a reader must never mistake the fifth for the whole -
which is why every caption built here prints its denominator.

This was ~140 lines wedged inside `build()` between the stylesheet and the HTML. It is the part
with the most arithmetic and the most ways to be quietly wrong: the rail once counted two synthetic
nodes as functions while the caption four lines below it did not, and nothing in one long function
compared them. Here both come out of one module and share `_real`.

SYNTHETIC NODES ARE NOT FUNCTIONS. `ENTRY` and `VIA-IMPORT` are scaffolding the drawing invents to
avoid a worse lie (see `layout._tree`); every count in this file filters them out, and hop 0 says
what it is rather than claiming that one function arrived.
"""
from __future__ import annotations

import json

from aea.tooling.page.layout import _pkg


def _real(T: dict) -> list:
    """Nodes that are actually functions. The one place that decision is made."""
    return [n for n in T["pos"] if ":" in n]


# =================================================================================================
# THE HOP AXIS - a slice of a structure that already exists, so it REVEALS.
# =================================================================================================
def hop_series(T: dict) -> tuple:
    """(deepest hop, arrivals per hop, cumulative) over real functions only."""
    maxd = T["maxd"]
    per = {}
    for n in _real(T):
        d = T["depth"].get(n, 9)
        per[d] = per.get(d, 0) + 1
    cum, run = [], 0
    for k in range(maxd + 1):
        run += per.get(k, 0)
        cum.append(run)
    return maxd, per, cum


def hop_captions(T: dict, maxd: int, per: dict) -> list:
    """THE CAPTION IS NOT OPTIONAL. The page honours prefers-reduced-motion, which kills the motion
    channel entirely - so what changed must survive with zero animation, in words, measured."""
    nreal = len(_real(T))
    caps, seen_pkg = [], set()
    for k in range(maxd + 1):
        at_k = [n for n in T["pos"] if T["depth"].get(n) == k]
        real_k = [n for n in at_k if ":" in n]
        new_pk = sorted({_pkg(n) for n in real_k} - seen_pkg)
        seen_pkg |= {_pkg(n) for n in real_k}
        where = ", ".join("aea." + p for p in new_pk) if new_pk else "-"
        creal = len([n for n in T["pos"] if ":" in n and T["depth"].get(n, 99) <= k])
        if not real_k:
            caps.append(f"HOP {k} — the entry bracket, which is not a function. The "
                        f"{per.get(1,0)} real entry points the wake starts from arrive at hop 1.")
            continue
        caps.append(f"HOP {k} — {len(real_k)} function{'s' if len(real_k)!=1 else ''} arrive — "
                    f"{creal} of {nreal} reachable — first reach into {where}")
    return caps


def hop_rail(maxd: int, per: dict, cum: list) -> str:
    return "".join(
        f'<button data-k="{k}" aria-current="{"step" if k==maxd else "false"}">'
        f'<b>HOP {k}</b><span>+{per.get(k,0)}</span><em>{cum[k]}</em></button>'
        for k in range(maxd + 1))


# =================================================================================================
# THE RUNG AXIS - each rung was BUILT ON the ones beneath it, so it ACCUMULATES.
#
# ONE RUNG VOCABULARY, AND IT IS `state/ladder.json`. This list came from `assembly.STEPS`, which
# holds five entries and begins at R2 - so the instrument meant to show the climb could not show
# its first three rungs, and named the rest in a vocabulary the section below it does not use.
# =================================================================================================
def rung_series(lad: dict, T: dict) -> tuple:
    """(rungs as (id, title, record), functions added per rung, cumulative)."""
    rungs = [(str(r.get("id", "")), str(r.get("title", "")), r) for r in (lad.get("rungs") or [])]
    count = {}
    for _n, i in (T.get("rung") or {}).items():
        count[i] = count.get(i, 0) + 1
    cum, run = [], 0
    for i in range(len(rungs)):
        run += count.get(i, 0)
        cum.append(run)
    return rungs, count, cum


def rung_rest(rungs: list) -> int:
    """WHERE THE AXIS COMES TO REST: the FRONTIER - the highest rung carrying any measurement.

    Resting on the LAST rung drew SELF-MODIFICATION in amber as the steady state of the page: a rung
    that is unbuilt and shut on purpose, claimed by the resting frame without a word of text being
    wrong. That was the first correction.

    THIS IS THE SECOND, and it is the opposite mistake. Resting on the highest PROVEN rung parks the
    page on the last thing that finished, so the reader's final impression is a completed thing while
    the work is one rung above it. The frontier is where a rung is measured and not yet met - it has
    numbers, so the page can be honest about it, and it is the only frame where the next thing that
    happens to this system is visible. A page about something still being built should come to rest
    on the part that is still being built."""
    measured = [k for k, (_i, _t, r) in enumerate(rungs) if (r.get("measured") or {})]
    if measured:
        return max(measured)
    return max([k for k, (_i, _t, r) in enumerate(rungs) if r.get("status") != "future"] or [0])


def rung_rail(rungs: list, count: dict, cum: list, rest: int) -> str:
    return "".join(
        f'<button data-k="{k}" aria-current="{"step" if k==rest else "false"}" '
        f'data-st="{r.get("status","future")}">'
        f'<b>{i}</b><span>+{count.get(k,0)}</span><em>{cum[k]}</em></button>'
        for k, (i, _t, r) in enumerate(rungs))


def rung_captions(rungs: list, T: dict, count: dict, cum: list) -> str:
    """THE RUNG CAPTION CARRIES WHAT THE PICTURE CANNOT DRAW: that a rung declaring nothing is not
    a rendering failure. Most of the ladder adds zero functions, and the honest sentence for those
    is what they are WAITING ON, read from the same manifest.

    Nothing here is typed: id, title, blocked_on, standby and beat come from ladder.json, every
    count from the live call graph. Returned as JSON because the page's one integer of state
    indexes into it."""
    nreal = len(_real(T))
    declared = len(T.get("rung") or {})
    out = []
    for k, (rid, rtitle, r) in enumerate(rungs):
        n_k = count.get(k, 0)
        head = (f"{rid} {rtitle} — {n_k} function{'s' if n_k != 1 else ''} declared — "
                f"{cum[k]} of {declared} the ladder names, "
                f"{nreal - declared} of {nreal} live functions declared by no rung.")
        if n_k == 0:
            blocked = r.get("blocked_on")
            head = (f"{rid} {rtitle} — nothing in the live graph belongs to this rung. "
                    + (f"Waiting on {blocked}." if blocked else "Not built.")
                    + f" The organism stops growing here: {cum[k]} of {nreal} functions are"
                      f" declared by any rung, and every one of them was added below this line.")
        # STANDBY IS A DIFFERENT SENTENCE FROM ABSENT, and the picture can only carry it if the
        # caption names it - the dots are out in the field at one and a half pixels.
        sb = r.get("standby") or []
        if sb:
            mods = sorted({f.split(":")[0] for f in sb})
            head += (f" {len(sb)} function{'s' if len(sb) != 1 else ''} for this rung already"
                     f" exist and nothing calls them ({', '.join('aea.' + m for m in mods)},"
                     f" {r.get('standby_state')}) — lit in brass out in the field, because they are"
                     f" written and have never run.")
        # DECLARED BUT UNREACHABLE. A rung may name a function that exists in the tree and that
        # nothing calls - `verify_funcs` checks the name resolves, which is a weaker question than
        # whether the organism can get to it. Saying so costs one clause and stops the rail's count
        # from reading as coverage.
        dead_named = [f for f in (r.get("funcs") or []) if ("aea." + f) not in T["pos"]]
        if dead_named:
            head += (f" {len(dead_named)} declared function"
                     f"{'s' if len(dead_named) != 1 else ''} on this rung "
                     f"{'are' if len(dead_named) != 1 else 'is'} not reachable from the wake: "
                     + ", ".join(sorted(dead_named)) + ".")
        beat = str(r.get("beat") or "").strip()
        out.append(head + ("  " + beat if beat else ""))
    return json.dumps(out)
