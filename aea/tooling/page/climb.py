"""climb.py - THE SUBSYSTEMS, IN THE ONLY ORDER THEY CAN COME ONLINE.

Reads `state/ladder.json` and nothing else. A rung with no instrument renders a dash rather than a
sentence, and that asymmetry is the point: a reader can see at a glance which rungs are receipts and
which are still only claims.

WHAT WAS WRONG WITH THE PREVIOUS VERSION, found by rendering it and reading the image as somebody
who does not work here:

  IT LED WITH WHAT THE SYSTEM CANNOT DO. The list was `column-reverse`, so a stranger landed on
  SELF-MODIFICATION - unbuilt, and shut on purpose - and scrolled past six greyed "waiting on..."
  boxes before reaching anything that had happened. The reverse was chosen so the climb would read
  bottom-to-top like a ladder, and on a scrolling page that inverts reading order against build
  order. Reading order wins: the earned floor first, the dark top last, and the ladder feeling
  carried by a spine that fills rather than by the direction of the list.

  EVERY ROW LOOKED THE SAME. Proven and unbuilt differed by a small badge and a little opacity, so
  the difference that matters most on the page was the one carried by the least ink.

  IT SPOKE ONLY ITS OWN LANGUAGE. `R1.5`, `R4a`, "THE DECISION IS PARSED". Every row now carries a
  plain name in a reader's language beside the formal title - `human` in the manifest, so it is data
  rather than something typed into a template - and a reader can cross between the two vocabularies
  instead of being required to already hold one.

THE FRAME IS A DEEP-SPACE PROBE, AND IT IS ALLOWED TO DESCRIBE THE SHAPE OF THE PROBLEM ONLY.
Spacecraft order is real: nothing does science until the power holds, the clock holds and the radio
holds, and the most impressive thing about a probe that has flown for decades is the least glamorous
one - it is still running. Everything anyone knows about it is telemetry; nobody has seen the
spacecraft. That is this page's epistemology in the metaphor's own words.

What the metaphor may NEVER do is describe the system's properties. It explains why order matters.
It does not say the entity is a spacecraft, and it is kept out of every block that carries a
measured number, so a reader can always tell which is which.
"""
from __future__ import annotations


def _evidence(r: dict, gate: tuple) -> str:
    """The receipt line, assembled from what the measurement actually holds.

    EVERY NUMBER IN THE DENOMINATOR IS READ, NOT TYPED. This printed `%s/8 situations` against a
    criterion that had been retired from the gate, so the published page carried the words
    `None/8 situations` - a hand-typed threshold outliving the thing it measured, on a page whose
    subtitle is that nothing is typed by hand. The gate now arrives as an argument."""
    m = r.get("measured") or {}
    i = r.get("id")
    if i == "R0" and m.get("longest_hours") is not None:
        return "%.1f hours unbroken, %d ticks, %d crashes - the gate is 72 hours" % (
            m["longest_hours"], m.get("longest_ticks") or 0, m.get("crashes") or 0)
    if i == "R1" and m.get("comparable"):
        return "%d of %d comparable ticks chose differently from the floor" % (
            m.get("differed") or 0, m["comparable"])
    if i == "R1.5" and m.get("ticks"):
        return "%d parses, %d receipts, %d swallowed" % (
            m.get("valid") or 0, m.get("receipts") or 0, m.get("swallowed") or 0)
    if i == "R2" and m.get("invocations") is not None:
        bits = ["%s of %s invocations" % (m["invocations"], gate[0] if gate else "?"),
                "%s of %s tools" % (m.get("tools"), gate[1] if len(gate or ()) > 1 else "?")]
        return ", ".join(bits)
    if i == "R3" and m.get("graded") is not None:
        return "%s graded outcomes, %s not repeated, bound %s over %s paired witnesses" % (
            m["graded"], m.get("not_repeated") or 0, m.get("bound"), m.get("bound_pairs"))
    if i == "R4a" and m.get("by_entity") is not None:
        return ("%s looks chosen by the entity, %s carried a reason, %s changed what it examined, "
                "%s distinct thing%s looked at" % (
                    m["by_entity"], m.get("with_reason") or 0, m.get("changed_with_reason") or 0,
                    m.get("distinct") or 0, "" if (m.get("distinct") or 0) == 1 else "s"))
    # A MEASURED RUNG THAT PRINTS "nothing measured here yet" IS THE FALSE DASH THIS PAGE EXISTS TO
    # PREVENT, and it takes one wrong key to produce. R4a landed with `by_entity`/`with_reason`/
    # `distinct` and this function asked for `distinct_sources`, so a PARTIAL rung carrying four
    # real numbers rendered as untouched. A dash must mean the repository cannot prove it - never
    # that the reader of the measurement guessed at its shape. Checked against the manifest below.
    # R4b IS THE FIRST RUNG WHOSE TWO HALVES ARE MEASURED SEPARATELY, and it is drawn that way on
    # purpose. A rung is POWER plus BOUND, and this one had its BOUND certified and taken to a
    # council while nobody had checked whether anything was behind the door - so a line that
    # reported only the certificate would repeat the mistake in the place most people read.
    #
    # `condition_2` is the council, and it is never inferred from the numbers. It stays false until
    # a human records that it happened, because a gate whose last condition is a judgement cannot be
    # closed by arithmetic.
    if i == "R4b" and m.get("condition_1") is not None:
        bits = ["bound: %s, %s outbound request%s, %s leak%s, %s bits of selection channel" % (
            "certified" if m["condition_1"] else "FAILED", m.get("requests"),
            "" if m.get("requests") == 1 else "s", m.get("leaks"),
            "" if m.get("leaks") == 1 else "s", m.get("selection_bits"))]
        if m.get("power"):
            bits.append("power: %s, %s" % (str(m["power"]).lower(), m.get("power_topics")))
        bits.append("council: not reconvened against these numbers")
        return "; ".join(bits)
    if (r.get("measured") or {}) and i not in ("R0", "R1", "R1.5", "R2", "R3", "R4a", "R4b"):
        return "measured, but this page has no reader for %s yet" % i
    return ""


