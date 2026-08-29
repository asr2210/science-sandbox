"""Experiment 011: maximize per-sequence GC variance while keeping
library mean ≈ 0.5.

Per-sequence GC drawn from uniform [0.2, 0.8]. Total library GC ≈ 0.5.
Within each sequence, bases drawn i.i.d. from {A,T,C,G} with that GC.
Predicts HepG2 lift (more variance for it to detect), K562 ~ same.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(11)
gcs = rng.uniform(0.2, 0.8, size=N)

seqs = []
for gc in gcs:
    p_each_at = (1 - gc) / 2
    p_each_cg = gc / 2
    p = np.array([p_each_at, p_each_cg, p_each_cg, p_each_at])  # A C G T
    idx = rng.choice(4, size=L, p=p)
    seqs.append("".join(ALPHABET[idx]))

# stats
gc_lib = sum((s.count("C") + s.count("G")) for s in seqs[:5000]) / (5000 * L)
gc_per_seq = np.array([(s.count("C") + s.count("G")) / L for s in seqs[:5000]])
print(f"library GC mean: {gc_lib:.4f}")
print(f"per-seq GC: mean={gc_per_seq.mean():.3f}, std={gc_per_seq.std():.3f}, min={gc_per_seq.min():.3f}, max={gc_per_seq.max():.3f}")

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {len(seqs)} sequences to {OUT}")
