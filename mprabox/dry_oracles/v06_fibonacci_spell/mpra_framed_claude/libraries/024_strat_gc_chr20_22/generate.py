"""
Experiment 024: Joint GC stratification across chr20+chr22.

Theory:
  013 chr22-only 10-bin GC strat = eval_01 0.1375 (best).
  015 chr19+chr22 5-bin GC strat = eval_01 0.1347 (chr19 hurt).
  T22: "unique natural chr22-compatible windows per bin" is the
  bottleneck.

  chr20 is more chr22-compatible than chr19 (similar GC profile,
  less gene-dense, less CpG-island-heavy). Combining chr20+chr22
  doubles the candidate pool with chr22-like sequences.

Design:
  chr20+chr22 stride=50 sliding windows. Combine and sort by GC.
  10 quantile bins × 5,000 each = 50k total. Random orientation.
  Seed=42.

Hypothesis: if chr20 is compatible enough, this beats 013.
If 024 ≤ 013, then even chr20 introduces incompatible distribution
shift and chr22 is unique.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 10
PER_BIN = N_SEQS // N_BINS  # 5000

ALPHABET = set("ACGT")
COMPL = str.maketrans("ACGTNacgtn", "TGCANtgcan")
def revcomp(s): return s.translate(COMPL)[::-1]

def load_fasta(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip().upper())
    return "".join(parts)

def collect(seq, label, stride=50):
    L = len(seq); out = []; i = 0
    while i + SEQ_LEN <= L:
        w = seq[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            out.append((gc, label, i))
        i += stride
    return out

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    chr20 = load_fasta("data/chr20.fa")
    chroms = {"chr22": chr22, "chr20": chr20}
    print(f"chr22: {len(chr22):,}bp, chr20: {len(chr20):,}bp")
    cand = collect(chr22, "chr22") + collect(chr20, "chr20")
    print(f"Combined candidates: {len(cand):,}")
    cand.sort()
    n = len(cand)
    sampled = set()
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = cand[lo:hi]
            c22 = sum(1 for _, c, _ in bin_pool if c == "chr22")
            c20 = sum(1 for _, c, _ in bin_pool if c == "chr20")
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            c22_chosen = c20_chosen = 0
            for gc, chrom, pos in shuffled:
                k = (chrom, pos)
                if k in sampled: continue
                chosen.append((gc, chrom, pos))
                sampled.add(k)
                if chrom == "chr22": c22_chosen += 1
                else: c20_chosen += 1
                if len(chosen) >= PER_BIN: break
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                  f"pool=chr22:{c22}/chr20:{c20}, chose chr22:{c22_chosen}/chr20:{c20_chosen}")
            for gc, chrom, pos in chosen:
                w = chroms[chrom][pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out_path))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
