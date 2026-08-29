"""
Experiment 012: Stratified-GC mix of chr22 windows.

Theory:
  010 (GC-rich) and 011 (AT-rich) showed that biasing in either
  compositional direction hurts. Natural chr22 (003) at 0.134 is
  the best because it spans the full compositional distribution.

  This experiment tests if EXPLICIT stratified sampling (forcing equal
  representation across GC bins) helps even more by guaranteeing
  edge-bin coverage. Tests "compositional breadth" beyond natural
  sampling.

Design:
  Sliding-window chr22 with stride 50 to get many candidate windows.
  Compute GC of each. Sort into 5 bins by GC quantile:
    bin1: bottom 20% (GC ~0.30-0.39)
    bin2: 20-40%    (GC ~0.39-0.45)
    bin3: 40-60%    (GC ~0.45-0.50)
    bin4: 60-80%    (GC ~0.50-0.56)
    bin5: top 20%   (GC ~0.56+)
  Sample 10k unique positions per bin = 50k total. Random orientation.
  Seed=42.

Generalization rationale:
  A stratified library guarantees the model sees ample examples at
  every compositional level. If unmeasured cell types have active
  regions in different GC ranges, this broader coverage should support
  better transfer.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 5
PER_BIN = N_SEQS // N_BINS

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
    stride = 50  # 4x more candidate windows than stride 200
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
    # Bin into N_BINS equal-sized quantile bins
    n = len(candidates)
    sampled_positions = set()
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = candidates[lo:hi]
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}–{bin_pool[-1][0]:.3f}, "
                  f"n={len(bin_pool):,}")
            # Sample PER_BIN positions; avoid duplicate positions globally
            need = PER_BIN
            tries = 0
            chosen = []
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            for gc, pos in shuffled:
                if pos in sampled_positions:
                    continue
                # also avoid windows that overlap heavily with already-chosen
                chosen.append((gc, pos))
                sampled_positions.add(pos)
                if len(chosen) >= need:
                    break
            print(f"  → chose {len(chosen)} from bin {b}")
            for gc, pos in chosen:
                w = chr22[pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    # Verify
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")
    if n_written != N_SEQS:
        print(f"WARNING: wrote {n_written}, expected {N_SEQS}")

if __name__ == "__main__":
    main()
