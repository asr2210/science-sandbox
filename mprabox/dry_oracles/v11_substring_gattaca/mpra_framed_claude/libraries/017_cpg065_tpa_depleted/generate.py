"""Experiment 017: CpG-enriched + TpA-depleted Markov chain at GC=0.55.

Builds on exp 015 (NEW BEST so far: mean_r=0.868, eval_01=0.884). Tests
whether stacking a second dinucleotide bias adds value.

- T[C→G] = 0.65 (same as 015; CpG dinucleotide rate ~0.18)
- T[T→A] = T[A→T] = 0.10 (TpA AND ApT depleted ~55% vs iid)
- Stationary GC = 0.55 (verified)

Biological motivation: TpA is the most destabilizing dinucleotide and is
depleted in active regulatory regions (CpG islands and beyond). If the
model learns TpA → silent and CpG → active, stacking both should help.

Side effect: T[A→A] = T[T→T] = 0.50 (A and T runs more common). Mean run
length 2.0, not pathological for 200bp.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
ALPHABET = list("ACGT")


def build_transition():
    T = np.array([
        [0.50278, 0.30556, 0.09167, 0.10],     # A: A→T depleted, A→A elevated
        [0.125,   0.10,    0.65,    0.125],    # C: CpG boost
        [0.20,    0.40,    0.20,    0.20],     # G
        [0.10,    0.30556, 0.09167, 0.50278],  # T: T→A depleted, T→T elevated
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
    print(f"Expected TpA rate: {pi[3]*T[3,0]:.4f} (vs iid {pi[3]*pi[0]:.4f})")

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
    tpa = sum("".join(s.tolist()).count("TA") for s in samp)
    print(f"realized GC: mean={gc_per_seq.mean():.4f} std={gc_per_seq.std():.4f}")
    print(f"realized CpG rate: {cpg / (2000 * (L-1)):.4f}")
    print(f"realized TpA rate: {tpa / (2000 * (L-1)):.4f}")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in chars:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"wrote {N} sequences")


if __name__ == "__main__":
    main()
