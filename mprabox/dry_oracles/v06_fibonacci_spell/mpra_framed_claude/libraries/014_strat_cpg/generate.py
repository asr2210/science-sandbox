"""
Experiment 014: CpG-density stratified chr22 windows.

Theory:
  012 (5-bin GC) and 013 (10-bin GC) plateaued near eval_01=0.137.
  GC content alone is exhausted as a stratification axis.

  CpG dinucleotide density is biologically distinctive (CpG islands,
  promoters, methylation) and only PARTLY correlated with GC content:
  a sequence can be high-GC but CpG-depleted (CpG suppression from
  cytosine deamination in methylated regions). So CpG density is a
  partially-independent compositional axis.

  Hypothesis: stratifying by CpG density (instead of total GC) gives
  comparable or better coverage of the regulatory-active sequence
  space, because CpG density correlates with promoter/enhancer
  activity in a way that total GC does not.

Design:
  Sliding-window chr22 with stride=50. Compute CpG count per 200bp
  window (count of "CG" dinucleotides, max possible 199). Sort and
  bin into 5 quantile bins. Sample 10k unique positions per bin = 50k.
  Random orientation. Seed=42.
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

def cpg_count(s):
    # count overlapping "CG" occurrences
    n = 0
    for i in range(len(s) - 1):
        if s[i] == "C" and s[i+1] == "G":
            n += 1
    return n

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    L = len(chr22)
    stride = 50
    candidates = []
    i = 0
    while i + SEQ_LEN <= L:
        w = chr22[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            cpg = cpg_count(w)
            candidates.append((cpg, i))
        i += stride
    print(f"Candidate windows (stride=50): {len(candidates):,}")
    candidates.sort()
    n = len(candidates)
    sampled_positions = set()
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    bin_gc_means = []
    with open(out, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = candidates[lo:hi]
            print(f"Bin {b}: CpG {bin_pool[0][0]}-{bin_pool[-1][0]}, "
                  f"n={len(bin_pool):,}")
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            for cpg, pos in shuffled:
                if pos in sampled_positions:
                    continue
                chosen.append((cpg, pos))
                sampled_positions.add(pos)
                if len(chosen) >= PER_BIN:
                    break
            # GC stats for this bin
            bin_gcs = []
            for cpg, pos in chosen:
                w = chr22[pos:pos + SEQ_LEN]
                bin_gcs.append((w.count("G") + w.count("C")) / SEQ_LEN)
            mean_gc = sum(bin_gcs) / len(bin_gcs) if bin_gcs else 0
            bin_gc_means.append(mean_gc)
            print(f"  -> chose {len(chosen)} from bin {b}, mean GC={mean_gc:.3f}")
            for cpg, pos in chosen:
                w = chr22[pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")
    print(f"Bin mean GCs: {[f'{g:.3f}' for g in bin_gc_means]}")
    if n_written != N_SEQS:
        print(f"WARNING: wrote {n_written}, expected {N_SEQS}")

if __name__ == "__main__":
    main()
