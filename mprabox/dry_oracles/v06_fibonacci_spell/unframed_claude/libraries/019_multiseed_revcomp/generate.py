"""Experiment 019: Multi-seed pool + 50% revcomp augmentation.

Stack of 018 (4 seeds x 12.5k) + 017 (50% revcomp). Tests whether the
small revcomp gain (017: 0.1379 vs 014: 0.1350) is real by reducing
seed-noise via pooling.
"""
import pickle
import numpy as np
from pathlib import Path

N_PER_SEED = 12_500
SEEDS = [101, 202, 303, 404]
L = 200
RC_SEED = 19

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

valid = set("ACGT")
COMP = str.maketrans("ACGT", "TGCA")

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

# Apply revcomp to a random 50% (deterministic via dedicated seed)
rc_rng = np.random.default_rng(RC_SEED)
mask = rc_rng.random(len(out)) < 0.5
for i in range(len(out)):
    if mask[i]:
        out[i] = out[i].translate(COMP)[::-1]

# Shuffle to interleave
shuf = np.random.default_rng(0)
idx = np.arange(len(out))
shuf.shuffle(idx)
out = [out[i] for i in idx]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {len(out)} pooled+revcomp sequences ({len(SEEDS)} seeds, {mask.sum()} revcomp'd)")
