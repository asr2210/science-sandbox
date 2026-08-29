"""Experiment 027: Top-signal pooled cCRE∩DNase intersect.

024 used per-cell quotas (15K each). 027 pools all 3 cells' intersect
peaks and picks the TOP 45K by signalValue, regardless of which cell
they came from. This biases toward universally strong regulatory
regions — the "highest-confidence" intersection peaks across the
union.

If signal-strength concentration matters, this should beat 024.
If diversity matters more, this should lose to 024.
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
SEED = 27
INTERSECT_TARGET = 45_000  # rest random

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}


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


def parse_narrowpeak_with_signal(path, cell):
    out = []
    with gzip.open(path, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            start, end = int(parts[1]), int(parts[2])
            try: sig = float(parts[6])
            except (ValueError, IndexError): sig = 0.0
            try: so = int(parts[9])
            except (ValueError, IndexError): so = -1
            summit = (start + so) if so >= 0 else (start + end) // 2
            out.append((chrom, summit, sig, cell))
    return out


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

    pooled = []
    for cell, path in DNASE_FILES.items():
        peaks = parse_narrowpeak_with_signal(path, cell)
        ip = [p for p in peaks if point_in_intervals(ccre[p[0]], p[1])]
        print(f"  {cell}: {len(peaks)} DNase, {len(ip)} cCRE-intersect")
        # rank-normalize signal within this cell to percentile [0,1]
        ip.sort(key=lambda x: x[2])
        n = len(ip)
        ip_norm = [(c, s, (i + 1) / n, cell) for i, (c, s, _, _) in enumerate(ip)]
        pooled.extend(ip_norm)
    print(f"pooled intersect: {len(pooled)}")

    # Sort descending by rank-normalized signal (then small random jitter for tie breaking)
    rng.shuffle(pooled)  # tie-break randomness
    pooled.sort(key=lambda x: x[2], reverse=True)
    print(f"  top rank: {pooled[0][2]:.3f}, median: {pooled[len(pooled)//2][2]:.3f}")

    seqs = []
    seen = set()
    added = 0
    per_cell = {"K562": 0, "HepG2": 0, "SKNSH": 0}
    for chrom, summit, sig, cell in pooled:
        if added >= INTERSECT_TARGET: break
        ws, we = window_around(summit)
        if ws < 0 or we > contig_lens[chrom]: continue
        key = (chrom, ws)
        if key in seen: continue
        seq = fetch_clean(fa, chrom, ws, we)
        if seq is None: continue
        seen.add(key)
        seqs.append(seq)
        per_cell[cell] += 1
        added += 1
    print(f"  intersect: {added}/{INTERSECT_TARGET}")
    print(f"  per-cell origin: {per_cell}")
    print(f"  min retained signal: {sig:.2f}")

    # Fill remainder with random
    needed = N - len(seqs)
    chrom_list = sorted(AUTOSOMES, key=lambda c: int(c[3:]))
    w = np.array([contig_lens[c] for c in chrom_list], dtype=float)
    w /= w.sum()
    rand_added = 0
    tries = 0
    while rand_added < needed and tries < 500_000:
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
        rand_added += 1
    print(f"  random: {rand_added}/{needed}")

    if len(seqs) != N:
        raise RuntimeError(f"got {len(seqs)} != {N}")

    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"wrote {N} to {OUT}")


if __name__ == "__main__":
    main()
