"""pulse.py - the entity's NERVOUS SIGNAL. Every organ emits what it does, as it does it,
to one append-only stream (events.jsonl) - so the brain view can show the mind NAKED:
every draw, every memory write, every spoken word, every trust stamp, live.

  pulse.emit("energy", "draw", "groq/llama-3.3 ok 0.3s")     # organs call this
  pulse.tail(since_t)                                         # the brain view polls this

Bounded: rotates at ~1MB keeping the tail. Dependency-light (grid only for paths/locks).
Emitting must NEVER break an organ: emit() swallows every error.
"""
from __future__ import annotations
import json, os, time
import grid

EVENTS = os.path.join(grid.STATE, "events.jsonl")
MAX_BYTES = 1_000_000
KEEP_TAIL = 1200


def emit(organ: str, action: str, detail: str = "", ok: bool = True):
    """Fire-and-forget synapse. Never raises."""
    try:
        line = json.dumps({"t": round(time.time(), 3), "organ": organ, "action": action,
                           "detail": str(detail)[:220], "ok": bool(ok)}, ensure_ascii=False)
        with open(EVENTS, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        if os.path.getsize(EVENTS) > MAX_BYTES:
            _rotate()
    except Exception:
        pass


def _rotate():
    try:
        with grid.file_lock(EVENTS, timeout=1.0) as held:
            if not held:
                return
            with open(EVENTS, encoding="utf-8", errors="ignore") as f:
                tail = f.readlines()[-KEEP_TAIL:]
            tmp = EVENTS + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.writelines(tail)
            os.replace(tmp, EVENTS)
    except Exception:
        pass


def tail(since_t: float = 0.0, limit: int = 200) -> list[dict]:
    """Events after since_t, oldest first. The brain view's poll."""
    out = []
    try:
        with open(EVENTS, encoding="utf-8", errors="ignore") as f:
            for ln in f.readlines()[-1500:]:
                try:
                    e = json.loads(ln)
                    if e.get("t", 0) > since_t:
                        out.append(e)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return out[-limit:]


if __name__ == "__main__":
    emit("pulse", "selftest", "the nervous signal fires")
    ev = tail(0)
    print(f"events on the wire: {len(ev)}; last: {ev[-1] if ev else None}")
