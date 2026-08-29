"""Experiment 11: Natural hg38 backbone + motif insertion gradient.

Take random 200bp natural windows. Insert 0..6 strong activator motifs (varying
density across the library). Tests whether biological motifs in a natural
backbone (vs random in exp 003) add useful agreement-friendly variance.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=11)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"
def load_fa(p):
    with open(p) as f:
        lines = f.read().splitlines()
    return "".join(l for l in lines if not l.startswith(">")).upper()

print("Loading chromosomes...")
chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr22"]}

MOTIFS = [
    "AGATAAGG", "CCACACCC", "CAGCTGCC",                # K562
    "CAAAGTCCA", "TGAACCTTGA", "GTTAATCATTAAC",
    "TGTTTACTT", "ATTGCGCAAT",                          # HepG2
    "CTATAAATAG", "TGACTCA",                            # SKNSH / AP-1
    "GGGGCGGGG", "CCAATC", "CACGTG", "TGACGTCA", "GGGAATTTCC",  # universal
]

valid = re.compile(r"^[ACGT]+$")
chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()

# Densities: 0..6 motifs, 7 bins of ~7143
densities = np.repeat(np.arange(7), N // 7 + 1)[:N]
rng.shuffle(densities)

out = []
for i in range(N):
    while True:
        ci = int(rng.choice(len(chroms), p=weights))
        pos = int(rng.integers(0, chrom_lens[ci] - L))
        win = chrom_seq[chroms[ci]][pos:pos + L]
        if valid.match(win):
            break
    k = int(densities[i])
    if k > 0:
        arr = list(win)
        placements = []
        chosen_idx = rng.integers(0, len(MOTIFS), size=k)
        for mi in chosen_idx:
            m = MOTIFS[mi]
            ml = len(m)
            for _ in range(20):
                p = int(rng.integers(0, L - ml + 1))
                if all(p + ml <= sp or p >= sp + sl for sp, sl in placements):
                    placements.append((p, ml))
                    arr[p:p + ml] = list(m)
                    break
        win = "".join(arr)
    out.append(win)

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} natural+motif sequences, density distribution {dict(zip(*np.unique(densities, return_counts=True)))}")

# Stats
arr = np.array([[ord(b) for b in s] for s in out[:5000]], dtype=np.int8)
gc = ((arr == ord('C')) | (arr == ord('G'))).mean(axis=1)
print(f"GC% (5k sample): mean={gc.mean():.3f}, std={gc.std():.3f}")
