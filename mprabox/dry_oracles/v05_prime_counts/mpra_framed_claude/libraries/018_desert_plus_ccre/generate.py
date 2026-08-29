#!/usr/bin/env python3
"""
Experiment 018 — 40K gene-desert + 10K cCRE (additive test).

Combine the two directions that helped:
- Gene-desert background (016: HepG2 mean 0.056)
- Light cCRE enrichment (013: eval_01 0.049, HepG2 0.053)

If both lifts compound: eval_01 ~0.050, HepG2 ~0.058.
If they cancel: zero-sum — same signal axis.
If only one shows: that mechanism dominates.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_DESERT = 40_000
N_CCRE = 10_000
N_SEQ = N_DESERT + N_CCRE
LEN = 200
BUFFER = 100
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


def load_ccre_mask_and_list(path, chrs, buf):
    masks = {c: np.zeros(len(chrs[c]), dtype=bool) for c in chrs}
    ccres = []
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if p[0] not in masks:
                continue
            s, e = int(p[1]), int(p[2])
            ccres.append((p[0], s, e))
            ms, me = max(0, s - buf), min(len(masks[p[0]]), e + buf)
            masks[p[0]][ms:me] = True
    return masks, ccres


def sample_desert(chrs, masks, rng, n):
    names = list(chrs)
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()
    out = []
    attempts = 0
    max_attempts = n * 30
    while len(out) < n and attempts < max_attempts:
        batch = min(n - len(out), 5000) * 3
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
            if len(out) >= n:
                break
        attempts += batch
    assert len(out) == n
    return out


def sample_ccre(chrs, ccres, rng, n):
    rng.shuffle(ccres)
    half = LEN // 2
    out = []
    i = 0
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
    assert len(out) == n
    return out


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    all_chrs = load_fasta(DATA / 'hg38.fa')
    chrs = {c: all_chrs[c] for c in MAIN_CHRS if c in all_chrs}
    print('building cCRE mask + list...')
    masks, ccres = load_ccre_mask_and_list(DATA / 'GRCh38-cCREs.bed', chrs, BUFFER)
    print(f'  {len(ccres)} cCREs')
    print(f'sampling {N_DESERT} gene-desert + {N_CCRE} cCRE...')
    desert = sample_desert(chrs, masks, rng, N_DESERT)
    cc = sample_ccre(chrs, ccres, rng, N_CCRE)
    out = desert + cc
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
