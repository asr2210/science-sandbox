"""Experiment 026: Stronger 2nd-order CpG-island clustering.

Push the 025 success:
- P(C | xy=CG) = 0.60 (vs 0.50 in 025)
- P(G | xy=GC) = 0.85 (vs 0.75 in 025)

Continuation prob per CGCG pair: 0.60 * 0.85 = 0.51. Expected run length
= 1/(1-0.51) = 2.04 pairs ≈ 4.1 CGs in a cluster, span ~8bp.

Same 1st-order base (exp 021: GC=0.62 target, T[C→G]=0.65).

If mean keeps climbing, clustering is strongly monotone (push more).
If mean drops, we found the clustering peak.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
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
    T2[C, G, :] = [0.05, 0.60, 0.15, 0.20]  # after CG → boost C
    T2[G, C, :] = [0.05, 0.05, 0.85, 0.05]  # after GC → strong boost G
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
    print(f"1st-order GC: {pi1[1]+pi1[2]:.4f}")

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
    cgcg = sum("".join(s.tolist()).count("CGCG") for s in samp)
    print(f"realized GC: {gc.mean():.4f} (std {gc.std():.4f})")
    print(f"realized CpG rate: {cpg/(2000*(L-1)):.4f}")
    print(f"realized CGCG count per seq: {cgcg/2000:.3f}")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in chars:
            f.write("".join(row.tolist())); f.write("\n")
    print(f"wrote {N} sequences")


if __name__ == "__main__":
    main()
