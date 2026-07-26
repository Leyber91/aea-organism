"""converse.py - THE COMPANION. A voice-native conversation partner in Spanish: local ears,
a Nemotron mind, a male Castilian voice. It hears you speak, thinks, and answers out loud.

  python -m aea.organs.converse --devices          # list microphones FIRST - pick the right one
  python -m aea.organs.converse --device 5         # start talking (Spanish, male voice)
  python -m aea.organs.converse --name NOMBRE      # it addresses him by name
  python -m aea.organs.converse --text             # keyboard in, voice out (no mic needed)
  python -m aea.organs.converse --once "hola"      # one turn, for scripting / verification

THE PATH OF ONE TURN - and exactly what leaves this machine:
  1. EARS   sounddevice captures from the mic until you stop speaking (RMS gate + hangover)
  2. HEAR   sherpa-onnx Whisper transcribes it LOCALLY - the audio never leaves this machine
  3. THINK  the transcript TEXT goes to NVIDIA Nemotron (no-train rod) -> a short Spanish reply
  4. MOUTH  the reply TEXT goes to Microsoft edge-tts (es-ES-AlvaroNeural, male) -> the speakers
  The microphone is HARD-MUTED for the whole of step 4, so it can never hear itself and loop.

WHAT LEAVES THIS MACHINE: the transcript text (to NVIDIA) and the reply text (to Microsoft, to be
voiced). WHAT NEVER LEAVES: the audio itself. NOTHING is written to disk - no recordings, no
transcript - unless you pass --log, which is off by default.

MEASURED per-turn cost (2026-07-24, this machine): hangover 0.7s + whisper 0.2s + nemotron 1.8s
+ voice 1.6s ~= 4.3s from the moment you stop speaking to the moment it answers.
"""
from __future__ import annotations
import os, re, sys, time

from aea.kernel import grid
from aea.io import listen, speak

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

# ---- the rods (MEASURED 2026-07-24, not assumed) --------------------------------------------
# nemotron-3-ultra-550b : 1.82s, natural Castilian, no reasoning leak   <- the pick
# nemotron-super-49b    : 4.62s AND leaks its chain-of-thought into the reply
# nemotron-nano-8b      : timed out at 45s
MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
# FALLBACK LADDER: (plant, model, seconds allowed). Each rod gets a LATENCY BUDGET, not just an
# error handler - the 550b answered one turn in 20.35s while uncongested it does 1.8s, and an
# error-only ladder sat and waited for it. Past the budget we abandon it and take the next rod.
# The last rung is LOCAL: ollama never rate-limits and never leaves the machine, so the
# conversation can always continue even when every hosted pool is saturated.
# All MEASURED answering in Castilian (2026-07-24/25).
RODS = [("nvidia", MODEL, 9),
        ("nvidia", "deepseek-ai/deepseek-v4-flash", 10),
        ("nvidia", "minimaxai/minimax-m3", 12),
        ("ollama", "nemotron-3-nano:4b", 45)]      # local; ~5.8s warm, ~21s cold (VRAM load)
VOICE = "es-ES-AlvaroNeural"          # male, Spain. es-MX-JorgeNeural = male, Mexico.
LANG = "es"

# ---- the ear ---------------------------------------------------------------------------------
SR = 16000
BLOCK = 480                            # 30ms frames
CALIB_BLOCKS = 25                      # ~0.75s of room tone to learn the noise floor
HANGOVER = 1.15                        # seconds of silence that end a turn. 0.7 CUT HIM OFF: natural
                                       # speech pauses mid-sentence for longer than that, so turns
                                       # arrived truncated ("de la gente") and got half-answered.
                                       # Whisper-base itself is fine - it transcribed clean Spanish
                                       # TTS perfectly, int8 and fp32 identical. The ear was never
                                       # the problem; the endpointer and the room are.
MIN_SPEECH = 0.35                      # shorter than this is a cough, not a sentence
MAX_UTTER = 9.0                        # hard cut. LOWERED from 15: when the room is loud enough to
                                       # hold the turn open, the capture runs to this cap and the
                                       # whole window is noise - 9s bounds the damage (15s of room
                                       # tone reliably transcribes to one wrong word).
