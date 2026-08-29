"""Experiment 025: 2nd-order Markov chain with CpG-island core enrichment.

Builds on exp 021 (best 1st-order, GC=0.62, T[C→G]=0.65, mean_r=0.874).
Adds 2nd-order overrides:
- P(C | xy=CG) = 0.50 (boost C after CG, forming CGC)
- P(G | xy=GC) = 0.75 (boost G after GC, forming GCG)
- All other P(z | xy) = T_1(z | y) from exp 021

This creates short CGCG runs (mean run ~3 CGs ≈ 6bp) clustered like
real CpG island cores. Tests whether the model can pick up trinucleotide
/ short-range alternating structure.

RISK: clustering may break the local-uniformity rule (per exp 017 lesson).
The 5-7bp cluster span is shorter than typical CNN receptive fields, so
the model might still pool over them. Empirical test.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
ALPHABET = list("ACGT")
A, C, G, Tn = 0, 1, 2, 3


def build_1st_order():
    # exp 021: GC=0.62, T[C→G]=0.65
    T = np.array([
        [0.23487, 0.40789, 0.12237, 0.23487],
        [0.125,   0.10,    0.65,    0.125],
        [0.20,    0.40,    0.20,    0.20],
        [0.23487, 0.40789, 0.12237, 0.23487],
    ])
    return T / T.sum(axis=1, keepdims=True)


def build_2nd_order(T1):
    """T2[x,y,z] = P(z | prev_prev=x, prev=y). Defaults to T1[y,z]."""
    T2 = np.broadcast_to(T1[None, :, :], (4, 4, 4)).copy()
    # Override (x=C, y=G): boost C (form CGC)
    T2[C, G, :] = [0.10, 0.50, 0.20, 0.20]
    # Override (x=G, y=C): boost G (form GCG)
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
    print(f"1st-order GC: {pi1[1]+pi1[2]:.4f}")
    print(f"2nd-order overrides: P(C|CG)=0.50, P(G|GC)=0.75")

    rng = np.random.default_rng(SEED)
    T2cum = np.cumsum(T2, axis=2)  # (4,4,4)
    pi_cum = np.cumsum(pi1)
    T1cum = np.cumsum(T1, axis=1)

    seqs = np.empty((N, L), dtype=np.int8)
    u0 = rng.random(N)
    seqs[:, 0] = (u0[:, None] >= pi_cum).sum(axis=1)
    # Second base from 1st-order conditional on first
    u1 = rng.random(N)
    seqs[:, 1] = (u1[:, None] >= T1cum[seqs[:, 0]]).sum(axis=1)
    # Remaining bases from 2nd-order
    u = rng.random((N, L - 2))
    for t in range(2, L):
        x = seqs[:, t - 2]
        y = seqs[:, t - 1]
        rows = T2cum[x, y]  # (N, 4)
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
