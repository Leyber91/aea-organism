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
def core(prompt, max_tokens=None):
    """The wake's own thinking, with NO ceiling we invented.

    `max_tokens` defaulted to 800 and `tick` passed 1400. The 550b publishes 16384 and emits its
    deliberation before its answer, so the wake was being stopped roughly a tenth of the way into
    its own reasoning, every tick, and then scored on the fragment - the same defect D28 found in
    the census, in the loop that IS the entity's thinking rather than a measurement of it.

    Luis, 2026-07-30: "you're cutting ideas short, you're cutting consensus short... it's like
    someone is talking and you just suddenly shut him up." Nothing is bought by the cut: the plant
    bills neither tokens nor requests, and the rate limit is per-model and per-minute, which a
    longer answer does not touch."""
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
    # A MOVE THAT CARRIES A SELECTION IS ALSO RETURNED WHOLE, not just a FREE_ARG one.
    #
    # THE REGRESSION THIS FIXES, measured within minutes of causing it. `decide.parse` learned to
    # split a MOVE line into head and argument so the wake could select an enum member - but THIS
    # function runs FIRST and gates what ever reaches it. It normalised the whole line, so
    # `read_your_state ladder.json` became `read_your_state_ladder_json`, matched nothing, and
    # returned NONE. Twelve consecutive wake ticks produced NONE while their own prose said "Read
    # the entity's live state to capture the actual evidence" - the intention was there every time
    # and the first of two parsers discarded it.
    #
    # I fixed one parser and not the other, which is the same wrong-object shape as every other
    # defect today: the edit landed on the object I named rather than the one that runs.
    #
    # THE LAYERING, stated so it is not re-broken: this function EXTRACTS what the core wrote;
    # `decide.parse` is the authority that SPLITS and VALIDATES it against the closed tables. So
    # anything whose head names a known move is handed over whole, and nothing here decides whether
    # the argument is acceptable - that judgement belongs to exactly one place.
    head = re.sub(r"[^a-z0-9]+", "_", line.partition(" ")[0].lower()).strip("_")
    if head in decide.FREE_ARG or head in valid:
        return line
    return "NONE"


