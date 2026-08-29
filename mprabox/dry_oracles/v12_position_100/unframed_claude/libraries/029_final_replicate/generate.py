"""Exp 029: defensive replicate of the proven 020 recipe (TFBS-hub + 4 slides).

After 30 experiments, the slide-aug + top-TFBS-cCRE recipe gave the highest
eval_01 (0.0764 in 020, 0.0766 in 023). This is the 4th replicate with a
new seed to provide variance insurance for the final library set.
"""
import os
import gzip
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2
N_UNIQUE = 12_500
OFFSETS = [-75, -25, 25, 75]
SEED = 250

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

# Load TFBS for density scoring
tfbs_by_chrom = {}
with gzip.open(os.path.join(DATA, "encRegTfbsClusteredWithCells.hg38.bed.gz"), "rt") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        chrom = parts[0]
        if chrom not in CHRS:
            continue
        try:
            s, e = int(parts[1]), int(parts[2])
        except ValueError:
            continue
        tfbs_by_chrom.setdefault(chrom, []).append((s + e) // 2)
for c in tfbs_by_chrom:
    tfbs_by_chrom[c] = np.array(sorted(tfbs_by_chrom[c]))

acgt = set("ACGT")
# Build candidate list: (chrom, center, tfbs_count_in_400bp_window)
candidates = []
with open(os.path.join(DATA, "encodeCcre.bed")) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        chrom = parts[0]
        if chrom not in CHRS:
            continue
        try:
            s, e = int(parts[1]), int(parts[2])
        except ValueError:
            continue
        center = (s + e) // 2
        # Need 400bp around center valid (HALF + max offset 75 + L/2)
        outer_half = HALF + 75
        if center - outer_half < 0 or center + outer_half > len(CHRS[chrom]):
            continue
        ctx = CHRS[chrom][center - outer_half:center + outer_half]
        if not (set(ctx) <= acgt):
            continue
        arr = tfbs_by_chrom.get(chrom)
        if arr is None:
            count = 0
        else:
            lo = np.searchsorted(arr, center - outer_half)
            hi = np.searchsorted(arr, center + outer_half)
            count = hi - lo
        candidates.append((chrom, center, count))
print(f"candidates (ACGT in 400bp ctx): {len(candidates)}")

# Pick top N_UNIQUE by TFBS density.
rng = np.random.default_rng(SEED)
counts = np.array([c[2] for c in candidates], dtype=np.int32)
jitter = rng.random(len(candidates))
order = np.lexsort((jitter, -counts))
top = order[:N_UNIQUE]
print(f"top TFBS counts (in 400bp ctx): max={counts[top[0]]} median={int(np.median(counts[top]))} min={counts[top[-1]]}")

seqs = []
for ti in top:
    chrom, center, _ = candidates[ti]
    for off in OFFSETS:
        start = center + off - HALF
        end = start + L
        w = CHRS[chrom][start:end]
        seqs.append(w)
assert len(seqs) == N
print(f"unique seqs: {len(set(seqs))} / {len(seqs)}")
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
