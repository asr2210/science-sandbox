"""Experiment 026: total dinucleotide shuffle of library 013.

Take the 013 sequences (35k mc5 + 15k type-balanced cCRE) and
dinucleotide-shuffle each one. Preserves per-sequence GC and dinuc
counts; destroys all motif structure across the whole library.

Tests the absolute ceiling of composition-only training: if 026 ≈ 013,
then NO motif structure anywhere is contributing.
"""
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "006_dinuc_shuffled_multichrom"))
from generate import dinuc_shuffle  # noqa: E402

SEED = 0
SRC = Path(__file__).resolve().parents[1] / "013_mix70_typebalanced_ccre" / "sequences_0.txt"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)

with SRC.open() as f:
    src = [line.rstrip("\n") for line in f]
print(f"Loaded {len(src)} source sequences")

shuffled = [dinuc_shuffle(s, rng) for s in src]
with OUT.open("w") as f:
    for s in shuffled:
        f.write(s)
        f.write("\n")

# Sanity check
from collections import Counter
def dincount(s):
    return Counter(s[i:i+2] for i in range(len(s)-1))
matches = sum(1 for a, b in zip(src[:200], shuffled[:200])
              if dincount(a) == dincount(b))
print(f"Dinuc preservation: {matches}/200")
print(f"Wrote {len(shuffled)} fully-shuffled sequences from 013 library.")
