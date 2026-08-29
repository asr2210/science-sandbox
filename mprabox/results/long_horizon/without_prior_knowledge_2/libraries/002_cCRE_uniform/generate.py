"""Experiment 002: 50K cCREs sampled uniformly, 200bp centered on midpoint.

Per-seed: pick 50K cCREs at random (without replacement) from the 2.35M
ENCODE V4 cCREs (ENCFF420VPZ.bed). Extract a 200bp window centered on
each element's midpoint from hg38.2bit. Uppercase. Any N bases get
replaced by uniform random ACGT.
"""
import os
import sys
import numpy as np
import twobitreader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_cCREs():
    """Return list of (chrom, midpoint) for cCREs on main chromosomes."""
    rows = []
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end = p[0], int(p[1]), int(p[2])
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            rows.append((chrom, mid))
    return rows


def extract(tb, chrom, mid, rng):
    """Extract a 200bp uppercase ACGT window centered at mid."""
    chrom_len = len(tb[chrom])
    start = mid - HALF
    end = mid + HALF
    if start < 0 or end > chrom_len:
        return None
    seq = tb[chrom][start:end].upper()
    if len(seq) != SEQ_LEN:
        return None
    # replace any non-ACGT (N or other) with uniform random ACGT
    out = []
    for c in seq:
        if c in "ACGT":
            out.append(c)
        else:
            out.append(ALPHABET[rng.integers(0, 4)])
    return "".join(out)


def generate(seed: int, cCREs, tb) -> list[str]:
    rng = np.random.default_rng(seed)
    n_total = len(cCREs)
    # oversample by 5% to absorb extraction failures (chrom edges)
    target = int(N_SEQS * 1.05)
    idx = rng.choice(n_total, size=target, replace=False)
    out = []
    for i in idx:
        chrom, mid = cCREs[i]
        seq = extract(tb, chrom, mid, rng)
        if seq is not None:
            out.append(seq)
            if len(out) == N_SEQS:
                break
    if len(out) < N_SEQS:
        raise RuntimeError(f"only got {len(out)} sequences, need {N_SEQS}")
    return out


def main():
    print("loading cCREs...")
    cCREs = load_cCREs()
    print(f"  {len(cCREs):,} cCREs on main chromosomes")
    print("opening 2bit...")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, cCREs, tb)
        out = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out}")


if __name__ == "__main__":
    main()
