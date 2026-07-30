"""toolkinds.py - THE GRID. What a tool IS, on the two axes that actually matter.

Luis, 2026-07-30, correcting a taxonomy I got wrong: "you stated compute, read local, read remote,
perceive, recall, judge, write local, write remote, compose, execute. But I'm missing OCR, image
identification, image to text, video to text, audio to text... what about image generation models?
We need to be multimodal in terms of inputs. And being able to call an external service that is not
ours, being able to scrape the web, going to free APIs like the NASA exoplanet archive."

HE IS RIGHT AND THE ERROR IS STRUCTURAL. I listed ten types on ONE axis - what a tool does to the
world - and then quietly buried every modality inside one of them ("perceive"). That hides the
thing `modality.py` had just finished proving: `recall` and `understand` have the SAME effect on
the world (they read, they change nothing) and completely DIFFERENT protocols. One knocks on
/embeddings and answers at data[0].embedding; the other knocks on /chat/completions and answers at
choices[0].message.content. Collapsing them is exactly the mistake that made a live embedder look
dead.

So a tool is a CELL IN A GRID, not an item in a list:

    EFFECT  what it does to the world      -> decides PERMISSION (zone, capability, ceiling)
    SHAPE   what data goes in and comes out -> decides PROTOCOL (door, build, read, verify)

Two tools with the same EFFECT and different SHAPE need different code and the same gate.
Two tools with the same SHAPE and different EFFECT need the same code and different gates.
Every bug in this area so far has come from conflating one with the other.

WHY THE GRID IS THE SCHEMA-FOR-SCHEMAS. Luis also asked for "a tool generator, with schemas for
each type, and the ability to create new schemas for new types". A new type is a new CELL. Declaring
one means answering six questions - and if any is unanswerable, the tool is not ready to exist:

    door     where the request goes
    build    how the request body is shaped from the arguments
    read     where in the response the answer actually lives
    verify   what a GOOD answer looks like, so a 200 with junk in it is not counted as success
    gate     the zone and capability it runs under
    record   what gets written down about the run, so it can be judged and improved later

`verify` and `record` are the two everyone skips, and they are the two that make CREATE ->
REMEMBER -> IMPROVE possible at all. A tool with no verify cannot be judged; a tool with no record
cannot be improved. Everything else is plumbing.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------------------- AXIS 1
# WHAT IT DOES TO THE WORLD. This axis decides what may run and under whose permission. It is
# ordered by how much damage the worst case does, which is also the order the trust ladder climbs.
EFFECTS = {
    "compute":      dict(risk=0, note="pure and deterministic; no side effect, no network. calc."),
    "read_self":    dict(risk=1, note="its own state and structure. Local, no egress."),
    "perceive":     dict(risk=1, note="turn non-text INTO text. Local or hosted, no egress of "
                                      "anything the caller did not already hold."),
    "recall":       dict(risk=1, note="retrieve by meaning over its OWN store."),
    "judge":        dict(risk=1, note="classify or verify a value. Returns a verdict, never the "
                                      "content - which is what makes it composable with a fence."),
    "read_world":   dict(risk=2, note="fetch from outside. THE MODEL WRITES THE ADDRESS, so the "
                                      "request itself is an outbound channel (law B3)."),
    "call_service": dict(risk=2, note="a third party's API with its own schema, auth and quota. "
                                      "Read-shaped, but someone else's contract and someone "
                                      "else's uptime."),
    "generate":     dict(risk=2, note="make an artifact - image, audio, video. Produces a FILE, "
                                      "which is a write to local storage even when nothing is sent."),
    "write_self":   dict(risk=3, note="change its own state or files."),
    "write_world":  dict(risk=4, note="email, spend, publish. Irreversible outside this machine."),
    "compose":      dict(risk=3, note="define a NEW tool from existing primitives. No new code - "
                                      "see the note at the bottom of this file."),
    "execute":      dict(risk=5, note="run code it wrote. The top of the ladder; not scoped."),
}

# ---------------------------------------------------------------------------------------- AXIS 2
# WHAT SHAPE THE DATA IS. This axis decides the protocol - and this is the axis I omitted, which is
# why OCR, video-to-text and image generation all vanished into the word "perceive".
#
# `have` is honest about this machine, today: what is WIRED, not what is reachable.
SHAPES = {
    "text->text":     dict(door="/chat/completions", have="3 tiers wired (8B/49B/550B)"),
    "text->vector":   dict(door="/embeddings",       have="nv-embedqa-e5-v5, LIVE (1024d)"),
    "query+docs->order": dict(door="/ranking",       have="available, unwired"),
    "text->label":    dict(door="/chat/completions", have="5 guard models available, unwired"),
    "image->text":    dict(door="/chat/completions", have="llama-3.2-11b-vision REACHABLE, unwired"),
    "scan->text":     dict(door="/chat/completions", have="nemoretriever-parse alive, unwired"),
    "audio->text":    dict(door="local",             have="whisper-base, WIRED"),
    "text->audio":    dict(door="network",           have="edge-tts, WIRED"),
    "video->text":    dict(door="?",                 have="NOTHING - see the note below"),
    "text->image":    dict(door="?",                 have="NOTHING - deliberately deferred"),
    "url->text":      dict(door="http",              have="web_fetch, WIRED"),
    "query->results": dict(door="http",              have="web_search, WIRED"),
    "params->json":   dict(door="http",              have="json_get, WIRED - the shape every "
                                                          "third-party API already speaks"),
}

# ---------------------------------------------------------------------------------------- THE GRID
# A tool is (effect, shape). This is not every legal pair - it is the ones worth naming, with an
# honest status. `status` is one of:
#     WIRED     the entity can use it today
#     LIVE      the protocol works and nothing calls it yet
#     REACHABLE measured to answer, no protocol written
#     OPEN      nothing found or nothing tried
KINDS = {
    # what exists
    "arithmetic":     ("compute",      "text->text",        "WIRED",     "calc"),
    "introspect":     ("read_self",    "text->text",        "WIRED",     "self_map, list_tools"),
    "read_own_state": ("read_self",    "text->text",        "WIRED",     "read_state"),
    "fetch_page":     ("read_world",   "url->text",         "WIRED",     "web_fetch"),
    "search":         ("read_world",   "query->results",    "WIRED",     "web_search"),
    "hear":           ("perceive",     "audio->text",       "WIRED",     "whisper, local"),
    "speak":          ("generate",     "text->audio",       "WIRED",     "edge-tts"),
    # the sense that just landed
    "embed":          ("recall",       "text->vector",      "LIVE",      "nv-embedqa-e5-v5"),
    # measured to answer, no protocol yet
    "see":            ("perceive",     "image->text",       "REACHABLE", "llama-3.2-11b-vision"),
    "read_scan":      ("perceive",     "scan->text",        "REACHABLE", "nemoretriever-parse"),
    "rerank":         ("recall",       "query+docs->order", "REACHABLE", "ranking endpoint"),
    "guard":          ("judge",        "text->label",       "REACHABLE", "nemoguard x2"),
    # named, nothing found or nothing tried
    "watch":          ("perceive",     "video->text",       "OPEN",      "no video model surveyed"),
    "draw":           ("generate",     "text->image",       "OPEN",      "deferred by Luis"),
    "third_party":    ("call_service", "params->json",      "OPEN",      "NASA exoplanets, etc"),
    "scrape":         ("read_world",   "url->text",         "OPEN",      "fetch exists; parsing "
                                                                         "structure does not"),
    # the dangerous column, all absent on purpose
    "write_file":     ("write_self",   "text->text",        "OPEN",      "none"),
    "send":           ("write_world",  "text->text",        "OPEN",      "impl=None, ceiling 0"),
    "spend":          ("write_world",  "text->text",        "OPEN",      "impl=None, ceiling 0"),
    "make_tool":      ("compose",      "text->text",        "OPEN",      "see the note below"),
    "run_code":       ("execute",      "text->text",        "OPEN",      "not scoped"),
}


def grid() -> dict:
    """Everything, grouped by effect, so the permission story reads down one column."""
    out = {}
    for name, (eff, shape, status, note) in KINDS.items():
        out.setdefault(eff, []).append(dict(kind=name, shape=shape, status=status, note=note))
    return out


def missing(status: str = "OPEN") -> list:
    return sorted(k for k, v in KINDS.items() if v[2] == status)


def report() -> str:
    L = ["THE TOOL GRID - effect (permission) x shape (protocol)", "=" * 92]
    by = grid()
    for eff in EFFECTS:
        rows = by.get(eff) or []
        if not rows:
            continue
        L.append(f"\n  {eff.upper():13s} risk {EFFECTS[eff]['risk']}   {EFFECTS[eff]['note'][:62]}")
        for r in rows:
            L.append(f"      {r['status']:10s} {r['kind']:16s} {r['shape']:20s} {r['note'][:34]}")
    n = {s: sum(1 for v in KINDS.values() if v[2] == s)
         for s in ("WIRED", "LIVE", "REACHABLE", "OPEN")}
    L.append("\n" + "=" * 92)
    L.append(f"  WIRED {n['WIRED']}   LIVE {n['LIVE']}   REACHABLE {n['REACHABLE']}   "
             f"OPEN {n['OPEN']}   of {len(KINDS)} named kinds")
    return "\n".join(L)


# -------------------------------------------------------------------------------------------------
# THE LINE ON `compose` AND `execute`, written here because this is where someone will come looking.
#
# A GENERATED TOOL MUST BE A COMPOSITION OF ALREADY-PERMITTED PRIMITIVES PLUS A SCHEMA. NEVER NEW
# CODE.
#
# `compose` (risk 3) and `execute` (risk 5) are two rungs apart and it is tempting to treat them as
# one feature, because "the entity writes its own tools" sounds like a single idea. It is not. A
# composer that emits a declarative spec - this door, these arguments, this verify, this gate - can
# be validated before it runs, refused by the existing gate, and demoted by the existing ledger. A
# composer that emits PYTHON is self-modification with a friendlier name, and it would arrive with
# none of self-modification's gates.
#
# The practical shape, when it is built: a new tool is a JSON object naming an existing modality, an
# existing capability, arguments drawn from declared types, and a verify condition. It starts at
# DRAFT like every other capability, and it earns WATCHED by running clean - which is the same
# ladder, not a new one. Nothing about it needs an eval().
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(report())
    print(f"\n  OPEN kinds, in the order their dependencies allow:")
    print("     guard      -> completes hands.fence (judge without mangling)")
    print("     rerank     -> completes recall (embed finds, rerank reads)")
    print("     third_party-> params->json already WIRED; needs a schema per service")
    print("     see/read_scan -> reachable, but wait for a loop that needs to look")
    print("     watch/draw -> nothing surveyed; draw deliberately deferred")
