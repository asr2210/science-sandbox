"""Experiment 029: mild PhastCons tweak inside the 013 supplement.

35k mc5 base (013 recipe) + 9k type-balanced cCRE + 6k PhastCons
(>=30bp conserved elements, centered). Total 50k.

Hypothesis: pure PhastCons supplement (014) was worse than cCRE (013).
But a SMALL PhastCons fraction (40% of the 15k supplement) inside the
proven cCRE supplement might add a sliver of conservation grammar
without losing the cCRE composition shape.

If 029 > 013 (~0.5765 + noise): mild PhastCons addition helps.
If 029 <= 013: conservation supplement is pure noise on top of cCRE.
"""
from pathlib import Path
import numpy as np
import gzip
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 35_000
N_CCRE = 9_000
N_PC = 6_000
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
PC = DATA / "phastConsElements100way.txt.gz"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")
chrom_set = set(CHROMS)

# Genomic mc5 base
per_chrom = N_GENOMIC // len(CHROMS)
genomic = []
for c in CHROMS:
    chrom_len = len(fas[c][c])
    collected = []
    while len(collected) < per_chrom:
        batch = rng.integers(0, chrom_len - L,
                             size=4 * (per_chrom - len(collected)))
        for start in batch:
            if len(collected) >= per_chrom:
                break
            s = fas[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    genomic.extend(collected)

# Type-balanced cCREs
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
for t, pool in ccres_by_type.items():
    idx = rng.choice(len(pool), size=min(len(pool), 4 * per_type),
                     replace=False)
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

# PhastCons elements >=30bp, centered
pc_elems = []
with gzip.open(PC, "rt") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        chrom = parts[1]
        if chrom not in chrom_set:
            continue
        start, end = int(parts[2]), int(parts[3])
        if end - start < 30:
            continue
        mid = (start + end) // 2
        pc_elems.append((chrom, mid))

idx = rng.choice(len(pc_elems), size=min(len(pc_elems), 4 * N_PC),
                 replace=False)
pc_seqs = []
for i in idx:
    if len(pc_seqs) >= N_PC:
        break
    chrom, mid = pc_elems[i]
    start, end = mid - HALF, mid - HALF + L
    if start < 0 or end > len(fas[chrom][chrom]):
        continue
    s = fas[chrom][chrom][start:end]
    if len(s) == L and set(s).issubset(valid):
        pc_seqs.append(s)
assert len(pc_seqs) == N_PC

all_seqs = genomic + ccre_seqs + pc_seqs
assert len(all_seqs) == N
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")

gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
ccre_gcs = np.array([(s.count("G") + s.count("C")) / L for s in ccre_seqs])
pc_gcs = np.array([(s.count("G") + s.count("C")) / L for s in pc_seqs])
print(f"cCRE GC: {ccre_gcs.mean():.3f}, PhastCons GC: {pc_gcs.mean():.3f}")
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k mc5 + 9k cCRE + 6k PhastCons (60/40 supplement)")
