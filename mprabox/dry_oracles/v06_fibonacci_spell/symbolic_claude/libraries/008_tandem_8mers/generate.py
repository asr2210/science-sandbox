"""Experiment 008: Tandem 8-mer repeats.

Each of 50K sequences is a unique random 8-mer repeated 25 times
(8 * 25 = 200). 4^8 = 65536 possible 8-mers, sample 50K without
replacement. This is a focused k-mer probe: each sequence is one
"construct" whose activity is determined entirely by its 8-mer identity.

The Pearson r reveals how well eval and reference models agree on
ranking 8-mer constructs. If both models share similar k-mer biases
(likely for CNN-style DNA models), r should rise substantially.
"""
import os
import numpy as np

N_SEQS = 50_000
K = 8
REPS = 25
ALPHABET = "0123"
SEED = 53

assert K * REPS == 200

rng = np.random.default_rng(SEED)

# Encode 8-mers as integers and sample without replacement
total_kmers = 4 ** K
kmer_ids = rng.choice(total_kmers, size=N_SEQS, replace=False)

chars = np.array(list(ALPHABET))
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for kid in kmer_ids:
        # decode integer -> 8-char base-4 string
        digits = []
        x = int(kid)
        for _ in range(K):
            digits.append(chars[x & 3])
            x >>= 2
        kmer = "".join(reversed(digits))
        f.write(kmer * REPS + "\n")
print(f"Wrote {N_SEQS} tandem 8-mer sequences to {out_path}")
