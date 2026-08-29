"""
Experiment 027 — JASPAR-motif-planted GC-stratified random scaffolds.

Tests whether explicit motif content can break the 0.394 ceiling
set by GC-strat natural. Decomposition from exp 025/026 said:
+0.009 lift comes from motif content (k>=3) above i.i.d. random.
If MORE motifs lift further → motif density is an exploitable lever.

Design (50K):
  10K GC-strat random scaffolds per GC bin (matched to exp 025).
  Into each scaffold, plant 3 motifs (consensus k-mer of randomly
  chosen JASPAR vertebrate PWMs) at random non-overlapping positions.
"""

import os
import sys
import numpy as np

L = 200
SEED = 0
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "sequences_0.txt")
JASPAR = os.path.join(HERE, "..", "..", "data", "jaspar2024_vertebrates.jaspar")

BIN_PROBS = [
    [0.35, 0.15, 0.15, 0.35],  # GC=0.30
    [0.30, 0.20, 0.20, 0.30],  # GC=0.40
    [0.25, 0.25, 0.25, 0.25],  # GC=0.50
    [0.20, 0.30, 0.30, 0.20],  # GC=0.60
    [0.15, 0.35, 0.35, 0.15],  # GC=0.70
]
PER_BIN = 10_000
N_MOTIFS_PER_SEQ = 3
BASES = np.array(list("ACGT"))


def parse_jaspar(path):
    motifs = []
    with open(path) as f:
        lines = f.read().strip().split("\n")
    i = 0
    while i < len(lines):
        if lines[i].startswith(">"):
            header = lines[i][1:].split()
            name = header[1] if len(header) > 1 else header[0]
            mat = []
            for j in range(4):
                row = lines[i + 1 + j].split("[")[1].split("]")[0].split()
                mat.append([float(x) for x in row])
            mat = np.array(mat)  # (4, W)
            i += 5
            consensus = "".join(BASES[mat.argmax(axis=0)])
            if len(consensus) >= 5 and len(consensus) <= 20:
                motifs.append(consensus)
        else:
            i += 1
    return motifs


def gen_scaffold(rng, probs):
    return list(BASES[rng.choice(4, size=L, p=probs)])


def plant(seq_chars, motifs, rng):
    """Plant N_MOTIFS_PER_SEQ motifs at random non-overlapping positions."""
    placed = []  # list of (start, end)
    for _ in range(N_MOTIFS_PER_SEQ):
        m = motifs[rng.integers(0, len(motifs))]
        w = len(m)
        for attempt in range(20):
            s = int(rng.integers(0, L - w))
            e = s + w
            if not any(not (e <= ps or s >= pe) for ps, pe in placed):
                for k, ch in enumerate(m):
                    seq_chars[s + k] = ch
                placed.append((s, e))
                break
    return seq_chars


def main():
    rng = np.random.default_rng(SEED)
    motifs = parse_jaspar(JASPAR)
    print(f"Loaded {len(motifs)} JASPAR motif consensuses "
          f"(W={min(len(m) for m in motifs)}-{max(len(m) for m in motifs)})",
          file=sys.stderr)

    seqs = []
    for i, probs in enumerate(BIN_PROBS):
        print(f"  bin {i}, target GC={(probs[1]+probs[2]):.2f}",
              file=sys.stderr)
        for _ in range(PER_BIN):
            s = gen_scaffold(rng, probs)
            s = plant(s, motifs, rng)
            seqs.append("".join(s))

    assert len(seqs) == 50_000
    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
