"""persona.py - A PERSISTENT SELF FOR ONE SPEAKER, and the thing that separates four entities from
four costumes on one actor.

Luis, 2026-07-30: "same model, you put a filter prompt to put different personalities, then each of
them has to keep memory of the conversation and interactions with the others. So one model plus the
aspect of the exterior, which is the other three models."

He is right that the model can be shared, and that is worth saying plainly because it is the
counter-intuitive part: IDENTITY DOES NOT LIVE IN THE WEIGHTS. Two characters on the same model
with different persistent memories diverge much further than two characters on different models
with no memory at all. A model is a capacity for producing text; a self is what constrains which
text gets produced. That constraint is what this module holds.

THREE THINGS MAKE A SPEAKER, and they are stored separately because they bind differently:

  MEMORY        what happened. Informs. Retrieved by relevance, decays with time.
  IMPRESSIONS   the picture of each other speaker - "the aspect of the exterior". Rebuilt from
                evidence, correctable, and PERSISTED, because an impression that dies with the
                process is not a relationship.
  COMMITMENTS   what THIS speaker has asserted. Does not inform - it BINDS. A character who said
                "stories are attention-seeking" on turn 2 must be answerable to that on turn 40 and
                in next week's session. Consistency with your own prior claims, at a cost to
                contradict, is the operational content of having a self.

WHY THE STORES ARE SEPARATE, ONE FILE PER SPEAKER. A shared log would be one mind with four
voices - which is exactly the trick we are trying to stop doing. Four entities require that what
each one KNOWS differs: GRAVE remembers being contradicted, MIRA remembers who moved the
goalposts, and neither has access to the other's reading of it. Asymmetric knowledge is not a
detail of the implementation, it is the whole of what makes them separate.

RETRIEVAL, AND THE HONEST LIMIT. Scored on recency, importance and relevance, after Park et al.'s
memory-stream design. Relevance here is LEXICAL OVERLAP, not embedding similarity, because this
machine has no embedding model wired in. That is a real weakness and it is stated rather than
hidden: lexical matching misses paraphrase, so a memory about "lying" will not surface for a turn
about "dishonesty". When an embedder lands, `_relevance` is the one function to replace.

THE CLAIM CEILING APPLIES TO THIS FILE MORE THAN ANY OTHER. What is measurable here is CONSISTENCY
WITH PRIOR COMMITMENTS ACROSS SESSIONS. That is a receipt. It is not a self, it is not a concept of
self, and nothing in this module may be described as one.
"""
from __future__ import annotations

import math
import os
import re
import time

from aea.kernel import grid

DIR = os.path.join(str(grid.STATE), "personas")

HALF_LIFE_H = 20.0          # a memory loses half its recency weight in this many hours. Long
                            # enough that yesterday's conversation still pulls, short enough that
                            # it loses to today's.
W_RECENCY = 1.0
W_IMPORTANCE = 1.2          # importance outweighs recency deliberately: the point of scoring at
W_RELEVANCE = 1.6           # all is to beat "the last N turns", which recency alone reduces to.
KEEP = 400                  # records per speaker before the least valuable are dropped


def _words(t: str) -> set:
    return set(w for w in re.findall(r"[a-z']{4,}", (t or "").lower()))