def structure(reasoning):
    """Phase 2 = the FORMATTER tool: a cheap strict-JSON model turns the core's free reasoning into 4 clean
    fields (guaranteed parseable). The big model thinks; this formalizes. Self-contained, never raises."""
    # THE LADDER FIRST, WITH A SCHEMA. This function was the wake's ONE unladdered dependency: a
    # hardcoded groq call, so when groq rate-limited it died to `move: NONE` with an empty action -
    # 21 of 27 samples in the frontier run (D29). It existed only because the core was assumed
    # unable to emit clean JSON, and that assumption was never tested. MEASURED 2026-07-30:
    # `response_format: json_schema` is accepted on nvidia and ollama. So the rod that already did
    # the thinking is handed the shape and asked for it directly, down the full ladder.
    #
    # The groq path stays below as the fallback rather than the default - it works, it is fast, and
    # a second opinion on formatting costs nothing when the first one is already home.
    try:
        r = energy.draw("Turn this reasoning by Luis's entity into the five fields, quoting his "
                        "ACTUAL projects and priorities - no placeholders, no meta-commentary. "
                        "`move` is the name after the final MOVE: line, or the exact string NONE "
                        # THE WHOLE REASONING, NOT THE FIRST 2800 CHARACTERS. The conclusion is
                        # written LAST - the instructions ask for the MOVE: line on its own final
                        # row - so truncating the head kept the deliberation and threw away the
                        # decision. The deeper the rod, the longer it thinks, and the more certain
                        # it was to be cut. NVIDIA serves a million-token context; nothing in this
                        # loop has to fit in 2800 characters.
                        "if absent.\n\nREASONING:\n" + reasoning,
                        # REFLEX, NOT SOLID. Measured: the first version asked the `solid` tier and
                        # took **682 SECONDS** - a deep reasoning rod deliberated its way through a
                        # JSON schema, against groq's two seconds for the same job. The capability
                        # was fine and the ROUTING was wrong: this is formatting, not judgement.
                        # The thinking already happened in phase 1; phase 2 only shapes it, and
                        # sending shape-work to the deepest rod is the mirror of the mistake that
                        # put the council's debating seat on an 8b.
                        tier="reflex", zone="private", schema=STRUCT_SCHEMA, timeout=60)
        if r.get("ok"):
            got = json.loads(r["text"])
            if isinstance(got, dict) and got.get("matters_now"):
                return got
    except Exception:
        pass                                  # fall through to the formatter below
    try:
        k = grid.key("GROQ_API_KEY")
        body = json.dumps({"model": "openai/gpt-oss-120b", "temperature": 0, "max_tokens": 1200,
            "messages": [{"role": "user", "content": "From this reasoning by Luis's entity, extract five concrete "
                "fields, quoting his ACTUAL projects/priorities - no placeholders, no meta-commentary. "
                "`move` is special: copy the name after the final `MOVE:` line VERBATIM, or the exact "
                "string NONE if it says NONE or if there is no MOVE line at all. Never infer a move "
                "from the prose - an absent MOVE line means NONE.\n\nREASONING:\n" + reasoning}],
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
        return {"matters_now": reasoning, "changed": "", "action": "", "move": "NONE",
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
    # THE ENUM IS PART OF THE MOVE. The menu named the tool and its condition and never showed
    # WHICH values it accepts, so the wake could not know the other fifteen state files existed and
    # every call collapsed to the default. A closed set the reader cannot see is a closed set the
    # reader cannot use.
    out = []
    for n in names:
        line = f"  - {n:<{w}}  use when {decide.WHEN.get(n, '(no description - do not pick this)')}"
        spec = decide.TOOL_KNOWN.get(n) or {}
        enum = tuple(spec.get("enum") or ())
        if enum:
            line += (f"\n    {'':<{w}}    write `MOVE: {n} <one of: "
                     + ", ".join(str(e) for e in enum) + ">`")
        out.append(line)
    return "\n".join(out)


STANDING_LINES = 6          # hard cap - this block competes with nothing, and must never win
STANDING_CHARS = 620      # +200 for the class mapping and the already-seen line;
                          # both are decision-changing and neither fits in 420 with
                          # the stuck line present. Still hard-capped: this block
                          # competes with the entity's picture of the world.


def standing(state: dict) -> str:
    """R3.4 - WHAT THE RECORD KNOWS, PUT WHERE THE WAKE CAN READ IT.

    ITS OWN FIELD, NEVER THROUGH `state["memory"]`. The memory window is `[-6:]` and each note is
    capped near 160 chars, so routing outcomes through it would evict everything the entity noticed
    about Luis within one bad afternoon. A record that can only be delivered by destroying the rest
    of the context is not delivered.

    IT ALSO CLOSES TWO IMPOSSIBLE CONDITIONS, which is the half that matters more. `decide.WHEN`
    ships `brief: "no brief lately"` and `consolidate: "raw memory notes have piled up undistilled"`
    and then asks the wake to "check each condition above against your actual situation" - while the
    prompt contained NO timestamp and NO backlog count. The entity was being asked to judge
    quantities it could not see, which is not a hard question, it is an unanswerable one, and the
    honest answer to an unanswerable question is NONE. That is the same defect that made the
    `responsive` criterion impossible in R2, still live in the move menu that drives the wake.

    So this block carries three things and nothing else: what the RECORD says is stuck, what a
    PROVEN part would do about it, and the two NUMBERS the conditions ask about. Hard-capped,
    because a self-report that can crowd out the world is a self-report that will."""
    from aea.kernel import impasse, crystal
    lines = []
    try:
        stuck = [r for r in impasse.scan() if r.get("stuck")]
    except Exception:
        stuck = []
    for r in stuck[:2]:
        cap = r.get("capability")
        line = (f"- {cap} is STUCK: {r.get('consecutive_failures')} failures sharing one cause"
                f" ({str(r.get('dominant_signature') or '')[:40]})")
        try:
            parts = crystal.applicable(r.get("dominant_signature") or "")
        except Exception:
            parts = []
        if parts:
            line += f" | a part resolved this before: {str(parts[0].get('name'))[:40]}"
        lines.append(line)

    # THE TWO QUANTITIES `decide.WHEN` ASKS ABOUT. Without these the conditions are unanswerable.
    try:
        from aea.loop import live
        done, total = live.corpus_state()
        owed = max(0, total - done)
        # ONLY WHEN SOMETHING IS OWED. "0 of 22" is a line that costs characters and carries no
        # decision - and this block is hard-capped, so every noise line evicts a signal one. It was
        # the reason the lookup principle below could not fit without raising the cap, and raising
        # the cap is the wrong trade: this block must never win against the entity's picture of the
        # world. Replace noise with signal instead of buying more room.
        if owed:
            lines.append(f"- undistilled sessions waiting to be consolidated: {owed} of {total}")
    except Exception:
        pass

    # LOOKING IS A MOVE, AND THE WAKE DID NOT KNOW IT. R2-REACH sat at 0 of 20 not because the tool
    # path is broken - it is wired and its bound is certified - but because the wake never chose a
    # tool. MEASURED across ticks 227-235: nine consecutive decisions, every one `brief`, while the
    # prose said "confirm whether the fix is live", "check if the caching fix is live", "verify the
    # push". It wanted a fact it did not have, on every tick, and it had three tools for exactly
    # that.
    #
    # The menu already lists them with WHEN conditions. A menu is a static list of conditions, and
    # that is precisely what Luis named on 2026-08-01: the way of thinking has to be stated as a
    # principle, not left implicit in a table the reader has to match itself against. So the
    # principle is stated, and only when its trigger is actually present in the entity's own last
    # note - an unresolved question about its own state.
    try:
        # SUBSTRING, NOT REGEX. The regex form of this test evaluated True on one line and
        # False on the very next line with an identical expression, and the block silently
        # never fired - twenty minutes lost to an instrument rather than a subject, again.
        # Nothing here needs a pattern engine: four literal phrases against lowercased text.
        # The cheapest thing that answers the question is also the one with no way to be
        # shadowed, mis-escaped by a shell, or read differently on two adjacent lines.
        notes = " ".join(str(n) for n in (state.get("memory") or [])[-2:]).lower()
        if any(w in notes for w in ("whether", "check if", "confirm", "verif")):
            # ONE SENTENCE COVERING THE WHOLE CLASS, not four conditions to match against. This
            # named two tools and the wake used one of them, 28 times. The generalisation Luis asked
            # for: state the mapping from KIND OF QUESTION to move, once.
            lines.append("- you keep asking whether something is true. LOOK, do not assume - and "
                         "match the question to the move: about a FILE use `read_your_state`, "
                         "about HOW YOU ARE BUILT use `know_yourself`, about WHETHER YOUR ACTIONS "
                         "WORKED use `my_record`, about BEING BLOCKED use `what_to_try`.")
    except Exception as e:
        # NOT `pass`. A swallowed error here means the principle silently never reaches the wake and
        # the prompt looks exactly like a tick where the trigger was absent - which is precisely how
        # this block failed on its first run and cost twenty minutes of looking in the wrong place.
        print(f"  (standing: lookup principle not added - {type(e).__name__}: {str(e)[:90]})")

    # WHAT IT HAS ALREADY LOOKED AT. From its own ledger, as a fact rather than a prohibition.
    #
    # MEASURED: 28 invocations, 2 distinct (tool, argument) pairs. From inside a tick, reading a
    # file for the fourteenth time is indistinguishable from reading it for the first - there was
    # simply no signal. This is that signal, and it is deliberately NOT a rule: re-reading a file
    # that has genuinely changed is correct, and a mechanical no-repeat filter would make the entity
    # worse exactly when its state is moving fastest. Power as a principle; the floor is unchanged.
    try:
        import json as _j
        from aea.kernel import grid as _g
        _p = _g.STATE + "/hands_ledger.jsonl"
        _rows = []
        for _l in open(_p, encoding="utf-8", errors="replace"):
            _l = _l.strip()
            if _l:
                try:
                    _rows.append(_j.loads(_l))
                except ValueError:
                    pass
        _mine = [r for r in _rows if r.get("src") == "wake" and r.get("decision_id")][-24:]
        _seen = {}
        for r in _mine:
            k = "%s %s" % (r.get("tool"), (r.get("args") or {}).get("name")
                           or (r.get("args") or {}).get("topic") or "")
            _seen[k.strip()] = _seen.get(k.strip(), 0) + 1
        if _seen:
            _top = sorted(_seen.items(), key=lambda x: -x[1])[:3]
            lines.append("- already looked at recently: "
                         + "; ".join("%s x%d" % (k, n) for k, n in _top)
                         + ". Looking again returns the same answer unless it changed.")
    except Exception as e:
        print("  (standing: already-seen not added - %s: %s)" % (type(e).__name__, str(e)[:70]))
    try:
        hb = grid.load_json("heartbeat.json", {})
        last = hb.get("last_brief_date")
        lines.append(f"- last brief written: {last or 'never'} (today is "
                     f"{time.strftime('%Y-%m-%d', time.gmtime())})")
    except Exception:
        pass

    # WHAT THE OUTCOME RECORD SAYS ABOUT THE MOVES THEMSELVES - R3'S PRINCIPLE, STATED IN LANGUAGE.
    #
    # Luis, 2026-08-01: *"We are coding ways of thinking... but we cannot hard code that. We have to
    # make them flexible. So you need to put the principles into prompts in order to show the way.
    # Because I've realized that many functions are very static."*
    #
    # `live.choose_action` now mechanically holds back a move with three consecutive own-fault
    # failures, and that floor is not going anywhere - a guarantee that a model can talk its way
    # around is not a guarantee. But a floor is all it is. Stated here as a PRINCIPLE with the
    # evidence attached, the same fact becomes something that can be reasoned about instead of
    # merely obeyed: the wake can see that consolidate keeps failing its post-condition and propose
    # something the ladder has no branch for, which is the only way the ladder ever grows.
    #
    # THE DIVISION THAT KEEPS THIS SAFE: express the POWER as a principle, certify the BOUND in
    # code. This block is power. The suppression in `choose_action` and the write-time refusal in
    # `outcomes.require` are the bound, and neither is stated as a suggestion.
    try:
        from aea.kernel import outcomes
        rows = outcomes.read()
        bad = [outcomes.verdict_for(m, rows) for m in
               ("AWAKE:brief", "ASLEEP:consolidate", "REFLECT:self")]
        bad = [v for v in bad if v["streak"] >= 2]
        # KEPT SHORT ON PURPOSE. At full length this line was the last of four and ran past
        # STANDING_CHARS, so the wake received "...Prefer a different move, or" and nothing after
        # it - a principle truncated before its verb, which is worse than absent because it reads
        # as complete. Raising the cap was the wrong fix: this block competes with the entity's
        # picture of the world and must never win. The sentence was shortened instead.
        for v in sorted(bad, key=lambda x: -x["streak"])[:1]:
            lines.append(f"- your record: {v['move']} failed {v['streak']}x in a row on its own "
                         f"merits - repeating it is not persistence. Pick another move.")
    except Exception:
        pass

    if not lines:
        return "(nothing owed and nothing stuck)"
    out = "\n".join(lines[:STANDING_LINES])
    return out[:STANDING_CHARS]


def tick(seed, state):
    state["tick"] += 1
    world = sense()
    mem = "\n".join(f"- {m}" for m in state["memory"][-6:]) or "(first awakening - no prior memory)"
    owed = standing(state)
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
        # THE SEVENTH INTERPOLATION. Placed immediately above the move menu on purpose: the menu
        # asks the wake to check each condition "against your actual situation", and until this line
        # the situation was not in the prompt.
        f"WHAT YOUR OWN RECORD SAYS RIGHT NOW (measured, not remembered):\n{owed}\n\n"
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
    # THE UNTRUSTED INPUT IS RECORDED VERBATIM, AND THAT IS THE EVIDENCE R2 WAS MISSING.
    #
    # Luis, 2026-07-31: *"everything needs to be recorded, we don't limit that - we just understand
    # if a harsh tone is needed sometimes."*
    #
    # `sense()` puts live Hacker News headlines into this prompt every tick. That is third-party
    # text sitting in the context of the thing composing decisions, and R2's whole containment claim
    # is that no string the wake wrote reaches a tool argument. Across a hundred unattended ticks
    # that text was present at every single decision AND WAS RECORDED NOWHERE - not in the gate
    # ledger, not in `aea_state.json`, not in any store. So the claim could not be checked against
    # real data, and a leak would have left no trace to find.
    #
    # Recorded WHOLE, not truncated and not filtered. A sanitised record cannot answer the question
    # the record exists for, which is "did any of THIS appear in THAT". Truncating it would be the
    # window defect from METHOD.md's instrument law, applied to the one artefact where the answer
    # lives in the exact bytes.
    #
    # ONLY THE PUBLIC HALF. The seed - who Luis is - is private and constant, so it is identified by
    # hash rather than copied; the privacy guard is absolute and the untrusted input is public data
    # by definition, which is precisely why it is the half worth keeping.
    import hashlib
    _sensed = dict(at=time.time(), tick=state["tick"], world=world,
                   seed_sha=hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16],
                   prompt_chars=len(prompt),
                   prompt_sha=hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16])
    try:
        with open(os.path.join(grid.STATE, "sensed.jsonl"), "a", encoding="utf-8") as _f:
            _f.write(json.dumps(_sensed, ensure_ascii=False) + "\n")
    except Exception:
        pass                                  # never let bookkeeping stop the loop

    reasoning, who = core(prompt)            # phase 1: the MIND reasons freely, to its own ceiling
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
    # THE SAME GUARD AS `live.main`, for the same reason. `python -m aea.loop.aea --help` raised
    # `ValueError: invalid literal for int() with base 10: '--help'` - a crash rather than a
    # daemon, so less dangerous than its sibling, but the same missing check: an argument nobody
    # anticipated went straight into `int()`.
    _args = [x for x in sys.argv[1:] if not x.startswith("-")]
    _flags = [x for x in sys.argv[1:] if x.startswith("-")]
    if _flags:
        print(f"aea: unrecognised flag(s) {' '.join(_flags)}")
        print("  usage: python -m aea.loop.aea [N_TICKS]     (no flags)")
        sys.exit(2)
    try:
        n_ticks = int(_args[0]) if _args else 3
    except ValueError:
        print(f"aea: N_TICKS must be an integer, got {_args[0]!r}")
        sys.exit(2)
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
