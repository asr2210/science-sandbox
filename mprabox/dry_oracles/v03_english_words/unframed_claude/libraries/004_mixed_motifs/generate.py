"""Random uniform background + sprinkle 2-3 strong TF motifs per sequence.
Motifs span K562, HepG2, SKNSH cell types and common core promoter elements.
"""
import numpy as np

N, L = 50000, 200
rng = np.random.default_rng(4)

# Curated TF motifs (consensus, not full PWM):
MOTIFS = [
    # Core promoter
    "TATAAA",          # TATA box
    "CCAAT",           # CCAAT box
    "GGGCGG",          # GC box (SP1)
    # K562 / erythroid
    "GATAAG",          # GATA1
    "CACCC",           # KLF1
    "TGASTCA".replace("S", "G"),  # AP-1 / NFE2 like (TGAGTCA)
    "TGCTGAGTCAT",     # NFE2
    # HepG2 / liver
    "TGTTTGY".replace("Y", "C"),  # HNF1 (TGTTTGC)
    "CAAAGTCCA",       # HNF4A
    "TTGCGCAAT".replace("N", "A"),  # C/EBP-ish (TTGCGCAAT)
    "ATTGCGCAAT",      # C/EBP
    # SKNSH / neuronal
    "TTCAGCACCNNGGACAG".replace("N", "A"),  # NRSF/REST (relaxed)
    "CANNTG".replace("N", "C"),  # E-box (NEUROD1) - CACCTG
    "CAGCTG",          # bHLH E-box
    "GGGGGAGGGG",      # SP1-ish / neural
    # General enhancer-y
    "TGACTCA",         # AP-1
    "GGAAGT",          # ETS / Elk
    "CCGCCC",          # SP1 reverse
]

alphabet = np.array(list("ACGT"))
seqs = []
for i in range(N):
    # background random uniform
    seq = list(alphabet[rng.integers(0, 4, L)])
    # insert 2-3 motifs at random non-overlapping positions
    n_ins = rng.integers(2, 4)
    placed = []
    for _ in range(n_ins):
        m = MOTIFS[rng.integers(0, len(MOTIFS))]
        if len(m) >= L:
            continue
        # find a non-overlapping start
        for _try in range(20):
            start = int(rng.integers(0, L - len(m) + 1))
            if all(not (start < e and start + len(m) > s) for s, e in placed):
                seq[start:start + len(m)] = list(m)
                placed.append((start, start + len(m)))
                break
    seqs.append("".join(seq))

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N} mixed-motif sequences")
