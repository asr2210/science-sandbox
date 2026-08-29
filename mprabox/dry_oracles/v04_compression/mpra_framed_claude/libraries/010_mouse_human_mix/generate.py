"""Experiment 010: 25K human natural + 25K mouse (mm39) natural — cross-species test.

Tests whether evolutionary diversity (sequence from a different mammalian
species) breaks the plateau. The model's eval task is presumably human;
mouse DNA shares the regulatory grammar but differs in exact sequences.

Hypotheses:
- If 010 > 0.50: cross-species diversity adds genuine signal beyond
  human-only mixes. Plateau breaks.
- If 010 ≈ 0.49: mouse is interchangeable with human at the grammar
  level — confirms universality of regulatory features.
- If 010 < 0.49: mouse sequences hurt because they have human-irrelevant
  patterns.

Generalization argument: this is the MOST DIRECT test of cross-cell-type
generalization. Cell types within a species share the same DNA substrate
but differ in TF expression. If grammar is truly universal (across cell
types in human), it should also be largely universal across mammals
(across species). Training with cross-species samples adds an
"out-of-distribution" robustness signal.
"""
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_HUMAN = 25_000
N_MOUSE = N_SEQ - N_HUMAN
L = 200
SEED = 0

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HG38 = os.path.join(REPO_ROOT, "data", "hg38.fa")
MM39 = os.path.join(REPO_ROOT, "data", "mm39.fa")

HUMAN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
# mouse primary autosomes + sex
MOUSE_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]


def sample_natural(fa, chroms, n, rng):
    chrom_lens = {c: len(fa[c]) for c in chroms}
    chroms_arr = np.array(chroms)
    weights = np.array([chrom_lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = rng.choice(chroms_arr, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
    return out


def main():
    hg = Fasta(HG38, sequence_always_upper=True)
    mm = Fasta(MM39, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)
    human = sample_natural(hg, HUMAN_CHROMS, N_HUMAN, rng)
    print(f"human: {len(human)}")
    mouse = sample_natural(mm, MOUSE_CHROMS, N_MOUSE, rng)
    print(f"mouse: {len(mouse)}")
    seqs = human + mouse
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ} sequences")


if __name__ == "__main__":
    main()
