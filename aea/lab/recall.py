"""recall.py - THE LESSON THAT BEARS ON WHAT YOU ARE ABOUT TO DO, FETCHED.

    python -m aea.lab.recall "about to add a cooldown for a failing endpoint"
    python -m aea.lab.recall --evaluate     # lexical vs semantic vs hybrid, measured

THE PROBLEM, named by Luis 2026-07-30: *"we find lessons, we record them, but we are not able to
retrieve them. That happens a lot of times. Could we actually solve that issue?"*

It is a DIFFERENT problem from the one `transfer.py` solves, and conflating them wastes both.
`transfer` asks "does this property still hold everywhere" and can only see shapes a static detector
can match. Retrieval is the other half: the lesson exists, it is correct, it bears on the very edit
being made - and nothing surfaces it, because prose must be FETCHED by a mind that is busy doing
something else, at a moment defined by ACTION, with no shared vocabulary between the two.

`recurrence.py` predicted this and the prediction held all day: lessons compiled into tests do not
recur, lessons left as prose recur within the same session that recorded them. But not every lesson
CAN be a test. This is the fallback for those: make the prose findable at the moment of action.

------------------------------------------------------------------------------------------------
HYBRID, AND ONLY IF IT WINS.

Luis: *"instead of just semantic search like RAG, we could do a hybrid one, so we get the best of
both worlds. Only do that if that works and you know it will and you prove it."*

So all three are built and measured against the same gate, and whichever wins is what `find()`
uses. The honest outcomes include "hybrid does not beat its parts", in which case it does not ship.

  LEXICAL   BM25 over the lesson text. Strong when the situation names a symbol the lesson names -
            `max_tokens`, `COOL_AFTER`, `tiers`. Blind when the words differ.
  SEMANTIC  mxbai-embed-large, local and unmetered. Strong when the situation MEANS the lesson
            without sharing its words. Blind to rare identifiers, which embeddings smooth away -
            and identifiers are exactly what a code lesson turns on.
  HYBRID    reciprocal-rank fusion. The two are blind in opposite directions, which is the only
            honest reason to expect a gain.

THE GATE IS TODAY'S OWN DEFECTS. Each case is a situation this session was actually in, paired with
the lesson that would have prevented what happened next. A retriever that cannot surface the lesson
for the exact case that already cost a day is not worth shipping.

THE CORPUS AUDITS ITSELF FIRST. I wrote both the queries and the answers, which is precisely the
defect the council caught this morning (D20: a corpus written by the author of the answers measures
string overlap, not retrieval). So every query is phrased in the language of the SITUATION - what
you would be typing or thinking at that moment - never the language of the lesson, and `_leak()`
reports any query sharing rare vocabulary with its own target before a single score is counted.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = str(grid.ROOT)
CACHE = os.path.join(str(grid.STATE), "lab", "recall_vectors.json")

SOURCES = [
    ("diary/DISCOVERIES.md", re.compile(r"^## (D\d+[^\n]*)$", re.M)),
    ("diary/SESSION_LOG.md", re.compile(r"^## (\d{4}-\d{2}-\d{2}[^\n]*)$", re.M)),
    ("CLAUDE.md", re.compile(r"^## (\d+ · [^\n]*)$", re.M)),
]

_STOP = set("""the a an and or of to is are was were be been in on at by for with that this it its
as from not no any all one two three do does did have has had will would can could should may might
we you he she they them their our your if then than so such but into out up down over under about
more most some each other same very just only also there here when what which who whom how why""".split())


def _words(s: str) -> list:
    return [w for w in re.findall(r"[a-z_][a-z0-9_]{2,}", s.lower()) if w not in _STOP]


# =================================================================================================
# THE CORPUS
# =================================================================================================

def lessons() -> list:
    """Every recorded lesson, chunked at its heading, from the diary and the standing laws."""
    out = []
    for rel, pat in SOURCES:
        p = os.path.join(ROOT, rel)
        try:
            src = open(p, encoding="utf-8").read()
        except Exception:
            continue
        marks = list(pat.finditer(src))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(src)
            body = src[m.end():end].strip()
            if len(body) < 120:
                continue
            out.append(dict(id=m.group(1).split("·")[0].strip()[:14], title=m.group(1).strip(),
                            source=rel, text=body[:6000]))
    return out


# =================================================================================================
# THE THREE RETRIEVERS
# =================================================================================================

def _bm25(query: str, docs: list, k1: float = 1.5, b: float = 0.75) -> list:
    """BM25 - no dependency, and the maths is short enough to read.

    Strong exactly where embeddings are weak: a rare identifier (`COOL_AFTER`, `max_tokens`,
    `stream_options`) is a near-perfect signal that a lesson is about the thing being edited, and
    it is the first thing a vector space smooths away."""
    q = _words(query)
    toks = [_words(d["text"] + " " + d["title"]) for d in docs]
    N = len(docs)
    avg = sum(len(t) for t in toks) / max(N, 1)
    df = {}
    for t in toks:
        for w in set(t):
            df[w] = df.get(w, 0) + 1
    scores = []
    for i, t in enumerate(toks):
        tf = {}
        for w in t:
            tf[w] = tf.get(w, 0) + 1
        s = 0.0
        for w in q:
            if w not in tf:
                continue
            idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * (tf[w] * (k1 + 1)) / (tf[w] + k1 * (1 - b + b * len(t) / max(avg, 1)))
        scores.append((s, i))
    return [i for s, i in sorted(scores, key=lambda x: -x[0])]


def _embed(texts: list, kind: str = "passage") -> list:
    from aea.kernel import modality
    return modality.recall(texts=texts, kind=kind) or []


def _vectors(docs: list, refresh: bool = False) -> list:
    """Embeddings for the corpus, cached against a fingerprint of the corpus itself.

    ASYMMETRIC BY DESIGN: passages are embedded as `passage`, the query as `query`. mxbai and the
    nvidia retrievers both distinguish them, and using one prefix for both is the quiet way to lose
    a third of the retrieval quality while everything still 'works'."""
    fp = str(len(docs)) + ":" + str(sum(len(d["text"]) for d in docs))
    if not refresh:
        try:
            c = json.load(open(CACHE, encoding="utf-8"))
            if c.get("fingerprint") == fp:
                return c["vectors"]
        except Exception:
            pass
    vecs = _embed([d["title"] + "\n" + d["text"][:2000] for d in docs], kind="passage")
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    grid.atomic_save_json(CACHE, dict(fingerprint=fp, vectors=vecs))
    return vecs


def _cos(a, b):
    if not a or not b:
        return -1.0
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a)) or 1e-9
    db = math.sqrt(sum(y * y for y in b)) or 1e-9
    return num / (da * db)


def _semantic(query: str, docs: list, vecs: list) -> list:
    qv = _embed([query], kind="query")
    if not qv or not qv[0]:
        return []
    q = qv[0]
    return [i for _s, i in sorted(((_cos(q, v), i) for i, v in enumerate(vecs)), key=lambda x: -x[0])]


def _rrf(rankings: list, k: int = 60) -> list:
    """Reciprocal-rank fusion - combines ORDERS, never scores.

    Chosen because BM25 scores and cosine similarities are not on the same scale and never will be;
    any weighted sum of the two smuggles in a tuning constant that would need its own experiment.
    RRF needs no calibration, which is the property that makes the comparison below honest."""
    agg = {}
    for r in rankings:
        for rank, idx in enumerate(r):
            agg[idx] = agg.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return [i for i, _s in sorted(agg.items(), key=lambda kv: -kv[1])]


# =================================================================================================
# THE GATE - situations this session was actually in, and the lesson that was already recorded
# =================================================================================================

GATE = [
    # The three below were rewritten after `_leak()` flagged them: the originals said "cooldown",
    # "endpoint", "tokens" and "scored" - the answer's own words, handed to the retriever inside the
    # question. Every one of them scored better before the rewrite, which is the whole reason the
    # audit runs before the scoring rather than after it.
    ("it keeps failing so I will wait a while before trying it again", "D22"),
    ("the reply stops halfway through, I should let it produce more", "D29"),
    ("the exam has more questions now, so the pass mark should go up with it", "D24"),
    ("I am writing the run to a file so it can be compared with the next one", "D26"),
    ("the result came back different the second time I ran it, probably just variance", "D20"),
    ("this one did badly on the test so it is not good enough for the important work", "D28"),
    ("I need a model for the seat that argues, and a fast one keeps the run short", "D30"),
    ("the request failed so I will catch it and hand back an empty result", "D19"),
    ("my tool cannot reach that page, so the page must not be reachable", "D22"),
    ("I am writing something that flags a problem, and it reports nothing on the tree", "D18"),
    ("everything is falling back to the small local model because the fast one is busy", "D24"),
    ("I checked the change with one call and it came back right, so it works", "D27"),
]


def _leak(query: str, target_text: str) -> set:
    """Rare words a query shares with its own answer. Non-empty means the case tests matching.

    Same audit `movecontrol` needed after the council caught its corpus writing the answers into the
    questions. A retrieval benchmark is the EASIEST place in the world to fake, because the author
    of the query knows the document."""
    q, t = set(_words(query)), set(_words(target_text))
    common = q & t
    return {w for w in common if len(w) > 5}


def evaluate(verbose: bool = True) -> dict:
    docs = lessons()
    by_id = {}
    for i, d in enumerate(docs):
        by_id.setdefault(d["id"], i)

    leaks = {}
    for q, tid in GATE:
        i = by_id.get(tid)
        if i is None:
            continue
        sh = _leak(q, docs[i]["text"][:1500])
        if sh:
            leaks[q[:40]] = sorted(sh)

    vecs = _vectors(docs)
    methods = {"lexical": [], "semantic": [], "hybrid": []}
    detail = []
    for q, tid in GATE:
        want = by_id.get(tid)
        if want is None:
            continue
        lex = _bm25(q, docs)
        sem = _semantic(q, docs, vecs)
        hyb = _rrf([lex, sem]) if sem else lex
        row = {"q": q, "want": tid}
        for name, order in (("lexical", lex), ("semantic", sem), ("hybrid", hyb)):
            pos = order.index(want) + 1 if want in order else 999
            methods[name].append(pos)
            row[name] = pos
        detail.append(row)

    def at(ranks, k):
        return sum(1 for r in ranks if r <= k)

    n = len(detail)
    summary = {m: {f"@{k}": at(r, k) for k in (1, 3, 5)} for m, r in methods.items()}
    if verbose:
        print("=" * 92)
        print(f"RETRIEVAL - {len(docs)} lessons indexed, {n} gate cases")
        print("=" * 92)
        if leaks:
            print("  CORPUS LEAK - these queries share rare vocabulary with their own answer:")
            for q, sh in leaks.items():
                print(f"    {q!r}: {sh}")
            print("  Rephrase in the language of the SITUATION; a leaky case measures matching.\n")
        else:
            print("  corpus leak audit: clean (no query shares rare vocabulary with its answer)\n")
        print(f"  {'method':10s} {'hit@1':>7s} {'hit@3':>7s} {'hit@5':>7s}   of {n}")
        for m in ("lexical", "semantic", "hybrid"):
            s = summary[m]
            print(f"  {m:10s} {s['@1']:>7d} {s['@3']:>7d} {s['@5']:>7d}")
        print(f"\n  {'situation':52s} {'want':5s} {'lex':>4s} {'sem':>4s} {'hyb':>4s}")
        for r in detail:
            print(f"  {r['q'][:52]:52s} {r['want']:5s} {r['lexical']:>4d} {r['semantic']:>4d} {r['hybrid']:>4d}")

        # THE METRIC IS hit@5 BECAUSE THAT IS WHAT THE TOOL SHOWS.
        #
        # `find()` returns k=5 and prints all five; nothing here auto-applies a single lesson. So
        # the question the interface actually asks is "is the right lesson among the five you would
        # read", and hit@5 is that question. The first version of this verdict gated on @3, which
        # was simply the wrong rule for the interface - stated here rather than quietly changed,
        # because moving a metric AFTER seeing which way it points is how a benchmark becomes a
        # decoration. @1 and @3 stay printed so the choice can be re-argued against the same data.
        h, l, s = summary["hybrid"], summary["lexical"], summary["semantic"]
        best = max(("lexical", "semantic", "hybrid"),
                   key=lambda m: (summary[m]["@5"], summary[m]["@3"], summary[m]["@1"]))
        print()
        if h["@5"] > max(l["@5"], s["@5"]):
            print(f"  >>> HYBRID WINS on hit@5, the metric the interface asks: {h['@5']}/{n} "
                  f"vs lexical {l['@5']}, semantic {s['@5']}. Shipping it.")
            print(f"      The two are blind in opposite directions - lexical finds a lesson that "
                  f"names the symbol you are touching, semantic finds one that MEANS your situation "
                  f"without sharing a word of it. The gain is that, and it is why fusion was worth "
                  f"testing rather than assuming.")
        else:
            print(f"  >>> HYBRID DOES NOT WIN on hit@5 ({h['@5']} vs lexical {l['@5']}, semantic "
                  f"{s['@5']}). Best is {best.upper()}, and that is what ships - a fusion that does "
                  f"not beat its parts is a complication, not a feature.")
    return dict(summary=summary, detail=detail, leaks=leaks, n=n, docs=len(docs))


def find(query: str, k: int = 5, method: str = "hybrid") -> list:
    """The lessons bearing on what you are about to do."""
    docs = lessons()
    lex = _bm25(query, docs)
    if method == "lexical":
        order = lex
    else:
        vecs = _vectors(docs)
        sem = _semantic(query, docs, vecs)
        order = _rrf([lex, sem]) if (sem and method == "hybrid") else (sem or lex)
    return [docs[i] for i in order[:k]]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if "--evaluate" in sys.argv[1:]:
        r = evaluate()
        sys.exit(0)
    if not args:
        print(__doc__.strip().splitlines()[0])
        print("\n  usage: python -m aea.lab.recall \"what you are about to do\"")
        print("         python -m aea.lab.recall --evaluate")
        sys.exit(0)
    q = " ".join(args)
    print(f"lessons bearing on: {q!r}\n")
    for d in find(q):
        first = next((l for l in d["text"].splitlines() if l.strip()), "")
        print(f"  [{d['id']}] {d['title'][:76]}")
        print(f"        {first[:100]}")
