"""007_promoter_dense.

50,000 = 10,000 PROMOTER-class cCREs × 5 random-offset 200bp tiles
each. Promoter-like elements (PLS, PLS,CTCF-bound, DNase-H3K4me3,
DNase-H3K4me3,CTCF-bound) are the most cell-type-invariant
regulatory class — promoter activity correlates R=0.78-0.95 across
cell types in the literature. Tests whether the most universally
regulatory element class lifts performance above the cCRE-mixed
plateau.
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

DATA = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA / "GRCh38-cCREs.bed"
GENOME = DATA / "hg38.fa"

KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
PROMOTER_KEYS = ("PLS", "DNase-H3K4me3")

rows = []
with open(BED) as f:
    for ln in f:
        parts = ln.split("\t")
        chrom, start, end = parts[0], int(parts[1]), int(parts[2])
        if chrom not in KEEP_CHROMS:
            continue
        cls = parts[5] if len(parts) > 5 else ""
        if not any(k in cls for k in PROMOTER_KEYS):
            continue
        rows.append((chrom, (start + end) // 2))
print(f"Promoter-class cCREs on main chroms: {len(rows)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
order = rng.permutation(len(rows))

out_path = Path(__file__).parent / "sequences_0.txt"
n_written = 0
n_regions_used = 0
with open(out_path, "w") as f:
    for idx in order:
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
