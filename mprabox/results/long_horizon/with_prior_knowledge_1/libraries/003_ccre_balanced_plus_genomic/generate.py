#!/usr/bin/env python3
"""
Experiment 003 — cCRE class-balanced (40K) + random GENOMIC windows (10K).

Mechanism test: does the +0.030 eval_08 lift in exp 002 come from iid
randomness specifically, or from any out-of-cCRE sequence source?

cCRE backbone is sampled with the SAME RNG stream as exp 002, so the only
varying component between 002 and 003 is the 10K supplementary set.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

from twobitreader import TwoBitFile

REPO = Path(__file__).resolve().parents[2]
CCRE_BED = REPO / "data" / "cCRE" / "GRCh38-cCREs.bed"
GENOME = REPO / "data" / "genome" / "hg38.2bit"
OUT_DIR = Path(__file__).resolve().parent

WIN = 200
N_PER_CLASS = 8_000
N_GENOMIC = 10_000
N_TOTAL = 50_000
PRIMARY_CLASSES = ("PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3")
AUTOSOMES_PLUS_X = tuple(f"chr{i}" for i in range(1, 23)) + ("chrX",)
SEEDS = (0, 1, 2)

# Reject genomic windows whose midpoint falls within this many bp of any cCRE
# midpoint, to keep the genomic-background pool disjoint from the cCRE backbone.
CCRE_EXCLUSION_BP = 200


def primary_class(field6: str) -> str | None:
    head = field6.split(",", 1)[0]
    return head if head in PRIMARY_CLASSES else None


def load_cre_data() -> tuple[dict[str, list[tuple[str, int]]], dict[str, list[tuple[int, int]]]]:
    """Return (pools_by_class, intervals_by_chrom)."""
    pools: dict[str, list[tuple[str, int]]] = {c: [] for c in PRIMARY_CLASSES}
    intervals: dict[str, list[tuple[int, int]]] = {}
    with open(CCRE_BED) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            cls = primary_class(parts[5])
            if cls is not None:
                mid = (start + end) // 2
                pools[cls].append((chrom, mid))
            intervals.setdefault(chrom, []).append((start, end))
    # Sort intervals per chrom for binary-search overlap test
    for chrom in intervals:
        intervals[chrom].sort()
    for c in PRIMARY_CLASSES:
        print(f"  pool[{c}] = {len(pools[c]):,}", file=sys.stderr)
    return pools, intervals


def overlaps_cre(chrom: str, start: int, end: int, intervals: dict[str, list[tuple[int, int]]]) -> bool:
    """Return True if the window [start, end) overlaps any cCRE on chrom (with
    CCRE_EXCLUSION_BP padding)."""
    chr_intervals = intervals.get(chrom)
    if chr_intervals is None:
        return False
    s = start - CCRE_EXCLUSION_BP
    e = end + CCRE_EXCLUSION_BP
    # Linear scan with early termination — fine at 200K iterations per seed.
    # (Could replace with bisect-based search if it ever gets slow.)
    import bisect
    starts = [iv[0] for iv in chr_intervals]
    idx = bisect.bisect_right(starts, e)
    # Check intervals from idx-1 backward while their end > s
    i = idx - 1
    while i >= 0:
        iv_start, iv_end = chr_intervals[i]
        if iv_end <= s:
            break
        if iv_start < e and iv_end > s:
            return True
        i -= 1
    return False


def extract_window(genome: TwoBitFile, chrom: str, start: int, rng: random.Random) -> str | None:
    end = start + WIN
    chrom_len = len(genome[chrom])
    if start < 0 or end > chrom_len:
        return None
    seq = genome[chrom][start:end].upper()
    if len(seq) != WIN:
        return None
    n_count = seq.count("N")
    if n_count > WIN // 2:
        return None
    out = []
    for b in seq:
        out.append(b if b in "ACGT" else rng.choice("ACGT"))
    return "".join(out)


def sample_ccre(seed: int, pools: dict[str, list[tuple[str, int]]], genome: TwoBitFile) -> list[str]:
    """Identical RNG stream to exp 002's sample_ccre — keeps cCRE backbone byte-equal."""
    rng = random.Random(seed * 2 + 1)
    seqs: list[str] = []
    used: set[tuple[str, int]] = set()
    for cls in PRIMARY_CLASSES:
        pool = pools[cls]
        order = list(range(len(pool)))
        rng.shuffle(order)
        kept = 0
        for idx in order:
            if kept >= N_PER_CLASS:
                break
            chrom, mid = pool[idx]
            key = (chrom, mid)
            if key in used:
                continue
            start = mid - WIN // 2
            seq = extract_window(genome, chrom, start, rng)
            if seq is None:
                continue
            seqs.append(seq)
            used.add(key)
            kept += 1
        if kept < N_PER_CLASS:
            raise RuntimeError(f"seed {seed}: class {cls} only produced {kept}/{N_PER_CLASS}")
    return seqs


def random_genomic(seed: int, n: int, intervals: dict[str, list[tuple[int, int]]], genome: TwoBitFile) -> list[str]:
    """Sample n random 200 bp windows from autosomes + chrX, excluding cCREs."""
    rng = random.Random(seed * 2 + 2)
    chrom_lens = {c: len(genome[c]) for c in AUTOSOMES_PLUS_X}
    total = sum(chrom_lens.values())
    cum = []
    csum = 0
    chroms = list(AUTOSOMES_PLUS_X)
    for c in chroms:
        csum += chrom_lens[c]
        cum.append(csum)

    seqs: list[str] = []
    attempts = 0
    while len(seqs) < n:
        attempts += 1
        if attempts > n * 50:
            raise RuntimeError(f"seed {seed}: could not produce {n} genomic windows after {attempts} attempts")
        x = rng.randrange(total)
        # find chrom by linear search (only 23 entries)
        ci = 0
        while x >= cum[ci]:
            ci += 1
        chrom = chroms[ci]
        prev = cum[ci - 1] if ci > 0 else 0
        pos_in_chrom = x - prev
        start = pos_in_chrom - WIN // 2
        end = start + WIN
        if start < 0 or end > chrom_lens[chrom]:
            continue
        if overlaps_cre(chrom, start, end, intervals):
            continue
        seq = extract_window(genome, chrom, start, rng)
        if seq is None:
            continue
        seqs.append(seq)
    return seqs


def main() -> None:
    print("Loading cCRE pools + intervals...", file=sys.stderr)
    pools, intervals = load_cre_data()
    print("Opening hg38.2bit...", file=sys.stderr)
    genome = TwoBitFile(str(GENOME))
    for seed in SEEDS:
        print(f"\n[seed {seed}] sampling 40K cCRE...", file=sys.stderr)
        ccre = sample_ccre(seed, pools, genome)
        print(f"[seed {seed}] sampling 10K random genomic...", file=sys.stderr)
        gen = random_genomic(seed, N_GENOMIC, intervals, genome)
        seqs = ccre + gen
        if len(seqs) != N_TOTAL:
            raise RuntimeError(f"seed {seed}: total {len(seqs)} != {N_TOTAL}")
        random.Random(seed * 2 + 3).shuffle(seqs)
        out_path = OUT_DIR / f"sequences_{seed}.txt"
        with open(out_path, "w") as fh:
            fh.write("\n".join(seqs) + "\n")
        print(f"[seed {seed}] wrote {out_path} ({len(seqs)} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
