"""Experiment 012: FANTOM5 permissive enhancers (~63k).
Validated transcribed enhancers from CAGE data across many cell types.
For 50k sequences, sample with replacement; take 200bp window centered.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FASTA = os.path.join(ROOT, "hg38.fa")
BED = os.path.join(ROOT, "F5.hg38.enhancers.bed")
N = 50_000
L = 200

regions = []
with open(BED) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        chrom, start, end = parts[0], int(parts[1]), int(parts[2])
        regions.append((chrom, start, end))
print(f"Got {len(regions)} FANTOM5 enhancers")

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}

rng = np.random.default_rng(70)
seqs = []
attempts = 0
while len(seqs) < N and attempts < N * 5:
    attempts += 1
    i = rng.integers(0, len(regions))
    chrom, start, end = regions[i]
    if chrom not in chrom_lens:
        continue
    center = (start + end) // 2
    # Jitter slightly to add diversity
    jitter = int(rng.integers(-50, 51))
    p = center - L // 2 + jitter
    p = max(0, min(p, chrom_lens[chrom] - L))
    s = str(fa[chrom][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)
print(f"Got {len(seqs)} after {attempts} attempts")
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
