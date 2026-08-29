"""Exp 003: High GC (70%) with biased base composition.
Sample each base i.i.d. with p(A)=p(T)=0.15, p(C)=p(G)=0.35.
This pushes GC to 70% and naturally enriches CG dinucleotide.
"""
import numpy as np
import os

N = 50_000
L = 200
rng = np.random.default_rng(3)
bases = np.array(list("ACGT"))
probs = np.array([0.15, 0.35, 0.35, 0.15])  # A C G T
arr = rng.choice(4, size=(N, L), p=probs)
seqs = bases[arr]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} sequences (GC~70%) to {out_path}")
