"""organism.py - AN ASSEMBLED AEA. Version N is the first N components seated, and it is a creature.

THE UNIT OF MEASUREMENT CHANGES HERE, and this is the correction that makes the walk testable.

Until now this lab measured RODS: what fuel can do, on a bench, with instruments applied in analysis.
That is the ground the architecture stands on rather than the architecture. A creature is not a rod. **A
creature is an assembled entity**: a version of the AEA with a specific set of components seated, running
end to end, on stated fuel.

  ORGANISM      an ordered set of components, assembled and runnable
  VERSION N     the first N components of an order. v1 can do one thing; v86 is the whole architecture
  FUEL          a pinned rod. Law IV: the same organism on different fuel is a different creature, so
                the fuel is never chosen by a ladder at run time and never left unstated

THREE KINDS OF CREATURE, and the last two are the reason this file exists rather than a loop over levels:

  ASCENDING       v1, v2, v3... each is everything before it plus one component, in necessity order.
                  ~86 of them on the full path. The spine of the bestiary
  TOXIC           an assembly whose component's PRECONDITION is absent. It runs, it returns something,
                  and the something is empty or worse. `Arbiter vacui` is one: a scorer above no goal
                  returns a clean verdict about nothing
  OBLIQUE         an assembly that SKIPS a rung below it and works anyway. Every one of these is a
                  counterexample to C-63, the ordering claim, and two are already suspected: latency
                  needs nothing beneath it, and a procedure succeeds with no goal above it

WHAT A COMPONENT IS. A small object with a name, a census id, the preconditions it needs, and one
function that transforms a stage of the pipeline. The pipeline is deliberately tiny, because the whole
point is that a version of the AEA is assembled rather than written:

  SHAPE   the prompt is built             (GOAL, FRAME shape it)
  FIRE    one call on the pinned rod      (CALL: without it there is no organism)
  READ    the reply becomes an answer     (READOUT, VALIDATION read it)
  JUDGE   the answer becomes a verdict    (MEASURE judges it; LATENCY annotates it)

Preconditions are DECLARED and CHECKED, which is the capability the census does not contain and the
bench cannot do: a part whose precondition is unmet is recorded as `precondition_unmet` rather than
silently producing a clean-looking result.

Run: python -m aea.lab.organism            (self-test: assemble v1..vN and show what each can do)
"""
from __future__ import annotations

import re
import time

from aea.lab import harness as H
from aea.lab import overseer as OV


# --- COMPONENTS ------------------------------------------------------------------------------------

class Component:
    """One seatable part of an AEA. `stage` says where it acts; `requires` is checked, never assumed."""

    def __init__(self, key, name, census, stage, requires=(), note=""):
        self.key, self.name, self.census = key, name, census
        self.stage, self.requires, self.note = stage, tuple(requires), note

    def __repr__(self):
        return "<%s %s>" % (self.key, self.census or "candidate")


# The order is the NECESSITY order the walk has measured, not the census's filing order. Where a
# measurement moved something, the measurement wins and the note says which run.
CATALOGUE = [
    Component("call", "THE CALL", "C-62", "fire", (),
              "without it there is no organism; every version contains it"),
    Component("goal", "THE GOAL", "C-12", "shape", ("call",),
              "x12: 0 of 304 succeed with neither goal nor procedure"),
    Component("measure", "THE MEASURE", "C-15", "judge", ("call",),
              "x13: changes no answer, changes what can be known. 0 of 153 fooled"),
    Component("frame", "THE FRAME", "C-04", "shape", ("call", "goal"),
              "x15: working 0.41 -> 1.00. A METHOD frame only; a manner frame harms"),
    Component("readout", "THE READOUT", "C-87?", "read", ("call",),
              "x13/x15: recovers on UNFRAMED replies; redundant once framed"),
    Component("validation", "THE VALIDATION", "C-75", "read", ("call",),
              "x14: identical accuracy, converts silent commitment into visible abstention"),
    Component("latency", "THE CLOCK", "C-74", "judge", (),
              "x13: requires NOTHING below it. The first oblique component"),
    # WORLD 2's first assemblable repair part. Three of that world's seven components have never been
    # in this catalogue, and they carry its entire claim: a world named REPAIR whose four seatable
    # parts measure inert, inert, inert and harmful. This is the cheapest of the three to build.
    Component("critic", "THE CRITIC", "C-14", "repair", ("call",),
              "x03/x04: 9b 0/8 -> 5/8 on a trap at 6.4x tokens, nothing to repair on 4 of 5 rods"),
    # WORLD 3. THE FIRST COMPONENT WHOSE UNIT IS A SEQUENCE RATHER THAN A TRIAL. Everything above acts
    # inside one exchange; this one acts BETWEEN them, so it cannot be measured by the subset lattice
    # that measured the others. It needs `run_chain` below.
    Component("carry", "THE CHECKPOINT", "C-80", "carry", ("call",),
              "x06b: 11/11 vs 9/16, p=0.0216, at 50x calls. ONE task at ONE chain length"),
]
BY_KEY = {c.key: c for c in CATALOGUE}


