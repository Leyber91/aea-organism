"""battery.py - THE CONVERSATIONAL TEST BATTERY. Many real cases, run in batches, on the record.

Luis, 2026-07-29, going to bed: "generate a battery of tests... as real as possible, as many cases
as possible... do it in batches, correct and improve in the next batch... the more data the best,
so we can come up with a very formulated and elaborated case of all the test cases that will give
us lessons."

WHY BATCHES AND NOT ONE LONG RUN. A four-hour sweep that is wrong in its first ten minutes wastes
four hours - this project has already lost two experiments to exactly that (28 and 64 minutes on
one second of CPU each). Every suite here is separately runnable, writes its results as it goes,
and is cheap enough to re-run after a fix.

  python -m aea.lab.battery --fast          deterministic suites only: hundreds of cases, seconds
  python -m aea.lab.battery --audio         + the ear and prosody, on synthesised speech
  python -m aea.lab.battery --rods          + background review and full turns (spends real calls)
  python -m aea.lab.battery --all

Results land in state/lab/battery/<suite>.json and are rendered by `python -m aea.lab.battery
--report` into web/lab/battery.html.

EVERY CASE CARRIES ITS EXPECTED ANSWER, and the negatives matter more than the positives: a
detector that has only ever been shown things it should catch has not been tested, only run (D18).
Where a suite is asymmetric - a false cut is unrecoverable, a late take is merely slow - the two
error directions are counted SEPARATELY, because one combined accuracy hides the trade.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(str(grid.STATE), "lab", "battery")


def _save(name: str, rows: list, meta: dict) -> str:
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f"{name}.json")
    grid.atomic_save_json(p, {"suite": name, "at": time.strftime("%Y-%m-%d %H:%M"),
                              "meta": meta, "rows": rows})
    return p


def _report(name: str, rows: list) -> dict:
    ok = sum(1 for r in rows if r["ok"])
    return dict(suite=name, n=len(rows), pass_=ok, fail=len(rows) - ok,
                rate=round(ok / max(1, len(rows)), 3))


# =============================================================================================
# SUITE 1 - ENDPOINT. When has a person finished speaking?
# The two error directions are NOT symmetric and are counted apart: a FALSE CUT truncates someone
# mid-thought and cannot be undone; a LATE TAKE only makes them wait.
# =============================================================================================
COMPLETE = [
    "Run the test", "What is the capital of France", "Hey how is it going",
    "Can you check my heartbeat file", "Tell me something interesting", "Yes", "No thanks",
    "That sounds good to me", "I think we should try the other model",
    "What is 92837 times 4471", "Stop the server", "Open the file", "Read it back to me",
    "I had a rough day at work", "My name is Luis", "I live in Barcelona",
    "Can you search for the latest news", "How many modules do you have",
    "What can you actually do right now", "Show me the numbers",
    "The endpointer waits too long", "Let us try something different",
    "I want to understand how this works", "Does that make sense to you",
    "Why did it fail", "Tell me about the sea", "Check my email", "What time is it",
    "That is exactly what I meant", "Please do it again", "It worked",
    "I am not sure about that", "Give me the short version", "Explain it simply",
    "Are you still there", "Can you hear me", "Say that again",
    "What did you just do", "How long will it take", "I need a break",
]
INCOMPLETE = [
    "What is the capital of", "I was thinking that maybe we should", "Can you look at the",
    "So I wanted to ask you about", "I want to", "Show me my", "The problem is that the",
    "Could you please", "It seems like the", "When I try to", "My biggest issue is",
    "If we could just", "The reason I ask is because the", "I think the best way to",
    "Let me tell you about my", "What happens when the", "Do you know if the",
    "Before we start I need to", "The thing about it is", "One more thing about the",
    "And then after that we", "But the important part is", "Because of the",
    "Something I noticed in the", "Have you ever tried to", "It might be worth", "So",
    "Um", "And", "The", "Well I guess the", "Which means that the",
]

# SUITE 2 - TOOL PRE-FILTER. Which utterances plausibly need a tool.
TOOL_CASES = [
    # (text, expected tool names)
    ("What is 92837 times 4471", {"calc"}), ("Can you multiply 12 and 30", {"calc"}),
    ("Calculate 5 percent of 200", {"calc"}), ("What is 100 divided by 7", {"calc"}),
    ("compute 2 + 2", {"calc"}), ("what is 15 x 3", {"calc"}),
    ("What tools do you have", {"list_tools"}), ("What can you do", {"list_tools"}),
    ("What can you actually do right now", {"list_tools"}),
    ("what can you really do for me", {"list_tools"}),
    # BOTH IS CORRECT HERE, and the first version of this case was the test being wrong rather
    # than the code. "What are your capabilities" is legitimately about what it can DO
    # (list_tools) and what it IS (self_map); both are PREFETCH tools - local, free, no side
    # effects - so getting both costs a slightly longer injected context and gives the rod more
    # grounded fact to answer from. A test that encodes a preference as a requirement will make
    # someone "fix" working code later.
    ("What are your capabilities", {"list_tools", "self_map"}),
    ("List your tools", {"list_tools"}),
    ("Read your heartbeat file", {"read_state"}), ("Show me your state file", {"read_state"}),
    ("Search for the latest nemotron news", {"web_search"}),
    ("Look up who won the world cup", {"web_search"}),
    ("What is the current price of copper", {"web_search"}),
    ("How are you built", {"self_map"}), ("How many modules do you have", {"self_map"}),
    ("What are your laws", {"list_tools", "self_map"}),
    ("Tell me your architecture", {"self_map"}),
    ("Are you healthy", {"self_map"}),
    # NEGATIVES - the expensive direction. A spurious tool call costs a round trip and a
    # holding phrase on a turn that should have been instant.
    ("Hey how is it going", set()), ("I had a rough day at work", set()),
    ("Tell me something interesting", set()), ("What do you think about the sea", set()),
    ("Do you ever get tired", set()), ("That is funny", set()),
    ("I disagree with that", set()), ("Good morning", set()),
    ("What do you actually think about running a mind on a laptop", set()),
    ("My name is Luis and I live in Barcelona", set()),
    ("Thanks, that helps", set()), ("Can you say that again", set()),
    ("I am going to bed now", set()), ("Tell me a story", set()),
    ("How do you feel about that", set()),
]

# SUITE 3 - SPEECH CLEANING. What a rod emits that must never be spoken aloud.
SPEECH_CASES = [
    (["[heard: slower than usual] ", "That is a good point. ", "Second."],
     ["heard", "["], ["good point"], "prosody annotation leak"),
    (["Here's my response, adhering to the VOICE RULES:\n\n", "I am fine. ", "You?"],
     ["adhering", "RULES"], ["I am fine"], "meta preamble"),
    (["I will check. ", "*pause* ", "Done."], ["pause"], ["check"], "stage direction"),
    (["Hello. ", "*laughs* ", "Nice."], ["laughs"], ["Nice"], "stage direction laughs"),
    (["<thi", "nk>secret</thi", "nk>Real answer. ", "More."], ["secret", "think"],
     ["Real answer"], "think tag split across deltas"),
    (["<think>hidden reasoning here</think>", "Visible. ", "Yes."], ["hidden"], ["Visible"],
     "think tag whole"),
    (["Sure, here you go: ", "It works. ", "Great."], ["here you go"], ["It works"],
     "sure-here preamble"),
    (["**Bold** matters. ", "Yes."], ["**"], ["Bold"], "emphasis keeps its word"),
    (["That is *really* important. ", "Ok."], ["*"], ["really"], "single star emphasis"),
    (["Use `calc()` for that. ", "Ok."], ["`"], ["calc"], "backticks"),
    (["# Heading\n", "Then text. ", "End."], ["#"], ["Then text"], "markdown heading"),
    (["Okay: ", "Done here."], ["Okay:"], ["Done here"], "bare okay colon"),
    (["Here is the thing about the sea. ", "It is big."], [], ["Here is the thing"],
     "must NOT strip a real sentence starting with Here"),
    (["- item one\n", "- item two\n", "done"], ["-"], ["item one"], "list markers"),
    (["I think so.  ", "[note] ", "And more."], ["["], ["I think so"], "mid bracket"),
]

# SUITE 4 - MEMORY GATE. What may become a permanent fact about a person.
FACT_CASES = [
    ("His name is Luis", True), ("He lives in Barcelona", True),
    ("He works as an AI engineer", True), ("He is writing a science fiction series", True),
    ("He has <REDACTED-CIRCUMSTANCE>", True), ("He studied at 42", True), ("He prefers English", True),
    ("She is a nurse from Seville", True), ("He owns a laptop with an Ada GPU", True),
    ("He goes to bed late", True),
    # the REAL leaked reasoning, verbatim from the run that shipped it
    ("The user wants me to extract durable facts about the person from the conversation. "
     "The conversation shows them asking a math question", False),
    ("From the conversation: me: So, 92837 multiplied by 4471 equals 415,074,227", False),
    ("However, is that a fact stated by the person?", False),
    ("The instruction says to extract every durable fact", False),
    ("I need to look at what they said and decide", False),
    ("Let me analyze the conversation for facts", False),
    ("1. el: Que es eso? - No fact", False),
    ("NADA", False), ("NOTHING", False), ("", False), ("ok", False),
    ("The assistant calls the person Luis. That suggests the name is Luis. However", False),
    ("Extract all durable facts:", False),
]


def suite_endpoint() -> list:
    from aea.organs.converse import utterance_looks_complete as done
    rows = []
    for t in COMPLETE:
        got = done(t)
        rows.append(dict(case=t, want=True, got=got, ok=got is True,
                         err="late_take" if not got else ""))
    for t in INCOMPLETE:
        got = done(t)
        rows.append(dict(case=t, want=False, got=got, ok=got is False,
                         err="false_cut" if got else ""))
    return rows


def suite_prefilter() -> list:
    from aea.organs.converse import tools_for
    ALLOW = ("calc", "read_state", "list_tools", "self_map", "web_search", "web_fetch", "json_get")
    rows = []
    for text, want in TOOL_CASES:
        got = set(tools_for(text, ALLOW))
        # web_* are interchangeable for the search intent
        norm = lambda s: {"web_fetch": "web_search", "json_get": "web_search"}.get(s, s)
        g, w = {norm(x) for x in got}, {norm(x) for x in want}
        ok = g == w
        rows.append(dict(case=text, want=sorted(w), got=sorted(g), ok=ok,
                         err=("" if ok else ("spurious" if g - w else "missed"))))
    return rows


def suite_speech() -> list:
    from aea.organs.converse import speakable
    rows = []
    for deltas, must_go, must_stay, label in SPEECH_CASES:
        out = "".join(speakable(iter(deltas), max_sentences=3)).strip()
        leaked = [m for m in must_go if m in out]
        lost = [m for m in must_stay if m not in out]
        ok = not leaked and not lost
        rows.append(dict(case=label, got=out[:110], ok=ok,
                         err=("leaked:" + ",".join(leaked) if leaked else
                              "lost:" + ",".join(lost) if lost else "")))
    return rows


# SUITE 6 - THE ATTRIBUTION GUARD. The machine may not tell a person what they feel.
# Assertions are stripped; QUESTIONS survive, because a question invites correction and costs
# nothing when it is wrong. The MUST-KEEP half is the expensive direction: a guard that also
# deletes "that is a frustrating bug" has broken ordinary speech to prevent a rare harm.
ATTRIB_STRIP = [
    "You sound tired today.", "You seem stressed about this.", "You're upset, aren't you",
    "You must be frustrated with that.", "you sound a bit anxious.",
    "You are really angry right now.", "I can tell you are exhausted.",
    "It sounds like you are overwhelmed.", "I sense that you're uncomfortable with this.",
    "You seem quite down today.", "You look worried.",
    "You might be feeling anxious about it.", "You are getting frustrated.",
    "You sound so tired lately.", "I notice that you're upset.",
]
ATTRIB_KEEP = [
    "You sound quieter than usual, is everything alright?", "Are you tired?",
    "That is a frustrating bug.", "I do not have feelings, so I cannot be tired.",
    "The build failed and that is annoying.", "Do you want to talk about it?",
    "That sounds like a hard week.", "I am a machine, so nothing here is upset with anyone.",
    "The endpointer is slow and it is irritating to use.", "How are you doing today?",
    "Is something wrong?", "Was that a rough one?",
]


def suite_attribution() -> list:
    from aea.organs.converse import strip_attribution as strip
    rows = []
    for t in ATTRIB_STRIP:
        out = strip(t)
        ok = out.strip() != t.strip()
        rows.append(dict(case=t, got=out[:60], ok=ok, err="" if ok else "asserted_a_feeling"))
    for t in ATTRIB_KEEP:
        out = strip(t)
        ok = out.strip() == t.strip()
        rows.append(dict(case=t, got=out[:60], ok=ok, err="" if ok else "mangled_normal_speech"))
    return rows


def suite_facts() -> list:
    from aea.organs.converse import is_fact
    rows = []
    for text, want in FACT_CASES:
        got = is_fact(text)
        rows.append(dict(case=text[:80], want=want, got=got, ok=got == want,
                         err="" if got == want else ("false_memory" if got else "dropped_real")))
    return rows


FAST_SUITES = {"endpoint": suite_endpoint, "prefilter": suite_prefilter,
               "speech": suite_speech, "facts": suite_facts,
               "attribution": suite_attribution}


# =============================================================================================
# SUITE 5 - THE EAR, on synthesised speech with known text. OPTIMISTIC BOUND, stated once: a
# clean TTS voice is easier than a person across a room, and D13 recorded that the acoustic path
# was always the ceiling. This measures the MODEL, not the microphone.
# =============================================================================================
EAR_CASES = [
    "Run the test", "What is the capital of France", "Hey how is it going today",
    "Can you check my heartbeat file and tell me what is in it",
    "I was thinking that maybe we should try the other model instead",
    "Multiply ninety two thousand eight hundred and thirty seven by four thousand four hundred",
    "My name is Luis and I live in Barcelona", "Stop the server and restart it please",
    "How many modules do you have right now", "What are your laws",
    "Search the web for the latest nemotron benchmarks", "I had a really rough day at work today",
    "Could you read that back to me one more time", "The endpointer waits too long before replying",
    "Tell me something surprising about the ocean", "Are you still there",
    "What did you just do", "I am not sure that is correct",
    "Give me the short version please", "Open the file and show me the first ten lines",
]

PROSODY_SENTENCES = ["I really need you to do this now",
                     "That is not what I asked you for",
                     "Can you take a look at this"]
PROSODY_STYLES = [("neutral", {}), ("fast", {"rate": "+55%"}), ("slow", {"rate": "-40%"}),
                  ("high", {"pitch": "+50Hz"}), ("low", {"pitch": "-50Hz"}),
                  ("loud", {"volume": "+40%"}), ("quiet", {"volume": "-40%"})]


def _mk_wav(text: str, path: str, **kw) -> float:
    import asyncio
    import edge_tts
    mp3 = path.replace(".wav", ".mp3")
    if not os.path.exists(mp3):
        asyncio.run(edge_tts.Communicate(text, "en-US-AndrewMultilingualNeural", **kw).save(mp3))
    try:
        import numpy as np
        import soundfile as sf
        d, sr = sf.read(mp3, dtype="float32")
        if d.ndim > 1:
            d = d.mean(axis=1)
        if sr != 16000:
            n = int(len(d) * 16000 / sr)
            d = np.interp(np.linspace(0, len(d) - 1, n), np.arange(len(d)), d).astype("float32")
            sr = 16000
        sf.write(path, d, sr, subtype="PCM_16")
        return len(d) / sr
    except Exception:
        return 0.0


def suite_ear() -> list:
    from aea.io import listen
    from aea.lab.convbench import wer, semantic_match
    d = os.path.join(OUT, "audio")
    os.makedirs(d, exist_ok=True)
    listen.warm("en")
    rows = []
    for i, text in enumerate(EAR_CASES):
        wav = os.path.join(d, f"ear{i}.wav")
        dur = _mk_wav(text, wav)
        if not dur:
            continue
        s, sr = listen.read_wav(wav)
        t0 = time.time()
        got = listen.transcribe_samples(s, sr, "en").strip()
        el = time.time() - t0
        sem = semantic_match(text, got)
        rows.append(dict(case=text, got=got, wer=round(wer(text, got), 3),
                         seconds=round(el, 3), audio=round(dur, 2), ok=sem,
                         err="" if sem else "misheard"))
        print(f"   {dur:5.2f}s -> {el:5.3f}s  wer {rows[-1]['wer']:4.2f}  "
              f"{'ok ' if sem else 'MISS'}  {got[:52]!r}")
    return rows


def suite_prosody() -> list:
    """Does the prosody channel DISCRIMINATE deliveries the transcript cannot?

    Scored per sentence: how many distinct annotations across 7 deliveries whose transcripts are
    (expected to be) identical. The transcript column is the control - if it also varies, the
    comparison is not measuring what it claims to."""
    from aea.io import listen, prosody
    d = os.path.join(OUT, "audio")
    os.makedirs(d, exist_ok=True)
    rows = []
    for si, sent in enumerate(PROSODY_SENTENCES):
        base = {}
        neutral = os.path.join(d, f"p{si}_neutral.wav")
        _mk_wav(sent, neutral)
        s, sr = listen.read_wav(neutral)
        for _ in range(4):                    # earn a baseline before describe() may speak
            _, _m, base = prosody.annotate(s, sr, sent, base)
        texts, notes = set(), set()
        for label, kw in PROSODY_STYLES:
            p = os.path.join(d, f"p{si}_{label}.wav")
            if not _mk_wav(sent, p, **kw):
                continue
            s, sr = listen.read_wav(p)
            got = listen.transcribe_samples(s, sr, "en").strip()
            note, m, _ = prosody.annotate(s, sr, got, base)
            texts.add(got.lower().strip(" .!?"))
            notes.add(note)
            rows.append(dict(case=f"{sent[:28]} [{label}]", got=note or "(nothing unusual)",
                             transcript=got[:40], ok=True, err=""))
        n_t, n_n = len(texts), len(notes)
        rows.append(dict(case=f"SUMMARY {sent[:34]}", got=f"{n_t} transcripts vs {n_n} annotations",
                         ok=n_n > n_t, err="" if n_n > n_t else "no discrimination gained"))
        print(f"   {sent[:36]!r}: {n_t} distinct transcripts, {n_n} distinct annotations")
    return rows


AUDIO_SUITES = {"ear": suite_ear, "prosody": suite_prosody}


def run_audio() -> dict:
    summary = {}
    for name, fn in AUDIO_SUITES.items():
        print(f"\n== {name.upper()}")
        t0 = time.time()
        rows = fn()
        rep = _report(name, rows)
        rep["seconds"] = round(time.time() - t0, 2)
        _save(name, rows, rep)
        summary[name] = rep
        print(f"   -> {rep['pass_']}/{rep['n']} ({rep['rate']:.0%}) in {rep['seconds']}s")
        for r in rows:
            if not r["ok"]:
                print(f"   FAIL [{r.get('err','')}] {str(r['case'])[:60]!r} got={str(r.get('got'))[:50]!r}")
    return summary


def run_fast() -> dict:
    summary = {}
    for name, fn in FAST_SUITES.items():
        t0 = time.time()
        rows = fn()
        rep = _report(name, rows)
        rep["seconds"] = round(time.time() - t0, 2)
        _save(name, rows, rep)
        summary[name] = rep
        print(f"\n== {name.upper()}  {rep['pass_']}/{rep['n']} ({rep['rate']:.0%})  "
              f"{rep['seconds']}s")
        for r in rows:
            if not r["ok"]:
                print(f"   FAIL [{r.get('err','')}] {str(r['case'])[:66]!r}"
                      + (f"  got={r.get('got')}" if "got" in r else ""))
    # the asymmetric counts, reported apart because the trade matters
    ep = grid.load_json(os.path.join(OUT, "endpoint.json"), {}).get("rows", [])
    fc = sum(1 for r in ep if r.get("err") == "false_cut")
    lt = sum(1 for r in ep if r.get("err") == "late_take")
    pf = grid.load_json(os.path.join(OUT, "prefilter.json"), {}).get("rows", [])
    sp = sum(1 for r in pf if r.get("err") == "spurious")
    ms = sum(1 for r in pf if r.get("err") == "missed")
    fa = grid.load_json(os.path.join(OUT, "facts.json"), {}).get("rows", [])
    fm = sum(1 for r in fa if r.get("err") == "false_memory")
    at = grid.load_json(os.path.join(OUT, "attribution.json"), {}).get("rows", [])
    af = sum(1 for r in at if r.get("err") == "asserted_a_feeling")
    am = sum(1 for r in at if r.get("err") == "mangled_normal_speech")
    print("\n" + "=" * 78)
    print("ERROR DIRECTIONS - these are not interchangeable")
    print("=" * 78)
    print(f"  endpoint   false cuts {fc:3d}  (unrecoverable: truncates a person mid-thought)")
    print(f"             late takes {lt:3d}  (tolerable: they just wait)")
    print(f"  prefilter  spurious   {sp:3d}  (costs a round trip + a holding phrase on a chat turn)")
    print(f"             missed     {ms:3d}  (costs one clumsy reply; the person rephrases)")
    print(f"  memory     false      {fm:3d}  (POISONS the record - a fabricated fact about a person)")
    print(f"  attribution asserted {af:3d}  (tells a person what they feel - the harm this guard exists for)")
    print(f"             mangled   {am:3d}  (broke ordinary speech to prevent a rare harm)")
    summary["_directions"] = dict(false_cuts=fc, late_takes=lt, spurious=sp, missed=ms,
                                  false_memories=fm)
    return summary


if __name__ == "__main__":
    a = sys.argv[1:]
    s = {}
    if "--fast" in a or "--all" in a or not a:
        s.update(run_fast())
    if "--audio" in a or "--all" in a:
        s.update(run_audio())
    tot = sum(v["n"] for k, v in s.items() if isinstance(v, dict) and "n" in v)
    okc = sum(v["pass_"] for k, v in s.items() if isinstance(v, dict) and "n" in v)
    print(f"\nBATTERY: {okc}/{tot} ({okc/max(1,tot):.1%})   -> {OUT}")