def _climb(lad: dict):
    """The subsystems as a filling spine. Returns (html, css) - both generated, neither typed."""
    from html import escape as esc
    rungs = (lad or {}).get("rungs") or []
    if not rungs:
        return "", ""
    gate = tuple((lad or {}).get("reach_gate") or ())

    # HOW FAR THE CLIMB ACTUALLY GOT. The highest rung that is not `future` - the same integer the
    # animation rests on, because a page whose steady state draws an unbuilt rung in amber claims
    # the top of the ladder without a single word of text being wrong.
    rest = max([k for k, r in enumerate(rungs) if r.get("status") != "future"] or [0])
    earned = sum(1 for r in rungs if r.get("status") != "future")

    items = []
    for k, r in enumerate(rungs):
        st = r.get("status", "future")
        ev = _evidence(r, gate)
        blocked = r.get("blocked_on")
        if ev:
            line = '<p class="rev">%s</p>' % esc(ev)
        elif blocked:
            line = '<p class="rwait">not started &mdash; waiting on %s</p>' % esc(str(blocked))
        else:
            line = '<p class="rwait">nothing measured here yet</p>'
        human = str(r.get("human") or "").strip()
        items.append(
            '<li class="layer" data-k="%d" data-st="%s">'
            '<div class="spine"><i></i></div>'
            '<div class="lbody">'
            '<div class="lhead"><span class="rid">%s</span>'
            '<span class="rhuman">%s</span>'
            '<span class="rstat s-%s">%s</span></div>'
            '<p class="rtitle">%s</p>'
            '<p class="rplain">%s</p>%s</div></li>'
            % (k, st, esc(str(r.get("id", ""))), esc(human), st, st.upper(),
               esc(str(r.get("title", ""))), esc(str(r.get("plain", ""))), line))

    # ONE RULE PER FRAME, as everywhere else on this page: stepping is an attribute write over a
    # layout computed once, so going backward is free and nothing re-flows.
    css = []
    n = len(rungs)
    for k in range(n):
        for d in range(k + 1, n):
            css.append('#climb[data-frame="%d"] .layer[data-k="%d"]{opacity:.3}' % (k, d))
        css.append('#climb[data-frame="%d"] .layer[data-k="%d"]{background:#0e1114}' % (k, k))
        if rungs[k].get("status") != "future":
            css.append('#climb[data-frame="%d"] .layer[data-k="%d"] .rid,'
                       '#climb[data-frame="%d"] .layer[data-k="%d"] .rhuman'
                       '{color:var(--amber)}' % (k, k, k, k))

    rail = "".join('<button data-c="%d" aria-current="%s" data-st="%s">%s</button>'
                   % (k, "step" if k == rest else "false", r.get("status", "future"),
                      esc(str(r.get("id", ""))))
                   for k, r in enumerate(rungs))

    # THE ONE SENTENCE A STRANGER NEEDS, and every number in it is counted rather than written.
    here = ('<p class="youare"><b>%d of %d online.</b> The climb stops at <b>%s</b> &mdash; %s. '
            'Everything above that line is named so that nobody arrives at it by accident.</p>'
            % (earned, n, esc(str(rungs[rest].get("id", ""))),
               esc(str(rungs[rest].get("human") or rungs[rest].get("title") or ""))))

    html = ('<div class="climbwrap">%s'
            '<nav id="crail" aria-label="step through the subsystems">%s</nav>'
            '<ol id="climb" data-frame="%d" data-rest="%d">%s</ol></div>'
            % (here, rail, rest, rest, "".join(items)))
    return html, "\n".join(css)


