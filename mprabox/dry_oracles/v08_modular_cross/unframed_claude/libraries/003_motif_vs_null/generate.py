"""Motif-rich vs null library.

Tests "dynamic range" hypothesis: include sequences that should look
strongly active (densely packed canonical TF motifs in GC-rich
background) AND sequences that should look strongly inactive (low
complexity, AT-rich, no motifs).

If the scorer correlates two predictors of regulatory activity, the
correlation rises with variance across the library — so a deliberate
mix of "active" and "inactive" sequences should beat random.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200
SEED = 42

# Strong consensus motifs from multiple broadly-active TF families.
# These are short and unambiguous.
MOTIFS = [
    "TGACTCA",     # AP-1 (universal enhancer)
    "TGAGTCA",     # AP-1 variant
    "CACGTG",      # E-box (MYC/MAX)
    "GGGCGG",      # SP1 (GC box)
    "CCAATCA",     # NF-Y (CCAAT)
    "TGACGTCA",    # CREB / ATF
    "GATAAG",      # GATA (K562)
    "TGCACA",      # TEAD-like
    "AGGTCA",      # nuclear receptor half-site (HepG2)
    "GGAAGT",      # ETS
]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

def gc_random(n, length, gc=0.55):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)

def at_random(n, length, gc=0.20):
    return gc_random(n, length, gc=gc)

# Half "active": GC-rich background with 6 motifs sprinkled in
n_active = N_TOTAL // 2
active = gc_random(n_active, L, gc=0.55)
n_motifs_per_seq = 6
for i in range(n_active):
    for _ in range(n_motifs_per_seq):
        motif = MOTIFS[rng.integers(len(MOTIFS))]
        # also randomly reverse-complement
        if rng.random() < 0.5:
            comp = str.maketrans("ACGT", "TGCA")
            motif = motif.translate(comp)[::-1]
        pos = rng.integers(0, L - len(motif) + 1)
        active[i, pos:pos + len(motif)] = list(motif)

# Half "null": AT-rich, no motifs
n_null = N_TOTAL - n_active
null = at_random(n_null, L, gc=0.20)

# Stack and shuffle (order shouldn't matter for r, but be safe)
combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]

lines = ["".join(row) for row in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} sequences: {n_active} motif-rich + {n_null} AT-rich-null")
