#!/usr/bin/env python3
"""
Experiment 006 — Multi-source diverse library.

Mix three sources in equal parts to test if heterogeneity broadens what the
model can learn from a 50K library:
  - 16,667 cCRE-centered 200bp windows (regulatory enriched)
  - 16,667 random hg38 200bp windows (background diversity)
  - 16,666 synthetic dense-motif backgrounds (~10 motifs/seq)

Generalization justification: eval sets are anonymous and may draw from
varied distributions. A library combining regulatory, neutral, and explicit
motif content covers the broadest swath of cis-grammar substrate. If any
single source were strongly superior, the cluster at 0.04–0.05 across
single-source libraries would not be so flat.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
PER = N_SEQ // 3  # 16666; +1 to second part to reach 50000
PARTS = (16667, 16667, 16666)
MAIN_CHRS = set([f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY'])
ALPHA = list('ACGT')
RC_MAP = str.maketrans('ACGT', 'TGCA')


MOTIFS = [
    'TGAGTCA', 'TGACTCA', 'GGGCGG', 'CACGTG', 'CAGCTG',
    'AGATAA', 'ACCGGAAGT', 'GGAAG', 'TGACGTCA', 'GGGAATTCCC',
    'AGGAAG', 'AAGTAAACA', 'TAATTA', 'ATGCAAAT', 'CTATAAATAG',
    'GAACATGTCC', 'TGTGGT', 'CTTTGT', 'AGGTGT', 'GTTAATATTAAC',
    'AGGTCAAAGGTCA', 'GCGTG', 'TTCCAGGAA', 'GAAACTGAAACT', 'CCATCTT',
    'CCCTCCTCCCCCCT', 'TATAAA', 'AGGTCA', 'GGCCAATCT', 'CAAT',
]


def rc(s):
    return s.translate(RC_MAP)[::-1]


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


def load_ccres(path):
    rows = []
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            chrom = p[0]
            if chrom not in MAIN_CHRS:
                continue
            rows.append((chrom, int(p[1]), int(p[2])))
    return rows


def sample_ccres(chrs, ccres, n, rng):
    rng.shuffle(ccres)
    out = []
    half = LEN // 2
    i = 0
    while len(out) < n and i < len(ccres):
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
    return out


def sample_random_hg38(chrs, n, rng):
    main = [c for c in chrs if c in MAIN_CHRS]
    lens = np.array([len(chrs[c]) for c in main], dtype=np.float64)
    p = lens / lens.sum()
    out = []
    attempts = 0
    while len(out) < n and attempts < n * 10:
        batch = min(n - len(out), 5000)
        chosen = rng.choice(len(main), size=batch, p=p)
        starts = [rng.integers(0, len(chrs[main[c]]) - LEN + 1) for c in chosen]
        for c_idx, start in zip(chosen, starts):
            sub = chrs[main[c_idx]][start:start + LEN]
            if 'N' in sub:
                continue
            out.append(sub)
            if len(out) >= n:
                break
        attempts += batch
    return out


def synth_motif_dense(n, rng, k_motifs=10):
    motifs = MOTIFS
    alpha = np.array(ALPHA)
    bg_idx = rng.integers(0, 4, size=(n, LEN), dtype=np.int8)
    bg = alpha[bg_idx]
    seqs = [list(row) for row in bg.tolist()]
    for i in range(n):
        chosen = rng.choice(len(motifs), size=k_motifs, replace=True)
        placed = []
        for m_idx in chosen:
            motif = motifs[m_idx]
            if rng.random() < 0.5:
                motif = rc(motif)
            ml = len(motif)
            for _ in range(30):
                pos = rng.integers(0, LEN - ml + 1)
                if all(pos + ml <= a or b <= pos for (a, b) in placed):
                    placed.append((pos, pos + ml))
                    for j, ch in enumerate(motif):
                        seqs[i][pos + j] = ch
                    break
    return [''.join(s) for s in seqs]


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print('loading cCREs...')
    ccres = load_ccres(DATA / 'GRCh38-cCREs.bed')

    print('sampling cCREs...')
    part1 = sample_ccres(chrs, ccres, PARTS[0], rng)
    print(f'  got {len(part1)}')
    print('sampling random hg38...')
    part2 = sample_random_hg38(chrs, PARTS[1], rng)
    print(f'  got {len(part2)}')
    print('building synthetic dense motifs...')
    part3 = synth_motif_dense(PARTS[2], rng, k_motifs=10)
    print(f'  got {len(part3)}')

    all_seqs = part1 + part2 + part3
    assert len(all_seqs) == N_SEQ
    rng.shuffle(all_seqs)
    gc = sum(s.count('G') + s.count('C') for s in all_seqs) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(all_seqs))
        f.write('\n')
    print(f'wrote {N_SEQ} sequences to {OUT}')


if __name__ == '__main__':
    main(seed=0)
