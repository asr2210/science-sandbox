"""Experiment 008 — cCRE library with natural class proportions.

Sample 50,000 cCREs uniform-random from the full 2.35M cCRE pool
(no class balancing). Naturally yields ~62.6% dELS, ~10.6% pELS,
~10.5% CA, ~5.4% CA-CTCF, ~4.5% TF, ~3.4% CA-H3K4me3, ~2.0% PLS,
~1.1% CA-TF.

Tests whether dELS-only's gain (exp 007) is from "dELS specifically"
or from "natural class proportions" (which would also be ~62% dELS
with non-trivial fractions of other classes).
"""
from __future__ import annotations

import os
import sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXP002_DIR = os.path.join(ROOT, "libraries", "002_encode_ccre")
sys.path.insert(0, EXP002_DIR)
from generate import (  # type: ignore  # noqa: E402
    extract_window,
    GENOME_2BIT,
    SEQ_LEN,
    ALPHABET,
    CCRE_BED,
)
from twobitreader import TwoBitFile

N_SEQS = 50_000
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_all_ccres() -> list[tuple[str, int, int]]:
    out = []
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            out.append((chrom, start, end))
    return out


def generate(seed: int, pool: list, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    idx = rng.permutation(len(pool))
    i = 0
    while len(out) < N_SEQS:
        if i >= len(idx):
            idx = np.concatenate([idx, rng.permutation(len(pool))])
        chrom, start, end = pool[int(idx[i])]
        i += 1
        seq = extract_window(genome, chrom, start, end)
        if seq is None:
            continue
        out.append(seq)
    return out


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print("loading full cCRE BED (no class breakdown)...")
    pool = load_all_ccres()
    print(f"  pool: {len(pool)} cCREs")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: sampling 50K from full cCRE pool...")
        seqs = generate(seed, pool, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
