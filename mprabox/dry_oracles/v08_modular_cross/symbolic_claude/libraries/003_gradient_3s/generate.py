"""Gradient of '3' fraction across the 50k.

Sequence i has fraction(3) = i/50000 (random positions), with the remaining
positions uniform over {0,1,2}. The 50k sequences thus span 0% → 100% "3".

If the SET of sequences matters (not order), this is similar to uniform random
in aggregate composition (avg 50% "3"-rich) → mean_r ~ 0 most likely.

If ORDER matters (i.e., scorer aligns seq position i with a hidden target_i),
then having a monotone feature gives positive r if that feature aligns with target.
"""
import numpy as np
import os

SEED = 7
N = 50000
L = 200
rng = np.random.default_rng(SEED)

# Choose positions for "3"s in each sequence
arr = np.zeros((N, L), dtype=np.uint8)
for i in range(N):
    frac3 = i / (N - 1)  # 0 .. 1
    n3 = int(round(frac3 * L))
    # uniform over {0,1,2} for the rest
    rest = rng.integers(0, 3, size=L - n3, dtype=np.uint8)
    # combine: n3 threes + rest, then shuffle
    seq = np.concatenate([np.full(n3, 3, dtype=np.uint8), rest])
    rng.shuffle(seq)
    arr[i] = seq

ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} sequences (gradient of 3s) to {out_path}")