class Persona:
    """One speaker's persistent self. Load, use, save."""

    def __init__(self, name: str, persona: str = "", model: str = "", plant: str = ""):
        self.name = name
        self.persona = persona
        self.model, self.plant = model, plant
        self.path = os.path.join(DIR, f"{re.sub(r'[^a-z0-9]+', '_', name.lower())}.json")
        d = grid.load_json(self.path, {})
        self.memories: list = d.get("memories", [])
        self.impressions: dict = d.get("impressions", {})
        self.commitments: list = d.get("commitments", [])
        self.sessions: int = int(d.get("sessions", 0))
        self.first_seen: str = d.get("first_seen") or time.strftime("%Y-%m-%d")
        if d.get("persona") and not persona:
            self.persona = d["persona"]

    # -------------------------------------------------------------------------------- writing
    def remember(self, text: str, kind: str = "heard", about: str = "",
                 importance: float = 0.0) -> dict:
        """Store one record. `importance` 0-1; when not given it is scored cheaply and
        deterministically rather than with a model call, because a model call per remembered line
        would cost more than the conversation itself (four speakers x every turn)."""
        r = dict(t=time.time(), at=time.strftime("%Y-%m-%d %H:%M"), kind=kind,
                 about=about, text=text.strip(),
                 imp=round(importance if importance > 0 else self._score(text, kind), 3))
        self.memories.append(r)
        return r

    @staticmethod
    def _score(text: str, kind: str) -> float:
        """Cheap importance. Park et al. ask a model to rate poignancy 1-10; that is one call per
        memory and here there are four speakers hearing every line, so it is the wrong trade at
        this scale. These are the features that survive that substitution: a memory ABOUT someone,
        a disagreement, a question, a stated belief, and a personal disclosure are what a later turn
        actually needs to reach for."""
        t = (text or "").lower()
        s = 0.30
        if kind in ("said", "commitment"):
            s += 0.15                                    # my own words bind more than what I heard
        if "?" in t:
            s += 0.10
        if re.search(r"\b(?:i think|i believe|i don't|i do not|actually|disagree|wrong|no,|but )", t):
            s += 0.20                                    # a position, or a clash
        if re.search(r"\b(?:always|never|everyone|nobody|the point is|the truth)\b", t):
            s += 0.10                                    # a generalisation is a claim to be held to
        if re.search(r"\b(?:my|me|i was|i had|i used to|once)\b", t):
            s += 0.10                                    # disclosure - the stuff relationships use
        return min(1.0, s)

    def commit(self, claim: str) -> None:
        """Record a position THIS speaker has taken. Separate from memory on purpose: a memory is
        something to draw on, a commitment is something to answer for."""
        c = claim.strip()
        if len(c) < 12:
            return
        # A COMMITMENT IS FOREVER, SO THE DOOR IS NARROWER THAN THE MOUTH. Measured: a reasoning
        # rod's scratchpad - "The user is asking me to continue the conversation as GRAVE. Let me
        # analyze the situation:" - was spoken, and then stored here as a position GRAVE holds and
        # would be answerable to in every future session. The speaking path strips this now, but
        # this check stays because the two paths must fail independently: a persistent store is the
        # one place where a single unguarded output becomes a permanent belief.
        if re.search(r"\b(?:the user|as the character|let me analyz|i should respond|in character|"
                     r"my (?:line|reply|response) as)\b", c, re.I):
            return
        if any(len(_words(c) & _words(x["claim"])) / max(len(_words(c)), 1) > 0.7
               for x in self.commitments):
            return                                       # already said this - not a new position
        self.commitments.append(dict(at=time.strftime("%Y-%m-%d %H:%M"), claim=c))
        self.commitments = self.commitments[-40:]
        self.remember(c, kind="commitment", importance=0.85)

    def impression_of(self, other: str) -> str:
        return (self.impressions.get(other) or {}).get("text", "")

    def set_impression(self, other: str, text: str) -> None:
        if text and text.strip():
            self.impressions[other] = dict(text=text.strip(), at=time.strftime("%Y-%m-%d %H:%M"),
                                           n=(self.impressions.get(other) or {}).get("n", 0) + 1)

    # -------------------------------------------------------------------------------- reading
    def _relevance(self, q: set, text: str) -> float:
        """LEXICAL overlap. The known weakness of this whole module - see the header. Jaccard, not
        one-sided containment, so a long memory cannot score highly just by being long."""
        w = _words(text)
        if not q or not w:
            return 0.0
        return len(q & w) / len(q | w)

    def recall(self, query: str, k: int = 6, about: str = "") -> list:
        """The memories worth putting in front of this speaker right now.

        Recency decays exponentially, importance is stored, relevance is lexical. Weighted sum
        after Park et al., whose ablation is the reason this exists at all: removing the memory
        stream hurt their agents' believability more than removing planning did."""
        now = time.time()
        q = _words(query)
        scored = []
        for m in self.memories:
            rec = 0.5 ** ((now - m.get("t", now)) / 3600.0 / HALF_LIFE_H)
            rel = self._relevance(q, m.get("text", ""))
            if about and m.get("about") == about:
                rel += 0.25                              # asked about a person -> what they did
            s = W_RECENCY * rec + W_IMPORTANCE * m.get("imp", 0.3) + W_RELEVANCE * rel
            scored.append((s, m))
        scored.sort(key=lambda x: -x[0])
        return [m for _s, m in scored[:k]]

    def contradictions(self, text: str) -> list:
        """Prior commitments this line may clash with. NOT a truth check - a flag for the speaker
        to be reminded of what it already said. Lexically overlapping plus an opposing polarity
        marker is a weak signal deliberately: the cost of a false flag is one wasted line of
        prompt, and the cost of missing one is a character that contradicts itself."""
        w = _words(text)
        neg = bool(re.search(r"\b(?:not|never|no|disagree|wrong|actually)\b", text.lower()))
        out = []
        for c in self.commitments:
            ov = len(w & _words(c["claim"])) / max(len(w | _words(c["claim"])), 1)
            if ov > 0.18 and neg != bool(re.search(r"\b(?:not|never|no)\b", c["claim"].lower())):
                out.append(c["claim"])
        return out[:3]

    def brief(self, others: list, query: str = "") -> str:
        """The block that goes into this speaker's prompt. Everything it is bringing to this turn.

        Deliberately SHORT. The temptation is to hand over the whole store, and that produces a
        speaker who recites its memory instead of talking - the same failure as a system prompt that
        describes a signal it is not given. What it needs is a few things it might reach for, not
        everything it holds."""
        L = []
        if self.sessions > 1:
            L.append(f"You have talked with these people before ({self.sessions} times, "
                     f"first on {self.first_seen}).")
        seen = [f"  {o}: {self.impression_of(o)}" for o in others if self.impression_of(o)]
        if seen:
            L.append("WHAT YOU HAVE COME TO THINK OF THEM (private, never read aloud):")
            L += seen
        if self.commitments:
            L.append("WHAT YOU HAVE ALREADY SAID YOU THINK - stay answerable to it. If you have "
                     "changed your mind, say so out loud rather than quietly:")
            L += [f"  - {c['claim']}" for c in self.commitments[-4:]]
        mem = self.recall(query, k=4) if query else []
        old = [m for m in mem if time.time() - m.get("t", 0) > 900]
        if old:
            L.append("THINGS YOU REMEMBER that may be worth bringing up:")
            L += [f"  - ({m['at']}) {m['text'][:120]}" for m in old[:3]]
        return "\n".join(L)

    # -------------------------------------------------------------------------------- keeping
    def prune(self) -> None:
        """Drop the least valuable when over KEEP. Never drops commitments - those are the spine."""
        if len(self.memories) <= KEEP:
            return
        now = time.time()
        self.memories.sort(key=lambda m: (m.get("kind") == "commitment",
                                          m.get("imp", 0) + 0.5 ** ((now - m.get("t", now))
                                                                    / 3600.0 / HALF_LIFE_H)))
        self.memories = self.memories[-KEEP:]
        self.memories.sort(key=lambda m: m.get("t", 0))

    def save(self) -> str:
        os.makedirs(DIR, exist_ok=True)
        self.prune()
        grid.atomic_save_json(self.path, dict(
            name=self.name, persona=self.persona, model=self.model, plant=self.plant,
            first_seen=self.first_seen, sessions=self.sessions,
            impressions=self.impressions, commitments=self.commitments, memories=self.memories))
        return self.path

    def open_session(self) -> None:
        self.sessions += 1

    def stats(self) -> dict:
        return dict(name=self.name, sessions=self.sessions, memories=len(self.memories),
                    commitments=len(self.commitments), impressions=len(self.impressions))


def load_all(names: list) -> dict:
    return {n: Persona(n) for n in names}


def wipe(name: str = "") -> int:
    """Start someone over from nothing. Deliberate, never automatic."""
    if not os.path.isdir(DIR):
        return 0
    n = 0
    for f in os.listdir(DIR):
        if name and not f.startswith(re.sub(r"[^a-z0-9]+", "_", name.lower())):
            continue
        os.remove(os.path.join(DIR, f)); n += 1
    return n


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--wipe" in sys.argv:
        i = sys.argv.index("--wipe")
        who = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
        print(f"wiped {wipe(who)} persona file(s)")
    elif os.path.isdir(DIR):
        for f in sorted(os.listdir(DIR)):
            p = Persona(f.replace(".json", ""))
            s = p.stats()
            print(f"  {s['name']:8s} sessions {s['sessions']:3d}  memories {s['memories']:4d}  "
                  f"commitments {s['commitments']:3d}  knows {s['impressions']} others")
            for o, imp in p.impressions.items():
                print(f"      of {o:8s} ({imp.get('n',0)}x) {imp['text'][:88]}")
    else:
        print("no personas yet - run `python -m aea.lab.party`")
