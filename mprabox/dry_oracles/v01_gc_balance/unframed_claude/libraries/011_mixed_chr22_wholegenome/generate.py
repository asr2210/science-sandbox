"""Experiment 011: Mix 25k chr22 random + 25k whole-genome random.
Tests whether more biological diversity (gene-rich + gene-poor) improves r.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
FASTA = os.path.join(os.path.dirname(__file__), "..", "..", "data", "hg38.fa")
N_PER = 25_000
L = 200

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chr22_len = len(fa["chr22"])

rng = np.random.default_rng(60)

# First half: chr22 only
seqs = []
attempts = 0
while len(seqs) < N_PER and attempts < N_PER * 5:
    attempts += 1
    p = rng.integers(0, chr22_len - L)
    s = str(fa["chr22"][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)

# Second half: whole genome (autosomes + X)
chroms = [f"chr{i}" for i in range(1, 23)] + ["chrX"]
chrom_lens = {c: len(fa[c]) for c in chroms if c in fa.keys()}
total = sum(chrom_lens.values())
weights = np.array([chrom_lens[c] for c in chroms]) / total

attempts = 0
while len(seqs) < 2 * N_PER and attempts < N_PER * 5:
    attempts += 1
    c = rng.choice(chroms, p=weights)
    p = rng.integers(0, chrom_lens[c] - L)
    s = str(fa[c][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)

print(f"Got {len(seqs)} sequences")
# Shuffle order
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
