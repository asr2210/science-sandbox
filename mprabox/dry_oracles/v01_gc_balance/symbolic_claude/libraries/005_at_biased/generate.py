"""005_at_biased — opposite of 004. P(0)=P(3)=0.35, P(1)=P(2)=0.15."""
import os, numpy as np
N, L = 50_000, 200
rng = np.random.default_rng(13)
probs = np.array([0.35, 0.15, 0.15, 0.35])
arr = rng.choice(4, size=(N, L), p=probs).astype(np.int8)
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for row in arr:
        f.write("".join(str(c) for c in row.tolist()))
        f.write("\n")
print(f"Wrote {N} AT-biased sequences to {out}")
