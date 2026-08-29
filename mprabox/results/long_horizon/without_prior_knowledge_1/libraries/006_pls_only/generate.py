"""Experiment 006 — PLS (promoter-like) cCRE library only.

Sample 50,000 sequences from the 47,532-element PLS pool, with
replacement. Each sequence: central 200-bp window from GRCh38.

Tests whether the cCRE motif-rewarding gain comes from PLS specifically
or from the diversity of element classes.

Three seeds give three independent draws (with-replacement) so each
seed sees a slightly different per-element multiplicity.
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


def generate(seed: int, pls_pool: list, genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    # iterate, sampling cCREs with replacement, until we have 50K valid
    while len(out) < N_SEQS:
        n_needed = N_SEQS - len(out)
        # batch-sample to amortize Python overhead
        batch_idx = rng.integers(0, len(pls_pool), size=max(n_needed * 11 // 10, 1000))
        for i in batch_idx:
            chrom, start, end = pls_pool[int(i)]
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
    print("loading cCRE BED, extracting PLS...")
    by_class = load_ccres_by_class()
    pls_pool = by_class["PLS"]
    print(f"  PLS pool: {len(pls_pool)} cCREs")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: sampling 50K from PLS with replacement...")
        seqs = generate(seed, pls_pool, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
