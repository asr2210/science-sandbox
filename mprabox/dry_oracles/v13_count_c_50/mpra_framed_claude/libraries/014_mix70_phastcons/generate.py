"""Experiment 014: 70% multi-chrom-5 genomic + 30% PhastCons-centered.

Replace the cCRE supplement with a different functional curation:
evolutionarily conserved elements (PhastCons 100-way). PhastCons regions
are functionally constrained across vertebrates → contain universal
regulatory grammar, plus a different subset than just enhancer/promoter
annotations.

Filter for length ≥ 30bp (top ~10% of elements; small ones are noise).
Then take 200bp windows centered on each element.
"""
from pathlib import Path
import numpy as np
import gzip
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
MIN_ELEM = 30
GENOMIC_CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
ALL_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
N_GENOMIC = 35_000
N_PC = N - N_GENOMIC
DATA = Path(__file__).resolve().parents[2] / "data"
PC = DATA / "phastConsElements100way.txt.gz"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in ALL_CHROMS}
valid = set("ACGT")

# Genomic from chr5 (proven recipe)
per_chrom = N_GENOMIC // len(GENOMIC_CHROMS)
genomic = []
for c in GENOMIC_CHROMS:
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

# PhastCons elements ≥ MIN_ELEM bp from chr5 set first (GC alignment)
chrom_set = set(GENOMIC_CHROMS)
pc_elems = []
with gzip.open(PC, "rt") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        # Schema: bin, chrom, start, end, name(lod=X), score
        chrom = parts[1]
        if chrom not in chrom_set:
            continue
        start = int(parts[2])
        end = int(parts[3])
        if end - start < MIN_ELEM:
            continue
        mid = (start + end) // 2
        pc_elems.append((chrom, mid))
print(f"PhastCons elements ≥ {MIN_ELEM}bp in chr5 set: {len(pc_elems)}")

idx = rng.choice(len(pc_elems), size=min(len(pc_elems), 4 * N_PC), replace=False)
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
assert len(pc_seqs) == N_PC, f"only got {len(pc_seqs)}"

all_seqs = genomic + pc_seqs
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k multi-chrom-5 + 15k PhastCons-centered.")
