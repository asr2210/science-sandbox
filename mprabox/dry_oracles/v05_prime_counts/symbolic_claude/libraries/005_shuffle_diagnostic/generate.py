"""Experiment 005: SHUFFLE diagnostic.

Take the exact same 50K sequences from exp 001 (uniform random seed=0),
just reorder them with a different permutation.

If score is order-invariant (library statistic) -> r ≈ exp001.
If score depends on per-index alignment -> r differs.
"""
import os
import numpy as np

SHUFFLE_SEED = 12345

def main():
    here = os.path.dirname(__file__)
    src = os.path.join(here, "..", "001_uniform_random", "sequences_0.txt")
    with open(src) as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    assert len(lines) == 50_000
    rng = np.random.default_rng(SHUFFLE_SEED)
    perm = rng.permutation(len(lines))
    shuffled = [lines[i] for i in perm]
    out = os.path.join(here, "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(shuffled) + "\n")
    print(f"shuffled {len(shuffled)} lines, wrote to {out}")
    # quick sanity: first 3 lines of original vs shuffled
    print("original[0:2]:", [s[:30] for s in lines[:2]])
    print("shuffled[0:2]:", [s[:30] for s in shuffled[:2]])

if __name__ == "__main__":
    main()
