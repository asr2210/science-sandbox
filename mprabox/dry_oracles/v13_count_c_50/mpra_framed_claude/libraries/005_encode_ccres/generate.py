"""Experiment 005: ENCODE candidate cis-regulatory elements (cCREs).

Tests whether sequences enriched for regulatory function (motif-dense)
substantially outperform random natural sequences. Sample 50,000 cCREs
from the 5 chromosomes already on disk (chr8, chr19, chr21, chr22, chrX),
center each on its midpoint, extract a 200bp window.

cCRE set: ENCODE V3 SCREEN (~1M cCREs total).
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = {"chr8", "chr19", "chr21", "chr22", "chrX"}
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)

# Read all cCREs in our chromosomes
ccres = []  # (chrom, mid, classification)
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        chrom = parts[0]
        if chrom not in CHROMS:
            continue
        start, end = int(parts[1]), int(parts[2])
        mid = (start + end) // 2
        cls = parts[5] if len(parts) > 5 else "."
        ccres.append((chrom, mid, cls))

print(f"Found {len(ccres)} cCREs in {sorted(CHROMS)}")
# Random sample
idx = rng.choice(len(ccres), size=min(len(ccres), 4 * N), replace=False)
candidates = [ccres[i] for i in idx]

# Open fastas
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}

valid = set("ACGT")
seqs = []
type_counts = {}
for chrom, mid, cls in candidates:
    if len(seqs) >= N:
        break
    start = mid - HALF
    end = start + L
    if start < 0 or end > len(fas[chrom][chrom]):
        continue
    s = fas[chrom][chrom][start:end]
    if len(s) != L or not set(s).issubset(valid):
        continue
    seqs.append(s)
    primary = cls.split(",")[0]
    type_counts[primary] = type_counts.get(primary, 0) + 1

assert len(seqs) == N, f"only got {len(seqs)}"
print("cCRE type distribution:", type_counts)
rng.shuffle(seqs)
with OUT.open("w") as f:
    for s in seqs:
        f.write(s)
        f.write("\n")
print(f"Wrote {N} sequences (cCRE-centered 200bp windows).")
