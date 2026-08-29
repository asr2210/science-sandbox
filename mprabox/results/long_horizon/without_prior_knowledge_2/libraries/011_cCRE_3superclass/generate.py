"""Experiment 011: cCRE 3-superclass stratification (coarser than 006).

Collapse the 8 ENCODE V4 cCRE classes into 3 functional super-classes:
- promoters: PLS + pELS + CA-H3K4me3
- distal:    dELS + CA + TF
- insul/TF:  CA-CTCF + CA-TF

Equal counts per super-class (50K / 3 ≈ 16,667 each, with rounding).
Tests T8: is the right stratification axis 3 super-classes (coarser),
8 cCRE classes (006), or 168 (class × motif) bins (010)?
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

SUPER = {
    "promoter":   ["PLS", "pELS", "CA-H3K4me3"],
    "distal":     ["dELS", "CA", "TF"],
    "insul_tf":   ["CA-CTCF", "CA-TF"],
}
N_PER_SUPER = N_SEQS // 3  # 16666; one super gets +2 to make 50000


def load_cCREs_by_super():
    by_super = defaultdict(list)
    cls_to_super = {c: s for s, cs in SUPER.items() for c in cs}
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end, cls = p[0], int(p[1]), int(p[2]), p[9]
            if chrom not in MAIN_CHROMS:
                continue
            sup = cls_to_super.get(cls)
            if sup is None:
                continue
            mid = (start + end) // 2
            by_super[sup].append((chrom, mid))
    return by_super


def extract(tb, chrom, mid, rng):
    L = len(tb[chrom])
    s, e = mid - HALF, mid + HALF
    if s < 0 or e > L:
        return None
    seq = tb[chrom][s:e].upper()
    if len(seq) != SEQ_LEN:
        return None
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)


def generate(seed, by_super, tb):
    rng = np.random.default_rng(seed)
    out = []
    supers = list(SUPER.keys())
    counts = [N_PER_SUPER] * 3
    counts[0] += N_SEQS - sum(counts)  # absorb remainder
    for sup, n_take in zip(supers, counts):
        pool = by_super[sup]
        idx = rng.choice(len(pool), size=int(n_take * 1.05), replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract(tb, chrom, mid, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{sup}: got {added}, want {n_take}"
    rng.shuffle(out)
    return out


def main():
    by_super = load_cCREs_by_super()
    for s in SUPER:
        print(f"  {s}: {len(by_super[s]):,}")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_super, tb)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
