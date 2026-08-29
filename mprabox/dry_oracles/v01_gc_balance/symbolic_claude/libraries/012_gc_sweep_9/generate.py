"""
Experiment 012: fine GC-content sweep + anchors.

- 4 letter anchors × 1250 = 5000 (10%)
- 9 GC-content random strata × 5000 each = 45000
  GC fractions: 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85
  Within GC: 1 and 2 are equal. Within AT: 0 and 3 are equal.
"""
import os, random

random.seed(12)
L = 200
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

lines = []
for ch in "0123":
    lines += [ch * L] * 1250

gc_levels = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
for gc in gc_levels:
    w0 = (1 - gc) / 2
    w1 = gc / 2
    weights = [w0, w1, w1, w0]
    for _ in range(5000):
        lines.append("".join(random.choices(ALPHABET, weights=weights, k=L)))

assert len(lines) == 50000

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} seqs")
