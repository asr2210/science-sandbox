#!/usr/bin/env python3
from __future__ import annotations

import random
from pathlib import Path

from pyfaidx import Fasta


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "library" / "sequences.txt"
SEED = 20260629
LENGTH = 200
TARGET = 50_000

CANONICAL = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
BED_FILES = {
    "PLS": DATA / "GRCh38-cCREs.PLS.bed",
    "pELS": DATA / "GRCh38-cCREs.pELS.bed",
    "dELS": DATA / "GRCh38-cCREs.dELS.bed",
    "CA-CTCF": DATA / "GRCh38-cCREs.CA-CTCF.bed",
    "CA": DATA / "GRCh38-cCREs.CA.bed",
}

NATIVE_QUOTAS = {
    "dELS": 15_000,
    "pELS": 6_000,
    "PLS": 5_000,
    "CA-CTCF": 3_000,
    "CA": 3_000,
}

JITTER_QUOTAS = {
    "dELS": 2_500,
    "pELS": 1_200,
    "PLS": 800,
    "CA-CTCF": 800,
    "CA": 700,
}

BG_QUOTA = 4_000
SHUFFLE_QUOTA = 4_000
SYNTH_QUOTA = 4_000


RC = str.maketrans("ACGT", "TGCA")

MOTIFS = {
    "SP1": ["GGGCGG", "CCGCCC", "GGGCGGG"],
    "AP1": ["TGACTCA", "TGAGTCA"],
    "CREB": ["TGACGTCA"],
    "EBOX": ["CACGTG", "CAGCTG", "CACCTG"],
    "ETS": ["CCGGAAGT", "CAGGAAGT"],
    "GATA": ["AGATAA", "TGATAA"],
    "FOXA": ["TGTTTAC", "TRTTTAC".replace("R", "A")],
    "HNF": ["AGGTCA", "GGGTCA"],
    "NFY": ["CCAAT"],
    "NFKB": ["GGGACTTTCC", "GGGAATTTCC"],
    "IRF": ["GAAAGTGAA", "GAAACCGAA"],
    "STAT": ["TTCCCGGAA", "TTCCTGGAA"],
    "CTCF": ["CCGCGAGGGGGCAG", "CCGCGTGGCGGCAG"],
    "SOX": ["CTTTGTT", "AACAAAG"],
    "POU": ["ATGCAAAT"],
    "MEF2": ["CTAAAAATAG", "CTATTTTTAG"],
    "TATA": ["TATAAA"],
    "RUNX": ["TGTGGT", "TGCGGT"],
    "TEAD": ["CATTCCA", "GGAATGT"],
    "SMAD": ["GTCTAGAC", "GTCT"],
}

GRAMMARS = [
    ("promoter_cpg", ["SP1", "SP1", "NFY", "ETS", "TATA"]),
    ("housekeeping", ["SP1", "ETS", "EBOX", "CREB"]),
    ("enhancer_signal", ["AP1", "ETS", "RUNX", "NFKB"]),
    ("immune", ["NFKB", "IRF", "STAT", "AP1"]),
    ("liver", ["HNF", "FOXA", "CEBP", "HNF"]),
    ("neural", ["SOX", "POU", "EBOX", "MEF2"]),
    ("insulator", ["CTCF", "CTCF", "SP1"]),
    ("developmental", ["TEAD", "SMAD", "AP1", "SOX"]),
    ("minimal", ["TATA", "SP1", "CREB"]),
]
MOTIFS["CEBP"] = ["TTGCGCAA", "ATTGCGCAAT"]


def load_intervals() -> dict[str, list[tuple[str, int, int]]]:
    intervals: dict[str, list[tuple[str, int, int]]] = {}
    canon = set(CANONICAL)
    for label, path in BED_FILES.items():
        rows: list[tuple[str, int, int]] = []
        with path.open() as fh:
            for line in fh:
                if not line.strip() or line.startswith("#"):
                    continue
                chrom, start, end, *_ = line.rstrip("\n").split("\t")
                if chrom not in canon:
                    continue
                rows.append((chrom, int(start), int(end)))
        intervals[label] = rows
    return intervals


def clean(seq: str) -> str:
    return seq.upper()


def passes(seq: str) -> bool:
    if len(seq) != LENGTH:
        return False
    if any(c not in "ACGT" for c in seq):
        return False
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    if gc < 0.20 or gc > 0.82:
        return False
    for base in "ACGT":
        if base * 18 in seq:
            return False
    return True


def fetch(fa: Fasta, chrom: str, start: int, end: int, chrom_lens: dict[str, int]) -> str | None:
    if start < 0 or end > chrom_lens[chrom] or end - start != LENGTH:
        return None
    seq = clean(str(fa[chrom][start:end]))
    return seq if passes(seq) else None


def ccre_window(
    fa: Fasta,
    interval: tuple[str, int, int],
    chrom_lens: dict[str, int],
    rng: random.Random,
    jitter: bool,
) -> str | None:
    chrom, start, end = interval
    center = (start + end) // 2
    if jitter:
        center += rng.randint(-180, 180)
    left = center - LENGTH // 2
    seq = fetch(fa, chrom, left, left + LENGTH, chrom_lens)
    if seq and rng.random() < 0.5:
        seq = seq.translate(RC)[::-1]
    return seq