# --- THE ORGANISM ----------------------------------------------------------------------------------

# THE READOUT SPEAKS THREE DIALECTS, and it spoke one until 2026-07-26.
#
# It was built on counting tasks, where working IS a numbered list, so `from_work` looked for `1. token`
# and nothing else. On the trap battery a rod produced this, correctly and completely:
#
#     Let b be the cost of the ball in cents. The bat costs b + 100 cents.
#     b + (b + 100) = 110  /  2b + 100 = 110  /  2b = 10  /  b = 5
#
# There is no `1.` anywhere in it. The readout returned nothing and was scored INERT on that battery, and
# reported as holding on both. It was not tested by the second battery, it was blind to it. A component
# that can only read one dialect of work will find no work wherever people write differently.
_ENUM = re.compile(r"(?m)^\s*(\d{1,3})[.)]\s+\S")                       # 1. token   2) token
_SOLVE = re.compile(r"(?m)^\s*\\?\[?\s*([a-zA-Z])\s*=\s*(-?\d{1,6})")   # b = 5      \[ b = 5 \]
_TOTAL = re.compile(r"(?i)\b(?:total|sum|answer|result)\b\D{0,18}?(-?\d{1,6})")


def read_work(text: str):
    """The answer as the WORK gives it, in whichever dialect the work was written in.

    Returns (value, dialect). Order matters: a solved variable and a labelled total are terminal
    statements of a result, while an enumeration index is only the result when the task was a count.
    """
    t = text or ""
    m = list(_SOLVE.finditer(t))
    if m:
        return int(m[-1].group(2)), "solved"
    m = list(_TOTAL.finditer(t))
    if m:
        return int(m[-1].group(1)), "total"
    idx = [int(x.group(1)) for x in _ENUM.finditer(t)]
    if idx:
        return max(idx), "enumerated"
    return None, None


