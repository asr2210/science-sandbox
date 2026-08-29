#!/usr/bin/env python3
"""
Experiment 010 — Random hg38 windows from ALL main chromosomes (chr1..22 + X + Y).

Tests whether broader natural DNA sampling (24 chromosomes vs 3 in Exp 003)
improves performance. Same generative process otherwise: uniform random 200bp
windows, no Ns, forward strand only.

Sampling weighted by chromosome length (so larger chromosomes contribute
more sequences). Uses hg38.fa.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
MAIN_CHRS = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']


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


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    all_chrs = load_fasta(DATA / 'hg38.fa')
    chrs = {c: all_chrs[c] for c in MAIN_CHRS if c in all_chrs}
    names = list(chrs)
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()
    print(f'using {len(names)} chromosomes; total len {int(lens.sum()):,}')

    out = []
    attempts = 0
    max_attempts = N_SEQ * 10
    while len(out) < N_SEQ and attempts < max_attempts:
        batch = min(N_SEQ - len(out), 5000)
        chosen_c = rng.choice(len(names), size=batch, p=p)
        for ci in chosen_c:
            chrom = chrs[names[ci]]
            start = int(rng.integers(0, len(chrom) - LEN + 1))
            sub = chrom[start:start + LEN]
            if 'N' in sub:
                continue
            out.append(sub)
            if len(out) >= N_SEQ:
                break
        attempts += batch
    assert len(out) == N_SEQ
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
