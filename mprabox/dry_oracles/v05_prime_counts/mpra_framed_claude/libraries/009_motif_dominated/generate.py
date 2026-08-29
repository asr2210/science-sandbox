#!/usr/bin/env python3
"""
Experiment 009 — Motif-dominated synthetic library (~80% motif content).

Each 200bp sequence is densely packed with 15–25 TF motifs (4–15bp each)
with 1–4bp random linkers between them. Result: most bases come from a
known TF motif. The sequence statistics are dominated by motif content
rather than the random background.

Hypothesis: if the model can learn TF→activity grammar from a from-scratch
50K library, this distribution should be the most permissive: every
sequence has dozens of recognizable motifs, so motif counts/types are
the dominant feature.

Generalization justification: TF motifs are shared across cell types. A
model that learns the strength of each motif's contribution will be able
to predict activity in unseen cell types (assuming those cell types
express overlapping TFs).
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
ALPHA = list('ACGT')
RC_MAP = str.maketrans('ACGT', 'TGCA')

MOTIFS = [
    'TGAGTCA', 'TGACTCA', 'GGGCGG', 'CACGTG', 'CAGCTG',
    'AGATAA', 'ACCGGAAGT', 'GGAAGT', 'TGACGTCA', 'GGGAATTCCC',
    'AGGAAG', 'AAGTAAACA', 'TAATTA', 'ATGCAAAT', 'CTATAAATAG',
    'GAACATGTCC', 'TGTGGT', 'CTTTGT', 'AGGTGT', 'GTTAATATTAAC',
    'AGGTCAAAGGTCA', 'GCGTG', 'TTCCAGGAA', 'GAAACTGAAACT', 'CCATCTT',
    'CCCTCCTCCCCCCT', 'TATAAA', 'AGGTCA', 'GGCCAATCT',
    'GATAAG', 'CCAAT', 'GCGCGC', 'TGCAGT',
]


def rc(s):
    return s.translate(RC_MAP)[::-1]


def build_dense(n, rng):
    alpha = np.array(ALPHA)
    motifs = [m for m in MOTIFS if len(m) > 0]
    out = []
    for i in range(n):
        seq = []
        while sum(len(p) for p in seq) < LEN:
            mi = rng.integers(0, len(motifs))
            m = motifs[mi]
            if rng.random() < 0.5:
                m = rc(m)
            seq.append(m)
            # Random linker 0-3bp.
            linker_len = int(rng.integers(0, 4))
            if linker_len > 0:
                linker_idx = rng.integers(0, 4, size=linker_len)
                seq.append(''.join(alpha[linker_idx]))
        full = ''.join(seq)
        # Truncate or pad to LEN.
        if len(full) > LEN:
            # Random start within the over-built sequence.
            start = rng.integers(0, len(full) - LEN + 1)
            full = full[start:start + LEN]
        else:
            full = full + ''.join(alpha[rng.integers(0, 4, size=LEN - len(full))])
        out.append(full)
    return out


def main(seed=0):
    rng = np.random.default_rng(seed)
    print(f'{len(MOTIFS)} motifs, lengths {min(len(m) for m in MOTIFS)}..{max(len(m) for m in MOTIFS)}')
    seqs = build_dense(N_SEQ, rng)
    assert all(len(s) == LEN for s in seqs)
    rng.shuffle(seqs)
    gc = sum(s.count('G') + s.count('C') for s in seqs) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}; wrote {N_SEQ} x {LEN}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(seqs)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