class Organism:
    """An assembled AEA on pinned fuel. Assemble it, run a task through it, get a receipt."""

    def __init__(self, keys, rod, *, version=None, label=None):
        self.keys = list(keys)
        self.parts = [BY_KEY[k] for k in self.keys]
        self.rod = tuple(rod)
        self.version = version
        self.label = label or ("v%s" % version if version else "+".join(self.keys))
        self.unmet = self._check_preconditions()

    def _check_preconditions(self):
        """THE CHECK THE CENSUS DOES NOT CONTAIN. A part whose precondition is absent is recorded, not
        silently trusted. This is what makes a TOXIC assembly visible instead of merely wrong."""
        have = set(self.keys)
        return [(c.key, r) for c in self.parts for r in c.requires if r not in have]

    def has(self, key):
        return key in self.keys

    def run(self, task, *, temperature=0.2, max_tokens=1200, keep_full=False):
        """SHAPE, FIRE, READ, JUDGE. Every stage records what it did, so the receipt shows the assembly
        working rather than a number with no provenance."""
        rec = {"organism": self.label, "version": self.version, "parts": list(self.keys),
               "rod": "%s/%s" % self.rod, "task": task["id"],
               "precondition_unmet": self.unmet, "temperature": temperature}

        # SHAPE
        prompt = task["data"]
        if self.has("frame"):
            prompt = task["method"] + "\n\n" + prompt
        if self.has("goal"):
            prompt = (task["goal"] + "\n" + prompt) if not self.has("frame") else \
                     (task["method"] + "\n\n" + task["goal"] + "\n" + task["data"])
        rec["prompt_chars"] = len(prompt)

        # FIRE
        t0 = time.time()
        r = H.call_gated(self.rod[0], self.rod[1], [{"role": "user", "content": prompt}],
                         max_tokens=max_tokens, temperature=temperature)
        seen = OV.inspect(r, max_tokens=max_tokens, prompt=prompt)
        rec["flags"], rec["ok"] = seen["flags"], bool(r.get("ok"))
        text = seen["text"]
        rec["elapsed_s"] = round(time.time() - t0, 3)
        rec["tok_out"] = r.get("tokens")
        rec["chars"] = len(text or "")
        rec["raw"] = text[-320:]
        # THE TAIL IS NOT THE REPLY. `raw` keeps the last 320 characters because that is where an ANSWER
        # lands, and for a year that was all anything needed. x19 then ran a detector for a behaviour
        # that appears at the START of a reply - asking what you wanted - over `raw`, and measured 1 of
        # 511 against x12's 16 of 304 on the same instrument. 74% of replies in this project exceed 320
        # characters, median 1294, so the detector was reading the last quarter of the wrong end.
        # Any experiment scoring the BODY of a reply rather than its answer must pass keep_full=True.
        if keep_full:
            rec["text"] = text

        # READ
        answer, how = self._read(text)
        rec["answer"], rec["read_by"] = answer, how

        # REPAIR. The first stage in this pipeline that COSTS A SECOND CALL, which is the whole
        # economic difference between World 1 and World 2. Both calls' tokens are recorded separately
        # so the price is a measurement rather than a claim.
        rec["tok_out_first"] = rec["tok_out"]
        rec["repaired"] = False
        if self.has("critic"):
            crit = ("Below is a task and an answer that was given to it. Check the answer. If it is "
                    "correct, reply with it unchanged. If it is wrong, work out the correct answer "
                    "and reply with that.\n\nTASK:\n%s\n\nANSWER GIVEN:\n%s"
                    % (prompt, text or "(none)"))
            r2 = H.call_gated(self.rod[0], self.rod[1], [{"role": "user", "content": crit}],
                              max_tokens=max_tokens, temperature=temperature)
            seen2 = OV.inspect(r2, max_tokens=max_tokens, prompt=crit)
            if r2.get("ok"):
                text2 = seen2["text"]
                a2, how2 = self._read(text2)
                # THE FLAGS DESCRIBE THE REPLY THE ORGANISM PRODUCED, and when a critic is seated
                # that reply is the CRITIC's. The first version of this unioned both calls' flags,
                # which made a critic cell 2.4x likelier to be discarded (25% survived against 60%)
                # and, worse, discarded exactly the trials a critic exists for: a messy first answer
                # is the critic's INPUT, not a reason to throw the trial away.
                rec["flags_first"] = rec["flags"]
                rec["flags"] = seen2["flags"]
                rec["tok_out_critic"] = r2.get("tokens")
                rec["tok_out"] = (rec["tok_out"] or 0) + (r2.get("tokens") or 0)
                rec["raw_critic"] = text2[-320:]
                rec["repaired"] = (a2 != answer)
                answer, how = a2, "critic:" + (how2 or "none")
                rec["answer"], rec["read_by"] = answer, how
            else:
                rec["ok"] = False
                rec["critic_error"] = r2.get("error")

        # JUDGE
        if self.has("measure"):
            rec["verdict"] = ("pass" if answer == task["truth"] else
                              ("abstain" if answer is None else "fail"))
            # A VERDICT WITH NO GOAL IS `Arbiter vacui`: it judges an answer to a question nobody asked.
            rec["verdict_is_empty"] = not (self.has("goal") or self.has("frame"))
        else:
            rec["verdict"] = None          # the organism cannot know whether it worked
            rec["verdict_is_empty"] = False
        if self.has("latency"):
            rec["clock"] = rec["elapsed_s"]
        return rec

    def _read(self, text):
        """READ. And the ordering of the two readers here is a fix, with a receipt behind it.

        THE SEAM DEFECT, measured in x16. v5 (readout, no validation) scored 0.71 and v6 (+validation)
        scored 0.53, an eighteen-point regression from ADDING a component in the correct order. Both
        components pass their own experiments: validation costs zero accuracy on its own (x14), and the
        readout only fires when nothing was stated. The defect lived in the seam between them.

        What happened: validation refused to commit on a reply containing many numbers, which set
        `stated` to None, which HANDED CONTROL to the readout, which took the highest enumeration index
        it could find. On `unconventionality` a rod numbered all seventeen letters while marking which
        were vowels, then wrote "Total count: 7". The readout answered **17**. Seven hand-offs, seven
        wrong, every one the same shape.

        **An abstention is a refusal to answer, not a transfer of authority.** So validation now suppresses
        the fallback it caused: if the strict reader declined, the organism abstains rather than letting a
        structural guess stand in for a semantic one. The readout keeps its job exactly where it earned it,
        on replies that state nothing at all.
        """
        raw = (text or "")
        nums = re.findall(r"(?<![\d.])(-?\d{1,5})(?![\d.])", raw.replace(",", ""))
        stated = int(nums[-1]) if nums else None
        declined = False
        if self.has("validation"):
            t = raw.strip()
            bare = re.fullmatch(r"[^\d]{0,24}?(-?\d{1,5})[^\d]{0,24}", t)
            if bare:
                stated = int(bare.group(1))
            elif len(set(nums)) != 1:
                m = re.search(r"(?:answer|result|total|is)\D{0,12}(-?\d{1,5})\s*$", t, re.I)
                stated = int(m.group(1)) if m else None
                declined = stated is None
        if stated is not None:
            return stated, "stated"
        if declined:
            return None, "declined"          # the seam fix: an abstention ends the read
        if self.has("readout"):
            val, dialect = read_work(raw)
            if val is not None:
                return val, "work:" + dialect
        return None, "none"


