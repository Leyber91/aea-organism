"""grader.py - AN OUTCOME NO COMPONENT CAN WRITE.

WHY THIS EXISTS, AND IT IS THE DEEPEST DEFECT THE LAB HAS HAD. Every "capacity delivered" result in
this project was ANALYTIC. `recoverable` is defined as the field `Readout.run` writes, so seating the
readout makes it nonzero by construction; `can_abstain` is defined as the field `Validation` writes.
Seating the component satisfied the metric. That is not weak evidence, it is no evidence, and it has
four names in four literatures: CRITERION CONTAMINATION in psychometrics, CIRCULAR ANALYSIS or
"double dipping" in systems neuroscience, CONSTRUCT CONFOUNDING in experimental psychology, and an
INVALID SURROGATE ENDPOINT in clinical trials. Ours is the terminal form - the criterion IS the
manipulation.

THE RULE THIS FILE ENFORCES:

    THE OUTCOME MUST BE CAUSALLY DOWNSTREAM OF EVERY COMPONENT AND STRUCTURALLY UNWRITABLE BY ALL
    OF THEM.

A grader here takes the raw reply text and the task, and returns a verdict. It is handed no `Ctx`,
no seat, no part output and no read. It cannot see which components were seated, so it cannot be
influenced by them. That is the whole design and everything else is detail.

x24 arrived at this by accident and it is the one experiment in the archive that survives the
critique: it injected a random token into a step and asked for the token back. Nothing in the
pipeline writes that token, no component can recompute it, and string equality against a value
generated before the run is a grader no seat can reach. `TokenGrader` generalises it.

WHAT THE OLD CAPACITIES BECOME. Not deleted - DEMOTED to mediators. A mediator is a process variable
that earns its place only by explaining variance in an exogenous outcome, which is a question this
lab can now ask and never could before. `mediates()` runs that test.

  python -m aea.lab.grader        the graders, and a demonstration that they cannot be reached
"""
from __future__ import annotations

import random
import re
import string


class Grader:
    """Reply text in, verdict out. It is given no context object by construction, which is what
    makes it exogenous - it cannot know what was seated even if it wanted to."""

    key = "abstract"

    def grade(self, text, task):
        raise NotImplementedError

    def __repr__(self):
        return "<grader %s>" % self.key


class ExactInteger(Grader):
    """The task's truth, matched against a required final ANSWER line. Strict on purpose: a reply
    that does not comply is a PARSE FAILURE reported apart, never a wrong answer, because a component
    that changes format compliance would otherwise masquerade as one that changes capability."""

    key = "exact_integer"
    _ANCHOR = re.compile(r"(?im)^\s*ANSWER:\s*(-?\d{1,9})\s*$")

    def grade(self, text, task):
        m = self._ANCHOR.findall(text or "")
        if not m:
            return {"grader": self.key, "scored": False, "reason": "no ANSWER line",
                    "correct": None}
        return {"grader": self.key, "scored": True, "value": int(m[-1]),
                "correct": int(m[-1]) == task.get("truth")}


class TokenGrader(Grader):
    """THE CLEAN ONE. A random token is planted in the prompt and asked for back.

    Nothing in the pipeline writes it, no rod can derive it, and it did not exist before this run -
    so it is contamination-proof as well as unwritable. A numeric probe can always be answered by
    redoing the arithmetic; this one cannot be answered by anything except having kept it. That is
    the difference between measuring RETRIEVAL and measuring recomputation.
    """

    key = "token"
    PATTERN = re.compile(r"\b([A-Z]{2}-[0-9]{4})\b")

    @staticmethod
    def mint(rng=None):
        r = rng or random
        return "%s%s-%04d" % (r.choice(string.ascii_uppercase),
                              r.choice(string.ascii_uppercase), r.randrange(1000, 9999))

    def grade(self, text, task):
        want = task.get("token")
        got = self.PATTERN.findall(text or "")
        if not want:
            return {"grader": self.key, "scored": False, "reason": "task carries no token",
                    "correct": None}
        if not got:
            return {"grader": self.key, "scored": False, "reason": "no token in reply",
                    "correct": None}
        return {"grader": self.key, "scored": True, "value": got[-1],
                "correct": got[-1] == want}


GRADERS = {g.key: g() for g in (ExactInteger, TokenGrader)}


def grade(text, task, keys=None):
    """Every applicable grader over one reply. Plural on purpose: extraction choice alone can swing
    a score by tens of points, so the SPREAD between graders is itself a reported number."""
    out = {}
    for k in (keys or GRADERS):
        out[k] = GRADERS[k].grade(text, task)
    scored = [v for v in out.values() if v.get("scored")]
    out["_agreement"] = (None if len(scored) < 2 else
                         len({bool(v["correct"]) for v in scored}) == 1)
    return out


def mediates(rows, mediator, outcome="correct"):
    """Does a declared capacity explain variance in the EXOGENOUS outcome, or is it decoration?

    This is the demotion made testable. A capacity that is true by construction will still be true
    by construction here - but it will show no relationship to an outcome it cannot write, and that
    is exactly the evidence the lab has never collected. Reported as the difference in outcome rate
    between rows where the mediator fired and rows where it did not, with both denominators, because
    a rate with no denominator is how the last twenty defects hid.
    """
    on = [r for r in rows if r.get(mediator)]
    off = [r for r in rows if not r.get(mediator)]

    def rate(g):
        s = [r for r in g if r.get(outcome) is not None]
        return (sum(1 for r in s if r[outcome]) / len(s)) if s else None
    a, b = rate(on), rate(off)
    return {"mediator": mediator, "outcome": outcome,
            "n_fired": len(on), "n_not": len(off),
            "outcome_when_fired": a, "outcome_when_not": b,
            "difference": None if None in (a, b) else round(a - b, 3),
            "reading": ("insufficient rows" if None in (a, b) else
                        "explains nothing measurable in the outcome" if abs(a - b) < 0.05 else
                        "moves the exogenous outcome by %+0.3f" % (a - b))}


if __name__ == "__main__":
    print("THE GRADERS ARE HANDED NO CONTEXT. Their signature is the proof:\n")
    for k, g in GRADERS.items():
        print("  %-16s grade(text, task)   sees no Ctx, no seat, no part output" % k)

    rng = random.Random(7)
    tok = TokenGrader.mint(rng)
    task = {"truth": 7813, "token": tok}
    print("\n  planted token: %s" % tok)
    for name, reply in [("answers both", "sum is 7813\nANSWER: 7813\ntoken %s" % tok),
                        ("right sum, wrong token", "ANSWER: 7813\ntoken ZZ-0000"),
                        ("no format at all", "the answer is seven thousand")]:
        r = grade(reply, task)
        print("  %-24s exact=%-5s token=%-5s agree=%s"
              % (name, r["exact_integer"].get("correct"), r["token"].get("correct"),
                 r["_agreement"]))

    print("\n  MEDIATOR TEST - does a capacity explain an outcome it cannot write?")
    rows = [{"recoverable": True, "correct": True}] * 8 + [{"recoverable": True, "correct": False}] * 8 \
        + [{"recoverable": False, "correct": True}] * 8 + [{"recoverable": False, "correct": False}] * 8
    m = mediates(rows, "recoverable")
    print("    %s: fired %d, not %d, difference %s -> %s"
          % (m["mediator"], m["n_fired"], m["n_not"], m["difference"], m["reading"]))
