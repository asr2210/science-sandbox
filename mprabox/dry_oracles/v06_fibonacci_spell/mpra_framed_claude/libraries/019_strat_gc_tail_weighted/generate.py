"""
Experiment 019: Tail-weighted GC stratification of chr22 windows.

Theory:
  012 (uniform 5-bin × 10k) gave eval_01 = 0.1367.
  013 (uniform 10-bin × 5k) gave eval_01 = 0.1375 (best so far).
  010 (GC-rich only) and 011 (AT-rich only) both lost.

  Both pure-tail biases hurt because they NARROW composition. But the
  benefit of stratification comes from BREADTH at the tails. So:
  maybe OVER-allocating to tails (within full coverage) helps.

  Hypothesis: tail-weighted (15k bin0 + 7.5k bin1 + 5k bin2 + 7.5k bin3
  + 15k bin4 = 50k) keeps full coverage but emphasizes extremes.
  If model learns better at the tails, this should lift eval_01 above
  0.1375.

Design:
  5 GC quantile bins from chr22 (stride=50).
  Allocations: [15000, 7500, 5000, 7500, 15000].
  Random orientation. Seed=42.
"""

import os
import random

SEQ_LEN = 200
SEED = 42
N_BINS = 5
ALLOCS = [15000, 7500, 5000, 7500, 15000]
assert sum(ALLOCS) == 50_000

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
    print(f"Candidate windows: {len(candidates):,}")
    candidates.sort()
    n = len(candidates)
    sampled = set()
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for b, need in enumerate(ALLOCS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = candidates[lo:hi]
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                  f"pool={len(bin_pool):,}, need={need}")
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            for gc, pos in shuffled:
                if pos in sampled:
                    continue
                chosen.append((gc, pos))
                sampled.add(pos)
                if len(chosen) >= need:
                    break
            print(f"  -> chose {len(chosen)}")
            for gc, pos in chosen:
                w = chr22[pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
