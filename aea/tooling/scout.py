"""scout.py - SURVEY AN EXTERNAL REPOSITORY WITH RODS, NOT WITH THE OPERATOR'S CONTEXT.

THE CAPABILITY, and Luis named it: "an established way to scope repositories, take the relevant
information, and use the good combination of models we need." Reading a 324-item repo by hand burns
the one context that has to hold the whole project. Free measured rods cost nothing we are short of.

THE FIRST VERSION FAILED AND ITS FAILURE IS THE DESIGN NOTE. It scored each item 0-100 with a
separate `relevant` boolean, one item per call, 323 calls. Rods returned `relevant=true,
confidence=0` with reasons like "not needed" and "Yes, I am sure." Five causes, four of them mine:

  1 TWO FIELDS THAT CAN CONTRADICT. `relevant: bool` and `confidence: int` are independently valid,
    so a strict schema validates the contradiction. One field cannot disagree with itself.
  2 INFORMATION STARVATION. One line of description against a five-part purpose is a guess, not a
    judgement. Items now carry their opening body text too.
  3 ABSOLUTE SCORING WITHOUT ANCHORS. A 0-100 scale drifts per rod, which is why the scores came
    back bimodal at 0 and 95. Replaced by a CLOSED VOCABULARY, where there is nothing to anchor.
  4 COMPARATIVE BEATS ABSOLUTE, AND IS CHEAPER. Twenty items per call asks the rod to pick from a
    list, which is the task it is good at, and costs 7 calls per rod instead of 323.
  5 NO CONTROL (law M4, our own file). Now every batch carries a PLANTED POSITIVE and a PLANTED
    NEGATIVE. A rod that misses either has its whole batch VOIDED and re-run - which is D18 turned
    into a mechanism: a detector never shown a positive it must catch has not been tested, only run.

Two rods judge every batch. Agreement is the finding; DISAGREEMENT IS REPORTED rather than averaged
away, because a split verdict is the thing a human should read personally.

  python -m aea.tooling.scout NVIDIA/skills "reach the internet, speak, and retrieve"
  python -m aea.tooling.scout NVIDIA/skills "..." --limit 60 --batch 20
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

from aea.energy import rodprobe
from aea.kernel import grid

OUT = os.path.join(grid.STATE, "scout")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
API = dict(UA, Accept="application/vnd.github+json")

# Measured 2026-07-29: all four pass json_schema strictly. Spread across families on purpose, so a
# systematic bias in one does not colour the survey, and across buckets, since the rate ceiling is
# PER ROD (measured at 4 concurrent) and N rods is N times the throughput.
# MEASURED ON THIS TASK, not on a trivial one (law M10). Every rod below survived the planted
# control on a batched classification; the ones removed did not, and each failed differently:
#   nano-9b-v2      systematic `tool-calling` bias that SURVIVED an explicit written exclusion,
#                   even though it scored 3/3 with zero false rejects as a single-output inspector
#   nano-30b-a3b    leaked its reasoning into `content` on a long batch despite strict json_schema
#   gpt-oss-120b    three timeouts; measured at 129.6s average on structured output
#   deepseek-v4-pro two HTTP 500s of nine calls
PANEL = [
    "nvidia/nemotron-3-super-120b-a12b",         # 1M ctx, RULER 100, the only rod that held
    "nvidia/nemotron-3-ultra-550b-a55b",         # 1M ctx, TauBench 81.5; capacity-limited, so second
    "minimaxai/minimax-m3",                      # 1M ctx, a different family entirely
]

# A CLOSED VOCABULARY. Nothing to anchor, nothing to drift, and "none" is a real answer rather than
# the absence of one. Extend this list to re-scope; do not add a score.
CATEGORIES = ("voice", "retrieval", "internet", "tool-calling", "verify-change", "none")

# THE ANSWER KEY WE PLANT. Written here, so the hand that wrote the questions did not write these
# (law M3), and deliberately unambiguous: a rod that misses one is not judging, it is emitting.
CANARY_POS = {"unit": "__canary_web_search", "name": "web-search-live",
              "description": "Search the public web and return ranked results with citations. "
                             "Use when an agent needs live information from the internet.",
              "body": "Issues a query to a web search API and returns titles, URLs and snippets.",
              "expect": "internet"}
# THE NEGATIVE IS THE NEAR-MISS, not an obvious non-example (law M7). The first version planted a
# GPU fan-curve skill and six rods called it `tools`, which voided all eighteen batches - a real
# defect caught by luck, since the item was chosen for being plainly unrelated. This one is chosen
# to be maximally tempting: it uses agent vocabulary throughout and is still `none`, because
# configuring a deployment is not the entity reaching, speaking, retrieving or verifying itself.
CANARY_NEG = {"unit": "__canary_deploy", "name": "agent-runtime-autoscaler",
              "description": "Configure autoscaling and GPU affinity for an agent runtime cluster. "
                             "Use when agent workloads need more replicas or better placement.",
              "body": "Sets replica counts, node selectors and GPU memory limits for the serving "
                      "layer that hosts agent workloads. Does not change what any agent can do.",
              "expect": "none"}

VERDICTS = {
    "type": "object",
    "properties": {"verdicts": {"type": "array", "items": {
        "type": "object",
        "properties": {"n": {"type": "integer"},
                       "category": {"type": "string", "enum": list(CATEGORIES)},
                       "why": {"type": "string"}},
        "required": ["n", "category", "why"],
        "additionalProperties": False}}},
    "required": ["verdicts"],
    "additionalProperties": False,
}

ASK = """You are scoping a repository for one purpose. Classify EVERY numbered item below.

