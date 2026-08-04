"""invariants.py - WHAT THE SYSTEM CHECKS ABOUT ITSELF, and what those checks have caught.

THE CLAIM THIS SECTION EXISTS TO MAKE, and it is the last one the page was not making: every other
section reports what the system IS. This one reports how it is KEPT honest - and the verdict is
produced by a machine on a schedule rather than by a person remembering to look.

WHY IT IS NOT DECORATION. The finding underneath it was expensive: *a detection that changes no
number and fails no command is indistinguishable from no detection.* A sweep found 118 advisory
findings and nothing anywhere recorded that it was 118, so the 119th was invisible by construction.
Every ratchet below is that lesson wearing a number - a committed baseline that may fall freely and
may not rise without somebody writing a sentence explaining why.

READ FROM `state/selfcheck.json`, which the checker writes on every run. Nothing here is a
description of a check; it is the check's own last verdict, including the one that is ADVISORY and
must never be allowed to read as a pass - a style violation with zero blast radius shared a verdict
line with the privacy guard once, kept that line permanently red, and so the rule this repo calls
absolute could not signal.
"""
from __future__ import annotations


# THE CHECKS A READER CANNOT INTERPRET WITHOUT ONE CLAUSE. Their own `detail` is written for the
# person who runs them; this is the same fact in a stranger's language. Keyed on a stable prefix
# because the frozen-behaviour check carries its own count in its name.
_PLAIN = {
    "structure": "how much of the tree the running loop can reach, and how much it cannot",
    "state intact": "the durable stores still load, and the save that must never be lost is there",
    "no private data": "nothing in any tracked file identifies a person, a client, or this machine",
    "private stores": "the stores that hold private material are excluded from the repository",
    "no absolute paths": "no file knows where it lives except through one resolved root",
    "every module imports": "every module still loads - a module that cannot be imported is dead "
                            "in an unattended run and says nothing about it",
    "frozen behaviours": "recorded behaviours re-run on scripted input. Two are frozen at a "
                         "KNOWN-BAD value on purpose: fixing the reader is supposed to break them",
    "house style": "an advisory rule, and it reports rather than blocks - a style violation must "
                   "never be able to mask an invariant",
    "defect ratchet": "counted defect classes may not RISE against a committed baseline. This is "
                      "the one that turns a detection into something that can fail",
}


def _plain(name: str) -> str:
    for k, v in _PLAIN.items():
        if k in name:
            return v
    return ""


def invariants(sc: dict) -> str:
    """The self-check manifest, as the page's last section before the ending."""
    checks = (sc or {}).get("checks") or []
    if not checks:
        return ""
    from html import escape as esc

    rows = []
    for c in checks:
        name = str(c.get("check") or "")
        advisory = bool(c.get("advisory"))
        ok = bool(c.get("pass"))
        # AN ADVISORY IS NOT A PASS AND MUST NOT WEAR ITS BADGE. It reports and never blocks; saying
        # HOLDS over it would make the weakest check look exactly like the strongest.
        state = "note" if advisory else ("holds" if ok else "failing")
        rows.append(
            '<div class="inv" data-state="%s">'
            '<span class="inv-mark" aria-hidden="true"></span>'
            '<div class="inv-body"><p class="inv-name">%s</p>'
            '<p class="inv-plain">%s</p>'
            '<p class="inv-detail">%s</p></div>'
            '<span class="inv-state">%s</span></div>'
            % (state, esc(name), esc(_plain(name)), esc(str(c.get("detail") or "")),
               state.upper()))

    held = sum(1 for c in checks if c.get("pass") and not c.get("advisory"))
    total = sum(1 for c in checks if not c.get("advisory"))
    secs = sc.get("seconds")
    when = str(sc.get("at") or "")[:16]
    foot = ('<p class="src">state/selfcheck.json &mdash; <code>python -m aea.tooling.selfcheck</code>, '
            '%s of %s blocking invariants held on the last run, which took %s seconds and finished '
            '%s. A failing invariant refuses the commit; an advisory one never can.</p>'
            % (held, total, ("%.0f" % secs) if secs else "&mdash;", when or "&mdash;"))
    return '<div class="invs">%s</div>%s' % ("".join(rows), foot)


INVARIANTS_CSS = """
/* THE SELF-CHECK. A list, not a dashboard: the state is carried by one mark and one word, and the
   sentence explaining each check gets more room than its verdict, because the verdict is the least
   surprising thing on the row. */
.invs{margin:var(--s4) 0 var(--s3)}
.inv{display:flex;gap:var(--s3);align-items:flex-start;padding:var(--s3) 0;
 border-bottom:1px solid #131619}
.inv-mark{flex:none;width:8px;height:8px;margin-top:6px;border-radius:50%;
 background:#0a0c0e;border:2px solid #2b3138;box-sizing:border-box}
.inv[data-state="holds"] .inv-mark{background:var(--amber);border-color:var(--amber)}
.inv[data-state="note"] .inv-mark{border-color:var(--brass);border-style:dashed}
.inv[data-state="failing"] .inv-mark{background:#c2453a;border-color:#c2453a}
.inv-body{flex:1;min-width:0}
.inv-name{margin:0;font:600 var(--t1)/1.4 var(--mono);letter-spacing:.09em;text-transform:uppercase;
 color:#dfe3e8}
.inv-plain{margin:var(--s1) 0 0;font:var(--t2)/1.6 var(--prose);color:#96a0aa;max-width:70ch}
.inv-detail{margin:var(--s1) 0 0;font:var(--t0)/1.5 var(--mono);color:var(--f1);
 overflow-wrap:anywhere}
.inv-state{flex:none;font:var(--t0)/1.6 var(--mono);letter-spacing:.12em;color:var(--f1)}
.inv[data-state="holds"] .inv-state{color:var(--amber)}
.inv[data-state="note"] .inv-state{color:var(--brass)}
.inv[data-state="failing"] .inv-state{color:#c2453a}
@media (max-width:620px){.inv{flex-wrap:wrap}.inv-state{margin-left:20px}}
"""
