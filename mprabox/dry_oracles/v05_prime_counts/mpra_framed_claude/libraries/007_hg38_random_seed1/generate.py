#!/usr/bin/env python3
"""
Experiment 007 — Replicate of Exp 003 with seed=1.

Purpose: estimate library-level variance. If a *new draw* from the same
process (random 200bp hg38 windows from chr8/19/22) gives a noticeably
different eval_01, then the 0.04–0.05 differences across my designs may be
noise rather than signal. If it gives the same eval_01 (within ~0.005),
library design DOES matter even in this band.

Reuses the exact generate.py logic from 003 but with seed=1.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
CHRS = ['chr8.fa', 'chr19.fa', 'chr22.fa']


def load_chr(path):
    seq_parts = []
    with open(path) as f:
        for line in f:
            if line.startswith('>'):
                continue
            seq_parts.append(line.strip())
    return ''.join(seq_parts).upper()


def sample_from(seq, n, rng, L=LEN):
    out = []
    L_seq = len(seq)
    while len(out) < n:
        batch = min(n - len(out), 5000)
        starts = rng.integers(0, L_seq - L + 1, size=batch)
        for s in starts:
            sub = seq[s:s + L]
            if 'N' not in sub:
                out.append(sub)
                if len(out) == n:
                    break
    return out


def main(seed=1):
    rng = np.random.default_rng(seed)
    chrs = [load_chr(DATA / c) for c in CHRS]
    lens = np.array([len(c) for c in chrs])
    quotas = (lens / lens.sum() * N_SEQ).astype(int)
    quotas[-1] = N_SEQ - quotas[:-1].sum()
    out = []
    for c, q in zip(chrs, quotas):
        out.extend(sample_from(c, q, rng))
    assert len(out) == N_SEQ
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out))
        f.write('\n')


if __name__ == '__main__':
    main(seed=1)
