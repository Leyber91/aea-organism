"""senses.py - WHAT CAN THIS ENTITY BE GIVEN TO PERCEIVE WITH. A survey of the catalogue.

Luis, 2026-07-30: "if you go to nvidia there is a place for skills and blueprints, we have gone to
that website many times yet we don't have a list of the web's content and structure... This is
about adding senses, vision, OCR."

He is right that we have been there repeatedly and never mapped it. Everything the entity currently
perceives is TEXT: it reads its own state, it reads headlines, it hears speech that whisper has
already turned into text. It has never seen an image, never read a scanned page, never retrieved by
meaning. Those are senses, and the catalogue is full of them.

TWO RECORDED LESSONS SHAPE HOW THIS ASKS:

  DROP TO THE PRIMITIVE.  `WebFetch` timed out twice on build.nvidia.com and it was nearly recorded
  as "the page cannot be read". A plain urllib GET with a desktop User-Agent returned 200 and 200KB.
  A convenience tool's limit is not the world's limit.

  ASK THE LIVE THING.  A catalogue page describes the product; `/v1/models` describes what is
  actually SERVED to this key. They disagree constantly - a model card can list a rod the endpoint
  404s, and a catalogue entry is not a served model. So the authoritative set is derived from the
  provider, not from a page or from memory.

WHAT THIS PRODUCES: `state/senses.json` and a printed map, classified by WHICH SENSE each model
would give - sight, reading, hearing, voice, recall - rather than by vendor taxonomy, because the
question is not "what does NVIDIA sell" but "what can this thing be given".

    python -m aea.tooling.senses              survey and print the map
    python -m aea.tooling.senses --probe      additionally CALL one model per sense to see if it
                                              answers this key (a catalogue entry is not access)
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(str(grid.STATE), "senses.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0 Safari/537.36")

# WHICH SENSE, keyed on what the model id and its family actually indicate. Ordered: the first
# match wins, so the more specific patterns come first. This is a closed vocabulary over a corpus
# (law M8) and it will be wrong at the edges - the point is a map, not a taxonomy.
SENSES = (
    ("READING (OCR)",  r"ocr|donut|nemoretriever[-_]?parse|paddle|textract|doc.?layout|table.?struct"),
    ("SIGHT",          r"vision|vlm|vila|llava|florence|paligemma|internvl|qwen.?2?.?5?.?vl|"
                       r"phi.?\d.?vision|cosmos|nvclip|clip|image|visual|sam\b|segment"),
    ("HEARING",        r"whisper|asr|riva.*(asr|speech)|parakeet|canary|conformer|stt"),
    ("VOICE",          r"\btts\b|fastpitch|hifigan|radtts|magpie|riva.*tts|speech.?synth"),
    ("RECALL (embed)", r"embed|e5|gte|bge|nv-embed|arctic|retriev(?!er[-_]?parse)|nomic"),
    ("RECALL (rerank)", r"rerank|ranking|cross.?encoder"),
    ("SAFETY",         r"guard|safety|shield|moderat|jailbreak|topic.?control"),
    ("BODY (code)",    r"coder|code.?llama|starcoder|deepseek.?coder|codestral|granite.?code"),
    ("UNDERSTANDING",  r".*"),                       # the fallback: ordinary text models
)


def _get(url: str, timeout: int = 30, token: str = "") -> tuple:
    """A raw GET with a desktop UA. Returns (status, body). Never raises - a survey that dies on
    one bad URL is a survey nobody finishes."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Accept": "*/*",
            **({"Authorization": f"Bearer {token}"} if token else {})})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except Exception as e:
        return 0, f"{type(e).__name__}: {str(e)[:120]}"


def served() -> tuple:
    """THE AUTHORITATIVE LIST: what this key can actually reach right now."""
    plant = grid.PLANTS["nvidia"]
    key = os.environ.get(plant["auth"]) or grid.env(plant["auth"]) if hasattr(grid, "env") \
        else os.environ.get(plant["auth"])
    if not key:
        return [], f"no {plant['auth']} in the environment - cannot ask the endpoint"
    st, body = _get(plant["base"] + "/models", token=key)
    if st != 200:
        return [], f"/v1/models returned {st}: {str(body)[:90]}"
    try:
        data = json.loads(body).get("data") or []
    except Exception as e:
        return [], f"/v1/models was not json: {str(e)[:60]}"
    return sorted({d.get("id", "") for d in data if d.get("id")}), ""


def sense_of(model_id: str) -> str:
    m = (model_id or "").lower()
    for name, pat in SENSES:
        if re.search(pat, m):
            return name
    return "UNDERSTANDING"


def catalogue() -> dict:
    """The public site, for the things the API does not list: blueprints and collections.

    Kept honest: this reads whatever the server renders and extracts what it can. If the page is a
    client-rendered shell the extraction will be thin, and THIN IS REPORTED rather than dressed up -
    a survey that pretends to have found things is worse than one that says it found nothing."""
    found = {}
    for label, url in (("blueprints", "https://build.nvidia.com/nim/blueprints"),
                       ("explore", "https://build.nvidia.com/explore/discover"),
                       ("models", "https://build.nvidia.com/models")):
        st, body = _get(url, timeout=25)
        if st != 200:
            found[label] = dict(status=st, note=str(body)[:110], items=[])
            continue
        # slugs of the form /vendor/model-name, which is how the site addresses everything
        slugs = sorted(set(re.findall(r'"/([a-z0-9][\w.-]{1,40}/[\w.-]{2,60})"', body)))
        titles = sorted(set(t.strip() for t in re.findall(r'"name"\s*:\s*"([^"]{3,70})"', body)))
        found[label] = dict(status=st, bytes=len(body), items=slugs[:400], titles=titles[:200])
    return found


