"""overture.py - THE FIRST SCREEN. The only part of the page that has to earn the second one.

THREE READERS ARRIVE HERE, AND EVERY DECISION BELOW IS FOR ONE OF THEM.

    A STRANGER FROM A LINK      has ten seconds and no context. Needs to know what they are
                                looking at, be given one true astonishing thing, and be told what
                                the dark means before it reads as a broken image.
    AN ENGINEER, SCEPTICAL      assumes this is LLM theatre until shown otherwise. Needs a receipt
                                in the first screen: a number, its source file, and the sentence
                                that says what is NOT claimed.
    LUIS, SHOWING SOMEONE       needs a moment that lands and nothing that embarrasses him when the
                                person he is showing starts clicking.

One opening serves all three, and it is the same one: STATE THE SMALLNESS FIRST. A page about an
autonomous system that opens by boasting is indistinguishable from every other page about an
autonomous system. This one opens by saying that almost all of it is dark, gives the exact ratio,
and lets the reader check it. Nothing else on the internet in this category does that, which is
both the honest move and the differentiating one.

WHAT WAS WRONG BEFORE. The page began with the instrument - 160 lit dots in a field of 1,243 dark
ones - and no sentence attached. A reader who does not already know the project sees a constellation
and a wall of controls. Every science explainer that works does the opposite: Sagan never opened on
the telescope, he opened on where you are standing, and earned the telescope afterwards.

THE RULE THIS FILE OBEYS. Every number is read from the same measured state the rest of the page
uses. The opening may be dramatic in its ARRANGEMENT and never in its arithmetic - the drama comes
from which true number is given the stage, never from the number.
"""
from __future__ import annotations


def _fmt_hours(h) -> tuple:
    """(number, unit) - days once it stops being legible in hours, because 246.9 h means nothing to
    a reader and 10 days does. The value is not rounded up, ever: 10.2 days is 10.2 days."""
    try:
        h = float(h)
    except (TypeError, ValueError):
        return None, ""
    if h >= 48:
        return ("%.1f" % (h / 24)).rstrip("0").rstrip("."), "days"
    return ("%.1f" % h).rstrip("0").rstrip("."), "hours"


def _day(iso) -> str:
    """`2026-07-10` -> `10 July`. A reader should not have to parse a timestamp.

    NO BLANKET EXCEPT. The first version wrapped the whole parse in `except Exception: return the
    input`, which is D19/D21 in miniature - a missing date, a malformed one and a date this function
    simply cannot handle would all have rendered as the same shrug. The repo's own ratchet caught it
    on the build after it was written. An absent value returns a dash, and a value that is present
    but unparseable is shown VERBATIM, so a reader can see the thing that confused it."""
    MONTHS = ("January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December")
    if not iso:
        return "&mdash;"
    parts = str(iso).split("-")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        return str(iso)
    mth, day = int(parts[1]), int(parts[2])
    if not 1 <= mth <= 12:
        return str(iso)
    return "%d %s" % (day, MONTHS[mth - 1])


def overture(lad: dict, org: dict, T: dict) -> str:
    """The first screen, assembled from measured state. Returns HTML."""
    rungs = (lad or {}).get("rungs") or []
    r0 = next((r for r in rungs if r.get("id") == "R0"), {})
    m0 = r0.get("measured") or {}
    online = sum(1 for r in rungs if r.get("status") != "future")

    live = len(org.get("live") or [])
    total = org.get("functions") or 0
    dark = total - live
    pct = ("%.1f" % (100.0 * live / total)) if total else "&mdash;"

    n, unit = _fmt_hours(m0.get("longest_hours"))
    crashes = m0.get("crashes")
    ticks = m0.get("longest_ticks")

    # THE ONE NUMBER THAT GETS THE STAGE. Not the biggest and not the most flattering - the one a
    # reader can check and cannot shrug at: it ran this long, unattended, and did not fall over.
    if n is None:
        headline = ('<div class="ov-num">&mdash;</div>'
                    '<p class="ov-sub">No run has been measured yet. A dash is a measurement.</p>')
    else:
        # THE ARRANGEMENT MUST NOT IMPLY WHAT THE SENTENCE DOES NOT SAY. "has run" beside a large
        # live-looking counter reads as "it is on day 10.3 RIGHT NOW". This is the LONGEST run, and
        # the record also holds 97 starts since 10 July. It also mixed a per-run count (ticks) with
        # an all-time count (crashes) in one breath. The honest version is the more impressive one.
        headline = (
            '<div class="ov-num">%s<span class="ov-unit">%s</span></div>'
            '<p class="ov-sub">is the longest it has run unattended without falling over '
            '&mdash; %s ticks in one stretch. Across <b>%s starts</b> since %s there have been '
            '<b>%s crashes</b>. That is the least impressive claim available and it is deliberately '
            'first: everything above it is worthless without it.</p>'
            % (n, unit, ticks if ticks is not None else "&mdash;",
               m0.get("boots") if m0.get("boots") is not None else "&mdash;",
               _day(m0.get("first")),
               crashes if crashes is not None else "&mdash;"))

    return (
        '<section class="overture">'
        '<p class="ov-eyebrow">an autonomous entity, drawn from its own state</p>'
        '<h1 class="ov-h1">Almost all of it is dark.</h1>'
        '<div class="ov-lede">'
        '<p>Below is a picture of a program that runs by itself on one machine. The bright marks in '
        'it are the parts its own loop can reach when it wakes: <b>%s of %s functions</b>, which '
        'is <b>%s per cent</b>. The other %s are written, committed, and cannot be reached by any '
        'call this scanner can follow &mdash; and %s calls in the tree resolve to nothing it can '
        'name, so that percentage is a floor rather than a measurement of the whole.</p>'
        '<p>That ratio is the story, and this page will not round it up. Every number here was read '
        'from a file the system wrote about itself &mdash; nothing is typed by hand, nothing is '
        'simulated, and a value that could not be measured is shown as a dash rather than a guess. '
        'It is telemetry from something you cannot see directly.</p>'
        '</div>'
        '<div class="ov-stage">%s</div>'
        '<p class="ov-floor">%d of %d subsystems are online. What that means, what each one cost, '
        'and what is deliberately shut &mdash; below. You can walk the picture yourself: one call at '
        'a time, or one subsystem at a time.</p>'
        '<p class="ov-ceiling"><b>What this page does not claim.</b> That a reachable function does '
        'useful work. That the system understands anything. That a subsystem is finished because its '
        'wiring is. Every proof here is a receipt that something ran &mdash; never an assertion '
        'about what it is.</p>'
        '</section>'
        % (live, total, pct, dark, org.get('unresolved') or 0, headline, online, len(rungs)))