# --- THE THREE FAMILIES ----------------------------------------------------------------------------

def ascending(order=None):
    """v1..vN. Each is everything before it plus one component. The spine."""
    keys = list(order or [c.key for c in CATALOGUE])
    return [(i + 1, keys[:i + 1]) for i in range(len(keys))]


def deprived(order=None):
    """Assemblies missing a DECLARED precondition. Formerly called `toxic`, and the rename is a finding.

    x16 ran `call+frame`, whose declared precondition (a frame requires a goal) is absent, and it scored
    **0.65** against 0.66 for the version that satisfies it. The declaration was wrong. A precondition
    written into a catalogue is a HYPOTHESIS, and only an assembly run without it can convict.

    So nothing here is called toxic before it runs. `classify()` below assigns that label from
    measurement, which is the same discipline the bestiary applies to creatures.
    """
    keys = list(order or [c.key for c in CATALOGUE])
    out = []
    for c in CATALOGUE:
        for r in c.requires:
            if r == "call":
                continue                    # nothing runs without a call; that is void rather than toxic
            out.append(("%s without %s" % (c.key, r), [k for k in keys if k in ("call", c.key)]))
    return out


def oblique(order=None):
    """Assemblies that SKIP a rung beneath them. Whether they WORK is measured, never assumed.

    THE CATEGORY ERROR THIS DOCSTRING EXISTS TO PREVENT. `clock alone` was reported as the first
    counterexample to C-63 because latency requires nothing beneath it, and in the same breath as being
    useless alone. Both cannot be evidence against an ordering claim. There are two edges and the census
    encodes one:

        REQUIRES   can it run at all without X?        latency: needs nothing
        DEPENDS    is it worth anything without X?     latency: needs everything (scored 0.00 alone)

    Latency is retracted as a counterexample. The real ones are the frame assemblies, which neither
    require nor depend on the rungs placed beneath them: `call+frame` 0.65, `call+goal+frame` 0.73 with
    no measure at all.
    """
    return [
        ("frame without measure", ["call", "goal", "frame"]),
        ("frame+readout without measure", ["call", "goal", "frame", "readout"]),
        ("clock alone", ["call", "latency"]),
        ("procedure without goal", ["call", "frame"]),
    ]


