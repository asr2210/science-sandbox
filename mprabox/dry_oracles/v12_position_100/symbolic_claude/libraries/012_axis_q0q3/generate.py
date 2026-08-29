"""Exp 012: single-axis test (q0 vs q3).

Each seq has q0 = U(0,1), q3 = 1 - q0, q1 = q2 = 0.
All compositional variance concentrated on the q0-q3 axis.

If this axis aligns with hidden y, score >> Dir(0.3). Diagnostic.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(31)
chars = np.array(list("0123"))

lines = []
qs = rng.uniform(0.0, 1.0, size=N)
for i in range(N):
    q0 = qs[i]
    p = np.array([q0, 0.0, 0.0, 1.0 - q0])
    # need a positive prob — guard rare 0/1
    p = np.clip(p, 1e-6, None); p /= p.sum()
    idx = rng.choice(4, size=L, p=p)
    lines.append("".join(chars[idx]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} q0-q3 axis seqs")
