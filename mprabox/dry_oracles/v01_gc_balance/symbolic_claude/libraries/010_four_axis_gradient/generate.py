"""010_four_axis_gradient — independent per-char gradients, all monotone with row idx.
Row 0:   counts (2, 100, 78, 20). Sum 200.
Row N-1: counts (98, 10, 12, 80). Sum 200.
Char deltas: 0:+96, 1:-90, 2:-66, 3:+60. (0+3) net +156, (1+2) net -156, sum 0.
Keeps the (AT vs GC) gradient strong and adds independent 0-vs-3 and 1-vs-2 axes.
"""
import os, numpy as np
N, L = 50_000, 200
rng = np.random.default_rng(303)

def lerp(a, b, frac):
    return int(round(a + (b - a) * frac))

out_lines = []
for i in range(N):
    frac = i / (N - 1)
    c0 = lerp(2, 98, frac)
    c1 = lerp(100, 10, frac)
    c3 = lerp(20, 80, frac)
    c2 = L - c0 - c1 - c3
    assert c2 >= 2, (i, c0, c1, c2, c3)
    chars = [0]*c0 + [1]*c1 + [2]*c2 + [3]*c3
    assert len(chars) == L
    row = np.array(chars, dtype=np.int8)
    rng.shuffle(row)
    out_lines.append("".join(str(c) for c in row.tolist()))

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} 4-axis-gradient to {out}")
