"""020_wider_tiles.

5,000 cCREs × 10 tiles per cCRE = 50K, with each tile drawn from a
UNIFORM random offset in [-400, +400] from the cCRE midpoint
(instead of [-100, +100] as in 005/014).

The 200bp window can land anywhere within ~1kb of the cCRE,
exposing the model to flanking context that conventional core-
element tiling misses.

Generalization justification: regulatory activity depends on
flanking context (insulators, neighboring TFBSs, chromatin state).
Wider sampling trains context-aware grammar which is universal
across cell types.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_REGIONS = 5_000
TILES_PER = 10
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 400  # wider than usual 100
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

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

n_written = 0
n_regions_used = 0
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
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
        for seq in tile_seqs:
            f.write(seq)
            f.write("\n")
            n_written += 1
        n_regions_used += 1

print(f"Wrote {n_written} from {n_regions_used} regions")
assert n_written == N_REGIONS * TILES_PER == 50_000
