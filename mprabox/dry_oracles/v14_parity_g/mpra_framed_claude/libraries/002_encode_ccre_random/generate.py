"""Experiment 002: 50k random ENCODE V4 cCREs as 200bp windows.

Sample 50,000 candidate cis-regulatory elements from ENCODE V4
registry (2.35M elements) and extract a 200bp window centered on each.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
N = 50_000
L = 200

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BED = os.path.join(ROOT, "data", "ENCFF864OWG.bed")
FA = os.path.join(ROOT, "data", "hg38.fa")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(SEED)

# Load BED
print("Loading BED...")
regions = []
with open(BED) as f:
    for line in f:
        cols = line.rstrip().split("\t")
        chrom, start, end = cols[0], int(cols[1]), int(cols[2])
        # Skip alt/random/unplaced contigs for cleanness
        if "_" in chrom or chrom == "chrM":
            continue
        regions.append((chrom, start, end))

print(f"loaded {len(regions)} regulatory regions")

# Sample N * 1.5 to allow rejection (Ns)
sample_idx = rng.choice(len(regions), size=int(N * 1.5), replace=False)

fa = Fasta(FA, sequence_always_upper=True)

seqs = []
for i in sample_idx:
    chrom, start, end = regions[i]
    center = (start + end) // 2
    s = center - L // 2
    e = s + L
    if s < 0:
        continue
    chrom_len = len(fa[chrom])
    if e > chrom_len:
        continue
    seq = str(fa[chrom][s:e])
    if "N" in seq or len(seq) != L:
        continue
    seqs.append(seq)
    if len(seqs) == N:
        break

assert len(seqs) == N, f"only got {len(seqs)}"
print(f"got {len(seqs)} sequences")

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"wrote {OUT}")
