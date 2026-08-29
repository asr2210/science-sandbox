"""Multinomial truncated to [43,57] composition: like 007 but with the [43,57] range.
This SAMPLES each char independently i.i.d. then rejects if composition out of [43,57].

KEY DIFFERENCE from 009: distribution shape over composition tuples is multinomial
(concentrated near 50,50,50,50) instead of uniform-over-tuples (flat).

If 015 > 009: more concentrated (multinomial) compositions help.
If 015 < 009: flat (uniform-over-tuples) compositions help."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 43, 57
ALPHA = np.array(list("0123"))

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
n_written = 0
n_tries = 0
with open(OUT, "w") as f:
    while n_written < N:
        idx = rng.integers(0, 4, size=L)
        counts = np.bincount(idx, minlength=4)
        n_tries += 1
        if (counts >= LO).all() and (counts <= HI).all():
            f.write("".join(ALPHA[idx]) + "\n")
            n_written += 1
print(f"wrote {N} multinomial-truncated [{LO},{HI}] sequences "
      f"({n_tries} tries, accept rate {N/n_tries:.4f})")
