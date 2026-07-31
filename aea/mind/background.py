"""background.py - THE PART OF THE MIND THAT KEEPS WORKING WHILE THE MOUTH IS BUSY.

Luis, 2026-07-29: "When I'm talking, I need to think, but I'm dedicating brainpower to how things
are going to be said... We'll need to put one of the parts of the brain to speak, and then in the
background another model receiving information relevant to the conversation. Like when you think
'oh, I realize that' - that will be that other part of the brain."

THE NEUROSCIENCE IS ON HIS SIDE, and it is worth stating because it is why this is not decoration.
Speech production measurably consumes attentional resources: in dual-task studies, production
latencies rise with concurrent load, so a person really does think more slowly while speaking. And
the Default Mode Network is active DURING speech production, not only at rest, with its activation
strength and delay scaling with task complexity. There is a real second system running while the
speaking system is occupied, and its output arrives as an interruption: "oh, wait -".

THE MEASUREMENT THAT MAKES IT FREE. Duet, 2026-07-29: speech duration per turn was
6.05 / 27.22 / 6.29 / 30.58 / 13.08 / 29.81 seconds, median ~13s. Time to first token on a rod is
~0.5s. So while the voice is playing, this machine has been doing NOTHING for a median of thirteen
seconds a turn, with room for a dozen calls. The person hears no delay, because they are listening
to the answer that is already playing.

WHAT IT DOES WITH THAT TIME, and the choice is deliberate. It is a CRITIC of what was just said,
not a generator of extra content. x20 measured a critic as a real assemblable part; and a second
rod inventing additional things to say would be a machine that talks more, which is the opposite of
what this session has spent all night fixing. So it looks for exactly three things:

    a claim the speaker asserted with NO tool behind it and no way to know it
    a CONTRADICTION against a fact already stored about this person
    a question the person asked that the answer did not actually address

THE HONESTY LINE, and it decides whether a finding may ever be spoken. A realization is only real
if the background DERIVED something the foreground did not have. So a finding must name the exact
words it contradicts or corrects, and anything the speaker already said is dropped as a duplicate.
Otherwise the entity performs having-an-insight, which is a claim about interiority the ceiling
forbids - the same rule that governs the thinking sounds.
"""
from __future__ import annotations

import json
import re
import threading
import time

from aea.kernel import grid
from aea.mind import tiers

# The background may take as long as the speech it hides behind, and not one second longer: it is
# free ONLY while the mouth is busy. Past that it would delay the next turn, which is the exact
# cost this design exists to avoid paying.
MAX_SECONDS = 12

SCHEMA = {
    "type": "object",
    "properties": {
        "found": {"type": "boolean"},
        "kind": {"type": "string", "enum": ["unsupported_claim", "contradiction", "unanswered"]},
        "quote": {"type": "string"},
        "realization": {"type": "string"},
    },
    "required": ["found"],
}

PROMPT = """You are the BACKGROUND part of a mind. Another part just SAID something out loud in a
conversation, and it is still speaking. Your job is not to add more to say. Your job is to notice a
problem with what was just said, the way a person notices "oh wait, I said that wrong".

Look for EXACTLY one of these, in priority order:
1. unsupported_claim - it stated a specific fact (a number, a name, a date, a capability) that it
   could not know and that no tool result supports.
2. contradiction - it said something that conflicts with a KNOWN FACT listed below.
3. unanswered - the person asked something specific and the reply did not address it.

Rules:
- If none of these is clearly true, answer found=false. Most turns are fine. Saying nothing is the
  correct and common answer.
- `quote` must be the EXACT words from the reply that are the problem. If you cannot quote it, it
  is not real - answer found=false.
- `realization` is ONE short spoken sentence, in first person, as a correction the speaker would
  say next: for example "Actually, I should not have given you that number - I did not check it."
- Never invent a replacement fact. Correcting an unverified number with another unverified number
  is the same mistake twice.

KNOWN FACTS ABOUT THE PERSON:
{facts}

TOOL RESULTS AVAILABLE TO THE SPEAKER THIS TURN:
{tools}

THE PERSON SAID:
{said}

THE SPEAKER REPLIED:
{reply}
"""


def _clean(t: str) -> str:
    t = re.sub(r"<think>.*?</think>", " ", t or "", flags=re.S | re.I)
    return re.sub(r"\s+", " ", t).strip()