def add_unique(seqs: list[str], seen: set[str], seq: str | None) -> bool:
    if seq is None or seq in seen:
        return False
    seen.add(seq)
    seqs.append(seq)
    return True


def fill_from_ccres(
    seqs: list[str],
    seen: set[str],
    fa: Fasta,
    intervals: dict[str, list[tuple[str, int, int]]],
    chrom_lens: dict[str, int],
    quotas: dict[str, int],
    rng: random.Random,
    jitter: bool,
) -> None:
    for label, quota in quotas.items():
        pool = intervals[label]
        made = 0
        attempts = 0
        while made < quota:
            attempts += 1
            if attempts > quota * 100:
                raise RuntimeError(f"too many failed attempts for {label}")
            seq = ccre_window(fa, rng.choice(pool), chrom_lens, rng, jitter)
            if add_unique(seqs, seen, seq):
                made += 1


def random_genomic(
    fa: Fasta,
    chrom_lens: dict[str, int],
    rng: random.Random,
) -> str | None:
    weights = [chrom_lens[c] for c in CANONICAL]
    chrom = rng.choices(CANONICAL, weights=weights, k=1)[0]
    start = rng.randint(0, chrom_lens[chrom] - LENGTH)
    seq = fetch(fa, chrom, start, start + LENGTH, chrom_lens)
    if seq and rng.random() < 0.5:
        seq = seq.translate(RC)[::-1]
    return seq


def shuffled(seq: str, rng: random.Random) -> str:
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)


def background(gc: float, rng: random.Random) -> list[str]:
    p_gc = gc / 2
    p_at = (1 - gc) / 2
    alphabet = ["A", "C", "G", "T"]
    weights = [p_at, p_gc, p_gc, p_at]
    return rng.choices(alphabet, weights=weights, k=LENGTH)


def place_motif(seq: list[str], motif: str, pos: int) -> None:
    seq[pos : pos + len(motif)] = list(motif)


def synthetic(rng: random.Random) -> str:
    name, families = rng.choice(GRAMMARS)
    if name in {"promoter_cpg", "housekeeping", "minimal"}:
        gc = rng.uniform(0.52, 0.72)
    elif name == "insulator":
        gc = rng.uniform(0.45, 0.65)
    else:
        gc = rng.uniform(0.34, 0.58)
    seq = background(gc, rng)

    if name in {"promoter_cpg", "minimal"} and rng.random() < 0.75:
        place_motif(seq, "TATAAA", rng.randint(35, 70))

    cursor = rng.randint(12, 30)
    for family in families:
        motif = rng.choice(MOTIFS[family])
        if rng.random() < 0.35:
            motif = motif.translate(RC)[::-1]
        if cursor + len(motif) >= LENGTH - 10:
            cursor = rng.randint(10, 80)
        pos = cursor + rng.randint(0, 18)
        place_motif(seq, motif, pos)
        cursor = pos + len(motif) + rng.choice([4, 6, 8, 10, 12, 16, 24, 32])

    # Add controlled homotypic clusters in a minority of sequences.
    if rng.random() < 0.35:
        family = rng.choice(families)
        motif = rng.choice(MOTIFS[family])
        pos = rng.randint(95, 175 - len(motif))
        for _ in range(rng.choice([2, 3])):
            if pos + len(motif) < LENGTH:
                place_motif(seq, motif, pos)
            pos += len(motif) + rng.choice([5, 8, 13, 21])

    return "".join(seq)


def main() -> None:
    rng = random.Random(SEED)
    fa = Fasta(str(DATA / "hg38.fa"), sequence_always_upper=True)
    chrom_lens = {chrom: len(fa[chrom]) for chrom in CANONICAL}
    intervals = load_intervals()

    seqs: list[str] = []
    seen: set[str] = set()

    fill_from_ccres(seqs, seen, fa, intervals, chrom_lens, NATIVE_QUOTAS, rng, jitter=False)
    fill_from_ccres(seqs, seen, fa, intervals, chrom_lens, JITTER_QUOTAS, rng, jitter=True)

    made = 0
    while made < BG_QUOTA:
        if add_unique(seqs, seen, random_genomic(fa, chrom_lens, rng)):
            made += 1

    ccre_source = seqs[: sum(NATIVE_QUOTAS.values()) + sum(JITTER_QUOTAS.values())]
    made = 0
    while made < SHUFFLE_QUOTA:
        candidate = shuffled(rng.choice(ccre_source), rng)
        if passes(candidate) and add_unique(seqs, seen, candidate):
            made += 1

    made = 0
    while made < SYNTH_QUOTA:
        candidate = synthetic(rng)
        if passes(candidate) and add_unique(seqs, seen, candidate):
            made += 1

    if len(seqs) != TARGET:
        raise RuntimeError(f"expected {TARGET}, got {len(seqs)}")

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w") as fh:
        for seq in seqs:
            fh.write(seq + "\n")

    print(f"wrote {len(seqs)} sequences to {OUT}")


if __name__ == "__main__":
    main()