PURPOSE:
%s

CATEGORIES - choose exactly one per item:
  voice        speech in or out: ASR, TTS, transcription, diarization, translation of speech
  retrieval    finding things in our own documents: embedding, reranking, indexing, RAG
  internet     reaching the live outside world: web search, fetching, browsing, crawling
  tool-calling the item's SUBJECT is an agent calling tools: function calling, MCP, tool schemas,
               orchestrating multi-step agent work
  verify-change testing or gating a change to a system BEFORE adopting it
  none         everything else, INCLUDING excellent work for other hardware, other products,
               model training, robotics, simulation, graphics and infrastructure

EVERY item in this repository is itself a skill an agent can invoke. That alone NEVER makes it
`tool-calling` - choose that category only when the item is ABOUT agents calling tools. A skill that
configures hardware, trains a model or installs an SDK is `none`, however invokable it is.

Most items in a large repository are `none` for any given purpose. Saying `none` is the useful
answer and there is no penalty for it. `why` is one short clause naming what decided it.

ITEMS
%s

Return one verdict per item, using the item's number as `n`."""


# ------------------------------------------------------------------ the free half
def gh(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=API), timeout=60) as r:
        return json.load(r)


def _head(url, nbytes=2600):
    try:
        req = urllib.request.Request(url, headers=dict(UA, Range="bytes=0-%d" % nbytes))
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception:
        return ""


def inventory(repo: str) -> list:
    """Every unit, its description AND its opening body text. Free: no rod is spent here, and the
    body is what cures the starvation that made the first version guess."""
    meta = gh("https://api.github.com/repos/%s" % repo)
    branch = meta.get("default_branch") or "main"
    tree = gh("https://api.github.com/repos/%s/git/trees/%s?recursive=1" % (repo, branch))
    paths = sorted(e["path"] for e in (tree.get("tree") or [])
                   if e["path"].lower().endswith(("skill.md", "readme.md"))
                   and e["path"].count("/") <= 3)
    base = "https://raw.githubusercontent.com/%s/%s/" % (repo, branch)

    def one(p):
        t = _head(base + p)
        d = (re.search(r"^description:\s*(.+)$", t, re.M | re.I) or [None, ""])[1]
        n = (re.search(r"^name:\s*(.+)$", t, re.M | re.I) or [None, ""])[1]
        body = t.split("---", 2)[-1]
        body = re.sub(r"^#.*$", " ", body, flags=re.M)
        body = re.sub(r"\s+", " ", body).strip()
        return {"path": p, "unit": p.rsplit("/", 2)[-2] if "/" in p else p,
                "name": n.strip().strip('"'), "description": d.strip().strip('"')[:260],
                "body": body[:420]}
    with ThreadPoolExecutor(max_workers=16) as ex:
        rows = list(ex.map(one, paths))
    return [r for r in rows if r["description"] or r["body"]]