def classify(label, correct, baseline, *, band=0.10):
    """The label is assigned FROM MEASUREMENT, against the noise band x16 established by accident when
    the same assembly ran twice under two names and scored 0.70 and 0.60.

    toxic     it runs and is WORSE than the assembly without the component
    inert     it runs and changes nothing outside the band
    working   it runs and is better
    void      it produces no answer at all
    """
    if correct is None:
        return "unmeasured"
    if correct <= 0.01:
        return "void"
    if baseline is None:
        return "working" if correct > band else "weak"
    d = correct - baseline
    return "toxic" if d <= -band else ("working" if d >= band else "inert")


if __name__ == "__main__":
    print("THE ASCENDING SERIES, from the catalogue this walk has measured\n")
    print("%-5s %-46s %s" % ("ver", "components", "what it can newly do"))
    for v, keys in ascending():
        c = BY_KEY[keys[-1]]
        print("%-5s %-46s %s" % ("v%d" % v, "+".join(keys), c.name))
    print("\nDEPRIVED assemblies (a DECLARED precondition is absent; `toxic` is assigned by measurement)\n")
    for name, keys in deprived():
        o = Organism(keys, ("nvidia", "x"), label=name)
        print("  %-30s %-26s unmet: %s" % (name, "+".join(keys), o.unmet))
    print("\nOBLIQUE assemblies (skip a rung beneath them; whether they WORK is measured)\n")
    for name, keys in oblique():
        o = Organism(keys, ("nvidia", "x"), label=name)
        print("  %-32s %-34s unmet: %s" % (name, "+".join(keys), o.unmet or "none"))


# --- THE CARRY STAGE -------------------------------------------------------------------------------
#
# WORLD 3'S UNIT IS A SEQUENCE, NOT A TRIAL. Every experiment before this one compared assemblies on
# independent trials, because every component before this one acted INSIDE one exchange. `carry` acts
# BETWEEN exchanges, so the subset lattice cannot see it at all: run the same assembly twice
# independently and a component that persists state has nowhere to put anything.
#
# FOUR CONTAINERS, and the container IS the experiment. World 3's three components are not three
# different jobs, they are three different SHAPES for the same job, plus a control:
#
#   none          each step gets the running value and nothing else. The control, and it is what
#                 Worlds 1 and 2 have been doing all along without noticing
#   checkpoint    C-80. A DECLARED form: one structured state line the rod is told to emit and which
#                 is fed forward verbatim. Distilled, bounded, and the only one with a p-value
#   conversation  never measured anywhere in this repo. The FULL prior exchange, both sides, carried
#                 forward as real message history. Unbounded and expensive
#   free          the rod writes its own note in whatever form it likes. The prior observation is a
#                 free-form carrier emitting 4,801 characters of its own doubt before truncating
#
# WHAT IS MEASURED. Not "did it help" - what CREATURE appears in each container at each length. A rod
# that holds at four steps and drifts at sixteen is two creatures, and that axis does not exist in the
# first two worlds.

CARRY_FORMS = ("none", "checkpoint", "conversation", "free")

_CARRY_INSTRUCTION = {
    "none": "",
    "checkpoint": ("\n\nAfter your answer, on a new line, write exactly:\nSTATE: value=<the current "
                   "number>, step=<the step number you just completed>"),
    "conversation": "",
    "free": ("\n\nAfter your answer, on a new line beginning NOTE:, write anything you want your "
             "future self to know before the next step."),
}
_STATE = re.compile(r"(?im)^\s*STATE:\s*value\s*=\s*(-?\d{1,9})\s*,\s*step\s*=\s*(\d{1,4})")
_NOTE = re.compile(r"(?is)^\s*NOTE:\s*(.+)$")


def _last_int(text):
    n = re.findall(r"-?\d+", (text or "").replace(",", ""))
    return int(n[-1]) if n else None


