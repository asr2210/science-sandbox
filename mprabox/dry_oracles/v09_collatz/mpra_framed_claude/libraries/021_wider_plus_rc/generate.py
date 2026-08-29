"""021_wider_plus_rc.

50K = 5,000 cCREs × 5 wider-offset tiles + each tile's RC = 50K.
Stacks the two lever-positive interventions from prior experiments:
  - Wider tile offsets (±400bp) from 020: lifted eval_01 to 0.3216
  - RC augmentation from 012: lifted eval_01 to 0.3195

If they teach orthogonal universal priors (position-invariance +
context inference + strand invariance), the lift stacks.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_REGIONS = 5_000
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 400
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

COMP = str.maketrans("ACGT", "TGCA")
def rc(s):
    return s.translate(COMP)[::-1]

rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, (int(start) + int(end)) // 2))
print(f"cCREs: {len(rows)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
region_order = rng.permutation(len(rows))

forward = []
n_regions_used = 0
for idx in region_order:
    if n_regions_used >= N_REGIONS:
        break
    chrom, mid = rows[idx]
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
    forward.extend(tile_seqs)
    n_regions_used += 1

print(f"Forward tiles {len(forward)} from {n_regions_used} regions")
combined = []
for s in forward:
    combined.append(s)
    combined.append(rc(s))
rng.shuffle(combined)
assert len(combined) == 50_000

out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in combined:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(combined)}")
