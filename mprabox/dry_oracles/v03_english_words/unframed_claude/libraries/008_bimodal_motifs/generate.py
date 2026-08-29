"""Bimodal library: 25k pure random uniform (expected low activity)
+ 25k random with 4 strong enhancer motifs (expected high activity).
Goal: widen variance in predicted activity to boost correlation.
"""
import numpy as np

N_HALF, L = 25000, 200
rng = np.random.default_rng(8)
ALPH = np.array(list("ACGT"))

# Strong enhancer/promoter motifs, well-attested in ENCODE catalogs.
MOTIFS = [
    "TGACTCAGCA",   # AP-1
    "GGGCGGGGGC",   # SP1 / GC box
    "GATAAGGGAT",   # GATA + extension
    "TTGCGCAATCT",  # C/EBP composite
    "CAGGTG",       # E-box (NeuroD/MyoD)
    "TGASTCA".replace("S","G"),  # AP1 short
    "CACGTG",       # MYC/USF E-box
    "GGAATG",       # ETS-ish
    "TATAAAAG",     # TATA box
]

# half A: random uniform
randA = ALPH[rng.integers(0, 4, size=(N_HALF, L))]
seqs_A = ["".join(r) for r in randA]

# half B: random uniform + 4 motifs at non-overlapping random positions
seqs_B = []
for _ in range(N_HALF):
    seq = list(ALPH[rng.integers(0, 4, L)])
    placed = []
    n_motifs = 4
    attempts = 0
    while len(placed) < n_motifs and attempts < 50:
        attempts += 1
        m = MOTIFS[rng.integers(0, len(MOTIFS))]
        s = int(rng.integers(0, L - len(m) + 1))
        if all(not (s < e2 and s + len(m) > s2) for s2, e2 in placed):
            seq[s:s + len(m)] = list(m)
            placed.append((s, s + len(m)))
    seqs_B.append("".join(seq))

all_seqs = seqs_A + seqs_B
rng.shuffle(all_seqs)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    f.write("\n".join(all_seqs) + "\n")

print(f"Wrote {len(all_seqs)} bimodal sequences (25k random + 25k motif-loaded)")
