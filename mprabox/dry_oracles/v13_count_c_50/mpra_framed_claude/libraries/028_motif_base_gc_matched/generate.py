"""Experiment 028: motif-enriched base with mc5 GC histogram matching.

Same idea as 027 (base windows must overlap a cCRE = motif-enriched),
but the base is GC-subsampled to MATCH the GC distribution of plain mc5
random. This decouples motif enrichment from composition shift.

If 028 > 013: motif-only enrichment helps; new lever found.
If 028 ≈ 013: motif density alone doesn't break the ceiling.
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
N_GC_BINS = 25
GC_RANGE = (0.20, 0.80)
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")
chrom_set = set(CHROMS)


def gc_to_bin(gc):
    b = int((gc - GC_RANGE[0]) / (GC_RANGE[1] - GC_RANGE[0]) * N_GC_BINS)
    return min(max(b, 0), N_GC_BINS - 1)


# Build cCRE intervals + type lists
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

ccre_starts = {c: sorted(x[0] for x in ccre_intervals[c]) for c in CHROMS}
ccre_ends = {}
for c in CHROMS:
    ccre_intervals[c].sort()
    ccre_starts[c] = [x[0] for x in ccre_intervals[c]]
    ccre_ends[c] = [x[1] for x in ccre_intervals[c]]


def overlaps_ccre(c, start, end):
    starts = ccre_starts[c]
    ends = ccre_ends[c]
    i = bisect_left(starts, end)
    if i > 0 and ends[i - 1] > start:
        return True
    if i < len(starts) and starts[i] < end and ends[i] > start:
        return True
    return False


# Step 1: build the TARGET GC histogram from plain mc5 random windows
per_chrom_target = N_GENOMIC // len(CHROMS)
target_hist = np.zeros(N_GC_BINS, dtype=int)
mc5_baseline_collected = 0
chrom_lens = {c: len(fas[c][c]) for c in CHROMS}
for c in CHROMS:
    collected = 0
    while collected < per_chrom_target:
        batch = rng.integers(0, chrom_lens[c] - L,
                             size=4 * (per_chrom_target - collected))
        for start in batch:
            if collected >= per_chrom_target:
                break
            s = fas[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                gc = (s.count("G") + s.count("C")) / L
                if GC_RANGE[0] <= gc < GC_RANGE[1]:
                    target_hist[gc_to_bin(gc)] += 1
                collected += 1
print(f"Target hist sum: {target_hist.sum()}, dominant bins: "
      f"{sorted(zip(target_hist, range(N_GC_BINS)), reverse=True)[:5]}")

# Scale to N_GENOMIC
scaled = (target_hist.astype(float) / target_hist.sum() * N_GENOMIC).astype(int)
deficit = N_GENOMIC - scaled.sum()
if deficit > 0:
    big = np.argsort(-target_hist)[:deficit]
    for b in big:
        scaled[b] += 1
assert scaled.sum() == N_GENOMIC

# Step 2: sample cCRE-overlap mc5 windows, bucket by GC, fill to target
chrom_weights = np.array([chrom_lens[c] for c in CHROMS], dtype=float)
chrom_weights /= chrom_weights.sum()
bins = [[] for _ in range(N_GC_BINS)]
needed = scaled.copy()
attempts = 0
batch_size = 100_000
while needed.sum() > 0 and attempts < 60:
    chrom_choices = rng.choice(len(CHROMS), size=batch_size, p=chrom_weights)
    for ci in chrom_choices:
        c = CHROMS[ci]
        start = int(rng.integers(0, chrom_lens[c] - L))
        end = start + L
        if not overlaps_ccre(c, start, end):
            continue
        s = fas[c][c][start:end]
        if len(s) != L or not set(s).issubset(valid):
            continue
        gc = (s.count("G") + s.count("C")) / L
        if not (GC_RANGE[0] <= gc < GC_RANGE[1]):
            continue
        b = gc_to_bin(gc)
        if needed[b] > 0:
            bins[b].append(s)
            needed[b] -= 1
            if needed.sum() == 0:
                break
    attempts += 1

print(f"Filled in {attempts} batches; remaining: {needed.sum()}")
genomic = [s for bin_ in bins for s in bin_]
if len(genomic) < N_GENOMIC:
    short = N_GENOMIC - len(genomic)
    print(f"Top-up {short} from densest bins (rare-bin shortfall)")
    extra = list(rng.choice(genomic, size=short, replace=True))
    genomic.extend(extra)
assert len(genomic) == N_GENOMIC

base_gcs = np.array([(s.count("G") + s.count("C")) / L for s in genomic])
print(f"Base GC: mean={base_gcs.mean():.3f}, std={base_gcs.std():.3f}")

# Step 3: type-balanced cCRE supplement (013 recipe)
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
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k cCRE-overlap mc5 (GC-matched to mc5) + 15k cCRE.")
