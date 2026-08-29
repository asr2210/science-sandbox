"""Experiment 026 — pELS + CA-H3K4me3 combo (25K + 25K).

Top two single-class libraries: 012 pELS (mean=0.758) and
019 CA-H3K4me3 (mean=0.749). pELS = transcription-flanking
enhancer-like. CA-H3K4me3 = chromatin-accessible + active-
promoter mark. Different evidence types and genomic locations.

If union > 0.758, annotation-evidence diversification helps
generalization. If between or below, single-class beats simple
union.
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

N_PER_CLASS = 25_000
N_SEQS = 50_000
CLASS_A = "pELS"
CLASS_B = "CA-H3K4me3"
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
    a = sample_class(rng, pool_a, N_PER_CLASS, genome)
    b = sample_class(rng, pool_b, N_PER_CLASS, genome)
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
    print(f"  {CLASS_A}: {len(pool_a)} cCREs")
    print(f"loading {CLASS_B} cCREs...")
    pool_b = load_class(CLASS_B)
    print(f"  {CLASS_B}: {len(pool_b)} cCREs")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: 25K {CLASS_A} + 25K {CLASS_B}, shuffled...")
        seqs = generate(seed, pool_a, pool_b, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
