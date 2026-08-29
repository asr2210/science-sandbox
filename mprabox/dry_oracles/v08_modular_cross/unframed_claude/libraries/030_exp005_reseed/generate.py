"""Exp 005 recipe with new seed (final variance test).

Exp 005 (K562 motifs 8/seq, GC=50/50) was the 2nd-best eval_01 (+0.0043).
Re-run with a different seed to test recipe robustness.

If this lands ≥ +0.003, exp 005 is the robust recipe.
If near 0, single-seed noise dominates everything.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

K562_MOTIFS = [
    "AGATAA", "TGATAG", "AGATAG", "TGATAA",
    "CACCC", "CCACCC", "GGGGTG",
    "TGCTGAGTCAGCA",
    "CAGCTG", "CATCTG", "CACCTG",
    "TGAGTCA", "TGACTCA",
    "GGAAGT", "CGGAAG",
    "GGGCGGGG", "GGGCGG",
    "CAGTTG", "AACTG",
]

rng = np.random.default_rng(2303)  # different from exp 005's seed=42
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")


def bg(n, length, gc=0.50):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)


def insert(seqs, motifs, n_per_seq):
    for i in range(seqs.shape[0]):
        for _ in range(n_per_seq):
            m = motifs[rng.integers(len(motifs))]
            if rng.random() < 0.5:
                m = m.translate(COMP)[::-1]
            ml = len(m)
            pos = rng.integers(0, seqs.shape[1] - ml + 1)
            seqs[i, pos:pos + ml] = list(m)
    return seqs


half = N_TOTAL // 2
active = bg(half, L, gc=0.50)
active = insert(active, K562_MOTIFS, n_per_seq=8)
null = bg(N_TOTAL - half, L, gc=0.50)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (exp 005 recipe, seed=2303)")
