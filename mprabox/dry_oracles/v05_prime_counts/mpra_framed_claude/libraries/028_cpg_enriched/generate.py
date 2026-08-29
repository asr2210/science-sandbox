#!/usr/bin/env python3
"""
Experiment 028 — Natural-context CpG-enriched hg38 windows.

Sample 200K candidate windows; rank by CpG count; take top 50K.
Tests whether high-CpG natural context (a strong promoter/regulatory signal)
lifts over the 013 random+cCRE baseline.

Generalization justification: CpG islands are a key regulatory feature that
spans promoters AND many enhancers. They're enriched in cCREs but not all
cCREs are CpG-rich, and many CpG-rich regions are not in the cCRE catalog.
Sampling on the CpG axis is orthogonal to the cCRE axis tested in 013/023.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_CAND = 200_000
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
    chrs = load_fasta(DATA / 'hg38.fa')
    names = [c for c in MAIN_CHRS if c in chrs]
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()
    print(f'sampling {N_CAND} candidates...')
    cands = []
    cpg_counts = []
    attempts = 0
    while len(cands) < N_CAND and attempts < N_CAND * 8:
        batch = min(N_CAND - len(cands), 10000)
        chosen = rng.choice(len(names), size=batch, p=p)
        for ci in chosen:
            chrom = chrs[names[ci]]
            start = int(rng.integers(0, len(chrom) - LEN + 1))
            sub = chrom[start:start + LEN]
            if 'N' in sub:
                continue
            cands.append(sub)
            cpg_counts.append(sub.count('CG'))
            if len(cands) >= N_CAND:
                break
        attempts += batch
        if len(cands) % 50000 == 0:
            print(f'  {len(cands)}/{N_CAND}')
    print(f'  {len(cands)} candidates; CpG counts: median={np.median(cpg_counts):.1f}, max={max(cpg_counts)}')
    cpg_counts = np.array(cpg_counts)
    # Take top N_SEQ by CpG count (ties broken randomly by argsort tie order)
    # Add tiny random jitter to break ties
    jit = rng.uniform(0, 0.5, size=len(cpg_counts))
    score = cpg_counts + jit
    top_idx = np.argsort(-score)[:N_SEQ]
    out = [cands[i] for i in top_idx]
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
