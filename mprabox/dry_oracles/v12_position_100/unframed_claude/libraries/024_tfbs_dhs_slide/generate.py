"""Exp 024: TFBS-density + DHS-signal joint scoring + sliding window aug.

Variant of 020:
- Score each cCRE by (TFBS_count_in_400bp) * (max_DHS_signal_in_400bp+1)
- Top 12.5k -> 4 sliding windows each (offsets +-25, +-75)

Hypothesis: cCREs that are BOTH TFBS-dense AND highly accessible (in K562/HepG2/SKNSH)
are the most regulatory-informative. Joint score should beat TFBS-only.
"""
import os
import gzip
import glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2
N_UNIQUE = 12_500
OFFSETS = [-75, -25, 25, 75]
SEED = 131

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

# TFBS positions
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
print("TFBS loaded")

# DHS peaks: (chrom, start, end, signal). We'll create an interval index per chrom.
dhs_by_chrom = {}  # chrom -> (starts, ends, signals)
for bed in sorted(glob.glob(os.path.join(DATA, "k562_*.bed.gz")) +
                  glob.glob(os.path.join(DATA, "hepg2_*.bed.gz")) +
                  glob.glob(os.path.join(DATA, "sknsh_*.bed.gz"))):
    with gzip.open(bed, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 7:
                continue
            chrom = parts[0]
            if chrom not in CHRS:
                continue
            try:
                s, e = int(parts[1]), int(parts[2])
                sig = float(parts[6])
            except ValueError:
                continue
            dhs_by_chrom.setdefault(chrom, []).append((s, e, sig))
# Sort and arrayify
for c in dhs_by_chrom:
    arr = sorted(dhs_by_chrom[c])
    starts = np.array([x[0] for x in arr], dtype=np.int64)
    ends = np.array([x[1] for x in arr], dtype=np.int64)
    sigs = np.array([x[2] for x in arr], dtype=np.float32)
    dhs_by_chrom[c] = (starts, ends, sigs)
print(f"DHS chrom counts: {sum(len(v[0]) for v in dhs_by_chrom.values())}")

acgt = set("ACGT")
outer_half = HALF + max(abs(o) for o in OFFSETS)
candidates = []  # (chrom, center, tfbs_count, max_dhs_sig)
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
            tfbs_count = 0
        else:
            lo = np.searchsorted(arr, center - outer_half)
            hi = np.searchsorted(arr, center + outer_half)
            tfbs_count = hi - lo
        dhs = dhs_by_chrom.get(chrom)
        if dhs is None:
            max_sig = 0.0
        else:
            starts, ends, sigs = dhs
            # Find any DHS that overlaps [center-outer_half, center+outer_half]
            i = np.searchsorted(ends, center - outer_half, side="right")
            j = np.searchsorted(starts, center + outer_half, side="left")
            if j > i:
                max_sig = float(sigs[i:j].max())
            else:
                max_sig = 0.0
        candidates.append((chrom, center, tfbs_count, max_sig))
print(f"candidates: {len(candidates)}")

# Score: tfbs_count * log(1 + max_dhs_sig)
scores = np.array([c[2] * np.log1p(c[3]) for c in candidates], dtype=np.float32)
rng = np.random.default_rng(SEED)
jitter = rng.random(len(candidates))
order = np.lexsort((jitter, -scores))
top = order[:N_UNIQUE]
print(f"top scores: max={scores[top[0]]:.1f} median={float(np.median(scores[top])):.1f} min={scores[top[-1]]:.1f}")
print(f"  TFBS: max={candidates[top[0]][2]} median={int(np.median([candidates[i][2] for i in top]))}")
print(f"  DHS:  max={candidates[top[0]][3]:.1f} median={float(np.median([candidates[i][3] for i in top])):.1f}")

seqs = []
for ti in top:
    chrom, center, _, _ = candidates[ti]
    for off in OFFSETS:
        start = center + off - HALF
        end = start + L
        seqs.append(CHRS[chrom][start:end])
assert len(seqs) == N
print(f"unique seqs: {len(set(seqs))} / {len(seqs)}")
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
