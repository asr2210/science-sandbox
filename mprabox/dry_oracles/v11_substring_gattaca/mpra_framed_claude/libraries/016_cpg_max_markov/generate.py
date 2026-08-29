"""Experiment 016: Push CpG enrichment to T[C→G]=0.80 at stationary GC=0.55.

Direct test of whether CpG is monotone:
- exp 014: T[C→G]=0.50, CpG=0.117, GC=0.49 → mean_r=0.858 eval_01=0.872
- exp 015: T[C→G]=0.65, CpG=0.179, GC=0.55 → mean_r=0.868 eval_01=0.884
- exp 016: T[C→G]=0.80, CpG=0.220, GC=0.55 → ?

If mean_r increases further: CpG is monotone in the regime tested, push more.
If mean_r decreases: there's a plateau or the chain is now too "robotic"
(too repetitive CG patterns that look unnatural to the model).

Transition derivation (A↔T symmetry, target π=[0.225,0.275,0.275,0.225]):
  Row C: [0.075, 0.05, 0.80, 0.075]   <- maximum CpG
  Row G: [0.175, 0.55, 0.10, 0.175]   <- strong G→C to recycle chain
  Row A=T: [0.34722, 0.24444, 0.06111, 0.34722]
Verified numerically: stationary GC=0.5500, CpG rate=0.2200.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
ALPHABET = list("ACGT")


def build_transition():
    T = np.array([
        [0.34722, 0.24444, 0.06111, 0.34722],  # A
        [0.075,   0.05,    0.80,    0.075],    # C  -- max CpG
        [0.175,   0.55,    0.10,    0.175],    # G
        [0.34722, 0.24444, 0.06111, 0.34722],  # T
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
    print(f"Transition:\n{T}")
    print(f"Stationary (A,C,G,T): {pi}")
    print(f"Stationary GC: {pi[1]+pi[2]:.4f}")
    print(f"Expected CpG rate: {pi[1]*T[1,2]:.4f} (vs iid {pi[1]*pi[2]:.4f})")

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
    gc_per_seq = ((samp == "G").sum(axis=1) + (samp == "C").sum(axis=1)) / L
    cpg = sum("".join(s.tolist()).count("CG") for s in samp)
    cpg_rate = cpg / (2000 * (L - 1))
    print(f"realized GC: mean={gc_per_seq.mean():.4f} std={gc_per_seq.std():.4f}")
    print(f"realized CpG rate: {cpg_rate:.4f}")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in chars:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"wrote {N} sequences")


if __name__ == "__main__":
    main()
