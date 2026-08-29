"""Experiment 001 — Random 50% GC baseline.

50,000 sequences, 200bp each, sampled iid uniform from {A,C,G,T}.
Establishes baseline for scorer behavior.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(42)
N, L = 50_000, 200
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = bases[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row))
        f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