CLIMB_BASE_CSS = """
.climbwrap{margin:16px 0 6px}
.youare{margin:0 0 14px;color:#8b939c;font-size:12.5px;max-width:78ch}
.youare b{color:#eef1f4;font-weight:600}
#crail{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:14px}
#crail button{font:inherit;font-size:11px;letter-spacing:.06em;padding:4px 9px;cursor:pointer;
 background:#181d22;color:#9aa4ae;border:1px solid #333b44;border-radius:2px}
#crail button[data-st="future"]{color:#5d666f}
#crail button[aria-current="step"]{color:var(--amber);border-color:var(--amber)}

/* READING ORDER IS BUILD ORDER. The floor first, the dark top last. The ladder is carried by the
   spine, which fills where the climb actually reached, not by inverting the list. */
#climb{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:0}
.layer{display:flex;gap:14px;padding:0;background:transparent;
 transition:opacity .45s ease,background .45s ease}
.lbody{flex:1;min-width:0;padding:12px 14px 14px 0}

/* THE SPINE IS THE CLIMB. A continuous rail down the left, SOLID where a subsystem is online and
   hollow where it is not - so the difference that matters most on this page is the one carried by
   the most ink, instead of by a ten-pixel badge. */
.spine{position:relative;width:14px;flex:none}
.spine:before{content:"";position:absolute;left:6px;top:0;bottom:0;width:2px;background:#20262c}
.spine i{position:absolute;left:1px;top:16px;width:12px;height:12px;border-radius:50%;
 background:#0a0c0e;border:2px solid #2b3138;box-sizing:border-box}
.layer[data-st="proven"] .spine:before{background:var(--amber);opacity:.55}
.layer[data-st="proven"] .spine i{background:var(--amber);border-color:var(--amber)}
.layer[data-st="partial"] .spine:before{background:var(--brass);opacity:.45}
.layer[data-st="partial"] .spine i{background:#0a0c0e;border-color:var(--brass)}
.layer[data-st="future"] .spine:before{background:#191d22}
.layer[data-st="future"] .spine i{border-style:dashed}
.layer:first-child .spine:before{top:16px}
.layer:last-child .spine:before{bottom:calc(100% - 24px)}

.lhead{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.rid{font-weight:700;letter-spacing:.08em;color:#6d757e;min-width:38px;font-size:11px}
/* THE PLAIN NAME IS THE HEADLINE, and the formal title sits under it. A reader who has never seen
   this project reads a sentence; a reader who has, still gets the vocabulary. */
.rhuman{font-size:15px;letter-spacing:.01em;color:#dfe3e8}
.rstat{margin-left:auto;font-size:10px;letter-spacing:.1em;padding:1px 6px;
 border:1px solid #2b3138;color:#8b939c}
.s-proven{color:var(--amber);border-color:var(--amber)}
.s-partial{color:var(--brass);border-color:var(--brass)}
.s-future{color:#5d666f;border-color:#262c33}
.rtitle{margin:3px 0 0;font-size:10.5px;letter-spacing:.16em;color:#5c646d}
.rplain{margin:8px 0 5px;color:#939ca6;font-size:12.5px;line-height:1.6;max-width:76ch}
.rev{margin:0;font-size:11.5px;color:var(--brass);font-variant-numeric:tabular-nums}
.rwait{margin:0;font-size:11.5px;color:#5c646d}
@media (max-width:620px){.rstat{margin-left:0}.rplain{font-size:12px}.rhuman{font-size:13.5px}}
@media (prefers-reduced-motion:reduce){.layer{transition:none}}
"""


render = _climb
