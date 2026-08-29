"""Tiled AP-1 strong-enhancer vs poly-A null.

Tests "minimize within-class variance" hypothesis. Two near-identical
classes — active is AP-1 tiled, null is poly-A — should let two
predictors (in the scorer) snap to a clean active/inactive split,
maximizing Pearson r if they agree.

Active design: 8 copies of TGAGTCA (AP-1) tiled with random ACGT spacers
of length 12-18, total length 200bp. Most positions are AP-1 or spacer.

Null design: poly-A with rare random substitutions to avoid identical
sequence collisions.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

rng = np.random.default_rng(601)

# ---- active half: tiled AP-1 ----
AP1 = "TGAGTCA"   # consensus AP-1 (Jun/Fos)
N_TILES = 8       # 8*7 = 56bp of motif
SPACER_BUDGET = L - N_TILES * len(AP1)  # 144bp for 9 spacers (including ends)
# Distribute spacer across 9 gaps roughly evenly
def make_active():
    # Random spacer split: 9 spacers summing to SPACER_BUDGET
    # Use Dirichlet-like sample.
    cuts = sorted(rng.choice(SPACER_BUDGET + 9 - 1, size=8, replace=False).tolist())
    spacers = []
    prev = -1
    for c in cuts:
        spacers.append(c - prev - 1)
        prev = c
    spacers.append(SPACER_BUDGET + 8 - prev - 1)
    # ensure non-negative; shuffle so each AP-1 placement varies
    if any(s < 0 for s in spacers):
        # fallback even split
        even = SPACER_BUDGET // 9
        spacers = [even] * 9
        spacers[-1] += SPACER_BUDGET - sum(spacers)
    rng.shuffle(spacers)
    pieces = []
    bases = list("ACGT")
    for i, sp in enumerate(spacers):
        if sp > 0:
            pieces.append("".join(rng.choice(bases, size=sp)))
        if i < N_TILES:
            # Randomly use forward or reverse-complement (TGASTCA), occasionally TGACTCA
            choice = rng.random()
            if choice < 0.5:
                pieces.append("TGAGTCA")
            elif choice < 0.85:
                pieces.append("TGACTCA")
            else:
                pieces.append("TGAGTCA"[::-1].translate(str.maketrans("ACGT", "TGCA")))
    s = "".join(pieces)
    if len(s) != L:
        # pad / trim
        if len(s) < L:
            s += "".join(rng.choice(bases, size=L - len(s)))
        else:
            s = s[:L]
    return s

half = N_TOTAL // 2
active = [make_active() for _ in range(half)]

# ---- null half: poly-A with sparse random substitutions ----
def make_null():
    s = list("A" * L)
    # Random ~5% sub rate to avoid identical strings (prepare.py might dedupe)
    n_sub = rng.integers(5, 15)
    bases = list("CGT")  # any non-A
    for _ in range(n_sub):
        pos = rng.integers(0, L)
        s[pos] = rng.choice(bases)
    return "".join(s)

null = [make_null() for _ in range(N_TOTAL - half)]

combined = active + null
import random
random.Random(602).shuffle(combined)

out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} sequences (25k AP1-tiled + 25k poly-A-like)")
print(f"Sample active: {active[0][:80]}")
print(f"Sample null:   {null[0][:80]}")
