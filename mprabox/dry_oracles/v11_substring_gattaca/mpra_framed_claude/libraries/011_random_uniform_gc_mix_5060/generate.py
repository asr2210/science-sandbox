"""Experiment 011: within-library GC mix.

25k 200bp random uniform at GC=0.50 + 25k at GC=0.60. Tests whether a NARROW
GC mix (rather than fixed single GC or wide GC variance from exp 005) can
exploit both regimes simultaneously.
"""
import numpy as np
from pathlib import Path

N_HALF = 25_000
L = 200
SEED = 0
GCs = [0.50, 0.60]

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))


def sample(n, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    cum = np.cumsum(probs)
    u = rng.random(size=(n, L))
    idx = (u[..., None] >= cum).sum(axis=-1)
    return alphabet[idx]


parts = [sample(N_HALF, gc) for gc in GCs]
seqs = np.concatenate(parts, axis=0)
# shuffle so GCs are interleaved
perm = rng.permutation(seqs.shape[0])
seqs = seqs[perm]

mean_gc = np.mean([((s=='G').sum()+(s=='C').sum())/L for s in seqs[:2000]])
print(f"mean GC of first 2000 seqs: {mean_gc:.4f}")

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"wrote {seqs.shape[0]} sequences (mix of GC=0.50 and 0.60)")
