"""Experiment 022: GC-histogram-matched genomic supplement.

35k mc5 + 15k mc5 windows whose GC histogram is matched to the
cCRE supplement's GC histogram (type-balanced, chr5 set).

Tests whether the cCRE supplement's value is fully captured by its GC
distribution. If 022 ≈ 013, GC distribution explains everything.
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
N_BINS = 30
GC_RANGE = (0.20, 0.80)
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")
chrom_set = set(CHROMS)

# 1. Build target GC histogram from type-balanced cCREs
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

# Collect GC values from type-balanced cCRE pool
per_type_target = N_SUPP // 5
ccre_gcs = []
for t, pool in ccres_by_type.items():
    idx = rng.choice(len(pool), size=min(len(pool), 4 * per_type_target), replace=False)
    count = 0
    for i in idx:
        if count >= per_type_target:
            break
        chrom, mid = pool[i]
        start, end = mid - HALF, mid - HALF + L
        if start < 0 or end > len(fas[chrom][chrom]):
            continue
        s = fas[chrom][chrom][start:end]
        if len(s) == L and set(s).issubset(valid):
            ccre_gcs.append((s.count("G") + s.count("C")) / L)
            count += 1

ccre_gcs = np.array(ccre_gcs)
target_hist, bin_edges = np.histogram(ccre_gcs, bins=N_BINS, range=GC_RANGE)
print(f"cCRE GC mean={ccre_gcs.mean():.3f}, std={ccre_gcs.std():.3f}")
print(f"Target histogram: total {target_hist.sum()} across {N_BINS} bins")

# Scale target to sum to N_SUPP
target_counts = (target_hist / target_hist.sum() * N_SUPP).astype(int)
deficit = N_SUPP - target_counts.sum()
if deficit > 0:
    biggest = np.argsort(-target_hist)[:deficit]
    for b in biggest:
        target_counts[b] += 1
assert target_counts.sum() == N_SUPP

# 2. mc5 baseline (35k)
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

# 3. Sample mc5 windows to fill the target GC histogram
chrom_lens = {c: len(fas[c][c]) for c in CHROMS}
chrom_weights = np.array([chrom_lens[c] for c in CHROMS], dtype=float)
chrom_weights /= chrom_weights.sum()
bin_seqs = [[] for _ in range(N_BINS)]

needed = target_counts.copy()
attempts = 0
while needed.sum() > 0:
    if attempts > 200:
        # Some bins may be unreachable; report and break
        print(f"giving up, remaining needs: {needed}")
        break
    batch_size = max(int(2 * needed.sum()), 10_000)
    chrom_choices = rng.choice(len(CHROMS), size=batch_size, p=chrom_weights)
    for ci in chrom_choices:
        c = CHROMS[ci]
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = fas[c][c][start:start + L]
        if len(s) != L or not set(s).issubset(valid):
            continue
        gc = (s.count("G") + s.count("C")) / L
        if gc < GC_RANGE[0] or gc >= GC_RANGE[1]:
            continue
        # find bin
        b = min(int((gc - GC_RANGE[0]) / (GC_RANGE[1] - GC_RANGE[0]) * N_BINS),
                N_BINS - 1)
        if needed[b] > 0:
            bin_seqs[b].append(s)
            needed[b] -= 1
            if needed.sum() == 0:
                break
    attempts += 1

supp = [s for bin_ in bin_seqs for s in bin_]
print(f"Got {len(supp)} supplement sequences in {attempts} batches")

# If we couldn't fill some bins, top up from nearest filled bin
if len(supp) < N_SUPP:
    short = N_SUPP - len(supp)
    print(f"Topping up {short} from densest bins (rare-bin shortfall)")
    flat = [s for bin_ in bin_seqs for s in bin_]
    extra = list(rng.choice(flat, size=short, replace=True))
    supp.extend(extra)
assert len(supp) == N_SUPP

supp_gcs = np.array([(s.count("G") + s.count("C")) / L for s in supp])
print(f"Supp GC: mean={supp_gcs.mean():.3f}, std={supp_gcs.std():.3f}")

all_seqs = genomic + supp
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k mc5 + 15k mc5 GC-histogram-matched to cCREs.")
