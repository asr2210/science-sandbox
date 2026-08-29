"""017_class_balanced.

50K = 1,000 cCREs × 10 tiles per cCRE × 5 classes:
  - PLS (promoter-like)
  - pELS (proximal enhancer-like)
  - dELS (distal enhancer-like)
  - CTCF-only
  - DNase-H3K4me3

cCRE class is the 6th column, comma-separated tags. We assign each
cCRE to its PRIMARY tag (first tag before the comma). dELS dominates
74% of the file in random sampling; class-balanced design removes
this bias.

Generalization: cCRE classes are 5 distinct regulatory archetypes.
Balanced exposure gives the model the full archetypal vocabulary,
which transfers to any cell type's regulatory landscape better than
a dELS-dominated sample.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
from collections import defaultdict

PER_CLASS = 1_000
TILES_PER = 10
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0
CLASSES = ["PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3"]

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

by_class = defaultdict(list)
with open(BED) as f:
    for ln in f:
        parts = ln.rstrip().split("\t")
        chrom, start, end = parts[0], parts[1], parts[2]
        if chrom not in KEEP_CHROMS:
            continue
        tags = parts[5].split(",")
        primary = tags[0]  # first tag = main class
        if primary in CLASSES:
            mid = (int(start) + int(end)) // 2
            by_class[primary].append((chrom, mid))

for c in CLASSES:
    print(f"  {c}: {len(by_class[c])} cCREs available")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
selected = []
for c in CLASSES:
    candidates = by_class[c]
    rng.shuffle(candidates)
    selected.extend([(chrom, mid, c) for chrom, mid in candidates])
# Shuffle to mix classes
rng.shuffle(selected)

n_written = 0
n_regions_used = 0
class_counts = defaultdict(int)
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for chrom, mid, c in selected:
        if class_counts[c] >= PER_CLASS:
            continue
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
        class_counts[c] += 1
        n_regions_used += 1
        if all(class_counts[k] >= PER_CLASS for k in CLASSES):
            break

print(f"Class counts: {dict(class_counts)}")
print(f"Wrote {n_written} from {n_regions_used} regions")
assert n_written == 50_000
