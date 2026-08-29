"""Experiment 024: Pure cCRE∩DNase intersect, max per-cell.

Test the "signal density" hypothesis: every sequence is a
high-confidence per-cell regulatory element. No padding with weaker
broad cCREs. Fill any deficit with random.

- ~15K each cell type cCRE∩DNase (or as many as exist)
- random filler to 50K (small)
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta
from bisect import bisect_right

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
CCRE_BED = ROOT / "data" / "cCREs.bed"
DNASE_FILES = {
    "K562":   ROOT / "data" / "ENCFF821KDJ.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF341XEM.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF752OZB.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 24

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}
PER_CELL_TARGET = 15_000  # 3 * 15K = 45K, leaves 5K random


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_ccre_intervals(path):
    by_chrom = {c: [] for c in AUTOSOMES}
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            s, e = int(parts[1]), int(parts[2])
            by_chrom[chrom].append((s, e))
    for c in by_chrom:
        by_chrom[c].sort()
    return by_chrom


def point_in_intervals(intervals, pos):
    if not intervals: return False
    starts = [iv[0] for iv in intervals]
    i = bisect_right(starts, pos) - 1
    if i < 0: return False
    s, e = intervals[i]
    return s <= pos < e


def parse_narrowpeak(path):
    with gzip.open(path, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            start, end = int(parts[1]), int(parts[2])
            try: so = int(parts[9])
            except (ValueError, IndexError): so = -1
            summit = (start + so) if so >= 0 else (start + end) // 2
            yield chrom, summit


def window_around(center):
    s = center - L // 2
    return s, s + L


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs...")
    ccre = parse_ccre_intervals(CCRE_BED)

    seqs = []
    seen = set()

    for i, (cell, path) in enumerate(DNASE_FILES.items()):
        peaks = list(parse_narrowpeak(path))
        ip = [(c, s) for c, s in peaks if point_in_intervals(ccre[c], s)]
        print(f"  {cell}: {len(peaks)} DNase, {len(ip)} cCRE-intersect")
        rng_local = random.Random(SEED + 100 + i)
        rng_local.shuffle(ip)
        added = 0
        for chrom, summit in ip:
            if added >= PER_CELL_TARGET: break
            ws, we = window_around(summit)
            if ws < 0 or we > contig_lens[chrom]: continue
            key = (chrom, ws)
            if key in seen: continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None: continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  added {cell}: {added}/{PER_CELL_TARGET}")

    print(f"intersect total: {len(seqs)}")

    # Fill remainder with random
    needed = N - len(seqs)
    print(f"  need {needed} random")
    chrom_list = sorted(AUTOSOMES, key=lambda c: int(c[3:]))
    w = np.array([contig_lens[c] for c in chrom_list], dtype=float)
    w /= w.sum()
    added = 0
    tries = 0
    while added < needed and tries < 500_000:
        tries += 1
        chrom = nprng.choice(chrom_list, p=w)
        clen = contig_lens[chrom]
        start = int(nprng.integers(0, clen - L))
        seq = fetch_clean(fa, chrom, start, start + L)
        if seq is None: continue
        key = (chrom, start)
        if key in seen: continue
        seen.add(key)
        seqs.append(seq)
        added += 1
    print(f"  random: {added}/{needed}")

    if len(seqs) != N:
        raise RuntimeError(f"got {len(seqs)} != {N}")

    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"wrote {N} to {OUT}")


if __name__ == "__main__":
    main()
