"""009_top_signal_dhs.

50,000 = 10,000 TOP-SIGNAL HepG2 DNase peaks × 5 random-offset 200bp
tiles. Tests peak quality hypothesis: higher-accessibility peaks =
more confident regulatory elements = cleaner training pairs.

Combines top 10K HepG2 + top 10K K562 + top 10K SKNSH peaks (3.33k
per cell type × 5 tiles) for balanced quality across cell types.
Actually doing top 3334 of each so 3334+3333+3333 = 10000 regions.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

PER_TYPE = [3334, 3333, 3333]  # K562, HepG2, SKNSH
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
GENOME = DATA / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

def load_peaks(path, signal_col, has_header):
    """Load (chrom, midpoint, signal) from a peak file."""
    peaks = []
    with open(path) as f:
        for ln in f:
            if has_header and ln.startswith("#"):
                continue
            parts = ln.rstrip().split("\t")
            chrom = parts[0]
            if chrom not in KEEP_CHROMS:
                continue
            try:
                start = int(parts[1])
                end = int(parts[2])
                signal = float(parts[signal_col])
            except (ValueError, IndexError):
                continue
            mid = (start + end) // 2
            peaks.append((chrom, mid, signal))
    return peaks

# Format A (k562, hepg2): #chr start end id max_density summit_density summit smoothed_peak_height
#   has_header=True, signal_col=4 (max_density)
# Format B (sknsh): narrowPeak — chr start end name score strand signalValue pValue qValue peak
#   has_header=False, signal_col=6
k562 = load_peaks(DATA / "k562_dnase.bed", signal_col=4, has_header=True)
hepg2 = load_peaks(DATA / "hepg2_dnase.bed", signal_col=4, has_header=True)
# Check SKNSH format
sknsh_path = DATA / "sknsh_dnase.bed"
sknsh = load_peaks(sknsh_path, signal_col=6, has_header=False)
print(f"K562 {len(k562)}  HepG2 {len(hepg2)}  SKNSH {len(sknsh)}")

# Sort each by signal descending and take top
k562.sort(key=lambda x: -x[2])
hepg2.sort(key=lambda x: -x[2])
sknsh.sort(key=lambda x: -x[2])

selected = []
for peaks_list, n in zip((k562, hepg2, sknsh), PER_TYPE):
    for chrom, mid, sig in peaks_list[:n]:
        selected.append((chrom, mid))
print(f"Selected {len(selected)} top peaks across 3 cell types")

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
assert n_written == 50_000