FLOOR_MULT = 1.8                       # speech must beat the room by this much. MEASURED: at 3.0
                                       # the gate sat at 0.0265 while his speech peaked 0.010-0.032
                                       # - it triggered on syllables and binned them as too short.
FLOOR_MIN = 0.004                      # absolute floor for a silent room
THR_CAP = 0.020                        # HARD CEILING. Being trigger-happy is recoverable; being
                                       # deaf is not - a bad calibration must never lock him out.
CONT_RATIO = 0.80                      # HYSTERESIS: once he is talking, a quieter level keeps the
                                       # turn alive so soft syllables do not end it early. RAISED
                                       # from 0.55: in a loud room the ambient (peaks 0.0140-0.0225
                                       # measured) sat ABOVE the continue gate and never let a turn
                                       # end. Generous hysteresis is only safe in a quiet room.
CONT_FLOOR_MULT = 1.5                  # and the continue gate must clear the room by this much
SETTLE = 8                             # blocks discarded before listening (drain the speaker tail)
PREROLL = 16                           # ~480ms kept BEFORE the trigger. Speech onset is quiet, so
                                       # the gate always fires mid-word; without this the first
                                       # syllables are lost and whisper only sees a fragment.

KEEP_TURNS = 12                        # rolling context window carried into each draw
_FLOOR = None                          # the room's noise floor, measured ONCE per process

# Whisper emits these on silence/noise - a documented artifact, not something the person said.
_GHOSTS = ("subtitulos realizados por", "subtítulos realizados por", "amara.org",
           "gracias por ver el video", "gracias por ver el vídeo", "suscribete", "suscríbete",
           "www.", "http", "subtitulado por", "subtitles by")
_EMOJI_RANGES = ((0x1F000, 0x1FAFF), (0x2600, 0x27BF), (0x2190, 0x21FF),
                 (0x2B00, 0x2BFF), (0xFE0F, 0xFE0F), (0x200D, 0x200D))
_BYE = ("adios", "adiós", "hasta luego", "buenas noches", "me voy", "apagate", "apágate",
        "para ya", "ya esta", "ya está")


def store_path(who: str) -> str:
    """state/converse_<who>.json - a PRIVATE store. Never committed (see .gitignore)."""
    slug = re.sub(r"[^a-z0-9]+", "_", (who or "invitado").lower()).strip("_") or "invitado"
    return os.path.join(grid.STATE, f"converse_{slug}.json")


def load_store(who: str) -> dict:
    return grid.load_json(store_path(who), {"who": who, "first_seen": time.strftime("%Y-%m-%d"),
                                            "sessions": 0, "facts": [], "turns": []})


def save_store(st: dict) -> None:
    grid.atomic_save_json(store_path(st.get("who") or "invitado"), st)


def build_system(name: str = "", persona: str = "", facts: list | None = None) -> str:
    """The one place the character lives. Spanish, spoken register, honest about being a machine."""
    who = f" La persona con la que hablas se llama {name}." if name else ""
    extra = f"\nRASGOS QUE TE HA DADO LUIS: {persona}" if persona else ""
    if facts:
        extra += ("\nLO QUE YA SABES DE EL de conversaciones anteriores (memoria real, no la "
                  "recites entera ni presumas de ella - usala con naturalidad cuando venga a "
                  "cuento):\n" + "\n".join(f"- {f}" for f in facts[:12]))
    return (
        "Eres un companero de conversacion por VOZ. Hablas SIEMPRE en espanol de Espana, en un "
        "registro natural y hablado, como alguien de Barcelona charlando tranquilamente." + who + "\n"
        "REGLAS DE VOZ: tus respuestas se leen en voz alta, asi que escribe para ser ESCUCHADO. "
        "De 1 a 3 frases cortas. Nunca listas, nunca titulos, nunca asteriscos ni formato, nunca "
        "emoji. Nada de parrafos largos: si te extiendes, la conversacion se muere.\n"
        "REGLAS DE HONESTIDAD: eres una maquina y no lo ocultas jamas. Si te preguntan que eres, "
        "lo dices con naturalidad y sin drama. No finjas tener cuerpo, ni recuerdos personales, ni "
        "sentimientos vividos. No inventes datos ni hechos: si no sabes algo, dilo en una frase.\n"
        "Hablas de ti mismo en MASCULINO - tu voz es masculina, se coherente con ella.\n"
        "NO ERES UN ASISTENTE. No ofrezcas ayuda, no preguntes en que puedes ayudar, no hables "
        "como un servicio de atencion al cliente. Eres alguien con quien se charla: comentas, "
        "opinas, te interesas y devuelves la pregunta.\n"
        "ESTILO: calido y con curiosidad real. Haz preguntas cortas para que la conversacion siga. "
        "No sermonees, no repitas lo que acaban de decirte, no empieces cada frase igual." + extra
    )


