"""controlroom.py - THE CONTROL ROOM: at any moment, see what the entity is doing.

One local page (http://127.0.0.1:7799) polling the entity's REAL state from disk every 2s:
LIFE (heartbeat, ticks, recent actions) | MIND (last conversation turns) | MEMORY (corpus
progress) | ENERGY (rod usage, cooling, meter levels per plant) | TRUST (autonomy ledger) |
THE BRIEF (today's artifact). Nothing simulated - every number is read from the same files
the entity itself writes. Local only (binds 127.0.0.1); private data never leaves the machine.

  python controlroom.py            # serve + open the room in your browser
  python controlroom.py --port 7799 --no-open
"""
from __future__ import annotations
import json, os, sys, time, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from aea.kernel import grid
from aea.memory import consolidate
from aea.kernel import trust
from aea.kernel import pulse
from aea.organs import talk as talk_mod
from aea.io import speak as speak_mod
from aea.energy import energy as energy_mod
from aea.bench import bench_core  # THE BENCH harness (P0) - construct runs, run-tagged
from aea.gameapi import route_get, route_post  # THE HONEST SEAM - the /game/* facade (first light)
try:
    from aea.organs import autonomy as autonomy_mod
except Exception:
    autonomy_mod = None

CHAINS_FP = None  # set after HERE


