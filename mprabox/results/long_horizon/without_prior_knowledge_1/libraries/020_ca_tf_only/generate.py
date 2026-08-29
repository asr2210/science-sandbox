"""Experiment 020 — CA-TF only cCRE library.

50K x 200bp sampled WITH REPLACEMENT (pool is only ~26K, so
each element is used ~1.92x on average) from the CA-TF
(chromatin-accessible + TF-bound) cCRE class. Same
central-200bp extraction as exp 002.

CA-TF = DNase-accessible region with TF binding evidence (no
chromatin-mark evidence). Smallest SCREEN class.

Tests whether (i) CA-TF ranks above its constituent classes
(CA, TF), and (ii) whether 2x replication of high-quality
elements dominates the pool-diversity penalty established in
016.
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
TARGET_CLASS = "CA-TF"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_class(target: str) -> list[tuple[str, int, int]]:
    out: list[tuple[str, int, int]] = []
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[-1] == target:
                out.append((parts[0], int(parts[1]), int(parts[2])))
    return out


def generate(seed: int, pool: list, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    while len(out) < N_SEQS:
        n_needed = N_SEQS - len(out)
        batch_idx = rng.integers(0, len(pool), size=max(n_needed * 11 // 10, 1000))
        for i in batch_idx:
            chrom, start, end = pool[int(i)]
            seq = extract_window(genome, chrom, start, end)
            if seq is None:
                continue
            out.append(seq)
            if len(out) == N_SEQS:
                break
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
        print(f"seed {seed}: sampling 50K from {TARGET_CLASS} with replacement...")
        seqs = generate(seed, pool, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