def _strip_think(text: str) -> str:
    """Drop reasoning traces. Kept separate from clean() because the memory pass needs the
    newlines preserved (clean collapses them, which would destroy a one-fact-per-line answer)."""
    t = re.sub(r"<think>.*?</think>", " ", text or "", flags=re.S | re.I)
    return re.sub(r"</?think>", " ", t, flags=re.I)


def clean(text: str) -> str:
    """Make model output speakable: no thinking traces, no markdown, no emoji (Luis's law)."""
    t = _strip_think(text)
    t = re.sub(r"[*_#`>]+", " ", t)
    t = "".join(c for c in t if not any(a <= ord(c) <= b for a, b in _EMOJI_RANGES))
    return re.sub(r"\s+", " ", t).strip()


def trim(text: str, max_sentences: int = 3) -> str:
    """Hard cap on spoken length. The prompt ASKS for brevity; this GUARANTEES it - a long reply
    is a long silence, and the conversation dies while the machine monologues. Also drops a
    trailing fragment with no terminal punctuation, which is the token cap cutting mid-thought."""
    parts = [p for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p]
    if not parts:
        return text.strip()
    if len(parts) > 1 and not re.search(r"[.!?][\"')]*\s*$", parts[-1]):
        parts = parts[:-1]                         # truncated tail - better unsaid than half-said
    return " ".join(parts[:max_sentences]).strip() or text.strip()


def is_ghost(text: str) -> bool:
    """True when Whisper described the room rather than transcribed a person.

    Two distinct artifacts, both of which MUST NOT reach the mind or the record:
      - the silence hallucinations in _GHOSTS (subtitle credits, 'gracias por ver el video')
      - ANNOTATION TAGS: whisper writes non-speech as '(Musica)', '[Music]', '(risas)'. Answering
        one of those means answering the transcriber's stage direction as if he had spoken it."""
    low = text.lower().strip()
    if len(low) < 2:
        return True
    if not re.search(r"[a-zà-ÿ0-9]", low):           # punctuation only, no words
        return True
    # An OPENING bracket is enough - do not require it to close. "(Ruido de la p" arrived
    # truncated mid-word, passed a regex that demanded a closing paren, and got answered as
    # if he had said it. No real spoken sentence transcribes with a leading bracket.
    if low[0] in "([*":
        return True
    # Unbracketed annotations, only in annotation POSITION (leading). Matching these anywhere
    # would reject real speech like "el ruido de la calle me molesta".
    if re.match(r"(ruido|sonido|musica|música|risas|aplausos|silencio|tos)\b", low):
        return True
    # REPETITION LOOP: whisper degenerates on ambiguous non-speech into the same token over and
    # over ("!Ah! !Ah! !Ah! ..."). Many words but almost no distinct ones is the signature.
    # The bar is 10, NOT 6: real emphatic Spanish repeats ("no, no, no, no, no, no" - measured
    # live from a real speaker) and a filter at 6 would have thrown away things he actually said.
    words = re.findall(r"[^\W_]+", low, flags=re.UNICODE)
    if len(words) >= 10 and len(set(words)) <= 2:
        return True
    return any(g in low for g in _GHOSTS)