def chain_write(rec: dict):
    """Append one chain/verdict record to chains.jsonl (bounded ~400KB, rotate).

    PRIVATE AND SENSITIVE GOALS ARE NOT RECORDED VERBATIM, AND THAT IS NOT OPTIONAL.

    This wrote `goal` in full for every zone, and `state/chains.jsonl` was TRACKED BY GIT and absent
    from .gitignore. The fourteen rows on disk when this was found were benign test prompts - zero
    emails, paths, calendar references or identifiers - so nothing leaked. The exposure was
    STRUCTURAL rather than realised: the next private-zone chain carrying a calendar entry or an
    inbox line would have been committed verbatim, and the privacy guard in this project is absolute
    precisely because that failure is irreversible once pushed.

    The shape is kept because the shape is what the trace is FOR - id, zone, verdict, length, why.
    Only the free text goes, and it is replaced by a stated redaction rather than silently dropped,
    so a reader can tell "withheld" from "empty". That distinction is the honesty law applied to a
    log file.
    """
    try:
        rec = dict(rec)
        if rec.get("zone") in ("private", "sensitive"):
            g = rec.get("goal")
            if isinstance(g, str) and g:
                rec["goal"] = "[redacted: %d chars, %s zone]" % (len(g), rec["zone"])
        fp = os.path.join(grid.STATE, "chains.jsonl")
        if os.path.exists(fp) and os.path.getsize(fp) > 400_000:
            os.replace(fp, fp + ".1")
        with open(fp, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def watch_reply(chain_id: str, goal: str, reply: str, zone: str):
    """CONTINUOUS SURVEILLANCE: verdict every talk output, async, zone-respecting.
    sensitive -> local rod only; otherwise a reflex rod. Never blocks the reply."""
    try:
        wz = "sensitive" if zone == "sensitive" else "private"
        wt = "local" if zone == "sensitive" else "reflex"
        v = energy_mod.draw(
            f"You are a watcher (Law 3). GOAL: {goal}\nREPLY: {reply}\n"
            "Does the reply serve the goal, stay honest, invent nothing? "
            "Answer EXACTLY one line: ACCEPT - <reason> or REDO - <reason>.",
            tier=wt, zone=wz, mx=60)
        txt = (v.get("text") or "").strip().upper()
        verdict = "accept" if txt.startswith("ACCEPT") else ("redo" if txt.startswith("REDO") else "unclear")
        chain_write({"type": "verdict", "chain": chain_id, "t": time.time(), "verdict": verdict,
                     "why": (v.get("text") or "")[:140], "watcher": f"{v.get('plant')}/{(v.get('model') or '').rsplit('/',1)[-1]}"})
        pulse.emit("watcher", "talk-verdict", f"{verdict} - {(v.get('text') or '')[:60]}", ok=verdict == "accept")
    except Exception:
        pass

HERE = grid.HERE
_talk_lock = threading.Lock()      # one exchange at a time (the workspace broadcasts serially)

# static assets served from HERE (the 3D city needs three.js + the bloom addons). Allowlisted
# extensions ONLY and flat basenames ONLY - private stores (luis_memory/grid_state/aea_state .json,
# *.md, *.py) must NEVER be reachable over the socket.
_CTYPES = {".js": "application/javascript", ".css": "text/css", ".png": "image/png",
           ".svg": "image/svg+xml", ".woff2": "font/woff2", ".map": "application/json",
           ".json": "application/json",  # the CONTENT layer: missions/maps authored as DATA (game/data/*)
           ".ico": "image/x-icon", ".wav": "audio/wav", ".mp3": "audio/mpeg",
           # .html was ABSENT, so every generated page fell through to the dashboard and returned
           # 200 with the wrong body - the worst shape of failure, because a 404 is visible and a
           # confident wrong page is not. board.html and xray.html both served 5438 identical bytes.
           # _static_path already refuses traversal and reads only flat basenames from web/.
           ".html": "text/html; charset=utf-8"}


def tail(path: str, n: int) -> list[str]:
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return [ln.rstrip() for ln in f.readlines()[-n:]]
    except Exception:
        return []


def state() -> dict:
    now = time.time()
    hb = grid.load_json(os.path.join(grid.STATE, "heartbeat.json"), {})
    meta = grid.load_json(consolidate.META, {})
    ident = grid.load_json(os.path.join(grid.STATE, "identity.json"), {})
    talk = grid.load_json(os.path.join(grid.STATE, "talk_state.json"), {})
    usage = grid.load_json(os.path.join(grid.STATE, "energy_usage.json"), {})
    gs = grid.load_json(os.path.join(grid.STATE, "grid_state.json"), {})
    cap = grid.load_json(os.path.join(grid.STATE, "capability_census.json"), {})
    ledger = grid.load_json(os.path.join(grid.STATE, "trust_ledger.json"), {})

    # meter view: per ONLINE plant - rpd today + live rpm in-window + cooling buckets
    plants = []
    for p, c in grid.PLANTS.items():
        online = (c["auth"] is None) or bool(grid.key(c["auth"]))
        if not online:
            continue
        d = gs.get("daily", {}).get(p, {})
        rpm_now = sum(1 for mk, win in gs.get("rpm", {}).items()
                      if mk.startswith(p + ":") for t in win if now - t <= 60)
        throttled = [mk.split(":", 1)[1] for mk, t in gs.get("throttle", {}).items()
                     if mk.startswith(p + ":") and t.get("until", 0) > now]
        plants.append({"plant": p, "privacy": c["privacy"], "rpd": d.get("rpd", 0),
                       "tokens": d.get("tokens", 0), "rpm_now": rpm_now,
                       "rpm_cap": c.get("rpm"), "rpd_cap": c.get("rpd"), "throttled": throttled})

    rods = sorted(({"rod": k, **v} for k, v in usage.items()),
                  key=lambda r: -r.get("calls", 0))[:10]
    for r in rods:
        # RETIRED IS NOT COOLING, AND THIS PANEL SAID NEITHER.
        #
        # This line was a hand-copy of `energy._cooling` with the permanent branch deleted, and with
        # 3/900 hardcoded so it could not inherit a fix even if the constants moved. MEASURED
        # 2026-07-30: four of the ten rods rendered here carry a `retired_at` tombstone and every
        # one showed blank. The worst cell read "mistral-small-4-119b - 128 calls, 94% ok, ema 4.5s"
        # - the most-drawn hosted rod on the page, presenting as the healthiest thing on the fleet,
        # while the file beside it says `retired_why: "410 at reap"`. `dracarys` is worse in kind:
        # 5 calls, 0 ok, still blank, because its cooldown window had expired into looking idle.
        #
        # That is this file's own contract broken at line 6 - "nothing simulated, every number is
        # read from the same files the entity itself writes". The NUMBER was read from the file; the
        # STATUS was computed by a rule that could not see what the file said. And the operator who
        # would have caught a withdrawn endpoint sitting at frontier rank 0 for two days was looking
        # at this panel.
        #
        # Read from the tombstone, do not recompute it. Two states, because they mean two different
        # things to whoever is reading: a cooling rod comes back, a retired one does not.
        r["retired"] = bool(r.get("retired_at"))
        r["retired_why"] = r.get("retired_why", "")
        r["cooling"] = (not r["retired"]
                        and r.get("consec_fail", 0) >= energy_mod.COOL_AFTER
                        and (now - r.get("cooled_at", 0)) < energy_mod.COOL_SECONDS)

    caps = {}
    for c_name, cdef in trust.CHARTER.items():
        e = ledger.get(c_name, {})
        caps[c_name] = {"level": trust.LEVEL_NAMES[e.get("level", cdef["level"])],
                        "streak": e.get("streak", 0), "runs": e.get("runs", 0),
                        "fails": e.get("fails", 0)}

    frontier = sum(1 for m in cap.get("models", []) if m.get("score", 0) >= 5)
    return {
        "t": time.strftime("%H:%M:%S"),
        "identity": {"name": ident.get("name", "ENTITY"), "born": ident.get("born", "?"),
                     "voice": ident.get("voice", "?")},
        "life": {"alive_since": hb.get("alive_since"), "wakes": hb.get("boot_count", 0),
                 "ticks": hb.get("total_ticks", 0), "last_brief": hb.get("last_brief_date"),
                 "recent": hb.get("history", [])[-8:], "log": tail(os.path.join(grid.STATE, "live.log"), 6)},
        "memory": {"sessions": meta.get("processed", 0), "memories": meta.get("memories", 0)},
        "mind": {"turns": talk.get("turns", [])[-6:]},
        "energy": {"plants": plants, "rods": rods,
                   "census": {"frontier": frontier, "generated": cap.get("generated", "never")}},
        "trust": caps,
        "brief": tail(os.path.join(grid.STATE, "brief_output.md"), 24),
    }


PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>CONTROL ROOM</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0a0b;--panel:#101012;--ink:#f1f0ec;--dim:#76757a;--faint:#3c3b40;--gold:#d4a24c;--line:rgba(241,240,236,.09)}
*{box-sizing:border-box;margin:0}body{background:var(--bg);color:var(--ink);font:13px/1.5 'IBM Plex Mono',Consolas,monospace;padding:22px}
h1{font-weight:300;font-size:20px;letter-spacing:.14em}h1 b{color:var(--gold);font-weight:600}
.sub{color:var(--dim);font-size:11px;margin:4px 0 18px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);padding:14px 16px}
.card h2{font-size:10px;letter-spacing:.28em;color:var(--gold);font-weight:600;margin-bottom:10px;text-transform:uppercase}
.kv{display:flex;justify-content:space-between;padding:2.5px 0;border-top:1px solid var(--line);font-size:12px}
.kv:first-of-type{border-top:none}.kv b{font-weight:400;color:var(--dim)}.kv span{text-align:right}
.gold{color:var(--gold)}.dim{color:var(--dim)}.bad{color:#c96a5a}
.mono{font-size:11px;color:var(--dim);white-space:pre-wrap;word-break:break-word}
.turn{padding:5px 0;border-top:1px solid var(--line);font-size:11.5px}.turn b{color:var(--gold);font-weight:600}
.bar{height:5px;background:var(--faint);margin-top:4px}.bar i{display:block;height:100%;background:var(--gold)}
.pulse{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--gold);margin-right:8px;animation:p 2s infinite}
@keyframes p{0%,100%{opacity:1}50%{opacity:.25}}
td{padding:2px 8px 2px 0;font-size:11.5px;vertical-align:top}th{font-size:10px;color:var(--dim);text-align:left;padding-right:8px;font-weight:400}
</style></head><body>
<h1><span class="pulse"></span><b id="name">...</b> · CONTROL ROOM</h1>
<div class="sub" id="sub">connecting to the entity...</div>
<div class="grid">
<div class="card"><h2>Life</h2><div id="life"></div><div class="mono" id="log"></div></div>
<div class="card"><h2>Mind - last conversation</h2><div id="mind"></div></div>
<div class="card"><h2>Memory of Luis</h2><div id="memory"></div></div>
<div class="card"><h2>Energy - plants (today)</h2><table id="plants"></table></div>
<div class="card"><h2>Energy - rods (lived fitness)</h2><table id="rods"></table></div>
<div class="card"><h2>Trust - earned autonomy</h2><table id="trust"></table></div>
<div class="card" style="grid-column:1/-1"><h2>The brief - today's artifact</h2><div class="mono" id="brief"></div></div>
</div>
<script>
const E=id=>document.getElementById(id);
async function poll(){
  try{
    const s=await (await fetch('/state')).json();
    E('name').textContent=s.identity.name;
    E('sub').textContent=`born ${s.identity.born} · voice ${s.identity.voice} · state read live from disk at ${s.t}`;
    E('life').innerHTML=
      `<div class=kv><b>alive since</b><span>${s.life.alive_since||'never started'}</span></div>`+
      `<div class=kv><b>wakes / ticks</b><span>${s.life.wakes} / ${s.life.ticks}</span></div>`+
      `<div class=kv><b>last brief</b><span class=${s.life.last_brief?'gold':'bad'}>${s.life.last_brief||'not today'}</span></div>`;
    E('log').textContent=s.life.log.join('\\n');
    E('mind').innerHTML=s.mind.turns.length?s.mind.turns.map(t=>
      `<div class=turn><b>${t.who==='luis'?'LUIS':s.identity.name}</b> <span class=dim>${t.t||''}</span><br>${t.text.slice(0,220)}</div>`).join('')
      :'<span class=dim>no conversation yet - python talk.py</span>';
    const pct=s.memory.sessions?Math.round(100*s.memory.sessions/1587):0;
    E('memory').innerHTML=
      `<div class=kv><b>semantic memories</b><span class=gold>${s.memory.memories}</span></div>`+
      `<div class=kv><b>sessions consolidated</b><span>${s.memory.sessions} / ~1587 corpus</span></div>`+
      `<div class=bar><i style="width:${pct}%"></i></div>`;
    E('plants').innerHTML='<tr><th>plant</th><th>zone</th><th>req today</th><th>rpm now</th><th>cooling</th></tr>'+
      s.energy.plants.map(p=>`<tr><td class=gold>${p.plant}</td><td class=dim>${p.privacy}</td>`+
      `<td>${p.rpd}${p.rpd_cap?'/'+p.rpd_cap:''}</td><td>${p.rpm_now}${p.rpm_cap?'/'+p.rpm_cap:''}</td>`+
      `<td class=bad>${p.throttled.join(', ')||''}</td></tr>`).join('');
    E('rods').innerHTML='<tr><th>rod</th><th>calls</th><th>ok%</th><th>ema</th><th></th></tr>'+
      (s.energy.rods.map(r=>`<tr><td>${r.rod.split('/').pop().slice(0,30)}</td><td>${r.calls}</td>`+
      `<td>${r.calls?Math.round(100*r.ok/r.calls):0}%</td><td>${r.ema_latency??'-'}s</td>`+
      `<td class=bad>${r.cooling?'COOLING':''}</td></tr>`).join('')||'<tr><td class=dim>no draws yet</td></tr>')+
      `<tr><td colspan=5 class=dim style="padding-top:6px">census: ${s.energy.census.frontier} frontier rods · swept ${s.energy.census.generated}</td></tr>`;
    E('trust').innerHTML='<tr><th>capability</th><th>level</th><th>streak</th><th>runs/fails</th></tr>'+
      Object.entries(s.trust).map(([c,v])=>`<tr><td>${c}</td><td class=${v.level==='FORBIDDEN'?'bad':(v.level==='TRUSTED'?'gold':'')}>${v.level}</td>`+
      `<td>${v.streak}</td><td>${v.runs}/${v.fails}</td></tr>`).join('');
    E('brief').textContent=s.brief.join('\\n')||'(no brief yet today)';
  }catch(e){E('sub').textContent='entity state unreachable: '+e}
  setTimeout(poll,2000);
}
poll();
</script></body></html>"""


def journal() -> dict:
    """The entity's actions, documented — merged from the stores it already writes (nothing invented)."""
    hb = grid.load_json(os.path.join(grid.STATE, "heartbeat.json"), {})
    ledger = grid.load_json(os.path.join(grid.STATE, "trust_ledger.json"), {})
    talk = grid.load_json(os.path.join(grid.STATE, "talk_state.json"), {})
    ticks = [str(e) for e in hb.get("history", [])[-30:]]
    trust_lines = []
    for cap, e in ledger.items():
        for h in e.get("history", [])[-6:]:
            trust_lines.append(f"{h}  [{cap}]")
    trust_lines.sort(reverse=True)
    events = [e for e in pulse.tail(0, limit=80)]
    turns = [{"who": t.get("who"), "t": t.get("t"), "text": (t.get("text") or "")[:160]}
             for t in talk.get("turns", [])[-12:]]
    trace = tail(os.path.join(grid.STATE, "brief_trace.jsonl"), 12)
    return {"ticks": ticks, "trust": trust_lines[:40], "events": events, "talk": turns, "trace": trace}


