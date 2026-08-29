"""Experiment 012: random uniform GC=0.55 (refine peak location)."""
import numpy as np
from pathlib import Path

N, L, SEED, GC = 50_000, 200, 0, 0.55
rng = np.random.default_rng(SEED)
probs = np.array([(1 - GC) / 2, GC / 2, GC / 2, (1 - GC) / 2])
cum = np.cumsum(probs)
alphabet = np.array(list("ACGT"))
u = rng.random(size=(N, L))
idx = (u[..., None] >= cum).sum(axis=-1)
seqs = alphabet[idx]
print(f"GC sample (first 1000): "
      f"{np.mean([((s=='G').sum()+(s=='C').sum())/L for s in seqs[:1000]]):.4f}")
out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences")
