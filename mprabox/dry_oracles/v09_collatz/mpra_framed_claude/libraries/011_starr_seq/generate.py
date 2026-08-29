"""011_starr_seq.

50K = 10K STARR-seq active peaks (5K K562 + 5K HepG2 from Gerstein lab
whole-genome STARRPeaker calls) x 5 random-offset 200bp tiles.

STARR-seq directly measures enhancer activity in a reporter context.
These peaks are the closest functional analogue to MPRA. If the model
is bottlenecked by "how MPRA-like are the training sequences", STARR
peaks should be the biggest possible single-source lift.

No SKNSH STARR-seq is publicly available; library is K562/HepG2 only.
Per-cell-type budget chosen by signal-rank within each STARR file.

K562 file: ENCFF045TVA, HepG2 file: ENCFF047LDJ (both GRCh38,
output_type "peaks", STARRPeaker element enrichments).
Columns: chrom start end name score strand fold_enrichment ...
score is in column 4 (peak strength, integer).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

PER_TYPE = 5000
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
GENOME = DATA / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_starr(path):
    """Returns list of (chrom, midpoint, score). Score = col[4]."""
    peaks = []
    with open(path) as f:
        for ln in f:
            parts = ln.rstrip().split("\t")
            chrom = parts[0]
            if chrom not in KEEP_CHROMS:
                continue
            try:
                start = int(parts[1])
                end = int(parts[2])
                score = float(parts[4])
            except (ValueError, IndexError):
                continue
            mid = (start + end) // 2
            peaks.append((chrom, mid, score))
    return peaks


k562 = load_starr(DATA / "k562_starr.bed")
hepg2 = load_starr(DATA / "hepg2_starr.bed")
print(f"K562 STARR peaks {len(k562)}  HepG2 STARR peaks {len(hepg2)}")

# Sort by score descending, take top PER_TYPE from each
k562.sort(key=lambda x: -x[2])
hepg2.sort(key=lambda x: -x[2])

selected = []
for chrom, mid, _ in k562[:PER_TYPE]:
    selected.append((chrom, mid))
for chrom, mid, _ in hepg2[:PER_TYPE]:
    selected.append((chrom, mid))
print(f"Selected {len(selected)} top STARR peaks")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
rng.shuffle(selected)

out_path = Path(__file__).parent / "sequences_0.txt"
n_written = 0
n_regions_used = 0
with open(out_path, "w") as f:
    for chrom, mid in selected:
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
        if n_regions_used >= 10000:
            break
print(f"Wrote {n_written} from {n_regions_used} regions")
assert n_written == 50_000, f"Got {n_written}, expected 50000"