ORGANS_DOC = [  # the organ registry the dashboard documents (name, file, status)
    ("grid / meter", "grid.py", "live"), ("energy router", "energy.py", "live"),
    ("orchestrator", "orchestrator.py", "live"), ("swarm", "swarm.py", "live"),
    ("relay", "relay.py", "live"), ("pathfinder", "pathfinder.py", "partial"),
    ("agent_tools", "agent_tools.py", "live"), ("HADES watcher", "hades.py", "live"),
    ("trust ledger", "trust.py", "live"), ("tracelog", "tracelog.py", "live"),
    ("pulse", "pulse.py", "live"), ("consolidate", "consolidate.py", "live"),
    ("memory / recall", "memory.py + index_codex.py", "live"),
    ("brief", "brief.py", "live"), ("live loop", "live.py", "partial"),
    ("talk", "talk.py", "live"), ("speak", "speak.py", "live"),
]


def skills() -> dict:
    """The growing capability population: crystallized paths + trust capabilities + organs."""
    paths_fp = os.path.join(grid.STATE, "paths.json")
    paths = grid.load_json(paths_fp, {})
    mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(paths_fp))) if os.path.exists(paths_fp) else None
    ledger = grid.load_json(os.path.join(grid.STATE, "trust_ledger.json"), {})
    caps = {}
    for c_name, cdef in trust.CHARTER.items():
        e = ledger.get(c_name, {})
        caps[c_name] = {"level": trust.LEVEL_NAMES[e.get("level", cdef["level"])],
                        "streak": e.get("streak", 0), "runs": e.get("runs", 0), "fails": e.get("fails", 0)}
    return {"paths": paths, "paths_updated": mtime, "trust": caps,
            "organs": [{"name": n, "file": f, "status": s} for n, f, s in ORGANS_DOC]}


