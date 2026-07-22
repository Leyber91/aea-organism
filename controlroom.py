#!/usr/bin/env python
"""Root shim -> runs aea/controlroom.py (the server lives in the aea/ package now).
Keeps `python controlroom.py [args]` working after the 2026-07-22 reorg."""
import os, sys, subprocess
_aea = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aea")
sys.exit(subprocess.call([sys.executable, os.path.join(_aea, "controlroom.py")] + sys.argv[1:]))
