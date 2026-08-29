"""Experiment 008: 200bp sequences from Tewhey lab MPRA libraries (K562/HepG2/SK-N-SH).

Sources (ENCODE element quantification BED files from Tewhey lab MPRA assays):
- K562   : ENCFF822KPE (228k 200bp regions)
- HepG2  : ENCFF887WCC (109k 200bp regions)
- SK-N-SH: ENCFF861MOC (28k 200bp regions)

These are the exact format the simulator likely models: 200bp genomic
windows around (mostly) variants tested by MPRA in the three target
cell types.

EXCLUDES chr7 and chr13 (Gosai/Siraj convention test holdout).

Rationale: previous experiments (random, cCREs, motif inserts, DNase
peaks) all gave ~0. The eval simulator/model was likely trained on
MPRA data of this exact form. Matching the training distribution
should let the model learn something the simulator recognizes.

Generalization: human regulatory grammar is shared across cell types;
the simulator trained on these 3 should output coherent values for
other cell types' regulatory grammar too, provided my model learns
the underlying motif vocabulary.
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

# Pool all regions (deduplicate by coordinate)
all_regions = set()
for bed in BEDS:
    with open(bed) as f:
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[0]
            if chrom in EXCLUDE_CHR or "_" in chrom or chrom == "chrM":
                continue
            s, e = int(cols[1]), int(cols[2])
            if e - s != L:
                # adjust to L
                c = (s + e) // 2
                s = c - L // 2
                e = s + L
            all_regions.add((chrom, s, e))

all_regions = list(all_regions)
print(f"pooled unique regions (excl chr7/13): {len(all_regions)}")

rng.shuffle(all_regions)

seqs = []
for chrom, s, e in all_regions:
    if s < 0 or e > len(fa[chrom]):
        continue
    seq = str(fa[chrom][s:e])
    if "N" in seq or len(seq) != L:
        continue
    seqs.append(seq)
    if len(seqs) == N:
        break

print(f"got {len(seqs)} sequences")
assert len(seqs) == N

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote to {OUT}")
