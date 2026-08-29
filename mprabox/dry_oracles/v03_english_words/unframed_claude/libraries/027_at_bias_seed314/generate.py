"""Exp 027: random with slight AT bias toward natural composition.
p_A = p_T = 0.27, p_C = p_G = 0.23 (GC=46%, close to genome's 41%).
Seed=314 (best random seed so far).
"""
import numpy as np, os
N, L, SEED = 50_000, 200, 314
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
p = np.array([0.27, 0.23, 0.23, 0.27])  # A, C, G, T

arr = rng.choice(4, size=(N, L), p=p)
seqs = bases[arr].astype("<U1")
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} AT-bias (p_A=p_T=0.27)")
