"""Exp 015: Dir(0.3) + 5 random 6-mer motif insertions per seq.

Tests if k-mer-level / motif-level features add signal beyond composition.
Each seq: Dir(0.3) base, then overwrite 5 contiguous 6-char windows with
randomly drawn 6-mers. Total ~15% of seq overwritten.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
NMOTIF = 5
KLEN = 6

rng = np.random.default_rng(43)
weights = rng.dirichlet([0.3] * 4, size=N)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    base = rng.choice(4, size=L, p=weights[i])
    # Insert NMOTIF random k-mers at non-overlapping random positions
    # Choose positions sequentially without overlap
    available_positions = list(range(L - KLEN + 1))
    used = []
    for _ in range(NMOTIF):
        # pick from available, then remove overlapping
        if not available_positions:
            break
        p = int(rng.choice(available_positions))
        used.append(p)
        # remove overlapping
        available_positions = [q for q in available_positions if abs(q - p) >= KLEN]
    for p in used:
        motif = rng.integers(0, 4, size=KLEN)
        base[p:p+KLEN] = motif
    lines.append("".join(chars[base]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} Dir(0.3)+motif seqs")
