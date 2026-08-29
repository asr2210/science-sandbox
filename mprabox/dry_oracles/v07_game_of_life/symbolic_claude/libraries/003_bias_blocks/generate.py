"""Experiment 003: 4 blocks with strong bias toward each character.

12,500 strings biased 70% toward each of {0,1,2,3}.
Other 30% uniform among the other 3 chars.
Mean across blocks = (m_0 + m_1 + m_2 + m_3) / 4 -- tells us if bias is rewarded.
"""
import os
import numpy as np

N_PER_BLOCK = 12_500
L = 200
SEED = 7

rng = np.random.default_rng(SEED)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for bias_char in range(4):
        # probability vector: 0.7 for bias_char, 0.1 for each other
        probs = np.full(4, 0.1)
        probs[bias_char] = 0.7
        block = rng.choice(4, size=(N_PER_BLOCK, L), p=probs).astype(np.uint8)
        for row in block:
            f.write("".join(map(str, row.tolist())))
            f.write("\n")
print(f"Wrote 4 blocks of {N_PER_BLOCK} biased strings to {out_path}")
