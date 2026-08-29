"""007_row_gradient — composition linearly varies with row index.
Row 0: P(0,3)=0.10, P(1,2)=0.40 (GC-heavy)
Row 49999: P(0,3)=0.40, P(1,2)=0.10 (AT-heavy)
Tests if target activity is monotone in row index.
"""
import os, numpy as np
N, L = 50_000, 200
rng = np.random.default_rng(2026)

out_lines = []
for i in range(N):
    frac = i / (N - 1)              # 0 -> 1
    p_at = 0.10 + 0.30 * frac       # P for chars 0 and 3 (AT)
    p_gc = 0.40 - 0.30 * frac       # P for chars 1 and 2 (GC)
    probs = np.array([p_at, p_gc, p_gc, p_at])
    row = rng.choice(4, size=L, p=probs).astype(np.int8)
    out_lines.append("".join(str(c) for c in row.tolist()))

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} row-gradient sequences (GC->AT) to {out}")
