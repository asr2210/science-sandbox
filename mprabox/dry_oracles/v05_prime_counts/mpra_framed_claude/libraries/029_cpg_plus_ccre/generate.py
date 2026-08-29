#!/usr/bin/env python3
"""
Experiment 029 — Stack CpG-enriched + cCRE + random.

20K random hg38 + 15K cCRE-centered + 15K CpG-top-by-rank.
Tests whether the CpG lift (028) and cCRE lift (013) STACK or whether one
already contains the other's signal.

Generalization justification: 028 demonstrated CpG-axis lifts over the
random+cCRE 013 baseline by +0.0036. If CpG and cCRE capture orthogonal
regulatory features, stacking should lift further. If 029 ties 028,
they're redundant signals.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_RAND = 20_000
N_CCRE = 15_000
N_CPG = 15_000
N_CAND = 100_000  # for CpG ranking
N_SEQ = N_RAND + N_CCRE + N_CPG
LEN = 200
MAIN_CHRS = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']
MAIN_SET = set(MAIN_CHRS)


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


def load_ccres(path):
    rows = []
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if p[0] not in MAIN_SET:
                continue
            rows.append((p[0], int(p[1]), int(p[2])))
    return rows


def sample_random(chrs, rng, n, names, p):
    out = []
    while len(out) < n:
        chosen = rng.choice(len(names), size=min(n - len(out), 5000), p=p)
        for ci in chosen:
            chrom = chrs[names[ci]]
            start = int(rng.integers(0, len(chrom) - LEN + 1))
            sub = chrom[start:start + LEN]
            if 'N' in sub:
                continue
            out.append(sub)
            if len(out) >= n:
                break
    return out


def sample_ccre(chrs, ccres, rng, n):
    rng.shuffle(ccres)
    half = LEN // 2
    out, i = [], 0
    while len(out) < n and i < len(ccres):
        chrom, s, e = ccres[i]; i += 1
        mid = (s + e) // 2
        ws = mid - half
        we = ws + LEN
        if ws < 0 or we > len(chrs[chrom]):
            continue
        sub = chrs[chrom][ws:we]
        if 'N' in sub:
            continue
        out.append(sub)
    return out


def sample_cpg_enriched(chrs, rng, n_cand, n_keep, names, p):
    cands, cpg = [], []
    while len(cands) < n_cand:
        chosen = rng.choice(len(names), size=min(n_cand - len(cands), 5000), p=p)
        for ci in chosen:
            chrom = chrs[names[ci]]
            start = int(rng.integers(0, len(chrom) - LEN + 1))
            sub = chrom[start:start + LEN]
            if 'N' in sub:
                continue
            cands.append(sub)
            cpg.append(sub.count('CG'))
            if len(cands) >= n_cand:
                break
    cpg = np.array(cpg)
    jit = rng.uniform(0, 0.5, size=len(cpg))
    score = cpg + jit
    top_idx = np.argsort(-score)[:n_keep]
    return [cands[i] for i in top_idx]


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print('loading cCREs...')
    ccres = load_ccres(DATA / 'GRCh38-cCREs.bed')
    print(f'  {len(ccres)} cCREs')
    names = [c for c in MAIN_CHRS if c in chrs]
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()
    print(f'sampling {N_RAND} random, {N_CCRE} cCRE, {N_CPG} CpG-enriched (top {N_CPG}/{N_CAND})...')
    rand = sample_random(chrs, rng, N_RAND, names, p)
    ccre = sample_ccre(chrs, ccres, rng, N_CCRE)
    cpg = sample_cpg_enriched(chrs, rng, N_CAND, N_CPG, names, p)
    out = rand + ccre + cpg
    rng.shuffle(out)
    assert len(out) == N_SEQ
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg_freq = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg_freq:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
