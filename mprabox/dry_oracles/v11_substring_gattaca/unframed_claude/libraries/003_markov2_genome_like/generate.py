#!/usr/bin/env python3
"""Genome-like sequences via 1st-order Markov chain using human dinucleotide
frequencies (CpG-depleted, ~41% GC).

Dinucleotide counts approximated from human autosomes (see e.g. Lander 2001,
many subsequent refs). Values are rounded percentages and re-normalised
to a transition matrix P[from, to].
"""
import numpy as np
import os

SEED = 4242
N = 50_000
L = 200

BASES = "ACGT"
IDX = {b: i for i, b in enumerate(BASES)}

# Approximate dinucleotide frequencies of the human genome (%), CpG-depleted.
# Sources: Lander et al. 2001 / Karlin et al.; rounded.
DINUC_PCT = {
    "AA": 9.7, "AC": 5.0, "AG": 7.0, "AT": 7.5,
    "CA": 7.4, "CC": 5.3, "CG": 1.0, "CT": 7.0,
    "GA": 5.9, "GC": 4.4, "GG": 5.3, "GT": 5.0,
    "TA": 6.5, "TC": 5.9, "TG": 7.4, "TT": 9.7,
}

def build_transition():
    counts = np.zeros((4, 4), dtype=np.float64)
    for k, v in DINUC_PCT.items():
        counts[IDX[k[0]], IDX[k[1]]] = v
    # marginal of first base
    row_sums = counts.sum(axis=1)
    p_start = row_sums / row_sums.sum()
    P = counts / row_sums[:, None]
    return p_start, P

def main():
    rng = np.random.default_rng(SEED)
    p_start, P = build_transition()

    cum_start = np.cumsum(p_start)
    cum_trans = np.cumsum(P, axis=1)

    seqs = np.empty((N, L), dtype=np.int8)
    # vectorised first column
    u = rng.random(N)
    seqs[:, 0] = np.searchsorted(cum_start, u)
    for j in range(1, L):
        u = rng.random(N)
        prev = seqs[:, j - 1]
        # For each sample, draw from the row corresponding to prev
        cutoffs = cum_trans[prev]
        seqs[:, j] = (u[:, None] >= cutoffs[:, :-1]).sum(axis=1)
    alph = np.array(list(BASES))
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in alph[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    # sanity stats
    flat = seqs.ravel()
    base_pct = np.bincount(flat, minlength=4) / flat.size
    print({BASES[i]: round(float(base_pct[i]), 3) for i in range(4)})
    print(f"Wrote {N} seqs of length {L} to {out_path}")

if __name__ == "__main__":
    main()
