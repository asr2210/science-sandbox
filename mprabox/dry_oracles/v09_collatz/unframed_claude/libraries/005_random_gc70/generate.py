"""Experiment 005 — Random sequences at 70% GC.

Diagnostic: does GC content matter (independent of motifs)?
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(5)
N, L = 50_000, 200

# 70% GC: P(G)=P(C)=0.35, P(A)=P(T)=0.15
bases = np.array(list("ACGT"))
probs = np.array([0.15, 0.35, 0.35, 0.15])
idx = rng.choice(4, size=(N, L), p=probs)
seqs = bases[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row)); f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
