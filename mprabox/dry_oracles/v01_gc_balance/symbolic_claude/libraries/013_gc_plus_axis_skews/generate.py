"""
Experiment 013: GC sweep + orthogonal axis strata.

- 4 letter anchors × 1250 = 5000 (10%)
- 9 GC-content strata × 2500 = 22500 (45%)
- 6 axis strata × 3750 = 22500 (45%)
  Axes cover: 01-rich, 23-rich, 02-rich, 13-rich, very-02-rich, very-13-rich.
  The 02-rich and 13-rich orthogonal axes (purine/pyrimidine-like) are NEW
  — uniform random had p(02)=p(13) by symmetry, but these strata break it.
"""
import os, random

random.seed(13)
L = 200
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

lines = []

# Letter anchors
for ch in "0123":
    lines += [ch * L] * 1250

# GC sweep (same as exp 012 but reduced to 2500 per level)
gc_levels = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
for gc in gc_levels:
    w0 = (1 - gc) / 2; w1 = gc / 2
    weights = [w0, w1, w1, w0]
    for _ in range(2500):
        lines.append("".join(random.choices(ALPHABET, weights=weights, k=L)))

# Axis strata
axis_configs = [
    ([4,4,1,1], "01-rich"),
    ([1,1,4,4], "23-rich"),
    ([4,1,4,1], "02-rich"),
    ([1,4,1,4], "13-rich"),
    ([9,1,9,1], "very-02-rich"),
    ([1,9,1,9], "very-13-rich"),
]
for w, name in axis_configs:
    for _ in range(3750):
        lines.append("".join(random.choices(ALPHABET, weights=w, k=L)))

assert len(lines) == 50000

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} seqs")
