"""Half palindromes (Watson-Crick complement) + half random uniform.

Each palindrome: first 100 random; last 100 = reverse-complement (0↔3, 1↔2).
Tests if 'is palindrome' is a feature the model uses.
"""
import numpy as np
import os

SEED = 167
N = 50000
HALF = 25000
L = 200
ALPHA = "0123"

rng = np.random.default_rng(SEED)
COMPLEMENT = np.array([3, 2, 1, 0], dtype=np.uint8)  # 0↔3, 1↔2

# Half palindromes
left = rng.integers(0, 4, size=(HALF, L // 2), dtype=np.uint8)
right = COMPLEMENT[left[:, ::-1]]
palindromes = np.concatenate([left, right], axis=1)
assert palindromes.shape == (HALF, L)

# Half random uniform
random_unif = rng.integers(0, 4, size=(HALF, L), dtype=np.uint8)

# Combine (order doesn't matter)
arr = np.concatenate([palindromes, random_unif], axis=0)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} sequences (25k palindromes + 25k random) to {out_path}")
