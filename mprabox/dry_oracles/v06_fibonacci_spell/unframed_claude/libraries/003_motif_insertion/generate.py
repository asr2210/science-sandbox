"""Experiment 003: Insert canonical TFBS motifs into 42% GC random background.

50,000 sequences of 200bp. Each sequence has ~6 motifs inserted at random
positions. Motif set covers general (AP-1, CREB, SP1, TATA) and cell-type-
specific factors (GATA1/K562, HNF4/HepG2, E-box/NEUROD/SKNSH).
"""
import numpy as np

N = 50_000
L = 200
SEED = 3
MOTIFS_PER_SEQ = 6

# Canonical TFBS consensus sequences (use unambiguous bases).
MOTIFS = [
    "TGACTCA",        # AP-1 (general)
    "TGAGTCA",        # AP-1 alt
    "TGACGTCA",       # CREB / CRE
    "GGGGCGGGG",      # SP1
    "TATAAA",         # TATA box
    "CCAAT",          # CCAAT box
    "AGATAA",         # GATA1 (K562)
    "TTATCT",         # GATA1 reverse
    "AGGTCAAAGGTCA",  # HNF4 DR1
    "TGTTTGC",        # FOXA / HNF3
    "CAGCTG",         # E-box NeuroD (SKNSH)
    "CACGTG",         # E-box MYC
    "CCGCCATCTT",     # NRSF/REST (neural)
    "TGCTGAGTCA",     # NF-E2
    "CACCC",          # KLF1 (K562)
    "GGGAGG",         # MYB (K562)
    "TTGCGCAA",       # NF-Y
    "GGAA",           # ETS
    "CACGTG",         # MAX/USF
]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
p_bg = np.array([0.29, 0.21, 0.21, 0.29])  # 42% GC background

def make_seq():
    seq = list(rng.choice(bases, size=L, p=p_bg))
    # Insert MOTIFS_PER_SEQ motifs at random non-overlapping positions
    chosen = rng.choice(len(MOTIFS), size=MOTIFS_PER_SEQ, replace=True)
    used = []
    for mi in chosen:
        m = MOTIFS[mi]
        # try random position
        for _ in range(5):
            pos = int(rng.integers(0, L - len(m)))
            if all(abs(pos - u[0]) >= u[1] for u in used):
                used.append((pos, len(m)))
                for j, b in enumerate(m):
                    seq[pos + j] = b
                break
    return "".join(seq)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for _ in range(N):
        f.write(make_seq() + "\n")

print(f"Wrote {N} sequences of length {L} with ~{MOTIFS_PER_SEQ} motifs each")
