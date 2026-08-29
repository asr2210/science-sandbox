"""Experiment 015: Stronger CpG-enriched Markov chain at stationary GC=0.55.

Builds on exp 014 (T[C→G]=0.50, stationary GC=0.49, mean_r=0.858, eval_01=0.872).
Pushes CpG harder and fixes the GC drift:
- T[C→G] = 0.65 (vs 0.50 in 014)
- Stationary GC = 0.55 exactly (vs 0.49 in 014)
- Expected CpG dinucleotide rate = 0.179 (vs 0.117 in 014, vs iid 0.076)

If this beats 014 by > noise (~0.003), CpG enrichment is monotone in its
effect — the model is genuinely learning a CpG → activity association and
the more, the better (up to some plateau).

Transition derivation (with A↔T symmetry and target π=[0.225,0.275,0.275,0.225]):
  Row C: [0.125, 0.10, 0.65, 0.125]   <- 65% of post-C bases are G
  Row G: [0.20,  0.40, 0.20, 0.20]    <- G feeds C heavily for chain stability
  Row A=T: [0.30139, 0.30556, 0.09167, 0.30139]
Verified numerically: stationary = (0.225, 0.275, 0.275, 0.225), GC=0.5500.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
ALPHABET = list("ACGT")


def build_transition():
    T = np.array([
        [0.30139, 0.30556, 0.09167, 0.30139],  # A
        [0.125,   0.10,    0.65,    0.125],    # C  -- strong CpG boost
        [0.20,    0.40,    0.20,    0.20],     # G
        [0.30139, 0.30556, 0.09167, 0.30139],  # T
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
    cpg = 0
    for s in samp:
        cpg += "".join(s.tolist()).count("CG")
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
