"""Exp 024: deterministic 4-pattern library — 12,500 rows of each phase.

NO noise. Library has 4 unique sequences (one per phase).
Per position: exactly 25% each base. Tests extreme structure.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 24
assert N % 4 == 0

positions = np.arange(L, dtype=np.uint8)
# Build 4 patterns (one per phase)
patterns = np.stack([((p + positions) % 4).astype(np.uint8) for p in range(4)])

# 12,500 rows of each phase
phase_ids = np.repeat(np.arange(4, dtype=np.uint8), N // 4)
# Shuffle row order so phases are interleaved
rng = np.random.default_rng(SEED)
rng.shuffle(phase_ids)
seqs = patterns[phase_ids]  # (N, L)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
mins = [min((seqs[:, j] == b).sum() for b in range(4)) for j in range(L)]
print(f"wrote {N}; unique={len(set(map(bytes, seqs)))}; min count per base = {min(mins)}")
