"""002 — Motif insertions: random background with strong TF motifs.

Hypothesis: K562/HepG2 signal (which is 0.01 from random) needs specific TF
binding motifs to rise. If mean_r jumps, motif content matters.

We insert 6 strong TF motifs per sequence at random positions, drawing
from a curated list covering K562, HepG2, SKNSH, and broad activators.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(2)
N, L = 50_000, 200
ALPH = np.array(list("ACGT"))

# Curated strong TF motifs (consensus sequences from JASPAR / literature)
MOTIFS = [
    # K562 / hematopoietic
    "AGATAAG",      # GATA1
    "CACCCC",       # KLF1/EKLF
    "TGASTCA",      # already wildcard, expand below
    # HepG2 / liver
    "CAAAGTCCA",    # HNF4A core
    "GTTAATNATTAAC",# HNF1A
    "TTGCGCAAT",    # C/EBP-alpha
    # SKNSH / neural
    "CAGCTG",       # bHLH (NEUROD/ASCL1)
    "TTCAGCACCNNGGAGA", # NRSF/REST
    # broad strong activators
    "GGGCGG",       # SP1
    "CCAAT",        # NFY
    "TGACTCA",      # AP-1
    "TGACGTCA",     # CREB
    "TATAAAA",      # TATA box
    "CCACGTG",      # Myc E-box
    "GCCACGTGGC",   # USF
    "GGAAGT",       # ETS
]

def expand(m):
    """Expand IUPAC ambiguity codes."""
    mp = {"A":"A","C":"C","G":"G","T":"T",
          "R":"AG","Y":"CT","S":"GC","W":"AT","K":"GT","M":"AC",
          "B":"CGT","D":"AGT","H":"ACT","V":"ACG","N":"ACGT"}
    out = []
    for ch in m:
        choices = mp[ch]
        out.append(choices[rng.integers(0, len(choices))])
    return "".join(out)

def build_seq():
    arr = list(ALPH[rng.integers(0, 4, size=L)])
    # insert 6 motifs at random non-overlapping positions
    n_ins = 6
    positions = sorted(rng.choice(range(L - 16), size=n_ins, replace=False))
    for pos in positions:
        m = MOTIFS[rng.integers(0, len(MOTIFS))]
        m = expand(m)
        for i, ch in enumerate(m):
            if pos + i < L:
                arr[pos + i] = ch
    return "".join(arr)

out = Path(__file__).parent / "sequences_0.txt"
with open(out, "w") as f:
    for _ in range(N):
        f.write(build_seq() + "\n")

print(f"wrote {N} sequences to {out}")
