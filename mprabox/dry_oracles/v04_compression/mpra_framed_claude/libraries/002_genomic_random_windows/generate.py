"""Experiment 002: random 200bp windows from the human genome (GRCh38).

50,000 windows sampled uniformly across 6 GRCh38 chromosomes (1, 11, 19, 20,
21, 22). Reject windows containing N. Strand chosen uniformly.

Compares to 001 (uniform random ACGT) — tests whether natural genomic
sequence statistics (GC content, repeats, dinucleotide patterns, by-chance
motifs) make a library more informative for a sequence-to-activity model
than uniform-random sequences.

Why this generalizes beyond K562/HepG2/SKNSH: random genomic windows are
*not* enriched for any cell-type-specific element. They sample the natural
sequence space, which encodes the regulatory grammar shared across all
human cell types. If natural sequences help, the model is learning
something about regulatory grammar; this learning transfers to any cell
type because the grammar is the same.
"""
import os
import numpy as np
from pathlib import Path

N_SEQ = 50_000
LEN = 200
SEED = 42

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CHROMS = ["chr1", "chr11", "chr19", "chr20", "chr21", "chr22"]

def load_chrom(path):
    """Load a single-chromosome FASTA; return uppercase sequence string."""
    seq_parts = []
    with open(path) as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq_parts.append(line.strip())
    return "".join(seq_parts).upper()

def revcomp(s):
    tbl = str.maketrans("ACGT", "TGCA")
    return s.translate(tbl)[::-1]

def main():
    chrom_seqs = {}
    for c in CHROMS:
        path = DATA_DIR / f"{c}.fa"
        chrom_seqs[c] = load_chrom(path)
        print(f"{c}: {len(chrom_seqs[c]):,} bp")

    # Compute total non-N length per chromosome — but easier: just rejection
    # sample. Roughly half of GRCh38 chrs are N due to centromere/gaps, so
    # ~2× oversampling needed.
    rng = np.random.default_rng(SEED)
    chrom_list = CHROMS
    chrom_weights = np.array([len(chrom_seqs[c]) for c in chrom_list],
                              dtype=np.float64)
    chrom_weights /= chrom_weights.sum()

    seqs = []
    attempts = 0
    while len(seqs) < N_SEQ:
        # Pick chromosome by length
        ci = rng.choice(len(chrom_list), p=chrom_weights)
        s = chrom_seqs[chrom_list[ci]]
        pos = rng.integers(0, len(s) - LEN)
        window = s[pos:pos + LEN]
        attempts += 1
        if "N" in window:
            continue
        # Random strand
        if rng.random() < 0.5:
            window = revcomp(window)
        seqs.append(window)
    print(f"Sampled {len(seqs)} sequences in {attempts} attempts "
          f"({100 * len(seqs) / attempts:.1f}% accept).")

    out_path = Path(__file__).parent / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} sequences to {out_path}")

if __name__ == "__main__":
    main()
