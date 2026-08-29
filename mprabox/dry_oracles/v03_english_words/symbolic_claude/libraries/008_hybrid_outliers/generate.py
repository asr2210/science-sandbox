"""Experiment 008: hybrid iid + 2% outliers.

49,000 iid uniform random + 1,000 outlier sequences:
- 250 with 90% '0' (others 3.33% each)
- 250 with 90% '1'
- 250 with 90% '2'
- 250 with 90% '3'

Tests if a small fraction of extreme outliers boosts c (composition
variance reward) without crashing a, b.
"""
import numpy as np

N_iid = 49_000
N_out_per_char = 250
L = 200
rng = np.random.default_rng(1717)

iid = rng.integers(0, 4, size=(N_iid, L), dtype=np.uint8)

outliers = []
for c in range(4):
    p = np.full(4, 0.10 / 3)
    p[c] = 0.90
    for _ in range(N_out_per_char):
        outliers.append(rng.choice(4, size=L, p=p).astype(np.uint8))
outliers = np.array(outliers, dtype=np.uint8)

# Interleave outliers throughout the library to avoid block structure
all_seqs = np.concatenate([iid, outliers])
perm = rng.permutation(len(all_seqs))
all_seqs = all_seqs[perm]

with open("sequences_0.txt", "w") as f:
    for row in all_seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {len(all_seqs)} sequences of length {L}")
