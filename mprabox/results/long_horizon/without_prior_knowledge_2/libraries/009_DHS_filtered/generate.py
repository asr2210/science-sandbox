"""Experiment 009: DHS Index filtered to high-quality peaks.

Filter DHS to top-quartile mean_signal AND numsamples>=5 (681,721
elements remaining), then uniform sample 50K. 200bp centered on summit.
Tests whether 008's underperformance vs cCRE was driven by weak/rare
DHS calls (peak-quality noise) or by something the cCRE pipeline does
beyond peak filtering (e.g., regulatory class typing).
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
SIG_QUANTILE = 0.75
MIN_SAMPLES = 5


def load_dhs_filtered():
    rows = []
    sigs = []
    with gzip.open(DHS, "rt") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in MAIN_CHROMS:
                continue
            sig = float(p[4])
            ns = int(p[5])
            summit = int(p[6])
            rows.append((chrom, summit, sig, ns))
            sigs.append(sig)
    sig_thresh = float(np.quantile(np.array(sigs), SIG_QUANTILE))
    filtered = [(c, s) for (c, s, sig, ns) in rows if sig >= sig_thresh and ns >= MIN_SAMPLES]
    return filtered, sig_thresh


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
    print("loading + filtering DHS index...")
    dhs_rows, sig_thresh = load_dhs_filtered()
    print(f"  sig_thresh (q{SIG_QUANTILE})={sig_thresh:.3f}, min_samples={MIN_SAMPLES}")
    print(f"  {len(dhs_rows):,} filtered DHS elements")
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
