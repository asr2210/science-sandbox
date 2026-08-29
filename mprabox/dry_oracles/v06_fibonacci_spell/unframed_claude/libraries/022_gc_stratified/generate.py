"""Experiment 022: GC-stratified random hg38 sampling.

Force equal counts per GC bucket: 30-40%, 40-50%, 50-60%, 60-70%.
Tests whether broadening GC distribution beyond natural (peaked ~42%)
helps or hurts. If natural-distribution-wins theory holds, this hurts.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 22
BUCKETS = [(0.30, 0.40), (0.40, 0.50), (0.50, 0.60), (0.60, 0.70)]
PER_BUCKET = N // len(BUCKETS)  # 12,500 each

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")

buckets = {b: [] for b in BUCKETS}
done_buckets = 0
attempts = 0
print(f"Sampling until each of {len(BUCKETS)} buckets has {PER_BUCKET}")
while done_buckets < len(BUCKETS):
    attempts += 1
    ci = int(rng.choice(len(names), p=p))
    c = names[ci]
    pos = int(rng.integers(0, lens[ci] - L))
    w = chroms[c][pos:pos + L]
    if not (set(w) <= valid):
        continue
    gc = (w.count("G") + w.count("C")) / L
    for lo, hi in BUCKETS:
        if lo <= gc < hi:
            if len(buckets[(lo, hi)]) < PER_BUCKET:
                buckets[(lo, hi)].append(w)
                if len(buckets[(lo, hi)]) == PER_BUCKET:
                    done_buckets += 1
                    print(f"  bucket [{lo:.1f},{hi:.1f}] full after {attempts} attempts")
            break

out = []
for b in BUCKETS:
    out.extend(buckets[b])
rng.shuffle(out)
assert len(out) == N

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {N} GC-stratified sequences (total attempts={attempts})")
