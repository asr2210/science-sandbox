"""Exp 011: each seq has TWO different composition halves.

Per seq: first 100 chars from Dir(0.3) sample A, second 100 from Dir(0.3) sample B.
Adds local composition variance (half-window) beyond global composition.

If models use local windows, this provides info beyond global Dir(0.3).
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
HALF = L // 2

rng = np.random.default_rng(29)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    wa = rng.dirichlet([0.3] * 4)
    wb = rng.dirichlet([0.3] * 4)
    a = rng.choice(4, size=HALF, p=wa)
    b = rng.choice(4, size=HALF, p=wb)
    seq = np.concatenate([a, b])
    lines.append("".join(chars[seq]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} half-segment seqs")
