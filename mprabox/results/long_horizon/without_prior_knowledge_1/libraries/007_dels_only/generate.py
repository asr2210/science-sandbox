"""Experiment 007 — dELS (distal enhancer-like) cCRE library only.

50K x 200bp sampled (without replacement, pool is 1.47M) from the
dELS class. Tests whether single-class collapse seen in PLS-only
(exp 006) is universal or PLS-specific.
"""
from __future__ import annotations

import os
import sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXP002_DIR = os.path.join(ROOT, "libraries", "002_encode_ccre")
sys.path.insert(0, EXP002_DIR)
from generate import (  # type: ignore  # noqa: E402
    load_ccres_by_class,
    extract_window,
    GENOME_2BIT,
    SEQ_LEN,
    ALPHABET,
)
from twobitreader import TwoBitFile

N_SEQS = 50_000
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate(seed: int, dels_pool: list, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    idx = rng.permutation(len(dels_pool))
    i = 0
    while len(out) < N_SEQS:
        if i >= len(idx):
            idx = np.concatenate([idx, rng.permutation(len(dels_pool))])
        chrom, start, end = dels_pool[int(idx[i])]
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
    print("loading cCRE BED, extracting dELS...")
    by_class = load_ccres_by_class()
    pool = by_class["dELS"]
    print(f"  dELS pool: {len(pool)} cCREs")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: sampling 50K dELS...")
        seqs = generate(seed, pool, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