# ------------------------------------------------------------------ the judged half
def _render(items) -> str:
    out = []
    for i, it in enumerate(items, 1):
        out.append("%d. %s\n   %s\n   %s" % (i, it.get("name") or it["unit"],
                                             (it.get("description") or "")[:230],
                                             (it.get("body") or "")[:300]))
    return "\n".join(out)


def judge_batch(items, purpose, rod):
    """One call over a whole batch. Returns (verdict-by-index, void-reason-or-None)."""
    body = dict(rodprobe.body_for(rod, [{"role": "user",
                                         "content": ASK % (purpose, _render(items))}]),
                response_format={"type": "json_schema", "json_schema":
                                 {"name": "verdicts", "strict": True, "schema": VERDICTS}})
    body["max_tokens"] = 4000
    d, secs, err = rodprobe.ask("nvidia", "/v1/chat/completions", body)
    if err:
        return {}, "transport: " + err[:70]
    content, _, _ = rodprobe.reply_of(d)
    try:
        got = json.loads(content).get("verdicts") or []
    except Exception:
        return {}, "unparseable: " + content[:70]
    by_n = {v["n"]: v for v in got if isinstance(v.get("n"), int)}
    if len(by_n) < len(items):
        return by_n, "incomplete: %d of %d verdicts" % (len(by_n), len(items))
    # THE PLANTED KEY. A rod that misses either canary has its whole batch voided, because a judge
    # that cannot spot an obvious positive is not judging the ambiguous ones either.
    for i, it in enumerate(items, 1):
        if "expect" in it:
            said = (by_n.get(i) or {}).get("category")
            if said != it["expect"]:
                return by_n, "CANARY MISS: %s judged %r, expected %r" % (it["unit"], said,
                                                                         it["expect"])
    return by_n, None


