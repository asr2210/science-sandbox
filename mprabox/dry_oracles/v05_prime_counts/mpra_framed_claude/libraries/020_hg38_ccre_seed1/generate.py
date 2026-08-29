#!/usr/bin/env python3
"""
Experiment 020 — Replicate of 013 (40K random hg38 + 10K cCRE) with seed=1.

Variance check on the best-performing eval_01 library. If 013 holds at
eval_01 ≈ 0.049, it's the robust best.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '013_hg38_ccre_enriched'))
import generate as g  # noqa
g.OUT = HERE / 'sequences_0.txt'
from generate import main  # noqa

if __name__ == '__main__':
    main(seed=1)
