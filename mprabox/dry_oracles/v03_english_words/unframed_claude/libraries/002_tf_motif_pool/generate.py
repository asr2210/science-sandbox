"""Exp 002: TF motif pool.
Each 200bp sequence gets 3 random canonical TF motifs embedded at
random positions in an otherwise-random background. Tests whether
motif content moves the scoring function.

Motifs chosen as broad-coverage strong enhancer/promoter elements
known across K562 (myeloid), HepG2 (liver), SK-N-SH (neuron) and
generic core promoter machinery.
"""
import numpy as np
import os

N = 50_000
L = 200
SEED = 1
rng = np.random.default_rng(SEED)

# Canonical TF motifs (consensus or sub-consensus). Mix of liver/HNF,
# myeloid/GATA, neural/E-box, and broad activators.
MOTIFS = [
    "TGACTCA",      # AP-1
    "TGACGTCA",     # CREB / ATF
    "GGGACTTTCC",   # NF-kB
    "AGATAA",       # GATA
    "CACGTG",       # E-box (MYC/MAX, neural)
    "TATAAA",       # TATA
    "CCAAT",        # CCAAT box (NF-Y)
    "GGGCGG",       # SP1 / KLF
    "GTTAATNATTAAC", # HNF1 (palindrome) -- expand N
    "CAAAG",        # HNF4 partial / general
    "GGAA",         # ETS core
    "TTGCGCAA",     # generic GC-box
    "CCGCCC",       # SP1 reverse
    "TAATTA",       # homeobox
    "GCCNNNGGC",    # generic GC-rich
]

bases = np.array(list("ACGT"))

def expand_iupac(motif, rng):
    """Replace N with random base."""
    out = []
    for c in motif:
        if c == "N":
            out.append(bases[rng.integers(0, 4)])
        else:
            out.append(c)
    return "".join(out)

# Pre-generate random background as integers
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr].astype("<U1")

# Embed 3 motifs per sequence at random positions
for i in range(N):
    chosen_idxs = rng.choice(len(MOTIFS), size=3, replace=True)
    for mi in chosen_idxs:
        m = expand_iupac(MOTIFS[mi], rng)
        mlen = len(m)
        if mlen > L:
            continue
        pos = rng.integers(0, L - mlen + 1)
        for k, ch in enumerate(m):
            seqs[i, pos + k] = ch

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} sequences to {out_path}")
