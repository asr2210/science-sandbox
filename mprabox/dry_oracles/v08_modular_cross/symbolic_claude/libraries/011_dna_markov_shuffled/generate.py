"""Experiment 011: Shuffled exp 9 sequences (test if ordering matters).

Take 009_dna_markov/sequences_0.txt and apply a random permutation.
Same content, different position assignments.

If results match exp 9 → mean_r and conditions are position-invariant
(true Pearson r ignores ordering). If results differ → conditions are
position-based subsets and submission order matters.
"""
import os
import numpy as np

src = os.path.join(os.path.dirname(__file__), "..", "009_dna_markov", "sequences_0.txt")
with open(src) as f:
    lines = [ln for ln in f.read().splitlines() if ln]
assert len(lines) == 50_000

rng = np.random.default_rng(11)
order = rng.permutation(len(lines))
shuffled = [lines[i] for i in order]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(shuffled) + "\n")

print(f"Shuffled {len(shuffled)} sequences (same content as exp 9, different order)")
