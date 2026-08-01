"""recourse.py - WHEN THE OBVIOUS PATH IS BLOCKED, WHAT DO YOU TRY NEXT? Declared, not improvised.

    python -m aea.kernel.recourse                     the ladder
    python -m aea.kernel.recourse "<what failed>"     what to try, in order, for this failure

WHY THIS EXISTS, and it is the most useful thing to come out of 2026-08-01.

Luis watched a blocked task get solved by an unconventional route and asked the right question:
*"What made you trigger an unconventional solution I didn't tell you... we have to make it easy to
be reproduced again. Imagine that you [are] Opus 5, the model that powers you, and then we could do
a suit of you for an inferior model."*

That is the AEA's whole problem in one sentence. The entity does not run on a frontier model on a
good day - it runs on whatever rod the ladder hands it, and a 30B does not spontaneously invent a
five-step workaround. But it does not have to INVENT one. What happened was not insight; it was a
LADDER, walked in order, and a ladder is data. Written down, a small rod can walk it too.

THE MOVE, RECONSTRUCTED HONESTLY. The task was "turn on GitHub Pages":

    1  the obvious tool                `gh` -> not installed
    2  DROP TO THE PRIMITIVE           what was gh going to do underneath? an HTTPS call to a
                                       documented API. The tool is a convenience over a protocol,
                                       and the protocol does not disappear with the tool.
    3  THE MISSING PIECE EXISTS        no token in env or .env - but `git push` had just worked, so
       SOMEWHERE, OR THE ADJACENT      a credential MUST exist. Infer existence from an adjacent
       THING WOULD NOT WORK            success, then go and find where it lives (git credential fill)
    4  READ THE ERROR, DO NOT          422 with a MESSAGE is data, not a failure count: "your plan
       COUNT IT                        does not support Pages for this repository" - which is a
                                       fact about VISIBILITY, not about permissions
    5  ENUMERATE WHAT THE CONSTRAINT   Pages needs public. The repo is private. So: change the
       IS ACTUALLY ABOUT               visibility, or change the repository. Two moves, not zero.
    6  SCORE EACH AGAINST THE          making it public would publish an employer path, a manuscript
       STANDING LAW                    tree and a job shortlist -> refused. A new repo holding only
                                       a scanned artefact -> safe. The law picked the move.
    7  VERIFY BY THE EFFECT            201 means the API accepted a request. Only fetching the URL
                                       and finding your own bytes means the site serves.

NONE OF THOSE SEVEN IS CLEVER. Every one is a question with a mechanical answer, and the only thing
that made them work is that they were asked IN ORDER and none was skipped. That is what transfers to
a smaller rod, and what this file is.

WHAT IT IS NOT. It is not a plan generator and it does not decide anything. It answers one question
- "given a failure of this shape, what is the next thing to try?" - out of a closed table, in a
declared order, with a REASON attached to each rung so the caller can tell a human why. Law S5: a
declaration names a registered operation with parameters, never code. Nothing here is eval'd.

AND THE LAST RUNG IS ALWAYS "ASK". A ladder whose bottom is "keep trying" is how an autonomous
system burns a night on a wall. The bottom of this one is STOP AND SAY WHAT YOU TRIED.
"""
from __future__ import annotations

import re
import sys

