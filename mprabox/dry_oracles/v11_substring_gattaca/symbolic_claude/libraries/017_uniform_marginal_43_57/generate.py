"""Uniform marginal on c0, c1, c2 (uniform on [43,57]) with c3=200-c0-c1-c2 (in [43,57]).
Different distribution shape than 009: marginals on 3 chars are uniform [43,57]
(std≈4.03) instead of bell-shaped.

If 017 > 009: uniformizing marginals helps.
If 017 < 009: 009's natural bell-shaped marginals are better."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 43, 57

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = np.array(list("0123"))

n_written = 0
n_tries = 0
with open(OUT, "w") as f:
    while n_written < N:
        c0 = rng.integers(LO, HI + 1)
        c1 = rng.integers(LO, HI + 1)
        c2 = rng.integers(LO, HI + 1)
        c3 = L - c0 - c1 - c2
        n_tries += 1
        if LO <= c3 <= HI:
            seq = np.concatenate([np.full(c0, chars[0]),
                                  np.full(c1, chars[1]),
                                  np.full(c2, chars[2]),
                                  np.full(c3, chars[3])])
            rng.shuffle(seq)
            f.write("".join(seq) + "\n")
            n_written += 1
print(f"wrote {N} uniform-marginal [{LO},{HI}] sequences "
      f"({n_tries} tries, accept rate {N/n_tries:.4f})")
