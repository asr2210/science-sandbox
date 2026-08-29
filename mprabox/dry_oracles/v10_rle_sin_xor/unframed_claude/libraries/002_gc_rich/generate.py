"""Experiment 002: 65% GC content i.i.d. Diagnostic for GC sensitivity."""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))
# P(A)=P(T)=0.175, P(C)=P(G)=0.325  →  GC=0.65
P = np.array([0.175, 0.325, 0.325, 0.175])

rng = np.random.default_rng(2)
idx = rng.choice(4, size=(N, L), p=P)
seqs = ["".join(ALPHABET[row]) for row in idx]

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"wrote {len(seqs)} sequences to {OUT}")
