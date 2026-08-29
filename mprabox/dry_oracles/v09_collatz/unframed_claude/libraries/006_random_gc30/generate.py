"""Experiment 006 — Random sequences at 30% GC.

Counterpart to exp 005. If 70% boosts and 30% drops, GC content drives
the score (e.g., via CpG / GC-box / GC-context bias of activator models).
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(6)
N, L = 50_000, 200

# 30% GC
bases = np.array(list("ACGT"))
probs = np.array([0.35, 0.15, 0.15, 0.35])
idx = rng.choice(4, size=(N, L), p=probs)
seqs = bases[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row)); f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
