"""006_at_extreme — push AT-bias: P(0)=P(3)=0.45, P(1)=P(2)=0.05."""
import os, numpy as np
N, L = 50_000, 200
rng = np.random.default_rng(21)
probs = np.array([0.45, 0.05, 0.05, 0.45])
arr = rng.choice(4, size=(N, L), p=probs).astype(np.int8)
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for row in arr:
        f.write("".join(str(c) for c in row.tolist()))
        f.write("\n")
print(f"Wrote {N} extreme AT-biased sequences to {out}")
