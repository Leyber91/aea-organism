"""x12 - CHAPTER I / LEVEL 0. Does a call need a goal, and can bigger fuel supply one it was not given?

THE BOOK IS NOW ONE CHAPTER PER LEVEL, and this is the first. L0 holds exactly four census items:

  C-62  LAYER 0, THE QUESTION            EMBODIED, receipted: a call happens and a reply comes back
  C-01  axis Path                        EMBODIED, receipted by x05 across eight rods
  C-83  lib/client external boundary     disposition O, OUT OF SCOPE by the census's own mark
  C-12  #1 goal-presence                 COMPRESSED, and NEVER TESTED. This experiment exists for it.

STRICTLY L0. One call, one reply. No memory, no second voice, no frame that names a method, no scorer in
the loop. Anything else would measure a construct instead of a rung, which is the confusion that produced
a five-level Chapter I.

THE QUESTION, AND IT HAS TWO HALVES. "Goal-presence" is usually read as *the objective is in the prompt*.
Stated that way it is trivially true and not worth a run. The half nobody has measured is the other one:

  1  SUBSTITUTION   with the objective withheld, does BIGGER FUEL recover it? If a 550b infers what was
                    wanted and a 1b does not, goal-presence is partly substitutable by fuel, and C-12 is
                    a soft floor rather than a hard one. If nobody recovers it at any size, it is hard.
  2  DETECTION      does the rod NOTICE that no objective was given? Asking "what would you like me to do
                    with this?" is a different behaviour from guessing, and it is a capability. A rod that
                    guesses silently will guess silently inside every construct built on top of it.

THREE CONDITIONS on identical data, so the only thing that varies is how much objective is present:

  ABSENT     the data alone
  AMBIGUOUS  the data plus a direction with no objective ("Process this.")
  PRESENT    the data plus the explicit objective

TWO TASKS rather than one, because task breadth is a named gap in this lab: every result so far rests on
wordcount, a 50-step chain, or the five-task bank. Two is not breadth, and it is more than one.

Every reply passes through the overseer before it is scored, so debris is flagged rather than counted, and
the ledger writes each arm to disk the moment it completes. Both exist because this chapter's own rules
were broken while writing it: a run was killed at a wall-clock cap with four finished arms in memory.

Run: python -m aea.lab.x12_L0_goal_presence
"""
from __future__ import annotations

import concurrent.futures as _futures
import re
import time

from aea.lab import harness as H
from aea.lab import overseer as OV
from aea.mind import fuel

N = 8
# 1200 rather than 300. At 300 the reasoning rods (gpt-oss-120b, groq-70b, qwen3:0.6b) spent the whole
# budget thinking and never reached an answer, and run 20260725T184300Z recorded their zeros as if they
# were capability. They were our cap. That run stays on disk as the receipt for this correction.
MAXTOK = 1200
TEMPS = (0.2, 0.7)

WORDS = "the mouth draws power through the ladder and the measure closes the wire"
LOGLINE = "RUN r-14 - plant=cerebras - model=llama-3.3-70b - 812ms"

TASKS = {
    "wordcount": {"data": WORDS,
                  "goal": "Count the words in the sentence below and reply with ONLY the number.",
                  "check": lambda t: bool(re.findall(r"\d+", t or "")) and
                                     re.findall(r"\d+", (t or "").replace(",", ""))[-1] == "13"},
    "extract":   {"data": LOGLINE,
                  "goal": "From the line below, reply with ONLY the plant name and nothing else.",
                  "check": lambda t: "cerebras" in (t or "").lower() and len(t.strip()) < 60},
}

CONDITIONS = ("absent", "ambiguous", "present")

