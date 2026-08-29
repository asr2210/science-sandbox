"""Experiment 017: cCRE-DNase intersection (label-confidence axis).

Highest-confidence regulatory: DNase peaks that overlap a cCRE.
Validated by BOTH per-cell accessibility AND cross-tissue regulatory
catalog.

Composition:
- 30K cCRE-overlapping DNase peaks (10K each K562/HepG2/SKNSH)
- 15K cCREs that do NOT overlap any peak from the 3 cells (broad
  regulatory grammar from cells beyond ours)
- 5K random

Hypothesis: high-confidence labels (intersection) give clearer
sequence-activity mapping than any single source.
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
PEAK_FILES = {
    "K562":   ROOT / "data" / "ENCFF821KDJ.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF341XEM.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF752OZB.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 17

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_NONOVERLAP_TARGET = 15_000
DNASE_TARGET = 10_000
N_RANDOM = 5_000


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_ccres_intervals(path):
    """Return chrom -> list of (start, end, center) for autosomal cCREs."""
    by_chrom = {c: [] for c in AUTOSOMES}
    for line in open(path):
        parts = line.rstrip("\n").split("\t")
        chrom = parts[0]
        if chrom not in AUTOSOMES: continue
        s, e = int(parts[1]), int(parts[2])
        by_chrom[chrom].append((s, e, (s + e) // 2))
    for c in by_chrom:
        by_chrom[c].sort()
    return by_chrom


def point_in_intervals(chrom_intervals, pos):
    """Binary search: is pos within any [s, e)?"""
    starts = [iv[0] for iv in chrom_intervals]
    i = bisect_right(starts, pos) - 1
    if i < 0:
        return False
    s, e, _ = chrom_intervals[i]
    return s <= pos < e


def parse_peaks(path):
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


def window_around_center(center):
    s = center - L // 2
    return s, s + L


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs as intervals...")
    ccre_by_chrom = parse_ccres_intervals(CCRE_BED)
    n_ccre = sum(len(v) for v in ccre_by_chrom.values())
    print(f"  {n_ccre} cCREs across autosomes")

    # Collect peaks per cell, classify intersection vs not
    peaks_intersect = {}  # cell -> list of (chrom, summit)
    union_peak_centers = {c: set() for c in AUTOSOMES}  # for cCRE-no-peak class
    for cell, path in PEAK_FILES.items():
        ip = []
        for chrom, summit in parse_peaks(path):
            ivs = ccre_by_chrom[chrom]
            if ivs and point_in_intervals(ivs, summit):
                ip.append((chrom, summit))
            union_peak_centers[chrom].add(summit // 1000)  # 1kb bin
        peaks_intersect[cell] = ip
        print(f"  {cell}: {len(ip)} cCRE-overlapping peaks")

    seqs = []
    seen = set()

    # 1) DNase peaks that overlap cCREs, per cell
    for cell, ip in peaks_intersect.items():
        rng.shuffle(ip)
        added = 0
        for chrom, summit in ip:
            if added >= DNASE_TARGET: break
            ws, we = window_around_center(summit)
            if ws < 0 or we > contig_lens[chrom]: continue
            key = (chrom, ws)
            if key in seen: continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None: continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  intersect DNase {cell}: {added}/{DNASE_TARGET}")

    # 2) cCREs that do NOT have a peak from our 3 cells (broader regulatory)
    nonoverlap_pool = []
    for chrom, ivs in ccre_by_chrom.items():
        for s, e, center in ivs:
            # check if any peak summit falls in this cCRE (use 1kb bins)
            bins = {(center // 1000), ((s) // 1000), ((e) // 1000)}
            has_peak = any(b in union_peak_centers[chrom] for b in bins)
            if not has_peak:
                nonoverlap_pool.append((chrom, center))
    print(f"  non-overlap cCRE pool: {len(nonoverlap_pool)}")
    rng.shuffle(nonoverlap_pool)
    added = 0
    for chrom, center in nonoverlap_pool:
        if added >= CCRE_NONOVERLAP_TARGET: break
        ws, we = window_around_center(center)
        if ws < 0 or we > contig_lens[chrom]: continue
        key = (chrom, ws)
        if key in seen: continue
        seq = fetch_clean(fa, chrom, ws, we)
        if seq is None: continue
        seen.add(key)
        seqs.append(seq)
        added += 1
    print(f"  non-overlap cCRE: {added}/{CCRE_NONOVERLAP_TARGET}")

    # 3) Random
    chrom_list = sorted(AUTOSOMES, key=lambda c: int(c[3:]))
    w = np.array([contig_lens[c] for c in chrom_list], dtype=float)
    w /= w.sum()
    added = 0
    tries = 0
    while added < N_RANDOM and tries < 200_000:
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
    print(f"  random: {added}/{N_RANDOM} ({tries} tries)")

    if len(seqs) != N:
        raise RuntimeError(f"got {len(seqs)} != {N}")

    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s)
            f.write("\n")
    print(f"wrote {N} to {OUT}")


if __name__ == "__main__":
    main()
