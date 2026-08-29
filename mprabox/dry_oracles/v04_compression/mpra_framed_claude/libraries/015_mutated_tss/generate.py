"""Experiment 015: 008 with 15% per-base random mutations.

Take 008's 50k real TSS-proximal sequences and apply 15% per-base
random ACGT mutation. Tests theory v11: does the long-range
coherence axis survive small per-base noise?

- 015 ≈ 008 (~0.50): real backbones are robust; mutation augment works
- 015 < 008: exact sequence integrity matters

Why this generalizes: if augmentation via mutation preserves
training value, we can expand any natural-DNA source arbitrarily
to get larger effective libraries without needing more genome.
"""
import random
import numpy as np
from pathlib import Path

LEN = 200
MUT_RATE = 0.15
SEED = 42

HERE = Path(__file__).parent
SRC = HERE.parents[0] / "008_tss_proximal_random" / "sequences_0.txt"
ALPH = np.array(list("ACGT"))

def main():
    rng = np.random.default_rng(SEED)
    pyrng = random.Random(SEED + 1)

    with open(SRC) as f:
        src = [l.strip() for l in f if l.strip()]
    print(f"Source: {len(src)}")

    # Convert sequences to integer arrays
    a2i = {"A": 0, "C": 1, "G": 2, "T": 3}
    N = len(src)
    arr = np.zeros((N, LEN), dtype=np.int8)
    for i, s in enumerate(src):
        for j, ch in enumerate(s):
            arr[i, j] = a2i[ch]

    # Mutation mask: True where we replace with random nt
    mask = rng.random((N, LEN)) < MUT_RATE
    new_nts = rng.integers(0, 4, size=(N, LEN), dtype=np.int8)
    arr_mut = np.where(mask, new_nts, arr)
    n_changed = mask.sum()
    print(f"Mutated {n_changed} bases out of {N*LEN} ({n_changed/(N*LEN):.3f})")

    # Convert back to strings
    seqs = ["".join(ALPH[row]) for row in arr_mut]
    pyrng.shuffle(seqs)

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} to {out_path}")

if __name__ == "__main__":
    main()
