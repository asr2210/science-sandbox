"""Experiment 018: Multi-seed pooled hg38 random.

4 independent seeds, 12,500 windows each. Tests whether pooling reduces
seed variance and/or adds diversity beyond a single 50k draw. If the
0.139 from exp 006 was a lucky sample, pooling should land near 0.135;
if pooling actually helps, it should exceed.
"""
import pickle
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
N_PER_SEED = 12_500
SEEDS = [101, 202, 303, 404]
L = 200

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

valid = set("ACGT")
out = []
for seed in SEEDS:
    rng = np.random.default_rng(seed)
    got = 0
    while got < N_PER_SEED:
        ci = int(rng.choice(len(names), p=p))
        c = names[ci]
        pos = int(rng.integers(0, lens[ci] - L))
        w = chroms[c][pos:pos + L]
        if not (set(w) <= valid):
            continue
        out.append(w)
        got += 1

# Shuffle so seeds are interleaved in submission
rng = np.random.default_rng(0)
rng.shuffle(out)
assert len(out) == N_TOTAL

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {len(out)} pooled multi-seed sequences ({len(SEEDS)} seeds x {N_PER_SEED})")
