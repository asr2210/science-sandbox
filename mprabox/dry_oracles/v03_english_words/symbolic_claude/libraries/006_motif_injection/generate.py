"""Exp 006: motif library injection.

Generate 50k random uniform backgrounds. For each seq, sample K ~ U{0,20}.
Insert K randomly-chosen 8-mers (from a fixed library of 64 random 8-mers) at
random non-overlapping positions.

If both prediction and target respond to motif content, r should change vs random
uniform baseline.
"""
import os
import numpy as np

N = 50_000
L = 200
MOTIF_LEN = 8
N_MOTIFS = 64
MAX_K = 20
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(6)

# Motif library: 64 random 8-mers (fixed by seed)
lib_rng = np.random.default_rng(123)
motif_lib = lib_rng.integers(0, 4, size=(N_MOTIFS, MOTIF_LEN), dtype=np.int8)

# Background: random uniform
seqs = rng.integers(0, 4, size=(N, L), dtype=np.int8)

# Choose K per sequence
Ks = rng.integers(0, MAX_K + 1, size=N)

# Stamp motifs
for i in range(N):
    K = int(Ks[i])
    if K == 0:
        continue
    # choose K motifs (with replacement)
    motif_idx = rng.integers(0, N_MOTIFS, size=K)
    # choose K start positions, non-overlapping greedily
    starts = []
    occupied = np.zeros(L, dtype=bool)
    tries = 0
    while len(starts) < K and tries < 5 * K:
        s = int(rng.integers(0, L - MOTIF_LEN + 1))
        if not occupied[s:s + MOTIF_LEN].any():
            starts.append(s)
            occupied[s:s + MOTIF_LEN] = True
        tries += 1
    # stamp
    for j, s in enumerate(starts):
        seqs[i, s:s + MOTIF_LEN] = motif_lib[motif_idx[j]]

seqs += ord('0')
with open(OUT, "wb") as f:
    for i in range(N):
        f.write(bytes(seqs[i].tolist()))
        f.write(b"\n")
print(f"Wrote {N} sequences with {N_MOTIFS}-motif library injection to {OUT}")
print(f"Avg K per seq: {Ks.mean():.2f}")
