"""Experiment 005: Sub-alphabet test - only chars {0,1}.

50k sequences over alphabet {0,1} (50/50 random per position). Tests if reduced
alphabet improves or hurts. If target uses all 4 chars equally, this drops score.
If target only uses {0,1}, this boosts.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 13

rng = np.random.default_rng(SEED)
chars = rng.integers(0, 2, size=(N, L), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in chars:
        f.write("".join(map(str, row.tolist())))
        f.write("\n")
print(f"Wrote {N} {{0,1}}-only random sequences to {out_path}")
