"""Exp 013: Per-sequence balanced 50:50:50:50 (exactly 50 of each base).
Each 200bp sequence contains exactly 50 A, 50 C, 50 G, 50 T.
Sequences are randomly shuffled compositions of '50A+50C+50G+50T'.

If extreme per-seq uniformity helps K562/HepG2, this should beat random.
If not, random is the optimum and no further composition tuning helps.
"""
import numpy as np, os

N = 50_000
L = 200
SEED = 13
rng = np.random.default_rng(SEED)
template = list("A" * 50 + "C" * 50 + "G" * 50 + "T" * 50)
template_arr = np.array(template)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        arr = template_arr.copy()
        rng.shuffle(arr)
        f.write("".join(arr.tolist()) + "\n")
print(f"Wrote {N} balanced (50A,50C,50G,50T) sequences")
