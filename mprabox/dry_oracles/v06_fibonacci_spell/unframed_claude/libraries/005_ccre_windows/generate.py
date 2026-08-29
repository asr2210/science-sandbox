"""Experiment 005: 200bp windows centered on ENCODE cCREs.

ENCODE V3 has ~1M cCREs (candidate cis-regulatory elements). Sample 50,000
random elements and take the 200bp window centered on them. Predict: these
regulatory-element-enriched sequences should score above random chr22 windows.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 5

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

# Read cCRE BED
bed = []
with open(DATA / "cCREs.bed") as f:
    for line in f:
        parts = line.rstrip().split("\t")
        c, s, e = parts[0], int(parts[1]), int(parts[2])
        if c in chroms:
            bed.append((c, s, e))
print(f"Loaded {len(bed):,} cCREs on canonical chroms")

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

print(f"Wrote {N} sequences of length {L}")
