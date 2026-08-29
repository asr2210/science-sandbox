"""003_k562_dnase: 50,000 200bp windows centered on K562 DNase peaks.

Tests whether K562's stuck-at-r=0.14 (in 001 random and 002 cCRE
libraries) is due to K562-active elements being underrepresented in
those pools (cell-type-bias hypothesis), or to an intrinsic ceiling
on K562 predictability.

Source: ENCODE K562 DNase-seq narrowPeak (ENCFF599DEH, hotspot3,
~53k peaks). Sample 50k peaks (close to all), center 200bp window
on the peak summit (or midpoint if summit missing).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_SEQS = 50_000
LEN = 200
HALF = LEN // 2
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "k562_dnase.bed"
GENOME = DATA_DIR / "hg38.fa"

KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

# Load peaks. ENCFF599DEH header is:
# chr start end id max_density summit_density summit smoothed_peak_height
rows = []
with open(BED) as f:
    for ln in f:
        if ln.startswith("#") or not ln.strip():
            continue
        parts = ln.rstrip().split("\t")
        chrom = parts[0]
        if chrom not in KEEP_CHROMS:
            continue
        start = int(parts[1])
        end = int(parts[2])
        # summit is column 7 (index 6) in hotspot3 output
        try:
            summit = int(parts[6])
            if not (start <= summit <= end):
                summit = (start + end) // 2
        except (IndexError, ValueError):
            summit = (start + end) // 2
        rows.append((chrom, summit))
print(f"Loaded {len(rows)} K562 peaks on main chroms")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
order = rng.permutation(len(rows))

out_path = Path(__file__).parent / "sequences_0.txt"
n_written = 0
n_skipped = 0
with open(out_path, "w") as f:
    for idx in order:
        if n_written >= N_SEQS:
            break
        chrom, center = rows[idx]
        s = center - HALF
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            n_skipped += 1
            continue
        seq = fasta[chrom][s:e]
        if "N" in seq or len(seq) != LEN:
            n_skipped += 1
            continue
        f.write(seq)
        f.write("\n")
        n_written += 1

# If we ran out of peaks, sample with replacement to fill to 50k
if n_written < N_SEQS:
    print(f"Need {N_SEQS - n_written} more — sampling with replacement")
    extras_needed = N_SEQS - n_written
    while extras_needed > 0:
        idx = rng.integers(0, len(rows))
        chrom, center = rows[idx]
        # add a small random shift so the duplicate is not literally identical
        shift = int(rng.integers(-30, 31))
        s = center - HALF + shift
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            continue
        seq = fasta[chrom][s:e]
        if "N" in seq or len(seq) != LEN:
            continue
        with open(out_path, "a") as f:
            f.write(seq)
            f.write("\n")
        n_written += 1
        extras_needed -= 1

print(f"Wrote {n_written} sequences. Skipped {n_skipped}.")
assert n_written == N_SEQS
