"""Experiment 005: random 200bp genomic windows from hg38.

50K random 200bp windows sampled uniformly across the GRCh38 main
chromosomes (chr1-22, X, Y). NOT cCRE-selected. Skip windows with
>10% N. Replace remaining Ns with uniform random ACGT.

Tests where the cCRE benefit comes from:
  - 005 ≈ 001 → genomic context per se doesn't help; cCRE selection matters
  - 005 ≈ 002 → any genomic context is sufficient
  - 005 between → both genomic context AND regulatory selection contribute
"""
import os
import sys
import numpy as np
import twobitreader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
MAX_N_FRAC = 0.10
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]


def generate(seed, tb):
    rng = np.random.default_rng(seed)
    chrom_lens = np.array([len(tb[c]) for c in MAIN_CHROMS], dtype=np.int64)
    weights = chrom_lens / chrom_lens.sum()
    out = []
    attempts = 0
    max_attempts = N_SEQS * 10
    while len(out) < N_SEQS and attempts < max_attempts:
        attempts += 1
        ci = rng.choice(len(MAIN_CHROMS), p=weights)
        chrom = MAIN_CHROMS[ci]
        L = chrom_lens[ci]
        start = int(rng.integers(0, L - SEQ_LEN))
        end = start + SEQ_LEN
        seq = tb[chrom][start:end].upper()
        if len(seq) != SEQ_LEN:
            continue
        n_count = sum(1 for c in seq if c not in "ACGT")
        if n_count > MAX_N_FRAC * SEQ_LEN:
            continue
        if n_count > 0:
            seq = "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)
        out.append(seq)
    if len(out) < N_SEQS:
        raise RuntimeError(f"only {len(out)} after {attempts} attempts")
    return out


def main():
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, tb)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
