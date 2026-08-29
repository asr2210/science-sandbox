"""Universal-only saturated motifs in strict bimodal, moderate GC contrast.

Exp 012 won on K562 (+0.0089) using K562-specific motifs. But HepG2 only
got +0.0011 and SKNSH +0.0035 there. Hypothesis: universal TF motifs
(AP-1, SP1, ETS, NF-Y, CREB, MYC, CCAAT) activate all 3 cells equally
— so a saturated-universal design should lift all 3 r columns.

25k active: GC=60%, 16 universal motifs (overlap OK).
25k null: GC=30%, no motifs.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

UNIV_MOTIFS = [
    "TGAGTCA", "TGACTCA",        # AP-1
    "GGGCGG", "GGGCGGGG",        # SP1
    "CCAAT", "CCAATCA",          # NF-Y
    "TGACGTCA",                  # CREB
    "GGAAGT", "CGGAAG",          # ETS
    "CACGTG",                    # MYC E-box
    "CAGCTG", "CATCTG",          # E-box generic (TAL/ASCL1/NEUROD)
    "AGGTCA",                    # NR half-site (shared)
    "GGAATT",                    # NF-kB-like
]

rng = np.random.default_rng(1301)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")


def bg(n, length, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)


def insert(seqs, motifs, n_per_seq):
    for i in range(seqs.shape[0]):
        for _ in range(n_per_seq):
            m = motifs[rng.integers(len(motifs))]
            if rng.random() < 0.5:
                m = m.translate(COMP)[::-1]
            ml = len(m)
            if ml > seqs.shape[1]:
                continue
            pos = rng.integers(0, seqs.shape[1] - ml + 1)
            seqs[i, pos:pos + ml] = list(m)
    return seqs


half = N_TOTAL // 2
active = bg(half, L, gc=0.60)
active = insert(active, UNIV_MOTIFS, n_per_seq=16)

null = bg(N_TOTAL - half, L, gc=0.30)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k univ-saturated 16motifs GC60 + 25k null GC30)")
