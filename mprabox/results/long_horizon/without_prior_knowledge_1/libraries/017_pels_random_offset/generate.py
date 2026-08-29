"""Experiment 017 — pELS with random within-element offset.

50K unique pELS (no replacement). For each cCRE, the 200bp
window center is sampled uniformly from [start, end] of the
cCRE (rather than the central midpoint). This exposes the
model to varied positional views of each element.

For cCREs >= 200bp, the window is a random 200bp sub-slice
overlapping the cCRE. For shorter cCREs, the window includes
the cCRE plus a random amount of flanking on one side.

Tests whether central-200bp extraction is overly restrictive
(model only ever sees one slice per element) vs whether
positional variation is just noise. Unlike RC (exp 016), this
adds genuine sequence diversity per draw without reducing pool
size.
"""
from __future__ import annotations

import os
import sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXP002_DIR = os.path.join(ROOT, "libraries", "002_encode_ccre")
sys.path.insert(0, EXP002_DIR)
from generate import (  # type: ignore  # noqa: E402
    GENOME_2BIT,
    SEQ_LEN,
    HALF,
    ALPHABET,
    CCRE_BED,
)
from twobitreader import TwoBitFile

N_SEQS = 50_000
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


def extract_random_window(
    rng: np.random.Generator,
    genome: TwoBitFile,
    chrom: str,
    start: int,
    end: int,
) -> str | None:
    # Sample window center uniformly within [start, end] inclusive
    center = int(rng.integers(start, end + 1))
    win_start = center - HALF
    win_end = win_start + SEQ_LEN
    try:
        chrom_seq = genome[chrom]
        chrom_len = len(chrom_seq)
    except KeyError:
        return None
    if win_start < 0 or win_end > chrom_len:
        return None
    seq = str(chrom_seq[win_start:win_end]).upper()
    if len(seq) != SEQ_LEN:
        return None
    if not set(seq) <= ALPHABET:
        return None
    return seq


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
        seq = extract_random_window(rng, genome, chrom, start, end)
        if seq is None:
            continue
        out.append(seq)
    rng.shuffle(out)
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
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: 50K pELS at random within-element offset...")
        seqs = generate(seed, pool, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
