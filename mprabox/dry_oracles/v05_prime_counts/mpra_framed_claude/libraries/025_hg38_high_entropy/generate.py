#!/usr/bin/env python3
"""
Experiment 025 — High-entropy hg38 windows.

Sample random hg38 windows but reject those with low 4-mer entropy
(repeat / low-complexity regions). Keep the top 50K most-informative
sequences from 150K candidates.

Tests whether filtering out repeat-dominated windows lifts performance.
Hg38 has ~50% repeat content; if many of my random windows hit ALUs or
microsatellites, the model wastes capacity learning those patterns. A
high-entropy library teaches more diverse sequence features per byte.
"""
import os
import numpy as np
import math
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
N_CANDIDATES = 150_000
LEN = 200
K = 4
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


def kmer_entropy(seq, k=4):
    """Shannon entropy of k-mer distribution (max ~log2(4^k)=8 bits for k=4)."""
    n = len(seq) - k + 1
    if n <= 0:
        return 0.0
    counts = Counter(seq[i:i + k] for i in range(n))
    p = np.array(list(counts.values()), dtype=np.float64) / n
    return float(-(p * np.log2(p)).sum())


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    all_chrs = load_fasta(DATA / 'hg38.fa')
    chrs = {c: all_chrs[c] for c in MAIN_CHRS if c in all_chrs}
    names = list(chrs)
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()

    print(f'sampling {N_CANDIDATES} candidates...')
    cands = []
    attempts = 0
    while len(cands) < N_CANDIDATES and attempts < N_CANDIDATES * 5:
        batch = 5000
        chosen = rng.choice(len(names), size=batch, p=p)
        starts = rng.integers(0, 10**9, size=batch)
        for ci, st in zip(chosen, starts):
            chrom = names[ci]
            cs = chrs[chrom]
            start = int(st % (len(cs) - LEN + 1))
            sub = cs[start:start + LEN]
            if 'N' in sub:
                continue
            cands.append(sub)
            if len(cands) >= N_CANDIDATES:
                break
        attempts += batch
    print(f'  got {len(cands)} candidates')
    print('scoring entropy...')
    ents = np.array([kmer_entropy(s, K) for s in cands])
    # Keep top N_SEQ.
    order = np.argsort(-ents)[:N_SEQ]
    out = [cands[i] for i in order]
    print(f'  entropy range kept: {ents[order].min():.3f} – {ents[order].max():.3f}')
    print(f'  entropy range dropped: {ents[order[-1]:].max() if len(order) < len(cands) else "n/a"}')
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
