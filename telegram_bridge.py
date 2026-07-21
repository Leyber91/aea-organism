"""telegram_bridge.py - the CONVERSATION organ: Leyber reachable on the phone, FREE + UNLIMITED,
two-way. Luis texts a Telegram bot; the entity answers with its real grounded mind (talk.answer),
watched by HADES, from its memory of him. Binds to the FIRST chat that messages it (Luis) and
ignores everyone else - private to him. Pure HTTPS long-poll (EDR-safe).

ACTIVATE (one step, only Luis can do it):
  1. Open Telegram, message @BotFather, send /newbot, pick a name + username
  2. Copy the bot TOKEN it gives you  ->  put in .env as  TELEGRAM_TOKEN=<token>
  3. Restart the control room; the bridge auto-starts. Then message YOUR new bot - Leyber answers.

Runs as a daemon thread inside controlroom, or standalone:  python telegram_bridge.py
"""
from __future__ import annotations
import os, json, time, urllib.request, urllib.parse
import grid

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "telegram_state.json")
API = "https://api.telegram.org/bot"


def send(text: str, token: str | None = None, chat=None) -> dict:
    """Push a message to Luis's bound chat (used by the reach/notify path too)."""
    token = token or grid.key("TELEGRAM_TOKEN")
    chat = chat or grid.load_json(STATE, {}).get("chat")
    if not token or not chat:
        return {"ok": False, "why": "no TELEGRAM_TOKEN or no bound chat yet"}
    try:
        url = f"{API}{token}/sendMessage?" + urllib.parse.urlencode({"chat_id": chat, "text": (text or "")[:4000]})
        urllib.request.urlopen(url, timeout=20).read()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "why": str(e)[:120]}


def run(poll_secs: int = 50):
    token = grid.key("TELEGRAM_TOKEN")
    if not token:
        return
    import talk as talk_mod
    try:
        import pulse
    except Exception:
        pulse = None
    st = grid.load_json(STATE, {"offset": 0, "chat": None})
    while True:
        try:
            url = f"{API}{token}/getUpdates?offset={st.get('offset', 0)}&timeout={poll_secs}"
            updates = json.loads(urllib.request.urlopen(url, timeout=poll_secs + 15).read().decode("utf-8", "ignore")).get("result", [])
        except Exception:
            time.sleep(4); continue
        for u in updates:
            st["offset"] = u["update_id"] + 1
            msg = u.get("message") or u.get("edited_message") or {}
            text = (msg.get("text") or "").strip()
            cid = (msg.get("chat") or {}).get("id")
            if not text or not cid:
                continue
            if st.get("chat") is None:                      # first to reach it = Luis; bind him
                st["chat"] = cid
                grid.atomic_save_json(STATE, st)
                send("LEYBER here - reached on Telegram, free and unlimited, two-way. Ask me anything; "
                     "I answer from my real memory of you, watched by HADES.", token, cid)
            if cid != st.get("chat"):
                continue                                    # private to Luis only
            try:
                state = talk_mod.load_state()
                ident = grid.load_json(os.path.join(HERE, "identity.json"), {})
                seed = ""
                try:
                    seed = open(talk_mod.SEED_PATH, encoding="utf-8").read()
                except Exception:
                    pass
                state["turns"].append({"who": "luis", "text": text[:800], "t": time.strftime("%H:%M")})
                r = talk_mod.answer(text, state, ident, seed, "private")
                reply = r["text"].strip() if r.get("ok") else "(no rod answered)"
                state["turns"].append({"who": "entity", "text": reply[:1200], "t": time.strftime("%H:%M")})
                state["turns"] = state["turns"][-60:]
                talk_mod.save_state(state)
                if pulse:
                    pulse.emit("mind", "telegram", text[:60])
                send(reply, token, cid)
            except Exception as e:
                send("(error: " + str(e)[:90] + ")", token, cid)
        grid.atomic_save_json(STATE, st)


if __name__ == "__main__":
    print("telegram bridge:", "starting" if grid.key("TELEGRAM_TOKEN") else "NO TELEGRAM_TOKEN in .env")
    run()
