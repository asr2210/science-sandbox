#!/usr/bin/env python3
"""
Experiment 012 — 5-gram Markov chain matched to hg38.

Estimate 5-gram (4th-order Markov) transition probabilities from a chunk of
hg38, then sample 50K x 200bp sequences from that chain. Tests whether
matching short-range natural-DNA distribution (5-mer composition) is
sufficient to match real DNA performance, or whether real DNA carries
information beyond local k-mer statistics.

Generalization justification: 5-mer statistics capture CpG islands, motif
hints, di/tri/tetra/penta composition. If the model uses primarily these
features, a 5-gram-matched synthetic library should give the same
performance as real DNA. If real DNA is meaningfully better, the model
depends on longer-range structure not captured by local k-mers — which
would suggest pure-distribution-matching libraries are insufficient.

Implementation:
- Read chr8 (~145 Mb) to estimate 5-gram (prefix-4 → next-base) freq.
- Use Laplace smoothing for unseen 4-mers (rare).
- Sample 200bp sequences starting from random 4-mer seed (from observed),
  then extend by 196 with Markov chain.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
K = 5  # 5-gram = 4th-order Markov
PRE = K - 1  # prefix length = 4
ALPHA = 'ACGT'
B2I = {b: i for i, b in enumerate(ALPHA)}
ALPHA_ARR = np.array(list(ALPHA))


def load_chr(path):
    parts = []
    with open(path) as f:
        for line in f:
            if line.startswith('>'):
                continue
            parts.append(line.strip())
    return ''.join(parts).upper()


def kmer_to_idx(kmer):
    """Encode a string of A/C/G/T as base-4 integer."""
    n = 0
    for c in kmer:
        n = n * 4 + B2I[c]
    return n


def estimate_5gram(seq):
    """Return shape (4^4, 4) transition matrix P(next | prefix-4)."""
    N = 4 ** PRE  # 256
    counts = np.zeros((N, 4), dtype=np.int64)
    # Vectorize via integer codes.
    codes = np.fromiter((B2I.get(c, -1) for c in seq), dtype=np.int8, count=len(seq))
    # Skip Ns.
    valid = codes >= 0
    # We need 5-mers fully in valid regions.
    print('total bases:', len(codes), 'valid bases:', valid.sum())
    # Build prefix as 4-mer rolling integer.
    # At the start of each iteration, `pref` is the 4-mer ending at the
    # previous position (if `consecutive >= PRE`). We see new base c and
    # count the transition pref -> c, THEN roll pref forward.
    pref = 0
    consecutive = 0
    for c8 in codes:
        c = int(c8)
        if c < 0:
            consecutive = 0
            pref = 0
            continue
        if consecutive >= PRE:
            counts[pref, c] += 1
        pref = ((pref * 4) + c) % N
        if consecutive < PRE:
            consecutive += 1
    return counts


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading chr8...')
    seq = load_chr(DATA / 'chr8.fa')
    print(f'chr8 length: {len(seq):,}')
    print('estimating 5-gram counts...')
    counts = estimate_5gram(seq)
    print(f'5-gram counts: total transitions = {counts.sum():,}')
    # Laplace smoothing: add 1 to each.
    counts = counts + 1
    probs = counts / counts.sum(axis=1, keepdims=True)
    cdf = np.cumsum(probs, axis=1)

    # Sample 50K x 200 sequences.
    # Initialize each with a random 4-mer drawn from observed 4-mer frequencies.
    pref_freq = counts.sum(axis=1)
    pref_p = pref_freq / pref_freq.sum()
    # Sample initial 4-mer indices.
    init_idx = rng.choice(4 ** PRE, size=N_SEQ, p=pref_p)

    out_codes = np.zeros((N_SEQ, LEN), dtype=np.int8)
    # Decode init 4-mer to bases.
    for j in range(PRE):
        out_codes[:, PRE - 1 - j] = (init_idx >> (2 * j)) & 3

    # Extend.
    cur_pref = init_idx.copy()
    u = rng.random(size=(N_SEQ, LEN - PRE))
    for t in range(PRE, LEN):
        rows = cdf[cur_pref]  # (N_SEQ, 4)
        nxt = (u[:, t - PRE, None] < rows).argmax(axis=1).astype(np.int8)
        out_codes[:, t] = nxt
        cur_pref = (cur_pref * 4 + nxt) % (4 ** PRE)

    chars = ALPHA_ARR[out_codes]
    out = [''.join(row.tolist()) for row in chars]
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG frac: {cg:.4f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')
    print(f'wrote {N_SEQ} sequences')


if __name__ == '__main__':
    main(seed=0)
