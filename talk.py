"""talk.py - TALK TO IT. The conversational face of the entity: the first interface where
everything already built becomes usable in one place. Each turn it:

  1. RECALLS you - queries the consolidated memory (luis_memory.json, local embeddings) for
     what it knows about Luis relevant to what you just said;
  2. KNOWS ITSELF - injects its own live state (heartbeat, corpus progress, trust levels) so
     "what have you been doing?" gets a TRUE answer, not a hallucination;
  3. DRAWS ENERGY - answers through the continuum (frontier tier, private zone by default -
     no-train plants only; `/local` locks it to the machine for sensitive talk);
  4. SPEAKS - replies aloud through the local voice (speak.py) while printing;
  5. REMEMBERS - the conversation persists (talk_state.json) so tomorrow it recalls today.

  python talk.py                    # the conversation loop (this is the one you use)
  python talk.py --ask "question"   # one-shot (scripting / verification)
  python talk.py --mute             # text only, no voice

  In the loop:  /local  -> sensitive mode (local model only, nothing leaves the machine)
                /grid   -> back to private mode (frontier rods, no-train)
                /mute /speak /status /quit
Stdlib + the engine. The human is the watcher here (Law 6) - HADES guards the unattended paths.
"""
from __future__ import annotations
import json, os, sys, time
import grid, energy, speak, consolidate, trust, pulse

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE = grid.HERE
STATE = os.path.join(HERE, "talk_state.json")
SEED_PATH = os.path.join(HERE, "aea_seed.md")
IDENTITY = os.path.join(HERE, "identity.json")
KEEP_TURNS = 14           # rolling window of exchanges carried into context


def load_state() -> dict:
    return grid.load_json(STATE, {"turns": [], "started": time.strftime("%Y-%m-%d")})

def save_state(s: dict):
    grid.atomic_save_json(STATE, s)


def self_status() -> str:
    """The entity's TRUE live state - so it never has to invent what it has been doing."""
    hb = grid.load_json(os.path.join(HERE, "heartbeat.json"), {})
    meta = grid.load_json(consolidate.META, {})
    parts = []
    if hb:
        parts.append(f"alive since {hb.get('alive_since','?')}, {hb.get('boot_count',0)} wakes, "
                     f"{hb.get('total_ticks',0)} ticks, last brief: {hb.get('last_brief_date') or 'not yet today'}")
    if meta:
        parts.append(f"memory: {meta.get('memories',0)} consolidated facts about Luis from {meta.get('processed',0)} sessions")
    return "; ".join(parts) or "first breath - no history yet"


def self_digest() -> str:
    """The SELF, compacted for the mind (gauntlet 2026-07-11: without this it CONFABULATED its
    own history - invented a rate-limit story for the EDR voice revocation)."""
    s = grid.load_json(os.path.join(HERE, "self.json"), {})
    auto = s.get("autobiography", [])[-2:]
    lessons = s.get("lessons", [])[:5]
    tasks = [f"{t['id']}({t['status']}): {t['text'][:70]}" for t in s.get("tasks", [])
             if t.get("status") != "done"][:5]
    return ("MY RECENT HISTORY (true):\n" + "\n".join(f"- {a}" for a in auto)
            + "\nMY LESSONS:\n" + "\n".join(f"- {l}" for l in lessons)
            + "\nMY OPEN TASKS:\n" + "\n".join(f"- {t}" for t in tasks))


def build_system(ident: dict, seed: str, memories: list[str], zone: str) -> str:
    name = ident.get("name", "the entity")
    creed = " ".join(ident.get("creed", []))
    mem = "\n".join(f"- {m}" for m in memories) or "- (nothing recalled for this topic yet)"
    return (f"You are {name}, Luis's personal entity - not a generic assistant. You run on his free grid "
            f"({'LOCAL ONLY right now - sensitive mode' if zone == 'sensitive' else 'private no-train rods'}). "
            f"You speak aloud through this machine's voice, so keep replies tight and speakable: 2-6 sentences, "
            f"no lists unless asked, no emoji, no headers. Honest over polite; name failure modes.\n"
            f"HARD RULES: never invent facts about Luis or about your own history - if a specific is not in "
            f"your seed, memories, or self below, say you have nothing recorded rather than decorate. "
            f"When Luis demands an EXACT output (exact words, exact format, a number), produce exactly that "
            f"and NOTHING else - precision outranks eloquence.\n\n"
            f"WHO LUIS IS (your seed):\n{seed}\n\n"
            f"WHAT YOU REMEMBER ABOUT HIM (recalled for this turn):\n{mem}\n\n"
            f"YOUR OWN LIVE STATE (true, from disk): {self_status()}\n\n{self_digest()}\n\n"
            f"YOUR CREED: {creed}")


