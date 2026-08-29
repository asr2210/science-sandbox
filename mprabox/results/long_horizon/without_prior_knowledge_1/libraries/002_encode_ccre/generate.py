"""Experiment 002 — natural human regulatory DNA from ENCODE SCREEN cCREs.

For each seed, sample 50,000 cCREs (class-balanced across 8 SCREEN classes:
dELS, pELS, PLS, CA, CA-CTCF, CA-H3K4me3, CA-TF, TF) and extract a 200-bp
window centered on each cCRE's midpoint from GRCh38. cCREs vary 100–500
bp; for short ones the window extends into flanking genomic sequence,
which is fine — flanking context is part of the regulatory landscape.

Sequences containing 'N' are rejected and the seed re-drawn. This is a
fair test of whether biology-aware genomic sequences clear the random
floor from exp 001.
"""
from __future__ import annotations

import os
import sys
import numpy as np
from twobitreader import TwoBitFile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = {"A", "C", "G", "T"}
PER_CLASS = N_SEQS // 8  # 6250 each across 8 SCREEN classes

CLASSES = ("dELS", "pELS", "PLS", "CA", "CA-CTCF", "CA-H3K4me3", "CA-TF", "TF")

CCRE_BED = os.path.join(ROOT, "data", "cCRE", "GRCh38-cCREs.bed")
GENOME_2BIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_ccres_by_class() -> dict[str, list[tuple[str, int, int]]]:
    by_class: dict[str, list[tuple[str, int, int]]] = {c: [] for c in CLASSES}
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom, start, end, label = parts[0], int(parts[1]), int(parts[2]), parts[-1]
            if label in by_class:
                by_class[label].append((chrom, start, end))
    return by_class


def extract_window(genome: TwoBitFile, chrom: str, start: int, end: int) -> str | None:
    midpoint = (start + end) // 2
    win_start = midpoint - HALF
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


def generate(seed: int, by_class: dict[str, list], genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out: list[str] = []
    for cls in CLASSES:
        pool = by_class[cls]
        idx = rng.permutation(len(pool))
        chosen = 0
        i = 0
        while chosen < PER_CLASS:
            if i >= len(idx):
                # extremely unlikely with 25K+ candidates per class, but reseed extension
                idx = np.concatenate([idx, rng.permutation(len(pool))])
            chrom, start, end = pool[idx[i]]
            i += 1
            seq = extract_window(genome, chrom, start, end)
            if seq is None:
                continue
            out.append(seq)
            chosen += 1
    rng.shuffle(out)  # mix classes so training batches see all types
    return out


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS, f"got {len(seqs)} seqs, expected {N_SEQS}"
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print("loading cCRE BED...")
    by_class = load_ccres_by_class()
    for c in CLASSES:
        print(f"  {c}: {len(by_class[c])} cCREs available")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"generating seed {seed}...")
        seqs = generate(seed, by_class, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
