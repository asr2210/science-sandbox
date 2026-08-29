"""Experiment 009: 70% multi-chrom-5 genomic + 30% ENCODE cCREs.

Tests whether mixing two NATURAL sources (broad genomic + regulatory)
can keep most of the grammar performance while recovering eval_08.

Multi-chrom-5: 35,000 random 200bp windows from chr8/19/21/22/X
(2k each base x 7 for total 35k... actually 7k each to make 35k total).
cCREs: 15,000 cCREs sampled from same chromosomes, centered 200bp.
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
N_CCRE = N - N_GENOMIC
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)

fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")

# Genomic: even per-chromosome split
per_chrom = N_GENOMIC // len(CHROMS)
extras = N_GENOMIC - per_chrom * len(CHROMS)
genomic = []
for i, c in enumerate(CHROMS):
    target = per_chrom + (1 if i < extras else 0)
    collected = []
    chrom_len = len(fas[c][c])
    while len(collected) < target:
        batch = rng.integers(0, chrom_len - L, size=4 * (target - len(collected)))
        for start in batch:
            if len(collected) >= target:
                break
            s = fas[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    genomic.extend(collected)

# cCREs from same chromosomes
chrom_set = set(CHROMS)
ccres = []
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        chrom = parts[0]
        if chrom not in chrom_set:
            continue
        start, end = int(parts[1]), int(parts[2])
        mid = (start + end) // 2
        ccres.append((chrom, mid))

print(f"Total cCREs in {CHROMS}: {len(ccres)}")
idx = rng.choice(len(ccres), size=min(len(ccres), 4 * N_CCRE), replace=False)
ccre_seqs = []
for i in idx:
    if len(ccre_seqs) >= N_CCRE:
        break
    chrom, mid = ccres[i]
    start = mid - HALF
    end = start + L
    if start < 0 or end > len(fas[chrom][chrom]):
        continue
    s = fas[chrom][chrom][start:end]
    if len(s) == L and set(s).issubset(valid):
        ccre_seqs.append(s)
assert len(ccre_seqs) == N_CCRE, f"only got {len(ccre_seqs)}"

all_seqs = genomic + ccre_seqs
assert len(all_seqs) == N
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")

# Diagnostic
import numpy as _np
gcs = _np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"GC stats: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k multi-chrom-5 genomic + 15k cCREs.")
