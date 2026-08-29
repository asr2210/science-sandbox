"""Experiment 023 — pELS with 1% sequence mutation noise.

50K unique pELS (no replacement), central-200bp extraction.
Then for each sequence, randomly substitute 1% of bases
(= 2 substitutions per 200bp). Three seeds — each draws a
different mutation pattern per sequence.

Tests whether mild sequence-noise injection (the standard
DL augmentation when label-preserving transformations are
unavailable) improves generalization over clean cCREs. The
oracle in prepare.py recomputes labels from the mutated
sequences, so supervision matches input.
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
TARGET_CLASS = "pELS"
MUT_RATE = 0.01  # 1% — about 2 substitutions per 200bp
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BASES = np.array(["A", "C", "G", "T"])


def load_class(target: str) -> list[tuple[str, int, int]]:
    out: list[tuple[str, int, int]] = []
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[-1] == target:
                out.append((parts[0], int(parts[1]), int(parts[2])))
    return out


def mutate(seq: str, rng: np.random.Generator) -> str:
    arr = np.array(list(seq))
    n_mut = max(1, int(round(MUT_RATE * len(arr))))
    positions = rng.choice(len(arr), size=n_mut, replace=False)
    for p in positions:
        # pick a different base
        choices = BASES[BASES != arr[p]]
        arr[p] = rng.choice(choices)
    return "".join(arr.tolist())


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
        seq = mutate(seq, rng)
        out.append(seq)
    return out


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print(f"loading {TARGET_CLASS} cCREs...")
    pool = load_class(TARGET_CLASS)
    print(f"  pool: {len(pool)} {TARGET_CLASS} cCREs")
    print(f"mutation rate: {MUT_RATE} ({int(round(MUT_RATE * SEQ_LEN))} subs/seq)")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: 50K pELS with 1% mutations...")
        seqs = generate(seed, pool, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
