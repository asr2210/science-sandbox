"""Random uniform + neural-specific motifs (REST/NRSE, NeuroD E-box, MEF2).
Targets SKNSH without (hopefully) hurting K562/HepG2.
"""
import numpy as np

N, L = 50000, 200
rng = np.random.default_rng(14)
ALPH = np.array(list("ACGT"))

NEURAL_MOTIFS = [
    # REST/NRSE consensus (~21bp)
    "TTCAGCACCATGGACAG",
    "TTCAGCACCCTGGACAG",
    # NeuroD/E-box variants
    "CAGCTG", "CACCTG", "CAGGTG", "CATCTG",
    # MEF2 (10-12bp)
    "CTATAAATAG",
    "CTATTTATAG",
    # Sox motifs (neural crest)
    "ACAAAG", "CTTTGT",
    # POU3F2 (neural)
    "ATGCAAAT",
    # OLIG / ASCL1 bHLH
    "CAGCTGCT", "AGCAGCTG",
]

seqs = []
for _ in range(N):
    seq = list(ALPH[rng.integers(0, 4, L)])
    placed = []
    # insert 3 neural motifs
    for _ in range(3):
        m = NEURAL_MOTIFS[rng.integers(0, len(NEURAL_MOTIFS))]
        for _try in range(20):
            s = int(rng.integers(0, L - len(m) + 1))
            if all(not (s < e2 and s + len(m) > s2) for s2, e2 in placed):
                seq[s:s + len(m)] = list(m)
                placed.append((s, s + len(m)))
                break
    seqs.append("".join(seq))

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} sequences with 3 neural motifs each")
