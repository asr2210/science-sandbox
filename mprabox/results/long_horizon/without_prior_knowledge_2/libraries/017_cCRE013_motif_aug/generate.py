"""Experiment 017: 013-style cCRE + one inserted JASPAR motif per seq.

Take 013 sampling (10K each rare; 2.5K each abundant). For each 200bp
sequence, sample one of 20 JASPAR archetype motifs uniformly, sample
an instance from the PFM column probabilities, and overwrite a
random-position window with that instance.

Tests whether motif density is an axis of informativeness independent
of class balance (T5 refinement on the optimal class-balance library).
"""
import os
import numpy as np
import twobitreader
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")
JASPAR = os.path.join(ROOT, "data", "motifs", "JASPAR2024_CORE_vertebrates_nr.jaspar")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

CLASS_COUNTS = {
    "PLS": 10_000, "CA-CTCF": 10_000, "CA-TF": 10_000, "CA-H3K4me3": 10_000,
    "pELS": 2_500, "dELS": 2_500, "CA": 2_500, "TF": 2_500,
}
assert sum(CLASS_COUNTS.values()) == N_SEQS

# 20 archetypal JASPAR motifs (same as 010)
MOTIF_IDS = [
    "MA0139", "MA0079", "MA0476", "MA0105", "MA0137", "MA0035", "MA0148",
    "MA0114", "MA0090", "MA0024", "MA0058", "MA0142", "MA0106", "MA0002",
    "MA0768", "MA0143", "MA0162", "MA0594", "MA0113", "MA0605",
]


def load_pfms():
    """Return list of (id, prob[4xW], width) for the 20 archetypes."""
    pfms = []
    with open(JASPAR) as f:
        lines = f.read().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith(">"):
            i += 1
            continue
        mid = line[1:].split("\t")[0].split(".")[0]
        if mid not in MOTIF_IDS:
            i += 5
            continue
        rows = []
        for k in range(4):
            row = lines[i + 1 + k]
            nums = row.split("[")[1].split("]")[0].split()
            rows.append([float(x) for x in nums])
        m = np.array(rows)
        prob = (m + 0.5) / (m.sum(axis=0, keepdims=True) + 2.0)  # 4xW
        pfms.append((mid, prob, prob.shape[1]))
        i += 5
    assert len(pfms) == len(MOTIF_IDS), f"{len(pfms)} != {len(MOTIF_IDS)}"
    return pfms


def sample_instance(prob, rng):
    """Sample a length-W string from PFM column probabilities."""
    W = prob.shape[1]
    bases = []
    for j in range(W):
        bases.append(ALPHABET[rng.choice(4, p=prob[:, j])])
    return "".join(bases)


def load_cCREs_by_class():
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


def extract(tb, chrom, mid, rng):
    L = len(tb[chrom])
    s, e = mid - HALF, mid + HALF
    if s < 0 or e > L:
        return None
    seq = tb[chrom][s:e].upper()
    if len(seq) != SEQ_LEN:
        return None
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)


def insert_motif(seq, pfms, rng):
    mid_idx = rng.integers(0, len(pfms))
    _, prob, W = pfms[mid_idx]
    inst = sample_instance(prob, rng)
    pos = int(rng.integers(0, SEQ_LEN - W + 1))
    return seq[:pos] + inst + seq[pos + W:]


def generate(seed, by_cls, tb, pfms):
    rng = np.random.default_rng(seed)
    out = []
    for cls, n_take in CLASS_COUNTS.items():
        pool = by_cls[cls]
        n_draw = min(int(n_take * 1.05), len(pool))
        idx = rng.choice(len(pool), size=n_draw, replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract(tb, chrom, mid, rng)
            if seq is not None:
                seq = insert_motif(seq, pfms, rng)
                assert len(seq) == SEQ_LEN
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{cls}: got {added}, want {n_take}"
    rng.shuffle(out)
    return out


def main():
    print("loading PFMs...")
    pfms = load_pfms()
    widths = [w for _, _, w in pfms]
    print(f"  {len(pfms)} archetypes, widths {min(widths)}-{max(widths)}")
    by_cls = load_cCREs_by_class()
    for cls in CLASS_COUNTS:
        print(f"  {cls}: pool={len(by_cls[cls]):,}, take={CLASS_COUNTS[cls]:,}")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls, tb, pfms)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
