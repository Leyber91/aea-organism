"""checkpoint.py - C-80. THE ONE MUTABLE OBJECT EVERY LAYER READS AND WRITES.

The census records C-80 as EMBODIED. `grep -rl checkpoint aea/` returned zero files. What exists instead
is thirty-five separate JSON files under state/, each written alone and read alone. That is the largest
contradiction in the whole 86-item audit, and roughly forty items sit downstream of it.

This is the minimum honest version, built to be TESTED rather than to be complete (x06). It is L5 on the
derivation ladder - the first rung a bigger model cannot climb for you. A 550b saturates every one-call
task we can pose and still cannot remember what it concluded a minute ago; that is not a weakness of the
rod, it is the shape of L0.

TWO THINGS IT RECORDS THAT A PLAIN DICT WOULD NOT, and both exist because of law IV:

  `fuel_trail`  every revision records WHICH ROD wrote it. Chapter I proved the same composition on
                different fuel is a different organism, so the question "is this one self?" is exactly
                the question "can state written on one fuel be continued on another?" Without the trail
                that question cannot even be asked of the record.
  `history`     append-only revisions. A checkpoint that only holds its latest value cannot answer
                whether it DRIFTED, and drift is the failure mode that matters over a long chain.
"""
from __future__ import annotations

import os
import time

from aea.kernel import grid


def _path(name: str) -> str:
    d = os.path.join(grid.STATE, "checkpoints")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "%s.json" % name)


class Checkpoint:
    """One object. Every step reads it, every step writes it, and it survives the process."""

    def __init__(self, name: str, initial: dict | None = None, *, persist: bool = True):
        self.name, self.persist = name, persist
        self._st = grid.load_json(_path(name), None) if persist else None
        if self._st is None:
            self._st = {"name": name, "value": dict(initial or {}), "revision": 0,
                        "history": [], "fuel_trail": [],
                        "created": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
            self._flush()

    def _flush(self) -> None:
        if self.persist:
            grid.atomic_save_json(_path(self.name), self._st)

    def read(self) -> dict:
        return dict(self._st["value"])

    def write(self, *, rod: str | None = None, note: str = "", **fields) -> dict:
        """Merge fields into the one object. `rod` is who wrote it - required for the fuel question."""
        self._st["value"].update(fields)
        self._st["revision"] += 1
        self._st["history"].append({"revision": self._st["revision"], "wrote": sorted(fields),
                                    "value": dict(self._st["value"]), "rod": rod, "note": note})
        if rod and (not self._st["fuel_trail"] or self._st["fuel_trail"][-1] != rod):
            self._st["fuel_trail"].append(rod)
        self._flush()
        return self.read()

    @property
    def revision(self) -> int:
        return self._st["revision"]

    def history(self) -> list:
        return list(self._st["history"])

    def fuel_trail(self) -> list:
        """Every rod that has written this object, in order. One entry = one self, so far as fuel goes;
        more than one entry and the identity claim is doing real work."""
        return list(self._st["fuel_trail"])

    def crossed_fuel(self) -> bool:
        return len(self._st["fuel_trail"]) > 1

    def drift(self, key: str) -> list:
        """The value of one key across every revision. The only way to see a slow wrong turn."""
        return [(h["revision"], h["value"].get(key), h["rod"]) for h in self._st["history"]]


def wipe(name: str) -> None:
    """Remove a test checkpoint. Never used on real state - the sacred save is not managed here."""
    p = _path(name)
    if os.path.exists(p) and name.startswith("x0"):
        os.remove(p)
