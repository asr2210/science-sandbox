"""Experiment 027: motif-enriched base via cCRE overlap.

35k mc5 random 200bp windows that OVERLAP at least one cCRE annotation +
15k type-balanced cCRE supplement (013 recipe).

The base retains randomness (200bp windows drawn at random positions)
but requires overlap with cCRE → higher motif density per window than
purely random mc5.

Tests: can a motif-enriched base push past the 0.5765 ceiling?
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta
from bisect import bisect_left

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 35_000
N_SUPP = N - N_GENOMIC
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")
chrom_set = set(CHROMS)

# Build per-chrom sorted cCRE intervals
ccre_intervals = {c: [] for c in CHROMS}
ccres_by_type = {"PLS": [], "pELS": [], "dELS": [],
                 "CTCF-only": [], "DNase-H3K4me3": []}
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] not in chrom_set:
            continue
        s, e = int(parts[1]), int(parts[2])
        ccre_intervals[parts[0]].append((s, e))
        primary = parts[5].split(",")[0]
        if primary in ccres_by_type:
            mid = (s + e) // 2
            ccres_by_type[primary].append((parts[0], mid))

# Sort + build starts array for bisect
ccre_starts = {}
ccre_ends = {}
for c in CHROMS:
    ccre_intervals[c].sort()
    ccre_starts[c] = [x[0] for x in ccre_intervals[c]]
    ccre_ends[c] = [x[1] for x in ccre_intervals[c]]
print(f"cCREs in chr5 set: {sum(len(v) for v in ccre_intervals.values())}")

def overlaps_ccre(c, start, end):
    """True if [start,end) overlaps any cCRE on chrom c."""
    starts = ccre_starts[c]
    ends = ccre_ends[c]
    # Find first cCRE with start < end (window's end)
    i = bisect_left(starts, end)
    # Check cCRE at position i-1 (might overlap if its end > start)
    if i > 0 and ends[i - 1] > start:
        return True
    # Check cCRE at position i (might start before end but not before i-1's end)
    if i < len(starts) and starts[i] < end and ends[i] > start:
        return True
    return False

# Sample mc5 windows that overlap a cCRE
per_chrom = N_GENOMIC // len(CHROMS)
genomic = []
for c in CHROMS:
    chrom_len = len(fas[c][c])
    collected = []
    attempts = 0
    while len(collected) < per_chrom:
        batch = rng.integers(0, chrom_len - L, size=8 * (per_chrom - len(collected)))
        for start in batch:
            if len(collected) >= per_chrom:
                break
            start = int(start)
            end = start + L
            if not overlaps_ccre(c, start, end):
                continue
            s = fas[c][c][start:end]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
        attempts += 1
        if attempts > 200:
            print(f"chrom {c} stuck at {len(collected)}/{per_chrom}")
            break
    print(f"chrom {c}: {len(collected)} overlap-base windows, {attempts} batches")
    genomic.extend(collected)

# Type-balanced cCREs (013 recipe)
per_type = N_SUPP // 5
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
assert len(ccre_seqs) == N_SUPP

all_seqs = genomic + ccre_seqs
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")

gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
base_gcs = np.array([(s.count("G") + s.count("C")) / L for s in genomic])
print(f"Base GC: {base_gcs.mean():.3f} (mc5 random ~0.42)")
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k cCRE-overlap mc5 + 15k type-balanced cCRE.")