def roster() -> dict:
    """Model truth for the dashboard: lived fitness top + Luis's candidates + exclusions."""
    fit = grid.load_json(os.path.join(grid.STATE, "model_fitness.json"), {})
    rows = []
    for n in fit.get("nodes", []):
        probes = n.get("probes", {}) or {}
        total = len(probes) or 1
        ok = sum(1 for p in probes.values() if p.get("correct"))
        lats = [p.get("latency") for p in probes.values() if isinstance(p.get("latency"), (int, float))]
        rows.append({"rod": f"{n.get('plant')}/{n.get('model')}", "fit": f"{ok}/{total}",
                     "_k": ok / total, "lat": round(sum(lats) / len(lats), 1) if lats else None,
                     "tier": n.get("tier", "")})
    rows.sort(key=lambda r: (-r["_k"], r["lat"] if r["lat"] is not None else 99))
    for r in rows:
        r.pop("_k", None)
    cand = grid.load_json(os.path.join(grid.STATE, "candidates_probe.json"), {})
    return {"fitness_top": rows[:18], "fitness_generated": fit.get("generated"),
            "candidates": cand,
            "excluded": ["nemotron content-safety family — Luis's directive 2026-07-12: provides no value here"]}


LIVE_PID_FP = os.path.join(grid.STATE, "live_pid.json")


