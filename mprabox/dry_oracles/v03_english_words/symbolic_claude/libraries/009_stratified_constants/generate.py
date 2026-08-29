"""Exp 009: Pearson-stretch via stratified constants.

10k seqs each of all-'0', all-'1', all-'2', all-'3', plus 10k random uniform.

If the constant-blocks have well-separated and aligned (pred, target) means, the
Pearson r over the 50k pairs will be inflated by the between-stratum signal.
"""
import os
import numpy as np

N_EACH = 10_000
L = 200
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(9)

with open(OUT, "wb") as f:
    # 4 strata of all-c
    for c in [b'0', b'1', b'2', b'3']:
        line = c * L + b"\n"
        for _ in range(N_EACH):
            f.write(line)
    # 1 stratum of random uniform
    arr = rng.integers(0, 4, size=(N_EACH, L), dtype=np.int8) + ord('0')
    for i in range(N_EACH):
        f.write(bytes(arr[i].tolist()))
        f.write(b"\n")

print(f"Wrote {5*N_EACH} sequences (4x10k constants + 10k random) to {OUT}")
