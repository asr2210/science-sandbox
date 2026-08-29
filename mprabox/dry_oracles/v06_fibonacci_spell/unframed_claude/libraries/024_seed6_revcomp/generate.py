"""Experiment 024: Best base (exp 006 seed=6) + 50% revcomp augmentation.

Best replicable base (006 = 0.1387) layered with the best augmentation
attempt (017 with revcomp showed 0.1379 but was inside noise). If
revcomp contributes ANY signal, this stacks 006's upper-tail base + aug
for possible 0.140+.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 6        # Match exp 006 EXACTLY for the base
RC_SEED = 24    # Separate seed for the revcomp mask

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

print(f"Took {attempts} attempts for {N} clean windows (base seed=6)")

# Apply 50% revcomp via separate seed (doesn't affect base)
rc_rng = np.random.default_rng(RC_SEED)
COMP = str.maketrans("ACGT", "TGCA")
mask = rc_rng.random(N) < 0.5
for i in range(N):
    if mask[i]:
        out[i] = out[i].translate(COMP)[::-1]
print(f"Reverse-complemented {int(mask.sum())} / {N}")

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {N} sequences (006 base + 50% revcomp)")
