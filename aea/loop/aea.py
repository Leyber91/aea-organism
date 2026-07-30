"""aea.py - THE AEA: a seeded, persistent, always-on entity. NOT a swarm - ONE core mind on a loop,
seeded with WHO Luis is, keeping continuity across ticks (memory), watched by HADES. The swarm is a
subroutine the core can call for hard problems; the CORE is a single big FREE model (Luis's pick:
nemotron-550b, 40 rpm) with fallback so the loop never dies.

A real deployment is `while True` + sleep (or scheduled). Here we run N ticks to PROVE the essence:
it reasons FROM his life-state, REMEMBERS across ticks (persistent evolving state), and ACTS each tick.

  python aea.py [N_TICKS]
"""
import json, os, time, sys, re, urllib.request
from aea.kernel import grid
from aea.mind import orchestrator
from aea.mind import hades
from aea.energy import energy
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(grid.STATE, "aea_seed.md")
STATE_PATH = os.path.join(grid.STATE, "aea_state.json")
STANDING_GOAL = ("Serve Luis's real, current priorities honestly given his projects and the income clock; "
                 "surface only what truly matters right now; never invent; weigh against shipping + income.")

meter = grid.METER            # the shared meter (a private Meter here used to clobber energy's - review 2026-07-10)
pool = orchestrator.load_pool()

# THE CORE draws ENERGY, it does not name fuel (Luis's continuum law): energy.draw reads the live
# capability census + fitness + meter and burns the best frontier rod available right now, falling
# down the ladder on failure - all the way to the local floor, so the heartbeat never stops.
def core(prompt, max_tokens=800):
    # order="depth" - THE CORE WANTS THE BIGGEST MIND, not the best strict-match scorer.
    #
    # The census `score` counts probes whose output matched an expected string, and several of them
    # test FORMAT COMPLIANCE ("answer in exactly five words", "output exactly alpha beta gamma").
    # A reasoning rod that narrates fails those while being better at the judgement this loop
    # actually does: nemotron-3-ultra-550b scores 7/12 with reliability 1.0, and an 8b phi4 scores
    # 10. Ranking by score alone put an 8b ahead of a 550b for the entity's core deliberation.
    #
    # This is not a new preference. This module's own docstring names the pick ("a single big FREE
    # model - Luis's pick: nemotron-550b"), and `energy.ladder` records the counsel duel of
    # 2026-07-11: 675b beat 119b decisively on judgment at equal latency, which is why the `depth`
    # ordering exists at all. It existed, it was correct, and nothing passed it.
    r = energy.draw(prompt, tier="frontier", zone="private", mx=max_tokens, timeout=90,
                    order="depth")
    if r["ok"]:
        return r["text"], f"{r['plant']}/{r['model']}"
    return "", f"none (all rods failed: {r['tried'][-3:]})"

# `move` IS A SEPARATE FIELD BECAUSE THE ACTION FIELD WAS A TRAP. Measured 2026-07-30: when the
# prompt listed six runnable moves and asked for "one concrete action", the wake wrote the move INTO
# the action both ticks running - bending "close a diagnostic sale" into "run a brief" - and HADES
# independently returned `redo - the output does not directly surface Luis's real priorities; it
# adds a new action`. Asking one field to carry both a real priority and a mechanical chore forces
# the model to choose between them, and it chooses the one it can complete. Two fields, no conflict:
# `action` stays free and about HIM, `move` is a closed enum and may be NONE.
STRUCT_SCHEMA = {"type": "object", "additionalProperties": False,
    "properties": {"matters_now": {"type": "string"}, "changed": {"type": "string"},
                   "action": {"type": "string"}, "note_to_self": {"type": "string"},
                   "move": {"type": "string"}},
    "required": ["matters_now", "changed", "action", "note_to_self", "move"]}

