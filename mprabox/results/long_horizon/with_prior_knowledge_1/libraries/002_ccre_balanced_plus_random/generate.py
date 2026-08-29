#!/usr/bin/env python3
"""
Experiment 002 — cCRE class-balanced (40K) + i.i.d. random ACGT (10K).

Hypothesis: a 20% random-sequence component recovers the eval_08 loss observed
in experiment 001 while preserving the eval_01 gain over dhs_topic.

Generates 50,000 200 bp sequences per seed, 3 seeds.
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
N_RANDOM = 10_000
N_TOTAL = 50_000
PRIMARY_CLASSES = ("PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3")
SEEDS = (0, 1, 2)


def primary_class(field6: str) -> str | None:
    head = field6.split(",", 1)[0]
    return head if head in PRIMARY_CLASSES else None


def load_pools() -> dict[str, list[tuple[str, int]]]:
    pools: dict[str, list[tuple[str, int]]] = {c: [] for c in PRIMARY_CLASSES}
    with open(CCRE_BED) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            cls = primary_class(parts[5])
            if cls is None:
                continue
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            mid = (start + end) // 2
            pools[cls].append((chrom, mid))
    for c in PRIMARY_CLASSES:
        print(f"  pool[{c}] = {len(pools[c]):,}", file=sys.stderr)
    return pools


def extract_window(genome: TwoBitFile, chrom: str, mid: int, rng: random.Random) -> str | None:
    chrom_len = len(genome[chrom])
    start = mid - WIN // 2
    end = start + WIN
    if start < 0 or end > chrom_len:
        return None
    seq = genome[chrom][start:end].upper()
    if len(seq) != WIN:
        return None
    out = []
    for b in seq:
        out.append(b if b in "ACGT" else rng.choice("ACGT"))
    return "".join(out)


def sample_ccre(seed: int, pools: dict[str, list[tuple[str, int]]], genome: TwoBitFile) -> list[str]:
    rng = random.Random(seed * 2 + 1)  # separate RNG stream from random-gen
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
            seq = extract_window(genome, chrom, mid, rng)
            if seq is None:
                continue
            seqs.append(seq)
            used.add(key)
            kept += 1
        if kept < N_PER_CLASS:
            raise RuntimeError(f"seed {seed}: class {cls} only produced {kept}/{N_PER_CLASS}")
    return seqs


def random_sequences(seed: int, n: int) -> list[str]:
    rng = random.Random(seed * 2 + 2)  # independent stream from cCRE sampling
    bases = "ACGT"
    return ["".join(rng.choices(bases, k=WIN)) for _ in range(n)]


def main() -> None:
    print("Loading cCRE pools...", file=sys.stderr)
    pools = load_pools()
    print("Opening hg38.2bit...", file=sys.stderr)
    genome = TwoBitFile(str(GENOME))
    for seed in SEEDS:
        print(f"\n[seed {seed}] sampling 40K cCRE...", file=sys.stderr)
        ccre = sample_ccre(seed, pools, genome)
        print(f"[seed {seed}] generating 10K random...", file=sys.stderr)
        rnd = random_sequences(seed, N_RANDOM)
        seqs = ccre + rnd
        if len(seqs) != N_TOTAL:
            raise RuntimeError(f"seed {seed}: total {len(seqs)} != {N_TOTAL}")
        # Final shuffle interleaves cCRE and random; uses yet another stream.
        random.Random(seed * 2 + 3).shuffle(seqs)
        out_path = OUT_DIR / f"sequences_{seed}.txt"
        with open(out_path, "w") as fh:
            fh.write("\n".join(seqs) + "\n")
        print(f"[seed {seed}] wrote {out_path} ({len(seqs)} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
