"""Exp 002: uniform random over {0,1,2,3}. Baseline for no-structure."""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(42)
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
# Convert each row to string and write.
chars = np.array(list("0123"))
lines = ["".join(chars[arr[i]]) for i in range(N)]
with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} lines")
