"""Experiment 025: Seed lottery on best composition. seed=999."""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(999)
p = np.array([0.275, 0.2417, 0.2417, 0.2416])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
print(f"Wrote {N} sequences, p={p}, seed=999")
