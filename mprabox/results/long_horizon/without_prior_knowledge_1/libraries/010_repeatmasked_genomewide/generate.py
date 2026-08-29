"""Experiment 010 — repeat-masked genome-wide random.

Same uniform-random sampling from hg38 main chromosomes as exp 009,
but reject windows that are >50% soft-masked (repeat content from
RepeatMasker + Tandem Repeats Finder, embedded as lowercase in
hg38.2bit). Reject windows containing N.

Tests whether repeats are the active distractor that made exp 009
underperform uniform random ACGT.
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
MAX_REPEAT_FRAC = 0.5

MAIN_CHROMS = (
    "chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8",
    "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15",
    "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22",
    "chrX", "chrY",
)


def chrom_lengths(genome: TwoBitFile) -> list[tuple[str, int]]:
    return [(c, len(genome[c]) - SEQ_LEN) for c in MAIN_CHROMS]


def generate(seed: int, genome: TwoBitFile, lens: list[tuple[str, int]]) -> list[str]:
    rng = np.random.default_rng(seed)
    cum = np.cumsum([L for _, L in lens])
    total = int(cum[-1])
    out: list[str] = []
    cache: dict[str, object] = {}
    n_tries = 0
    n_n = 0
    n_repeat = 0
    while len(out) < N_SEQS:
        n_tries += 1
        pos = int(rng.integers(0, total))
        i = int(np.searchsorted(cum, pos, side="right"))
        chrom = lens[i][0]
        offset = pos - (cum[i - 1] if i > 0 else 0)
        if chrom not in cache:
            cache[chrom] = genome[chrom]
        raw = str(cache[chrom][offset:offset + SEQ_LEN])
        if len(raw) != SEQ_LEN:
            continue
        upper = raw.upper()
        if not set(upper) <= ALPHABET:
            n_n += 1
            continue
        n_lower = sum(1 for c in raw if c.islower())
        if n_lower / SEQ_LEN > MAX_REPEAT_FRAC:
            n_repeat += 1
            continue
        out.append(upper)
    print(f"  tries={n_tries}, N-rejected={n_n}, repeat-rejected={n_repeat}, kept={len(out)}")
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
    print(f"  main chroms: {len(lens)}, sampleable bp: {sum(L for _, L in lens):,}")
    for seed in (0, 1, 2):
        print(f"seed {seed}: sampling 50K repeat-masked windows (max {int(MAX_REPEAT_FRAC*100)}% repeat)...")
        seqs = generate(seed, genome, lens)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
