"""
Experiment 007: 16 distinct dimer-repeat templates, 3125 copies each.
Templates: '00'*100, '01'*100, '02'*100, ..., '33'*100.

Tests if 2-character variety creates non-constant f and g vectors.
Pearson r over 16 distinct (f,g) points should be meaningful (if not NaN).
"""
import os

L = 200
N = 50000
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

templates = []
for a in "0123":
    for b in "0123":
        dimer = a + b
        templates.append((dimer * (L // 2 + 1))[:L])

assert len(templates) == 16
reps = N // 16  # 3125
assert reps * 16 == N

lines = []
for t in templates:
    lines += [t] * reps
assert len(lines) == N

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} sequences (16 distinct dimer-repeat templates × {reps})")
