"""Experiment 004: ENCODE cCREs as the library.

Sample 50,000 candidate cis-regulatory elements (cCREs) from the
SCREEN/Wenglab catalog (GRCh38, V3, ~1M elements). Restrict to chrs
{1, 11, 19, 20, 21, 22} for parity with exp 002 (~250k cCREs
available). Use a 200bp window centered on each cCRE midpoint. If the
cCRE is shorter than 200bp, flanking genomic sequence pads each side
naturally.

Hypothesis: cCREs are enriched for motif content (selected on
chromatin accessibility + functional marks across many ENCODE cell
types). They should score higher than random genomic windows (002) if
motif density is a bottleneck for the model.

Why this generalizes beyond K562/HepG2/SKNSH: the SCREEN cCRE catalog
is built from ENCODE chromatin data across HUNDREDS of cell types and
tissues — it is the union of regulatory elements used by *any* cell
type. A library built from this is by construction not biased toward
the 3 measurement cell types.
"""
import os
import random
from pathlib import Path

N_SEQ = 50_000
LEN = 200
SEED = 42

HERE = Path(__file__).parent
DATA_DIR = HERE.parents[1] / "data"
CHROMS = ["chr1", "chr11", "chr19", "chr20", "chr21", "chr22"]

def load_chrom(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip())
    return "".join(parts).upper()

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def main():
    chrom_seqs = {c: load_chrom(DATA_DIR / f"{c}.fa") for c in CHROMS}
    chrom_set = set(CHROMS)

    rng = random.Random(SEED)

    # Load cCREs on our chromosomes
    ccres = []
    with open(DATA_DIR / "ccres.bed") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in chrom_set:
                continue
            start = int(parts[1])
            end = int(parts[2])
            ccres.append((parts[0], start, end))
    print(f"Loaded {len(ccres):,} cCREs on {len(CHROMS)} chromosomes.")

    # Shuffle and walk through; skip windows with N
    rng.shuffle(ccres)
    seqs = []
    used = 0
    for chrom, start, end in ccres:
        if len(seqs) >= N_SEQ:
            break
        mid = (start + end) // 2
        w_start = mid - LEN // 2
        w_end = w_start + LEN
        cs = chrom_seqs[chrom]
        if w_start < 0 or w_end > len(cs):
            continue
        window = cs[w_start:w_end]
        if "N" in window:
            continue
        if rng.random() < 0.5:
            window = revcomp(window)
        seqs.append(window)
        used += 1
    print(f"Sampled {len(seqs)} sequences from {used} cCREs.")
    assert len(seqs) == N_SEQ, len(seqs)

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} sequences to {out_path}")

if __name__ == "__main__":
    main()
