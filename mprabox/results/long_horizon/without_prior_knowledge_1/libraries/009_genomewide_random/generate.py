"""Experiment 009 — genome-wide random 200bp windows.

Sample 50,000 uniform-random 200bp windows from hg38 main chromosomes
(autosomes + chrX + chrY; exclude chrM and unplaced/alt contigs).
Skip windows containing any N (assembly gaps). No cCRE annotation
used at all — most windows will be intergenic non-regulatory.

Tests whether the cCRE annotation specifically helps the model, or
whether real human DNA in any region is enough.
"""
from __future__ import annotations

import os
import numpy as np
from twobitreader import TwoBitFile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GENOME_2BIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

N_SEQS = 50_000
SEQ_LEN = 200
ALPHABET = {"A", "C", "G", "T"}

MAIN_CHROMS = (
    "chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8",
    "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15",
    "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22",
    "chrX", "chrY",
)


def chrom_lengths(genome: TwoBitFile) -> list[tuple[str, int]]:
    return [(c, len(genome[c])) for c in MAIN_CHROMS]


def sample_window(rng: np.random.Generator, lens: list[tuple[str, int]],
                  cum: np.ndarray, total: int) -> tuple[str, int]:
    pos = int(rng.integers(0, total))
    i = int(np.searchsorted(cum, pos, side="right"))
    chrom, _ = lens[i]
    offset = pos - (cum[i - 1] if i > 0 else 0)
    return chrom, int(offset)


def generate(seed: int, genome: TwoBitFile, lens: list[tuple[str, int]]) -> list[str]:
    rng = np.random.default_rng(seed)
    sampleable = [(c, L - SEQ_LEN) for c, L in lens]
    cum = np.cumsum([L for _, L in sampleable])
    total = int(cum[-1])
    out: list[str] = []
    chrom_cache: dict[str, object] = {}
    while len(out) < N_SEQS:
        chrom, start = sample_window(rng, sampleable, cum, total)
        if chrom not in chrom_cache:
            chrom_cache[chrom] = genome[chrom]
        seq = str(chrom_cache[chrom][start:start + SEQ_LEN]).upper()
        if len(seq) != SEQ_LEN:
            continue
        if not set(seq) <= ALPHABET:
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
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    lens = chrom_lengths(genome)
    total = sum(L for _, L in lens)
    print(f"  main chroms: {len(lens)}, total bp: {total:,}")
    for seed in (0, 1, 2):
        print(f"seed {seed}: sampling 50K random 200bp windows...")
        seqs = generate(seed, genome, lens)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
