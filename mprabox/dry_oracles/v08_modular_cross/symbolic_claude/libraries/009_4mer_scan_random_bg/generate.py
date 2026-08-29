"""4-mer scan in random background.

50,000 sequences = random uniform length 200, with a 4-mer (one of 256, cycled)
inserted at center positions [98..101].

Tests whether 4-mer identity at a fixed central position matters to the model,
without losing background diversity (which we know condition_b for eval_01 likes).
"""
import numpy as np
import os

SEED = 53
N = 50000
L = 200
MK = 4
INSERT_POS = (L - MK) // 2  # 98
ALPHA = "0123"

rng = np.random.default_rng(SEED)

# Random uniform background
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

# Convert int to 4-mer
def int_to_kmer(x, k):
    out = []
    for _ in range(k):
        out.append(x % 4)
        x //= 4
    return out[::-1]

# Insert 4-mer at center
all_4mers = np.array([int_to_kmer(x, MK) for x in range(256)], dtype=np.uint8)
motif_idx = np.arange(N) % 256
arr[:, INSERT_POS : INSERT_POS + MK] = all_4mers[motif_idx]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} sequences (random bg + 4-mer at center) to {out_path}")
