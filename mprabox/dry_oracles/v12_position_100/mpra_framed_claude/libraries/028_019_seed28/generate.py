"""Experiment 019: Kitchen-sink 5-source combination.

Final breakout attempt. Combine all signal types tested so far in one
diverse library:
- 10K cCRE-DNase intersection (high-confidence per-cell regulatory)
- 15K pure cCRE (broad regulatory grammar)
- 15K DNase peaks (5K each cell)
- 5K CTCF ChIP-seq (concentrated motif signal, mixed cells)
- 5K random
= 50K. Seed=19.
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
CTCF_FILES = {
    "K562":   ROOT / "data" / "K562_ctcf.bed.gz",
    "HepG2":  ROOT / "data" / "HepG2_ctcf.bed.gz",
    "SKNSH":  ROOT / "data" / "SKNSH_ctcf.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 28

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    6_000,
    "pELS":    4_000,
    "PLS":     2_000,
    "CA_TF":   1_500,
    "CA-CTCF": 1_500,
}
INTERSECT_TARGET = 3_400  # × 3 cells ≈ 10K
DNASE_TARGET = 5_000      # × 3 cells = 15K
CTCF_PER_CELL = 1_700     # × 3 ≈ 5K
N_RANDOM = 5_000


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_ccres(path):
    by_chrom_intervals = {c: [] for c in AUTOSOMES}
    by_class = {k: [] for k in CCRE_TARGETS}
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            s, e, t = int(parts[1]), int(parts[2]), parts[5]
            center = (s + e) // 2
            by_chrom_intervals[chrom].append((s, e))
            if t == "PLS": grp = "PLS"
            elif t == "pELS": grp = "pELS"
            elif t == "dELS": grp = "dELS"
            elif t == "CA-CTCF": grp = "CA-CTCF"
            else: grp = "CA_TF"
            by_class[grp].append((chrom, center))
    for c in by_chrom_intervals:
        by_chrom_intervals[c].sort()
    return by_class, by_chrom_intervals


def point_in_intervals(intervals, pos):
    if not intervals:
        return False
    starts = [iv[0] for iv in intervals]
    i = bisect_right(starts, pos) - 1
    if i < 0:
        return False
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


def window_around_center(center):
    s = center - L // 2
    return s, s + L


def add_peaks(seqs, seen, fa, contig_lens, peaks, target, label, seed):
    rng = random.Random(seed)
    rng.shuffle(peaks)
    added = 0
    for chrom, summit in peaks:
        if added >= target: break
        ws, we = window_around_center(summit)
        if ws < 0 or we > contig_lens[chrom]: continue
        key = (chrom, ws)
        if key in seen: continue
        seq = fetch_clean(fa, chrom, ws, we)
        if seq is None: continue
        seen.add(key)
        seqs.append(seq)
        added += 1
    print(f"  {label}: {added}/{target}")
    return added


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs...")
    by_class, ccre_intervals = parse_ccres(CCRE_BED)

    # Build per-cell intersection peak lists
    intersect_peaks = {}
    all_peaks = {}
    for cell, path in DNASE_FILES.items():
        peaks = list(parse_narrowpeak(path))
        all_peaks[cell] = peaks
        ip = [(c, s) for c, s in peaks if point_in_intervals(ccre_intervals[c], s)]
        intersect_peaks[cell] = ip
        print(f"  {cell}: {len(peaks)} total, {len(ip)} intersect cCRE")

    seqs = []
    seen = set()

    # 1) cCRE-DNase intersection (high confidence per-cell)
    for i, (cell, ip) in enumerate(intersect_peaks.items()):
        add_peaks(seqs, seen, fa, contig_lens, ip[:], INTERSECT_TARGET,
                  f"INTERSECT {cell}", SEED + 100 + i)

    # 2) Pure cCREs (broad)
    for grp, target in CCRE_TARGETS.items():
        pool = by_class[grp][:]
        rng.shuffle(pool)
        added = 0
        for chrom, center in pool:
            if added >= target: break
            ws, we = window_around_center(center)
            if ws < 0 or we > contig_lens[chrom]: continue
            key = (chrom, ws)
            if key in seen: continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None: continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  cCRE {grp}: {added}/{target}")

    # 3) All DNase (5K each cell, dedup against intersection already in)
    for i, (cell, peaks) in enumerate(all_peaks.items()):
        add_peaks(seqs, seen, fa, contig_lens, peaks[:], DNASE_TARGET,
                  f"DNase {cell}", SEED + 200 + i)

    # 4) CTCF ChIP-seq from each cell
    for i, (cell, path) in enumerate(CTCF_FILES.items()):
        peaks = list(parse_narrowpeak(path))
        add_peaks(seqs, seen, fa, contig_lens, peaks, CTCF_PER_CELL,
                  f"CTCF {cell}", SEED + 300 + i)

    # 5) Random
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

    print(f"total: {len(seqs)}")
    # Trim or fill to N
    if len(seqs) > N:
        rng.shuffle(seqs)
        seqs = seqs[:N]
    elif len(seqs) < N:
        extra = N - len(seqs)
        added2 = 0
        tries2 = 0
        while added2 < extra and tries2 < 200_000:
            tries2 += 1
            chrom = nprng.choice(chrom_list, p=w)
            clen = contig_lens[chrom]
            start = int(nprng.integers(0, clen - L))
            seq = fetch_clean(fa, chrom, start, start + L)
            if seq is None: continue
            key = (chrom, start)
            if key in seen: continue
            seen.add(key)
            seqs.append(seq)
            added2 += 1
        print(f"  filler random: {added2}")

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
