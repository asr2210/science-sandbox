"""4 buckets HEAVY=0.85 INTERLEAVED: row i has bucket (i % 4).
Tests whether ROW ORDER matters — the scorer might use row index in
its target."""
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
HEAVY = 0.85

with open("libraries/017_heavy85_interleaved/sequences_0.txt", "w") as f:
    for i in range(N):
        k = i % 4
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        seq = rng.choice(4, size=L, p=probs)
        f.write("".join(map(str, seq.tolist())) + "\n")
