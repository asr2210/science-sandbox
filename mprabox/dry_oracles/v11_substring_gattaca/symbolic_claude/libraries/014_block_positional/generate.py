"""Block-positional structure: keep [43,57] composition but assign chars to
positional BLOCKS. Each sequence is split into 4 blocks of 50 positions.
Block k gets primarily character k (with composition c_k), but mixed.

This creates strong per-position bias (varies by position) while preserving
per-sequence [43,57] composition."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 43, 57
BLOCK = 50

# Enumerate valid count tuples for [43,57]
valid = []
for c0 in range(LO, HI + 1):
    for c1 in range(LO, HI + 1):
        for c2 in range(LO, HI + 1):
            c3 = L - c0 - c1 - c2
            if LO <= c3 <= HI:
                valid.append((c0, c1, c2, c3))
valid = np.array(valid)
print(f"# valid count tuples: {len(valid)}")

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = np.array(list("0123"))

with open(OUT, "w") as f:
    for _ in range(N):
        c = valid[rng.integers(0, len(valid))]
        # Build sorted seq: c0 zeros, c1 ones, c2 twos, c3 threes
        # Then split into 4 blocks of 50; shuffle within each block
        seq = np.concatenate([np.full(c[i], chars[i]) for i in range(4)])
        # Split into 4 blocks
        out = np.empty(L, dtype=seq.dtype)
        for b in range(4):
            block = seq[b*BLOCK:(b+1)*BLOCK].copy()
            rng.shuffle(block)
            out[b*BLOCK:(b+1)*BLOCK] = block
        f.write("".join(out) + "\n")
print(f"wrote {N} block-positional sequences ([{LO},{HI}], block size {BLOCK})")
