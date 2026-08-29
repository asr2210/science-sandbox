"""Experiment 010: 50/50 multi-chrom-5 genomic + cCREs.

Brackets the ratio. Exp 009 (70/30) was 0.575 on eval_01 — new best.
Try more cCRE share to see if grammar holds up.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 25_000
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
ccres = []
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] not in chrom_set:
            continue
        mid = (int(parts[1]) + int(parts[2])) // 2
        ccres.append((parts[0], mid))

idx = rng.choice(len(ccres), size=min(len(ccres), 4 * N_CCRE), replace=False)
ccre_seqs = []
for i in idx:
    if len(ccre_seqs) >= N_CCRE:
        break
    chrom, mid = ccres[i]
    start, end = mid - HALF, mid - HALF + L
    if start < 0 or end > len(fas[chrom][chrom]):
        continue
    s = fas[chrom][chrom][start:end]
    if len(s) == L and set(s).issubset(valid):
        ccre_seqs.append(s)
assert len(ccre_seqs) == N_CCRE

all_seqs = genomic + ccre_seqs
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 25k multi-chrom-5 + 25k cCREs.")
