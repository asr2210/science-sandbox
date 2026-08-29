"""030_hard_adjacent_negatives.

HARD (adjacent) negatives instead of FAR (>2kb) negatives.
5K cCREs x 8 WIDER tiles = 40K positives
+ 2.5K "adjacent" non-cCRE regions x 4 narrow tiles = 10K
= 50K (4:1 ratio).

Adjacent = midpoint 600-2000bp from nearest cCRE midpoint
(close enough to share intergenic/promoter neighborhood,
far enough that the 200bp window itself doesn't overlap any
cCRE).

Tests T20's discrimination axis: does HARDER negative
discrimination lift K562 beyond 028's 0.148? If yes, the lever
is "finer boundary" not just "anything non-cCRE." If no, easy
negatives are sufficient.

Compare:
  028 wider+far neg:  0.3229  K562=.148 HepG2=.203 SKNSH=.618
  030 wider+adj neg:  ?
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
from bisect import bisect_left

N_POS = 5_000
POS_TILES = 8
POS_OFFSET = 400
N_NEG = 2_500
NEG_TILES = 4
NEG_OFFSET = 100
LEN = 200
HALF = LEN // 2
# Adjacent zone: at least far enough that 200bp window doesn't
# touch a cCRE (cCREs are typically ~150-350bp); use 600bp lower
# bound and 2000bp upper bound (the previous "far" cutoff).
ADJ_MIN_DIST = 600
ADJ_MAX_DIST = 2_000
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

# Wider positives
pos_order = rng.permutation(len(ccre_pairs))
positives = []
n_pos_used = 0
for idx in pos_order:
    if n_pos_used >= N_POS:
        break
    chrom, mid = ccre_pairs[idx]
    offsets = rng.integers(-POS_OFFSET, POS_OFFSET + 1, size=POS_TILES)
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
    if len(tile_seqs) < POS_TILES:
        continue
    positives.extend(tile_seqs)
    n_pos_used += 1
print(f"Positives (wider): {len(positives)} from {n_pos_used} cCREs")

# ADJACENT negatives: sample by walking outward from cCREs.
# For each cCRE, generate candidate centers at +/- d for
# d in [ADJ_MIN_DIST, ADJ_MAX_DIST], then check that no other
# cCRE is within ADJ_MIN_DIST of the candidate.
chroms_list = list(ccre_mids_by_chrom.keys())
negatives = []
n_neg_used = 0
attempts = 0

# Random sampling: pick a random cCRE midpoint, then offset by
# d ~ uniform(ADJ_MIN_DIST, ADJ_MAX_DIST), random sign, and
# check the result isn't within ADJ_MIN_DIST of any cCRE.
while n_neg_used < N_NEG and attempts < 2_000_000:
    attempts += 1
    src_idx = int(rng.integers(0, len(ccre_pairs)))
    chrom, src_mid = ccre_pairs[src_idx]
    L = chrom_lens[chrom]
    d = int(rng.integers(ADJ_MIN_DIST, ADJ_MAX_DIST + 1))
    sign = 1 if rng.integers(0, 2) == 0 else -1
    mid = src_mid + sign * d
    if mid < LEN or mid > L - LEN:
        continue
    arr = ccre_mids_by_chrom[chrom]
    pos = bisect_left(arr, mid)
    dist = L
    if pos < len(arr):
        dist = min(dist, abs(arr[pos] - mid))
    if pos > 0:
        dist = min(dist, abs(arr[pos - 1] - mid))
    if dist < ADJ_MIN_DIST or dist > ADJ_MAX_DIST:
        continue
    offsets = rng.integers(-NEG_OFFSET, NEG_OFFSET + 1, size=NEG_TILES)
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
    if len(tile_seqs) < NEG_TILES:
        continue
    negatives.extend(tile_seqs)
    n_neg_used += 1

print(f"Adjacent negatives: {len(negatives)} from {n_neg_used} regions ({attempts} attempts)")

combined = positives + negatives
rng.shuffle(combined)
assert len(combined) == 50_000, f"got {len(combined)}"

out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in combined:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(combined)} to {out_path.name}")
