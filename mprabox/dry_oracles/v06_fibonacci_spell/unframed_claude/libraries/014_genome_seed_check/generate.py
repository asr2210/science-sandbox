"""Experiment 014: Repeat of exp 006 (full-genome random) with a different seed.

Tests reproducibility / noise floor of the best library found so far.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 14

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")
out = []
while len(out) < N:
    ci = int(rng.choice(len(names), p=p))
    c = names[ci]
    pos = int(rng.integers(0, lens[ci] - L))
    w = chroms[c][pos:pos + L]
    if set(w) <= valid:
        out.append(w)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {N} sequences (seed={SEED})")
