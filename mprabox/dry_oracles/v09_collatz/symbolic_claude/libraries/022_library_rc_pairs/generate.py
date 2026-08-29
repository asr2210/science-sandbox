"""Library-level RC pairing: 25k random + 25k their RC.

No per-sequence palindrome. Each sequence is uniform random; for each
random sequence we also include its reverse-complement in the library.
This decouples per-seq palindrome from library-level RC pairing.

If b detects library-level RC pairs, score >> baseline 0.24.
If b is per-sequence only, score ≈ baseline 0.24.
"""
import numpy as np
import os

rng = np.random.default_rng(2222)
N, L = 50000, 200
HALF_N = N // 2

A = rng.integers(0, 4, size=(HALF_N, L), dtype=np.uint8)
# RC: reverse and complement (0<->3, 1<->2 via 3-x)
RC_A = (3 - A).astype(np.uint8)[:, ::-1]

arr = np.concatenate([A, RC_A], axis=0)
# Shuffle so RC pairs are not adjacent
perm = rng.permutation(arr.shape[0])
arr = arr[perm]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {arr.shape[0]} sequences to {out_path}")
