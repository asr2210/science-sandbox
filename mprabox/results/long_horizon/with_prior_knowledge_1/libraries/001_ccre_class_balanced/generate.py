#!/usr/bin/env python3
"""
Experiment 001 — cCRE class-balanced sampling.

Sample 10,000 elements from each of 5 ENCODE SCREEN cCRE primary classes
(PLS, pELS, dELS, CTCF-only, DNase-H3K4me3) and extract a 200 bp window
centered on each cCRE midpoint from hg38. Repeat for three seeds.

Hypothesis: annotation diversity (5 cCRE classes equally) drives the
generalization signal more than the specific DHS index.
"""
from __future__ import annotations

import os
import random
import sys
from pathlib import Path

from twobitreader import TwoBitFile

REPO = Path(__file__).resolve().parents[2]
CCRE_BED = REPO / "data" / "cCRE" / "GRCh38-cCREs.bed"
GENOME = REPO / "data" / "genome" / "hg38.2bit"
OUT_DIR = Path(__file__).resolve().parent

WIN = 200
N_PER_CLASS = 10_000
N_TOTAL = 50_000
PRIMARY_CLASSES = ("PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3")
SEEDS = (0, 1, 2)


def primary_class(field6: str) -> str | None:
    """Return the first token of the cCRE class column (collapses CTCF-bound)."""
    head = field6.split(",", 1)[0]
    return head if head in PRIMARY_CLASSES else None


def load_pools() -> dict[str, list[tuple[str, int]]]:
    """Return {class: [(chrom, midpoint), ...]} from the cCRE BED."""
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
    """Return a WIN-bp uppercase ACGT sequence centered at mid, or None on edge fail."""
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
        if b in "ACGT":
            out.append(b)
        else:
            out.append(rng.choice("ACGT"))
    return "".join(out)


def sample_one_seed(seed: int, pools: dict[str, list[tuple[str, int]]], genome: TwoBitFile) -> list[str]:
    rng = random.Random(seed)
    seqs: list[str] = []
    used: set[tuple[str, int]] = set()
    for cls in PRIMARY_CLASSES:
        pool = pools[cls]
        # Sample with rejection: draw, extract, accept if within bounds and unseen.
        target = N_PER_CLASS
        kept = 0
        order = list(range(len(pool)))
        rng.shuffle(order)
        for idx in order:
            if kept >= target:
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
        if kept < target:
            raise RuntimeError(f"seed {seed}: class {cls} only produced {kept}/{target}")
    if len(seqs) != N_TOTAL:
        raise RuntimeError(f"seed {seed}: total {len(seqs)} != {N_TOTAL}")
    rng.shuffle(seqs)
    return seqs


def main() -> None:
    print("Loading cCRE pools...", file=sys.stderr)
    pools = load_pools()
    print("Opening hg38.2bit...", file=sys.stderr)
    genome = TwoBitFile(str(GENOME))
    for seed in SEEDS:
        out_path = OUT_DIR / f"sequences_{seed}.txt"
        print(f"\n[seed {seed}] sampling 50k...", file=sys.stderr)
        seqs = sample_one_seed(seed, pools, genome)
        with open(out_path, "w") as fh:
            fh.write("\n".join(seqs) + "\n")
        print(f"[seed {seed}] wrote {out_path} ({len(seqs)} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
