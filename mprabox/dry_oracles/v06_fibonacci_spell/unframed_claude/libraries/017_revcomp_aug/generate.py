"""Experiment 017: Full-genome random with 50% reverse-complemented.

Tests whether revcomp augmentation helps. DNA is double-stranded so both
strands carry information. If the scorer model is strand-aware, training
on both strands should add coverage. If not, this is no-op.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 17

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")
COMP = str.maketrans("ACGT", "TGCA")

out = []
while len(out) < N:
    ci = int(rng.choice(len(names), p=p))
    c = names[ci]
    pos = int(rng.integers(0, lens[ci] - L))
    w = chroms[c][pos:pos + L]
    if not (set(w) <= valid):
        continue
    if rng.random() < 0.5:
        w = w.translate(COMP)[::-1]
    out.append(w)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {N} hg38 random sequences with 50% revcomp")