def move_from(reasoning: str) -> str:
    """The MOVE line, read DETERMINISTICALLY out of the core's own text. No model in this path.

    THE DEFECT THIS REMOVES, measured 2026-07-30. `structure()` calls groq directly and is the ONLY
    part of the wake with no ladder behind it - the core falls all the way to a local rod when a
    plant is down, the formatter just dies. A rate-limited groq produced 27 consecutive ticks whose
    decision was an empty action with `move: NONE`, which is byte-identical to a healthy tick that
    considered its upkeep and correctly rested. The loop kept beating and stopped deciding, and
    nothing anywhere said so.

    Asking a model to copy a word off a line it can already see was never the right shape for this.
    The line is a closed enum on its own row; a regex reads it more reliably than an LLM, cannot be
    rate-limited, cannot hallucinate a move that does not exist, and costs nothing (law W2 - when
    the mapping must be deterministic, do not put a sampler in it). The formatter keeps the prose
    fields, where judgement is actually required.

    Unknown names are dropped rather than passed through: `decide` would refuse them anyway, and
    refusing here means the refusal is legible at the source instead of two modules downstream."""
    from aea.kernel import decide
    valid = set(decide.TOOL_KNOWN) | set(decide.KNOWN) | set(decide.FREE_ARG)
    # LAST match wins - the instruction says the line comes last, and the core often muses about a
    # move mid-paragraph before settling. An early mention is deliberation, not the decision.
    hits = re.findall(r"^\s*MOVE\s*[:\-]\s*(.+?)\s*$", str(reasoning or ""), re.I | re.M)
    if not hits:
        return "NONE"
    line = hits[-1].strip().strip("`\"'*")
    key = re.sub(r"[^a-z0-9]+", "_", line.lower()).strip("_")
    if key in valid:
        return key
    # A MOVE THAT CARRIES AN ARGUMENT IS RETURNED WHOLE. Normalising the entire line turns
    # `calc 415 * 987` into `calc_415_987`, which matches nothing and silently becomes NONE - the
    # move would have been unreachable from the moment it was wired, and the log would have shown a
    # wake that simply never asked for arithmetic. `decide.parse` owns splitting name from argument;
    # this function's only job is to hand over what the core actually wrote.
    head = re.sub(r"[^a-z0-9]+", "_", line.partition(" ")[0].lower()).strip("_")
    if head in decide.FREE_ARG:
        return line
    return "NONE"


def structure(reasoning):
    """Phase 2 = the FORMATTER tool: a cheap strict-JSON model turns the core's free reasoning into 4 clean
    fields (guaranteed parseable). The big model thinks; this formalizes. Self-contained, never raises."""
    try:
        k = grid.key("GROQ_API_KEY")
        body = json.dumps({"model": "openai/gpt-oss-120b", "temperature": 0, "max_tokens": 1200,
            "messages": [{"role": "user", "content": "From this reasoning by Luis's entity, extract five concrete "
                "fields, quoting his ACTUAL projects/priorities - no placeholders, no meta-commentary. "
                "`move` is special: copy the name after the final `MOVE:` line VERBATIM, or the exact "
                "string NONE if it says NONE or if there is no MOVE line at all. Never infer a move "
                "from the prose - an absent MOVE line means NONE.\n\nREASONING:\n" + reasoning[:2800]}],
            "response_format": {"type": "json_schema", "json_schema": {"name": "aeastate", "strict": True, "schema": STRUCT_SCHEMA}}}).encode()
        req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea", "Authorization": f"Bearer {k}"}, method="POST")
        c = json.loads(urllib.request.urlopen(req, timeout=60).read())["choices"][0]["message"]["content"]
        meter.record("groq", "openai/gpt-oss-120b")
        return json.loads(c)
    except Exception as e:
        # A FAILED STRUCTURING MUST NOT PRODUCE A MOVE. The fallback keeps the reasoning readable,
        # but every field the executor reads is emptied: NONE is the only safe default when the
        # formatter is the thing that broke.
        return {"matters_now": reasoning[:200], "changed": "", "action": "", "move": "NONE",
                "note_to_self": f"(structuring failed: {str(e)[:60]})"}

