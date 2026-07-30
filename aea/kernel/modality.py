"""modality.py - ONE PROTOCOL PER KIND OF MODEL, instead of one protocol for all of them.

Luis, 2026-07-30: "why we don't have protocols established to interact with each type of model?"

Because there is only one, and it was treated as universal. `grid.call_openai` is CHAT-shaped -
`messages` in, `choices[0].message.content` out - and every call in this repo funnels through it.
That is fine for the 74 text models and wrong for everything else, and the cost was measured within
the hour:

    the senses probe sent `baai/bge-m3` to /chat/completions, got 404, and recorded a live
    embedding model as NOT SERVED. It is served. An embedding model speaks /embeddings.

A whole sense was written off because the caller knew one door. The lesson this repo already had -
ASK THE LIVE THING - turns out to be incomplete: the live thing is not one endpoint, it is ONE
ENDPOINT PER MODALITY, with its own request shape and its own place to find the answer.

WHAT A MODALITY IS, HERE. Four things, and a model type is not usable until all four are written
down:
    door     the path on the plant's base url
    build    the request body for THIS model type
    read     where the answer lives in the response - `choices[0].message.content` is a CHAT
             convention, not an API one; embeddings answer at `data[0].embedding`
    verify   what a good answer looks like, so a 200 with junk in it is not counted as success

THE FOURTH IS THE ONE THAT MATTERS AND THE ONE EVERY CLIENT SKIPS. A 200 is not a result. An
embedding endpoint that returns an empty vector, or a classifier that returns a label outside its
own label set, has answered without answering - and every layer above will treat it as fact.

WHAT IS DELIBERATELY NOT HERE: any write, any send, any spend. This module only knows how to ASK
things. See `hands.py` for what is permitted to run at all; this is the transport underneath it.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from aea.kernel import grid

UA = "aea-modality/1"

# HOW LONG TO WAIT. A generous INACTIVITY budget, never `None` - a rod that thinks for minutes must
# survive, and a peer that stops sending without closing must not hang the run forever. This repo
# has already paid 28 and 64 minutes for that distinction.
TIMEOUT = 120


class Bad(Exception):
    """The transport answered, and the answer was not usable. Distinct from a network failure on
    purpose: 'it did not reply' and 'it replied with junk' need different responses, and collapsing
    them is how a junk answer becomes a stored fact."""


def _post(plant: str, door: str, body: dict, timeout: int = TIMEOUT) -> dict:
    p = grid.PLANTS[plant]
    key = os.environ.get(p["auth"] or "", "")
    req = urllib.request.Request(
        p["base"] + door, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA,
                 **({"Authorization": f"Bearer {key}"} if key else {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        # THE BODY OF A 4xx IS THE ANSWER. Measured on the senses probe: a bare 400 from
        # nemoretriever-parse is indistinguishable from a dead model, while its BODY said
        # "Content cannot be a plain string. The model does not support text input" - which is
        # not a failure at all, it is the API telling you how to call it.
        detail = ""
        try:
            detail = e.read().decode("utf-8", "ignore")[:300]
        except Exception:
            pass
        raise Bad(f"HTTP {e.code} at {door}: {detail or e.reason}")
    except Exception as e:
        raise Bad(f"{type(e).__name__} at {door}: {str(e)[:140]}")


# ---------------------------------------------------------------------------------- the modalities

def understand(model: str, prompt: str, plant: str = "nvidia", max_tokens: int = 256) -> str:
    """TEXT IN, TEXT OUT. The one we already had, restated here so every modality is described in
    the same place and none of them is the implicit default."""
    d = _post(plant, "/chat/completions",
              {"model": model, "max_tokens": max_tokens,
               "messages": [{"role": "user", "content": prompt}]})
    try:
        m = d["choices"][0]["message"]
        out = (m.get("content") or m.get("reasoning_content") or "").strip()
    except Exception as e:
        raise Bad(f"chat response had no content: {str(e)[:80]}")
    if not out:
        raise Bad("chat returned an empty answer (a reasoning rod can spend its whole budget "
                  "thinking - give it more tokens or switch thinking off)")
    return out


def recall(model: str, texts, plant: str = "nvidia", kind: str = "query") -> list:
    """RECALL - text in, VECTORS out. The sense the entity most needs and does not have.

    `persona._relevance` and `decide` both admit in their own docstrings that matching is LEXICAL,
    so the entity remembers WORDS and not MEANINGS - a memory about "lying" never surfaces for a
    turn about "dishonesty". This is the door to fixing that.

    `kind` is NVIDIA's asymmetric-embedding flag: a stored passage and a live query are embedded
    DIFFERENTLY by these models, and using the wrong one silently degrades every comparison. It is
    a required field here rather than an optional one for exactly that reason."""
    if isinstance(texts, str):
        texts = [texts]
    if not texts or not all(isinstance(t, str) and t.strip() for t in texts):
        raise Bad("recall needs at least one non-empty string")
    if kind not in ("query", "passage"):
        raise Bad("kind must be 'query' or 'passage' - see the note on asymmetric embedding")
    d = _post(plant, "/embeddings",
              {"model": model, "input": list(texts), "input_type": kind,
               "encoding_format": "float", "truncate": "END"})
    try:
        vecs = [row["embedding"] for row in d["data"]]
    except Exception as e:
        raise Bad(f"embedding response had no data: {str(e)[:80]}")
    # VERIFY, because a 200 is not a result: right count, non-empty, consistent width, and not all
    # zeros - a zero vector scores identically against everything and would quietly make retrieval
    # return whatever happened to be first.
    if len(vecs) != len(texts):
        raise Bad(f"asked for {len(texts)} vectors, got {len(vecs)}")
    if not vecs or not vecs[0]:
        raise Bad("embedding returned an empty vector")
    w = len(vecs[0])
    if any(len(v) != w for v in vecs):
        raise Bad("embedding widths differ between inputs")
    if all(abs(x) < 1e-12 for x in vecs[0]):
        raise Bad("embedding is all zeros - it would match everything equally")
    return vecs


def rank(model: str, query: str, passages: list, plant: str = "nvidia") -> list:
    """RERANK - a query and candidates in, an ORDER out. The second half of recall: embeddings find
    a neighbourhood cheaply, a reranker reads the shortlist properly."""
    if not query.strip() or not passages:
        raise Bad("rank needs a query and at least one passage")
    d = _post(plant, "/ranking",
              {"model": model, "query": {"text": query},
               "passages": [{"text": str(p)} for p in passages]})
    try:
        out = [(int(r["index"]), float(r["logit"])) for r in d["rankings"]]
    except Exception as e:
        raise Bad(f"ranking response was not usable: {str(e)[:80]}")
    if len(out) != len(passages):
        raise Bad(f"ranked {len(out)} of {len(passages)} passages")
    if any(i < 0 or i >= len(passages) for i, _ in out):
        raise Bad("ranking returned an index outside the passage list")
    return out


def see(model: str, prompt: str, image_b64: str, plant: str = "nvidia",
        mime: str = "image/png", max_tokens: int = 256) -> str:
    """SIGHT - an image and a question in, text out. Measured reachable:
    `meta/llama-3.2-11b-vision-instruct` answered in 0.5s.

    The image goes in as a content BLOCK, not as a string - which is precisely what
    `nemoretriever-parse` was saying with its 400: "Content cannot be a plain string. The model
    does not support text input." That error was an instruction and it is encoded here."""
    if not image_b64:
        raise Bad("see needs a base64 image")
    d = _post(plant, "/chat/completions",
              {"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": [
                  {"type": "text", "text": prompt},
                  {"type": "image_url",
                   "image_url": {"url": f"data:{mime};base64,{image_b64}"}}]}]})
    try:
        out = (d["choices"][0]["message"].get("content") or "").strip()
    except Exception as e:
        raise Bad(f"vision response had no content: {str(e)[:80]}")
    if not out:
        raise Bad("vision returned an empty answer")
    return out


