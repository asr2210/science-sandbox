#!/usr/bin/env python3
"""
Experiment 024 — Replicate of 013 with seed=2 (triplicate variance).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '013_hg38_ccre_enriched'))
import generate as g  # noqa
g.OUT = HERE / 'sequences_0.txt'
from generate import main  # noqa

if __name__ == '__main__':
    main(seed=2)
