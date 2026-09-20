#!/usr/bin/env python3
"""Run from any directory; schemas and dependencies resolve relative to this file."""

import sys

from careerkit.cli import main

if __name__ == "__main__":
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure:
        reconfigure(encoding="utf-8")
    raise SystemExit(main())
