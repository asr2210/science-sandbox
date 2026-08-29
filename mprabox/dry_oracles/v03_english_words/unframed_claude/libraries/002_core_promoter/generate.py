"""Experiment 002: random scaffolds with canonical core-promoter elements embedded.

Hypothesis: realistic regulatory motifs are in-distribution for both scoring
models; embedding them should raise predicted-activity variance and the
correlation between scoring functions.

Layout for each 200bp sequence:
  pos 0   .. 49  : random padding (50 bp)
  pos 50  .. 59  : SP1 / GC-box ('GGGGCGGGGC')        — 10 bp
  pos 60  .. 99  : random (40 bp)
  pos 100 .. 107 : TATA box     ('TATAAAAG')          — 8 bp
  pos 108 .. 124 : random (17 bp)  — canonical ~25bp from TATA to TSS
  pos 125 .. 131 : Inr          ('TCAGTTT')           — 7 bp (Inr consensus YYANWYY → TCAGTTT)
  pos 132 .. 199 : random (68 bp)
"""
import os
import numpy as np

RNG_SEED = 1002
N_SEQS = 50_000
LEN = 200
ALPHABET = np.array(list("ACGT"))

SP1     = "GGGGCGGGGC"   # 10 bp
TATA    = "TATAAAAG"     #  8 bp
INR     = "TCAGTTT"      #  7 bp

INSERTS = [
    (50,  SP1),
    (100, TATA),
    (125, INR),
]


def main():
    rng = np.random.default_rng(RNG_SEED)
    idx = rng.integers(0, 4, size=(N_SEQS, LEN), dtype=np.int8)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in idx:
            seq = list(ALPHABET[row])
            for pos, motif in INSERTS:
                for j, c in enumerate(motif):
                    seq[pos + j] = c
            f.write("".join(seq))
            f.write("\n")
    print(f"wrote {N_SEQS} sequences of length {LEN} to {out_path}")


if __name__ == "__main__":
    main()
