"""016_conserved_ccres.

50K = top 5,000 cCREs by phastCons-conserved-base density within
their 200bp core × 10 random-offset tiles per cCRE.

Tests "conservation enriches per-base information" hypothesis.
phastCons elements identify bases preserved by selection across
100 vertebrate species. cCREs with the highest conserved-base
fraction in their core should be enriched for functional
regulatory grammar.

phastConsElements100way: ~10.3M short elements (avg 16bp), columns:
  bin  chrom  start  end  name(lod=)  score(0-1000)
"""
import numpy as np
from pathlib import Path
from collections import defaultdict
from bisect import bisect_left
from pyfaidx import Fasta

N_REGIONS = 5_000
TILES_PER = 10
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
PHAST = DATA_DIR / "phastConsElements100way.txt"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

print("Loading phastCons elements...")
# Build per-chromosome arrays of (start, end) sorted by start.
phast_by_chrom = defaultdict(list)
with open(PHAST) as f:
    for ln in f:
        parts = ln.rstrip().split("\t")
        # bin chrom start end name score
        chrom = parts[1]
        if chrom not in KEEP_CHROMS:
            continue
        s = int(parts[2])
        e = int(parts[3])
        phast_by_chrom[chrom].append((s, e))
for c in phast_by_chrom:
    phast_by_chrom[c].sort()
total = sum(len(v) for v in phast_by_chrom.values())
print(f"phastCons elements on main chroms: {total}")

# Pre-extract start arrays for fast bisect
phast_starts = {c: [s for s, _ in v] for c, v in phast_by_chrom.items()}


def conserved_bases_in_window(chrom, qs, qe):
    """Count conserved bases in [qs, qe) using phast intervals."""
    if chrom not in phast_by_chrom:
        return 0
    starts = phast_starts[chrom]
    arr = phast_by_chrom[chrom]
    # find first idx with start >= qs - max_element_len (use 4000 to be safe)
    lo = bisect_left(starts, qs - 4000)
    total = 0
    i = lo
    while i < len(arr) and arr[i][0] < qe:
        s, e = arr[i]
        a = max(s, qs)
        b = min(e, qe)
        if b > a:
            total += b - a
        i += 1
    return total


print("Loading cCREs and scoring conservation...")
rows = []  # (chrom, mid)
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, (int(start) + int(end)) // 2))
print(f"cCRE midpoints on main chroms: {len(rows)}")

# Score every cCRE by conservation density in its core ±100bp
scored = []
for chrom, mid in rows:
    qs = mid - HALF
    qe = mid + HALF
    cb = conserved_bases_in_window(chrom, qs, qe)
    scored.append((cb, chrom, mid))

scored.sort(reverse=True)  # highest conservation first
top = scored[:N_REGIONS * 3]  # take 3x to allow Ns / boundary skips
print(f"Top-conservation cCREs: top score={scored[0][0]}, "
      f"5000th={scored[N_REGIONS - 1][0]}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)

n_written = 0
n_regions_used = 0
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for cb, chrom, mid in top:
        if n_regions_used >= N_REGIONS:
            break
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
