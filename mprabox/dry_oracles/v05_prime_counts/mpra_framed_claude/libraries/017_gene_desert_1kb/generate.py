#!/usr/bin/env python3
"""
Experiment 017 — Deeper gene-desert (1kb cCRE buffer).

Same as 016 but with a 1kb (vs 100bp) exclusion buffer around every cCRE.
Tests whether deeper gene-desert lifts HepG2 transfer further (016 nudged
HepG2 mean from 0.053 to 0.056).
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
BUFFER = 1000
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


def load_ccre_mask(path, chrs, buf):
    masks = {c: np.zeros(len(chrs[c]), dtype=bool) for c in chrs}
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if p[0] not in masks:
                continue
            s, e = int(p[1]), int(p[2])
            s = max(0, s - buf)
            e = min(len(masks[p[0]]), e + buf)
            masks[p[0]][s:e] = True
    return masks


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    all_chrs = load_fasta(DATA / 'hg38.fa')
    chrs = {c: all_chrs[c] for c in MAIN_CHRS if c in all_chrs}
    print(f'building cCRE mask ({BUFFER}bp buffer)...')
    masks = load_ccre_mask(DATA / 'GRCh38-cCREs.bed', chrs, BUFFER)
    total_free = sum((1 - masks[c].mean()) * len(chrs[c]) for c in chrs)
    print(f'  free fraction: {total_free / sum(len(chrs[c]) for c in chrs):.3f}')

    names = list(chrs)
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()

    out = []
    attempts = 0
    max_attempts = N_SEQ * 60
    while len(out) < N_SEQ and attempts < max_attempts:
        batch = min(N_SEQ - len(out), 5000) * 5
        chosen = rng.choice(len(names), size=batch, p=p)
        starts = rng.integers(0, 10**9, size=batch)
        for ci, st in zip(chosen, starts):
            chrom = names[ci]
            cs = chrs[chrom]
            ms = masks[chrom]
            start = int(st % (len(cs) - LEN + 1))
            sub = cs[start:start + LEN]
            if 'N' in sub:
                continue
            if ms[start:start + LEN].any():
                continue
            out.append(sub)
            if len(out) >= N_SEQ:
                break
        attempts += batch
    assert len(out) == N_SEQ
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
