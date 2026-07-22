"""consolidate.py - MEMORY CONSOLIDATION: episodic transcripts -> semantic memory of Luis.

The neuroscience mechanism that actually translates: the hippocampus replays raw episodes during
sleep and the cortex distills them into durable semantic memory. Luis has 1,587 raw conversation
transcripts (episodic) and zero consolidation. This reads them, distills each into a few DURABLE
facts about him - goals, principles, preferences, decisions - and stores them as retrievable
semantic memory the small models reason FROM. The entity stops being generic and becomes HIS.

HARD BOUNDARY: these transcripts are PRIVATE (they name his life). Consolidation runs LOCAL ONLY
(Ollama) - the free hosted grid, even no-train, never sees a word. Slower, private, incremental -
which is exactly how sleep consolidation works. Resumable: it tracks processed sessions and grinds
the backlog a slice at a time.

  python consolidate.py --limit 15        # consolidate 15 not-yet-processed sessions (newest first)
  python consolidate.py --recall "what are Luis's principles about shipping?"
  python consolidate.py --board           # how much of the corpus is consolidated
"""
from __future__ import annotations
import json, os, sys, glob, urllib.request
from aea.kernel import grid
from aea.kernel import pulse

LOCAL_MODEL = "llama3.1:8b"          # local, non-thinking, reliable (the fitness lesson: qwen3 empty-traps)
STORE = os.path.join(grid.STATE, "luis_memory.json")
# 2026-07-19: the corpus WIDENED to every project's top-level sessions (the old single-project
# corpus was silently pruned by Claude Code's 30-day transcript cleanup - 1,570 unmined sessions
# lost; cleanupPeriodDays now 3650 in settings so it never happens again). Top-level only:
# subagent/workflow transcripts live deeper and are machine chatter, not Luis.
PROJECTS_ROOT = "<REDACTED-PATH>/.claude/projects"
PROJECT = os.path.join(PROJECTS_ROOT, "c--REDACTED-PORTFOLIO")
MIN_TURN = 24        # ignore trivial turns ("proceed", "go")
MAX_CHARS = 4200     # cap his voice per session so the local model stays fast + in-context

DISTILL = (
    "Below are Luis's OWN words across one working session with an AI assistant. "
    "Extract 1 to 3 DURABLE facts about Luis himself - his goals, working principles, preferences, "
    "values, or decisions - that would help an assistant serve him better in the future. "
    "Ignore one-off task mechanics and anything about this specific session's code. "
    "Write each as one terse third-person line starting 'Luis'. If there is nothing durable, output NOTHING.\n\n"
    "LUIS'S WORDS:\n{body}\n\nDURABLE FACTS:")


# ---- local, private embedding + store ----
def embed(text: str):
    body = json.dumps({"model": "mxbai-embed-large", "input": text}).encode()
    req = urllib.request.Request("http://localhost:11434/v1/embeddings", data=body,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())["data"][0]["embedding"]

META = STORE.replace(".json", ".meta.json")   # tiny sidecar: counts only, so live.py never parses embeddings

def load_store() -> dict:
    # grid.load_json QUARANTINES a torn file instead of silently resetting (review 2026-07-10:
    # a mid-write kill used to erase the whole consolidated memory without one error line)
    return grid.load_json(STORE, {"processed": [], "memories": []})

def save_store(s: dict):
    grid.atomic_save_json(STORE, s)           # kill-safe: temp + os.replace
    grid.atomic_save_json(META, {"processed": len(s["processed"]), "memories": len(s["memories"])})


# ---- read his voice out of one episodic transcript ----
def user_voice(path: str) -> str:
    turns = []
    try:
        for line in open(path, encoding="utf-8"):
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get("type") != "user" or not isinstance(o.get("message"), dict):
                continue
            c = o["message"].get("content")
            txt = c if isinstance(c, str) else (
                " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
                if isinstance(c, list) else "")
            txt = txt.strip()
            if len(txt) >= MIN_TURN and not txt.lstrip().startswith("<") \
               and "tool_result" not in txt[:30] and "[Request interrupted" not in txt:
                turns.append(txt)
    except Exception:
        return ""
    # newest, richest turns matter most; keep the tail within the char budget
    body, total = [], 0
    for t in reversed(turns):
        if total + len(t) > MAX_CHARS:
            break
        body.append(t); total += len(t)
    return "\n".join(reversed(body))


