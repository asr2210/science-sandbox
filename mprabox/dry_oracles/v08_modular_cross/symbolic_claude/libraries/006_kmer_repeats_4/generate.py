"""K-mer repeats library: each sequence is a random 4-mer repeated 50 times.

256 unique 4-mers; 50000 sequences span them (~195 of each). All sequences are
highly periodic, low-complexity, but differ in their 4-mer identity.

If M and T both respond systematically to 4-mer identity (e.g., both score CGCG
high and AAAA low), correlation across the 50k will be strong.
"""
import numpy as np
import os

SEED = 17
N = 50000
L = 200
K = 4
ALPHA = "0123"

rng = np.random.default_rng(SEED)
# Random 4-mer per sequence, repeated to length 200
kmer_idx = rng.integers(0, 4**K, size=N)  # 0..255

# Convert each integer to a 4-mer
def int_to_kmer(x, k):
    out = []
    for _ in range(k):
        out.append(x % 4)
        x //= 4
    return out[::-1]

kmers = np.array([int_to_kmer(x, K) for x in kmer_idx], dtype=np.uint8)  # (N, K)

# Repeat to length 200 (200 = 50 * 4)
reps = L // K  # 50
arr = np.tile(kmers, (1, reps))  # (N, L)
assert arr.shape == (N, L)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} 4-mer repeat sequences to {out_path}")
