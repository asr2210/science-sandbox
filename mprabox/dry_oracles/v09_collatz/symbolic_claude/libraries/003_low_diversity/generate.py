"""Low-diversity library: one balanced template + 5% mutations per copy.

Composition stays uniform (within tolerance), but between-sequence
diversity drops dramatically. Tests whether the scorer rewards
library diversity (especially condition c, which is 0.63 on uniform).
"""
import numpy as np
import os

rng = np.random.default_rng(303)
N, L = 50000, 200

# Build a balanced template: 50 of each character, then shuffle.
template_chars = np.array([0]*50 + [1]*50 + [2]*50 + [3]*50, dtype=np.uint8)
rng.shuffle(template_chars)

arr = np.tile(template_chars, (N, 1))  # (N, L)
# Apply 5% iid substitution: pick positions, set to a random other char.
mut_mask = rng.random(arr.shape) < 0.05
# For mutated positions, draw a new uniform char in {0,1,2,3}, but ensure
# different from current (typical mutation semantics).
random_chars = rng.integers(0, 4, size=arr.shape, dtype=np.uint8)
# If random_chars equals current, increment mod 4 to force change.
same = (random_chars == arr) & mut_mask
random_chars[same] = (random_chars[same] + 1) % 4
arr[mut_mask] = random_chars[mut_mask]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")

# Sanity check composition
unique, counts = np.unique(arr, return_counts=True)
total = arr.size
print("composition:", {int(u): float(c) / total for u, c in zip(unique, counts)})
