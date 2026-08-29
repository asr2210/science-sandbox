#!/usr/bin/env python3
"""
Experiment 004 — ENCODE cCRE-centered 200bp windows.

Tests whether enriching the library with known active regulatory elements
(candidate cis-regulatory elements; cCREs from ENCODE V3) widens activity
dynamic range and yields a stronger training signal than random genomic DNA.

Procedure:
- Load hg38.
- Load 1.06M cCREs from BED (chr, start, end, type).
- Randomly sample 50K cCREs (uniform).
- Take 200bp window CENTERED on each cCRE midpoint.
- Reject windows containing N (and resample).
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
    chrs = {}
    cur = None
    parts = []
    with open(path) as f:
        for line in f:
            if line.startswith('>'):
                if cur is not None:
                    chrs[cur] = ''.join(parts).upper()
                cur = line[1:].split()[0]
                parts = []
            else:
                parts.append(line.rstrip())
        if cur is not None:
            chrs[cur] = ''.join(parts).upper()
    return chrs


def load_ccres(path, main_chrs):
    rows = []
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            chrom = p[0]
            if chrom not in main_chrs:
                continue
            start = int(p[1])
            end = int(p[2])
            rows.append((chrom, start, end))
    return rows


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print(f'  loaded {len(chrs)} contigs')
    print('loading cCREs...')
    ccres = load_ccres(DATA / 'GRCh38-cCREs.bed', MAIN_CHRS)
    print(f'  {len(ccres)} cCREs on main chromosomes')
    rng.shuffle(ccres)

    out = []
    half = LEN // 2
    i = 0
    while len(out) < N_SEQ and i < len(ccres):
        chrom, s, e = ccres[i]
        i += 1
        mid = (s + e) // 2
        ws = mid - half
        we = ws + LEN
        if ws < 0 or we > len(chrs[chrom]):
            continue
        sub = chrs[chrom][ws:we]
        if 'N' in sub:
            continue
        out.append(sub)
    assert len(out) == N_SEQ, f'got {len(out)} (used {i} cCREs)'
    rng.shuffle(out)

    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out))
        f.write('\n')
    print(f'wrote {N_SEQ} sequences')


if __name__ == '__main__':
    main(seed=0)
