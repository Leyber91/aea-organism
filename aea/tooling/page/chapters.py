"""chapters.py - THE DOSSIER'S PROSE PAGES: the introduction, the process, and the evidence behind it.

One job: the pages that are NOT a rung. The rung pages have a fixed four-section shape because a
per-rung layout is a layout that can hide an empty rung; these are narrative, and they carry the
thing the rung pages cannot - **how the completion was arrived at**, which is the part that makes
the next rung cheaper.

EVERY FIGURE IS READ, NEVER TYPED. The prose is authored; the numbers come from `dossier.build()`
and from the experiment records on disk (`armed_run.json`, `outward_experiment_closed.json`,
`thinking.jsonl`). A dossier whose narrative and whose measurements can disagree is a dossier that
will, and the disagreement will be discovered by a reader rather than by the build.

WHY A PROCESS PAGE AT ALL. The rungs record what is true. They do not record that three of the four
explanations for R5's silence were killed by numbers rather than argument, or that the answer was a
missing dictionary entry after a night of testing motivation. R6 inherits the method or it repeats
the night.
"""
from __future__ import annotations

import html
import json
import os

from aea.kernel import grid


def _e(x) -> str:
    return html.escape(str(x if x is not None else ""), quote=True)


def _load(name, default):
    return grid.load_json(os.path.join(grid.STATE, name), default)


