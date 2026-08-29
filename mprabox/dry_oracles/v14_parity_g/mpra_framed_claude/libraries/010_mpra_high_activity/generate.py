"""Experiment 010: top-|log2FC| Tewhey MPRA BED regions (excl chr7/13).

008 showed mean_r=0.003, eval_13 K562=0.0143 with uniform sampling
across the same Tewhey BED pool (365k regions, sampled 50k uniformly).
But 008's regions span the entire activity distribution, including
very many weak ones (mode at log2FC≈0).

Hypothesis: the model learns better from strong activity gradients.
Filter the same Tewhey pool to top 50k by |log2FoldChange|. If this
boosts mean_r vs 008, magnitude filtering matters and we go further.

Procedure:
- pool 200bp BED regions from K562, HepG2, SK-N-SH MPRA BEDs
- excl chr7/13, chrM, alt contigs
- dedupe by coordinate (keep max |log2FC| if duplicated across cells)
- pick top 50,000 unique regions by |log2FC|
- extract hg38 sequence, skip N/short
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
N = 50_000

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
BEDS = [
    os.path.join(ROOT, "data", "ENCFF822KPE.bed"),  # K562
    os.path.join(ROOT, "data", "ENCFF887WCC.bed"),  # HepG2
    os.path.join(ROOT, "data", "ENCFF861MOC.bed"),  # SK-N-SH
]
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"chr7", "chr13"}

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)

# pool (chrom,start,end) -> max |log2FC|
region_abs_lfc = {}
for bed in BEDS:
    with open(bed) as f:
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[0]
            if chrom in EXCLUDE_CHR or "_" in chrom or chrom == "chrM":
                continue
            s, e = int(cols[1]), int(cols[2])
            if e - s != L:
                c = (s + e) // 2
                s = c - L // 2
                e = s + L
            try:
                lfc = float(cols[6])
            except (ValueError, IndexError):
                continue
            key = (chrom, s, e)
            v = abs(lfc)
            if key not in region_abs_lfc or v > region_abs_lfc[key]:
                region_abs_lfc[key] = v

print(f"pooled unique regions (excl chr7/13): {len(region_abs_lfc)}")

# sort by |log2FC| descending
sorted_regions = sorted(region_abs_lfc.items(), key=lambda kv: -kv[1])

seqs = []
for (chrom, s, e), lfc in sorted_regions:
    if chrom not in fa.keys():
        continue
    if s < 0 or e > len(fa[chrom]):
        continue
    seq = str(fa[chrom][s:e])
    if "N" in seq or len(seq) != L:
        continue
    seqs.append(seq)
    if len(seqs) == N:
        break

print(f"got {len(seqs)} top-|log2FC| sequences (lowest kept |log2FC| ~ {lfc:.3f})")
assert len(seqs) == N

# Shuffle so order isn't activity-correlated (in case the model
# would exploit positional ordering, which it shouldn't).
rng.shuffle(seqs)

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote to {OUT}")
