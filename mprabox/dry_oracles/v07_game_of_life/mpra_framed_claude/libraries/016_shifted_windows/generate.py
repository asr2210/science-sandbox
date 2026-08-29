"""
Experiment 016 — shifted-window augmentation.

Tests whether positional-invariance training (same regulatory context
at multiple offsets) lifts mean_r beyond pure natural sampling.

Design (50K):
  10K random anchor positions in hg38 (length-weighted, GC-stratified)
  Each anchor yields 5 windows at offsets [-50, -25, 0, +25, +50]
  Total: 50K windows, with each "scene" appearing 5 times shifted.

If positional invariance is learnable from training data alone,
model should generalize better than baseline natural at same N=50K.
"""

import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 0
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HG38 = os.path.join(DATA, "hg38.fa")
HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
ALPHABET = set("ACGT")
OFFSETS = [-50, -25, 0, 25, 50]
N_ANCHORS = 10_000


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)
    lens = {c: len(fa[c]) for c in HG38_CHROMS if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()

    out = []
    n_anchors = 0
    margin = max(abs(o) for o in OFFSETS) + L // 2 + 10
    while n_anchors < N_ANCHORS:
        c = cs[rng.choice(len(cs), p=weights)]
        center = int(rng.integers(margin, lens[c] - margin))
        # Sample all 5 windows, verify each is all-ACGT
        windows = []
        ok = True
        for off in OFFSETS:
            start = center + off - L // 2
            seq = str(fa[c][start:start + L]).upper()
            if len(seq) != L or not set(seq).issubset(ALPHABET):
                ok = False
                break
            windows.append(seq)
        if not ok:
            continue
        out.extend(windows)
        n_anchors += 1
        if n_anchors % 1000 == 0:
            print(f"  {n_anchors}/{N_ANCHORS} anchors", file=sys.stderr)

    assert len(out) == 50_000
    print(f"Generated {len(out)} sequences", file=sys.stderr)

    perm = rng.permutation(len(out))
    out = [out[i] for i in perm]
    with open(OUT, "w") as f:
        for s in out:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