def answer(user_text: str, state: dict, ident: dict, seed: str, zone: str) -> dict:
    try:
        memories = consolidate.recall(user_text, k=4)      # local embeddings; needs ollama
    except Exception:
        memories = []
    try:
        import index_codex                                  # the WHOLE book: his real documents
        memories += index_codex.recall(user_text, k=2)
    except Exception:
        pass
    system = build_system(ident, seed, memories, zone)
    recent = state["turns"][-KEEP_TURNS:]
    convo = "\n".join(f"{'Luis' if t['who'] == 'luis' else 'you'}: {t['text']}" for t in recent)
    prompt = (f"Conversation so far:\n{convo}\n\nLuis: {user_text}\n\n"
              f"Reply as yourself - grounded in the seed, the memories, and your true state.")
    tier = "local" if zone == "sensitive" else "frontier"
    r = energy.draw(prompt, tier=tier, zone=zone, mx=420, temp=0.4, system=system,
                    timeout=45, order="depth")   # conversation draws by DEPTH (the counsel duel)
    r["memories"] = memories[:4]        # the RECEIPT: what it attended to for this answer
    return r


def main():
    a = sys.argv[1:]
    mute = "--mute" in a
    ident = grid.load_json(IDENTITY, {})
    seed = open(SEED_PATH, encoding="utf-8").read() if os.path.exists(SEED_PATH) else ""
    state = load_state()
    zone = "private"
    name = ident.get("name", "ENTITY")

    def exchange(text: str) -> str:
        pulse.emit("mind", "hears-luis", text[:90])
        state["turns"].append({"who": "luis", "text": text[:800], "t": time.strftime("%H:%M")})
        r = answer(text, state, ident, seed, zone)
        pulse.emit("mind", "replies", (r.get("text") or "(no rod)")[:90], ok=r["ok"])
        if not r["ok"]:
            reply = f"(no rod answered - tried {r['tried'][-3:]})"
        else:
            reply = r["text"].strip()
        state["turns"].append({"who": "entity", "text": reply[:1200], "t": time.strftime("%H:%M")})
        state["turns"] = state["turns"][-60:]              # bounded (review lesson: nothing grows forever)
        save_state(state)
        src = f"{r.get('plant')}/{(r.get('model') or '').rsplit('/', 1)[-1]}" if r["ok"] else "none"
        print(f"\n{name} ({src}, {r.get('latency', 0)}s):\n{reply}\n")
        if not mute and reply and trust.check("speak")["allowed"]:
            spoke = speak.speak(reply)
            trust.record("speak", spoke)
        return reply

    if "--ask" in a:                                        # one-shot: scripting + verification
        exchange(a[a.index("--ask") + 1])
        return

    print(f"=== {name} ===  ({len(state['turns'])} remembered turns | zone={zone} | "
          f"{'muted' if mute else 'voice on'})")
    print("talk to it. /local /grid /mute /speak /status /quit\n")
    while True:
        try:
            text = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n(sleeping - the conversation is remembered)"); break
        if not text:
            continue
        if text == "/quit":
            print("(sleeping - the conversation is remembered)"); break
        if text == "/local":
            zone = "sensitive"; print("(sensitive mode: LOCAL model only - nothing leaves this machine)\n"); continue
        if text == "/grid":
            zone = "private"; print("(private mode: frontier rods, no-train plants)\n"); continue
        if text == "/mute":
            mute = True; print("(voice off)\n"); continue
        if text == "/speak":
            mute = False; print("(voice on)\n"); continue
        if text == "/status":
            print(self_status() + "\n"); continue
        exchange(text)


if __name__ == "__main__":
    main()