def survey(repo: str, purpose: str, limit: int = 0, batch: int = 10) -> dict:
    items = inventory(repo)
    print("  inventory: %d units with description + body (free)" % len(items), flush=True)
    if limit:
        items = items[:limit]

    # Batches carry both canaries at fixed positions, so the layout is reproducible.
    batches = []
    for i in range(0, len(items), batch):
        chunk = items[i:i + batch]
        mixed = chunk[:3] + [CANARY_POS] + chunk[3:] + [CANARY_NEG]
        batches.append(mixed)
    print("  %d batches of ~%d, each carrying a planted positive and negative"
          % (len(batches), batch), flush=True)

    # TWO RODS PER BATCH. Agreement is the finding, disagreement is reported.
    jobs = [(bi, b, PANEL[(bi + k) % len(PANEL)]) for bi, b in enumerate(batches) for k in (0, 1)]
    ceiling = grid.METER.ceiling("nvidia") or 4

    def run(job):
        bi, b, rod = job
        by_n, void = judge_batch(b, purpose, rod)
        return bi, b, rod, by_n, void

    with ThreadPoolExecutor(max_workers=ceiling * len(PANEL)) as ex:
        results = list(ex.map(run, jobs))

    voided = [(r[2], r[4]) for r in results if r[4]]
    votes = defaultdict(dict)                      # unit -> rod -> (category, why)
    for bi, b, rod, by_n, void in results:
        if void:
            continue
        for i, it in enumerate(b, 1):
            if "expect" in it:
                continue
            v = by_n.get(i)
            if v:
                votes[it["unit"]][rod] = (v["category"], v.get("why", ""))

    agreed, split, agreed_none = [], [], []
    meta = {it["unit"]: it for it in items}
    for unit, byrod in votes.items():
        cats = {c for c, _ in byrod.values()}
        row = {"unit": unit, "name": meta.get(unit, {}).get("name", ""),
               "description": meta.get(unit, {}).get("description", "")[:150],
               "votes": {r.rsplit("/", 1)[-1]: c for r, (c, _) in byrod.items()},
               "why": next(iter(byrod.values()))[1][:110]}
        if len(cats) == 1:
            row["category"] = cats.pop()
            # WRITTEN PLAINLY, BECAUSE THE CLEVER VERSION WAS SILENTLY DEAD. This was
            # `(agreed if row["category"] != "none" else []) and agreed.append(row)`, and `agreed`
            # starts EMPTY, so `[] and ...` short-circuited and append never ran. Three whole runs
            # reported "0 relevant" from a one-liner, not from the rods. Law M9: the line I wrote
            # fastest is the line I never re-read.
            if row["category"] != "none":
                agreed.append(row)
            else:
                agreed_none.append(row)
        else:
            row["category"] = "SPLIT"
            split.append(row)

    doc = {"repo": repo, "purpose": purpose, "units": len(items), "batches": len(batches),
           "calls": len(jobs), "voided": voided, "judged": len(votes),
           "agreed_relevant": agreed, "split": split, "panel": PANEL,
           # EVERY verdict is kept, including the unanimous `none`s. Dropping them made a wrong
           # zero indistinguishable from a right one, and cost three runs to notice.
           "agreed_none": [r["unit"] for r in agreed_none]}
    grid.atomic_save_json(os.path.join(OUT, repo.replace("/", "_") + ".json"), doc, indent=1)
    return doc


def render(doc: dict) -> str:
    L = ["SCOUT - %s" % doc["repo"], "purpose: %s" % doc["purpose"][:96], "=" * 100,
         "%d units | %d batches | %d calls (was 323 one-per-item) | %d judged | %d batches VOIDED"
         % (doc["units"], doc["batches"], doc["calls"], doc["judged"], len(doc["voided"])), ""]
    for rod, why in doc["voided"][:8]:
        L.append("  VOID  %-40s %s" % (rod.rsplit("/", 1)[-1], why[:60]))
    by_cat = defaultdict(list)
    for r in doc["agreed_relevant"]:
        by_cat[r["category"]].append(r)
    L.append("")
    L.append("BOTH RODS AGREED AND IT IS NOT `none`  (%d)" % len(doc["agreed_relevant"]))
    for cat in ("internet", "voice", "retrieval", "tools", "self-modify"):
        rows = by_cat.get(cat) or []
        if not rows:
            continue
        L.append("")
        L.append("--- %s (%d) ---" % (cat.upper(), len(rows)))
        for r in rows[:12]:
            L.append("   %-40s %s" % (r["unit"][:39], r["why"][:64]))
    L += ["", "SPLIT - the two rods disagreed, so a human decides (%d):" % len(doc["split"])]
    for r in doc["split"][:12]:
        L.append("   %-38s %s" % (r["unit"][:37], r["votes"]))
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python -m aea.tooling.scout OWNER/REPO \"the purpose\" [--limit N] [--batch N]")
        raise SystemExit(2)
    repo, purpose = sys.argv[1], sys.argv[2]
    lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0
    bs = int(sys.argv[sys.argv.index("--batch") + 1]) if "--batch" in sys.argv else 10
    print("SCOUTING %s\n" % repo, flush=True)
    print(render(survey(repo, purpose, limit=lim, batch=bs)))
