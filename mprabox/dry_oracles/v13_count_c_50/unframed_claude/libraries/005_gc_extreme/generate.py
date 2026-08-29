"""Experiment 5: Push GC range to [0.05, 0.95].

If the metric scales with GC variance, this should improve over exp 4 (range [0.2, 0.8]).
Test whether monotonic improvement continues at extreme GC composition.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=5)
N, L = 50000, 200

gc_targets = rng.uniform(0.05, 0.95, size=N)

is_gc_mat = rng.random((N, L)) < gc_targets[:, None]
gc_choice = rng.integers(0, 2, size=(N, L))   # within GC: 0=C, 1=G
at_choice = rng.integers(0, 2, size=(N, L))   # within AT: 0=A, 1=T
arr = np.where(is_gc_mat,
               np.where(gc_choice == 0, 1, 2),
               np.where(at_choice == 0, 0, 3)).astype(np.int8)

alphabet = np.array(list("ACGT"))
seqs = ["".join(alphabet[row]) for row in arr]

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(seqs) + "\n")

actual_gc = ((arr == 1) | (arr == 2)).mean(axis=1)
print(f"Wrote {N}. Realized GC: min={actual_gc.min():.3f}, "
      f"median={np.median(actual_gc):.3f}, max={actual_gc.max():.3f}, std={actual_gc.std():.3f}")
