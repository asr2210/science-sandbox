"""010_diff_activity.

50,000 = 2,500 regions × 5 tiles per region, balanced across 4 cell-
type-overlap categories:
  - K562-specific:   in K562 DHS, NOT in HepG2 DHS, NOT in SKNSH DHS
  - HepG2-specific:  in HepG2 DHS, NOT K562, NOT SKNSH
  - SKNSH-specific:  in SKNSH DHS, NOT K562, NOT HepG2
  - Shared:          in all three DHS sets

This deliberately maximizes activity VARIANCE across cell types.
Tests "differential activity is the training signal" hypothesis.

Overlap test: peaks overlap if their intervals share any base.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
from collections import defaultdict

PER_CLASS = 2500
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
GENOME = DATA / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

def load_peaks(path, has_header):
    """Load (chrom, start, end). Returns dict chrom -> sorted list of (start, end)."""
    by_chrom = defaultdict(list)
    with open(path) as f:
        for ln in f:
            if has_header and ln.startswith("#"):
                continue
            parts = ln.rstrip().split("\t")
            chrom = parts[0]
            if chrom not in KEEP_CHROMS:
                continue
            try:
                start = int(parts[1])
                end = int(parts[2])
            except (ValueError, IndexError):
                continue
            by_chrom[chrom].append((start, end))
    for c in by_chrom:
        by_chrom[c].sort()
    return by_chrom

print("Loading peaks...")
k562 = load_peaks(DATA / "k562_dnase.bed", has_header=True)
hepg2 = load_peaks(DATA / "hepg2_dnase.bed", has_header=True)
sknsh = load_peaks(DATA / "sknsh_dnase.bed", has_header=False)

def overlaps(chrom_dict, chrom, mid):
    """Check if [mid-HALF, mid+HALF) overlaps any peak on chrom."""
    if chrom not in chrom_dict:
        return False
    arr = chrom_dict[chrom]
    qs, qe = mid - HALF, mid + HALF
    # binary search for first peak with end > qs
    lo, hi = 0, len(arr)
    while lo < hi:
        m = (lo + hi) // 2
        if arr[m][1] <= qs:
            lo = m + 1
        else:
            hi = m
    # check arr[lo] and following until start >= qe
    while lo < len(arr) and arr[lo][0] < qe:
        if arr[lo][1] > qs and arr[lo][0] < qe:
            return True
        lo += 1
    return False

# Classify each peak by overlap pattern. Iterate over all peaks (union)
# to find candidates of each category. Use HepG2 as the "iterate" set
# because we need a lot of peaks and it's mid-size (120K).
all_peaks = []  # (chrom, mid, k_in, h_in, s_in)
for src_dict, src_name in [(k562, "k562"), (hepg2, "hepg2"), (sknsh, "sknsh")]:
    for chrom, peaks in src_dict.items():
        for s, e in peaks:
            mid = (s + e) // 2
            all_peaks.append((chrom, mid))

# Dedup by (chrom, mid // 200) so we don't double-count
seen = set()
dedup = []
for chrom, mid in all_peaks:
    key = (chrom, mid // 200)
    if key not in seen:
        seen.add(key)
        dedup.append((chrom, mid))
print(f"Unique peak midpoints: {len(dedup)}")

print("Classifying...")
by_class = {"k562_only": [], "hepg2_only": [], "sknsh_only": [], "shared3": []}
for chrom, mid in dedup:
    k_in = overlaps(k562, chrom, mid)
    h_in = overlaps(hepg2, chrom, mid)
    s_in = overlaps(sknsh, chrom, mid)
    if k_in and not h_in and not s_in:
        by_class["k562_only"].append((chrom, mid))
    elif h_in and not k_in and not s_in:
        by_class["hepg2_only"].append((chrom, mid))
    elif s_in and not k_in and not h_in:
        by_class["sknsh_only"].append((chrom, mid))
    elif k_in and h_in and s_in:
        by_class["shared3"].append((chrom, mid))
for cls, lst in by_class.items():
    print(f"  {cls}: {len(lst)}")

rng = np.random.default_rng(SEED)

# Sample 2500 regions from each class
selected = []
for cls, lst in by_class.items():
    rng.shuffle(lst)
    chosen = lst[:PER_CLASS]
    if len(chosen) < PER_CLASS:
        # sample with replacement to fill
        extra = rng.choice(len(lst), size=PER_CLASS - len(chosen), replace=True)
        chosen = chosen + [lst[i] for i in extra]
    print(f"  using {len(chosen)} from {cls}")
    selected.extend([(c, m, cls) for c, m in chosen])

rng.shuffle(selected)

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

out_path = Path(__file__).parent / "sequences_0.txt"
n_written = 0
n_regions_used = 0
with open(out_path, "w") as f:
    for chrom, mid, cls in selected:
        offsets = rng.integers(-OFFSET_MAX, OFFSET_MAX + 1, size=TILES_PER)
        tile_seqs = []
        for off in offsets:
            center = mid + int(off)
            s = center - HALF
            e = s + LEN
            if s < 0 or e > chrom_lens[chrom]:
                continue
            seq = fasta[chrom][s:e]
            if "N" in seq or len(seq) != LEN:
                continue
            tile_seqs.append(seq)
        if len(tile_seqs) < TILES_PER:
            continue
        for seq in tile_seqs:
            f.write(seq)
            f.write("\n")
            n_written += 1
        n_regions_used += 1
print(f"Wrote {n_written} from {n_regions_used} regions")
assert n_written == 50_000, f"Got {n_written}, expected 50000"
