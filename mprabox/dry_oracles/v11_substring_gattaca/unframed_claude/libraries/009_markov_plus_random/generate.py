#!/usr/bin/env python3
"""25k Markov-2 (genome-like) + 25k uniform random. Tests if hybrid-lift is
generic to any two distinct modes or specific to strict+random.
"""
import numpy as np
import os

SEED = 86420
N = 50_000
HALF = N // 2
L = 200
BASES = "ACGT"
IDX = {b: i for i, b in enumerate(BASES)}

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
    row_sums = counts.sum(axis=1)
    p_start = row_sums / row_sums.sum()
    P = counts / row_sums[:, None]
    return p_start, P


def make_markov(n, rng):
    p_start, P = build_transition()
    cum_start = np.cumsum(p_start)
    cum_trans = np.cumsum(P, axis=1)
    seqs = np.empty((n, L), dtype=np.int8)
    u = rng.random(n)
    seqs[:, 0] = np.searchsorted(cum_start, u)
    for j in range(1, L):
        u = rng.random(n)
        prev = seqs[:, j - 1]
        cutoffs = cum_trans[prev]
        seqs[:, j] = (u[:, None] >= cutoffs[:, :-1]).sum(axis=1)
    return seqs


def main():
    rng = np.random.default_rng(SEED)
    m = make_markov(HALF, rng)
    r = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    seqs = np.concatenate([m, r], axis=0)
    order = rng.permutation(N)
    seqs = seqs[order]
    alph = np.array(list(BASES))
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in alph[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} markov+random hybrid seqs to {out_path}")


if __name__ == "__main__":
    main()
