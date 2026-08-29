"""Markov chain (p_stay=0.4) with rejection on [43,57] composition.
Tests whether within-string autocorrelation helps when composition is constrained.
If 016 > 009: structure (autocorrelation, dinucleotide bias) helps.
If 016 < 009: i.i.d. within-string is optimal."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 43, 57
p_stay = 0.4
p_switch = (1 - p_stay) / 3

T = np.full((4, 4), p_switch)
np.fill_diagonal(T, p_stay)
ALPHA = np.array(list("0123"))

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
n_written = 0
n_tries = 0
with open(OUT, "w") as f:
    while n_written < N:
        idx = np.empty(L, dtype=np.int8)
        prev = rng.integers(0, 4)
        idx[0] = prev
        for j in range(1, L):
            prev = rng.choice(4, p=T[prev])
            idx[j] = prev
        counts = np.bincount(idx, minlength=4)
        n_tries += 1
        if (counts >= LO).all() and (counts <= HI).all():
            f.write("".join(ALPHA[idx]) + "\n")
            n_written += 1
        if n_tries > 5_000_000:
            print("WARNING: too many tries, breaking")
            break
print(f"wrote {n_written} Markov [{LO},{HI}] sequences "
      f"({n_tries} tries, accept rate {n_written/n_tries:.4f})")