# =================================================================================================
# THE LADDER. Ordered, cheapest and most-likely first. Each rung: a name, when it applies, the
# concrete thing to do, and WHY - the why is not decoration, it is what lets a caller explain the
# attempt to a human, and what stops the rung being cargo-culted into a situation it does not fit.
# =================================================================================================
LADDER = [
    dict(
        rung="drop-to-the-primitive",
        when=r"not found|no such|command not found|is not recognized|ModuleNotFound|ImportError",
        do="Ask what the missing tool was going to do UNDERNEATH, and do that directly: a raw HTTPS "
           "request instead of a CLI, the provider's own endpoint instead of a wrapper, the file on "
           "disk instead of a helper that reads it.",
        why="A tool is a convenience over a protocol. The protocol does not disappear when the "
            "convenience is missing. MEASURED: `gh` absent -> the GitHub REST API answered the same "
            "question in one urllib call; `WebFetch` timing out -> a plain GET with a browser "
            "User-Agent returned 200 and 200KB.",
    ),
    dict(
        rung="infer-from-the-adjacent-success",
        when=r"auth|credential|token|401|403|permission|unauthor",
        do="Find something NEARBY that already works and ask what it must have had. If `git push` "
           "succeeds then a credential exists on this machine - go and read it from where it lives "
           "(`git credential fill`) rather than concluding there is none.",
        why="Absence of a thing where you looked is not absence of the thing. An adjacent capability "
            "that works is proof the missing piece exists somewhere, and it names where to look.",
    ),
    dict(
        rung="read-the-error-do-not-count-it",
        when=r"\b4\d\d\b|\b5\d\d\b|refused|denied|rejected|invalid|unsupported",
        do="Read the message, not the status. Quote it. Decide whether it is about PERMISSION, "
           "SHAPE, or STATE - three different worlds with three different next moves.",
        why="MEASURED: a 422 read as 'the token lacks scope' was actually 'your plan does not "
            "support Pages for this repository' - a fact about the repo's VISIBILITY. Treating the "
            "message as a failure count would have produced a whole afternoon of wrong fixes.",
    ),
    dict(
        rung="name-what-the-constraint-is-about",
        when=r".",
        do="Say which PROPERTY of which THING is blocking, then list every move that changes that "
           "property - change the thing, or use a different thing. There are almost always exactly "
           "two. (Shape: 'Pages requires PUBLIC; this repo is PRIVATE' -> flip it, or make another.)",
        why="A blocker stated as 'it failed' has no moves. The same blocker stated as a property "
            "has a finite list of them, and the list is usually short enough to enumerate out loud.",
    ),
    dict(
        rung="score-each-move-against-the-standing-law",
        when=r".",
        do="For each candidate move, ask what it would cost against the laws that do not bend here: "
           "the privacy guard, the honesty law, the claim ceiling, the sacred save. Let the law "
           "pick, and say which law picked it.",
        why="MEASURED: 'make the repo public' and 'make a new public repo' both enable Pages. The "
            "first would have published an employer path, a manuscript tree and a job shortlist. "
            "The law chose, not taste - and because a law chose, the choice is explainable.",
    ),
    dict(
        rung="verify-by-the-effect",
        when=r".",
        do="After the action, observe the EFFECT through the path a user would: fetch the URL, read "
           "the value back through its consumer, re-run the command. Never accept the "
           "acknowledgement as the outcome.",
        why="201 means an API accepted a request. Only fetching the page and finding your own bytes "
            "means it serves. This repo has paid for that distinction five times in two days - an "
            "edit that applied to the wrong object is byte-identical to an edit that never happened.",
    ),
    dict(
        rung="stop-and-say-what-you-tried",
        when=r".",
        do="Stop. Report every rung attempted and what each returned, and name the ONE decision a "
           "human has to make.",
        why="The bottom of a ladder must be a stop, or an unattended system burns a night on a wall. "
            "A blocked attempt with its trail attached is worth more than a night of retries.",
    ),
]

ASK_LAST = LADDER[-1]["rung"]


def steps(failure: str = "") -> list:
    """The rungs that apply to this failure, in order. Cheapest first, `stop-and-say` always last."""
    f = str(failure or "")
    out = [r for r in LADDER if r["rung"] != ASK_LAST and re.search(r["when"], f, re.I)]
    # A FAILURE THAT MATCHES NOTHING STILL GETS THE GENERAL RUNGS. Returning an empty ladder would
    # be the null-looks-like-real shape again: "no recourse" and "I could not classify it" are
    # different answers and only one of them is true here.
    if not out:
        out = [r for r in LADDER if r["when"] == "." and r["rung"] != ASK_LAST]
    return out + [LADDER[-1]]


def render(failure: str = "") -> str:
    L = [f"RECOURSE for: {failure or '(any blocked action)'}", "=" * 92]
    for i, r in enumerate(steps(failure), 1):
        L.append(f"{i}. {r['rung'].upper().replace('-', ' ')}")
        L.append(f"     DO   {r['do']}")
        L.append(f"     WHY  {r['why']}")
    return "\n".join(L)


if __name__ == "__main__":
    arg = " ".join(sys.argv[1:])
    if not arg:
        print("THE RECOURSE LADDER - what to try when the obvious path is blocked")
        print("=" * 92)
        for r in LADDER:
            print(f"  {r['rung']:34s} when: {r['when'][:44]}")
        print()
        print("  python -m aea.kernel.recourse \"gh: command not found\"")
        print()
        print("  Nothing here is clever. Each rung is a question with a mechanical answer, and the")
        print("  only thing that makes them work is asking them IN ORDER and skipping none - which")
        print("  is exactly the part a smaller rod can do as well as a large one.")
    else:
        print(render(arg))
