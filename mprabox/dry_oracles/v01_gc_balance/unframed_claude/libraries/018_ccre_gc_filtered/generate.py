"""Experiment 018: cCREs filtered by per-sequence GC content (40-55%).
Removes the GC-extreme ends to keep composition near genomic average.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FASTA = os.path.join(ROOT, "hg38.fa")
BED = os.path.join(ROOT, "GRCh38-cCREs.bed")
N = 50_000
L = 200
GC_LOW = 0.40
GC_HIGH = 0.55

regions = []
with open(BED) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        chrom, start, end = parts[0], int(parts[1]), int(parts[2])
        regions.append((chrom, start, end))
print(f"Total cCREs: {len(regions)}")

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}

rng = np.random.default_rng(130)
# Shuffle order, iterate
order = rng.permutation(len(regions))
seqs = []
i_ord = 0
attempts = 0
while len(seqs) < N and i_ord < len(order):
    chrom, start, end = regions[order[i_ord]]
    i_ord += 1
    attempts += 1
    if chrom not in chrom_lens:
        continue
    center = (start + end) // 2
    p = max(0, min(center - L // 2, chrom_lens[chrom] - L))
    s = str(fa[chrom][p:p+L])
    if len(s) != L or "N" in s:
        continue
    gc = (s.count("G") + s.count("C")) / L
    if GC_LOW <= gc <= GC_HIGH:
        seqs.append(s)
print(f"Got {len(seqs)} after {attempts} attempts")
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
