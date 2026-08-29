"""Exp 003: stratified GC composition.

Each of 50k sequences has GC fraction p ~ U[0, 1]. Each position is:
  - G or C (chars 1, 2 — picked uniformly) with prob p
  - A or T (chars 0, 3 — picked uniformly) with prob 1-p
Within G/C and A/T, uniform pick between the two members.

Tests whether activity / target correlates with GC content; if yes this should
significantly boost K562/HepG2 r above the random baseline (0.59 / 0.62).
"""
import os
import numpy as np

N = 50_000
L = 200
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(3)
p = rng.uniform(0.0, 1.0, size=N).astype(np.float32)            # per-seq GC fraction
# For each row, sample which positions are GC vs AT
is_gc = rng.random(size=(N, L)) < p[:, None]                    # bool [N,L]
# Within GC pick 1 or 2; within AT pick 0 or 3
sub = rng.integers(0, 2, size=(N, L), dtype=np.int8)            # 0/1
chars = np.where(is_gc, 1 + sub, 0 + 3 * sub).astype(np.int8)   # gc:{1,2}, at:{0,3}
chars += ord('0')

with open(OUT, "wb") as f:
    for i in range(N):
        f.write(bytes(chars[i].tolist()))
        f.write(b"\n")
print(f"Wrote {N} GC-stratified sequences to {OUT}")
