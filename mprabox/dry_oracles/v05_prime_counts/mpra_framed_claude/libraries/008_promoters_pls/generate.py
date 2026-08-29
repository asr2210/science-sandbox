#!/usr/bin/env python3
"""
Experiment 008 — Promoter-focused library (PLS + pELS cCREs).

Hypothesis: promoter-like sequences (PLS) and proximal enhancer-like
sequences (pELS) carry the densest, most universally-active TF-binding
content. Promoters in particular are active in essentially all cell types
because they recruit general transcription machinery. A library biased
toward these should give the model TF features that transfer across cell
types.

40K PLS (+CTCF-bound) and 10K pELS (sampled uniformly) → 50K total.
200bp windows centered on element midpoints.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
MAIN_CHRS = set([f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY'])


def load_fasta(path):
    chrs, cur, parts = {}, None, []
    with open(path) as f:
        for line in f:
            if line.startswith('>'):
                if cur is not None:
                    chrs[cur] = ''.join(parts).upper()
                cur = line[1:].split()[0]; parts = []
            else:
                parts.append(line.rstrip())
        if cur is not None:
            chrs[cur] = ''.join(parts).upper()
    return chrs


def load_ccres(path, types_starts):
    """Load cCREs whose type starts with one of the given prefixes."""
    rows = []
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if p[0] not in MAIN_CHRS:
                continue
            tp = p[5]
            if any(tp.startswith(s) for s in types_starts):
                rows.append((p[0], int(p[1]), int(p[2]), tp))
    return rows


def take_windows(chrs, rows, n, rng):
    rng.shuffle(rows)
    out = []
    half = LEN // 2
    i = 0
    while len(out) < n and i < len(rows):
        chrom, s, e, _ = rows[i]; i += 1
        mid = (s + e) // 2
        ws = mid - half; we = ws + LEN
        if ws < 0 or we > len(chrs[chrom]):
            continue
        sub = chrs[chrom][ws:we]
        if 'N' in sub:
            continue
        out.append(sub)
    return out


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print('loading PLS+pELS cCREs...')
    pls = load_ccres(DATA / 'GRCh38-cCREs.bed', ['PLS'])
    pels = load_ccres(DATA / 'GRCh38-cCREs.bed', ['pELS'])
    print(f'  PLS={len(pls)} pELS={len(pels)}')

    n_pls = 40_000
    n_pels = N_SEQ - n_pls
    print(f'sampling {n_pls} PLS and {n_pels} pELS...')
    a = take_windows(chrs, list(pls), n_pls, rng)
    b = take_windows(chrs, list(pels), n_pels, rng)
    out = a + b
    rng.shuffle(out)
    assert len(out) == N_SEQ
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}; PLS={len(a)} pELS={len(b)}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
