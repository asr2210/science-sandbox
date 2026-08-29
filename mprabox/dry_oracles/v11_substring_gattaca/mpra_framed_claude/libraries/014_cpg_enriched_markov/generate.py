"""Experiment 014: CpG-enriched Markov-chain sequences.

1st-order Markov chain on {A,C,G,T} with:
- target stationary marginal: π(A)=π(T)=0.225, π(C)=π(G)=0.275 (GC=0.55)
- elevated P(G|C) = 0.5 (vs iid 0.275) to boost CpG dinucleotide

Other transitions tuned so stationary marginal stays close to GC=0.55.

The simplest construction:
- T[C→G] = 0.50 (boost CpG)
- T[C→A] = T[C→T] = 0.20 each (rest of C row)
- T[C→C] = 0.10
- T[A→G] = T[T→G] = 0.138 (reduce G destinations from A/T to compensate)
- T[A→C] = T[T→C] = 0.275
- T[A→A] = T[A→T] = (1 - 0.275 - 0.138) / 2 = 0.2935
- T[T→A] = T[T→T] = 0.2935
- T[G→A] = T[G→T] = 0.225
- T[G→C] = T[G→G] = 0.275

Run chain forward for 200 steps from a random uniform first base.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 0
ALPHABET = list("ACGT")
IDX = {b: i for i, b in enumerate(ALPHABET)}


def build_transition():
    T = np.zeros((4, 4))
    # rows: A=0, C=1, G=2, T=3
    # From A
    T[0] = [0.2935, 0.275, 0.138, 0.2935]
    # From C  (boost C→G)
    T[1] = [0.20, 0.10, 0.50, 0.20]
    # From G
    T[2] = [0.225, 0.275, 0.275, 0.225]
    # From T
    T[3] = [0.2935, 0.275, 0.138, 0.2935]
    # normalize rows for safety
    T = T / T.sum(axis=1, keepdims=True)
    return T


def stationary(T, tol=1e-10, max_iter=5000):
    pi = np.ones(4) / 4
    for _ in range(max_iter):
        pi_new = pi @ T
        if np.allclose(pi_new, pi, atol=tol):
            pi = pi_new
            break
        pi = pi_new
    return pi


def main():
    T = build_transition()
    pi = stationary(T)
    print(f"Transition matrix:\n{T}")
    print(f"Stationary distribution (A,C,G,T): {pi}")
    print(f"Stationary GC: {pi[1] + pi[2]:.4f}")
    # expected CpG dinucleotide frequency
    expected_cpg = pi[1] * T[1, 2]
    print(f"Expected CpG dinucleotide rate: {expected_cpg:.4f} "
          f"(vs iid ~{pi[1]*pi[2]:.4f})")

    rng = np.random.default_rng(SEED)
    # cumulative transition rows for fast sampling
    Tcum = np.cumsum(T, axis=1)  # (4, 4)
    # start state from stationary
    pi_cum = np.cumsum(pi)
    seqs = np.empty((N, L), dtype=np.int8)
    u0 = rng.random(N)
    seqs[:, 0] = (u0[:, None] >= pi_cum).sum(axis=1)
    u = rng.random((N, L - 1))
    for t in range(1, L):
        prev = seqs[:, t - 1]
        # for each row i, sampling pos based on Tcum[i]
        rows = Tcum[prev]  # (N, 4)
        seqs[:, t] = (u[:, t - 1, None] >= rows).sum(axis=1)

    alphabet = np.array(ALPHABET)
    chars = alphabet[seqs]
    # diagnostics
    samp = chars[:2000]
    gc_per_seq = np.array([((s == "G").sum() + (s == "C").sum()) / L for s in samp])
    cpg_count = 0
    total_dinucs = 0
    for s in samp:
        s_str = "".join(s.tolist())
        cpg_count += s_str.count("CG")
        total_dinucs += L - 1
    cpg_rate = cpg_count / total_dinucs
    print(f"realized GC: mean={gc_per_seq.mean():.4f} std={gc_per_seq.std():.4f}")
    print(f"realized CpG dinucleotide rate: {cpg_rate:.4f}")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in chars:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"wrote {N} sequences")


if __name__ == "__main__":
    main()
