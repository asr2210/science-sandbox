"""Experiment 002: random 200bp windows from real hg38 (chr1, 11, 19, 22).

Sample 50k non-N windows uniformly at random from a pooled chromosome set
spanning varied gene density (chr1 large/varied, chr11 medium, chr19 gene-rich,
chr22 small/gene-poor). Skip any window containing N. Seed 0.
"""
import gzip
import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "hg38"
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
    seqs = [load_chrom(c) for c in CHROMS]
    lengths = np.array([len(s) for s in seqs])
    weights = lengths / lengths.sum()
    print({c: len(s) for c, s in zip(CHROMS, seqs)})

    out_lines = []
    tries = 0
    while len(out_lines) < N:
        tries += 1
        ci = rng.choice(len(seqs), p=weights)
        s = seqs[ci]
        start = rng.integers(0, len(s) - L)
        window = s[start : start + L]
        if "N" in window:
            continue
        out_lines.append(window)
    print(f"sampled {len(out_lines)} windows from {tries} tries "
          f"({tries - len(out_lines)} rejected for N)")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        f.write("\n".join(out_lines))
        f.write("\n")
    print(f"wrote to {out}")


if __name__ == "__main__":
    main()
