"""027_pos_neg_ratio_4to1.

Pos:neg ratio sweep at 4:1.
5K cCREs x 8 narrow tiles (positives, +/-100bp) = 40K
+ 2.5K non-cCRE genomic regions x 4 narrow tiles (negatives) = 10K
= 50K total.

Tests T18: if the K562 bump from 024 survives at lower neg
fraction AND SKNSH recovers, we hit a new high.

Compare to 024 (1:1, 25K/25K) which had K562=0.148, HepG2=0.201,
SKNSH=0.613.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
from bisect import bisect_left

N_POS = 5_000
POS_TILES = 8
N_NEG = 2_500
NEG_TILES = 4
LEN = 200
HALF = LEN // 2
OFFSET = 100
EXCLUDE_RADIUS = 2_000
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

# Positives
pos_order = rng.permutation(len(ccre_pairs))
positives = []
n_pos_used = 0
for idx in pos_order:
    if n_pos_used >= N_POS:
        break
    chrom, mid = ccre_pairs[idx]
    offsets = rng.integers(-OFFSET, OFFSET + 1, size=POS_TILES)
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
print(f"Positives: {len(positives)} from {n_pos_used} cCREs")

# Negatives
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
    arr = ccre_mids_by_chrom[chrom]
    pos = bisect_left(arr, mid)
    dist = L
    if pos < len(arr):
        dist = min(dist, abs(arr[pos] - mid))
    if pos > 0:
        dist = min(dist, abs(arr[pos - 1] - mid))
    if dist <= EXCLUDE_RADIUS:
        continue
    offsets = rng.integers(-OFFSET, OFFSET + 1, size=NEG_TILES)
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

print(f"Negatives: {len(negatives)} from {n_neg_used} non-cCRE regions ({attempts} attempts)")

combined = positives + negatives
rng.shuffle(combined)
assert len(combined) == 50_000, f"got {len(combined)}"

out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in combined:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(combined)} to {out_path.name}")
