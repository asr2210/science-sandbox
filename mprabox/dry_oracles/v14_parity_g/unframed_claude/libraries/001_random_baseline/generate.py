#!/usr/bin/env python3
"""Random uniform ACGT baseline. 50,000 x 200bp."""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]
lines = ["".join(row) for row in seqs]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} sequences to {out}")
