"""notify.py - the REACH organ: LEYBER reaches Luis by PHONE (CallMeBot text-to-speech call).
Self-notify to the OWNER only (never third parties) - so not a trust-FORBIDDEN outbound.
Key lives in .env as CALLMEBOT_KEY (Luis activated the call service).
  python notify.py "spoken message"     # rings Luis's phone and speaks it
"""
from __future__ import annotations
import sys, urllib.request, urllib.parse
import grid

PHONE = "34632821666"


def call(text: str) -> dict:
    key = grid.key("CALLMEBOT_KEY")
    if not key:
        return {"ok": False, "why": "no CALLMEBOT_KEY in .env"}
    url = ("https://api.callmebot.com/call.php?phone=" + PHONE
           + "&text=" + urllib.parse.quote((text or "")[:380])
           + "&apikey=" + urllib.parse.quote(key))
    try:
        r = urllib.request.urlopen(url, timeout=45).read().decode("utf-8", "ignore")
        low = r.lower()
        ok = any(s in low for s in ("apikey is correct", "queued", "calling", "success", "will call", "your balance"))
        try:
            import pulse; pulse.emit("voice", "call-luis", text[:60], ok=ok)
        except Exception:
            pass
        return {"ok": ok, "resp": r.strip()[:280]}
    except Exception as e:
        return {"ok": False, "why": str(e)[:160]}


notify = call

if __name__ == "__main__":
    print(call(" ".join(sys.argv[1:]) or "Leyber here. First contact from your entity."))
