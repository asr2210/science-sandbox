#!/usr/bin/env python3
"""
Experiment 003 — Random hg38 genomic windows (200bp).

Tests how much lift comes from real genomic context (composition + motifs +
repeats + biological grammar) vs. synthetic baselines. Samples uniform random
200bp windows from chr8, chr19, chr22 (a gene-poor, gene-dense, and small
chromosome — modest diversity proxy).

Excludes any window containing 'N'. Uses only the forward strand (the model
should be strand-insensitive in a 1D CNN, but I keep it simple).
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
CHRS = ['chr8.fa', 'chr19.fa', 'chr22.fa']  # ~280MB total


def load_chr(path):
    seq_parts = []
    with open(path) as f:
        for line in f:
            if line.startswith('>'):
                continue
            seq_parts.append(line.strip())
    return ''.join(seq_parts).upper()


def sample_from(seq, n, rng, L=LEN, max_tries_factor=10):
    out = []
    L_seq = len(seq)
    if L_seq < L:
        return out
    # Sample more than needed and reject those with N.
    attempts = 0
    max_attempts = n * max_tries_factor
    while len(out) < n and attempts < max_attempts:
        batch = min(n - len(out), 5000)
        starts = rng.integers(0, L_seq - L + 1, size=batch)
        for s in starts:
            sub = seq[s:s + L]
            if 'N' not in sub:
                out.append(sub)
                if len(out) == n:
                    break
        attempts += batch
    return out


def main(seed=0):
    rng = np.random.default_rng(seed)
    chrs = [load_chr(DATA / c) for c in CHRS]
    print('chr lengths:', [len(c) for c in chrs])
    # Allocate roughly proportional to length.
    lens = np.array([len(c) for c in chrs])
    quotas = (lens / lens.sum() * N_SEQ).astype(int)
    # Make sums match N_SEQ.
    quotas[-1] = N_SEQ - quotas[:-1].sum()
    print('quotas:', quotas)
    out = []
    for c, q in zip(chrs, quotas):
        sampled = sample_from(c, q, rng)
        print(f'  got {len(sampled)} from chromosome of length {len(c)}')
        out.extend(sampled)
    assert len(out) == N_SEQ, f"got {len(out)} expected {N_SEQ}"
    rng.shuffle(out)
    # GC sanity.
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out))
        f.write('\n')


if __name__ == '__main__':
    main(seed=0)
