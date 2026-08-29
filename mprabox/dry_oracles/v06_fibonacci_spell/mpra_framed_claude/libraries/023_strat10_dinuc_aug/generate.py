"""
Experiment 023: 10-bin GC strat × 2.5k unique chr22 + dinuc-shuffle aug.

Combines the two best moves so far:
  - 013's 10-bin GC granularity (eval_01 = 0.1375)
  - 018's dinuc-shuffle 2x augmentation (eval_01 = 0.1367, ties 012)

Hypothesis: 10 bins × 2,500 unique chr22 windows × 2 versions
(real + dinuc-shuffled) = 50,000 retains 013's granularity benefit
AND adds dinuc-equivalent variety. May give a small but real lift.
"""

import os
import random
from collections import defaultdict

N_UNIQUE = 25_000
SEQ_LEN = 200
SEED = 42
N_BINS = 10
PER_BIN = N_UNIQUE // N_BINS  # 2500

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
    if n < 2: return seq
    first, last = seq[0], seq[-1]
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
        order = [last]; idx = 0
        while idx < len(order):
            u = order[idx]; idx += 1
            preds = list(rev.get(u, []))
            rng.shuffle(preds)
            for p in preds:
                if p not in visited:
                    visited.add(p); last_edge[p] = u; order.append(p)
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
            if cur not in edges or not edges[cur]: break
            nxt = edges[cur].pop(0); result.append(nxt); cur = nxt
        if len(result) == n:
            return "".join(result)
    chars = list(seq); rng.shuffle(chars)
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
        shuffled = bin_pool.copy()
        rng.shuffle(shuffled)
        chosen = [pos for _, pos in shuffled[:PER_BIN]]
        chosen_positions.extend(chosen)
        if b in (0, 4, 9):
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                  f"chose {len(chosen)}")
    print(f"Unique positions: {len(set(chosen_positions))}")

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    written = 0
    with open(out, "w") as f:
        for pos in chosen_positions:
            w = chr22[pos:pos + SEQ_LEN]
            w1 = revcomp(w) if rng.random() < 0.5 else w
            f.write(w1 + "\n"); written += 1
            shuf = euler_dinuc_shuffle(w, rng)
            w2 = revcomp(shuf) if rng.random() < 0.5 else shuf
            f.write(w2 + "\n"); written += 1
    print(f"Total written: {written}")

if __name__ == "__main__":
    main()
