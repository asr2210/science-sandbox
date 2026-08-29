"""Experiment 010: per-position random PSWM.

Sample one Dirichlet(alpha=1) per position (200 distributions).
Each sequence: independently sample each position from that position's distribution.
All sequences use the SAME PSWM. Per-sequence composition is roughly uniform
on average; per-position composition follows the PSWM.

Tests if position-specific composition bias matters (regardless of which direction).
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(2026)

# Per-position distribution (200 distributions, each over 4 chars)
pswm = rng.dirichlet(np.ones(4), size=L)  # (L, 4)
print(f"PSWM shape: {pswm.shape}")
print(f"PSWM[0]: {pswm[0]}")
print(f"PSWM[100]: {pswm[100]}")

# Sample sequences
arr = np.empty((N, L), dtype=np.uint8)
for j in range(L):
    arr[:, j] = rng.choice(4, size=N, p=pswm[j])

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}")
