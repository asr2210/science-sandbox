"""Experiment 018: Bisect CpG curve. T[C→G]=0.70 at GC=0.55.

CpG curve data so far:
- T[C→G]=0.50 (014, CpG=0.117 GC=0.49): mean_r=0.858
- T[C→G]=0.65 (015, CpG=0.179 GC=0.55): mean_r=0.868 [best]
- T[C→G]=0.80 (016, CpG=0.219 GC=0.55): mean_r=0.857

If 0.70 ≈ 0.868 → flat plateau between 0.65 and 0.70.
If 0.70 > 0.868 → peak shifted right, push more.
If 0.70 < 0.868 → confirm 0.65 is the peak.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
ALPHABET = list("ACGT")


def build_transition():
    T = np.array([
        [0.30903, 0.29028, 0.09167, 0.30903],
        [0.1125,  0.075,   0.70,    0.1125],  # T[C→G]=0.70
        [0.20,    0.45,    0.15,    0.20],
        [0.30903, 0.29028, 0.09167, 0.30903],
    ])
    return T / T.sum(axis=1, keepdims=True)


def stationary(T, n_iter=5000):
    pi = np.ones(4) / 4
    for _ in range(n_iter):
        pi = pi @ T
    return pi


def main():
    T = build_transition()
    pi = stationary(T)
    print(f"Stationary GC: {pi[1]+pi[2]:.4f}, CpG rate: {pi[1]*T[1,2]:.4f}")

    rng = np.random.default_rng(SEED)
    Tcum = np.cumsum(T, axis=1)
    pi_cum = np.cumsum(pi)
    seqs = np.empty((N, L), dtype=np.int8)
    u0 = rng.random(N)
    seqs[:, 0] = (u0[:, None] >= pi_cum).sum(axis=1)
    u = rng.random((N, L - 1))
    for t in range(1, L):
        rows = Tcum[seqs[:, t - 1]]
        seqs[:, t] = (u[:, t - 1, None] >= rows).sum(axis=1)

    alphabet = np.array(ALPHABET)
    chars = alphabet[seqs]
    samp = chars[:2000]
    gc = ((samp == "G").sum(axis=1) + (samp == "C").sum(axis=1)) / L
    cpg = sum("".join(s.tolist()).count("CG") for s in samp)
    print(f"realized GC: {gc.mean():.4f}, CpG rate: {cpg/(2000*(L-1)):.4f}")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in chars:
            f.write("".join(row.tolist())); f.write("\n")
    print(f"wrote {N} sequences")


if __name__ == "__main__":
    main()
