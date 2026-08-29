"""Experiment 014: Top-signal DNase peaks (quality > quantity).

013 revealed pipeline noise floor ~0.004 on eval_01 — within-band differences
across 003-013 are not significant. To break the band, try QUALITY-FIRST:
restrict DNase peaks to the highest-signal subset (cleaner labels, fewer
false-positive accessible regions).

Composition (50K total), same overall as 009 but with top-signal DNase:
- 20K cCREs (8K dELS + 5K pELS + 3K PLS + 2K CA_TF + 2K CTCF)
- 8K K562 DNase peaks: TOP 8K by signalValue (top ~3.4%)
- 8K HepG2 DNase peaks: TOP 8K (top ~9%)
- 9K SK-N-SH DNase peaks: TOP 9K (top ~5.8%)
- 5K random

Hypothesis: top-signal peaks are more confidently regulatory (stronger
accessibility = stronger TF binding = sharper activity signal). The model
should learn a sharper sequence-activity mapping from cleaner labels.

If 014 eval_01 ≥ 0.080: real signal, top peaks matter
If 014 ∈ [0.074, 0.078]: noise band, no clear effect
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

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
SEED = 14

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    8_000,
    "pELS":    5_000,
    "PLS":     3_000,
    "CA_TF":   2_000,
    "CA-CTCF": 2_000,
}
DNASE_TARGETS = {"K562": 8_000, "HepG2": 8_000, "SKNSH": 9_000}
N_RANDOM = 5_000


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_ccres(path):
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            yield chrom, int(parts[1]), int(parts[2]), parts[5]


def parse_top_narrowpeak(path, n_top):
    """Read narrowPeak, return TOP n_top by signalValue (col 7)."""
    rows = []
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
            rows.append((sig, chrom, summit))
    rows.sort(reverse=True)  # highest signal first
    print(f"  pool {path.name}: {len(rows)} peaks, signal range "
          f"{rows[-1][0]:.1f}–{rows[0][0]:.1f}, "
          f"top-{n_top} min signal {rows[n_top-1][0]:.1f}")
    return [(c, s) for _, c, s in rows[:n_top * 3]]  # 3x for window-fail headroom


def window_around_center(center):
    s = center - L // 2
    return s, s + L


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs...")
    by_class = {k: [] for k in CCRE_TARGETS}
    for chrom, s, e, t in parse_ccres(CCRE_BED):
        if t == "PLS": grp = "PLS"
        elif t == "pELS": grp = "pELS"
        elif t == "dELS": grp = "dELS"
        elif t == "CA-CTCF": grp = "CA-CTCF"
        else: grp = "CA_TF"
        by_class[grp].append((chrom, (s + e) // 2))

    seqs = []
    seen = set()

    for grp, target in CCRE_TARGETS.items():
        pool = by_class[grp]
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

    for cell, target in DNASE_TARGETS.items():
        peaks = parse_top_narrowpeak(PEAK_FILES[cell], target)
        # peaks are already in top-signal order; iterate without shuffle
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
        print(f"  TOP DNase {cell}: {added}/{target}")

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
