"""Experiment 001: random uniform 200bp baseline.

Sample 50,000 sequences of length 200, each base drawn i.i.d. uniform from
{A,C,G,T}. Seed 0.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 0

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = alphabet[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences of length {L} to {out}")