def distill(body: str) -> list[str] | None:
    """LOCAL model turns his words into durable facts. Never leaves the machine.
    Returns None on MODEL FAILURE (Ollama down) vs [] for a genuinely fact-free session -
    the review caught these conflated: with Ollama down, up to 144 sessions/day were being
    marked consolidated with zero memories extracted, silently, forever."""
    r = grid.call_openai("ollama", LOCAL_MODEL,
                         [{"role": "user", "content": DISTILL.format(body=body[:MAX_CHARS])}],
                         max_tokens=300, temperature=0.2, timeout=180)
    if not r["ok"]:
        return None
    out = []
    for ln in (r.get("text") or "").splitlines():
        ln = ln.strip().lstrip("-*0123456789. ").strip()
        if ln.lower().startswith("luis") and len(ln) > 20:
            out.append(ln[:400])
    return out[:3]


def consolidate(limit: int):
    import time as _t
    store = load_store()
    done = set(store["processed"])
    sessions = sorted(glob.glob(os.path.join(PROJECTS_ROOT, "*", "*.jsonl")),
                      key=os.path.getmtime, reverse=True)
    # You don't consolidate the episode you're still living: skip sessions touched in the last 10 min
    # (the active conversation). Consolidation is for closed episodes, like sleep replays the past day.
    LIVE = 600
    now = _t.time()
    todo = [p for p in sessions
            if os.path.basename(p)[:-6] not in done and (now - os.path.getmtime(p)) > LIVE]
    print(f"CONSOLIDATION (LOCAL {LOCAL_MODEL}, private)  |  corpus {len(sessions)} sessions, "
          f"{len(done)} already consolidated, processing {min(limit, len(todo))} now\n" + "=" * 74)
    added, engine_down = 0, False
    with grid.file_lock(STORE, timeout=2.0) as held:
        if not held:
            print("  another consolidation is running - yielding (no double-grind)"); return 0
        for path in todo[:limit]:
            sid = os.path.basename(path)[:-6]
            body = user_voice(path)
            if len(body) < MIN_TURN:
                store["processed"].append(sid); save_store(store); continue   # trivial session, done
            try:
                facts = distill(body)
                if facts is None:                             # MODEL DOWN: do NOT mark processed
                    engine_down = True
                    print("  ! local model unreachable - stopping; these sessions will retry next tick")
                    break
                for fct in facts:
                    store["memories"].append({"text": fct, "emb": embed(fct), "source": sid[:8]})
                    added += 1
                    print(f"  + {fct[:96]}")
                pulse.emit("memory", "distill", f"+{len(facts)} facts from session {sid[:8]}")
            except Exception as e:                            # embed died mid-session: stop, don't mark
                engine_down = True
                print(f"  ! consolidation error ({str(e)[:60]}) - stopping; session will retry")
                break
            store["processed"].append(sid)
            save_store(store)                                 # persist per session -> resumable/crash-safe
    print("=" * 74)
    print(f"  +{added} semantic memories  |  store now {len(store['memories'])} memories "
          f"from {len(store['processed'])}/{len(sessions)} sessions consolidated")
    return 1 if engine_down else 0


def _cos(a, b):
    import math
    d = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0

def recall(query: str, k: int = 5):
    store = load_store()
    if not store["memories"]:
        return []
    q = embed(query)
    pulse.emit("memory", "recall", query[:80])
    return [m["text"] for m in sorted(store["memories"], key=lambda m: -_cos(q, m["emb"]))[:k]]


def board():
    store = load_store()
    total = len(glob.glob(os.path.join(PROJECTS_ROOT, "*", "*.jsonl")))
    pct = round(100 * len(store["processed"]) / total, 1) if total else 0
    print(f"CONSOLIDATION BOARD\n  corpus: {total} sessions\n  consolidated: {len(store['processed'])} ({pct}%)\n"
          f"  semantic memories of Luis: {len(store['memories'])}\n  store: {STORE} (local, gitignored)")


if __name__ == "__main__":
    a = sys.argv
    if "--recall" in a:
        for m in recall(a[a.index("--recall") + 1]):
            print("  -", m)
    elif "--board" in a:
        board()
    else:
        lim = int(a[a.index("--limit") + 1]) if "--limit" in a else 15
        sys.exit(consolidate(lim))    # nonzero when the local engine is down -> live.py logs a true FAIL
