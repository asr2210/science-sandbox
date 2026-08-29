#!/usr/bin/env python3
"""GC-rich random sequences. 70% GC content."""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
# P(A)=0.15, P(C)=0.35, P(G)=0.35, P(T)=0.15
probs = [0.15, 0.35, 0.35, 0.15]
bases = np.array(list("ACGT"))
arr = rng.choice(4, size=(N, L), p=probs)
seqs = bases[arr]
lines = ["".join(row) for row in seqs]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} sequences to {out}")
