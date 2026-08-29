"""Two-bank: K562 saturated (exp 012 design) + SKNSH motifs (exp 007 design) + null.

Exp 012's eval_01 K562 = +0.0089 was the lift, exp 007's eval_01 SKNSH
was modest but eval_07/08 SKNSH = +0.008. Try combining: each bank fires
its own model, null suppresses all.

Composition:
- 12,500 K562-saturated (GC=65, 12 K562/universal motifs) — from exp 012
- 12,500 SKNSH-motif (GC=50, 6 SKNSH motifs) — from exp 007
- 25,000 null (GC=40, no motifs) — between active GCs to avoid HepG2 trap
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

K562_MOTIFS = [
    "AGATAA", "TGATAA", "AGATAG", "TGATAG",
    "CACCC", "GGGGTG", "GGGTGGGG",
    "TGCTGAGTCAGCA",
    "CAGCTG", "CATCTG", "CACCTG",
    "TGAGTCA", "TGACTCA",
    "GGGCGG", "GGGCGGGG",
    "GGAAGT", "CGGAAG",
    "CCAAT",
    "TGACGTCA",
    "CACGTG",
]

SKNSH_MOTIFS = [
    "CAGATG",     # NEUROD
    "CAGCTG",     # ASCL1 / TAL E-box
    "TAATTA",     # homeobox
    "TAATT",      # homeobox extended
    "ATGCAT",     # POU3F2 half
    "ATGCATAT",   # POU3F2
    "CAGGTG",     # E-box (NEUROD-like)
    "TGAGTCA",    # AP-1 (universal)
    "GGAAGT",     # ETS
]

rng = np.random.default_rng(1101)
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


N_K562 = 12_500
N_SKNSH = 12_500
N_NULL = 25_000

k562_block = bg(N_K562, L, gc=0.65)
k562_block = insert(k562_block, K562_MOTIFS, n_per_seq=12)

sknsh_block = bg(N_SKNSH, L, gc=0.50)
sknsh_block = insert(sknsh_block, SKNSH_MOTIFS, n_per_seq=8)

null_block = bg(N_NULL, L, gc=0.40)

combined = np.concatenate([k562_block, sknsh_block, null_block], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (12.5k K562-sat GC65 + 12.5k SKNSH-motif GC50 + 25k null GC40)")
