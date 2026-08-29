"""Experiment 005: synthetic motif library (JASPAR PWMs embedded in random).

For each sequence:
  - draw a uniform random 200bp background
  - pick K=3 distinct JASPAR vertebrate motifs
  - sample one instance of each motif from its PWM
  - insert at random positions (non-overlapping)

Hypothesis test: does explicit motif coverage (with synthetic context)
beat natural sequences with implicit motifs? Also: does this lift eval_08?

Generalization argument: JASPAR vertebrate motifs are the TF-binding
vocabulary that drives transcription in *any* mammalian cell type. A
model that learns to recognize them should transfer across cell types
that differ in *which* TFs are expressed (changes the importance of each
motif) but not in *what each motif looks like*.

Risk: random backgrounds may have unrealistic flanking dinucleotide stats
that bias the model. Mitigated by using neutral-GC (40% GC) random.
"""
import os
import re

import numpy as np

N_SEQ = 50_000
L = 200
SEED = 0
K_MOTIFS = 3  # motifs per sequence
PAD = 5

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
JASPAR = os.path.join(REPO_ROOT, "data", "jaspar2024_vertebrates.jaspar")

# Slightly AT-rich background (40% GC, closer to genomic non-coding)
GC_FRACTION = 0.40
BG_P = np.array(
    [(1 - GC_FRACTION) / 2, GC_FRACTION / 2, GC_FRACTION / 2, (1 - GC_FRACTION) / 2]
)
ALPHABET = np.array(list("ACGT"))


def parse_jaspar(path):
    """Return list of (name, pwm) where pwm is shape (4, w) normalized."""
    motifs = []
    with open(path) as f:
        text = f.read()
    entries = text.strip().split("\n>")
    for i, e in enumerate(entries):
        if not e:
            continue
        if i == 0 and e.startswith(">"):
            e = e[1:]
        lines = e.strip().split("\n")
        header = lines[0]
        name = header.split()[0]
        rows = []
        for line in lines[1:5]:
            nums = re.findall(r"\d+\.?\d*", line)
            rows.append([float(x) for x in nums])
        # rows is [A, C, G, T]
        pfm = np.array(rows, dtype=np.float64)
        if pfm.shape[0] != 4 or pfm.shape[1] == 0:
            continue
        # normalize with pseudocount
        pfm = pfm + 0.5
        pwm = pfm / pfm.sum(axis=0, keepdims=True)
        motifs.append((name, pwm))
    return motifs


def sample_motif_instance(pwm, rng):
    """Sample a sequence from the PWM (column-wise multinomial)."""
    w = pwm.shape[1]
    idx = np.array(
        [rng.choice(4, p=pwm[:, j] / pwm[:, j].sum()) for j in range(w)],
        dtype=np.int8,
    )
    return idx


def main():
    motifs = parse_jaspar(JASPAR)
    print(f"loaded {len(motifs)} motifs")
    rng = np.random.default_rng(SEED)

    seqs = []
    for n in range(N_SEQ):
        bg = rng.choice(4, size=L, p=BG_P).astype(np.int8)
        # pick K distinct motifs
        choice = rng.choice(len(motifs), size=K_MOTIFS, replace=False)
        # try to place non-overlapping
        occupied = []  # list of (start, end)
        for mi in choice:
            _, pwm = motifs[mi]
            w = pwm.shape[1]
            if w + 2 * PAD >= L:
                continue
            # find a valid start
            for _ in range(20):
                start = int(rng.integers(PAD, L - w - PAD))
                end = start + w
                if all(end + PAD <= s or start >= e + PAD for (s, e) in occupied):
                    inst = sample_motif_instance(pwm, rng)
                    bg[start:end] = inst
                    occupied.append((start, end))
                    break
        seqs.append("".join(ALPHABET[bg]))
        if (n + 1) % 10_000 == 0:
            print(f"  {n+1} sequences")

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    assert len(seqs) == N_SEQ
    assert all(len(s) == L for s in seqs)
    print(f"wrote {N_SEQ} sequences to {out}")


if __name__ == "__main__":
    main()
