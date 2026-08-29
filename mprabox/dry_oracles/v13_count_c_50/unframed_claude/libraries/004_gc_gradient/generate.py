"""Experiment 4: GC-content gradient (no motifs).

Each sequence drawn from a Bernoulli/categorical distribution with target GC%
sampled uniformly from [0.20, 0.80] across the library. Pure 4-letter alphabet,
no inserted patterns. Tests whether smooth GC variance alone increases r.

A/T and C/G drawn equiprobably within their group.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=4)
N, L = 50000, 200

gc_targets = rng.uniform(0.20, 0.80, size=N)

# For each sequence: draw 200 bases; each base is G/C with prob gc, else A/T.
# Within G/C: 50/50 G or C. Within A/T: 50/50 A or T.
arr = np.empty((N, L), dtype=np.int8)
for i, gc in enumerate(gc_targets):
    # 0=A, 1=C, 2=G, 3=T
    is_gc = rng.random(L) < gc
    # within GC: half C (1), half G (2)
    gc_choice = rng.integers(0, 2, size=L)  # 0 or 1
    at_choice = rng.integers(0, 2, size=L)  # 0 or 1
    bases = np.where(is_gc,
                     np.where(gc_choice == 0, 1, 2),
                     np.where(at_choice == 0, 0, 3))
    arr[i] = bases

alphabet = np.array(list("ACGT"))
seqs = ["".join(alphabet[row]) for row in arr]

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(seqs) + "\n")

# Sanity: check actual GC% per sequence
actual_gc = ((arr == 1) | (arr == 2)).mean(axis=1)
print(f"Wrote {N} seqs. Target GC in [0.2, 0.8]. Realized GC: "
      f"min={actual_gc.min():.3f}, median={np.median(actual_gc):.3f}, max={actual_gc.max():.3f}, std={actual_gc.std():.3f}")
