#!/usr/bin/env python3
"""
Experiment 027 — Chimeric 100bp cCRE + 100bp random hg38 (within-sequence).

Each 200bp sequence = 100bp from a cCRE center + 100bp random hg38 flank.
Half of the library has cCRE on the LEFT, half on the RIGHT.

Tests whether MPRA-cassette-style sequences (active element embedded in
random context within the same window) match the eval distribution better
than centered cCREs alone. If the held-out eval set is constructed in a
synthetic-context manner (cassette + flank), within-sequence chimerics
should match it better than 013's centered cCREs.

Generalization justification: real MPRA libraries often place a candidate
regulatory element inside a synthetic backbone, then assay activity. A
purely centered cCRE library has the active region spread across the whole
window; a chimeric library localizes activity to a 100bp sub-region with
random flank — closer to a cassette assay layout.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
HALF = 100  # 100bp cCRE + 100bp random
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


def sample_random_frag(chrs, rng, names, p, length):
    while True:
        ci = int(rng.choice(len(names), p=p))
        chrom = chrs[names[ci]]
        start = int(rng.integers(0, len(chrom) - length + 1))
        sub = chrom[start:start + length]
        if 'N' not in sub:
            return sub


def sample_ccre_frag(chrs, ccres, rng, length, attempt_idx):
    """Take a `length`-bp window centered on a cCRE midpoint."""
    half = length // 2
    while attempt_idx[0] < len(ccres):
        chrom, s, e = ccres[attempt_idx[0]]
        attempt_idx[0] += 1
        mid = (s + e) // 2
        ws = mid - half
        we = ws + length
        if ws < 0 or we > len(chrs[chrom]):
            continue
        sub = chrs[chrom][ws:we]
        if 'N' in sub:
            continue
        return sub
    raise RuntimeError('exhausted cCREs')


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print('loading cCREs...')
    ccres = load_ccres(DATA / 'GRCh38-cCREs.bed')
    print(f'  {len(ccres)} cCREs on main chromosomes')
    rng.shuffle(ccres)
    names = [c for c in MAIN_CHRS if c in chrs]
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()
    ccre_idx = [0]
    print(f'building {N_SEQ} chimerics: 100bp cCRE + 100bp random, side randomized...')
    out = []
    for i in range(N_SEQ):
        cc = sample_ccre_frag(chrs, ccres, rng, HALF, ccre_idx)
        rnd = sample_random_frag(chrs, rng, names, p, HALF)
        if rng.random() < 0.5:
            seq = cc + rnd
        else:
            seq = rnd + cc
        out.append(seq)
        if (i + 1) % 10000 == 0:
            print(f'  {i+1}/{N_SEQ}')
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
