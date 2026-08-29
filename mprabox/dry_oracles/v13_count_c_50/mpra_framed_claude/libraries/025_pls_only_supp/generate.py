"""Experiment 025: PLS-only cCRE supplement (promoter focus).

35k mc5 + 15k PLS (Promoter-Like Signatures) cCREs from chr5 set.
PLS are CpG-island promoters: very high GC, high CpG, highly active.

Tests if promoter-dominant supplement beats type-balanced (013).
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 35_000
N_SUPP = N - N_GENOMIC
TARGET_TYPE = "PLS"
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")
chrom_set = set(CHROMS)

per_chrom = N_GENOMIC // len(CHROMS)
genomic = []
for c in CHROMS:
    chrom_len = len(fas[c][c])
    collected = []
    while len(collected) < per_chrom:
        batch = rng.integers(0, chrom_len - L, size=4 * (per_chrom - len(collected)))
        for start in batch:
            if len(collected) >= per_chrom:
                break
            s = fas[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    genomic.extend(collected)

pls_pool = []
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] not in chrom_set:
            continue
        primary = parts[5].split(",")[0]
        if primary == TARGET_TYPE:
            mid = (int(parts[1]) + int(parts[2])) // 2
            pls_pool.append((parts[0], mid))
print(f"PLS available in chr5 set: {len(pls_pool)}")

# PLS pool may be smaller than 15k — use with replacement if needed
need_replace = len(pls_pool) < N_SUPP
idx = rng.choice(len(pls_pool), size=min(len(pls_pool), 4 * N_SUPP),
                 replace=need_replace)

supp = []
for i in idx:
    if len(supp) >= N_SUPP:
        break
    chrom, mid = pls_pool[i]
    start, end = mid - HALF, mid - HALF + L
    if start < 0 or end > len(fas[chrom][chrom]):
        continue
    s = fas[chrom][chrom][start:end]
    if len(s) == L and set(s).issubset(valid):
        supp.append(s)

# If still short, sample with replacement
if len(supp) < N_SUPP:
    print(f"only {len(supp)}, sampling with replacement")
    while len(supp) < N_SUPP:
        i = int(rng.integers(0, len(pls_pool)))
        chrom, mid = pls_pool[i]
        start, end = mid - HALF, mid - HALF + L
        if start < 0 or end > len(fas[chrom][chrom]):
            continue
        s = fas[chrom][chrom][start:end]
        if len(s) == L and set(s).issubset(valid):
            supp.append(s)

assert len(supp) == N_SUPP

all_seqs = genomic + supp
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
supp_gcs = np.array([(s.count("G") + s.count("C")) / L for s in supp])
print(f"PLS supp GC: mean={supp_gcs.mean():.3f}, std={supp_gcs.std():.3f}")
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k mc5 + 15k PLS-only cCREs.")
