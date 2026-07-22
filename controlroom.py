#!/usr/bin/env python
"""Root shim -> runs `python -m aea.server.controlroom` (the server lives in aea/server/ after the
2026-07-22 subpackage reorg). Keeps `python controlroom.py [args]` working."""
import os, sys, subprocess
_root = os.path.dirname(os.path.abspath(__file__))
sys.exit(subprocess.call([sys.executable, "-m", "aea.server.controlroom"] + sys.argv[1:], cwd=_root))