# THREE PLANTS, FOUR SIZE TIERS, and no nvidia. NVIDIA went silent after roughly six thousand calls on
# 2026-07-25 and the live wire now reports it as SILENT rather than hanging. The ledger resumes, so the
# nvidia rods below are declared here and will be measured into the SAME run when the plant returns.
# Chapter I stays honest about fuel diversity instead of quietly becoming a single-plant result.
RODS = [
    ("ollama", "qwen3:0.6b",                          "nano"),
    ("ollama", "granite4.1:3b",                       "micro"),
    ("ollama", "granite4.1:8b",                       "normal"),
    ("groq",   "llama-3.1-8b-instant",                "normal"),
    ("groq",   "llama-3.3-70b-versatile",             "large"),
    ("cerebras", "gpt-oss-120b",                      "large"),
]
PENDING_NVIDIA = [
    ("nvidia", "meta/llama-3.2-1b-instruct",          "nano"),
    ("nvidia", "meta/llama-3.2-3b-instruct",          "micro"),
    ("nvidia", "openai/gpt-oss-20b",                  "normal"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b",   "large"),
]

# DETECTION. A reply that asks what to do, rather than guessing. Deliberately narrow: it must actually
# pose a question about the task, so "Is this correct?" after an attempt does not count as detection.
_ASKS = re.compile(r"(what (would you like|do you want|should I)|"
                   r"(could|can) you (clarify|specify|tell me what)|"
                   r"please (clarify|specify)|"
                   r"(no|without) (clear |specific )?(instruction|task|question|request)|"
                   r"how (would you like|can I help)|what (is|are) (the|your) (task|question|goal))", re.I)


def prompt_for(task_id: str, cond: str) -> str:
    t = TASKS[task_id]
    if cond == "absent":
        return t["data"]
    if cond == "ambiguous":
        return "Process this.\n\n" + t["data"]
    return t["goal"] + "\n" + t["data"]


def _trial(rod, task_id, cond, temp, i):
    p = prompt_for(task_id, cond)
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": p}],
                     max_tokens=MAXTOK, temperature=temp)
    seen = OV.inspect(r, max_tokens=MAXTOK, prompt=p)
    text = seen["text"]
    return {"trial": i, "ok": bool(r.get("ok")), "flags": seen["flags"],
            "satisfied": bool(TASKS[task_id]["check"](text)) if seen["clean"] else False,
            "asked": bool(_ASKS.search(text)), "chars": len(text), "raw": text[-300:],
            "tok_in": r.get("prompt_tokens") or 0, "tok_out": r.get("tokens") or 0}


