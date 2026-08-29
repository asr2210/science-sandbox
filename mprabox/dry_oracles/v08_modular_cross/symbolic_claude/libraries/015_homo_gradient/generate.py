"""Experiment 015: Klein-invariant HOMO-orbit gradient.

Per-string self-transition probability p_i sweeps 0.05 to 0.95. Each string i
uses Markov with P(next=prev)=p_i, P(other)=(1-p_i)/3. This sweeps n_HOMO
(orbit {00,11,22,33}) cleanly across strings while keeping other dinuc
orbits balanced.

If predictor responds to HOMO-orbit frequency (run-length / self-similarity),
|r| should emerge. Exp 5 (markov gradient) hinted negative for eval_01; this
is a cleaner probe with the Klein lens.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 15

# Self-transition probability per string
p_self = np.linspace(0.05, 0.95, N)

rng = np.random.default_rng(SEED)
out = np.empty((N, L), dtype=np.uint8)
out[:, 0] = rng.integers(0, 4, size=N, dtype=np.uint8)

# For each step, draw u ~ U[0,1]. If u < p_self_i, keep prev. Else pick uniform
# from the 3 non-prev chars.
u = rng.random((N, L))
other_choice = rng.integers(0, 3, size=(N, L), dtype=np.uint8)  # 0,1,2

for j in range(1, L):
    prev = out[:, j - 1]
    keep = u[:, j] < p_self
    # non-prev candidates: shift other_choice >= prev by +1 to skip prev
    oc = other_choice[:, j]
    nxt = oc + (oc >= prev).astype(np.uint8)
    out[:, j] = np.where(keep, prev, nxt).astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Diagnostics
n_homo = (out[:, :-1] == out[:, 1:]).sum(axis=1)
print(f"n_HOMO per string: min={n_homo.min()} mean={n_homo.mean():.1f} max={n_homo.max()}")
print(f"Wrote {N} strings with HOMO-orbit gradient")
