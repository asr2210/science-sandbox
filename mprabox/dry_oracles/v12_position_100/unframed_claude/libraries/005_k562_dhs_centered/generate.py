"""Exp 005: K562 DNase-Hypersensitive Site (DHS) centered 200bp windows.

Hypothesis: matched cell-type accessibility (K562 is one of 3 eval cell types).
If H1 is right, eval_01 should jump well above 0.08 (the natural-DNA band).

Sampling: combine 5 K562 DNase-seq peak files from ENCODE. Each peak has a
'summit' coordinate (column 7, 0-indexed 6). Center a 200bp window on the
summit. Drop peaks where the window contains N. Sort by 'smoothed_peak_height'
(column 8) and keep top 50k.
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
SEED = 13
HALF = L // 2

def load_chr(name: str) -> str:
    with open(os.path.join(DATA, name)) as f:
        f.readline()
        return "".join(line.strip() for line in f).upper()

chr_names = [f"chr{x}" for x in list(range(1, 23)) + ["X"]]
chrs = {c: load_chr(f"{c}.fa") for c in chr_names}
print("loaded", len(chrs), "chromosomes")

# Gather K562 peaks across files, dedupe on (chr, summit) by max height.
best = {}  # key (chr, summit) -> height
for path in sorted(glob.glob(os.path.join(DATA, "k562_*.bed.gz"))):
    with gzip.open(path, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 8:
                continue
            chrom = parts[0]
            try:
                summit = int(parts[6])
                height = float(parts[7])
            except ValueError:
                continue
            if chrom not in chrs:
                continue
            k = (chrom, summit)
            if height > best.get(k, -1):
                best[k] = height
print(f"unique K562 summits: {len(best)}")

# Sort by height desc, take top.
items = sorted(best.items(), key=lambda kv: -kv[1])

acgt = set("ACGT")
seqs = []
for (chrom, summit), _ in items:
    seq = chrs[chrom]
    start = summit - HALF
    if start < 0 or start + L > len(seq):
        continue
    w = seq[start:start + L]
    if set(w) <= acgt:
        seqs.append(w)
    if len(seqs) >= N:
        break

# If we don't have 50k strong peaks, pad with random genome windows.
rng = np.random.default_rng(SEED)
if len(seqs) < N:
    chr_list = list(chrs.values())
    weights = np.array([len(c) for c in chr_list], dtype=np.float64)
    weights /= weights.sum()
    while len(seqs) < N:
        ci = rng.choice(len(chr_list), p=weights)
        c = chr_list[ci]
        s = rng.integers(0, len(c) - L + 1)
        w = c[s:s + L]
        if set(w) <= acgt:
            seqs.append(w)

with open(OUT, "w") as f:
    f.write("\n".join(seqs[:N]) + "\n")
print(f"wrote {OUT}: {N} x {L}")
