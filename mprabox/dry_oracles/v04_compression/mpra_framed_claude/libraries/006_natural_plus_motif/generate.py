"""Experiment 006: motifs embedded in NATURAL background.

50K natural genomic windows (200bp, same source as exp 002). Then for
each, with prob 1.0, insert 1-2 JASPAR vertebrate motif instances at
random positions, replacing the underlying genomic bases.

This tests whether motif augmentation adds value when the surrounding
context is natural (which exp 005 lacked).

Hypothesis: should beat exp 002 (pure natural, 0.480) because the model
sees stronger motif signal embedded in realistic context. Should beat
exp 005 (random+motif) because context is natural.

Generalization argument: this trains the model on "natural genome with
boosted motif content." Natural context teaches generalizable composition;
inserted motifs teach generalizable motif recognition. Both should
transfer across cell types using the same regulatory machinery.

If this DOES NOT beat exp 002, the implication is that natural genomic
DNA already contains enough motif density for the model to learn — adding
more is redundant or disruptive.
"""
import os
import re

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
L = 200
SEED = 0
N_INSERT_MIN = 1
N_INSERT_MAX = 2
PAD = 5

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GENOME = os.path.join(REPO_ROOT, "data", "hg38.fa")
JASPAR = os.path.join(REPO_ROOT, "data", "jaspar2024_vertebrates.jaspar")

PRIMARY_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
ALPHABET = np.array(list("ACGT"))


def parse_jaspar(path):
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
        rows = []
        for line in lines[1:5]:
            nums = re.findall(r"\d+\.?\d*", line)
            rows.append([float(x) for x in nums])
        pfm = np.array(rows, dtype=np.float64)
        if pfm.shape[0] != 4 or pfm.shape[1] == 0:
            continue
        pfm = pfm + 0.5
        pwm = pfm / pfm.sum(axis=0, keepdims=True)
        motifs.append(pwm)
    return motifs


def sample_motif(pwm, rng):
    w = pwm.shape[1]
    idx = np.empty(w, dtype=np.int8)
    for j in range(w):
        col = pwm[:, j]
        idx[j] = rng.choice(4, p=col / col.sum())
    return idx


def main():
    fa = Fasta(GENOME, sequence_always_upper=True)
    chrom_lens = {c: len(fa[c]) for c in PRIMARY_CHROMS}
    chroms = np.array(PRIMARY_CHROMS)
    weights = np.array([chrom_lens[c] for c in PRIMARY_CHROMS], dtype=np.float64)
    weights /= weights.sum()

    motifs = parse_jaspar(JASPAR)
    print(f"loaded {len(motifs)} motifs")

    rng = np.random.default_rng(SEED)
    base_idx = {b: i for i, b in enumerate("ACGT")}

    seqs = []
    while len(seqs) < N_SEQ:
        c = rng.choice(chroms, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        arr = np.array([base_idx[b] for b in s], dtype=np.int8)

        k = int(rng.integers(N_INSERT_MIN, N_INSERT_MAX + 1))
        choice = rng.choice(len(motifs), size=k, replace=False)
        occupied = []
        for mi in choice:
            pwm = motifs[mi]
            w = pwm.shape[1]
            if w + 2 * PAD >= L:
                continue
            for _ in range(20):
                pos = int(rng.integers(PAD, L - w - PAD))
                if all(pos + w + PAD <= s_o or pos >= e_o + PAD for (s_o, e_o) in occupied):
                    arr[pos:pos + w] = sample_motif(pwm, rng)
                    occupied.append((pos, pos + w))
                    break
        seqs.append("".join(ALPHABET[arr]))
        if len(seqs) % 10_000 == 0:
            print(f"  {len(seqs)} sequences")

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    assert len(seqs) == N_SEQ
    print(f"wrote {N_SEQ} sequences to {out}")


if __name__ == "__main__":
    main()
