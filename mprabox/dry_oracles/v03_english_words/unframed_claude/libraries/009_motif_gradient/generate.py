"""Activity gradient: each sequence has K copies of a strong motif,
K varies from 0 to 9 (5000 sequences per K).
If predictor is monotonic in motif content, this produces a clean
ranked gradient → high correlation.
Motif: TGACTCA (AP-1, a strong, broadly-active enhancer motif).
"""
import numpy as np

N_PER_K = 5000
L = 200
MAX_K = 10
MOTIF = "TGACTCA"
ML = len(MOTIF)

rng = np.random.default_rng(9)
ALPH = np.array(list("ACGT"))

seqs = []
for k in range(MAX_K):
    for _ in range(N_PER_K):
        seq = list(ALPH[rng.integers(0, 4, L)])
        placed = []
        while len(placed) < k:
            s = int(rng.integers(0, L - ML + 1))
            if all(not (s < e2 and s + ML > s2) for s2, e2 in placed):
                seq[s:s + ML] = list(MOTIF)
                placed.append((s, s + ML))
        seqs.append("".join(seq))

rng.shuffle(seqs)
with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {len(seqs)} sequences with AP1 motif count 0..{MAX_K-1}")