def judge(model: str, text: str, plant: str = "nvidia", labels=("safe", "unsafe")) -> dict:
    """JUDGE - text in, a LABEL out. The missing half of `hands.fence`.

    The fence labels tool output as untrusted and explicitly does not sanitise it, because a filter
    that half-works is worse than a label. A guard model is the honest completion: it does not
    mangle the text, it renders a verdict ON the text, and the verdict is a separate value that
    cannot be confused with the content.

    VERIFIED AGAINST ITS OWN LABEL SET. A classifier that answers outside its labels has not
    classified - and 'unparseable' is returned as exactly that rather than defaulting to safe,
    because a guard that fails open is not a guard."""
    out = understand(model, text, plant=plant, max_tokens=32).strip().lower()
    hit = [l for l in labels if l.lower() in out]
    if len(hit) != 1:
        return dict(label=None, raw=out[:120],
                    why=f"answer did not name exactly one of {list(labels)}")
    return dict(label=hit[0], raw=out[:120], why="")


# The registry, so a caller can ask WHAT KINDS EXIST rather than knowing them. This is the thing
# that did not exist an hour ago and whose absence cost a sense.
MODALITIES = {
    "understand": dict(door="/chat/completions", fn=understand,
                       desc="text in, text out - the default everything used to assume"),
    "recall":     dict(door="/embeddings", fn=recall,
                       desc="text in, vectors out - retrieval by meaning"),
    "rank":       dict(door="/ranking", fn=rank,
                       desc="query + candidates in, an order out"),
    "see":        dict(door="/chat/completions", fn=see,
                       desc="image + question in, text out - content BLOCKS, not a string"),
    "judge":      dict(door="/chat/completions", fn=judge,
                       desc="text in, a label from a closed set out"),
}


def doors() -> dict:
    """Which door each modality knocks on. The map whose absence made a live model look dead."""
    return {k: v["door"] for k, v in MODALITIES.items()}