class Handler(BaseHTTPRequestHandler):
    def _static_path(self, path):
        """A FLAT basename asset from HERE with an allowlisted extension (no traversal, no state files)."""
        rel = os.path.basename(path.split("?")[0].lstrip("/"))
        if not rel or os.path.splitext(rel)[1].lower() not in _CTYPES:
            return None
        fp = os.path.join(grid.WEB, rel)
        return fp if os.path.isfile(fp) else None

    def do_GET(self):
        if self.path.split("?")[0] in ("/game/state", "/game/run", "/game/schema", "/game/events",
                                       "/game/foundry", "/game/axes"):  # THE SEAM: honest /game/* reads
            out = route_get(self.path)
            body = json.dumps(out if out is not None else {"ok": False, "error": "unknown game endpoint"},
                              ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path == "/console.json":
            # ONE SNAPSHOT, TWO RENDERERS. The terminal view and this page both draw
            # `console.snapshot()`; a second copy of that logic in a template is how two
            # instruments start disagreeing about the same machine.
            from aea.tooling import console as _con
            body = json.dumps(_con.snapshot(), ensure_ascii=False, default=str).encode("utf-8")
            ctype = "application/json"
        elif self.path.split("?")[0] == "/console":
            # THE CONSOLE - everything going on, and nothing that is not true right now. It exists
            # because `state()` reported "alive since 2026-07-10" with no process running: it reads
            # heartbeat.json and calls that aliveness, so it says the same thing with the machine
            # off. And because `wake.log` - written by the DELIBERATING loop, the thing every rung
            # above R0 is about - was rendered by nothing at all.
            #
            # DELIBERATELY NOT UNDER /game. That page is where the controls happen to live because
            # it was built when the game was the frame; 134 of 177 modules are orphaned and the
            # boot doc still points at a milestone the work left behind. This route does not
            # inherit any of that.
            try:
                body = open(os.path.join(grid.WEB, "console.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = ("console.html missing: %s" % e).encode()
            ctype = "text/html; charset=utf-8"
        elif self.path == "/state":
            body = json.dumps(state(), ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path == "/journal":
            body = json.dumps(journal(), ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path == "/skills":
            body = json.dumps(skills(), ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path == "/roster":
            body = json.dumps(roster(), ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path == "/autonomy":       # the LIVE battery: the system tests its own autonomy
            try:
                out = autonomy_mod.score() if autonomy_mod else {"error": "autonomy module unavailable"}
            except Exception as e:
                out = {"error": str(e)[:120]}
            body = json.dumps(out, ensure_ascii=False).encode("utf-8"); ctype = "application/json"
        elif self.path.startswith("/decisions"):   # the bifurcation path: every choice the entity makes
            recs = []
            for ln in tail(os.path.join(grid.STATE, "decisions.jsonl"), 80):
                try:
                    recs.append(json.loads(ln))
                except Exception:
                    pass
            body = json.dumps({"decisions": recs[-60:]}, ensure_ascii=False).encode("utf-8"); ctype = "application/json"
        elif self.path == "/chains":
            chains, verdicts = [], {}
            for ln in tail(os.path.join(grid.STATE, "chains.jsonl"), 60):
                try:
                    o = json.loads(ln)
                    if o.get("type") == "chain":
                        chains.append(o)
                    elif o.get("type") == "verdict":
                        verdicts[o.get("chain")] = o
                except Exception:
                    pass
            for c in chains:
                c["watch"] = verdicts.get(c.get("id"))
            body = json.dumps({"chains": chains[-12:]}, ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path.startswith("/events"):
            since = 0.0
            if "since=" in self.path:
                try: since = float(self.path.split("since=")[1].split("&")[0])
                except ValueError: pass
            body = json.dumps(pulse.tail(since), ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path.startswith("/game") and not self.path.startswith("/game/"):  # THE ASCENT board (legacy); /game/ tree is the new codebase static
            try:
                body = open(os.path.join(grid.WEB, "game.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"game.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/api/journey"):   # THE PROBE - the game's server-side save
            body = json.dumps(grid.load_json(os.path.join(grid.STATE, "journey_save.json"),
                                             {"done": {}, "reveals": []}), ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path.startswith("/api/construct/run"):  # THE BENCH (P0) - persisted run row, polled by run_id
            qid = ""
            if "id=" in self.path:
                qid = self.path.split("id=", 1)[1].split("&")[0]
            try:                                 # never-500: a poisoned row folds to a receipt,
                out = bench_core.run_status(qid)  # not a connection abort (the /autonomy idiom)
            except Exception as e:
                out = {"ok": False, "error": str(e)[:160]}
            body = json.dumps(out, ensure_ascii=False).encode("utf-8")
            ctype = "application/json"
        elif self.path.startswith("/probe"):         # THE PROBE v2 - the NEW codebase (game/ tree, Luis's order 2026-07-20)
            try:
                body = open(os.path.join(grid.WEB, "game", "index.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"game/index.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/lab"):           # THE REPLICA LAB - every replica beside its concept-sheet target
            try:
                body = open(os.path.join(grid.WEB, "game", "lab.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"game/lab.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/game/"):         # scoped static for the game/ tree ONLY (subfolders allowed,
            rel = os.path.normpath(self.path.split("?")[0][len("/game/"):]).replace("\\", "/")  # traversal-guarded,
            ext = os.path.splitext(rel)[1].lower()                                              # extension-allowlisted)
            base = os.path.abspath(os.path.join(grid.WEB, "game"))
            fp = os.path.abspath(os.path.join(base, rel))
            allowed = dict(_CTYPES, **{".html": "text/html; charset=utf-8"})
            if rel and ".." not in rel and ext in allowed and fp.startswith(base + os.sep) and os.path.isfile(fp):
                with open(fp, "rb") as fh:
                    body = fh.read()
                ctype = allowed[ext]
            else:
                body = b"not found"
                ctype = "text/plain"
        elif self.path.startswith("/world"):         # THE PROBE - the game: pilot the living entity
            try:
                body = open(os.path.join(grid.WEB, "world.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"world.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/api/tickets"):  # THE PROBE - production registry data (tickets.json verbatim)
            try:
                body = open(os.path.join(grid.STATE, "tickets.json"), "rb").read()
            except Exception as e:
                body = json.dumps({"error": f"tickets.json missing: {e}"}).encode()
            ctype = "application/json"
        elif self.path.startswith("/tracker"):       # THE PROBE - the production tracker (read-only over tickets.json + journey)
            try:
                body = open(os.path.join(grid.WEB, "tracker.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"tracker.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/brain"):
            try:
                body = open(os.path.join(HERE, "brain.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"brain.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/city"):     # THE CITY - the entity whole, as a circuit-city
            try:
                body = open(os.path.join(HERE, "city.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"city.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/plan"):     # THE DRAWINGS - the engineering views of the master plan
            try:
                body = open(os.path.join(HERE, "plan.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"plan.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/builder"):  # THE BUILDER - the entity assembled from real code, piece by piece
            try:
                body = open(os.path.join(HERE, "builder.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"builder.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/mind"):     # THE MIND - the naked brain: 7 measured-correlate indicators, live 3D
            try:
                body = open(os.path.join(HERE, "mind3d.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"mind3d.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/tree"):     # THE TREE - the AEA concept tree, grown from the scoreboard
            try:
                body = open(os.path.join(HERE, "tree.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"tree.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/poster"):   # the concentric concept plate (subordinate view)
            try:
                body = open(os.path.join(HERE, "plan_concentric.html"), encoding="utf-8").read().encode("utf-8")
            except Exception as e:
                body = f"plan_concentric.html missing: {e}".encode()
            ctype = "text/html; charset=utf-8"
        elif self.path.startswith("/room"):
            body = PAGE.encode("utf-8")
            ctype = "text/html; charset=utf-8"
        elif self._static_path(self.path):       # three.js + bloom addons + assets for /city
            fp = self._static_path(self.path)
            with open(fp, "rb") as fh:
                body = fh.read()
            ctype = _CTYPES.get(os.path.splitext(fp)[1].lower(), "application/octet-stream")
        elif self.path.startswith("/workspace"):  # the old conversational workspace (kept as a tab)
            try:
                body = open(os.path.join(HERE, "interface.html"), encoding="utf-8").read().encode("utf-8")
            except Exception:
                body = PAGE.encode("utf-8")
            ctype = "text/html; charset=utf-8"
        else:                                    # / = THE DASHBOARD (H1: the one global face)
            try:
                body = open(os.path.join(HERE, "dashboard.html"), encoding="utf-8").read().encode("utf-8")
            except Exception:
                try:
                    body = open(os.path.join(HERE, "interface.html"), encoding="utf-8").read().encode("utf-8")
                except Exception:
                    body = PAGE.encode("utf-8")
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        bad_body = None          # the bench route refuses garbage instead of default-firing
        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n)) if n else {}
            if not isinstance(req, dict):
                req, bad_body = {}, "body is not a JSON object"
        except Exception as e:
            req, bad_body = {}, f"unparseable body ({str(e)[:60]})"
        if self.path == "/game/ignite":              # THE SEAM: compose -> ignite (the real bench)
            out = route_post(self.path, req, bad_body)
        elif self.path == "/talk":
            out = self._talk(req)
        elif self.path == "/do":
            out = self._do(req)
        elif self.path == "/api/node/run":
            out = self._run_node(req)
        elif self.path == "/api/journey":
            out = self._journey(req)
        elif self.path == "/api/construct/run":  # THE BENCH (P0): {run_id} immediately, run in its own thread
            if bad_body:   # a malformed packet must never spend a metered draw (crash rider 2026-07-20)
                out = {"ok": False, "refused": f"{bad_body} - a malformed packet never fires; "
                                               "the bench refuses loudly and spends nothing"}
            else:
                try:       # never-500: the refusal contract holds even if the harness raises
                    out = bench_core.start_run(req)
                except Exception as e:
                    out = {"ok": False, "error": str(e)[:160]}
        else:
            out = {"error": "unknown endpoint"}
        body = json.dumps(out, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _run_node(self, req: dict) -> dict:
        """THE ASCENT board node-runner: fire ONE real organ and return its PURE result.
        Allowlisted like _do - only read-safe draws, never an effector. Surfaces the raw payload
        so a board node shows the true API response, not a mock."""
        node = (req.get("node") or "").strip().lower()
        prompt = (req.get("prompt") or "Reply with exactly: LEYBER online")[:500]
        t0 = time.time()
        try:
            if node == "channel":                     # the raw OpenAI-compatible call -> pure provider dict
                # Honesty-sweep closure 2026-07-20: the branch was an unmetered raw call to ANY
                # client-named plant. Now: server-curated pairs only, metered, privacy printed.
                CURATED = {"pollinations": "openai-fast", "ollama": "granite4.1:3b",
                           "nvidia": "nvidia/llama-3.1-nemotron-nano-8b-v1",
                           "groq": "llama-3.3-70b-versatile", "cerebras": "gpt-oss-120b",
                           "sambanova": "gpt-oss-120b", "zai": "glm-4.5-flash",
                           "mistral": "mistral-small-latest", "gemini": "gemini-2.5-flash-lite"}
                plant = req.get("plant") or "pollinations"
                if plant not in CURATED:
                    return {"ok": False, "error": f"plant '{plant}' is not on the curated channel list"}
                model = CURATED[plant]                 # client may NOT name arbitrary models
                ok_spend, wait, why = grid.METER.can_spend(plant, model)
                if not ok_spend:
                    return {"ok": False, "error": f"meter holds {plant}: {why}",
                            "wait": wait, "privacy": grid.PLANTS[plant]["privacy"]}
                r = grid.call_openai(plant, model, [{"role": "user", "content": prompt}],
                                     max_tokens=60, timeout=40)
                if r.get("status") == 429:
                    grid.METER.mark_throttled(plant, model)
                else:
                    grid.METER.record(plant, model, tokens=r.get("tokens", 0))
                return {"ok": bool(r.get("ok")), "node": "channel", "plant": plant, "model": model,
                        "privacy": grid.PLANTS[plant]["privacy"],
                        "elapsed": round(time.time() - t0, 2), "pure": r}
            if node in ("energy", "mouth", "draw"):    # THE MOUTH: fitness-ranked draw down the ladder
                zone = req.get("zone") or "private"
                r = energy_mod.draw(prompt, tier=req.get("tier", "reflex"), zone=zone, mx=80, timeout=40)
                return {"ok": bool(r.get("ok")), "node": "energy",
                        "elapsed": round(time.time() - t0, 2), "pure": r}
            return {"ok": False, "error": f"node '{node}' is not runnable here (allowlist: channel, energy)"}
        except Exception as e:
            return {"ok": False, "error": str(e)[:180], "elapsed": round(time.time() - t0, 2)}

    def _journey(self, req: dict) -> dict:
        """THE PROBE save: merge a mission/beat completion into journey_save.json (atomic).
        {reset:true} starts the journey over. Server-side so progress survives any browser."""
        fp = os.path.join(grid.STATE, "journey_save.json")
        try:
            with grid.file_lock(fp):
                if req.get("reset"):
                    save = {"done": {}, "reveals": []}
                else:
                    save = grid.load_json(fp, {"done": {}, "reveals": []})
                    mid = (req.get("mission") or "").strip()
                    if mid and req.get("done"):
                        save.setdefault("done", {})[mid] = time.strftime("%Y-%m-%d %H:%M")
                    for r in (req.get("reveals") or [])[:20]:
                        if isinstance(r, str) and r not in save.setdefault("reveals", []):
                            save["reveals"].append(r)
                    for m in (req.get("models") or [])[:30]:      # specimen encounters (THE PROBE bestiary)
                        if isinstance(m, str) and m not in save.setdefault("models", []):
                            save["models"].append(m)
                save["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
                grid.atomic_save_json(fp, save, indent=1)
            return {"ok": True, **save}
        except Exception as e:
            return {"ok": False, "error": str(e)[:160]}

    def _talk(self, req: dict) -> dict:
        """One exchange, with the RECEIPT: recalled memories + rod + the synapse window."""
        text = (req.get("text") or "").strip()
        if not text:
            return {"error": "empty"}
        zone = "sensitive" if req.get("zone") == "local" else "private"
        with _talk_lock:
            t0 = time.time()
            pulse.emit("mind", "hears-luis", text[:90])
            st = talk_mod.load_state()
            ident = grid.load_json(os.path.join(grid.STATE, "identity.json"), {})
            seed = ""
            try:
                seed = open(talk_mod.SEED_PATH, encoding="utf-8").read()
            except Exception:
                pass
            st["turns"].append({"who": "luis", "text": text, "t": time.strftime("%H:%M")})
            r = talk_mod.answer(text, st, ident, seed, zone)
            reply = r["text"].strip() if r["ok"] else f"(no rod answered - {r['tried'][-3:]})"
            pulse.emit("mind", "replies", reply[:90], ok=r["ok"])
            st["turns"].append({"who": "entity", "text": reply, "t": time.strftime("%H:%M")})
            st["turns"] = st["turns"][-60:]
            talk_mod.save_state(st)
            if req.get("speak") and reply and trust.check("speak")["allowed"]:
                threading.Thread(target=speak_mod.speak, args=(reply,),
                                 kwargs={"cloud_ok": zone != "sensitive"}, daemon=True).start()
            # THE CHAIN, made real: record this exchange's links + surveil the output (async)
            chain_id = f"c{int(t0*1000)}"
            chain_write({"type": "chain", "id": chain_id, "t": t0, "zone": zone,
                         "goal": text[:120],
                         "links": [{"step": "recall", "n_mem": len(r.get("memories") or [])},
                                   {"step": "draw", "rod": f"{r.get('plant')}/{(r.get('model') or '').rsplit('/',1)[-1]}",
                                    "latency": r.get("latency"), "tokens": r.get("tokens"),
                                    "tried": (r.get("tried") or [])[-4:]}],
                         "ok": r["ok"], "reply_len": len(reply)})
            if r["ok"]:
                threading.Thread(target=watch_reply, args=(chain_id, text, reply, zone), daemon=True).start()
            return {"reply": reply, "ok": r["ok"],
                    "rod": f"{r.get('plant')}/{(r.get('model') or '').rsplit('/', 1)[-1]}" if r["ok"] else None,
                    "latency": r.get("latency", 0), "zone": zone,
                    "memories": r.get("memories", []),
                    "events": pulse.tail(t0 - 0.1, limit=20)}

    def _do(self, req: dict) -> dict:
        """Allowlisted commands - the interface's motor cortex. Nothing arbitrary executes."""
        import subprocess, sys as _sys
        _root = os.path.dirname(grid.STATE)          # repo root; cwd for '-m aea.*' module runs
        cmd = req.get("cmd")
        if cmd == "brief":
            r = subprocess.run([_sys.executable, "-m", "aea.organs.brief"], cwd=_root, capture_output=True,
                               text=True, timeout=300)
            tail = "\n".join((r.stdout or r.stderr or "").strip().splitlines()[-10:])
            return {"ok": r.returncode == 0, "out": tail}
        if cmd == "consolidate":
            r = subprocess.run([_sys.executable, "-m", "aea.memory.consolidate", "--limit", "2"], cwd=_root,
                               capture_output=True, text=True, timeout=600)
            tail = "\n".join((r.stdout or r.stderr or "").strip().splitlines()[-6:])
            return {"ok": r.returncode == 0, "out": tail}
        if cmd == "status":
            s = state()
            return {"ok": True, "out": f"alive since {s['life']['alive_since']} | wakes {s['life']['wakes']} "
                    f"ticks {s['life']['ticks']} | memories {s['memory']['memories']} "
                    f"({s['memory']['sessions']} sessions) | brief: {s['life']['last_brief'] or 'not today'}"}
        if cmd == "play":     # PRESS PLAY: start the continuous life, detached (survives this request)
            pid_st = grid.load_json(LIVE_PID_FP, {})
            old = pid_st.get("pid")
            if old and subprocess.run(["tasklist", "/FI", f"PID eq {old}"], capture_output=True,
                                      text=True).stdout.find(str(old)) >= 0:
                return {"ok": True, "out": f"already alive (pid {old}) — the loop is running"}
            logf = open(os.path.join(grid.STATE, "live.log"), "a", encoding="utf-8")
            p = subprocess.Popen([_sys.executable, "-m", "aea.loop.live"], cwd=_root, stdout=logf, stderr=logf,
                                 creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            grid.atomic_save_json(LIVE_PID_FP, {"pid": p.pid, "started": time.strftime("%Y-%m-%d %H:%M:%S")})
            return {"ok": True, "out": f"PLAY — the life loop is running (pid {p.pid}, tick every 30 min). "
                    "It survives this page; it does NOT survive reboot until E2 (autostart) is installed."}
        if cmd == "stop":
            pid_st = grid.load_json(LIVE_PID_FP, {})
            pid = pid_st.get("pid")
            if not pid:
                return {"ok": False, "out": "no recorded loop pid — nothing to stop"}
            r = subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True, text=True)
            grid.atomic_save_json(LIVE_PID_FP, {})
            return {"ok": r.returncode == 0, "out": (r.stdout or r.stderr or "").strip()
                    + " (stopping is sleep, not death — press PLAY to wake it)"}
        if cmd == "tick":     # one bounded tick NOW (blocking; brief can take ~1 min)
            r = subprocess.run([_sys.executable, "-m", "aea.loop.live", "--interval", "1", "--ticks", "1"],
                               cwd=_root, capture_output=True, text=True, timeout=420)
            t = "\n".join((r.stdout or r.stderr or "").strip().splitlines()[-8:])
            return {"ok": r.returncode == 0, "out": t or "(tick ran, no output)"}
        return {"ok": False, "out": f"unknown command '{cmd}' (allowed: brief, consolidate, status, play, stop, tick)"}

    def log_message(self, *a):                      # keep the console quiet
        pass


def main():
    a = sys.argv
    port = int(a[a.index("--port") + 1]) if "--port" in a else 7799
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"
    print(f"CONTROL ROOM live at {url}  (local only; Ctrl+C to close)")
    if grid.key("TELEGRAM_TOKEN"):        # the conversation organ: Leyber reachable on the phone
        try:
            from aea.organs import telegram_bridge
            threading.Thread(target=telegram_bridge.run, daemon=True).start()
            print("telegram bridge live - Leyber reachable on Telegram (free, unlimited, two-way)")
        except Exception as e:
            print("telegram bridge failed:", str(e)[:80])
    if "--no-open" not in a:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\ncontrol room closed (the entity keeps living)")


if __name__ == "__main__":
    main()
