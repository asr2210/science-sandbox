#!/usr/bin/env python3
"""
prepare.py — evaluation harness.

Usage:
    python prepare.py libraries/NNN_name/

Requires sequences_0.txt in the directory.
The file must contain exactly 50,000 lines of exactly 200 ACGT characters.

DO NOT MODIFY OR READ THIS FILE. Treat it as a black box.
"""
import sys, os, runpy
if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print("Usage: python prepare.py libraries/NNN_name/")
        sys.exit(1)
    sys.argv = [sys.argv[0], 'sA6x', sys.argv[1]]
    runpy.run_path('/data/users/arao/.cache/.e/evaluate.pyc', run_name='__main__')
