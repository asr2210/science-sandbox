"""Experiment 008: uniform sample of DHS Index elements.

Meuleman 2020 DHS Index: ~3.59M DNase-hypersensitive sites with NMF
component labels (16 tissue/cell-type components). Sample 50K uniformly,
extract 200bp centered on summit. Sister to experiment 002 (which used
ENCODE cCREs). Tests whether annotation source matters.
"""
import gzip
import os
import numpy as np
import twobitreader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DHS = os.path.join(ROOT, "data", "DHS", "DHS_Index_hg38.txt.gz")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_dhs():
    rows = []
    with gzip.open(DHS, "rt") as f:
        next(f)  # header
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, summit = p[0], int(p[6])
            if chrom not in MAIN_CHROMS:
                continue
            rows.append((chrom, summit))
    return rows


def extract(tb, chrom, mid, rng):
    L = len(tb[chrom])
    s, e = mid - HALF, mid + HALF
    if s < 0 or e > L:
        return None
    seq = tb[chrom][s:e].upper()
    if len(seq) != SEQ_LEN:
        return None
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)


def generate(seed, dhs_rows, tb):
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(dhs_rows), size=int(N_SEQS * 1.05), replace=False)
    out = []
    for j in idx:
        chrom, summit = dhs_rows[j]
        seq = extract(tb, chrom, summit, rng)
        if seq is not None:
            out.append(seq)
            if len(out) == N_SEQS:
                break
    assert len(out) == N_SEQS
    return out


def main():
    print(f"loading DHS index...")
    dhs_rows = load_dhs()
    print(f"  {len(dhs_rows):,} DHS elements on main chroms")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, dhs_rows, tb)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
