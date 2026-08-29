"""
Experiment 018: GC-stratified chr22 + dinucleotide-shuffle augmentation.

Theory:
  012 (5-bin GC strat, 50k unique windows) gave eval_01 = 0.1367.
  013 (10-bin GC strat, 50k unique windows) gave eval_01 = 0.1375.
  009 (random chr22 dinuc-shuffled) gave eval_01 = 0.1333.

  Dinucleotide-shuffled chr22 preserves composition but destroys
  higher-order structure (motifs, repeats). It performs equivalently
  to natural chr22 random (0.133 vs 0.134), confirming the model
  learns dinuc-composition.

  Hypothesis: combining real and dinuc-shuffled versions of the same
  GC-stratified windows gives the model MORE training-sequence
  variety at the SAME compositional content per bin. This should
  help generalization to unseen sequences with similar composition.

Design:
  5 GC quantile bins of chr22 windows (stride=50).
  Pick 5,000 unique windows per bin (25,000 total).
  For each: write the original AND its dinucleotide-shuffled version.
  Total = 50,000. Random orientation per output. Seed=42.
"""

import os
import random
from collections import defaultdict

N_UNIQUE = 25_000
SEQ_LEN = 200
SEED = 42
N_BINS = 5
PER_BIN = N_UNIQUE // N_BINS  # 5000

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

def euler_dinuc_shuffle(seq, rng):
    n = len(seq)
    if n < 2:
        return seq
    first = seq[0]
    last = seq[-1]
    out = defaultdict(list)
    for i in range(n - 1):
        out[seq[i]].append(seq[i + 1])

    for _ in range(50):
        rev = defaultdict(list)
        for v, neigh in out.items():
            for w in neigh:
                rev[w].append(v)
        last_edge = {}
        visited = {last}
        order = [last]
        idx = 0
        while idx < len(order):
            u = order[idx]; idx += 1
            preds = list(rev.get(u, []))
            rng.shuffle(preds)
            for p in preds:
                if p not in visited:
                    visited.add(p)
                    last_edge[p] = u
                    order.append(p)
        if first not in visited and first != last:
            continue
        edges = {v: list(neigh) for v, neigh in out.items()}
        for v in edges:
            if v != last and v in last_edge:
                edges[v].remove(last_edge[v])
                rng.shuffle(edges[v])
                edges[v].append(last_edge[v])
            else:
                rng.shuffle(edges[v])
        result = [first]; cur = first
        for _ in range(n - 1):
            if cur not in edges or not edges[cur]:
                break
            nxt = edges[cur].pop(0)
            result.append(nxt); cur = nxt
        if len(result) == n:
            return "".join(result)
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)

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
    chosen_positions = []
    for b in range(N_BINS):
        lo = (b * n) // N_BINS
        hi = ((b + 1) * n) // N_BINS
        bin_pool = candidates[lo:hi]
        print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
              f"n={len(bin_pool):,}")
        shuffled = bin_pool.copy()
        rng.shuffle(shuffled)
        chosen = [pos for _, pos in shuffled[:PER_BIN]]
        chosen_positions.extend(chosen)
        print(f"  -> chose {len(chosen)} for bin {b}")
    print(f"Unique positions: {len(set(chosen_positions))}")

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    written = 0
    with open(out, "w") as f:
        for pos in chosen_positions:
            w = chr22[pos:pos + SEQ_LEN]
            # Write original (random orientation)
            w1 = revcomp(w) if rng.random() < 0.5 else w
            f.write(w1 + "\n")
            written += 1
            # Write dinuc-shuffled version (random orientation)
            shuf = euler_dinuc_shuffle(w, rng)
            w2 = revcomp(shuf) if rng.random() < 0.5 else shuf
            f.write(w2 + "\n")
            written += 1
    print(f"Total written: {written}")

if __name__ == "__main__":
    main()
