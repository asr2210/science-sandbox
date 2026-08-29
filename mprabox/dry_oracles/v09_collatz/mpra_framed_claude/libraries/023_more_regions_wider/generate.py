"""023_more_regions_wider.

10,000 cCREs × 5 tiles per cCRE = 50K, with each tile offset
uniform in [-400, +400] (wider sampling from 020).

Tests whether saturation point shifts UP under wider sampling
(more regions help) or holds at 5K (parity with 020).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_REGIONS = 10_000
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 400
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
assert n_written == 50_000
