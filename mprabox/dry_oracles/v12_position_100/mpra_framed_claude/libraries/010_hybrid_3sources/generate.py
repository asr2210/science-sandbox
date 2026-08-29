"""Experiment 010: 3-source hybrid library — cCREs + DNase + H3K27ac + random.

Tests the "more orthogonal signal sources = better" hypothesis from 009.
Adds H3K27ac ChIP-seq peaks for the 3 measured cells as a third source,
on top of the cCRE + DNase + random hybrid that broke the cCRE plateau.

Composition (50K total):
- 15K cCREs (broad regulatory grammar across many cell types)
   - 6K dELS, 4K pELS, 2.5K PLS, 1.5K CA_TF, 1K CA-CTCF
- 5K K562 DNase peaks
- 5K HepG2 DNase peaks
- 5K SK-N-SH DNase peaks
- 5K K562 H3K27ac peaks
- 5K HepG2 H3K27ac peaks
- 5K SK-N-SH H3K27ac peaks
- 5K random non-cCRE/non-peak autosomal background

Each cell gets 10K total (5K DNase + 5K H3K27ac), tripling cell-type
coverage vs cCREs-only baseline. H3K27ac is a complementary mark to
DNase: DNase marks accessibility, H3K27ac marks transcriptionally
active enhancers/promoters. Together they capture different aspects
of regulatory activity in each cell type.

Hypothesis: H3K27ac will add NEW signal beyond DNase because:
1. H3K27ac is a direct activity mark (DNase only marks accessibility,
   which doesn't always mean active)
2. Many accessible regions have low H3K27ac (poised but inactive)
3. The model can learn the joint distribution of accessibility + active
   mark to predict MPRA activity more accurately

Generalization argument: H3K27ac marks ACTIVE enhancers, which contain
strong TF motifs. Training on H3K27ac peaks exposes the model to
high-signal motif content. The learned motif features transfer across
cell types because TF binding is sequence-driven, not chromatin-state-
driven.

If 010 > 009: orthogonal signals stack — keep adding sources
If 010 ≈ 009: signal saturated — optimize composition or stratify
If 010 < 009: H3K27ac is redundant with DNase, narrows diversity
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
CCRE_BED = ROOT / "data" / "cCREs.bed"
DNASE_FILES = {
    "K562":   ROOT / "data" / "ENCFF821KDJ.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF341XEM.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF752OZB.bed.gz",
}
H3K27AC_FILES = {
    "K562":   ROOT / "data" / "ENCFF038DDS.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF886SZT.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF790UBM.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 10

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    6_000,
    "pELS":    4_000,
    "PLS":     2_500,
    "CA_TF":   1_500,
    "CA-CTCF": 1_000,
}
DNASE_TARGET = 5_000
H3K27AC_TARGET = 5_000
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


def sample_peaks_to(seqs, seen, fa, contig_lens, peaks, target, label):
    rng = random.Random(SEED + hash(label) % 1000)
    rng.shuffle(peaks)
    added = 0
    for chrom, summit in peaks:
        if added >= target:
            break
        ws, we = window_around_center(summit)
        if ws < 0 or we > contig_lens[chrom]:
            continue
        key = (chrom, ws)
        if key in seen:
            continue
        seq = fetch_clean(fa, chrom, ws, we)
        if seq is None:
            continue
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
            if added >= target:
                break
            ws, we = window_around_center(center)
            if ws < 0 or we > contig_lens[chrom]:
                continue
            key = (chrom, ws)
            if key in seen:
                continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None:
                continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  cCRE {grp}: {added}/{target}")

    for cell, path in DNASE_FILES.items():
        peaks = list(parse_peaks(path))
        sample_peaks_to(seqs, seen, fa, contig_lens, peaks, DNASE_TARGET, f"DNase {cell}")

    for cell, path in H3K27AC_FILES.items():
        peaks = list(parse_peaks(path))
        sample_peaks_to(seqs, seen, fa, contig_lens, peaks, H3K27AC_TARGET, f"H3K27ac {cell}")

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
        if seq is None:
            continue
        key = (chrom, start)
        if key in seen:
            continue
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
