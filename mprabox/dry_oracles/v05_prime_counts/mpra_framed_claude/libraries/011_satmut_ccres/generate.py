#!/usr/bin/env python3
"""
Experiment 011 — Saturation-mutagenesis-like library on 500 cCREs.

Take 500 ENCODE cCREs (sampled uniformly from all types). For each, generate
100 variants:
  - 1 original cCRE-centered 200bp window
  - 99 mutants with a number of random point mutations chosen so that the
    library covers a wide range of perturbation strengths:
      - ~20 mutants with 1-2 point mutations (mild)
      - ~30 mutants with 3-6 mutations (moderate)
      - ~30 mutants with 7-15 mutations (heavy)
      - ~19 mutants with 16-40 mutations (severe)

Hypothesis: each (cCRE, variant) pair gives the MPRA a slightly different
activity. With 100 measurements per biological context, the model can learn
position-specific contributions (which positions matter for activity) much
more efficiently than from independent sequences. This is label-informative
library design.

Generalization justification: the model learns *features of motif
disruption*: that mutating bases inside known TF binding sites reduces
activity, while mutating background bases doesn't. These features apply to
ANY TF and ANY cell type that uses the same TF motifs, so the learned
representations should transfer beyond K562/HepG2/SK-N-SH.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_CCRES = 500
N_PER = 100
N_SEQ = N_CCRES * N_PER  # 50000
LEN = 200
MAIN_CHRS = set([f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY'])
ALPHA = np.array(list('ACGT'))


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
            if p[0] not in MAIN_CHRS:
                continue
            rows.append((p[0], int(p[1]), int(p[2])))
    return rows


def get_window(chrs, chrom, s, e):
    mid = (s + e) // 2
    ws = mid - LEN // 2
    we = ws + LEN
    if ws < 0 or we > len(chrs[chrom]):
        return None
    sub = chrs[chrom][ws:we]
    if 'N' in sub:
        return None
    return sub


def make_variants(orig, rng):
    """For one cCRE: return 100 variants spanning mild to severe."""
    orig_arr = np.array([ord(c) for c in orig], dtype=np.uint8)  # ACGT bytes
    a_codes = np.array([ord(c) for c in 'ACGT'], dtype=np.uint8)
    variants = [orig]
    # Distribution of mutation counts.
    # 20 mild, 30 moderate, 30 heavy, 19 severe.
    mut_counts = (
        list(rng.integers(1, 3, size=20))    # 1-2
        + list(rng.integers(3, 7, size=30))  # 3-6
        + list(rng.integers(7, 16, size=30))  # 7-15
        + list(rng.integers(16, 41, size=19))  # 16-40
    )
    assert len(mut_counts) == 99
    for k in mut_counts:
        v = orig_arr.copy()
        positions = rng.choice(LEN, size=int(k), replace=False)
        for p in positions:
            cur = v[p]
            # Pick a different base.
            others = a_codes[a_codes != cur]
            v[p] = others[rng.integers(0, 3)]
        variants.append(v.tobytes().decode())
    return variants


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print('loading cCREs...')
    ccres = load_ccres(DATA / 'GRCh38-cCREs.bed')
    rng.shuffle(ccres)

    selected = []
    i = 0
    while len(selected) < N_CCRES and i < len(ccres):
        chrom, s, e = ccres[i]; i += 1
        w = get_window(chrs, chrom, s, e)
        if w is not None:
            selected.append(w)
    assert len(selected) == N_CCRES, f'got only {len(selected)}'
    print(f'selected {len(selected)} cCREs')

    out = []
    for orig in selected:
        out.extend(make_variants(orig, rng))
    assert len(out) == N_SEQ
    rng.shuffle(out)
    gc = sum(s.count('G') + s.count('C') for s in out) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}; {N_SEQ} sequences')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
