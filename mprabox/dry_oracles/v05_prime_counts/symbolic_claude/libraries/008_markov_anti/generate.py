"""Experiment 008: 1st-order Markov, anti-autocorrelated transitions.

T[i][i] = 0.10, T[i][j!=i] = 0.30. Stationary distribution uniform.
Consecutive bases agree with prob 0.10 (vs 0.25 for iid uniform).

Tests if dinucleotide-level structure matters for the score.
"""
import os
import numpy as np

SEED = 8
N = 50_000
L = 200
ALPHA = "0123"

P_STAY = 0.10
P_SWITCH = (1.0 - P_STAY) / 3  # 0.30

def main():
    rng = np.random.default_rng(SEED)
    # build transition matrix
    T = np.full((4, 4), P_SWITCH)
    for i in range(4):
        T[i, i] = P_STAY
    # cumulative for sampling
    Tcum = np.cumsum(T, axis=1)
    arr = np.empty((N, L), dtype=np.int8)
    # start state uniformly
    arr[:, 0] = rng.integers(0, 4, size=N, dtype=np.int8)
    # vectorized markov chain step
    for t in range(1, L):
        u = rng.random(N)
        prev = arr[:, t - 1]
        # for each row, sample j with cumulative T[prev[i]]
        cum_for_each = Tcum[prev]  # (N, 4)
        # find smallest j with u <= cum_for_each[:, j]
        # use searchsorted-like trick
        diff = cum_for_each - u[:, None]
        # next state = argmax of (diff>=0) along axis=1
        arr[:, t] = (diff < 0).sum(axis=1).astype(np.int8)
    lut = np.array([ord(c) for c in ALPHA], dtype=np.uint8)
    bytes_arr = lut[arr]
    lines = [row.tobytes().decode("ascii") for row in bytes_arr]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {N} sequences to {out_path}")
    # composition check
    flat = arr[:1000].flatten()
    counts = np.bincount(flat, minlength=4)
    print(f"base proportions: {(counts / counts.sum()).round(3).tolist()}")
    # autocorrelation check
    same = (arr[:, 1:] == arr[:, :-1]).mean()
    print(f"P(next==prev) sampled: {same:.3f}  (target {P_STAY})")

if __name__ == "__main__":
    main()
