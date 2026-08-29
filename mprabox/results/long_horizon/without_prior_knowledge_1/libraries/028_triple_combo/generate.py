"""Experiment 028 — triple orthogonal-class combo.

16,667 pELS + 16,667 CA-H3K4me3 + 16,666 CA-CTCF = 50,000.
All three confirmed orthogonal evidence types: transcription-
flanking enhancer (pELS), active-promoter chromatin mark
(CA-H3K4me3), CTCF-bound chromatin (CA-CTCF).

Tests whether stacking orthogonal classes compounds the
diversity gain (026's +0.022 over pELS) or saturates at two
classes.
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

CLASSES = ["pELS", "CA-H3K4me3", "CA-CTCF"]
N_PER_CLASS = [16_667, 16_667, 16_666]
N_SEQS = sum(N_PER_CLASS)
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


def generate(seed: int, pools: list, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    combined: list[str] = []
    for pool, n in zip(pools, N_PER_CLASS):
        combined.extend(sample_class(rng, pool, n, genome))
    rng.shuffle(combined)
    return combined


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS, (len(seqs), N_SEQS)
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    pools = []
    for cls, n in zip(CLASSES, N_PER_CLASS):
        print(f"loading {cls} cCREs...")
        p = load_class(cls)
        print(f"  {cls}: {len(p)} cCREs (sampling {n})")
        pools.append(p)
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: triple combo {N_PER_CLASS}, shuffled...")
        seqs = generate(seed, pools, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
