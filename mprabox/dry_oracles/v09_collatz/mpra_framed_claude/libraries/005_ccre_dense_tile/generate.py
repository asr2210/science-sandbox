"""005_ccre_dense_tile.

50,000 = 10,000 cCREs × 5 random-offset 200bp windows per cCRE.
Tests whether dense per-region position diversity helps the model
learn motif/position invariance. Inspired by PARM (Movva et al.)
which used dense random partially-overlapping fragments per region
and achieved R=0.92 on K562, 0.89 on HepG2 (much higher than
single-tile designs).

Each tile is a 200bp window with offset drawn uniformly in
[-100, +100] from the cCRE midpoint, so all tiles overlap the cCRE
core but cover a different ~300bp span around it.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_REGIONS = 10_000
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
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
print(f"cCRE midpoints on main chroms: {len(rows)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
region_order = rng.permutation(len(rows))

out_path = Path(__file__).parent / "sequences_0.txt"
n_written = 0
n_regions_used = 0
seqs_per_region = []
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
            # skip regions where we can't make all 5 clean tiles
            continue
        for seq in tile_seqs:
            f.write(seq)
            f.write("\n")
            n_written += 1
        n_regions_used += 1
print(f"Wrote {n_written} from {n_regions_used} regions.")
assert n_written == N_REGIONS * TILES_PER == 50_000