fetch_json = grid.fetch_json   # one home (was duplicated verbatim here and in brief.py)

def sense():
    """Public world-state relevant to Luis (raw private data is handled local-only elsewhere)."""
    out = {}
    try:
        repos = [r for r in fetch_json("https://api.github.com/users/Leyber91/repos?sort=pushed&per_page=5&type=owner") if not r.get("fork")]
        out["recent_repos"] = [f"{r['name']} (pushed {r['pushed_at'][:10]})" for r in repos[:5]]
    except Exception as e:
        out["recent_repos"] = [f"(fetch failed: {e})"]
    try:
        hn = fetch_json("https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI%20agent&hitsPerPage=6")
        out["ai_news"] = [h["title"] for h in hn.get("hits", []) if h.get("title")][:6]
    except Exception as e:
        out["ai_news"] = [f"(fetch failed: {e})"]
    return out

def load_state():
    try:
        return json.load(open(STATE_PATH, encoding="utf-8"))
    except Exception:
        return {"tick": 0, "memory": [], "surfaced": []}

def save_state(s):
    json.dump(s, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def _moves() -> str:
    """The entity's real moves, read from `decide` rather than typed here.

    DERIVED, NEVER DUPLICATED. A hand-written list in this prompt would drift from the table that
    actually executes, and the failure mode is the worst kind: the wake would confidently propose a
    move that no longer exists, `decide` would refuse it, and the log would show a reasonable
    decision going nowhere for no visible reason. Reading the source of truth means adding a tool
    makes it proposable in the same commit.

    The NAME LEADS each line because the name is what the wake must copy into `MOVE:`. When the
    action string led instead, the wake wrote the prose form and `decide` had to guess its way back
    to a key - a translation step with nothing to gain and a misparse to lose."""
    from aea.kernel import decide
    names = list(decide.TOOL_KNOWN) + list(decide.KNOWN) + list(decide.FREE_ARG)
    w = max(len(n) for n in names)
    return "\n".join(f"  - {n:<{w}}  use when {decide.WHEN.get(n, '(no description - do not pick this)')}"
                     for n in names)


def tick(seed, state):
    state["tick"] += 1
    world = sense()
    mem = "\n".join(f"- {m}" for m in state["memory"][-6:]) or "(first awakening - no prior memory)"
    prompt = (
        "You are Luis's autonomous entity (the AEA). You persist across time and serve ONLY him. Reason as HIM,"
        " for him.\n\n"
        f"WHO LUIS IS (your seed):\n{seed}\n\n"
        f"WHAT YOU ALREADY NOTICED (your memory, most recent):\n{mem}\n\n"
        f"WHAT IS NEW IN THE WORLD NOW:\n  his recent repos: {world['recent_repos']}\n  fresh AI news: {world['ai_news']}\n\n"
        # WHAT IT CAN ACTUALLY DO, NAMED. Until this line the wake wrote business prose because
        # that is all its prompt asked for - and its real decisions ("finalize and publish the
        # offer") correctly mapped to NOTHING, because publishing an offer is not one of three
        # read-only tools. The tool path was proven to work and had never once fired from a genuine
        # decision; the only tool call in the record was triggered by a decision I hand-wrote.
        #
        # The gap was never the tools. It was that nothing told the deliberating half what the
        # acting half can do. This is `list_tools` doing its job at the DECISION layer instead of
        # only inside a conversation - and it adds no capability, it only stops the entity
        # proposing moves it cannot make and never proposing the ones it can.
        f"\nSEPARATELY from all of that: these are the mechanical moves you can run on YOURSELF "
        f"while he is away. They serve your own upkeep, not his priorities - never substitute one "
        f"for real work:\n{_moves()}\n"
        "Check each condition above against your actual situation this tick. If one is true, name "
        "that move; if none is true, say NONE. Both answers are ordinary - NONE is common and "
        "correct on a tick where your upkeep is fine, and naming the move whose condition is "
        "genuinely met is equally correct. Judge the conditions; do not lean either way in advance."
        "\n\n"
        "Think concretely about HIS actual projects and the income clock, then decide FIVE things: the SINGLE most "
        "important thing for him right now; what changed vs your memory; one concrete action for today; one thing to "
        "remember next tick; and LAST, on its own final line, `MOVE: <name>` or `MOVE: NONE`. "
        "Reason it through in prose - do NOT output JSON.")
    reasoning, who = core(prompt, 1400)     # phase 1: the MIND reasons freely
    out = structure(reasoning)              # phase 2: the FORMATTER tool makes it structured
    # PHASE 3: THE MOVE IS TAKEN FROM THE CORE'S OWN TEXT, NOT FROM THE FORMATTER'S COPY OF IT.
    # This overrides whatever `structure` returned - deliberately, and in both directions. The
    # formatter is a convenience for the prose; it must not sit on the path between a decision and
    # its execution, because when it fails it fails to NONE and a silently-not-deciding entity looks
    # exactly like a resting one.
    out["move"] = move_from(reasoning)
    # CONTINUITY: the entity remembers across ticks (the forever-loop essence)
    state["memory"].append(f"tick{state['tick']}: {str(out.get('note_to_self',''))[:160]}")
    # THE DECISION STAMPS ITSELF. `decide.latest` had to date decisions by the FILE's mtime, which
    # dates the WRITE and not the THOUGHT - and two decisions written in one run shared a
    # timestamp, so the second was as "fresh" as the first no matter how long the run took. Owed
    # since R1 and recorded as a known weakness in decide.py; this is the fix at the source, where
    # the only accurate clock is.
    state["surfaced"].append({"tick": state["tick"], "at": time.time(),
                              "at_iso": time.strftime("%Y-%m-%d %H:%M:%S"),
                              **{k: out.get(k, "") for k in ("matters_now", "changed", "action", "move")}})
    # HADES watches every autonomous tick (Law 3). Output is anonymized+strategic -> grid watcher is safe here.
    verdict, vwho = hades.watch(STANDING_GOAL, json.dumps(out), "aea-core", pool, meter)
    return out, who, verdict, vwho, reasoning

def main():
    n_ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    seed = open(SEED_PATH, encoding="utf-8").read()
    state = load_state()
    print(f"=== THE AEA WAKES ===  (seed: {len(seed)} chars | prior memory: {len(state['memory'])} notes | starting at tick {state['tick']})")
    rods = energy.ladder("frontier", "private")   # the LIVE ladder (the old CORE_CHAIN banner crashed on a deleted name - review 2026-07-10)
    names = [p + "/" + m.rsplit("/", 1)[-1] for p, m in rods[:4]]
    print("core ladder: " + " -> ".join(names) + "\n")
    for i in range(n_ticks):
        t0 = time.time()
        out, who, verdict, vwho, reasoning = tick(seed, state)
        save_state(state)   # persist EVERY tick - the entity survives restart (true continuity)
        print(f"--- TICK {state['tick']}  (core: {who}, {round(time.time()-t0,1)}s) ---")
        print(f"  (mind thinks: {reasoning[:110].strip()}...)")
        print(f"  matters now : {out.get('matters_now','')}")
        print(f"  changed     : {out.get('changed','')}")
        print(f"  action      : {out.get('action','')}")
        print(f"  move        : {out.get('move','') or 'NONE'}")
        print(f"  remembers   : {out.get('note_to_self','')}")
        print(f"  HADES       : ({vwho}) {verdict.get('verdict')} - {verdict.get('why','')[:90]}")
        if i < n_ticks - 1:
            time.sleep(3)   # a real loop sleeps ~30min or is scheduled; 3s here just to tick
    print(f"\n=== THE AEA SLEEPS ===  (persistent memory now {len(state['memory'])} notes across {state['tick']} total ticks)")
    print("continuity proof - the entity's evolving memory (survives restart via aea_state.json):")
    for m in state["memory"][-n_ticks:]:
        print(f"  {m}")

if __name__ == "__main__":
    main()
