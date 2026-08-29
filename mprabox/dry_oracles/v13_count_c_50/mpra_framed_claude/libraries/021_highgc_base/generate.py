"""Experiment 021: high-GC base library (chr16/17/19/20/22) + cCRE supp.

Replace mc5 (chr8/19/21/22/X, mean GC ~0.42) with high-GC chroms
(chr16/17/19/20/22, mean GC ~0.46). Keep the proven 35k base + 15k
type-balanced cCRE supplement from the same chroms.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr16", "chr17", "chr19", "chr20", "chr22"]
N_GENOMIC = 35_000
N_CCRE = N - N_GENOMIC
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")

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

chrom_set = set(CHROMS)
ccres_by_type = {"PLS": [], "pELS": [], "dELS": [],
                 "CTCF-only": [], "DNase-H3K4me3": []}
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] not in chrom_set:
            continue
        primary = parts[5].split(",")[0]
        if primary in ccres_by_type:
            mid = (int(parts[1]) + int(parts[2])) // 2
            ccres_by_type[primary].append((parts[0], mid))

per_type = N_CCRE // 5
ccre_seqs = []
for t in ccres_by_type:
    pool = ccres_by_type[t]
    idx = rng.choice(len(pool), size=min(len(pool), 4 * per_type), replace=False)
    type_seqs = []
    for i in idx:
        if len(type_seqs) >= per_type:
            break
        chrom, mid = pool[i]
        start, end = mid - HALF, mid - HALF + L
        if start < 0 or end > len(fas[chrom][chrom]):
            continue
        s = fas[chrom][chrom][start:end]
        if len(s) == L and set(s).issubset(valid):
            type_seqs.append(s)
    ccre_seqs.extend(type_seqs)
assert len(ccre_seqs) == N_CCRE

all_seqs = genomic + ccre_seqs
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
base_gcs = np.array([(s.count("G") + s.count("C")) / L for s in genomic])
supp_gcs = np.array([(s.count("G") + s.count("C")) / L for s in ccre_seqs])
print(f"Base GC: {base_gcs.mean():.3f}, supp GC: {supp_gcs.mean():.3f}")
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: high-GC chroms + type-balanced cCREs.")
