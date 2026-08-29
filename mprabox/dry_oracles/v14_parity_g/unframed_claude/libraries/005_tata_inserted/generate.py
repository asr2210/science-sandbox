#!/usr/bin/env python3
"""Random sequences with a TATA box motif (TATAAA) inserted at position 50,
plus a CAAT box (CCAAT) at position 100. Tests motif sensitivity for promoter
elements."""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]

# Insert motifs at fixed positions
tata = list("TATAAA")
caat = list("CCAAT")
for i in range(N):
    seqs[i, 50:50+len(tata)] = tata
    seqs[i, 100:100+len(caat)] = caat

lines = ["".join(row) for row in seqs]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} sequences (with TATA+CAAT motifs) to {out}")
