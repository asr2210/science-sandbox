#!/usr/bin/env python3
"""
Experiment 016 — Gene-desert: random hg38 EXCLUDING cCRE-overlapping windows.

50K random 200bp windows from hg38 that DO NOT overlap any ENCODE cCRE.
Tests whether unstructured background DNA is actually a better substrate
for cross-cell-type generalization than cCRE-enriched libraries.

If 016 ≈ 010 (random hg38, eval_01=0.048), regulatory content is roughly
neutral. If 016 > 010, cCRE content actively hurts. If 016 < 010, cCRE
content is mildly beneficial despite the 008/015 evidence.
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


def load_ccre_mask(path, chrs):
    """Build per-chromosome boolean mask True where any cCRE covers position."""
    masks = {c: np.zeros(len(chrs[c]), dtype=bool) for c in chrs}
    n = 0
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if p[0] not in masks:
                continue
            s, e = int(p[1]), int(p[2])
            # Pad cCRE by 100bp on each side to be conservative.
            s = max(0, s - 100)
            e = min(len(masks[p[0]]), e + 100)
            masks[p[0]][s:e] = True
            n += 1
    print(f'  marked {n} cCREs in mask')
    return masks


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    all_chrs = load_fasta(DATA / 'hg38.fa')
    chrs = {c: all_chrs[c] for c in MAIN_CHRS if c in all_chrs}
    print('building cCRE mask...')
    masks = load_ccre_mask(DATA / 'GRCh38-cCREs.bed', chrs)
    free_frac = {c: 1 - masks[c].mean() for c in chrs}
    total_free = sum((1 - masks[c].mean()) * len(chrs[c]) for c in chrs)
    print(f'  free fraction (no cCRE within 100bp): {total_free / sum(len(chrs[c]) for c in chrs):.3f}')

    names = list(chrs)
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()

    out = []
    attempts = 0
    max_attempts = N_SEQ * 30
    while len(out) < N_SEQ and attempts < max_attempts:
        batch = min(N_SEQ - len(out), 5000) * 3  # over-sample, expect some rejects
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
            # Reject if any base in window is within mask (cCRE-overlap).
            if ms[start:start + LEN].any():
                continue
            out.append(sub)
            if len(out) >= N_SEQ:
                break
        attempts += batch
    assert len(out) == N_SEQ, f'got {len(out)}'
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
