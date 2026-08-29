"""Experiment 3: Motif-density gradient with cross-cell-type activators.

Goal: induce a strong activity gradient that both eval and ground-truth models
should agree on. Stratify across 10 density bins (0 to 9 motifs per sequence).

Motifs chosen from well-characterized strong activators across K562, HepG2, SKNSH,
plus universal regulators. This should:
- Boost HepG2_r (current bottleneck on eval_01: 0.033)
- Boost SKNSH_r (current: 0.121)
- Maintain K562_r (current: 0.314)
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=3)
N, L = 50000, 200
alphabet = np.array(list("ACGT"))

# Well-characterized strong activator motifs (consensus / known strong instances)
MOTIFS = [
    # K562 (erythroid/myeloid)
    "AGATAAGG",      # GATA1 (TGATAA + flanking)
    "CCACACCC",      # KLF1 / KLF family
    "CAGCTGCC",      # TAL1 / E-box
    # HepG2 (hepatocyte)
    "CAAAGTCCA",     # HNF4A consensus
    "TGAACCTTGA",    # HNF4A alternate
    "GTTAATCATTAAC", # HNF1A palindrome
    "TGTTTACTT",     # FOXA1/2
    "ATTGCGCAAT",    # CEBPA
    # SKNSH (neuronal)
    "CTATAAATAG",    # MEF2 (CTA-w7-TAG)
    "TGACTCA",       # AP-1 (also pan-active)
    # Universal strong activators
    "GGGGCGGGG",     # SP1
    "CCAATC",        # NF-Y
    "CACGTG",        # USF / E-box
    "TGACGTCA",      # CREB
    "GGGAATTTCC",    # NF-kB
]
MOTIFS = np.array(MOTIFS, dtype=object)
motif_lens = np.array([len(m) for m in MOTIFS])
max_motif_len = int(motif_lens.max())

# 10 density bins, 5000 sequences per bin
densities = np.repeat(np.arange(10), N // 10)  # 0..9, 5000 each
rng.shuffle(densities)

# Generate random backgrounds
bg = rng.integers(0, 4, size=(N, L), dtype=np.int8)
seqs = ["".join(alphabet[row]) for row in bg]


def insert_motifs(seq, k):
    """Insert k motifs at non-overlapping random positions, replacing background bases."""
    if k == 0:
        return seq
    chosen_idx = rng.integers(0, len(MOTIFS), size=k)
    chosen = [MOTIFS[i] for i in chosen_idx]
    # Sort by length descending for placement, then place greedily
    placements = []
    arr = list(seq)
    attempts = 0
    for m in chosen:
        ml = len(m)
        for _ in range(20):  # try up to 20 times to find a non-overlapping slot
            pos = int(rng.integers(0, L - ml + 1))
            if all(pos + ml <= p or pos >= p + l for p, l in placements):
                placements.append((pos, ml))
                arr[pos:pos + ml] = list(m)
                break
            attempts += 1
    return "".join(arr)


out_seqs = [insert_motifs(s, int(k)) for s, k in zip(seqs, densities)]

# Sanity
assert len(out_seqs) == N
assert all(len(s) == L for s in out_seqs)
assert all(set(s) <= set("ACGT") for s in out_seqs[:100])

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out_seqs) + "\n")

print(f"Wrote {N} sequences (L={L}) with motif density 0..9 stratified.")
print(f"Density counts: {dict(zip(*np.unique(densities, return_counts=True)))}")
