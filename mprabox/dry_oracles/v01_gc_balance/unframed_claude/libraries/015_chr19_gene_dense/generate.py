"""Experiment 015: chr19 random 200bp slices.
chr19 is the most gene-dense chromosome (~26 genes/Mb vs chr22's 12 vs genome avg 6).
Higher GC (~48%). Tests if even more gene-density improves on chr22.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
FASTA = os.path.join(os.path.dirname(__file__), "..", "..", "data", "hg38.fa")
N = 50_000
L = 200

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_len = len(fa["chr19"])
print(f"chr19 length: {chrom_len}")

rng = np.random.default_rng(100)
seqs = []
attempts = 0
while len(seqs) < N and attempts < N * 5:
    attempts += 1
    p = rng.integers(0, chrom_len - L)
    s = str(fa["chr19"][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)
print(f"Got {len(seqs)} after {attempts} attempts")
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
