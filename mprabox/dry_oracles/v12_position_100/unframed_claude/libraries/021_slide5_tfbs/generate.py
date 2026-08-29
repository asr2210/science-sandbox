"""Exp 021: 5 sliding windows x 10k TFBS-hub cCREs.

Variation of 020. Try 5 offsets including the centered window {-80, -40, 0, 40, 80}
on 10k highest-TFBS-density cCREs. Tests whether more views per region
(but fewer regions) helps further.
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
N_UNIQUE = 10_000
OFFSETS = [-80, -40, 0, 40, 80]
SEED = 103

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

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
outer_half = HALF + max(abs(o) for o in OFFSETS)
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
print(f"candidates: {len(candidates)}")

rng = np.random.default_rng(SEED)
counts = np.array([c[2] for c in candidates], dtype=np.int32)
jitter = rng.random(len(candidates))
order = np.lexsort((jitter, -counts))
top = order[:N_UNIQUE]
print(f"top TFBS counts: max={counts[top[0]]} median={int(np.median(counts[top]))} min={counts[top[-1]]}")

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
