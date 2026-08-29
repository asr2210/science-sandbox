"""Experiment 009: random uniform with fixed GC=0.60 (vs 0.50 baseline).

If higher GC matches the eval distribution better (regulatory regions are
often GC-rich), this should beat random uniform GC=0.50.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 0
GC = 0.60

rng = np.random.default_rng(SEED)
probs = np.array([(1 - GC) / 2, GC / 2, GC / 2, (1 - GC) / 2])  # A C G T
cum = np.cumsum(probs)
alphabet = np.array(list("ACGT"))

u = rng.random(size=(N, L))
idx = (u[..., None] >= cum).sum(axis=-1)
seqs = alphabet[idx]

# verify GC
sample_gc = np.array([(s == "G").sum() + (s == "C").sum() for s in seqs[:1000]]) / L
print(f"target GC=0.60, realized GC: {sample_gc.mean():.4f} ± {sample_gc.std():.4f}")

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out}")
