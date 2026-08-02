"""dispatch_power.py - DOES THE OTHER HALF OF R4b ACTUALLY WORK? The POWER, measured.

    python -m aea.lab.dispatch_power            run it
    python -m aea.lab.dispatch_power --json     also write state/dispatch_power.json

WHY THIS EXISTS, AND IT IS A CORRECTION TO MY OWN WORK.

`dispatch_cert.py` certifies R4b's BOUND: no byte of any outbound request originates from model
output, enumerated over a finite domain, 0 leaks. It is a good certificate and it proves half a rung.

A rung is POWER plus BOUND wearing one name, and this repo's oldest recorded defect is that only one
half ever gets gated. So a council was convened to judge whether to open a door - while NOBODY HAD
CHECKED WHETHER ANYTHING IS BEHIND IT. Measured: `dispatch.run` has zero callers and has never
executed, and `web_search` has NEVER BEEN INVOKED ONCE across 121 ledger rows. The safest possible
design is one that returns nothing, and `dispatch.py`'s own docstring says a design that is safe by
being useless should say so.

WHAT THIS MEASURES, and none of it is a security claim:

  reaches      does web_search execute at all, and return text
  survives     how many returned URLs survive the topic's domain allowlist. IF THIS IS ZERO the
               rung is safe and worthless, and that is a finding, not a pass
  fetches      do the surviving URLs actually return a body
  useful       is there enough content for the entity to have learned anything

STAMPED AS A PROBE, NEVER AS THE ENTITY. This opens real sockets, and a human running a probe is not
the entity choosing to reach the world - that distinction is the whole rung. Every call here goes
through an invoke that stamps `src="probe"`, so no row it produces can ever grade R4b. The harness
that once stamped `src="wake"` on 16 substituted actions blamed the entity for a move it never
chose; this is that lesson applied before the fact rather than after.
"""
from __future__ import annotations

import json
import sys
import time

from aea.kernel import dispatch, grid

OUT = "dispatch_power.json"


def _probe_invoke(name: str, args: dict):
    """The real tools, in the public zone, stamped so this can never be read as the entity acting."""
    from aea.kernel import hands
    return hands.invoke(name, args, zone="public", allow=("web_search", "web_fetch"), src="probe")


def measure(topic: str) -> dict:
    row = dict(topic=topic, query=None, searched=False, search_chars=0, urls=0, survived=0,
               fetched=0, body_chars=0, refused=[], hosts=[], error=None)
    try:
        p = dispatch.plan(topic)
    except dispatch.Refused as e:
        row["error"] = "plan refused: %s" % e
        return row
    row["query"] = p["query"]
    t0 = time.time()
    try:
        raw = _probe_invoke("web_search", {"query": p["query"]})
    except Exception as e:
        row["error"] = "web_search: %s: %s" % (type(e).__name__, str(e)[:110])
        return row
    row["searched"] = True
    row["search_chars"] = len(str(raw))
    # Reuse the module's own extraction rather than re-implementing it - a probe that rebuilds the
    # thing it measures is testing its own copy.
    d = dispatch.dry(topic, serp=str(raw))
    fetches = [r for r in d["requests"] if r["tool"] == "web_fetch"]
    import re as _re
    row["urls"] = len({u for u in _re.findall(r"https?://[^\s\)\]\"'<>]+", str(raw))})
    row["survived"] = len(fetches)
    row["refused"] = [x["url"][:90] for x in d["refused"]][:6]
    row["hosts"] = sorted({dispatch._host(r["bytes"]) for r in fetches})
    for r in fetches:
        try:
            body = _probe_invoke("web_fetch", {"url": r["bytes"]})
            row["fetched"] += 1
            row["body_chars"] += len(str(body))
        except Exception as e:
            row["refused"].append("%s :: %s" % (r["bytes"][:60], str(e)[:60]))
    row["seconds"] = round(time.time() - t0, 1)
    return row


def run() -> dict:
    rows = [measure(t) for t in dispatch.topics()]
    reached = [r for r in rows if r["searched"]]
    productive = [r for r in rows if r["fetched"] > 0]
    starved = [r for r in rows if r["searched"] and r["survived"] == 0]
    return dict(
        claim="whether R4b's POWER half functions at all. NOT a security claim - the BOUND is "
              "certified separately by dispatch_cert, and neither certificate substitutes for the "
              "other.",
        topics=len(rows),
        search_works=len(reached),
        topics_with_a_survivor=len([r for r in rows if r["survived"] > 0]),
        topics_that_fetched=len(productive),
        starved_by_the_allowlist=[r["topic"] for r in starved],
        total_body_chars=sum(r["body_chars"] for r in rows),
        rows=rows,
        src="probe",
        not_claimed=[
            "that any of this is safe. dispatch_cert certifies the bound; this measures only "
            "whether anything comes back",
            "that the entity did any of it. Every call is stamped src=probe and cannot grade R4b",
            "that the content is true. A fetched page is third-party text and stays untrusted",
        ],
        verdict=("FUNCTIONS" if productive else
                 "SAFE AND USELESS - the door opens onto nothing" if reached else
                 "THE SEARCH TOOL DOES NOT WORK"))


if __name__ == "__main__":
    r = run()
    if "--json" in sys.argv:
        grid.atomic_save_json(OUT, r, indent=1)
        print("wrote %s" % OUT)
    print("=" * 100)
    print("R4b POWER - does anything actually come back?   (src=probe, never the entity)")
    print("=" * 100)
    print("  %s" % r["claim"])
    print()
    print("  %-26s %-7s %-6s %-9s %-8s %s" % ("topic", "search", "urls", "survived", "fetched",
                                              "body"))
    for x in r["rows"]:
        print("  %-26s %-7s %-6s %-9s %-8s %s"
              % (x["topic"], "ok" if x["searched"] else "FAIL", x["urls"], x["survived"],
                 x["fetched"], x["body_chars"]))
        if x["error"]:
            print("      error: %s" % x["error"])
        if x["hosts"]:
            print("      hosts: %s" % ", ".join(x["hosts"])[:88])
    print()
    print("  search worked on          %d/%d topics" % (r["search_works"], r["topics"]))
    print("  had a surviving url on    %d/%d" % (r["topics_with_a_survivor"], r["topics"]))
    print("  actually fetched on       %d/%d" % (r["topics_that_fetched"], r["topics"]))
    print("  starved by the allowlist  %s" % (r["starved_by_the_allowlist"] or "none"))
    print()
    for n in r["not_claimed"]:
        print("    not claimed: %s" % n)
    print()
    print("  VERDICT: %s" % r["verdict"])
