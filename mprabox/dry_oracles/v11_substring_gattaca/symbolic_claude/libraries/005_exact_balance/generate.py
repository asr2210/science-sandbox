"""Each sequence is a random permutation of exactly 50 each of 0, 1, 2, 3.
Tests whether eliminating compositional inter-sequence variance helps."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200

base = np.array(list("0"*50 + "1"*50 + "2"*50 + "3"*50))
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(OUT, "w") as f:
    for i in range(N):
        perm = rng.permutation(L)
        f.write("".join(base[perm]) + "\n")
print(f"wrote {N} balanced-composition sequences")
