"""
Experiment 001: Pure random 200bp sequences.

Purpose:
  Establish a baseline for what a sequence-to-activity model can learn when the
  only structure in the library is the global A/C/G/T distribution. Sets the
  floor for all subsequent experiments and calibrates the dynamic range of the
  eval metrics.

Theory:
  Random sequences broaden representation space (de Boer et al.) and the model
  should still pick up rare chance occurrences of TF-like patterns. But with
  most sequences inactive, the model has limited gradient information.
  Prediction: low mean_r, mostly recapitulating GC-content / dinucleotide
  biases.

Design:
  50,000 sequences, each 200bp, sampled iid uniform from {A, C, G, T}.
  Single seed.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
ALPHABET = "ACGT"
SEED = 42

def main():
    rng = random.Random(SEED)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for _ in range(N_SEQS):
            seq = "".join(rng.choice(ALPHABET) for _ in range(SEQ_LEN))
            f.write(seq + "\n")
    print(f"Wrote {N_SEQS} sequences of length {SEQ_LEN} to {out_path}")

if __name__ == "__main__":
    main()
