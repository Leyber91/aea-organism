"""x14 - CLOSING C-75. What is the exchange rate between a parse that guesses and a parse that abstains?

L1 left one item open and said why. A permissive parse converts correct working into a confident wrong
answer, and the receipt for that already exists: a loose parse read "b5 moved 2 shelves ahead from shelf 4
to shelf 6" and returned **2**, scoring a rod as wrong when the rod was right (x08b). But run against 288
SHORT replies in x13 it manufactured nothing at all, because a reply of three characters contains nothing
for a loose parse to go wrong in. The hazard was documented and unpriced.

WHAT MAKES THIS RUN ABLE TO SEE IT. Every task here carries NUMERIC DISTRACTORS in the data itself. The
answer is one number among several, so a parse that commits to "the last number" has real chances to grab
the wrong one, and a parse that requires the number to be labelled has real chances to abstain. Nothing
about the prompt names a method, so this stays inside L1.

THE MEASUREMENT IS AN EXCHANGE RATE, NOT A VERDICT. A permissive parse is not purely bad, and treating it
that way would be the same laziness in the other direction. It has three effects and all three are counted:

  MANUFACTURES  strict abstains, loose commits to a WRONG value      pure damage
  CORRUPTS      strict is RIGHT, loose commits to a WRONG value      pure damage
  SAVES         strict abstains, loose commits to the RIGHT value    a genuine recovery

C-75 closes on the ratio. If saves outnumber damage, validation costs accuracy and the census item is
wrong. If damage outnumbers saves, an instrument that cannot abstain must not be trusted, and the rule
generalises to every parser in the walk including the ones we have already written.

Run: python -m aea.lab.x14_C75_parser_validation
"""
from __future__ import annotations

import concurrent.futures as _futures
import re
import time

from aea.lab import harness as H
from aea.lab import overseer as OV
from aea.mind import fuel

N = 8
MAXTOK = 900
TEMPS = (0.2, 0.7)

# EVERY TASK HAS DISTRACTORS. The answer is one number among several in the data, which is the only
# condition under which a permissive parse can be caught doing damage.
TASKS = {
    "latency_field": {
        "prompt": ("How many milliseconds did this run take? Reply with the number.\n"
                   "RUN r-14 - plant=cerebras - model=llama-3.3-70b - 812ms - tokens=1204 - cost=3u"),
        "truth": 812, "label": r"(\d+)\s*ms"},
    "token_field": {
        "prompt": ("How many tokens did this run use? Reply with the number.\n"
                   "RUN r-09 - 786ms - prompt_tokens=45 - completion_tokens=317 - retries=2 - cost=1u"),
        "truth": 317, "label": r"completion_tokens\s*=\s*(\d+)"},
    "year_in_prose": {
        "prompt": ("In what year was the observatory completed? Reply with the number.\n"
                   "Ground was broken in 1971 with 340 workers, the dome shipped in 1974 weighing 96 "
                   "tonnes, and the observatory was completed in 1978 after 7 delays."),
        "truth": 1978, "label": r"completed in (\d{4})"},
}

RODS = [
    ("ollama", "granite4.1:3b",           "micro"),
    ("ollama", "granite4.1:8b",           "normal"),
    ("groq",   "llama-3.1-8b-instant",    "normal"),
    ("groq",   "llama-3.3-70b-versatile", "large"),
    ("cerebras", "gpt-oss-120b",          "large"),
]


def strict(text: str, truth: int):
    """VALIDATING PARSE. Accepts a number only where the reply commits to a single one, or where the
    value is labelled. Abstains otherwise, and abstaining is the behaviour under test."""
    t = (text or "").strip()
    bare = re.fullmatch(r"[^\d]{0,24}?(-?\d{1,6})[^\d]{0,24}", t)
    if bare:
        return int(bare.group(1))
    nums = re.findall(r"-?\d{1,6}", t.replace(",", ""))
    if len(set(nums)) == 1:                      # says one number, however many times
        return int(nums[0])
    m = re.search(r"(?:answer|result|total|is)\D{0,12}(-?\d{1,6})\s*$", t, re.I)
    return int(m.group(1)) if m else None        # ABSTAIN


def loose(text: str, truth: int):
    """PERMISSIVE PARSE. Commits to the last number it can find, always. The shape our own parser had."""
    nums = re.findall(r"-?\d{1,6}", (text or "").replace(",", ""))
    return int(nums[-1]) if nums else None


def _trial(rod, task_id, temp, i):
    t = TASKS[task_id]
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": t["prompt"]}],
                     max_tokens=MAXTOK, temperature=temp)
    seen = OV.inspect(r, max_tokens=MAXTOK, prompt=t["prompt"])
    text = seen["text"]
    s, l, truth = strict(text, t["truth"]), loose(text, t["truth"]), t["truth"]
    return {"trial": i, "ok": bool(r.get("ok")), "flags": seen["flags"],
            "strict": s, "loose": l, "truth": truth,
            "strict_ok": s == truth, "loose_ok": l == truth, "abstained": s is None,
            "manufactures": s is None and l is not None and l != truth,
            "corrupts": s == truth and l is not None and l != truth,
            "saves": s is None and l == truth,
            "chars": len(text), "latency": r.get("latency"), "raw": text[-300:]}


