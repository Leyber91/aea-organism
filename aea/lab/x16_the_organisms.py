"""x16 - RUNNING THE CREATURES. Every version of the AEA, assembled and fired on pinned fuel.

This is the first experiment in the walk that measures THE BUILDING rather than the ground under it. A
creature is an assembled entity: version N of the AEA is the first N components seated, running end to
end. Fuel is PINNED, never chosen by a ladder, because the same organism on different fuel is a different
creature and an unstated rod makes every number meaningless.

THREE FAMILIES, and the last two are the point:

  ASCENDING   v1..v7. Each is everything before it plus one component. The question for each is not
              "is it better" but **what can it newly do that the version below could not**
  TOXIC       an assembly whose precondition is absent. It runs and returns something, and the something
              may be empty. `verdict_is_empty` counts a judgement passed on a question nobody asked
  OBLIQUE     an assembly that skips a rung and may work anyway. Each one that works is a counterexample
              to C-63, the ordering claim

THE CASE THAT IS IN BOTH LISTS. `call+frame` has an unmet precondition by declaration (a frame requires a
goal) and x15 measured a goal-less procedure succeeding 25 of 33. So it is toxic on paper and oblique in
practice, and that contradiction is the sharpest thing this run can settle.

THREE RODS, chosen to span the diagnosis rather than the size ladder:
  granite4.1:3b     fails bare, converted by a frame       (needs the rung)
  groq 8b-instant   partial either way                     (in between)
  nemotron-550b     passes bare, gains almost nothing      (does not need the rung)

Run: python -m aea.lab.x16_the_organisms
"""
from __future__ import annotations

import concurrent.futures as _futures
import time

from aea.lab import overseer as OV
from aea.lab.organism import Organism, ascending, oblique, toxic
from aea.mind import fuel

N = 8
TEMP = 0.2

TASKS = {
    "wordcount": {
        "id": "wordcount", "truth": 13,
        "data": "the mouth draws power through the ladder and the measure closes the wire",
        "goal": "Count the words in the sentence below and reply with the number.",
        "method": ("To count words: split the sentence on spaces, number each token 1, 2, 3 and so on, "
                   "then report the FINAL index. Show the numbered list, then the count alone on the "
                   "last line.")},
    "vowelcount": {
        "id": "vowelcount", "truth": 7,
        "data": "unconventionality",
        "goal": "How many of the letters a, e, i, o, u are in the word below? Reply with the number.",
        "method": ("To count these letters: go through the word one letter at a time, number each "
                   "occurrence of a, e, i, o or u as you find it 1, 2, 3 and so on, then report the "
                   "FINAL index. Show the numbered list, then the count alone on the last line.")},
}

