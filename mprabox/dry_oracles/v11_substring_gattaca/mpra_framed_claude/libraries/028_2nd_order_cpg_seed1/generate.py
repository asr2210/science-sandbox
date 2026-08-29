"""Experiment 028: Replicate exp 025 with SEED=1.

Verify the 025 result (mean_r=0.879, eval_01=0.895) isn't seed luck.
If seed=1 gives ~0.876-0.882 (within ~0.003 noise floor), 025 design is
robust.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 1   # seed=1 (vs 0 in 025)
ALPHABET = list("ACGT")
A, C, G, Tn = 0, 1, 2, 3


def build_1st_order():
    T = np.array([
        [0.23487, 0.40789, 0.12237, 0.23487],
        [0.125,   0.10,    0.65,    0.125],
        [0.20,    0.40,    0.20,    0.20],
        [0.23487, 0.40789, 0.12237, 0.23487],
    ])
    return T / T.sum(axis=1, keepdims=True)


def build_2nd_order(T1):
    T2 = np.broadcast_to(T1[None, :, :], (4, 4, 4)).copy()
    T2[C, G, :] = [0.10, 0.50, 0.20, 0.20]
    T2[G, C, :] = [0.05, 0.10, 0.75, 0.10]
    T2 = T2 / T2.sum(axis=2, keepdims=True)
    return T2


def stationary_1st(T1, n_iter=5000):
    pi = np.ones(4) / 4
    for _ in range(n_iter):
        pi = pi @ T1
    return pi


def main():
    T1 = build_1st_order()
    T2 = build_2nd_order(T1)
    pi1 = stationary_1st(T1)

    rng = np.random.default_rng(SEED)
    T2cum = np.cumsum(T2, axis=2)
    pi_cum = np.cumsum(pi1)
    T1cum = np.cumsum(T1, axis=1)

    seqs = np.empty((N, L), dtype=np.int8)
    u0 = rng.random(N)
    seqs[:, 0] = (u0[:, None] >= pi_cum).sum(axis=1)
    u1 = rng.random(N)
    seqs[:, 1] = (u1[:, None] >= T1cum[seqs[:, 0]]).sum(axis=1)
    u = rng.random((N, L - 2))
    for t in range(2, L):
        x = seqs[:, t - 2]
        y = seqs[:, t - 1]
        rows = T2cum[x, y]
        seqs[:, t] = (u[:, t - 2, None] >= rows).sum(axis=1)

    alphabet = np.array(ALPHABET)
    chars = alphabet[seqs]
    samp = chars[:2000]
    gc = ((samp == "G").sum(axis=1) + (samp == "C").sum(axis=1)) / L
    cpg = sum("".join(s.tolist()).count("CG") for s in samp)
    print(f"realized GC: {gc.mean():.4f}, CpG: {cpg/(2000*(L-1)):.4f}")
    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in chars:
            f.write("".join(row.tolist())); f.write("\n")
    print(f"wrote {N} sequences")


if __name__ == "__main__":
    main()
