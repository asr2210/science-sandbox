"""Experiment 002: GC-balanced random at ~42% GC (human genome average).

50,000 sequences of 200bp. P(A)=P(T)=0.29, P(C)=P(G)=0.21.
Isolates the effect of base composition vs uniform 50% GC.
"""
import numpy as np

N = 50_000
L = 200
SEED = 2
# Human genome ~41% GC. Use 0.42 for slight margin.
P = np.array([0.29, 0.21, 0.21, 0.29])  # A, C, G, T

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.choice(4, size=(N, L), p=P)
seqs = bases[idx]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N} sequences of length {L}, GC~42%")
