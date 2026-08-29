"""Experiment 003: 200bp windows centered on ENCODE V4 cCREs (pan-tissue).

cCRE V4 catalog covers ~2.3M elements across all human tissues (DNase /
H3K27ac / H3K4me1 / CTCF derived). Sampling uniformly at random gives a
pan-tissue regulatory mixture — NOT specific to K562/HepG2/SKNSH.

For each sampled cCRE, take the 200bp window centered on the element midpoint
from the hg38 chromosome. Skip windows with N. Seed 0.

I have chr1/11/19/22 downloaded; restrict to those to avoid extra downloads
(~424k cCREs available, sampling ~12%).
"""
import gzip
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hg38"
CCRE = ROOT / "data" / "ccre_v4.bed"
CHROMS = ["chr1", "chr11", "chr19", "chr22"]
N = 50_000
L = 200
SEED = 0


def load_chrom(name):
    text_chunks = []
    with gzip.open(DATA / f"{name}.fa.gz", "rt") as f:
        for line in f:
            if line.startswith(">"):
                continue
            text_chunks.append(line.strip())
    return "".join(text_chunks).upper()


def main():
    rng = np.random.default_rng(SEED)
    chrset = set(CHROMS)
    ccres = []
    with CCRE.open() as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] in chrset:
                start, end = int(parts[1]), int(parts[2])
                ccres.append((parts[0], start, end, parts[5]))
    print(f"loaded {len(ccres)} cCREs on {CHROMS}")
    type_counts = {}
    for _, _, _, t in ccres:
        type_counts[t] = type_counts.get(t, 0) + 1
    print("types:", type_counts)

    print("loading chromosomes...")
    seqs = {c: load_chrom(c) for c in CHROMS}

    out_lines = []
    sampled_types = {}
    # shuffle indices once and walk
    idx_perm = rng.permutation(len(ccres))
    cursor = 0
    while len(out_lines) < N:
        if cursor >= len(idx_perm):
            # in case of many rejections, reshuffle and continue
            idx_perm = rng.permutation(len(ccres))
            cursor = 0
        i = idx_perm[cursor]
        cursor += 1
        chrom, start, end, ctype = ccres[i]
        mid = (start + end) // 2
        w_start = mid - L // 2
        w_end = w_start + L
        s = seqs[chrom]
        if w_start < 0 or w_end > len(s):
            continue
        window = s[w_start:w_end]
        if "N" in window:
            continue
        out_lines.append(window)
        sampled_types[ctype] = sampled_types.get(ctype, 0) + 1

    print("sampled type mix:", sampled_types)
    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        f.write("\n".join(out_lines))
        f.write("\n")
    print(f"wrote {len(out_lines)} sequences to {out}")


if __name__ == "__main__":
    main()
