"""1000 unique random sequences, each replicated 50 times → 50K total.
Tests whether averaging via replicates beats one-shot unique sampling."""
import random, os
random.seed(42)
N_UNIQUE, REP, L = 1000, 50, 200
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N_UNIQUE):
        s = "".join(random.choice(ALPHA) for _ in range(L)) + "\n"
        f.writelines([s] * REP)
print(f"Wrote {N_UNIQUE * REP} sequences ({N_UNIQUE} unique x {REP})")
