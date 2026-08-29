"""Experiment 022 — pELS top-50K-shortest cCREs.

From the 249K pELS pool, sort by cCRE length and take the
50K SHORTEST. Threshold: ≤186bp. Same central-200bp
extraction. Three seeds.

Validates length-as-quality direction. With exp 021 already
showing length≥336bp drops -0.007 vs uniform, this tells
whether the loss is "long is bad" or "extremes are bad".
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
N_SELECT = 50_000
TARGET_CLASS = "pELS"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_class(target: str) -> list[tuple[str, int, int]]:
    out: list[tuple[str, int, int]] = []
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[-1] == target:
                out.append((parts[0], int(parts[1]), int(parts[2])))
    return out


def select_shortest(pool: list, n: int) -> list:
    pool_sorted = sorted(pool, key=lambda r: r[2] - r[1])
    return pool_sorted[:n]


def generate(seed: int, filtered: list, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    idx = rng.permutation(len(filtered))
    i = 0
    while len(out) < N_SEQS:
        if i >= len(idx):
            idx = np.concatenate([idx, rng.permutation(len(filtered))])
        chrom, start, end = filtered[int(idx[i])]
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
    print(f"loading {TARGET_CLASS} cCREs...")
    pool = load_class(TARGET_CLASS)
    print(f"  pool: {len(pool)} {TARGET_CLASS} cCREs")
    filtered = select_shortest(pool, N_SELECT)
    min_len = min(r[2] - r[1] for r in filtered)
    max_len = max(r[2] - r[1] for r in filtered)
    print(f"  filtered top-{N_SELECT} shortest: length {min_len}-{max_len}bp")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: 50K from filtered pELS-shortest pool...")
        seqs = generate(seed, filtered, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
