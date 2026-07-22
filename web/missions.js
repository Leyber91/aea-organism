/* missions.js — THE PROBE · mission data (Acts 0–I)
   Data only: the engine lives in world.html. Every DO/PROVE acts on REAL endpoints —
   nothing here is simulated (the AEA honesty law). Beat kinds:
   brief | learn | do | observe | prove.  All text is terminal-voice: lowercase, terse. */
"use strict";
window.MISSIONS = [

/* ================= ACT 0 · GENESIS ================= */
{ id:"M0.1", act:"0", title:"FIRST LIGHT", node:"socket",
  objective:"reach the signal at the edge of the dark",
  beats:[
   { kind:"brief", lines:[
     "cold boot. no memory of why.",
     "the field is dark. one structure at the edge is drawing power.",
     "it is keyless. it accepts anyone who asks."] },
   { kind:"learn", title:"the entire protocol", code:
`POST https://text.pollinations.ai/openai
{ "model": "openai-fast",
  "messages": [ { "role": "user",
                  "content": "..." } ] }`,
     note:"a prompt goes in. tokens come out. everything above this is architecture." },
   { kind:"do", label:"TRANSMIT — one prompt into the dark",
     action:{ type:"node_channel", plant:"pollinations", model:"openai-fast",
              prompt:"Reply with exactly: FIRST LIGHT" } },
   { kind:"prove", assert:"last_ok_text",
     pass:"something answered. it was listening the whole time.",
     fail:"nothing answered. the dark stays dark. retry the transmission." }
  ],
  rewards:{ reveals:["plant_pollinations"], log:"first light · the socket answers" } },

/* ================= ACT I · POWER ================= */
{ id:"M1.1", act:"I", title:"THE CATALOGUE", node:"console",
  objective:"survey the field the socket belongs to",
  beats:[
   { kind:"brief", lines:[
     "the socket is not alone.",
     "this field is a foundry: fifteen power plants in four privacy rings —",
     "local. no-train. trains. keyless."] },
   { kind:"learn", title:"one registry, machine-readable", code:
`PLANTS = {
 "ollama":  dict(privacy="local",    rpm=None), # private, unlimited
 "nvidia":  dict(privacy="no-train", rpm=40),   # 121 models, 40rpm EACH
 "groq":    dict(privacy="no-train", rpm=30),
 "pollinations": dict(privacy="none", rpm=4),   # the keyless socket
 # ... one line per plant
}`,
     note:"adding a plant is one line. the mind never names a model — that is what model-agnostic means." },
   { kind:"do", label:"SURVEY THE FIELD", action:{ type:"survey" } },
   { kind:"prove", assert:"plants_online",
     pass:"the lit plants answer to this machine. the dark ones await keys — capacity is a set of locks.",
     fail:"no plant answered the survey. is the entity's server running?" }
  ],
  rewards:{ reveals:["foundry_all"], log:"the catalogue · plants revealed" } },

{ id:"M1.2", act:"I", title:"THE CHANNEL", node:"plant_nvidia",
  objective:"reach THE GRID — the largest plant in the field",
  beats:[
   { kind:"brief", lines:[
     "fifteen plants. one language.",
     "every plant speaks the same protocol — so the mind can leave any of them",
     "without changing a line of itself."] },
   { kind:"learn", title:"one function, any model", code:
`def call_openai(plant, model, messages, ...):
    url = PLANTS[plant]["base"] + "/chat/completions"
    if PLANTS[plant]["auth"]:
        headers["Authorization"] = "Bearer " + key(...)
    ...
    return dict(ok, latency, text, tokens, status, error)`,
     note:"local ollama and the nvidia cloud walk the SAME path. only base + auth differ." },
   { kind:"do", label:"SAME PROMPT · THREE PLANTS",
     action:{ type:"channel_multi", prompt:"Reply with exactly: CHANNEL OPEN", max:3 } },
   { kind:"prove", assert:"multi_served",
     pass:"different plants, different latencies, one protocol. the channel is the freedom.",
     fail:"no plant served the prompt. retry — the grid may be resting." }
  ],
  rewards:{ reveals:["roads"], log:"the channel · one language proven" } },

{ id:"M1.3", act:"I", title:"THE METER", node:"meter",
  objective:"find the grid operator at the center of the foundry",
  beats:[
   { kind:"brief", lines:[
     "free power has breakers.",
     "trip one and the plant browns out for every organ at once.",
     "the meter exists so that never happens."] },
   { kind:"learn", title:"the breaker check", code:
`def can_spend(self, plant, model, est_tokens=800):
    with self.lock, file_lock(self.state_path):  # shared truth
        win = self._win(st, plant+":"+model, now) # sliding 60s
        if len(win) >= cap["rpm"]:
            return (False, 60-(now-win[0]), "rpm")`,
     note:"a locked read-modify-write on ONE file. every process sees the same budget." },
   { kind:"do", label:"DRAW TWICE, FAST — load the window",
     action:{ type:"meter_load", plant:"pollinations", model:"openai-fast", shots:2 } },
   { kind:"observe", label:"the window slides. wait it out.",
     action:{ type:"meter_watch", plant:"pollinations", seconds:60 },
     note:"nothing speeds this up. patience is a resource the entity budgets for you." },
   { kind:"prove", assert:"no_throttle",
     pass:"the window slid clean. no breaker tripped. this is why it runs 24/7 on free power.",
     fail:"a plant is cooling from a real 429. the meter is routing around it — wait, then retry." }
  ],
  rewards:{ reveals:["foundry_edges"], log:"the meter · the mana lesson" } },

{ id:"M1.4", act:"I", title:"THE LADDER", node:"nexus",
  objective:"follow the trunk line out of the foundry",
  beats:[
   { kind:"brief", lines:[
     "no organ names a model. ever.",
     "every draw enters one mouth and falls down a ladder of live rods",
     "until something answers. models are fuel — the mind is the structure."] },
   { kind:"learn", title:"the mouth", code:
`def draw(prompt, tier="solid", zone="private"):
    for plant, model in ladder(tier, zone):   # fitness-ranked
        if _cooling(plant, model): continue    # skip cooling rods
        if not _meter.can_spend(...): continue
        r = grid.call_openai(plant, model, ...)
        if r.ok and r.text: return r           # else: fall`,
     note:"the ladder re-ranks itself from every call. rods rot; the mouth routes around the dead." },
   { kind:"do", label:"DRAW THROUGH THE MOUTH",
     action:{ type:"node_energy", prompt:"Reply with exactly: LADDER HOLDS" } },
   { kind:"prove", assert:"last_ok_text",
     pass:"watch the tried-list: that is the real routing history of your draw.",
     fail:"the mouth starved — every rod refused. rare, and honest. retry." }
  ],
  rewards:{ reveals:["trunk"], log:"the ladder · the mouth answered" } },

{ id:"M1.5", act:"I", title:"BOSS · BROWNOUT DRILL", node:"nexus", boss:true,
  objective:"return to the nexus. the drill awaits.",
  beats:[
   { kind:"brief", lines:[
     "the drill: four draws, back to back.",
     "the grid must not leak one unhandled failure —",
     "reroute, cool, fall to the floor, but never break."] },
   { kind:"do", label:"RUN THE DRILL — four draws",
     action:{ type:"drill", shots:4, prompt:"Reply with one word: HOLDING" } },
   { kind:"prove", assert:"drill_clean",
     pass:"zero leaks. the foundry stands. ACT I COMPLETE — restorable coherence, proven live.",
     fail:"a draw broke through unhandled. the grid is weaker than it claims today. run it again." }
  ],
  rewards:{ reveals:["foundry_full","archive_tease"], act_complete:"I",
            log:"brownout drill passed · act I complete" } }
];
