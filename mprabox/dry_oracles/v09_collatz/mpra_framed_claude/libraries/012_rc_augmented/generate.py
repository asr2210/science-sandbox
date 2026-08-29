"""012_rc_augmented.

50,000 = 5,000 cCREs × 5 random-offset 200bp tiles = 25,000 forward
tiles + their 25,000 reverse complements.

Tests whether explicit strand-invariance augmentation lifts the
plateau. TF binding is strand-invariant by physics (motifs work on
either strand); a model trained with RC pairs learns this prior
from data without relying on architectural symmetry.

Net training pairs = 50K (same budget); effective sequence
diversity per K of genomic region budget = 2x because each region's
content is presented as both strands.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_REGIONS = 5_000
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"

KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

COMP = str.maketrans("ACGT", "TGCA")

def rc(seq):
    return seq.translate(COMP)[::-1]

rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, (int(start) + int(end)) // 2))
print(f"cCRE midpoints on main chroms: {len(rows)}")

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

print(f"Forward tiles: {len(forward)} from {n_regions_used} regions")

# Build interleaved [fwd_1, rc_1, fwd_2, rc_2, ...] then shuffle
combined = []
for s in forward:
    combined.append(s)
    combined.append(rc(s))
rng.shuffle(combined)

assert len(combined) == 50_000, f"Got {len(combined)}"

out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in combined:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(combined)} sequences (25K fwd + 25K RC)")
