"""Experiment 015: SKNSH-heavy library.

Across all prior cCRE/DNase experiments, SKNSH is the weakest per-cell
correlation (0.066-0.070 vs K562 0.076-0.080). Mean eval_01 is dragged
down by SKNSH. To break the noise band, lift SKNSH.

Composition (50K total):
- 10K cCREs (5K dELS + 3K pELS + 1K PLS + 1K CA-CTCF)
- 8K K562 DNase
- 8K HepG2 DNase
- 14K SKNSH DNase (2x normal allocation)
- 5K SKNSH H3K27ac (extra SKNSH-specific signal)
- 5K random

SKNSH allocation: 19K (38% of library) vs K562 8K (16%), HepG2 8K (16%).

Hypothesis: SKNSH is data-limited. Doubling SKNSH-specific peaks lifts
SKNSH per-cell correlation, which lifts mean eval_01 above noise band.

If 015 SKNSH ≥ 0.075: data-limited, more SKNSH-specific data helps
If 015 SKNSH ≈ 0.067-0.071: SKNSH bottleneck is sequence-intrinsic
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
CCRE_BED = ROOT / "data" / "cCREs.bed"
PEAK_NP = {
    "K562":   (ROOT / "data" / "ENCFF821KDJ.bed.gz", 8_000),
    "HepG2":  (ROOT / "data" / "ENCFF341XEM.bed.gz", 8_000),
    "SKNSH":  (ROOT / "data" / "ENCFF752OZB.bed.gz", 14_000),
}
SKNSH_H3K27AC = ROOT / "data" / "ENCFF790UBM.bed.gz"
SKNSH_H3K27AC_TARGET = 5_000
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 15

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    5_000,
    "pELS":    3_000,
    "PLS":     1_000,
    "CA-CTCF": 1_000,
}
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
        else: continue  # skip CA_TF for simpler 4-class
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

    for cell, (path, target) in PEAK_NP.items():
        peaks = list(parse_narrowpeak(path))
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
        print(f"  DNase {cell}: {added}/{target}")

    # SKNSH H3K27ac (extra)
    peaks = list(parse_narrowpeak(SKNSH_H3K27AC))
    rng.shuffle(peaks)
    added = 0
    for chrom, summit in peaks:
        if added >= SKNSH_H3K27AC_TARGET: break
        ws, we = window_around_center(summit)
        if ws < 0 or we > contig_lens[chrom]: continue
        key = (chrom, ws)
        if key in seen: continue
        seq = fetch_clean(fa, chrom, ws, we)
        if seq is None: continue
        seen.add(key)
        seqs.append(seq)
        added += 1
    print(f"  H3K27ac SKNSH: {added}/{SKNSH_H3K27AC_TARGET}")

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
