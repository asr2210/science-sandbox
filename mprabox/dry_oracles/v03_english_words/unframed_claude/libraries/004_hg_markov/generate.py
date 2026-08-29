"""Experiment 004: 50k sequences sampled from a 1st-order Markov chain whose
dinucleotide frequencies match human genome (hg38) averages.

Hypothesis: realistic dinucleotide composition (notably CpG depletion) is
in-distribution for the scoring models and should outperform random uniform
if "looks-like-DNA" beats "max entropy".

Dinucleotide frequencies are taken from published hg38 average values
(Karlin & Burge 1995-era, widely reproduced):
  AA 0.0997  AC 0.0507  AG 0.0716  AT 0.0762
  CA 0.0735  CC 0.0526  CG 0.0103  CT 0.0716
  GA 0.0580  GC 0.0428  GG 0.0526  GT 0.0507
  TA 0.0560  TC 0.0580  TG 0.0735  TT 0.0997
(They sum to ~1.0. CpG is heavily depleted, ~5x less than other XG.)
"""
import os
import numpy as np

RNG_SEED = 1004
N_SEQS = 50_000
LEN = 200
BASES = "ACGT"
B2I = {b: i for i, b in enumerate(BASES)}

DINUC = {
    "AA": 0.0997, "AC": 0.0507, "AG": 0.0716, "AT": 0.0762,
    "CA": 0.0735, "CC": 0.0526, "CG": 0.0103, "CT": 0.0716,
    "GA": 0.0580, "GC": 0.0428, "GG": 0.0526, "GT": 0.0507,
    "TA": 0.0560, "TC": 0.0580, "TG": 0.0735, "TT": 0.0997,
}


def build_transition_matrix():
    # P[i, j] = P(next=j | curr=i) derived from joint frequencies.
    P = np.zeros((4, 4))
    for ab, p in DINUC.items():
        i, j = B2I[ab[0]], B2I[ab[1]]
        P[i, j] = p
    P /= P.sum(axis=1, keepdims=True)
    return P


def stationary_distribution(P):
    # Left eigenvector for eigenvalue 1.
    eigvals, eigvecs = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigvals - 1.0))
    v = np.real(eigvecs[:, idx])
    v = v / v.sum()
    return v


def sample_markov(rng, P, pi, n_seqs, length):
    # Cumulative for vectorised sampling.
    cum_P = np.cumsum(P, axis=1)
    cum_pi = np.cumsum(pi)
    # First base
    first = (rng.random(n_seqs)[:, None] >= cum_pi[None, :]).sum(axis=1)
    out = np.empty((n_seqs, length), dtype=np.int8)
    out[:, 0] = first
    # Subsequent bases column-by-column (need previous column)
    u = rng.random((n_seqs, length))
    for t in range(1, length):
        prev = out[:, t - 1]
        thr = cum_P[prev]  # (n_seqs, 4)
        out[:, t] = (u[:, t][:, None] >= thr).sum(axis=1)
    return out


def main():
    rng = np.random.default_rng(RNG_SEED)
    P = build_transition_matrix()
    pi = stationary_distribution(P)
    seqs = sample_markov(rng, P, pi, N_SEQS, LEN)
    alphabet = np.array(list(BASES))
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in seqs:
            f.write("".join(alphabet[row]))
            f.write("\n")
    print(f"wrote {N_SEQS} hg38-Markov sequences; stationary={pi.round(4).tolist()}")


if __name__ == "__main__":
    main()
