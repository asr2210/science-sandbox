"""Experiment 003: Random scaffold + universal TFBS motifs.

Each 200bp sequence is uniform random with ~6 well-known universal TFBSs
inserted at random non-overlapping positions. Tests whether motif content
beats the random baseline (0.32 on eval_01).

Motif set chosen for broad/ubiquitous expression across K562, HepG2, SK-N-SH:
- TATA box, SP1, AP-1, NF-Y(CCAAT), ETS, CREB, E-box, KLF, NRF1, YY1
- A few are given with reverse complement so both strands are exercised.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = np.array(list("ACGT"))

MOTIFS = [
    "TATAAA",        # TATA box
    "GGGCGG",        # SP1
    "TGACTCA",       # AP-1 (TRE)
    "CCAAT",         # NF-Y / CCAAT box
    "ACCGGAAGT",     # ETS (PU.1-like, broad)
    "TGACGTCA",      # CREB / CRE
    "CACGTG",        # E-box (Myc/USF)
    "GGGGGCGGGG",    # KLF / SP family
    "GCGCATGCGC",    # NRF1
    "CCATCTT",       # YY1
    # reverse complements for some
    "TTTATA",        # TATA-rc
    "TGAGTCA",       # AP-1 alt
    "ATTGG",         # CCAAT-rc
    "CCGGT",         # ETS-rc partial
]

MOTIFS_BYTES = [m.encode() for m in MOTIFS]
MIN_M, MAX_M = 4, 8  # motifs per sequence

rng = np.random.default_rng(20260604)


def gen_sequence(rng):
    idx = rng.integers(0, 4, size=LEN)
    seq = bytearray("".join(ALPHABET[idx]), "ascii")
    n_motifs = int(rng.integers(MIN_M, MAX_M + 1))
    chosen = rng.choice(len(MOTIFS_BYTES), size=n_motifs, replace=True)
    used = []  # list of (start, end)
    for mi in chosen:
        m = MOTIFS_BYTES[mi]
        L = len(m)
        # try a few times to place without overlap
        for _ in range(20):
            pos = int(rng.integers(0, LEN - L + 1))
            if all(not (pos < u_end and pos + L > u_start) for u_start, u_end in used):
                seq[pos:pos + L] = m
                used.append((pos, pos + L))
                break
    return seq.decode("ascii")


seqs = [gen_sequence(rng) for _ in range(N_SEQ)]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences with embedded universal motifs to {out_path}")
print(f"  Sample: {seqs[0]}")
