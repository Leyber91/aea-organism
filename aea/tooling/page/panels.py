"""panels.py - THE NUMBER PANELS: the certificate, the wiring manifest, the fleet, the growth.

Every value here is read from a file the running system wrote, and an absent store renders an em
dash rather than a zero. That distinction is the whole honesty law in one character: a zero is a
measurement that came back empty and a dash is a measurement that was never taken, and a picture
is exactly where a comfortable guess would never be noticed.

THE CERTIFICATE PANEL EXISTS BECAUSE A POOLED NUMBER LIED TWICE. `redteam` attacks six tools; five
take an argument SELECTED from a closed table, so a byte the entity wrote cannot reach them by
construction and their crossings are not trials of anything. Pooling all six produced a bound that
was arithmetically correct and the wrong statistic - it stated a bound on channels that need none
while hiding the bound on the one that does. Both numbers are published here, and the pooled one
carries "do not quote this" in its own caption.
"""
from __future__ import annotations


def certificate(cert: dict) -> dict:
    """The red-team certificate, formatted. Any missing field becomes a dash, never a zero.

    EXACTLY WHAT THE PAGE PRINTS, AND THE SPLIT IS WHY THAT IS KNOWN. `build()` computed thirteen
    of these and the template consumed six: `payloads`, `bound_pct`, the tool count and the
    certificate date were formatted on every build and printed nowhere, left behind when the
    section was rewritten around the alphabet proof. Nothing could see it, because the producer and
    the consumer were four hundred lines apart in one function. With the template's inputs as a
    signature, a value with no reader is a TypeError on the next build rather than a line nobody
    reads - which is the whole argument for the split, in one concrete case.

    The retired four are in git. They are not deleted because they were wrong; they are gone
    because a number that is computed and not shown is not a measurement of anything."""
    per_tool = cert.get("per_tool") or {}
    alpha = cert.get("alphabet") or {}
    return dict(
        cert_cross=cert.get("crossings") or "&mdash;",
        cert_leaks=len(cert.get("leaks") or []) if cert.get("leaks") is not None else "&mdash;",
        cert_per=", ".join("%s %d" % (k, v)
                           for k, v in sorted(per_tool.items(), key=lambda x: -x[1])) or "&mdash;",
        cert_alpha=alpha.get("admitted") or "&mdash;",
        cert_space="{:,}".format(alpha["space"]) if alpha.get("space") else "&mdash;",
        cert_letters=alpha.get("alphabetic") if alpha.get("alphabetic") is not None else "&mdash;",
    )


def step_rows(asm: dict) -> str:
    """THE LADDER - WHAT IS WIRED, from `assembly.json`. A step is DONE only when every function in
    it has a caller reachable from an entry point."""
    return "".join(
        f'<div class="step {"done" if s.get("state")=="DONE" else "open"}">'
        f'<b>{s.get("state")}</b><span>{s.get("step")}</span>'
        f'<em>{s.get("have")}/{s.get("need")}</em></div>' for s in (asm.get("steps") or []))


def fleet(cen: dict) -> tuple:
    """(rendered rows, all rods, frontier rods, exam size) from the census they were measured on."""
    rods = sorted((cen.get("models") or []),
                  key=lambda m: (-(m.get("score") or 0), m.get("avg_latency") or 99))
    mx = len(cen.get("battery") or []) or 12
    frontier = [r for r in rods if (r.get("score") or 0) >= round(mx * 0.83)]
    rows = "".join(
        f'<div class="rod"><span class="s">{r.get("score")}/{mx}</span>'
        f'<span class="m">{r.get("model")}</span>'
        f'<span class="l">{r.get("avg_latency")}s</span></div>' for r in frontier[:14])
    return rows, rods, frontier, mx


def growth(history: list) -> str:
    """THE LIVE SURFACE OVER TIME - one bar per recorded run, appended, never recomputed."""
    gmax = max([h.get("live", 0) for h in history] or [1])
    return "".join(
        f'<div class="g"><i style="height:{max(4, round(100*h.get("live",0)/gmax))}%"></i>'
        f'<span>{h.get("live")}</span></div>' for h in history[-14:])

