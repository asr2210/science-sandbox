"""Experiment 016: iid reducing '3' specifically.

'3' was the worst char in probes 011-014. Reduce it instead of boosting '0'.
p = (0.30, 0.30, 0.30, 0.10). Note '0' still up modestly so should compound.

Strategy: combine the wins (less '3') with breakthrough (more '0').
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

p = np.array([0.30, 0.30, 0.30, 0.10])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, p={p}")
