"""
Experiment 015: Joint GC stratification across chr19+chr22.

Theory:
  012-014 plateau near eval_01 = 0.137 with chr22-only stratified
  designs. To extend the compositional range I add chr19, the most
  GC-rich human autosome (mean GC ~0.48, with a heavier high-GC
  tail than chr22's ~0.42 mean GC).

  Hypothesis: a joint 5-bin GC pool spanning chr19+chr22 will:
  - extend the high-GC tail with more diverse, high-quality high-GC
    sequences (chr19 has many CpG islands and gene-dense regions)
  - keep enough chr22 in the mid/low bins
  giving broader compositional coverage at each bin.

Design:
  Sliding window stride=50 over chr19 and chr22 separately.
  Compute GC of each window. Combine pools, sort, bin into 5 equal
  quantile bins of the combined pool. Sample 10k unique positions per
  bin = 50k total. Random orientation. Seed=42.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 5
PER_BIN = N_SEQS // N_BINS  # 10000

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

def collect_windows(seq, chrom_label, stride=50):
    L = len(seq)
    out = []
    i = 0
    while i + SEQ_LEN <= L:
        w = seq[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            out.append((gc, chrom_label, i))
        i += stride
    return out

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    chr19 = load_fasta("data/chr19.fa")
    chroms = {"chr22": chr22, "chr19": chr19}
    cand22 = collect_windows(chr22, "chr22")
    cand19 = collect_windows(chr19, "chr19")
    print(f"chr22 windows: {len(cand22):,}, chr19 windows: {len(cand19):,}")
    candidates = cand22 + cand19
    candidates.sort()
    n = len(candidates)
    print(f"Combined: {n:,}, GC range: {candidates[0][0]:.3f}-{candidates[-1][0]:.3f}")
    sampled = set()
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = candidates[lo:hi]
            c22 = sum(1 for _, c, _ in bin_pool if c == "chr22")
            c19 = sum(1 for _, c, _ in bin_pool if c == "chr19")
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                  f"n={len(bin_pool):,} (chr22={c22}, chr19={c19})")
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            c22_chosen = 0
            c19_chosen = 0
            for gc, chrom, pos in shuffled:
                key = (chrom, pos)
                if key in sampled:
                    continue
                chosen.append((gc, chrom, pos))
                sampled.add(key)
                if chrom == "chr22":
                    c22_chosen += 1
                else:
                    c19_chosen += 1
                if len(chosen) >= PER_BIN:
                    break
            print(f"  -> chose {len(chosen)}: chr22={c22_chosen}, chr19={c19_chosen}")
            for gc, chrom, pos in chosen:
                w = chroms[chrom][pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out_path))
    print(f"Total written: {n_written}")
    if n_written != N_SEQS:
        print(f"WARNING: wrote {n_written}, expected {N_SEQS}")

if __name__ == "__main__":
    main()
