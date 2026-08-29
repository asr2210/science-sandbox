"""Experiment 007: random uniform scaffold + insert ONE real regulatory core.

Each 200bp sequence is uniform random with one 20-35bp literature-validated
regulatory core overlaid at a random position. The bank has 12 well-known
mammalian enhancer/promoter cores chosen to be active across cell types.
Different cores per sequence + different positions → library remains diverse.

Tests whether longer real biological elements help vs the random baseline (0.32).
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = np.array(list("ACGT"))

# 12 mammalian regulatory cores (each 20-40bp, from literature).
# Designed for broad / cross-cell-type activity.
CORES = [
    "AAAGCATGCATCTCAATTAGTCAGCAACCATAGT",   # 1. SV40 enhancer downstream half
    "AGGGACTTTCCATTGACGCAATG",              # 2. CMV NFkB element
    "TGACTCATGAGTCATGACTCA",                # 3. AP-1 trimer (TRE)
    "GGGCGGGGGGCGGGGGGCGGG",                # 4. SP1 trimer (GC box)
    "CCAATCAGCCAATCAGCCAAT",                # 5. NFY/CCAAT trimer
    "TGACGTCATGCATGACGTCA",                 # 6. CREB/CRE tandem
    "AGGAAGTAGGAAGTAGGAAGT",                # 7. ETS trimer
    "CACGTGCACGTGCACGTG",                   # 8. E-box trimer (Myc/USF)
    "AGATAAGAGATAAGAGATAAG",                # 9. GATA trimer
    "AAGGTCAAAGGTCAAAGGTCA",                # 10. Nuclear receptor half-sites
    "GAAACCGAAACCGAAACC",                   # 11. IRF / ISRE-like
    "CTTCCTCTTCCTCTTCCT",                   # 12. ETS/PU.1 alt
]
CORES_BYTES = [c.encode() for c in CORES]

# reverse complement function
COMP = bytes.maketrans(b"ACGT", b"TGCA")


def rc(b):
    return b.translate(COMP)[::-1]


rng = np.random.default_rng(20260608)


def gen_sequence(rng):
    idx = rng.integers(0, 4, size=LEN)
    seq = bytearray("".join(ALPHABET[idx]), "ascii")
    # pick a core
    ci = int(rng.integers(0, len(CORES_BYTES)))
    core = CORES_BYTES[ci]
    if rng.random() < 0.5:
        core = rc(core)
    pos = int(rng.integers(0, LEN - len(core) + 1))
    seq[pos:pos + len(core)] = core
    return seq.decode("ascii")


seqs = [gen_sequence(rng) for _ in range(N_SEQ)]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences (random + 1 real core) to {out_path}")
print(f"  Sample: {seqs[0]}")
