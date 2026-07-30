# THE SENSES MAP - what this entity could perceive with, and what it actually reaches

*2026-07-30. Luis: "we have gone to that website many times yet we don't have a list of the web's
content and structure... This is about adding senses, vision, OCR."*

*He is right that we had never mapped it. Everything the entity perceives today is TEXT: its own
state, headlines, and speech that whisper already turned into text. It has never seen an image,
never read a scanned page, never retrieved by meaning.*

*Survey: `python -m aea.tooling.senses [--probe]`. Re-runnable, saves `state/senses.json`.*

---

## 1 - WHAT IS SERVED, BY SENSE

**102 models served to this key.** Classified by what SENSE each would give rather than by vendor
taxonomy, because the question is not what NVIDIA sells but what this thing can be given.

| sense | available | wired today |
|---|---|---|
| **SIGHT** | **7** | **NOTHING** |
| **READING (OCR)** | **1** | **NOTHING** |
| **RECALL (embeddings)** | **11** | **NOTHING** |
| **SAFETY (guard models)** | **5** | **NOTHING** |
| BODY (code) | 4 | NOTHING |
| UNDERSTANDING | 74 | 3 tiers (8B / 49B / 550B) |
| HEARING | 0 here | whisper-base, local |
| VOICE | 0 here | edge-tts, network |

HEARING and VOICE returning zero **confirms** the earlier finding rather than contradicting it:
NVIDIA serves no ASR or TTS on this REST path, which is why the ear and the mouth are local and
network-TTS respectively. That was measured before and it still holds.

---

## 2 - THE PROBE. A CATALOGUE ENTRY IS NOT ACCESS.

One call per sense, at the correct door for that modality, reading the RESPONSE BODY - which is
where the answer actually was:

```
SIGHT           meta/llama-3.2-11b-vision-instruct   /chat/completions   REACHABLE  0.5s
READING (OCR)   nvidia/nemoretriever-parse           /chat/completions   HTTP 400   0.3s
                "Content cannot be a plain string. The model does not support text input."
RECALL (embed)  baai/bge-m3                          /embeddings         HTTP 500   0.3s
                "Something went wrong with the request."
SAFETY          meta/llama-guard-4-12b               /chat/completions   HTTP 0     60.2s (timeout)
UNDERSTANDING   01-ai/yi-large                       /chat/completions   HTTP 404   0.3s
                "Function '23bd454d-...': Not found"
BODY (code)     bigcode/starcoder2-15b               /chat/completions   HTTP 404   0.2s
```

**Read those as four different results, not one column of failures:**

- **SIGHT is available right now.** 200 in half a second. The entity can be given eyes today.
- **OCR is ALIVE and the 400 is the useful part** - it is telling us exactly how to call it. Not a
  failure; an instruction.
- **RECALL is a 500, not a 404** - the door is right and the request shape is wrong. One call away.
- **The 404s are genuinely retired.** "Function ...: Not found" is the endpoint saying the model
  is listed and gone - the exact page-versus-endpoint disagreement this survey exists to catch.

---

## 3 - THE INSTRUMENT WAS WRONG FIRST, AGAIN

The first probe sent every model to `/chat/completions` and reported `bge-m3` as **404 - not
served**. It is served. I knocked on the wrong door: an embedding model speaks `/embeddings` and a
reranker speaks `/ranking`.

That is this module's own headline lesson - **ask the live thing** - failing inside the module that
quotes it, because "the live thing" is not one endpoint. **It is one endpoint per modality.** For
about a minute a whole sense was written off on my own bad call.

The fix is in `_DOOR`, and reading the error BODY is what made the rest legible: without it, "wrong
door" and "no such model" are both a bare 404.

---

## 4 - WHAT THIS CHANGES, RANKED

**1 · RECALL is the highest-value missing sense, and the code already says so.** `decide.py` and
`persona.py` both carry the same admission: relevance is LEXICAL, so the entity remembers *words,
not meanings* - a memory about "lying" will never surface for a turn about "dishonesty".
`persona._relevance` is named in its own docstring as "the one function to replace when an embedder
lands". **Eleven embedders are available and the replacement is one working request away.**

**2 · SAFETY guards are the missing half of the fence.** `hands.fence()` labels tool output as
untrusted and explicitly does not sanitise it, because a filter that half-works is worse than a
label. `llama-3.1-nemoguard-8b-content-safety` and `-topic-control` are classifiers built for
exactly that gap - they can *judge* returned text rather than trusting or mangling it. That is the
honest completion of the R2 output problem.

**3 · SIGHT is reachable and has no job yet.** Real, and worth naming carefully: an entity that can
see but has nothing to look at has gained a capability, not a sense. It becomes a sense when
something in the loop needs to look. Do not wire it before that exists.

**4 · OCR waits on sight.** Same argument, one step further out.

---

## 5 - THE SITE, HONESTLY

`build.nvidia.com` returns 200 and ~380KB to a plain urllib GET with a desktop User-Agent - the
recorded lesson holds, and `WebFetch` still times out on it.

**But the extraction is thin and that is reported rather than dressed up:** 25-26 slugs per page and
zero names, because the catalogue is client-rendered and only the initial payload is server-side.
Real blueprint slugs did come through - `nvidia/aiq`, `ambient-healthcare-agents`,
`content-localization`, `ai-model-distillation-for-financial-data`,
`build-your-own-transaction-foundation-model` - and the explore taxonomy
(`automotive`, `biology`, `climate-weather`, `financial-services`).

**A full blueprint inventory needs their API, not their HTML.** Recorded as unfinished; a survey
that pretends to have found things is worse than one that says it found nothing.

---

## 6 - THE RULE THIS SURVEY EARNS

**A sense is not a model. A sense is a model plus a reason to use it.**

The catalogue has 102 models and the entity is short of exactly two things it can act on now: a way
to retrieve by meaning, and a way to judge what comes back through its tools. Both serve loops that
already exist and are already limited by their absence. Sight and OCR are real and should wait for
a loop that needs to look - otherwise they are 200-OK decorations.
