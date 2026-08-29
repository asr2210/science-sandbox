"""Experiment 002: GC-rich (60%) random sequences.

50k x 200bp, sampled i.i.d. with P(G)=P(C)=0.30, P(A)=P(T)=0.20.
Tests whether GC content alone moves the score off the uniform baseline.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = np.array(list("ACGT"))
PROBS = np.array([0.20, 0.30, 0.30, 0.20])  # A, C, G, T

rng = np.random.default_rng(20260603)
idx = rng.choice(4, size=(N_SEQ, LEN), p=PROBS)
seqs = ["".join(ALPHABET[row]) for row in idx]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences of length {LEN} (60% GC) to {out_path}")
