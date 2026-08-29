"""Position-specific bias: position p prefers character (p mod 4) with 70% prob.
All 50000 sequences share the same per-position bias, but are individually
randomized. Probes whether the scorer cares about per-position character
preferences that are constant across the library."""
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
arr = np.zeros((N, L), dtype=np.int8)
for p in range(L):
    target = p % 4
    probs = np.full(4, 0.10)
    probs[target] = 0.70
    arr[:, p] = rng.choice(4, size=N, p=probs)

with open("libraries/002_position_pattern/sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(map(str, row.tolist())) + "\n")
