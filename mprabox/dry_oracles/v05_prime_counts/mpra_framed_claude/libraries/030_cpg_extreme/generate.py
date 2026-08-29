#!/usr/bin/env python3
"""
Experiment 030 — Extreme CpG enrichment (top 50K of 500K, top 10%).

Stricter version of 028 (which used top 50K of 200K, top 25%). Tests
whether the CpG-axis lift saturates or continues to climb with stricter
selectivity.

Generalization justification: 028 demonstrated +0.0036 eval_01 lift over
013 baseline by selecting top-quartile CpG hg38 windows. If the lift is
linear in CpG-density, top-decile should add more. If it saturates or
inverts, 028 is near the optimum on this axis.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_CAND = 500_000
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
    # Memory-efficient: keep just CpG counts and indices, drop low-rank cands periodically
    # Simpler: just hold all 500K (each is 200 bytes => 100MB) - feasible
    cands = []
    cpg = []
    seen = 0
    while seen < N_CAND:
        batch = min(N_CAND - seen, 20000)
        chosen = rng.choice(len(names), size=batch, p=p)
        for ci in chosen:
            chrom = chrs[names[ci]]
            start = int(rng.integers(0, len(chrom) - LEN + 1))
            sub = chrom[start:start + LEN]
            if 'N' in sub:
                continue
            cands.append(sub)
            cpg.append(sub.count('CG'))
            seen += 1
            if seen >= N_CAND:
                break
        if seen % 100000 == 0:
            print(f'  {seen}/{N_CAND}')
    cpg = np.array(cpg)
    print(f'  candidate CpG: median={np.median(cpg):.1f}, p90={np.percentile(cpg,90):.1f}, max={cpg.max()}')
    jit = rng.uniform(0, 0.5, size=len(cpg))
    score = cpg + jit
    top_idx = np.argsort(-score)[:N_SEQ]
    out = [cands[i] for i in top_idx]
    out_cpg = [cpg[i] for i in top_idx]
    print(f'  selected CpG: min={min(out_cpg)}, median={np.median(out_cpg):.1f}')
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg_freq = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg_freq:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
