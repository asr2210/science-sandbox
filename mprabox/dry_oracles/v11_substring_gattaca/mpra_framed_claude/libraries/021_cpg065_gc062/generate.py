"""Experiment 021: CpG=0.65, GC=0.62. Push past plateau."""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
ALPHABET = list("ACGT")

def build_transition():
    T = np.array([
        [0.23487, 0.40789, 0.12237, 0.23487],
        [0.125,   0.10,    0.65,    0.125],
        [0.20,    0.40,    0.20,    0.20],
        [0.23487, 0.40789, 0.12237, 0.23487],
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
    print(f"GC: {pi[1]+pi[2]:.4f} CpG: {pi[1]*T[1,2]:.4f}")

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
    print(f"realized GC: {gc.mean():.4f}, CpG: {cpg/(2000*(L-1)):.4f}")
    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in chars:
            f.write("".join(row.tolist())); f.write("\n")
    print(f"wrote {N} sequences")

if __name__ == "__main__":
    main()
