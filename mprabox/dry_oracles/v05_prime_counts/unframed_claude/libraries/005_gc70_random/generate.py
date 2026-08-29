#!/usr/bin/env python3
"""70% GC uniform random. Each base iid with P(G)=P(C)=0.35,
P(A)=P(T)=0.15."""
import numpy as np
import os

N_SEQ = 50_000
LEN = 200
SEED = 5
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

p = np.array([0.15, 0.35, 0.35, 0.15])  # A C G T
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.choice(4, size=(N_SEQ, LEN), p=p)
seqs = bases[idx]

with open(OUT, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N_SEQ} sequences of length {LEN} at 70% GC to {OUT}")
