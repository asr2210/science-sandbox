"""Exp 008: natural DNA-like Markov-1 chain (CpG-depleted human-like).

Assume mapping A=0, C=1, G=2, T=3. Build a transition matrix approximating human
genomic dinucleotide frequencies — notably CG depleted, TG/CA enriched.

If the scorer's model is trained on real DNA, in-distribution sequences should
match better between prediction and target.
"""
import os
import numpy as np

N = 50_000
L = 200
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

# Approximate human dinucleotide transition matrix (rows = from, cols = to)
# Order: A=0, C=1, G=2, T=3
P = np.array([
    [0.301, 0.205, 0.286, 0.207],  # from A
    [0.166, 0.221, 0.080, 0.532],  # from C  (G after C depleted)
    [0.260, 0.196, 0.207, 0.337],  # from G
    [0.215, 0.252, 0.250, 0.282],  # from T
], dtype=np.float64)
P /= P.sum(axis=1, keepdims=True)

# Stationary marginal (close to human): roughly A=T=0.295, C=G=0.205
pi0 = np.array([0.295, 0.205, 0.205, 0.295])

rng = np.random.default_rng(8)

# Pre-compute cumulative for fast sampling
cumP = np.cumsum(P, axis=1)
cum0 = np.cumsum(pi0)

# Sample 50k sequences
out = np.zeros((N, L), dtype=np.int8)
# Initial state for all sequences
u0 = rng.random(N)
out[:, 0] = np.searchsorted(cum0, u0)
# Step through
for t in range(1, L):
    prev = out[:, t - 1]
    u = rng.random(N)
    # For each row pick using its previous state's cumulative
    rows_cum = cumP[prev]                  # shape (N, 4)
    out[:, t] = (u[:, None] < rows_cum).argmax(axis=1)

out += ord('0')
with open(OUT, "wb") as f:
    for i in range(N):
        f.write(bytes(out[i].tolist()))
        f.write(b"\n")
print(f"Wrote {N} natural-Markov sequences to {OUT}")