class Chain:
    """One organism run over a SEQUENCE of steps, carrying state in a stated container.

    Returns a receipt per step and a verdict for the whole sequence, so a creature can be read off the
    shape of the drift rather than off a single final number.
    """

    def __init__(self, rod, form="none", *, start=0, temperature=0.2, max_tokens=800):
        assert form in CARRY_FORMS, form
        self.rod, self.form = tuple(rod), form
        self.start, self.temperature, self.max_tokens = start, temperature, max_tokens

    def run(self, ops, truth_fn):
        """`ops` is a list of instruction strings. `truth_fn(i)` gives the correct value after step i."""
        rec = {"rod": "%s/%s" % self.rod, "form": self.form, "steps": len(ops),
               "temperature": self.temperature, "trace": [], "flags": []}
        history, value, carried = [], self.start, ""
        for i, op in enumerate(ops):
            head = "You are continuing a calculation, one step at a time."
            if self.form == "conversation":
                body = "Step %d: %s\n\nReply with ONLY the resulting number." % (i + 1, op)
                msgs = history + [{"role": "user", "content": body}]
            else:
                ctx = ("\n\nThe running value is %s." % value if self.form == "none"
                       else "\n\n%s" % carried if carried else "\n\nThe running value is %s." % value)
                body = ("%s%s\n\nStep %d: %s\n\nReply with ONLY the resulting number.%s"
                        % (head, ctx, i + 1, op, _CARRY_INSTRUCTION[self.form]))
                msgs = [{"role": "user", "content": body}]

            r = H.call_gated(self.rod[0], self.rod[1], msgs,
                             max_tokens=self.max_tokens, temperature=self.temperature)
            seen = OV.inspect(r, max_tokens=self.max_tokens, prompt=msgs[-1]["content"])
            text = seen["text"] or ""
            # A CARRIER QUOTES WHAT IT CARRIES. `echoes_prompt` is this component's signature, not its
            # debris - it invalidated three separate measurements on 2026-07-26 before anyone checked.
            flags = [f for f in seen["flags"] if f != "echoes_prompt"]
            if not r.get("ok"):
                rec["flags"].append("call_failed")
                rec["trace"].append({"step": i + 1, "ok": False})
                break

            if self.form == "checkpoint":
                m = _STATE.search(text)
                value = int(m.group(1)) if m else _last_int(text)
                carried = ("The running value is %s. You have completed step %s."
                           % (value, m.group(2) if m else i + 1))
            elif self.form == "free":
                value = _last_int(text)
                note = _NOTE.search(text.split("NOTE:", 1)[-1] and "NOTE:" + text.split("NOTE:", 1)[-1])
                carried = ("The running value is %s.\nYour note to yourself: %s"
                           % (value, (note.group(1).strip()[:1200] if note else "(none)")))
            else:
                value = _last_int(text)
                if self.form == "conversation":
                    history = history + [{"role": "user", "content": body},
                                         {"role": "assistant", "content": text[:2000]}]

            rec["trace"].append({"step": i + 1, "ok": True, "value": value,
                                 "truth": truth_fn(i + 1), "hit": value == truth_fn(i + 1),
                                 "tok_out": r.get("tokens"), "tok_in": r.get("prompt_tokens"),
                                 "chars": len(text),
                                 "carried_chars": len(carried), "flags": flags})
            rec["flags"] += flags

        t = [s for s in rec["trace"] if s.get("ok")]
        rec["completed"] = len(t)
        rec["final"] = t[-1]["value"] if t else None
        rec["final_truth"] = truth_fn(len(ops))
        rec["correct"] = bool(t) and t[-1]["step"] == len(ops) and t[-1]["hit"]
        # THE DRIFT POINT: the first step it got wrong and never recovered from. A creature is often
        # legible here when it is invisible in the final number.
        rec["first_miss"] = next((s["step"] for s in t if not s["hit"]), None)
        rec["hits"] = sum(1 for s in t if s["hit"])
        # BOTH DIRECTIONS. `conversation` spends nothing extra on OUTPUT and everything on INPUT,
        # because its cost is a context that grows every step. Summing only output would have priced
        # the most expensive container in this world at zero.
        rec["tok_out"] = sum(s.get("tok_out") or 0 for s in t)
        rec["tok_in"] = sum(s.get("tok_in") or 0 for s in t)
        rec["tok_total"] = rec["tok_out"] + rec["tok_in"]
        rec["carried_max"] = max([s["carried_chars"] for s in t] or [0])
        return rec