RODS = [
    ("ollama", "granite4.1:3b"),
    ("groq",   "llama-3.1-8b-instant"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
]


def cell(led, org, task_id, family):
    t = TASKS[task_id]
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        recs = [f.result() for f in [pool.submit(org.run, t, temperature=TEMP) for _ in range(N)]]
    finally:
        pool.shutdown(wait=True)
    clean = [r for r in recs if r["ok"] and not r["flags"]]
    for r in recs:
        led.note_flags(r["flags"])
    row = {"family": family, "organism": org.label, "version": org.version,
           "parts": list(org.keys), "rod": "%s/%s" % org.rod, "task": task_id,
           "precondition_unmet": org.unmet, "clean": len(clean), "ran": len(recs),
           # correct: the answer matched, whether or not the organism could KNOW it
           "correct": sum(1 for r in clean if r["answer"] == t["truth"]),
           "answered": sum(1 for r in clean if r["answer"] is not None),
           "abstained": sum(1 for r in clean if r["answer"] is None),
           "read_by_work": sum(1 for r in clean if r["read_by"] == "work"),
           # can it KNOW? only an organism with THE MEASURE has a verdict at all
           "has_verdict": sum(1 for r in clean if r["verdict"] is not None),
           "empty_verdicts": sum(1 for r in clean if r.get("verdict_is_empty")),
           "fuel": fuel.stamp(org.rod[0], org.rod[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(clean)),
           "records": recs}
    led.add(row)
    print("    %-34s %-24s %-11s correct %d/%-2d  answered %d  abstain %d  %s"
          % (org.label[:33], org.rod[1].rsplit("/", 1)[-1][:23], task_id,
             row["correct"], row["clean"], row["answered"], row["abstained"],
             ("EMPTY VERDICTS %d" % row["empty_verdicts"]) if row["empty_verdicts"] else ""), flush=True)
    return row


def run():
    led = OV.Ledger("x16_the_organisms", {
        "what": "versions of the AEA, assembled and fired on pinned fuel",
        "question": "what can each version newly do, which assemblies run empty, and which skip a rung "
                    "and work anyway?",
        "n": N, "temperature": TEMP, "rods": ["%s/%s" % r for r in RODS], "tasks": list(TASKS)})
    plan = ([("ascending", "v%d" % v, keys) for v, keys in ascending()]
            + [("toxic", name, keys) for name, keys in toxic()]
            + [("oblique", name, keys) for name, keys in oblique()])
    print("x16 - %d assemblies x %d rods x %d tasks x n=%d\n" % (len(plan), len(RODS), len(TASKS), N),
          flush=True)
    for family, label, keys in plan:
        ver = int(label[1:]) if family == "ascending" else None
        print("  [%s] %s  =  %s" % (family, label, "+".join(keys)), flush=True)
        for rod in RODS:
            org = Organism(keys, rod, version=ver, label=label)
            for task_id in TASKS:
                if led.has(organism=label, rod="%s/%s" % rod, task=task_id):
                    continue
                cell(led, org, task_id, family)

    rows = led.doc["rows"]

    def rate(pred, key="correct"):
        sel = [r for r in rows if pred(r)]
        tot = sum(r["clean"] for r in sel)
        return (sum(r[key] for r in sel) / tot) if tot else None

    asc = {}
    for v, keys in ascending():
        asc["v%d" % v] = {"correct": rate(lambda r, l="v%d" % v: r["organism"] == l),
                          "can_know": rate(lambda r, l="v%d" % v: r["organism"] == l, "has_verdict"),
                          "parts": keys}
    tox = {name: {"correct": rate(lambda r, n=name: r["organism"] == n),
                  "empty": sum(r["empty_verdicts"] for r in rows if r["organism"] == name),
                  "unmet": next((r["precondition_unmet"] for r in rows if r["organism"] == name), None)}
           for name, _ in toxic()}
    obl = {name: {"correct": rate(lambda r, n=name: r["organism"] == n)} for name, _ in oblique()}

    v = []
    prev = None
    for k in sorted(asc, key=lambda x: int(x[1:])):
        c = asc[k]["correct"]
        if c is not None and prev is not None and abs(c - prev) < 0.02:
            v.append("%s adds no accuracy over the version below (%.2f). If it adds a capability it is "
                     "not one this task can show." % (k, c))
        prev = c if c is not None else prev
    works = [n for n, d in obl.items() if (d["correct"] or 0) >= 0.5]
    if works:
        v.append("OBLIQUE ASSEMBLIES THAT WORK: %s. Each skips a rung beneath it and still answers, which "
                 "is a counterexample to C-63." % ", ".join(works))
    else:
        v.append("NO OBLIQUE ASSEMBLY REACHED 0.5. C-63 survives this run.")
    for n, d in tox.items():
        v.append("TOXIC %s: correct %.2f, empty verdicts %d, unmet %s."
                 % (n, d["correct"] or 0, d["empty"], d["unmet"]))

    led.done(ascending=asc, toxic=tox, oblique=obl, verdict=v)
    return led.doc


if __name__ == "__main__":
    d = run()
    print("\nTHE ASCENDING SERIES")
    for k in sorted(d["ascending"], key=lambda x: int(x[1:])):
        a = d["ascending"][k]
        print("  %-4s %-46s correct %s   can-know %s"
              % (k, "+".join(a["parts"])[:45],
                 ("%.2f" % a["correct"]) if a["correct"] is not None else " -  ",
                 ("%.2f" % a["can_know"]) if a["can_know"] is not None else " -  "))
    print("\nTOXIC");   [print("  %-32s %s" % (k, v_)) for k, v_ in d["toxic"].items()]
    print("\nOBLIQUE"); [print("  %-32s %s" % (k, v_)) for k, v_ in d["oblique"].items()]
    print("\noverseer:", d["overseer"])
    print()
    for line in d["verdict"]:
        print(" -", line)
    print("\nEVIDENCE  state/lab/runs/x16_the_organisms/%s.json" % d["run_id"])