# A SENSE HAS ITS OWN DOOR. An embedding model does not speak /chat/completions and a reranker does
# not either - asking them there returns 404, which reads exactly like "retired" and is not.
#
# MEASURED, first probe run: bge-m3 came back 404 and I had it written down as not-served for about
# a minute. It is served; I knocked on the wrong door. That is this module's own headline lesson -
# ASK THE LIVE THING - failing inside the module that quotes it, because "the live thing" is not one
# endpoint, it is one endpoint PER MODALITY.
_DOOR = {
    "RECALL (embed)":  ("/embeddings", lambda m: {"model": m, "input": ["ping"],
                                                  "input_type": "query", "encoding_format": "float"}),
    "RECALL (rerank)": ("/ranking", lambda m: {"model": m, "query": {"text": "ping"},
                                               "passages": [{"text": "pong"}]}),
}
_CHAT = ("/chat/completions", lambda m: {"model": m, "max_tokens": 8,
                                         "messages": [{"role": "user", "content": "ok?"}]})


def probe(ids: list, key: str, per_sense: int = 1) -> list:
    """A CATALOGUE ENTRY IS NOT ACCESS. Knock on the right door for each sense and record what
    this key actually gets. 200 = reachable. 404 at the CORRECT door = listed but not served."""
    out, seen = [], {}
    for mid in ids:
        s = sense_of(mid)
        if seen.get(s, 0) >= per_sense:
            continue
        seen[s] = seen.get(s, 0) + 1
        path, body = _DOOR.get(s, _CHAT)
        t0 = time.time()
        try:
            req = urllib.request.Request(
                grid.PLANTS["nvidia"]["base"] + path,
                data=json.dumps(body(mid)).encode(),
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                         "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                code, note = r.status, "answered"
        except Exception as e:
            code = getattr(e, "code", 0)
            note = str(getattr(e, "reason", e))[:70]
            # the body of a 4xx says WHY, and "wrong door" and "no such model" look identical
            # without it
            try:
                note = (e.read().decode("utf-8", "ignore")[:110] or note)
            except Exception:
                pass
        out.append(dict(sense=s, model=mid, door=path, status=code,
                        seconds=round(time.time() - t0, 1), note=note))
    return out


def run(do_probe: bool = False) -> dict:
    ids, why = served()
    print("=" * 100)
    print("THE SENSES SURVEY - what this entity could be given to perceive with")
    print("=" * 100)
    if why:
        print(f"  endpoint: {why}")
    print(f"  models SERVED to this key: {len(ids)}")

    by = {}
    for mid in ids:
        by.setdefault(sense_of(mid), []).append(mid)
    print()
    print(f"  {'sense':18s} {'n':>4}  examples")
    for name, _pat in SENSES:
        got = by.get(name) or []
        if not got:
            print(f"  {name:18s} {0:4d}  -")
            continue
        print(f"  {name:18s} {len(got):4d}  " + ", ".join(x.rsplit('/', 1)[-1] for x in got[:3]))

    print()
    print("  WHAT THE ENTITY HAS TODAY, against that:")
    have = {"HEARING": "whisper-base, local", "VOICE": "edge-tts, network",
            "UNDERSTANDING": "3 tiers wired (8B/49B/550B)"}
    for name, _p in SENSES:
        n = len(by.get(name) or [])
        print(f"    {name:18s} available {n:4d}   wired: {have.get(name, 'NOTHING')}")

    cat = catalogue()
    print()
    print("  THE SITE (blueprints and collections the API does not list):")
    for label, d in cat.items():
        print(f"    {label:12s} http {d['status']}  {d.get('bytes', 0):>7} bytes  "
              f"{len(d.get('items') or [])} slugs, {len(d.get('titles') or [])} names")
        for s in (d.get("items") or [])[:6]:
            print(f"        {s}")

    probes = []
    if do_probe and ids:
        key = os.environ.get(grid.PLANTS["nvidia"]["auth"], "")
        print()
        print("  PROBE - a catalogue entry is not access:")
        probes = probe(ids, key)
        for p in probes:
            mark = "REACHABLE" if p["status"] == 200 else f"HTTP {p['status']}"
            print(f"    {p['sense']:18s} {p['model'][:40]:40s} {p['door']:20s} {mark:11s} "
                  f"{p['seconds']}s")
            if p["status"] != 200:
                print(f"        {str(p['note'])[:104]}")

    res = dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), served=len(ids), why=why,
               by_sense={k: v for k, v in by.items()}, catalogue=cat, probes=probes)
    grid.atomic_save_json(OUT, res)
    print(f"\n  -> {os.path.relpath(OUT, str(grid.ROOT))}")
    return res


if __name__ == "__main__":
    run(do_probe="--probe" in sys.argv)
