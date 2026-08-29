#!/usr/bin/env python3
"""
Experiment 026 — 30K random hg38 + cCRE-type-balanced 20K (4K each of 5 types).

Tests whether balanced cCRE-type representation (PLS, pELS, dELS, CTCF-only,
DNase-H3K4me3 — 4K each) lifts over the dELS-dominated mix in 013 (where
20K random cCREs are mostly dELS by population frequency).
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_RAND = 30_000
N_PER_TYPE = 4_000
TYPES = ['PLS', 'pELS', 'dELS', 'CTCF-only', 'DNase-H3K4me3']
N_CCRE = N_PER_TYPE * len(TYPES)
N_SEQ = N_RAND + N_CCRE
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


def load_ccres_by_type(path):
    by_type = {t: [] for t in TYPES}
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if p[0] not in MAIN_SET:
                continue
            type_field = p[-1]  # e.g., "dELS,CTCF-bound"
            primary = type_field.split(',')[0]
            if primary in by_type:
                by_type[primary].append((p[0], int(p[1]), int(p[2])))
    return by_type


def sample_random(chrs, rng, n):
    names = [c for c in MAIN_CHRS if c in chrs]
    lens = np.array([len(chrs[c]) for c in names], dtype=np.float64)
    p = lens / lens.sum()
    out = []
    attempts = 0
    max_attempts = n * 10
    while len(out) < n and attempts < max_attempts:
        batch = min(n - len(out), 5000)
        chosen = rng.choice(len(names), size=batch, p=p)
        for ci in chosen:
            chrom = chrs[names[ci]]
            start = int(rng.integers(0, len(chrom) - LEN + 1))
            sub = chrom[start:start + LEN]
            if 'N' in sub:
                continue
            out.append(sub)
            if len(out) >= n:
                break
        attempts += batch
    assert len(out) == n
    return out


def sample_ccre_subset(chrs, ccre_list, rng, n):
    rng.shuffle(ccre_list)
    half = LEN // 2
    out = []
    i = 0
    while len(out) < n and i < len(ccre_list):
        chrom, s, e = ccre_list[i]; i += 1
        mid = (s + e) // 2
        ws = mid - half
        we = ws + LEN
        if ws < 0 or we > len(chrs[chrom]):
            continue
        sub = chrs[chrom][ws:we]
        if 'N' in sub:
            continue
        out.append(sub)
    assert len(out) == n, f'got {len(out)}/{n}'
    return out


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print('loading cCREs by type...')
    by_type = load_ccres_by_type(DATA / 'GRCh38-cCREs.bed')
    for t, lst in by_type.items():
        print(f'  {t}: {len(lst)}')
    print(f'sampling {N_RAND} random + {N_CCRE} balanced cCRE...')
    rand = sample_random(chrs, rng, N_RAND)
    cc_parts = []
    for t in TYPES:
        part = sample_ccre_subset(chrs, by_type[t], rng, N_PER_TYPE)
        cc_parts.extend(part)
    out = rand + cc_parts
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    cpg = sum(s.count('CG') for s in out) / (N_SEQ * (LEN - 1))
    print(f'GC: {gc:.3f}; CpG: {cpg:.4f}; n={N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
