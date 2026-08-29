"""Experiment 007: Multi-window augmentation per cCRE.

Take ~16,667 unique cCREs and generate 3 overlapping 200bp windows per
cCRE (centered at cCRE_center - 60, cCRE_center, cCRE_center + 60),
yielding 50K sequences from ~16.7K unique cCRE regions.

This is positional data augmentation. The model sees the same
regulatory grammar in three different translational framings:
- Window 1: left-shifted (motifs near right edge of window)
- Window 2: centered (motifs in middle)
- Window 3: right-shifted (motifs near left edge)

Hypothesis: shifting the position of regulatory elements within the
200bp window forces the model to learn position-invariant motif
detectors. This should improve generalization because:
1. The model can't memorize "activity correlates with position X"
2. Motif features become more robust (translation-equivariant)
3. Same labels seen 3x effectively increases label SNR per region

Generalization argument: cross-cell-type generalization requires
robust motif detection. Position-shift augmentation makes the model
more robust by teaching positional invariance — a property of any
good convolutional regulator-grammar learner.

If 007 > 003: augmentation helps; trade unique sequence count for
positional diversity. (Direction: more aggressive augmentation.)
If 007 < 003: unique sequences > augmentation; the model gets enough
positional variation from the natural cCRE position distribution.
"""
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
BED = ROOT / "data" / "cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 7
WINDOWS_PER_CCRE = 3
OFFSETS = (-60, 0, 60)  # bp shifts from cCRE center
N_UNIQUE_TARGET = N // WINDOWS_PER_CCRE + 50  # 16,716 unique cCREs

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

UNIQUE_TARGETS = {
    "dELS":    7_000,
    "pELS":    3_500,
    "PLS":     2_000,
    "CA_TF":   2_500,
    "CA-CTCF": 1_700,
}


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_bed(path):
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES:
                continue
            yield chrom, int(parts[1]), int(parts[2]), parts[5]


def main():
    rng = random.Random(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs...")
    by_class = {k: [] for k in UNIQUE_TARGETS}
    for chrom, s, e, t in parse_bed(BED):
        if t == "PLS": grp = "PLS"
        elif t == "pELS": grp = "pELS"
        elif t == "dELS": grp = "dELS"
        elif t == "CA-CTCF": grp = "CA-CTCF"
        else: grp = "CA_TF"
        by_class[grp].append((chrom, s, e))

    selected = []
    for grp, target in UNIQUE_TARGETS.items():
        pool = by_class[grp]
        rng.shuffle(pool)
        added = 0
        for chrom, s, e in pool:
            if added >= target:
                break
            selected.append((chrom, (s + e) // 2))
            added += 1
        print(f"  {grp}: selected {added}")

    print(f"total unique cCREs selected: {len(selected)}")
    # For each, generate 3 windows; 3*16700 = 50100, will trim to N
    seqs = []
    seen = set()
    rng.shuffle(selected)
    for chrom, center in selected:
        if len(seqs) >= N:
            break
        clen = contig_lens[chrom]
        for off in OFFSETS:
            ws = center + off - L // 2
            we = ws + L
            if ws < 0 or we > clen:
                continue
            key = (chrom, ws)
            if key in seen:
                continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None:
                continue
            seen.add(key)
            seqs.append(seq)
            if len(seqs) >= N:
                break
    if len(seqs) < N:
        raise RuntimeError(f"got only {len(seqs)} sequences; need {N}")
    seqs = seqs[:N]
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s)
            f.write("\n")
    print(f"wrote {N} sequences to {OUT}")


if __name__ == "__main__":
    main()
