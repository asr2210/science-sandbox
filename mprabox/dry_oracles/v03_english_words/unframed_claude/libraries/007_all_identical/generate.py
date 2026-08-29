"""Diagnostic: all 50k sequences identical.
If score is correlation-based (needs variance), r should crash toward 0.
If score is per-sequence aggregate, r should be similar to random baseline.
Sequence chosen: a single random 200bp draw (seed 0).
"""
import numpy as np

L = 200
N = 50000
rng = np.random.default_rng(0)
alphabet = np.array(list("ACGT"))
single = "".join(alphabet[rng.integers(0, 4, L)].tolist())
print("Template:", single[:60], "...")

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for _ in range(N):
        f.write(single + "\n")

print(f"Wrote {N} identical copies")
