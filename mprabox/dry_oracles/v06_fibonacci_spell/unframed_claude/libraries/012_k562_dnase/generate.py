"""Experiment 012: K562 DNase peak-centered 200bp windows.

Tests cell-type-specific accessible chromatin hypothesis. K562 is the cell
type that has scored worst in random libraries (k562_r=0.012 random, 0.049
genome). If K562-accessible regions are over-represented in test sets, this
should improve mean_r — primarily via k562_r.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 12

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

bed = []
with open(DATA / "k562_dnase.bed") as f:
    for line in f:
        parts = line.rstrip().split("\t")
        c, s, e = parts[0], int(parts[1]), int(parts[2])
        if c in chroms:
            bed.append((c, s, e))
print(f"Loaded {len(bed):,} K562 DNase peaks on canonical chroms")

rng = np.random.default_rng(SEED)
valid = set("ACGT")
out = []
attempts = 0
while len(out) < N:
    i = int(rng.integers(0, len(bed)))
    c, s, e = bed[i]
    center = (s + e) // 2
    start = center - L // 2
    end = start + L
    if start < 0 or end > len(chroms[c]):
        attempts += 1
        continue
    w = chroms[c][start:end]
    attempts += 1
    if set(w) <= valid:
        out.append(w)

print(f"Took {attempts} attempts for {N} clean windows")

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
