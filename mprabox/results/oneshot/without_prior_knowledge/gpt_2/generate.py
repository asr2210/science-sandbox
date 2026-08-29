#!/usr/bin/env python3
"""Root entry point for generating the MPRA library."""

from pathlib import Path
import runpy


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "library" / "generate.py"), run_name="__main__")
