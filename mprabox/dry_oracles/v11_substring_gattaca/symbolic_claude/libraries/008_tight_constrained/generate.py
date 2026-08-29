"""Tight composition constraint: each char count ∈ [48,52]. Direct construction."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 48, 52  # each count must be in [LO, HI], summing to 200

# Generate valid count tuples
valid = []
for c0 in range(LO, HI + 1):
    for c1 in range(LO, HI + 1):
        for c2 in range(LO, HI + 1):
            c3 = L - c0 - c1 - c2
            if LO <= c3 <= HI:
                valid.append((c0, c1, c2, c3))
valid = np.array(valid)
print(f"# valid count tuples: {len(valid)}")

# For each sequence, choose a tuple at random, then shuffle the chars
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = np.array(list("0123"))
with open(OUT, "w") as f:
    for _ in range(N):
        c = valid[rng.integers(0, len(valid))]
        seq = np.concatenate([np.full(c[i], chars[i]) for i in range(4)])
        rng.shuffle(seq)
        f.write("".join(seq) + "\n")
print(f"wrote {N} tight-constrained sequences ([48,52])")
