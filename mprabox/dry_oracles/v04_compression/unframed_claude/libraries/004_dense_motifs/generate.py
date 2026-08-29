"""Experiment 004: High-density motif packing (~20 motifs / 200bp).

Each sequence: pack TFBSs back-to-back to nearly fill the 200bp, separated
by short uniform-random spacers. Tests whether motif density is the lever.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = np.array(list("ACGT"))

MOTIFS = [
    "TATAAA", "GGGCGG", "TGACTCA", "CCAAT", "ACCGGAAGT",
    "TGACGTCA", "CACGTG", "GGGGGCGGGG", "GCGCATGCGC", "CCATCTT",
    "TTTATA", "TGAGTCA", "ATTGG", "AGGAAGT", "GATAAG",
    "CAGCTG", "GCCNNNGGC".replace("N", "G"), "AAGGTCA",
]
MOTIFS_BYTES = [m.encode() for m in MOTIFS]

rng = np.random.default_rng(20260605)

# Strategy: fill the sequence by concatenating motifs with short (0–3 bp)
# uniform-random spacers until we hit 200bp; pad with random if short.


def gen_sequence(rng):
    parts = []
    used = 0
    while used < LEN:
        m = MOTIFS_BYTES[int(rng.integers(0, len(MOTIFS_BYTES)))]
        spacer_len = int(rng.integers(0, 4))
        spacer = "".join(ALPHABET[rng.integers(0, 4, size=spacer_len)]) if spacer_len else ""
        chunk = m.decode() + spacer
        if used + len(chunk) > LEN:
            break
        parts.append(chunk)
        used += len(chunk)
    seq = "".join(parts)
    if len(seq) < LEN:
        seq += "".join(ALPHABET[rng.integers(0, 4, size=LEN - len(seq))])
    return seq[:LEN]


seqs = [gen_sequence(rng) for _ in range(N_SEQ)]
assert all(len(s) == LEN for s in seqs)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences with packed motifs to {out_path}")
print(f"  Sample: {seqs[0]}")
