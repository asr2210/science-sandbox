"""Exp 008: GC-stratified library.

Each sequence has a target GC fraction drawn uniformly from 0.2 to 0.8.
This tests whether COMPOSITION DIVERSITY (wide GC range across the library)
helps the trained model learn — e.g., if the labelling function depends
strongly on GC content, this library would give it the broadest label range.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
SEED = 29

rng = np.random.default_rng(SEED)
gc_targets = rng.uniform(0.2, 0.8, size=N)

bases = np.array(list("ACGT"))
seqs = []
for gc in gc_targets:
    g_or_c = rng.random(L) < gc
    # For G/C positions choose G or C 50/50; for A/T positions choose A or T 50/50.
    gc_choice = rng.integers(0, 2, size=L)  # 0 -> G, 1 -> C
    at_choice = rng.integers(0, 2, size=L)  # 0 -> A, 1 -> T
    arr = np.where(g_or_c, np.where(gc_choice == 0, 2, 1), np.where(at_choice == 0, 0, 3))
    seqs.append("".join(bases[arr]))

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
