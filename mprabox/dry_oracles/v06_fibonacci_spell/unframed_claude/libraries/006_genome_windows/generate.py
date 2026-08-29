"""Experiment 006: Random 200bp windows from FULL hg38 genome.

Uniformly sample positions across all autosomes + X + Y, weighted by chrom
length. Test whether full-genome diversity beats chr22-only.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 6

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")
out = []
attempts = 0
while len(out) < N:
    ci = int(rng.choice(len(names), p=p))
    c = names[ci]
    pos = int(rng.integers(0, lens[ci] - L))
    w = chroms[c][pos:pos + L]
    attempts += 1
    if set(w) <= valid:
        out.append(w)

print(f"Took {attempts} attempts for {N} clean windows")

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")

print(f"Wrote {N} sequences of length {L}")
