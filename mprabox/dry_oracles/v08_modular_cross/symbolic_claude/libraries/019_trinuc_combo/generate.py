"""Experiment 019: Combined trinuc orbit gradient (O012 + AAA, both per-string).

Test additivity of trinuc-orbit signals discovered in exp 016 (eval_10 +0.0104)
and exp 018 (eval_10 +0.0059). Each string i has k_i = round(i/(N-1) * 66)
blocks of length 3 replaced by either an O012-orbit rep OR an AAA-orbit rep
(50/50 random per block). Total non-random trinuc density max ~66 per string.

If eval_10 mean_r reaches ~0.02, signals compound. Also scan eval_01 for
new structure that combined trinuc enrichment might tickle.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 19
KMAX = 66

rng = np.random.default_rng(SEED)
out = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

orbit_o012 = np.array([
    [0, 1, 2], [1, 0, 3], [2, 3, 0], [3, 2, 1],
], dtype=np.uint8)
orbit_aaa = np.array([
    [0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3],
], dtype=np.uint8)

ks = np.round(np.linspace(0, KMAX, N)).astype(int)
n_blocks = L // 3
block_starts = np.arange(n_blocks) * 3

rand_ord = rng.random((N, n_blocks))
order = np.argsort(rand_ord, axis=1)
orbit_pick = rng.integers(0, 2, size=(N, KMAX), dtype=np.uint8)
rep_pick = rng.integers(0, 4, size=(N, KMAX), dtype=np.uint8)

for i in range(N):
    k = ks[i]
    if k == 0:
        continue
    chosen_blocks = order[i, :k]
    starts = block_starts[chosen_blocks]
    for j, s in enumerate(starts):
        if orbit_pick[i, j] == 0:
            out[i, s:s + 3] = orbit_o012[rep_pick[i, j]]
        else:
            out[i, s:s + 3] = orbit_aaa[rep_pick[i, j]]

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

trin = out[:, :-2] * 16 + out[:, 1:-1] * 4 + out[:, 2:]
o012_codes = [0*16+1*4+2, 1*16+0*4+3, 2*16+3*4+0, 3*16+2*4+1]
aaa_codes = [0, 21, 42, 63]
n_o012 = np.isin(trin, o012_codes).sum(axis=1)
n_aaa = np.isin(trin, aaa_codes).sum(axis=1)
print(f"O012 per string: min={n_o012.min()} mean={n_o012.mean():.1f} max={n_o012.max()}")
print(f"AAA per string : min={n_aaa.min()} mean={n_aaa.mean():.1f} max={n_aaa.max()}")
print(f"Wrote {N} sequences with combined trinuc gradient")
