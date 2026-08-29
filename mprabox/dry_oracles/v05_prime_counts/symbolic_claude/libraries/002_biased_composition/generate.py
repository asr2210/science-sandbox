"""Experiment 002: per-sequence composition bias.

For each of 50K sequences, pick a dominant base uniformly at random from {0,1,2,3},
then sample each position to be the dominant base with prob 0.90, else uniform
over the other 3 with prob 0.10/3 each.

This gives LOW within-sequence diversity but HIGH between-sequence diversity
(roughly equal sub-populations of "mostly-0", "mostly-1", "mostly-2", "mostly-3").

Compare to exp 001 (uniform random, high within and between).
- If within-sequence diversity drives score, mean_r should drop.
- If between-sequence composition diversity matters, mean_r may stay or rise.
"""
import os
import numpy as np

SEED = 1
N = 50_000
L = 200
ALPHA = "0123"
BIAS = 0.90

def main():
    rng = np.random.default_rng(SEED)
    dominant = rng.integers(0, 4, size=N)  # per-sequence dominant base
    arr = np.empty((N, L), dtype=np.int8)
    for i in range(N):
        dom = int(dominant[i])
        # sample positions
        u = rng.random(L)
        seq = np.where(
            u < BIAS,
            dom,
            rng.integers(0, 3, size=L),
        )
        # for the random branch we drew from {0,1,2} - we need to remap to non-dom alphabet
        # easier: redo cleanly per position
        # Redo: use 0.90 dom, 0.10/3 each others.
        choices = np.array([dom] + [b for b in range(4) if b != dom])  # [dom, o1, o2, o3]
        p = np.array([BIAS, (1 - BIAS) / 3, (1 - BIAS) / 3, (1 - BIAS) / 3])
        seq = choices[rng.choice(4, size=L, p=p)]
        arr[i] = seq
    lut = np.array([ord(c) for c in ALPHA], dtype=np.uint8)
    bytes_arr = lut[arr]
    lines = [row.tobytes().decode("ascii") for row in bytes_arr]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    # sanity
    assert len(lines) == N
    assert all(len(s) == L for s in lines)
    # check distribution of dominant base
    counts = np.bincount(dominant, minlength=4)
    print(f"dominant base distribution: {counts.tolist()}")
    print(f"wrote {N} sequences to {out_path}")

if __name__ == "__main__":
    main()
