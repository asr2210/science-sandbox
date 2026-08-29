"""024_paired_random_genomic.

5K cCREs x 5 narrow tiles (positives, +/-100bp of cCRE midpoint)
  + 5K random non-cCRE genomic windows x 5 tiles per region
    (paired negatives, >2kb from any cCRE midpoint)
= 50K.

Tests whether the wider-tile lift (020/021/022) comes from
implicit positive/negative pairing across the offset range. If
explicit pairing matches or beats wider tiling, pairing is the
true lever and we can stack it with other levers. If it
underperforms, wider tiling is doing something different
(positional invariance or context modulation per se).

Negative regions are sampled from the genome at sites far from
any cCRE midpoint (>2kb away). 5 narrow tiles per negative
region mirror the positive sampling exactly.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
from bisect import bisect_left

N_POS = 5_000
N_NEG = 5_000
TILES_PER = 5
LEN = 200
HALF = LEN // 2
POS_OFFSET = 100
NEG_OFFSET = 100  # match positive tile sampling width
EXCLUDE_RADIUS = 2_000  # negative regions must be >2kb from any cCRE midpoint
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

ccre_mids_by_chrom = {}
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        mid = (int(start) + int(end)) // 2
        ccre_mids_by_chrom.setdefault(chrom, []).append(mid)

ccre_pairs = []
for chrom, mids in ccre_mids_by_chrom.items():
    mids.sort()
    for m in mids:
        ccre_pairs.append((chrom, m))
print(f"cCREs total: {len(ccre_pairs)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)

# --- Positive tiles: 5K cCREs x 5 narrow tiles (+/-100bp) ---
pos_order = rng.permutation(len(ccre_pairs))
positives = []
n_pos_used = 0
for idx in pos_order:
    if n_pos_used >= N_POS:
        break
    chrom, mid = ccre_pairs[idx]
    offsets = rng.integers(-POS_OFFSET, POS_OFFSET + 1, size=TILES_PER)
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
    positives.extend(tile_seqs)
    n_pos_used += 1
print(f"Positive tiles: {len(positives)} from {n_pos_used} cCREs")

# --- Negative regions: 5K random midpoints, >2kb from any cCRE midpoint ---
chroms_list = [c for c in KEEP_CHROMS if c in chrom_lens and c in ccre_mids_by_chrom]
chrom_weights = np.array([chrom_lens[c] for c in chroms_list], dtype=float)
chrom_weights /= chrom_weights.sum()

negatives = []
n_neg_used = 0
attempts = 0
while n_neg_used < N_NEG and attempts < 1_000_000:
    attempts += 1
    chrom = chroms_list[rng.choice(len(chroms_list), p=chrom_weights)]
    L = chrom_lens[chrom]
    mid = int(rng.integers(LEN, L - LEN))
    # check distance to nearest cCRE midpoint on this chrom
    arr = ccre_mids_by_chrom[chrom]
    pos = bisect_left(arr, mid)
    dist = L
    if pos < len(arr):
        dist = min(dist, abs(arr[pos] - mid))
    if pos > 0:
        dist = min(dist, abs(arr[pos - 1] - mid))
    if dist <= EXCLUDE_RADIUS:
        continue
    # 5 narrow tiles at this neg region
    offsets = rng.integers(-NEG_OFFSET, NEG_OFFSET + 1, size=TILES_PER)
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
    negatives.extend(tile_seqs)
    n_neg_used += 1

print(f"Negative tiles: {len(negatives)} from {n_neg_used} non-cCRE regions ({attempts} attempts)")

combined = positives + negatives
rng.shuffle(combined)
assert len(combined) == 50_000, f"got {len(combined)}"

out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in combined:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(combined)} to {out_path.name}")
