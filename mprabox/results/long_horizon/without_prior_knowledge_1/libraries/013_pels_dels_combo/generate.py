"""Experiment 013 — pELS + dELS combined library.

25K pELS + 25K dELS, sampled (no replacement) from their pools,
shuffled together. Same central-200bp extraction as exp 002.

Tests whether the two best single-class libraries combine
additively. pELS leads on general/high-baseline evals; dELS leads
on motif-rewarding evals (07/13). If the model can learn both
sets of features, combo > pELS-only and > dELS-only.
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
N_SEQS = 2 * N_PER_CLASS
CLASSES = ("pELS", "dELS")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_classes(targets: tuple[str, ...]) -> dict[str, list[tuple[str, int, int]]]:
    out: dict[str, list[tuple[str, int, int]]] = {t: [] for t in targets}
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            label = parts[-1]
            if label in out:
                out[label].append((parts[0], int(parts[1]), int(parts[2])))
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


def generate(seed: int, by_class: dict[str, list], genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    for cls in CLASSES:
        out.extend(sample_class(rng, by_class[cls], N_PER_CLASS, genome))
    rng.shuffle(out)
    return out


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print(f"loading {CLASSES} cCREs...")
    by_class = load_classes(CLASSES)
    for c in CLASSES:
        print(f"  {c}: {len(by_class[c])} cCREs")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: 25K pELS + 25K dELS...")
        seqs = generate(seed, by_class, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
