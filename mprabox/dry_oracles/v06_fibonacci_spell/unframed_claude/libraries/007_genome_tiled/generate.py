"""Experiment 007: Tiled non-overlapping windows across full hg38.

Tile each chromosome at uniform interval such that total ~60-70k windows
result, then take first 50k that are N-free. Maximally non-redundant.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
total = sum(len(chroms[n]) for n in names)
# Aim for ~80k windows to have a buffer for N-rejection
target = 80_000
step = total // target  # ~38 kb step
print(f"step = {step:,}")

valid = set("ACGT")
out = []
for name in names:
    seq = chroms[name]
    for pos in range(0, len(seq) - L, step):
        w = seq[pos:pos + L]
        if set(w) <= valid:
            out.append(w)
        if len(out) >= N:
            break
    if len(out) >= N:
        break

# Should have plenty
print(f"Generated {len(out)} clean tiled windows; trimming to {N}")
out = out[:N]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")

print(f"Wrote {len(out)} sequences of length {L}")
