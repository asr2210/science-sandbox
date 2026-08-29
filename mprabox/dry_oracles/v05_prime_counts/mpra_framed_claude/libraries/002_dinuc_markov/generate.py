#!/usr/bin/env python3
"""
Experiment 002 — 1st-order Markov (dinucleotide-matched) random sequences.

Tests whether matching low-order genomic composition alone lifts the model
above the random-uniform floor. If yes, much of generalizable signal is
low-order; if no, the model needs higher-order/motif features.

Transition matrix is a rough hand-curated approximation of human autosomal
dinucleotide frequencies (~41% GC, CpG depletion ~5x).
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sequences_0.txt')

N_SEQ = 50_000
LEN = 200
ALPHA = list('ACGT')
IDX = {b: i for i, b in enumerate(ALPHA)}

# Rough hg38 1st-order Markov transitions P(next | prev).
# Sources: standard published genomic dinucleotide frequencies.
# Row = prev base, Col = next base, rows sum to 1.
#                  A      C      G      T
TRANS = np.array([
    [0.295, 0.205, 0.290, 0.210],  # prev A
    [0.320, 0.295, 0.040, 0.345],  # prev C   (CG depleted)
    [0.290, 0.210, 0.295, 0.205],  # prev G
    [0.205, 0.205, 0.295, 0.295],  # prev T
])
# Stationary distribution (~41% GC).
PI = np.array([0.295, 0.205, 0.205, 0.295])


def sample_sequences(n, L, seed):
    rng = np.random.default_rng(seed)
    # Vectorized Markov chain sampling.
    seqs = np.empty((n, L), dtype=np.int8)
    # First base from stationary.
    seqs[:, 0] = rng.choice(4, size=n, p=PI)
    # Precompute cumulative transitions for inverse-CDF sampling per row.
    cdf = np.cumsum(TRANS, axis=1)
    # Random uniforms for all subsequent positions.
    u = rng.random(size=(n, L - 1))
    for t in range(1, L):
        prev = seqs[:, t - 1]
        # For each sequence, sample using its row's cdf.
        rows = cdf[prev]  # (n, 4)
        seqs[:, t] = (u[:, t - 1, None] < rows).argmax(axis=1)
    return seqs


def main(seed=0):
    seqs = sample_sequences(N_SEQ, LEN, seed)
    alpha_arr = np.array(ALPHA)
    chars = alpha_arr[seqs]
    with open(OUT, 'w') as f:
        for row in chars:
            f.write(''.join(row.tolist()))
            f.write('\n')
    # Quick sanity: GC content and CpG depletion.
    gc = ((seqs == 1) | (seqs == 2)).mean()
    # Count CG dinucleotides as fraction of all dinucleotides.
    dinuc = seqs[:, :-1] * 4 + seqs[:, 1:]
    cg_frac = (dinuc == (1 * 4 + 2)).mean()
    cc_frac = (dinuc == (1 * 4 + 1)).mean()
    print(f"wrote {N_SEQ} x {LEN} to {OUT}")
    print(f"GC content: {gc:.3f}  CpG frac: {cg_frac:.4f}  CC frac: {cc_frac:.4f}")


if __name__ == '__main__':
    main(seed=0)
