#!/usr/bin/env python3
"""
Experiment 005 — Synthetic library with explicit TF motif injection.

Hypothesis: All natural-DNA libraries clustered at eval_01≈0.04–0.05.
If the bottleneck is "the model can't extract motifs from sparse,
contextually-noisy natural DNA," then deliberately injecting clean,
identifiable TF motifs into random backgrounds may give it the
substrate to learn TF→activity mapping in a way that transfers across
cell types.

Procedure:
- Random uniform background (200bp).
- Choose 1–5 motifs uniformly at random from a hand-curated list of
  ~25 canonical vertebrate TF consensus motifs.
- For each chosen motif: random position (no overlap), 50% RC.
- 50K sequences with seed 0.

Generalization justification: TF binding motifs are essentially shared
across cell types. What differs is TF expression. A model that learns
"these short patterns drive activity" will transfer to a cell type
where some of those TFs are also expressed.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'sequences_0.txt'

N_SEQ = 50_000
LEN = 200
ALPHA = list('ACGT')

# Canonical TF consensus motifs (mostly from JASPAR / literature).
# Hand-selected to span major activator/repressor TF families.
MOTIFS = [
    'TGAGTCA',         # AP-1 (FOS/JUN)
    'TGACTCA',         # AP-1 variant
    'GGGCGG',          # SP1/KLF
    'CACGTG',          # E-box (USF, MYC)
    'CAGCTG',          # MyoD E-box
    'AGATAA',          # GATA1/2/3
    'ACCGGAAGT',       # ETS (ELK, ETS1)
    'GGAAG',           # ETS short
    'TGACGTCA',        # CREB
    'GGGAATTCCC',      # NF-kB
    'AGGAAG',          # ELF
    'AAGTAAACA',       # FOXA
    'TAATTA',          # HOX
    'ATGCAAAT',        # POU/OCT
    'CTATAAATAG',      # MEF2
    'GAACATGTCC',      # p53 half-site
    'TGTGGT',          # RUNX
    'CTTTGT',          # TCF/LEF
    'AGGTGT',          # T-box
    'GTTAATNATTAAC'.replace('N', ''),  # HNF1 (simplified)
    'AGGTCAAAGGTCA',   # nuclear receptor DR1 (HNF4-like)
    'GCGTG',           # AHR (xenobiotic)
    'TTCCAGGAA',       # STAT
    'GAAACTGAAACT',    # IRF
    'CCATCTT',         # YY1
    'CCCTCNCTCCCCCNCCT'.replace('N', ''),  # CTCF simplified
    'TATAAA',          # TATA box
    'AGGTCA',          # NR half-site
    'GGCCAATCT',       # CCAAT/NFY
    'CAAT',            # short CAAT
]

RC_MAP = str.maketrans('ACGT', 'TGCA')

def rc(s):
    return s.translate(RC_MAP)[::-1]


def main(seed=0):
    rng = np.random.default_rng(seed)
    motifs = [m for m in MOTIFS if len(m) > 0]
    motif_lens = np.array([len(m) for m in motifs])
    print(f'{len(motifs)} motifs; lens min={motif_lens.min()} max={motif_lens.max()}')
    alpha = np.array(ALPHA)

    # Pre-build random uniform backgrounds.
    bg_idx = rng.integers(0, 4, size=(N_SEQ, LEN), dtype=np.int8)
    bg = alpha[bg_idx]  # (N_SEQ, LEN) of chars
    # Convert each row to a mutable list.
    seqs = [list(row) for row in bg.tolist()]

    n_motifs_per_seq = rng.integers(1, 6, size=N_SEQ)
    counts = np.zeros(len(motifs), dtype=int)

    for i in range(N_SEQ):
        k = n_motifs_per_seq[i]
        chosen = rng.choice(len(motifs), size=k, replace=True)
        placed_intervals = []
        for m_idx in chosen:
            motif = motifs[m_idx]
            if rng.random() < 0.5:
                motif = rc(motif)
            ml = len(motif)
            # Try positions until non-overlapping.
            for _ in range(20):
                pos = rng.integers(0, LEN - ml + 1)
                if all(pos + ml <= a or b <= pos for (a, b) in placed_intervals):
                    placed_intervals.append((pos, pos + ml))
                    for j, ch in enumerate(motif):
                        seqs[i][pos + j] = ch
                    counts[m_idx] += 1
                    break

    print(f'motif placement counts (top 5): {sorted(counts, reverse=True)[:5]}')
    out_lines = [''.join(s) for s in seqs]
    gc = sum(s.count('G') + s.count('C') for s in out_lines) / (N_SEQ * LEN)
    print(f'GC content: {gc:.3f}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(out_lines))
        f.write('\n')
    print(f'wrote {N_SEQ} x {LEN} to {OUT}')


if __name__ == '__main__':
    main(seed=0)
