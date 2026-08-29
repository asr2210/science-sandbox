"""Experiment 030 (FINAL) — 30K pELS + 20K CA-H3K4me3.

Ratio-bias test on the optimal combo (026 = 25K + 25K =
0.780). pELS is the stronger single class (0.758 vs 0.749);
biasing the mix toward it tests whether stronger-parent depth
further improves performance.

If 030 > 026: pELS depth dominates within the orthogonal-
combo formula.
If 030 ≈ 026: the 25/25 split is robust to small ratio
changes.
If 030 < 026: balanced mixing matters; reducing the partner
below 25K starves the orthogonal-evidence contribution.
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

CLASS_A = "pELS"
CLASS_B = "CA-H3K4me3"
N_A = 30_000
N_B = 20_000
N_SEQS = N_A + N_B
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_class(target: str) -> list[tuple[str, int, int]]:
    out: list[tuple[str, int, int]] = []
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[-1] == target:
                out.append((parts[0], int(parts[1]), int(parts[2])))
    return out


def sample_class(rng: np.random.Generator, pool: list, n: int, genome: TwoBitFile) -> list[str]:
    out: list[str] = []
    idx = rng.permutation(len(pool))
    i = 0
    while len(out) < n:
        if i >= len(idx):
            idx = np.concatenate([idx, rng.permutation(len(pool))])
        chrom, start, end = pool[int(idx[i])]
        i += 1
        seq = extract_window(genome, chrom, start, end)
        if seq is None:
            continue
        out.append(seq)
    return out


def generate(seed: int, pool_a: list, pool_b: list, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    a = sample_class(rng, pool_a, N_A, genome)
    b = sample_class(rng, pool_b, N_B, genome)
    combined = a + b
    rng.shuffle(combined)
    return combined


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print(f"loading {CLASS_A} cCREs...")
    pool_a = load_class(CLASS_A)
    print(f"  {CLASS_A}: {len(pool_a)} cCREs (sampling {N_A})")
    print(f"loading {CLASS_B} cCREs...")
    pool_b = load_class(CLASS_B)
    print(f"  {CLASS_B}: {len(pool_b)} cCREs (sampling {N_B})")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: {N_A} {CLASS_A} + {N_B} {CLASS_B}, shuffled...")
        seqs = generate(seed, pool_a, pool_b, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
