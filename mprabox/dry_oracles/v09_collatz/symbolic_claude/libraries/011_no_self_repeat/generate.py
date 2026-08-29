"""Markov chain avoiding self-repeats (P(X_{t+1}=X_t) = 0).

Each step samples uniformly from the 3 non-equal chars. Stationary
distribution is uniform; dinucleotide composition has zeros on the
diagonal but is otherwise uniform across the 12 off-diagonal pairs.

No scaffold here — tests whether tail-level structure alone helps.
"""
import numpy as np
import os

rng = np.random.default_rng(1111)
N, L = 50000, 200

# Vectorized: start with random char, then each next is random in
# {0..3} \ {prev}.
arr = np.empty((N, L), dtype=np.uint8)
arr[:, 0] = rng.integers(0, 4, size=N, dtype=np.uint8)
for t in range(1, L):
    prev = arr[:, t - 1]
    # Sample uniform in {0,1,2,3} excluding prev: pick an offset in {1,2,3}
    offset = rng.integers(1, 4, size=N, dtype=np.uint8)
    arr[:, t] = (prev + offset) % 4

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
