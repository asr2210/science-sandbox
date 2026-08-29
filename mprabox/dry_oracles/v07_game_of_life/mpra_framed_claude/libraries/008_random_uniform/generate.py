"""
Experiment 008 — pure random uniform DNA, 40% GC. Floor calibration
in v07 (v04 had this at 0.31).
"""
import os
import sys
import numpy as np

L = 200
N = 50_000
SEED = 0
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")


def main():
    rng = np.random.default_rng(SEED)
    # 40% GC, 60% AT, uniform between A/T and between G/C
    bases = np.array(list("ACGT"))
    probs = np.array([0.30, 0.20, 0.20, 0.30])
    seqs = []
    for _ in range(N):
        idxs = rng.choice(4, size=L, p=probs)
        seqs.append("".join(bases[idxs]))
    with open(OUT, "w") as f:
        f.write("\n".join(seqs) + "\n")
    print(f"Wrote {N} random uniform sequences (40% GC)", file=sys.stderr)


if __name__ == "__main__":
    main()
