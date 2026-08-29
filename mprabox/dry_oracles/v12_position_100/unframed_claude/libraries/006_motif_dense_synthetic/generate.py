"""Exp 006: synthetic motif-dense 200bp sequences.

Each sequence packs 8 instances of a randomly chosen strong TF motif
(from 20 well-characterized human regulatory motifs) into a random
background, with random spacing. This tests whether MOTIF DENSITY
(rather than biological context) is the bottleneck.

If eval_01 > 0.10, motif density matters.
If eval_01 ~ 0.07, motif density alone is not the answer.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
SEED = 17

# Strong, well-characterized TF motif consensus sequences.
# Single canonical sequence (not PWM) — keeps the implementation simple.
MOTIFS = [
    "TGACTCA",     # AP-1 (JUN/FOS)
    "GGGACTTTCC",  # NF-kB
    "CCAAT",       # CEBP/NF-Y
    "TATAAA",      # TATA box
    "CCGCCC",      # SP1
    "ATGCAAAT",    # OCT
    "GATAA",       # GATA1
    "CACGTG",      # E-box (MYC/USF)
    "GGGCGG",      # SP1 alt
    "AGGTCA",      # nuclear receptor half-site
    "TTGCGCAA",    # CREB
    "TTCCGGAA",    # ETS
    "AATAAA",      # poly-A signal-ish
    "CTCFCONS",    # placeholder, replaced below
    "GCCACGTGGC",  # USF1
    "CAGCTG",      # E-box alt
    "AGGAAG",      # ETS-like
    "TGAGTCA",     # AP-1 alt
    "GGGGAGGG",    # KLF-like
    "TAATTA",      # HOX
]
# Replace placeholder with CTCF-like consensus.
MOTIFS[13] = "CCACCAGGTGGCAG"

# Drop any with non-ACGT (defensive).
MOTIFS = [m for m in MOTIFS if set(m) <= set("ACGT")]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

def gen_seq():
    # Choose primary motif type for this sequence (one TF per seq emphasized).
    primary = MOTIFS[rng.integers(len(MOTIFS))]
    n_primary = 6 + int(rng.integers(0, 5))  # 6-10 copies of primary
    # Add 2-4 different secondary motifs to break monotony.
    secondary = [MOTIFS[i] for i in rng.choice(len(MOTIFS), size=int(rng.integers(2, 5)), replace=False)]
    motifs_to_insert = [primary] * n_primary + secondary
    rng.shuffle(motifs_to_insert)

    # Reserve space for motifs.
    total_motif_len = sum(len(m) for m in motifs_to_insert)
    spacer_total = L - total_motif_len
    if spacer_total < len(motifs_to_insert) + 1:
        # Too many motifs; drop until fits with ≥1bp spacer between.
        while spacer_total < len(motifs_to_insert) + 1 and motifs_to_insert:
            motifs_to_insert.pop()
            spacer_total = L - sum(len(m) for m in motifs_to_insert)

    # Split spacer_total into (n_motifs + 1) random non-negative integers.
    n = len(motifs_to_insert)
    breakpoints = sorted(rng.integers(0, spacer_total + 1, size=n))
    parts = []
    prev = 0
    for bp in breakpoints:
        parts.append(bp - prev)
        prev = bp
    parts.append(spacer_total - prev)

    pieces = []
    for sp_len, motif in zip(parts, motifs_to_insert):
        sp = "".join(bases[rng.integers(0, 4, size=sp_len)])
        pieces.append(sp)
        pieces.append(motif)
    # Last spacer.
    sp = "".join(bases[rng.integers(0, 4, size=parts[-1])])
    pieces.append(sp)

    s = "".join(pieces)
    assert len(s) == L, (len(s), L)
    return s

seqs = [gen_seq() for _ in range(N)]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
