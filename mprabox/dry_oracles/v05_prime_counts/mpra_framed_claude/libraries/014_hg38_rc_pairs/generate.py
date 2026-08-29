#!/usr/bin/env python3
"""
Experiment 014 — Strand augmentation: 25K random hg38 windows + their RC.

For each of 25K random 200bp windows from hg38, generate the forward
sequence AND its reverse complement. Total = 50K sequences, 25K distinct
biological contexts but the model sees each context from both strands.

Generalization justification: TF binding sites are largely strand-symmetric
(e.g., palindromic motifs like CACGTG, asymmetric motifs like GATA that
operate on either strand). Showing the model paired strands forces it to
learn strand-invariant features — which is the right inductive bias for
generalization to unseen sequences where any motif can appear on either
strand.

Tradeoff: lower context diversity (25K vs 50K). Exp 011 showed diversity
matters; this halves contexts to gain explicit RC pairing. If prepare.py
already RC-augments internally, this provides no lift and only hurts via
diversity loss. If it doesn't, the lift should outweigh the diversity cost.
"""
import os
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'sequences_0.txt'

N_CTX = 25_000
LEN = 200
N_SEQ = N_CTX * 2
MAIN_CHRS = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']

RC = str.maketrans('ACGT', 'TGCA')


def rev_comp(s):
    return s.translate(RC)[::-1]


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


def sample_windows(chrs, rng, n):
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


def main(seed=0):
    rng = np.random.default_rng(seed)
    print('loading hg38...')
    chrs = load_fasta(DATA / 'hg38.fa')
    print(f'sampling {N_CTX} contexts...')
    fwd = sample_windows(chrs, rng, N_CTX)
    print('generating RC pairs...')
    pairs = []
    for s in fwd:
        pairs.append(s)
        pairs.append(rev_comp(s))
    assert len(pairs) == N_SEQ
    rng.shuffle(pairs)
    gc = sum(s.count('G') + s.count('C') for s in pairs) / (N_SEQ * LEN)
    print(f'GC: {gc:.3f}; total {N_SEQ}')
    with open(OUT, 'w') as f:
        f.write('\n'.join(pairs)); f.write('\n')


if __name__ == '__main__':
    main(seed=0)