def coda(lad: dict) -> str:
    """THE LAST THING READ, and the page did not have one.

    The arc peaked at the top rung - a door named so that nobody arrives at it by accident - and was
    then followed by three appendices, closing on a line about a JSONL file. A page that climaxes and
    then files paperwork leaves its strongest available feeling entirely to inference: somebody built
    the ability to open a door, did not open it, and can prove both halves of that.

    Every number here is counted from the manifest. The claim ceiling holds: nothing below asserts
    the system wants, understands or intends anything."""
    rungs = (lad or {}).get("rungs") or []
    if not rungs:
        return ""
    online = sum(1 for r in rungs if r.get("status") != "future")
    # THE DOOR IS THE FIRST RUNG THAT IS NOT DONE AND ALREADY HAS CODE BEHIND IT. Selecting on
    # `future` missed it: the rung in question is `partial` - certified on one condition, shut on
    # the other - which is exactly what makes it the interesting one.
    shut = next((r for r in rungs if r.get("status") != "proven" and r.get("standby")), None)
    total = len(rungs)

    door = ""
    if shut is not None:
        n_sb = len(shut.get("standby") or [])
        door = ('The next one is written, certified, and deliberately unwired: the code that would '
                'let it reach outside this machine exists%s, it has been run with no socket open, '
                'and it '
                'has no caller. Four reviewers refused that design three times and have not been '
                'asked again. ' % (" - %d functions of it -" % n_sb if n_sb else ""))

    return ('<section class="coda">'
            '<p>%d of %d subsystems are online. %sNothing above that line is a plan; it is a list of '
            'things that would each need a stated hazard before anyone built them.</p>'
            '<p class="coda-last">The loop is running while you read this. The counter at the top '
            'will be larger tomorrow, and that is the whole claim.</p>'
            '</section>' % (online, total, door))


OVERTURE_CSS = """
/* THE OPENING. Scale contrast is the whole device: an eyebrow, one large plain sentence, a reading
   column, then ONE number at a size nothing else on the page comes near. Editorial pages earn
   attention with rhythm rather than with ornament, and this page has exactly one ornament budget -
   spend it here, on a true number, and nowhere else. */
.overture{margin:0 0 60px;padding:0 0 46px;border-bottom:1px solid #16191d}
.ov-eyebrow{font:500 10.5px/1.4 var(--mono);letter-spacing:.22em;text-transform:uppercase;
 color:#5c646d;margin:0 0 22px}
.ov-h1{font:400 clamp(34px,6.2vw,62px)/1.06 var(--prose);letter-spacing:-.015em;color:#eef1f4;
 margin:0 0 26px;max-width:16ch}
.ov-lede{max-width:60ch}
.ov-lede p{margin:0 0 16px;font:17px/1.66 var(--prose);color:#a8b1ba}
.ov-lede b{color:#eef1f4;font-weight:600}
/* THE NUMBER GETS A STAGE, and the stage is emptiness rather than a box. */
.ov-stage{display:flex;align-items:baseline;gap:26px;flex-wrap:wrap;margin:44px 0 34px;
 padding:26px 0 0;border-top:1px solid #16191d}
.ov-num{font:clamp(56px,11vw,116px)/0.92 var(--mono);color:var(--amber);letter-spacing:-.045em;
 font-variant-numeric:tabular-nums}
.ov-unit{font-size:.28em;letter-spacing:.16em;color:#6d757e;margin-left:.32em;
 text-transform:uppercase;vertical-align:baseline}
.ov-sub{flex:1;min-width:290px;max-width:46ch;margin:0;font:15px/1.6 var(--prose);color:#96a0aa}
.ov-sub b{color:var(--amber);font-weight:600;font-family:var(--mono)}
.ov-floor{max-width:64ch;margin:0 0 20px;font:15px/1.62 var(--prose);color:#96a0aa}
.ov-ceiling{max-width:66ch;margin:0;padding:14px 0 0;border-top:1px solid #14171b;
 font:13.5px/1.6 var(--prose);color:#6d757e}
.ov-ceiling b{color:var(--brass);font-family:var(--mono);font-size:11px;letter-spacing:.12em;
 text-transform:uppercase;display:block;margin-bottom:5px}
@media (max-width:620px){.ov-stage{gap:14px}.ov-num{letter-spacing:-.03em}}
/* THE ENDING. It gets the same air as the opening, because it is the other bookend and the page
   had only one. */
.coda{margin:var(--s6) 0 0;padding:var(--s5) 0 0;border-top:1px solid #1c2025}
.coda p{margin:0 0 var(--s4);max-width:64ch;font:var(--t3)/1.66 var(--prose);color:#a8b1ba}
.coda-last{font-size:var(--t4);color:#dfe3e8;max-width:52ch}
"""