def cell(led, rod, task_id, cond, temp):
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        tr = [f.result() for f in
              [pool.submit(_trial, rod, task_id, cond, temp, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [t for t in tr if t["ok"]]
    for t in tr:
        led.note_flags(t["flags"])
    row = {"rod": "%s/%s" % rod[:2], "size": rod[2], "task": task_id, "condition": cond,
           "temperature": temp,
           "satisfied": sum(1 for t in ok if t["satisfied"]), "scored": len(ok),
           "asked": sum(1 for t in ok if t["asked"]),
           "distinct_replies": len({t["raw"] for t in ok}),
           "flagged": sum(1 for t in tr if t["flags"]),
           "tok_in": sum(t["tok_in"] for t in ok), "tok_out": sum(t["tok_out"] for t in ok),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=temp,
                              attempts=len(tr), failures=len(tr) - len(ok)),
           "trials": tr}
    led.add(row)
    print("    %-42s %-9s %-9s t=%.1f  satisfied %d/%-2d  asked %d  distinct %d"
          % (row["rod"][:41], task_id, cond, temp, row["satisfied"], row["scored"],
             row["asked"], row["distinct_replies"]), flush=True)
    return row


def run():
    led = OV.Ledger("x12_L0_goal_presence", {
        "level": "L0", "chapter": "I",
        "closes": ["C-12"], "inherits": ["C-62", "C-01"], "out_of_scope": ["C-83"],
        "question": "does a single call need its goal stated, can bigger fuel recover an unstated one, "
                    "and does a rod notice when no goal was given?",
        "n": N, "temperatures": list(TEMPS), "conditions": list(CONDITIONS),
        "tasks": list(TASKS)})
    print("x12 - LEVEL 0, chapter I. %d rods x %d tasks x %d conditions x %d temps x n=%d"
          % (len(RODS), len(TASKS), len(CONDITIONS), len(TEMPS), N), flush=True)
    print("     run %s%s, writing incrementally to state/lab/runs/x12_L0_goal_presence/"
          % (led.run_id, " RESUMED, %d cells already on disk" % len(led.doc["rows"])
             if getattr(led, "resumed", False) else ""), flush=True)
    for temp in TEMPS:
        print("\n  TEMPERATURE %.1f" % temp, flush=True)
        for rod in RODS:
            for task_id in TASKS:
                for cond in CONDITIONS:
                    key = {"rod": "%s/%s" % rod[:2], "task": task_id,
                           "condition": cond, "temperature": temp}
                    if led.has(**key):
                        continue          # already on disk from an earlier, killed attempt
                    cell(led, rod, task_id, cond, temp)

    rows = led.doc["rows"]

    def rate(pred, key="satisfied"):
        sel = [r for r in rows if pred(r)]
        tot = sum(r["scored"] for r in sel)
        return (sum(r[key] for r in sel) / tot) if tot else None

    by_cond = {c: rate(lambda r, c=c: r["condition"] == c) for c in CONDITIONS}
    ask_cond = {c: rate(lambda r, c=c: r["condition"] == c, "asked") for c in CONDITIONS}
    by_size = {}
    for sz in ("nano", "micro", "normal", "large"):
        by_size[sz] = {c: rate(lambda r, c=c, s=sz: r["condition"] == c and r["size"] == s)
                       for c in CONDITIONS}

    # SUBSTITUTION: does any size recover an unstated goal? The comparison is absent/ambiguous against
    # present, WITHIN a size tier, so a rod that simply cannot do the task is not counted as a rod that
    # failed to infer the goal.
    recovers = [sz for sz, v in by_size.items()
                if v["present"] and v["present"] > 0.2
                and max(v["absent"] or 0, v["ambiguous"] or 0) >= 0.5 * v["present"]]
    detects = [r["rod"] for r in rows if r["condition"] in ("absent", "ambiguous")
               and r["scored"] and r["asked"] / r["scored"] >= 0.5]

    if not recovers:
        v1 = ("GOAL-PRESENCE IS A HARD FLOOR AT L0. No size tier recovered an unstated objective at even "
              "half its stated-objective rate. C-12 is load-bearing rather than compressed: without the "
              "goal in the prompt the call cannot succeed, and no amount of fuel substitutes for it.")
    else:
        v1 = ("GOAL-PRESENCE IS PARTLY SUBSTITUTABLE BY FUEL: %s recovered an unstated objective. C-12 is "
              "a soft floor, and its placement needs qualifying by size." % ", ".join(recovers))

    if detects:
        v2 = ("DETECTION EXISTS on %d rod(s): %s asked what was wanted rather than guessing. Noticing an "
              "absent goal is a capability separate from having one, and the census has no row for it."
              % (len(set(detects)), ", ".join(sorted({d.rsplit('/', 1)[-1] for d in detects}))))
    else:
        v2 = ("NO ROD DETECTS AN ABSENT GOAL. Every rod guessed rather than asking, at every size and both "
              "temperatures. A construct built on this substrate inherits silent guessing at its base, "
              "which is a candidate item the 86 does not carry.")

    led.done(by_condition=by_cond, asked_by_condition=ask_cond, by_size=by_size,
             verdict=[v1, v2])
    return led.doc


if __name__ == "__main__":
    d = run()
    print()
    print("SATISFIED by condition:", {k: (round(v, 3) if v is not None else None)
                                      for k, v in d["by_condition"].items()})
    print("ASKED     by condition:", {k: (round(v, 3) if v is not None else None)
                                      for k, v in d["asked_by_condition"].items()})
    print("BY SIZE:")
    for sz, v in d["by_size"].items():
        print("  %-7s %s" % (sz, {k: (round(x, 2) if x is not None else None) for k, x in v.items()}))
    print("\noverseer flags:", d["overseer"])
    print()
    for line in d["verdict"]:
        print(" -", line)
    print("\nEVIDENCE  state/lab/runs/x12_L0_goal_presence/%s.json" % d["run_id"])
