#!/usr/bin/env python3
"""
Experiment 022 — GC-stratified random hg38.

Sample 50K windows with uniform coverage of GC bins. Natural hg38 is
heavily skewed toward 40% GC. Force the library to span 30-70% GC in 4
equal-frequency bins, so the model gets better coverage of high-GC
sequences (promoters, CpG islands) and low-GC sequences (gene deserts).
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

PER_BIN = 12_500
BINS = [(0.30, 0.40), (0.40, 0.50), (0.50, 0.60), (0.60, 0.70)]
N_SEQ = PER_BIN * len(BINS)
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

    bin_counts = [0] * len(BINS)
    bin_targets = [PER_BIN] * len(BINS)
    out = []
    attempts = 0
    max_attempts = N_SEQ * 100
    while sum(bin_counts) < N_SEQ and attempts < max_attempts:
        batch = 10000
        chosen = rng.choice(len(names), size=batch, p=p)
        starts = rng.integers(0, 10**9, size=batch)
        for ci, st in zip(chosen, starts):
            chrom = names[ci]
            cs = chrs[chrom]
            start = int(st % (len(cs) - LEN + 1))
            sub = cs[start:start + LEN]
            if 'N' in sub:
                continue
            gc = (sub.count('G') + sub.count('C')) / LEN
            for bi, (lo, hi) in enumerate(BINS):
                if lo <= gc < hi and bin_counts[bi] < bin_targets[bi]:
                    out.append(sub)
                    bin_counts[bi] += 1
                    break
            if sum(bin_counts) >= N_SEQ:
                break
        attempts += batch
        if attempts % 100000 == 0:
            print(f'  attempts={attempts}; bins={bin_counts}')
    print(f'  final bins={bin_counts}; attempts={attempts}')
    assert sum(bin_counts) == N_SEQ, f'got {sum(bin_counts)}'
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