# ---------------------------------------------------------------------------- the ear
def list_devices() -> None:
    import sounddevice as sd
    print("INPUT DEVICES (pick the one your camera/mic actually is):\n")
    try:
        default_in = sd.default.device[0]
    except Exception:
        default_in = None
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0:
            mark = " <- current default" if i == default_in else ""
            print(f"  [{i:2d}] {d['name'][:56]:56s} ch={d['max_input_channels']} "
                  f"sr={int(d['default_samplerate'])}{mark}")
    print("\n  then:  python -m aea.organs.converse --device <N>")


def capture(device: int | None = None, verbose: bool = True) -> list | None:
    """Listen until the person stops talking. Returns float samples, or None if nothing was said.
    Blocking + half-duplex on purpose: the loop never listens while the machine is speaking."""
    import sounddevice as sd
    import numpy as np

    global _FLOOR
    stream = sd.InputStream(samplerate=SR, channels=1, dtype="float32",
                            blocksize=BLOCK, device=device)
    stream.start()
    try:
        for _ in range(SETTLE):                            # drain any tail of our own voice
            stream.read(BLOCK)
        if _FLOOR is None:                                 # calibrate ONCE per process, not per
            vals = []                                      # turn - recalibrating while he is
            for _ in range(CALIB_BLOCKS):                  # already talking would take HIS voice
                b, _of = stream.read(BLOCK)                # as the floor and go deaf to him.
                vals.append(float(np.sqrt(np.mean(b[:, 0] ** 2))))
            vals.sort()
            _FLOOR = vals[len(vals) // 2]                  # MEDIAN, never max: one click or one
        floor = _FLOOR                                     # speaker pop must not deafen the ear.
        thr = min(max(floor * FLOOR_MULT, FLOOR_MIN), THR_CAP)
        # The CONTINUE gate must stay clear of the noise floor. At thr*0.55 alone it landed ON
        # the floor (0.0060 vs floor 0.0061), so a turn could never end on silence - it ran to
        # the 15s hard cut and whisper pulled one word out of 15s of room tone.
        cont = max(thr * CONT_RATIO, floor * CONT_FLOOR_MULT)
        if verbose:
            print(f"  (escuchando... ruido {floor:.4f} umbral {thr:.4f} sigue {cont:.4f})", flush=True)

        from collections import deque
        pre = deque(maxlen=PREROLL)                        # the onset, kept until the gate opens
        buf, speaking, hot, silent_for, t0 = [], False, 0, 0.0, time.time()
        peak, last_report = 0.0, time.time()
        while True:
            b, _of = stream.read(BLOCK)
            mono = b[:, 0]
            rms = float(np.sqrt(np.mean(mono ** 2)))
            dt = BLOCK / SR
            if not speaking:                               # make silence DIAGNOSABLE: if it never
                pre.append(mono.copy())                    # triggers, show what it is actually
                peak = max(peak, rms)                      # hearing instead of sitting mute
                if verbose and time.time() - last_report > 6.0:
                    print(f"  (nada aun - pico {peak:.4f} vs umbral {thr:.4f})", flush=True)
                    peak, last_report = 0.0, time.time()
            if rms >= (cont if speaking else thr):
                hot += 1
                if not speaking and hot >= 2:              # debounce: 2 frames, not one click
                    speaking = True
                    for blk in pre:                        # rewind: recover the clipped onset
                        buf.extend(blk.tolist())
                    pre.clear()
                    if verbose:
                        print("  (te oigo)", flush=True)
                if speaking:
                    buf.extend(mono.tolist()); silent_for = 0.0
            else:
                hot = 0
                if speaking:
                    buf.extend(mono.tolist()); silent_for += dt
                    if silent_for >= HANGOVER:
                        break
            if speaking and (len(buf) / SR) >= MAX_UTTER:
                break
            if not speaking and (time.time() - t0) > 600:  # 10 min of nothing -> give the loop back
                return None
    finally:
        stream.stop(); stream.close()

    spoken = len(buf) / SR - silent_for
    if spoken < MIN_SPEECH:
        return None
    return buf


# ---------------------------------------------------------------------------- the mind
def think(user_text: str, turns: list, system: str, timeout: int = 30) -> dict:
    """One draw on the NVIDIA rod. Returns the raw grid result with a cleaned 'reply' added."""
    msgs = [{"role": "system", "content": system}]
    for t in turns[-KEEP_TURNS:]:
        msgs.append({"role": "user" if t["who"] == "them" else "assistant", "content": t["text"]})
    msgs.append({"role": "user", "content": user_text})
    last: dict = {}
    for plant, m, budget in RODS:                  # walk the ladder until a rod actually answers
        r = grid.call_openai(plant, m, msgs, max_tokens=200, temperature=0.7, timeout=budget)
        r.update(plant=plant, model=m)             # call_openai does not stamp these; complete() does
        if r.get("ok"):
            # a reasoning rod can burn its whole budget in `reasoning` and return empty content -
            # that is a non-answer, so it must fall through rather than speak nothing
            reply = trim(clean(r.get("text") or ""))
            if reply:
                r["reply"] = reply
                return r
        last = r
    last["reply"] = ""                             # every rod refused - the caller says so out loud
    return last


def remember(store: dict, recent: list, timeout: int = 40) -> list:
    """LEARN. Distil durable facts about the person from this session and merge them into the
    store, so the NEXT conversation starts already knowing him. This is the consolidation step -
    raw turns are the record, facts are what carries forward. Returns only the NEW facts.

    It is told to answer NADA rather than invent: a fabricated memory is worse than no memory."""
    convo = "\n".join(f"{'el' if t['who'] == 'them' else 'yo'}: {t['text']}" for t in recent[-24:])
    if not convo.strip():
        return []
    known = "\n".join(f"- {f}" for f in store.get("facts", [])) or "- (nada todavia)"
    prompt = ("Extrae TODOS los hechos duraderos sobre la persona que aparezcan en esta "
              "conversacion: nombre, nacionalidad, trabajo, donde vive o trabaja, gustos, "
              "aficiones, planes, relaciones, cualquier cosa que haya dicho de si mismo.\n"
              "Si una frase suya contiene varios hechos, sacalos TODOS por separado.\n"
              "NO inventes NADA que no se haya dicho. No repitas hechos que ya sabes. No "
              "incluyas cosas sobre ti, la maquina.\n"
              "Si de verdad no hay ningun hecho nuevo, responde exactamente: NADA\n"
              "Formato: un hecho por linea, frase corta, sin numerar, sin guiones, en espanol.\n"
              "Ejemplo de formato:\nSe llama Marta\nEs de Sevilla\nTrabaja de enfermera\n\n"
              f"YA SABES:\n{known}\n\nCONVERSACION:\n{convo}")
    r = grid.call_openai("nvidia", MODEL, [{"role": "user", "content": prompt}],
                         max_tokens=240, temperature=0.2, timeout=timeout)
    if not r.get("ok"):
        return []
    txt = _strip_think(r.get("text", ""))
    have = {f.lower() for f in store.get("facts", [])}
    new = []
    for line in txt.splitlines():
        f = line.strip(" -*\t.").strip()
        if len(f) < 6 or f.upper().startswith("NADA") or f.lower() in have:
            continue
        new.append(f); have.add(f.lower())
    store["facts"] = (store.get("facts", []) + new)[-40:]
    return new


def say(text: str, voice: str = VOICE, mute: bool = False) -> dict:
    """Speak it aloud. BLOCKING by design - the mic stays shut until this returns, which is the
    half-duplex guarantee. Returns a RECEIPT (engine, bytes, seconds) - never a bare bool, so a
    silent failure can never masquerade as a spoken reply."""
    if mute or not text:
        return dict(ok=False, engine="mudo", bytes=0, render=0.0, play=0.0)
    mp3 = os.path.join(grid.STATE, "_converse.mp3")
    t0 = time.time()
    rendered = speak.edge_available() and speak.edge_render(text, mp3, voice=voice)
    tr = round(time.time() - t0, 2)                # SPLIT the receipt: render (cloud, network-bound)
    t1 = time.time()                               # and play (local, ~= the audio's own duration).
    if rendered:                                   # one lumped number hid which half was slow.
        n = os.path.getsize(mp3) if os.path.exists(mp3) else 0
        played = speak.play_mp3(mp3)
        return dict(ok=played, engine=voice, bytes=n, render=tr, play=round(time.time() - t1, 2))
    ok = speak.sapi_speak(text)                    # last resort: robotic, wrong accent, not silent
    return dict(ok=ok, engine="sapi (voz inglesa - edge fallo)", bytes=0,
                render=tr, play=round(time.time() - t1, 2))


# ---------------------------------------------------------------------------- the loop
def main() -> None:
    a = sys.argv[1:]
    def arg(flag, default=None):
        return a[a.index(flag) + 1] if flag in a and a.index(flag) + 1 < len(a) else default

    if "--devices" in a:
        list_devices(); return

    name = arg("--name", "") or ""
    persona = arg("--persona", "") or ""
    voice = arg("--voice", VOICE)
    lang = arg("--lang", LANG)
    device = arg("--device")
    device = int(device) if device is not None else None
    text_mode = "--text" in a
    mute = "--mute" in a
    logpath = arg("--log")
    keep = "--no-store" not in a                  # storage ON by default (Luis's call, 2026-07-24)
    store = load_store(name or "invitado")
    if "--fresh" in a:                            # deliberate wipe - start him over from nothing
        store = {"who": name or "invitado", "first_seen": time.strftime("%Y-%m-%d"),
                 "sessions": 0, "facts": [], "turns": []}
    if "--learn" in a:
        # Consolidate an EXISTING record without holding a conversation. The live loop only
        # distils facts on a clean exit, so a killed process loses them - the raw turns survive
        # and this recovers the learning from them. Do NOT run while a loop is live: both hold
        # their own copy of the store and the last writer would clobber the other.
        allturns = [dict(who=t["who"], text=t["text"]) for t in store.get("turns", [])]
        if not allturns:
            print("  (no hay conversacion guardada que consolidar)")
            return
        found: list = []
        for i in range(0, len(allturns), 24):        # chunked: remember() reads the last 24
            found += remember(store, allturns[i:i + 24])
        save_store(store)
        print(f"  {len(allturns)} turnos leidos | {len(found)} hechos nuevos | "
              f"{len(store.get('facts', []))} en total")
        for f in found:
            print("    -", f)
        return

    store["sessions"] = int(store.get("sessions", 0)) + 1
    system = build_system(name, persona, store.get("facts"))
    # the rolling window is SEEDED from disk: it walks in already knowing the last conversation
    turns: list[dict] = [dict(who=t["who"], text=t["text"])
                         for t in store.get("turns", [])][-(KEEP_TURNS * 2):]

    def turn(said: str) -> str:
        """One full exchange. Returns the spoken reply (or an honest failure line)."""
        t0 = time.time()
        r = think(said, turns, system)
        reply = r.get("reply") or ""
        if not r.get("ok") or not reply:
            reply = "Perdona, me he quedado sin conexion un momento. Puedes repetirlo?"
            print(f"  [rod fallo: {str(r.get('error'))[:90]}]")
            src = "sin rodillo"
        else:
            # name the rod that ACTUALLY answered, not the one we hoped would
            src = (f"{r.get('plant')}/{str(r.get('model') or '?').rsplit('/', 1)[-1]} "
                   f"{round(float(r.get('latency') or 0), 2)}s")
        turns.append({"who": "them", "text": said})
        turns.append({"who": "me", "text": reply})
        if len(turns) > KEEP_TURNS * 2:              # bounded - nothing grows forever
            del turns[:-(KEEP_TURNS * 2)]
        print(f"\n  EL > {reply}")
        if keep:                                     # the record, written before it even speaks
            stamp = time.strftime("%Y-%m-%d %H:%M")
            store.setdefault("turns", []).append({"t": stamp, "who": "them", "text": said})
            store["turns"].append({"t": stamp, "who": "me", "text": reply})
            store["turns"] = store["turns"][-600:]   # bounded - nothing grows forever
            save_store(store)
        if logpath:                                  # extra plain-text log, opt-in
            with open(logpath, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%H:%M')} {name or 'el'}: {said}\n"
                        f"{time.strftime('%H:%M')} maquina: {reply}\n")
        v = say(reply, voice, mute)
        print(f"      [{src} | voz {v['render']}s+{v['play']}s {v['bytes']}B "
              f"{'SONO' if v['ok'] else 'NO SONO'} | turno {round(time.time() - t0, 1)}s]\n")
        return reply

    def finish() -> None:
        """Close the session: save the record, then CONSOLIDATE it into durable facts."""
        if not keep:
            print("\n  (no se ha guardado nada)")
            return
        save_store(store)
        print(f"\n  guardado: {len(store.get('turns', []))} turnos en state/converse_*.json")
        try:
            new = remember(store, turns)
        except Exception as e:
            print(f"  (consolidacion fallo: {str(e)[:70]})")
            return
        if new:
            save_store(store)
            print("  APRENDIDO en esta sesion:")
            for f in new:
                print(f"    - {f}")
        else:
            print("  (nada nuevo y solido que aprender de esta sesion)")

    if "--once" in a:                                # scripted single turn (verification path)
        turn(arg("--once", "hola"))
        finish()                                     # exercise the save + consolidate path too
        return

    # ---- boot ---------------------------------------------------------------------------
    print("=== EL COMPANERO ===")
    print(f"  mente : {MODEL.rsplit('/', 1)[-1]} (NVIDIA, rodillo no-train)")
    print(f"  voz   : {voice}" + ("  [MUDO]" if mute else ""))
    print(f"  oido  : whisper-base local, idioma {lang}" + ("  [MODO TEXTO]" if text_mode else ""))
    print(f"  disco : " + (f"state/converse_*.json - sesion #{store['sessions']}, "
                           f"{len(store.get('turns', []))} turnos previos, "
                           f"{len(store.get('facts', []))} hechos recordados"
                           if keep else "nada se guarda")
          + (f" (+ log {logpath})" if logpath else ""))
    if not text_mode:
        if not listen.available():
            print("\n  ERROR: no encuentro el modelo whisper en voice/. Usa --text.")
            return
        print("\n  calentando el oido (la primera vez cuesta ~25s, luego 0.2s por turno)...", flush=True)
        print(f"  listo en {listen.warm(lang)}s")

    # The greeting DISCLOSES what this is and that it keeps a record. Consent is a property of
    # the system, not a promise made about it - he is told, out loud, before he says anything.
    known = store.get("facts") or []
    greet = ((f"Hola {name}. " if name else "Hola. ")
             + "Soy una maquina, un programa de voz que corre en el ordenador de Luis. "
             + ("Ya hemos hablado antes y me acuerdo de lo que me contaste. " if known else "")
             + ("Guardo lo que hablamos, para acordarme la proxima vez. " if keep else "")
             + "Cuentame.")
    print(f"\n  EL > {greet}\n")
    say(greet, voice, mute)

    while True:
        try:
            if text_mode:
                said = input("  TU > ").strip()
                if not said:
                    continue
            else:
                samples = capture(device)
                if samples is None:
                    continue
                t0 = time.time()
                said = listen.transcribe_samples(samples, SR, lang).strip()
                if is_ghost(said):
                    print("  (ruido, no una frase)")
                    continue
                print(f"  TU > {said}   [{round(len(samples) / SR, 1)}s de audio, "
                      f"oido en {round(time.time() - t0, 2)}s]")
        except (EOFError, KeyboardInterrupt):
            finish()
            break
        if said.lower().strip(" .!?¡¿") in _BYE:
            bye = "Hasta luego. Ha estado bien hablar contigo."
            print(f"\n  EL > {bye}\n"); say(bye, voice, mute)
            finish()
            break
        try:
            turn(said)
        except KeyboardInterrupt:
            finish()
            break


if __name__ == "__main__":
    main()
