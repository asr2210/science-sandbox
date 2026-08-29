"""
Experiment 011: TATA box motif insertion.

50K uniform random 200-char sequences. Each one has a TATA box
"TATAAA" (= "303000" with mapping A=0,C=1,G=2,T=3) overwritten at
a random position in [0, 194]. Per-position composition stays roughly
uniform (motif positions vary). Per-sequence content: each contains a
TATA box at a different position.

Tests whether the score recognizes specific regulatory motifs.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = "0123"
MOTIF = "303000"  # TATAAA in our mapping
ML = len(MOTIF)

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        seq = list(random.choices(ALPHA, k=L))
        pos = random.randint(0, L - ML)
        seq[pos:pos + ML] = list(MOTIF)
        f.write("".join(seq))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} (with TATA box at random pos) to {OUT}")
