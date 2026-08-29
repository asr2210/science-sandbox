"""4 buckets with EXACT per-seq composition (no draw noise).
Each seq has exactly 170 of bucket char + 10 of each other char,
shuffled. Tests whether cond_b prefers exact vs distributed compositions."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 12_500
L = 200
N_HEAVY = 170  # 85%
N_LIGHT = 10   # 5% each x 3

with open("libraries/015_4buckets_exact_compo/sequences_0.txt", "w") as f:
    for k in range(4):
        for j in range(N_BUCKET):
            chars = [k] * N_HEAVY
            for o in range(4):
                if o != k:
                    chars += [o] * N_LIGHT
            rng.shuffle(chars)
            f.write("".join(map(str, chars)) + "\n")
