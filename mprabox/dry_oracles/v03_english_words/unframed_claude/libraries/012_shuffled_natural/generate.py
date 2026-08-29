"""Exp 012: per-sequence mononucleotide-shuffled natural sequences.
Take the 50k natural sequences from Exp 006, shuffle each one's bases
in place. Preserves per-sequence base composition (incl. natural per-seq
GC variation) but destroys all motifs and dinucleotide structure.

Compare to:
  - Exp 006 natural (has motifs, has per-seq GC variation, has di-freq)
  - Exp 008 Markov-1 (has di-freq but not per-seq variation, no motifs)
  - Exp 001 random (no per-seq variation, no motifs, no di-bias)
"""
import numpy as np, os

L = 200
N = 50_000
SEED = 12
rng = np.random.default_rng(SEED)

SRC = os.path.join(os.path.dirname(__file__), "..", "006_natural_genomic",
                   "sequences_0.txt")

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(SRC) as fi, open(out_path, "w") as fo:
    for line in fi:
        s = line.strip()
        if len(s) != L:
            continue
        arr = np.array(list(s))
        rng.shuffle(arr)
        fo.write("".join(arr.tolist()) + "\n")
print(f"Wrote shuffled natural sequences to {out_path}")
