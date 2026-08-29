"""Experiment 010: TF-motif × cCRE-class stratified library.

Within each cCRE class (8), bin by dominant JASPAR-archetype motif
(20 TF families + a "no-strong-motif" bucket). Sample 50K with a per-bin
cap to upweight rare (class × TF) combinations.

Tests whether motif-level diversity is a separate axis of library
informativeness beyond cCRE class diversity (refines T5).
"""
import os
import sys
import numpy as np
import twobitreader
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")
JASPAR = os.path.join(ROOT, "data", "motifs", "JASPAR2024_CORE_vertebrates_nr.jaspar")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
BASE2IDX = {"A": 0, "C": 1, "G": 2, "T": 3}
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
CLASSES = ["PLS", "pELS", "dELS", "CA-CTCF", "CA-H3K4me3", "CA-TF", "CA", "TF"]
N_PRESCAN_PER_CLASS = 25_000   # candidate pool per class to bin

# 20 archetypal JASPAR motifs spanning major TF families
MOTIF_IDS = [
    "MA0139", "MA0079", "MA0476", "MA0105", "MA0137", "MA0035", "MA0148",
    "MA0114", "MA0090", "MA0024", "MA0058", "MA0142", "MA0106", "MA0002",
    "MA0768", "MA0143", "MA0162", "MA0594", "MA0113", "MA0605",
]
SCORE_THRESHOLD = 6.0  # bits-equivalent log-odds; sequences below get "BG" bin
PER_BIN_CAP = 320      # 8 classes * 21 bins = 168 → ~298 per bin if balanced


def load_pwms():
    """Return list of (id, name, log_odds_pwm[4xW], width)."""
    pwms = []
    with open(JASPAR) as f:
        lines = f.read().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith(">"):
            i += 1
            continue
        header = line[1:].split("\t")
        mid_full, name = header[0], header[1] if len(header) > 1 else ""
        mid = mid_full.split(".")[0]
        if mid not in MOTIF_IDS:
            i += 5
            continue
        rows = []
        for k in range(4):
            row = lines[i + 1 + k]
            nums = row.split("[")[1].split("]")[0].split()
            rows.append([float(x) for x in nums])
        m = np.array(rows)  # 4xW
        # Convert counts to probabilities with pseudocount
        m = (m + 0.5) / (m.sum(axis=0, keepdims=True) + 2.0)
        # Log-odds vs uniform background 0.25
        lo = np.log2(m / 0.25)
        pwms.append((mid, name, lo, m.shape[1]))
        i += 5
    return pwms


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


def seq_to_idx(seq):
    return np.array([BASE2IDX[c] for c in seq], dtype=np.int8)


def revcomp_idx(idx):
    return 3 - idx[::-1]


def score_pwm_max(seq_idx, lo, w):
    """Best log-odds score for any window in seq, considering both strands."""
    L = len(seq_idx)
    if L < w:
        return -1e9
    # Forward strand: windows shape (L-w+1, w); per-pos lookup
    fwd_scores = np.zeros(L - w + 1, dtype=np.float32)
    for j in range(w):
        fwd_scores += lo[seq_idx[j:L - w + 1 + j], j]
    rc = revcomp_idx(seq_idx)
    rev_scores = np.zeros(L - w + 1, dtype=np.float32)
    for j in range(w):
        rev_scores += lo[rc[j:L - w + 1 + j], j]
    return max(fwd_scores.max(), rev_scores.max())


def best_motif_bin(seq, pwms):
    seq_idx = seq_to_idx(seq)
    best_score = -1e9
    best_id = "BG"
    for mid, name, lo, w in pwms:
        s = score_pwm_max(seq_idx, lo, w)
        if s > best_score:
            best_score = s
            best_id = mid
    if best_score < SCORE_THRESHOLD:
        return "BG"
    return best_id


def generate(seed, by_cls, tb, pwms):
    rng = np.random.default_rng(seed)
    # Step 1: pre-sample N_PRESCAN_PER_CLASS per class, extract sequences
    prescan = []  # list of (class, seq)
    for cls in CLASSES:
        pool = by_cls[cls]
        n_take = min(N_PRESCAN_PER_CLASS, len(pool))
        n_draw = min(int(n_take * 1.05), len(pool))
        idx = rng.choice(len(pool), size=n_draw, replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract(tb, chrom, mid, rng)
            if seq is not None:
                prescan.append((cls, seq))
                added += 1
                if added == n_take:
                    break
    print(f"  pre-scanned {len(prescan):,} sequences")

    # Step 2: bin by (class, best_motif)
    bins = defaultdict(list)  # (cls, mid) -> [seqs]
    for cls, seq in prescan:
        b = best_motif_bin(seq, pwms)
        bins[(cls, b)].append(seq)
    print(f"  {len(bins)} (class × motif) bins")
    counts = Counter({k: len(v) for k, v in bins.items()})
    top5 = counts.most_common(5)
    print(f"  top-5 bins: {top5}")

    # Step 3: sample with per-bin cap, then top up to N_SEQS uniformly
    out = []
    for k, vs in bins.items():
        rng.shuffle(vs)
        out.extend(vs[:PER_BIN_CAP])
    print(f"  capped sample: {len(out):,}")

    if len(out) < N_SEQS:
        # Top up: weighted draw from remaining (smaller bins fully used,
        # larger bins still have leftovers). Take leftovers proportional
        # to bin remaining size capped by what's left.
        leftover = []
        for (cls, b), vs in bins.items():
            leftover.extend(vs[PER_BIN_CAP:])
        rng.shuffle(leftover)
        need = N_SEQS - len(out)
        out.extend(leftover[:need])
    elif len(out) > N_SEQS:
        rng.shuffle(out)
        out = out[:N_SEQS]

    rng.shuffle(out)
    return out


def main():
    print("loading PWMs...")
    pwms = load_pwms()
    assert len(pwms) == len(MOTIF_IDS), f"got {len(pwms)} of {len(MOTIF_IDS)}"
    print(f"  {len(pwms)} PWMs: {[name for _, name, _, _ in pwms]}")

    print("loading cCREs by class...")
    by_cls = load_cCREs_by_class()
    for cls in CLASSES:
        print(f"  {cls}: {len(by_cls[cls]):,}")

    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls, tb, pwms)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