def review(said: str, reply: str, facts: list, tool_calls: list,
           timeout: int = MAX_SECONDS) -> dict:
    """One background pass over the turn just spoken. Returns {} when there is nothing to say.

    Runs on the DEPTH organ, because this is the one job where being slow costs nothing: it is
    hidden entirely behind speech that is already playing, and it is the job where being right
    matters most - a false realization spoken aloud is worse than silence."""
    # DEPTH, MEASURED BOTH WAYS 2026-07-29, and the result is a capability finding rather than a
    # tuning one:
    #     depth (550b)  caught the unsupported claim in 1.9s with an exact quote;
    #                   hit the 12s window on the other two - VARIABLE, not uniformly slow
    #     voice (49b)   answered in 2.5-2.9s and found NOTHING on any of the three
    # So this is law M10: the smaller rod is not a cheaper version of the bigger one on this task,
    # it is unable to do it. Fitness is per task SHAPE. Judging whether a claim is unsupported,
    # quoting the exact words, and writing a correction that invents nothing is a genuinely hard
    # combined judgement, and the 49b returns "nothing found" rather than doing it.
    #
    # Partial coverage is the honest answer and it is also the human one: a person does not have a
    # realization on every turn either. A review that misses its window is simply dropped, and
    # BOTH rods keep the same property that matters most - zero false positives on clean turns,
    # measured 3 of 3. Second-guessing itself out loud for no reason is the expensive error here.
    o = tiers.organ("depth")
    tools = "\n".join("- %s -> %s" % (c.get("tool"), str(c.get("out"))[:160])
                      for c in (tool_calls or [])) or "- (none: the speaker used no tool)"
    prompt = PROMPT.format(facts="\n".join("- %s" % f for f in (facts or [])[:12]) or "- (none)",
                           tools=tools, said=said, reply=reply)
    r = grid.call_openai(o["plant"], o["model"], [{"role": "user", "content": prompt}],
                         max_tokens=220, temperature=0.1, timeout=timeout)
    if not r.get("ok"):
        return {}
    txt = _clean(r.get("text") or "")
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return {}
    try:
        d = json.loads(m.group(0))
    except Exception:
        return {}
    if not d.get("found"):
        return {}
    quote = (d.get("quote") or "").strip().strip('"')
    real = (d.get("realization") or "").strip()
    # THE GROUNDING CHECK, and it is what separates a realization from a performance. The quoted
    # words must ACTUALLY APPEAR in what was said - a background that can cite anything can invent
    # anything, and law B2 says test the property, never a proxy for it.
    if not quote or not real:
        return {}
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
    if norm(quote)[:40] not in norm(reply):
        return {}
    # and it must not merely repeat something already spoken
    if norm(real)[:40] in norm(reply):
        return {}
    return dict(kind=d.get("kind", "?"), quote=quote, realization=real,
                seconds=round(r.get("latency") or 0, 2))


class Thinker:
    """Runs `review` in a thread so the caller can speak while it works, then collect the result.

    Deliberately NOT a queue of pending work: one turn, one review, collected at the next turn
    boundary. A backlog would mean surfacing a realization about a turn three exchanges ago, which
    is not how the phenomenon works and would be confusing rather than human."""

    def __init__(self):
        self._t = None
        self._out: dict = {}
        self._started = 0.0

    def start(self, said: str, reply: str, facts: list, tool_calls: list) -> None:
        if self._t and self._t.is_alive():
            return                      # still working on the previous turn; do not stack
        self._out = {}
        self._started = time.time()

        def run():
            try:
                self._out = review(said, reply, facts, tool_calls)
            except Exception:
                self._out = {}
        self._t = threading.Thread(target=run, daemon=True)
        self._t.start()

    def collect(self, wait: float = 0.0) -> dict:
        """Take whatever the background finished. Waits at most `wait` seconds - normally ZERO,
        because the whole point is that it ran during speech that has already finished playing.
        An unfinished review is simply dropped: making the person wait for it would spend the very
        time this was built to reclaim."""
        if self._t and self._t.is_alive() and wait > 0:
            self._t.join(timeout=wait)
        if self._t and self._t.is_alive():
            return {}
        out, self._out = self._out, {}
        return out

    def busy(self) -> bool:
        return bool(self._t and self._t.is_alive())
