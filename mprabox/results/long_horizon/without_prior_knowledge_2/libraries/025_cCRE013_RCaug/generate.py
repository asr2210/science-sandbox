"""Experiment 025: 013 cCRE with reverse-complement augmentation.

Same 013 recipe (10K rare + 2.5K abundant = 50K), but for each
class take twice as many cCREs and emit each as a forward + RC pair,
then trim back to the target count. Half the entries per class are
RC of a different cCRE — keeping per-class diversity equal to 013.

Concretely: for each class, draw 2*N unique cCREs, take the first N
forward, the next N as RC. Result: same per-class count, but each
class effectively covers 2N distinct cCRE midpoints, with half
strand-flipped.

Hypothesis: explicit RC augmentation gives strand-invariance lift
typical of genomic CNNs (+0.005-0.015), if prepare.py's training
doesn't already do RC augmentation internally.
"""
import os
import numpy as np
import twobitreader
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

CLASS_COUNTS = {
    "PLS":         10_000,
    "CA-CTCF":     10_000,
    "CA-TF":       10_000,
    "CA-H3K4me3":  10_000,
    "pELS":         2_500,
    "dELS":         2_500,
    "CA":           2_500,
    "TF":           2_500,
}
assert sum(CLASS_COUNTS.values()) == N_SEQS

COMP = str.maketrans("ACGTN", "TGCAN")


def revcomp(s):
    return s.translate(COMP)[::-1]


def load_cCREs():
    by_cls = defaultdict(list)
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end, cls = p[0], int(p[1]), int(p[2]), p[9]
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            by_cls[cls].append((chrom, mid))
    return by_cls


def load_chrom_seqs(tb):
    seqs = {}
    for c in sorted(MAIN_CHROMS):
        print(f"  loading {c}...", flush=True)
        seqs[c] = tb[c][:].upper()
    return seqs


def clean_seq(raw, rng):
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in raw)


def extract_window(chrom_seqs, chrom, mid, rng):
    s = mid - HALF
    e = mid + HALF
    L = len(chrom_seqs[chrom])
    if s < 0 or e > L:
        return None
    raw = chrom_seqs[chrom][s:e]
    if len(raw) != SEQ_LEN:
        return None
    return clean_seq(raw, rng)


def generate(seed, by_cls, chrom_seqs):
    rng = np.random.default_rng(seed)
    out = []
    for cls, n_take in CLASS_COUNTS.items():
        pool = by_cls[cls]
        # Need ~2N distinct cCREs (half forward, half RC)
        # Pull a 5% buffer in case some windows fall off chrom edges
        n_distinct = min(int(n_take * 2.1), len(pool))
        idx = rng.choice(len(pool), size=n_distinct, replace=False)
        n_per = n_take // 2  # = N (half forward, half RC)
        # if n_take is odd, give the extra to the forward half
        n_fwd = n_take - n_per
        n_rc = n_per
        added_fwd, added_rc = 0, 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract_window(chrom_seqs, chrom, mid, rng)
            if seq is None:
                continue
            if added_fwd < n_fwd:
                out.append(seq)
                added_fwd += 1
            elif added_rc < n_rc:
                out.append(revcomp(seq))
                added_rc += 1
            if added_fwd == n_fwd and added_rc == n_rc:
                break
        assert added_fwd == n_fwd and added_rc == n_rc, (
            f"{cls}: fwd={added_fwd}/{n_fwd}, rc={added_rc}/{n_rc}"
        )
    rng.shuffle(out)
    return out


def main():
    print("loading cCREs...")
    by_cls = load_cCREs()
    for cls in CLASS_COUNTS:
        print(f"  {cls}: pool={len(by_cls[cls]):,}, take={CLASS_COUNTS[cls]:,}")
    print("loading hg38 main chromosomes into memory...")
    tb = twobitreader.TwoBitFile(TWOBIT)
    chrom_seqs = load_chrom_seqs(tb)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls, chrom_seqs)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
