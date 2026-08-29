"""Exp 009: Random background + 3 neural-specific motifs per sequence.
Goal: keep K562/HepG2 near their random-50%-GC optimum, while injecting
the kind of homeobox/bHLH content that natural DNA carries and that
boosted SKNSH from 0.06 to 0.10 in Exp 006.
"""
import numpy as np, os

N = 50_000
L = 200
N_MOTIFS = 3
SEED = 9
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

# Curated neural-specific motifs (homeobox + bHLH families).
NEURAL_MOTIFS = [
    "TAATTA",     # PHOX2/CRX/OTX (homeobox)
    "TAATCC",     # alt homeobox
    "ATTAAT",     # RC homeobox
    "TAATTG",     # POU/homeobox
    "CAATTA",     # POU2F
    "CAGCTG",     # ASCL1 / bHLH
    "CAGCTG",     # repeated for weight
    "CATCTG",     # NEUROD bHLH
    "CAGATG",     # NEUROD RC family
    "CACGTG",     # MYC E-box (myc neural)
    "CTAATTG",    # ISL1
    "CAATTAG",    # ISL1 RC
    "TTCAGCACCTG",# REST/NRSF half
    "CGGTGCTGAA", # REST RC
    "ATTTAGCATAC",# Hox
]

# Random background
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr].astype("<U1")

for i in range(N):
    chosen = rng.choice(len(NEURAL_MOTIFS), size=N_MOTIFS, replace=True)
    used = []
    for mi in chosen:
        m = NEURAL_MOTIFS[mi]
        mlen = len(m)
        if mlen > L:
            continue
        for _ in range(10):
            pos = int(rng.integers(0, L - mlen + 1))
            if all(not (pos < p[1] and pos + mlen > p[0]) for p in used):
                break
        used.append((pos, pos + mlen))
        for k, ch in enumerate(m):
            seqs[i, pos + k] = ch

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} sequences (random + {N_MOTIFS} neural motifs)")
