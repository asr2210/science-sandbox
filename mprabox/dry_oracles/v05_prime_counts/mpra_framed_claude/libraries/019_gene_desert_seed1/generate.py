#!/usr/bin/env python3
"""
Experiment 019 — Replicate of 016 (gene-desert) with seed=1 (variance check).

Tests reproducibility of the HepG2 lift from gene-desert. If HepG2 mean
stays ≈ 0.056, the gene-desert signal is real. If it drops to ≈ 0.053
(roughly random hg38 level), the previous result was noise.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '016_gene_desert'))
from generate import main  # noqa

if __name__ == '__main__':
    main(seed=1)
