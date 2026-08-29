"""Experiment 001: Pure uniform random DNA baseline.

50,000 sequences, 200bp each, sampled i.i.d. from uniform {A,C,G,T}.
Establishes a floor — the simplest possible library. Random TF binding
sites will occur by chance (6-12bp motifs in 200bp windows), giving the
model some opportunity to learn motif recognition.
"""
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = bases[idx]

with open(OUT, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")

print(f"wrote {N} sequences of length {L} to {OUT}")
