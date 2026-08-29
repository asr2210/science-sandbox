"""
Experiment 013: Finer-grained stratified-GC mix of chr22 windows.

Theory:
  012 used 5 GC quantile bins x 10k each = 50k, achieving the first
  plateau break (eval_01 = 0.1367 vs 003's 0.1341).

  Hypothesis: if "compositional breadth" is the right axis, then a
  finer-grained stratification (10 bins x 5k each) should extract more
  benefit by hitting more compositional cells. If 5 bins already
  captured most of the benefit, 013 should be ~equal to 012.

Design:
  Sliding-window chr22 with stride=50 (same as 012). Compute GC of each.
  Sort and bin into 10 equal quantile bins. Sample 5k unique positions
  per bin = 50k total. Random orientation. Seed=42.
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
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            candidates.append((gc, i))
        i += stride
    print(f"Candidate windows (stride=50): {len(candidates):,}")
    candidates.sort()
    n = len(candidates)
    sampled_positions = set()
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = candidates[lo:hi]
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                  f"n={len(bin_pool):,}")
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            for gc, pos in shuffled:
                if pos in sampled_positions:
                    continue
                chosen.append((gc, pos))
                sampled_positions.add(pos)
                if len(chosen) >= PER_BIN:
                    break
            print(f"  -> chose {len(chosen)} from bin {b}")
            for gc, pos in chosen:
                w = chr22[pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")
    if n_written != N_SEQS:
        print(f"WARNING: wrote {n_written}, expected {N_SEQS}")

if __name__ == "__main__":
    main()