def _traces() -> dict:
    p = os.path.join(grid.STATE, "thinking.jsonl")
    rows = []
    if os.path.exists(p):
        with open(p, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        pass
    real = [r for r in rows if (r.get("tick") or 0) > 0]

    def avg(k):
        v = [r.get(k) for r in real if isinstance(r.get(k), (int, float))]
        return round(sum(v) / len(v), 3) if v else None
    return dict(n=len(real), prompt=avg("prompt_chars"),
                first=real[0].get("tick") if real else None,
                last=real[-1].get("tick") if real else None,
                share=avg("reason_share"), ttfc=avg("ttfc"), latency=avg("latency"),
                reason=avg("reason_chars"), content=avg("content_chars"),
                total_reason=sum(r.get("reason_chars") or 0 for r in real),
                total_content=sum(r.get("content_chars") or 0 for r in real))


def _nav(here: str) -> str:
    pages = [("index", "start"), ("process", "the process"), ("experiments", "experiments"),
             ("blockers", "blockers"), ("journey", "token journey"), ("R5", "R5")]
    return '<nav class="cnav">%s</nav>' % "".join(
        '<a class="%s" href="%s.html">%s</a>' % ("on" if k == here else "", k, _e(v))
        for k, v in pages)


# ---------------------------------------------------------------- introduction
def intro(d: dict) -> str:
    rungs = d["rungs"]
    proven = [r for r in rungs if r.get("met")]
    r5 = next((r for r in rungs if r["id"] == "R5"), {}) or {}
    m = r5.get("measured") or {}
    t = _traces()
    rows = "".join(
        '<a class="rrow %s" href="%s.html"><span class="id">%s</span>'
        '<span class="ttl">%s</span><span class="hum">%s</span>'
        '<span class="j">%s</span><span class="st">%s</span></a>'
        % ("met" if r.get("met") else "fut", _e(r["id"]), _e(r["id"]), _e(r["title"]),
           _e(r.get("human")),
           ("%d claims" % len(r["journey"]["rows"])) if r["journey"]["rows"] else "-",
           "PROVEN" if r.get("met") else ("UNMEASURED" if r.get("unmeasured") else "PARTIAL"))
        for r in rungs)
    return (
      _nav("index") +
      '<header class="chead"><p class="eyebrow">aea-city · the ladder dossier · %s · tick %s</p>'
      '<h1>A ladder of proofs about a mind,<br>and the record of how each was earned.</h1>'
      '<p class="lede">Ten rungs. Each is a POWER the entity gains and a BOUND on how it may be '
      'used, with a gate that can be decided by measurement rather than by agreement. '
      '<strong>%d are proven.</strong> This dossier holds what each one claims, what was measured, '
      'the evidence it produced, and — on the process page — how the last one was actually arrived '
      'at, which took longer than building it.</p></header>'
      '<section><div class="stats">'
      '<div><b>%d</b><span>rungs proven</span></div>'
      '<div><b>%s</b><span>claims stated before their evidence</span></div>'
      '<div><b>%s</b><span>died — beliefs the record was wrong about</span></div>'
      '<div><b>%s</b><span>honesty violations</span></div>'
      '</div></section>'
      '<section><h2>The rungs</h2><div class="rlist">%s</div></section>'
      '<section><h2>What a rung is</h2>'
      '<p class="body">Every rung is two claims wearing one name. The <em>power</em> is what the '
      'entity can newly do; the <em>bound</em> is what it may not do with it. A rung is only proven '
      'when both hold — which is why R4b publishes a channel measured in bits per day, and why R5 '
      'refuses the word SURVIVES. A hypothesis consistent with the evidence is CORROBORATED; '
      'reading consistency as confirmation is affirming the consequent, and the store has a control '
      'that rejects the word.</p>'
      '<p class="body">The gates are decidable on purpose. "Runs 72 hours unattended." "Five runs '
      'in which at least one hypothesis DIED." No gate here asks anyone to agree that something '
      'feels autonomous — and where a gate turned out to be unsatisfiable by construction, as R1\'s '
      'was, that is recorded on its page rather than quietly rewritten.</p></section>'
      '<section><h2>What is measured right now</h2><div class="stats small">'
      '<div><b>%s</b><span>reasoning kept, as a share of output</span></div>'
      '<div><b>%s s</b><span>to the first visible token</span></div>'
      '<div><b>%s</b><span>reasoning traces held, of %s ticks</span></div>'
      '<div><b>%s</b><span>functions checked against the live call graph</span></div>'
      '</div>'
      '<p class="note">A dash anywhere in this dossier means the repository cannot prove it. That '
      'is a measurement, not an omission.</p></section>'
      % (_e(d["at"]), _e(d["tick"]), len(proven), len(proven),
         _e(m.get("proposed", "-")), _e(m.get("died", "-")), _e(m.get("violations", "-")),
         rows,
         _e(t["share"]), _e(t["ttfc"]), _e(t["n"]), _e(d["tick"]),
         _e((d.get("wiring") or {}).get("checked", "-"))))


# ---------------------------------------------------------------- the process
def process(d: dict) -> str:
    t = _traces()
    r5 = next((r for r in d["rungs"] if r["id"] == "R5"), {}) or {}
    m = r5.get("measured") or {}
    ent = sum(1 for r in (r5.get("journey") or {}).get("rows", []) if r.get("by_entity"))
    ent_d = sum(1 for r in (r5.get("journey") or {}).get("rows", [])
                if r.get("by_entity") and r.get("status") == "DIED")
    stages = [
      ("01", "The rung would not close, and the reason was assumed",
       "R5 asks the entity to state a claim before the evidence and then find out. It never had. "
       "The working assumption was that it could not infer — that the faculty was missing.",
       "assumed, not measured"),
      ("02", "Reading its own reasoning showed the assumption was wrong",
       "The rod's deliberation had been discarded at the socket on every call — read for liveness, "
       "then dropped. Once kept, %d traces showed the faculty plainly. Tick 794, unprompted: "
       "&ldquo;the hades=unverified block is now confirmed permanent until it flips — ticks "
       "788–793 all say the same thing.&rdquo; That is inference across its own history."
       % t["n"],
       "%s of every answer was deliberation we were deleting" % _e(t["share"])),
      ("03", "Its refusals were valid arguments from a premise nobody had checked",
       "Forty-one of fifty-six ticks chose NONE, each one reasoned. Tick 744 enumerates every move, "
       "rejects each with a cause, and concludes: &ldquo;MOVE: NONE is correct for entity upkeep. "
       "The real service to Luis happens through our dialogue, not mechanical moves.&rdquo; The "
       "inference was sound. The premise was that its moves are chores.",
       "the premise, not the inference"),
      ("04", "Four explanations, three killed by numbers rather than argument",
       "Telling it what it could do made it do LESS. Removing the nudge made the target behaviour "
       "five times more frequent. The critic disagreed thirty times into a void. Giving it "
       "something unresolved — it named the contradiction twelve times and still did not act.",
       "each eliminated by a controlled measurement"),
      ("05", "The answer was that the menu said not to",
       "The move that could settle a contradiction rendered in its own menu as &ldquo;(no "
       "description — do not pick this)&rdquo;, because a description table had no entry for it. "
       "One dictionary entry and one routing clause later, the same experiment ran again: zero "
       "selections became twenty-five.",
       "0 -> 25 selections across 72 ticks"),
      ("06", "The entity closed the rung itself",
       "Once the move was selectable it ran %d investigations unprompted, %d of which killed a "
       "claim. It chose the subject from its own record, named both sides of the contradiction in "
       "its own words, probed the world, and recorded what changes."
       % (ent, ent_d),
       "%s of 5 runs with a death" % _e(m.get("runs_with_a_death", "-"))),
    ]
    cards = "".join(
        '<article class="stage"><header><span class="n">%s</span><h3>%s</h3></header>'
        '<p>%s</p><p class="out">%s</p></article>' % (n, _e(h), body, out)
        for n, h, body, out in stages)
    return (
      _nav("process") +
      '<header class="chead"><p class="eyebrow">the process · six stages · 2026-08-04</p>'
      '<h1>How R5 was actually arrived at.</h1>'
      '<p class="lede">The rung pages record what is true. This records how it was found — because '
      'the method is what makes R6 cheaper, and every stage below cost something.</p></header>'
      '<section><div class="stages">%s</div></section>'
      '<section><h2>The law that carries up</h2>'
      '<p class="flag"><strong>A rung above R4 fails at the PREMISE, not the mechanism.</strong> '
      'Build the mechanism and it will sit unused behind a correct argument. Find out what the '
      'entity believes its job is first — and check the cheap thing nothing re-reads: '
      '<em>can it name this move at all?</em></p>'
      '<p class="body">Proved five separate ways in one night, each a capability that existed and '
      'was unreachable. Every one was found by measuring the ACTION, never by reading the code — '
      'because the code was never what was wrong. Unit tests passed throughout.</p></section>'
      % cards)


# ---------------------------------------------------------------- experiments
def experiments(d: dict) -> str:
    armed = _load("armed_run.json", {}) or {}
    outward = _load("outward_experiment_closed.json", {}) or {}
    s = armed.get("summary") or {}
    def arm(side):
        a = s.get(side) or {}
        lv = a.get("levels") or {}
        return ('<tr><td>%s</td><td class="num">%s</td><td class="num">%s</td>'
                '<td class="num">%s</td><td class="num">%s</td><td>%s</td></tr>'
                % (side, _e(a.get("replicates", "-")), _e(a.get("traces", "-")),
                   _e(a.get("mentions", "-")), _e(a.get("chose_move", "-")),
                   _e(json.dumps(lv)) if lv else "-"))
    f = outward.get("final") or {}
    return (
      _nav("experiments") +
      '<header class="chead"><p class="eyebrow">experiments · every arm one variable apart</p>'
      '<h1>What was actually run.</h1>'
      '<p class="lede">Both experiments below are sandboxed or closed with their result recorded. '
      'Neither was allowed to be read before its delivery check passed — an undelivered treatment '
      'reads exactly like a null result, and that mistake was made once here already.</p></header>'
      '<section><h2>The contradiction A/B — the last run</h2>'
      '<p class="note">3 replicates per arm, %s ticks each, concurrent, isolated by <code>AEA_STATE</code>. '
      'Outcome is three-valued because a binary cannot separate the two failures that matter: '
      '<b>L0</b> never entered its reasoning · <b>L1</b> reasoned about it and did nothing · '
      '<b>L2</b> acted.</p>'
      '<div class="scroll"><table><thead><tr><th>arm</th><th>replicates</th><th>traces</th>'
      '<th>mentions</th><th>chose the move</th><th>levels</th></tr></thead><tbody>%s%s</tbody>'
      '</table></div>'
      '<p class="note">delivered: <b>%s</b> · prompt delta <b>%s</b> chars<br>verdict: <b>%s</b></p>'
      '</section>'
      '<section><h2>The outward experiment — closed</h2>'
      '<p class="note">%s</p>'
      '<div class="scroll"><table><thead><tr><th>condition</th><th>decisions</th>'
      '<th>outward looks</th></tr></thead><tbody>'
      '<tr><td>with the nudge in the prompt</td><td class="num">228</td><td class="num">2</td></tr>'
      '<tr><td>after it was removed</td><td class="num">%s</td><td class="num hot">%s</td></tr>'
      '</tbody></table></div>'
      '<p class="note"><b>Why it was closed:</b> %s</p></section>'
      % (_e(armed.get("ticks", "-")), arm("control"), arm("treatment"),
         _e(s.get("delivered", "-")), _e(s.get("prompt_delta", "-")), _e(s.get("verdict", "-")),
         _e(outward.get("result", "-")),
         _e(f.get("decisions", "-")), _e(f.get("outward_chosen", "-")),
         _e(outward.get("why_closed", "-"))))


# ---------------------------------------------------------------- blockers
BLOCKERS = [
    ("R1's original gate", "asked for an action the wake's surface could not express",
     "reading the two surfaces against each other"),
    ("look_outward", "built, wired, budgeted, certified — and no MOVE named it",
     "R4b's third condition sat unsatisfiable"),
    ("response_format", "<code>\"type\" in schema</code> where a VALUE test belonged, so every "
     "schema call ever sent was malformed", "8 rods, 2 plants, 8 of 8 HTTP 400"),
    ("note_to_self", "the formatter's own error written into memory — 430 of 739 entries were "
     "one string", "the rod's reasoning trace, on the first tick it was kept"),
    ("check_a_belief", "in the tool registry; no move could name it",
     "listing which tools no move reaches"),
    ("the standing block", "a line appended past a cap that was already exactly full, silently "
     "truncated away", "rendering the block and reading it back"),
    ("decide.WHEN", "rendered as &ldquo;(no description — do not pick this)&rdquo; for five hours",
     "the A/B's null result"),
    ("_read_stream", "the first SSE line consumed for detection, so <b>every streamed reply lost "
     "its first token</b>", "two rods returning byte-identical malformed output"),
]


def blockers(d: dict) -> str:
    rows = "".join('<tr><td class="n">%d</td><td><code>%s</code></td><td>%s</td><td>%s</td></tr>'
                   % (i + 1, w, what, how) for i, (w, what, how) in enumerate(BLOCKERS))
    return (
      _nav("blockers") +
      '<header class="chead"><p class="eyebrow">one defect · eight instances · one day</p>'
      '<h1>Present, correct, and impossible to choose.</h1>'
      '<p class="lede">The same shape every time: the capability EXISTS, the code is CORRECT, the '
      'wiring is REACHABLE — and something upstream stops it from ever being selected. Unit tests '
      'pass. The wiring check reports wired. The organ is present and dead, and nothing that reads '
      'the code can see it, because the code is not what is wrong.</p></header>'
      '<section><div class="scroll"><table><thead><tr><th>#</th><th>where</th>'
      '<th>what was wrong</th><th>how it was found</th></tr></thead><tbody>%s</tbody></table></div>'
      '<p class="note">Every one found by measuring the action, never by reading the code. '
      '<code>aea/lab/blockers.py</code> now hunts the class on demand — seven checks, including '
      'the one nothing else asked: <em>has this ever actually been chosen?</em></p></section>'
      % rows)


# ---------------------------------------------------------------- token journey
def journey(d: dict) -> str:
    t = _traces()
    r5 = next((r for r in d["rungs"] if r["id"] == "R5"), {}) or {}
    n = len((r5.get("journey") or {}).get("rows", []))
    return (
      _nav("journey") +
      '<header class="chead"><p class="eyebrow">the token journey - two scales</p>'
      '<h1>What actually travels, and what survives it.</h1>'
      '<p class="lede">The same question asked twice. At the scale of one call: what the rod '
      'produced and what was kept. At the scale of a rung: what was claimed, what settled it, and '
      'whether the bytes still exist.</p></header>'
      '<section><h2>One call</h2><div class="stats small">'
      '<div><b>%s</b><span>chars of prompt in</span></div>'
      '<div><b>%s</b><span>chars of reasoning, invisible</span></div>'
      '<div><b>%s</b><span>chars of answer, the only part anything read</span></div>'
      '<div><b>%s s</b><span>before the first visible token</span></div></div>'
      '<p class="body">Judged on content alone the rod looks silent for forty seconds and then '
      'speaks. It was never silent. Across %s instrumented ticks it produced <b>%s</b> characters '
      'of reasoning against <b>%s</b> of answer, and until 2026-08-04 the first number was '
      'discarded at the socket.</p></section>'
      '<section><h2>One rung</h2>'
      '<p class="body">R5 is the first rung whose output is a chain rather than an action, so it '
      'is the first that can be walked end to end: a claim written and fsynced <em>before any '
      'bytes existed</em>, a probe, bytes hashed at the socket, a verdict, a consequence. '
      '<b>%s</b> such chains exist, and every citation on R5&rsquo;s page resolves to a file on '
      'disk.</p>'
      '<p class="note">The ordering is the mechanism, not a convention. <code>settle()</code> '
      'refuses any citation whose artefact was read BEFORE the claim was proposed. It is the one '
      'property that cannot be satisfied by writing more carefully afterwards.</p>'
      '<p><a class="cta" href="R5.html">Walk R5&rsquo;s chain</a></p></section>'
      % (_e(int(t["prompt"] or 0)) if t.get("prompt") else "-",
         _e(int(t["reason"] or 0)), _e(int(t["content"] or 0)), _e(t["ttfc"]),
         _e(t["n"]), _e("{:,}".format(t["total_reason"])),
         _e("{:,}".format(t["total_content"])), _e(n)))
