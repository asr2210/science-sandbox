"""4 buckets HEAVY=0.85 composition + STAY=0.4 within-seq Markov.
Combine bias (boosts b) with autocorrelation (might boost c)."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 12_500
L = 200
HEAVY = 0.85
STAY = 0.4

with open("libraries/010_buckets85_markov40/sequences_0.txt", "w") as f:
    for k in range(4):
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        for _ in range(N_BUCKET):
            seq = np.empty(L, dtype=np.int8)
            seq[0] = rng.choice(4, p=probs)
            for p in range(1, L):
                if rng.random() < STAY:
                    seq[p] = seq[p-1]
                else:
                    seq[p] = rng.choice(4, p=probs)
            f.write("".join(map(str, seq.tolist())) + "\n")
