"""Experiment 005 — 50/50 mixture of cCRE-derived and uniform-random.

Per seed:
- 25,000 cCRE-derived sequences (class-balanced, central 200 bp from
  GRCh38, sampled from ENCODE SCREEN cCREs)
- 25,000 uniform-random ACGT sequences

Mix and shuffle. Tests whether biology and composition coverage are
additive — does the mixture beat both pure libraries?

Generation uses the same seed for both halves; results are still
deterministic per seed.
"""
from __future__ import annotations

import os
import sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

EXP002_DIR = os.path.join(ROOT, "libraries", "002_encode_ccre")
sys.path.insert(0, EXP002_DIR)
from generate import (  # type: ignore  # noqa: E402
    load_ccres_by_class,
    extract_window,
    GENOME_2BIT,
    SEQ_LEN,
    ALPHABET as CCRE_ALPHABET,
)
from twobitreader import TwoBitFile

N_SEQS = 50_000
N_CCRE = 25_000
N_RAND = 25_000
PER_CLASS_CCRE = N_CCRE // 8  # 3,125 per class
ALPHABET = CCRE_ALPHABET  # {"A","C","G","T"}
RAND_ALPHABET = np.array(list("ACGT"))
CLASSES = ("dELS", "pELS", "PLS", "CA", "CA-CTCF", "CA-H3K4me3", "CA-TF", "TF")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def gen_ccre_half(seed: int, by_class: dict, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    for cls in CLASSES:
        pool = by_class[cls]
        idx = rng.permutation(len(pool))
        chosen, i = 0, 0
        while chosen < PER_CLASS_CCRE:
            if i >= len(idx):
                idx = np.concatenate([idx, rng.permutation(len(pool))])
            chrom, start, end = pool[idx[i]]
            i += 1
            seq = extract_window(genome, chrom, start, end)
            if seq is None:
                continue
            out.append(seq)
            chosen += 1
    return out


def gen_random_half(seed: int) -> list[str]:
    # use a different RNG stream so the two halves are independent
    rng = np.random.default_rng(seed + 100_000)
    idx = rng.integers(0, 4, size=(N_RAND, SEQ_LEN), dtype=np.uint8)
    chars = RAND_ALPHABET[idx]
    return ["".join(row) for row in chars]


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS, f"got {len(seqs)} seqs, expected {N_SEQS}"
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print("loading cCRE BED...")
    by_class = load_ccres_by_class()
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: cCRE half...")
        ccre_half = gen_ccre_half(seed, by_class, genome)
        print(f"  cCRE half: {len(ccre_half)}")
        rand_half = gen_random_half(seed)
        print(f"  random half: {len(rand_half)}")
        combined = ccre_half + rand_half
        # mix so training batches see both types
        shuffler = np.random.default_rng(seed + 500_000)
        order = shuffler.permutation(len(combined))
        combined = [combined[i] for i in order]
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(combined, out)
        print(f"  wrote {out}: {len(combined)} seqs")
