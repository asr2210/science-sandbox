#!/usr/bin/env python3
"""Baseline: 50K uniformly random DNA sequences, 200bp each."""
import numpy as np
import os

N_SEQ = 50_000
LEN = 200
SEED = 0
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N_SEQ, LEN))
seqs = bases[idx]

with open(OUT, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N_SEQ} sequences of length {LEN} to {OUT}")
