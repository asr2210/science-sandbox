"""Experiment 007: 50k 200bp random slices from whole hg38 (autosomes + X).
Diverse multi-chromosome sample to test if diversity alone matters.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
FASTA = os.path.join(os.path.dirname(__file__), "..", "..", "data", "hg38.fa")
N = 50_000
L = 200

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chroms = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
chroms = [c for c in chroms if c in fa.keys()]
chrom_lens = {c: len(fa[c]) for c in chroms}
total = sum(chrom_lens.values())
weights = np.array([chrom_lens[c] for c in chroms]) / total
print(f"Sampling from {len(chroms)} chroms, total {total} bp")

rng = np.random.default_rng(48)
seqs = []
attempts = 0
while len(seqs) < N and attempts < N * 5:
    attempts += 1
    c = rng.choice(chroms, p=weights)
    p = rng.integers(0, chrom_lens[c] - L)
    s = str(fa[c][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)
print(f"Got {len(seqs)} sequences after {attempts} attempts")
assert len(seqs) == N
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print("Done.")
