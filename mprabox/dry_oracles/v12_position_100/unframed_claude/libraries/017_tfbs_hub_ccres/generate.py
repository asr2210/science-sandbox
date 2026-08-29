"""Exp 017: TFBS-hub cCREs.

Score each cCRE by count of TFBS clusters overlapping its 200bp center window.
Take top 50k by TFBS density — sequences packed with multiple TF binding events
should carry more regulatory information per sample.

Augmentation over plain cCRE: prefer information-DENSE regions, not just
"regulatory" regions.
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
SEED = 71

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

# Load TFBS positions by chrom.
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
print(f"TFBS chrom counts: {sum(len(v) for v in tfbs_by_chrom.values())}")

# Score each cCRE by TFBS count in its 200bp window.
acgt = set("ACGT")
candidates = []  # (count, seq)
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
        start = center - HALF
        end = start + L
        if start < 0 or end > len(CHRS[chrom]):
            continue
        w = CHRS[chrom][start:end]
        if not (set(w) <= acgt):
            continue
        tfbs = tfbs_by_chrom.get(chrom)
        if tfbs is None or len(tfbs) == 0:
            count = 0
        else:
            lo = np.searchsorted(tfbs, start)
            hi = np.searchsorted(tfbs, end)
            count = hi - lo
        candidates.append((count, w))
print(f"scored {len(candidates)} cCREs")

# Top N by TFBS count. Tiebreak by random.
rng = np.random.default_rng(SEED)
counts = np.array([c for c, _ in candidates], dtype=np.int32)
jitter = rng.random(len(candidates))
# Negative count for descending; jitter for tiebreak
order = np.lexsort((jitter, -counts))
top = order[:N]
print(f"top cCRE TFBS counts: max={counts[top[0]]} median={int(np.median(counts[top]))} min={counts[top[-1]]}")

seqs = [candidates[i][1] for i in top]
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
