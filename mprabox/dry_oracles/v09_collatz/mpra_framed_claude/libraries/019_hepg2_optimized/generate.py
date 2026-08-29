"""019_hepg2_optimized.

50K = 5,000 HepG2-SPECIFIC DHS peaks × 10 random-offset 200bp tiles.
HepG2-specific = HepG2 DHS peak whose 200bp core does NOT overlap
any K562 DHS or SKNSH DHS peak.

Tests whether maximally pushing HepG2-specific exposure can lift
the HepG2 head past its observed ~0.19 ceiling. mean_r is bottle-
necked by HepG2 (K562 pinned ~0.146, SKNSH pinned ~0.625 across
all libraries). Lifting HepG2 is the only path to break the
0.318 plateau.

Selection rule:
  - HepG2 DHS peak overlaps neither K562 DHS nor SKNSH DHS within
    its 200bp window.
  - Among qualifying peaks, take top 5K by HepG2 signal
    (max_density column 4).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
from collections import defaultdict
from bisect import bisect_left

N_REGIONS = 5_000
TILES_PER = 10
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
GENOME = DATA / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_peaks_intervals(path, has_header):
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
                s = int(parts[1])
                e = int(parts[2])
            except (ValueError, IndexError):
                continue
            by_chrom[chrom].append((s, e))
    for c in by_chrom:
        by_chrom[c].sort()
    return by_chrom


def overlaps(chrom_dict, chrom, qs, qe):
    if chrom not in chrom_dict:
        return False
    arr = chrom_dict[chrom]
    lo = 0
    hi = len(arr)
    while lo < hi:
        m = (lo + hi) // 2
        if arr[m][1] <= qs:
            lo = m + 1
        else:
            hi = m
    while lo < len(arr) and arr[lo][0] < qe:
        if arr[lo][1] > qs and arr[lo][0] < qe:
            return True
        lo += 1
    return False


print("Loading DHS files...")
k562 = load_peaks_intervals(DATA / "k562_dnase.bed", has_header=True)
sknsh = load_peaks_intervals(DATA / "sknsh_dnase.bed", has_header=False)

# Load HepG2 with signal
hepg2 = []
with open(DATA / "hepg2_dnase.bed") as f:
    for ln in f:
        if ln.startswith("#"):
            continue
        parts = ln.rstrip().split("\t")
        chrom = parts[0]
        if chrom not in KEEP_CHROMS:
            continue
        try:
            s = int(parts[1])
            e = int(parts[2])
            sig = float(parts[4])  # max_density
        except (ValueError, IndexError):
            continue
        mid = (s + e) // 2
        hepg2.append((chrom, mid, sig))
print(f"K562 DHS peaks: {sum(len(v) for v in k562.values())}")
print(f"SKNSH DHS peaks: {sum(len(v) for v in sknsh.values())}")
print(f"HepG2 DHS peaks: {len(hepg2)}")

# Filter HepG2-specific (200bp window does not overlap K562 or SKNSH)
print("Filtering HepG2-specific...")
hepg2_specific = []
for chrom, mid, sig in hepg2:
    qs, qe = mid - HALF, mid + HALF
    if overlaps(k562, chrom, qs, qe):
        continue
    if overlaps(sknsh, chrom, qs, qe):
        continue
    hepg2_specific.append((chrom, mid, sig))
print(f"HepG2-specific: {len(hepg2_specific)}")

# Sort by signal desc, take top
hepg2_specific.sort(key=lambda x: -x[2])
selected = [(c, m) for c, m, _ in hepg2_specific[:N_REGIONS * 2]]
print(f"Selected (with margin): {len(selected)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)

n_written = 0
n_regions_used = 0
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for chrom, mid in selected:
        if n_regions_used >= N_REGIONS:
            break
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
assert n_written == 50_000
