"""
Experiment 011: AT-rich chr22 windows.

Theory:
  010 showed GC-rich biasing hurts (0.119 vs 0.134). Test other direction.
  If AT-rich also hurts → ANY compositional narrowing hurts.
  If AT-rich ≈ chr22 random → GC-rich was specifically bad.

Design:
  Bottom 30% of chr22 200bp windows by GC, expanded with 50bp-shift
  neighbors if needed. Random orientation. Seed=42.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
GC_QUANTILE = 0.30

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
    stride = 200
    candidates = []
    i = 0
    while i + SEQ_LEN <= L:
        w = chr22[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            candidates.append((gc, i))
        i += stride
    print(f"Non-overlapping valid windows: {len(candidates):,}")
    candidates.sort()
    cutoff = int(len(candidates) * GC_QUANTILE)
    bottom = candidates[:cutoff]
    print(f"Bottom {GC_QUANTILE*100:.0f}% pool: {len(bottom):,}, "
          f"GC range: {bottom[0][0]:.3f} to {bottom[-1][0]:.3f}")
    if len(bottom) < N_SEQS:
        expanded = list(bottom)
        for gc, pos in bottom:
            for offset in (50, 100, 150, -50, -100, -150):
                p = pos + offset
                if 0 <= p and p + SEQ_LEN <= L:
                    w = chr22[p:p + SEQ_LEN]
                    if all(c in ALPHABET for c in w):
                        g = (w.count("G") + w.count("C")) / SEQ_LEN
                        if g <= bottom[-1][0]:
                            expanded.append((g, p))
        print(f"Expanded pool: {len(expanded):,}")
        bottom = expanded
    positions = list({pos: gc for gc, pos in bottom}.keys())
    if len(positions) < N_SEQS:
        sampled = [rng.choice(positions) for _ in range(N_SEQS)]
    else:
        sampled = rng.sample(positions, N_SEQS)

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for s in sampled:
            w = chr22[s:s + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            f.write(w + "\n")
    gcs = [(line.count("G") + line.count("C")) / SEQ_LEN
           for line in open(out)]
    print(f"Wrote {N_SEQS}. Mean GC = {sum(gcs)/len(gcs):.3f}, "
          f"min={min(gcs):.3f}, max={max(gcs):.3f}")

if __name__ == "__main__":
    main()
