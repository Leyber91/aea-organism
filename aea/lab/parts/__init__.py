"""Importing this package registers every part. Adding a module is all it takes to seat one."""
from aea.lab.parts.base import (STAGES, Ctx, Part, check_against_catalogue,  # noqa: F401
                                load_catalogue, unmet, wire)
from aea.lab.parts import capacity, carry, dna, fire, judge, read, repair, shape  # noqa: F401,E402
from aea.lab.parts.dna import classify_seat, edges  # noqa: F401,E402

__all__ = ["STAGES", "Ctx", "Part", "wire", "unmet", "load_catalogue", "check_against_catalogue"]
