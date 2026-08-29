"""Exp 002: human-like dinucleotide via 1st-order Markov.

Uses approximate genome-wide human dinucleotide frequencies to build a
1st-order Markov transition matrix. Sequences are sampled from this chain.
This tests whether composition alone (without true regulatory grammar)
moves eval_01 above the random-uniform floor.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
SEED = 1

# Approximate genome-wide human autosomal dinucleotide frequencies (joint).
# Rows: previous base; cols: next base. Order ACGT.
# Values from Lander 2001 / standard human-genome composition refs.
dinuc = np.array([
    [0.097, 0.052, 0.072, 0.073],  # A_
    [0.073, 0.052, 0.010, 0.072],  # C_
    [0.060, 0.043, 0.052, 0.052],  # G_
    [0.063, 0.060, 0.073, 0.097],  # T_
], dtype=np.float64)
# Normalize each row to get conditional P(next | prev).
trans = dinuc / dinuc.sum(axis=1, keepdims=True)
# Marginal P(base) from row sums.
marginal = dinuc.sum(axis=1) / dinuc.sum()

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

# Pre-compute CDFs per row for fast vectorized sampling.
cdf = np.cumsum(trans, axis=1)

# Sample starting base for each sequence.
starts = rng.choice(4, size=N, p=marginal)

idx = np.empty((N, L), dtype=np.uint8)
idx[:, 0] = starts
# Pre-sample uniforms for the whole matrix; we apply per column with prev's cdf.
u = rng.random((N, L - 1))
for t in range(1, L):
    prev = idx[:, t - 1]
    row_cdf = cdf[prev]                       # (N,4)
    idx[:, t] = (u[:, t - 1, None] < row_cdf).argmax(axis=1)

seqs = bases[idx]
lines = ["".join(row) for row in seqs]
with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {OUT}: {N} x {L}")
