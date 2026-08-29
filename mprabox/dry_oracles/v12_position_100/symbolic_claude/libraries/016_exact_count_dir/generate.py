"""Exp 016: Exact-count Dir(0.3) compositions.

Sample weights from Dir(0.3). Convert to exact integer counts summing to L.
Build seq with exactly those counts (shuffled). Reduces sampling noise in
compositions.

If the score depends purely on composition, this should give cleaner signal.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(53)
weights = rng.dirichlet([0.3] * 4, size=N)
chars = np.array(list("0123"))

# Convert each weight to exact integer counts summing to L
def to_counts(w, total):
    raw = w * total
    counts = np.floor(raw).astype(int)
    rem = total - counts.sum()
    if rem > 0:
        # distribute remaining to largest fractional parts
        frac = raw - counts
        order = np.argsort(-frac)
        for k in range(rem):
            counts[order[k]] += 1
    return counts

lines = []
for i in range(N):
    c = to_counts(weights[i], L)
    base = np.concatenate([np.full(c[k], k, dtype=np.int8) for k in range(4)])
    rng.shuffle(base)
    lines.append("".join(chars[base]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} exact-count Dir(0.3) seqs")