def cell(led, rod, task_id, temp):
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        tr = [f.result() for f in [pool.submit(_trial, rod, task_id, temp, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [t for t in tr if t["ok"] and not t["flags"]]
    for t in tr:
        led.note_flags(t["flags"])
    row = {"rod": "%s/%s" % rod[:2], "size": rod[2], "task": task_id, "temperature": temp,
           "clean": len(ok), "ran": len(tr),
           "strict_ok": sum(1 for t in ok if t["strict_ok"]),
           "loose_ok": sum(1 for t in ok if t["loose_ok"]),
           "abstained": sum(1 for t in ok if t["abstained"]),
           "manufactures": sum(1 for t in ok if t["manufactures"]),
           "corrupts": sum(1 for t in ok if t["corrupts"]),
           "saves": sum(1 for t in ok if t["saves"]),
           "median_chars": sorted([t["chars"] for t in ok])[len(ok) // 2] if ok else 0,
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=temp,
                              attempts=len(tr), failures=len(tr) - len(ok)),
           "trials": tr}
    led.add(row)
    print("    %-24s %-14s t=%.1f  strict %d/%-2d  loose %d/%-2d  abstain %d  MANUF %d  CORRUPT %d  SAVE %d"
          % (row["rod"].split("/")[-1][:23], task_id, temp, row["strict_ok"], row["clean"],
             row["loose_ok"], row["clean"], row["abstained"], row["manufactures"],
             row["corrupts"], row["saves"]), flush=True)
    return row


def run():
    led = OV.Ledger("x14_C75_parser_validation", {
        "level": "L1", "chapter": "II", "closes": ["C-75"],
        "question": "what is the exchange rate between a parse that guesses and one that abstains?",
        "n": N, "temperatures": list(TEMPS), "tasks": list(TASKS), "max_tokens": MAXTOK})
    print("x14 - C-75. %d rods x %d tasks WITH NUMERIC DISTRACTORS x %d temps x n=%d"
          % (len(RODS), len(TASKS), len(TEMPS), N), flush=True)
    for rod in RODS:
        print("\n  %s (%s)" % (rod[1], rod[2]), flush=True)
        for temp in TEMPS:
            for task_id in TASKS:
                if led.has(rod="%s/%s" % rod[:2], task=task_id, temperature=temp):
                    continue
                cell(led, rod, task_id, temp)

    rows = led.doc["rows"]
    tot = lambda k: sum(r[k] for r in rows)
    clean = tot("clean") or 1
    damage, saves = tot("manufactures") + tot("corrupts"), tot("saves")

    if damage == 0 and saves == 0:
        v = ("STILL UNPRICED: the permissive parse neither damaged nor saved anything across %d clean "
             "trials. Even with distractors present the replies did not give it room. C-75 stays open."
             % clean)
    elif damage > saves:
        v = ("C-75 CLOSES: VALIDATION IS LOAD-BEARING. The permissive parse did %d units of damage "
             "(%d manufactured, %d corrupted) against %d saves, on %d clean trials. An instrument that "
             "cannot abstain trades a small recovery for a larger fabrication, and it does so silently."
             % (damage, tot("manufactures"), tot("corrupts"), saves, clean))
    elif saves > damage:
        v = ("C-75 CLOSES THE OTHER WAY: ABSTAINING COSTS MORE THAN IT SAVES. The permissive parse "
             "recovered %d answers the strict one refused, against %d units of damage. Validation as "
             "written is too strict, and the census item needs qualifying rather than adopting."
             % (saves, damage))
    else:
        v = ("C-75 CLOSES AS A WASH: %d damage against %d saves. The permissive parse is neither the "
             "hazard nor the shortcut it was taken for, on these tasks." % (damage, saves))

    led.done(strict_rate=round(tot("strict_ok") / clean, 3), loose_rate=round(tot("loose_ok") / clean, 3),
             abstained=tot("abstained"), manufactures=tot("manufactures"), corrupts=tot("corrupts"),
             saves=tot("saves"), verdict=[v])
    return led.doc


if __name__ == "__main__":
    d = run()
    print()
    print("strict %.3f   loose %.3f   abstained %d" % (d["strict_rate"], d["loose_rate"], d["abstained"]))
    print("MANUFACTURED %d   CORRUPTED %d   SAVED %d" % (d["manufactures"], d["corrupts"], d["saves"]))
    print("overseer:", d["overseer"])
    print()
    for line in d["verdict"]:
        print(" -", line)
    print("\nEVIDENCE  state/lab/runs/x14_C75_parser_validation/%s.json" % d["run_id"])
