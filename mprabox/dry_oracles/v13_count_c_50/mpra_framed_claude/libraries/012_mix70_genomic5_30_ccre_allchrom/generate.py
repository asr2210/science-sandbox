"""Experiment 012: 70/30 multi-chrom-5 genomic + cCREs from ALL chromosomes.

Same ratio that won (009), but draw cCREs from all 24 chromosomes (not
just chr8/19/21/22/X). Tests whether broader chromosomal diversity in
the regulatory portion adds value.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
GENOMIC_CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
ALL_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
N_GENOMIC = 35_000
N_CCRE = N - N_GENOMIC
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas_g = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                  sequence_always_upper=True) for c in GENOMIC_CHROMS}
fas_all = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                    sequence_always_upper=True) for c in ALL_CHROMS}
valid = set("ACGT")

per_chrom = N_GENOMIC // len(GENOMIC_CHROMS)
genomic = []
for c in GENOMIC_CHROMS:
    chrom_len = len(fas_g[c][c])
    collected = []
    while len(collected) < per_chrom:
        batch = rng.integers(0, chrom_len - L, size=4 * (per_chrom - len(collected)))
        for start in batch:
            if len(collected) >= per_chrom:
                break
            s = fas_g[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    genomic.extend(collected)

# cCREs from all chromosomes
all_chrom_set = set(ALL_CHROMS)
ccres = []
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] not in all_chrom_set:
            continue
        mid = (int(parts[1]) + int(parts[2])) // 2
        ccres.append((parts[0], mid))
print(f"Total cCREs across {len(ALL_CHROMS)} chroms: {len(ccres)}")

idx = rng.choice(len(ccres), size=min(len(ccres), 4 * N_CCRE), replace=False)
ccre_seqs = []
for i in idx:
    if len(ccre_seqs) >= N_CCRE:
        break
    chrom, mid = ccres[i]
    start, end = mid - HALF, mid - HALF + L
    if start < 0 or end > len(fas_all[chrom][chrom]):
        continue
    s = fas_all[chrom][chrom][start:end]
    if len(s) == L and set(s).issubset(valid):
        ccre_seqs.append(s)
assert len(ccre_seqs) == N_CCRE

all_seqs = genomic + ccre_seqs
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
print(f"Wrote {N}: 35k multi-chrom-5 + 15k cCREs (all chroms).")
