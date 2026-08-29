"""
Experiment 002 — random genomic 200bp windows from GRCh38 chr22.

Samples 50,000 non-overlapping or randomly-positioned 200bp windows
from human chromosome 22 (hg38). Drops any window that contains an N
(repeat-masked / assembly gap) and resamples until we have 50,000.

This is the "natural DNA" baseline. No regulatory enrichment — windows
are positioned uniformly at random along chr22, so they contain
whatever chr22 happens to contain (mostly non-regulatory DNA: genes,
introns, intergenic, repeats, some regulatory elements proportional to
their genome-wide density).

Compared to 001 (uniform iid {ACGT}), this library has:
- realistic GC content (~48% on chr22)
- realistic dinucleotide / k-mer statistics
- realistic repetitive element content
- a small fraction of true regulatory elements (proportional to genome
  density, ~1-2% of windows likely overlap a cCRE)
- realistic background DNA structure of any kind
"""
import os
import sys
import numpy as np

N_SEQ = 50_000
L = 200
SEED = 0

def load_chr22(fa_path):
    """Load chr22 fasta as a single uppercase string."""
    with open(fa_path) as f:
        lines = f.read().splitlines()
    # skip header
    assert lines[0].startswith(">")
    seq = "".join(lines[1:]).upper()
    return seq

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    fa_path = os.path.join(repo_root, "data", "chr22.fa")
    seq = load_chr22(fa_path)
    print(f"chr22 length: {len(seq):,}")

    rng = np.random.default_rng(SEED)
    # Positions where any of the 200bp window has N → reject.
    # Strategy: oversample positions, vectorize the N check via numpy.
    arr = np.frombuffer(seq.encode("ascii"), dtype=np.uint8)
    # mark N positions
    is_n = (arr == ord("N")).astype(np.int32)
    # cumulative count of N up to position i: prefix[i] = sum(is_n[:i])
    prefix = np.concatenate(([0], np.cumsum(is_n)))
    # window [i, i+L) has any N if prefix[i+L] - prefix[i] > 0
    max_start = len(seq) - L
    assert max_start > 0

    out = []
    bases = set("ACGT")
    while len(out) < N_SEQ:
        # oversample by 2x to account for rejections
        need = N_SEQ - len(out)
        starts = rng.integers(0, max_start + 1, size=need * 2, dtype=np.int64)
        # filter out N-containing windows
        n_in_window = prefix[starts + L] - prefix[starts]
        good = starts[n_in_window == 0]
        for s in good:
            if len(out) >= N_SEQ:
                break
            window = seq[s:s + L]
            # extra paranoia: ensure only ACGT
            if set(window) <= bases:
                out.append(window)
        if len(out) < N_SEQ and len(good) == 0:
            # extreme bad luck — shouldn't happen
            raise RuntimeError("could not sample enough N-free windows")

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in out:
            f.write(s)
            f.write("\n")
    # sanity check
    with open(out_path) as f:
        lines = f.read().splitlines()
    assert len(lines) == N_SEQ, f"expected {N_SEQ} lines, got {len(lines)}"
    assert all(len(s) == L for s in lines), "wrong length"
    assert all(set(s) <= bases for s in lines[:1000]), "bad bases"
    # report GC content
    gc = sum(1 for line in lines[:5000] for c in line if c in "GC") / (5000 * L)
    print(f"wrote {len(lines)} sequences of length {L} to {out_path}")
    print(f"approximate GC fraction (first 5000): {gc:.3f}")

if __name__ == "__main__":
    main()
