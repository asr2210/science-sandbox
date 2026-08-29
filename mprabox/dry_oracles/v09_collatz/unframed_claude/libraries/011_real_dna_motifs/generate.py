"""Experiment 011 — Real chr22 DNA + light motif augmentation.

Sample 50k real 200bp chr22 windows (same as exp 009), then inject 3
strong universal activator motifs at random positions.

Motifs: AP-1 (TGAGTCA), SP1 (GGGCGGGGC), NFY/CCAAT (ATTGGCTAATC),
        CRE (TGACGTCA), Ebox (CACGTG).
Inserts/seq: 3 (low so we mostly preserve natural composition).

Hypothesis: real DNA = 0.32; add a few strong motifs on top = maybe
0.33-0.35. Risk: motif insertion displaces natural content; might hurt
HepG2 by raising GC slightly.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(11)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"):
            continue
        parts.append(line.strip().upper())
seq = "".join(parts)

MOTIFS = [
    "TGAGTCA", "GGGCGGGGC", "ATTGGCTAATC", "TGACGTCA", "CACGTG",
]
INSERTS_PER_SEQ = 3

def gen_one():
    while True:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s:
            continue
        if any(s.count(c * 20) > 0 for c in "ACGT"):
            continue
        break
    s = list(s)
    chosen = rng.choice(len(MOTIFS), size=INSERTS_PER_SEQ, replace=True)
    used = []
    for mi in chosen:
        m = MOTIFS[mi]
        for _ in range(40):
            pos = int(rng.integers(0, L - len(m) + 1))
            ok = all(not (pos < e and pos + len(m) > st) for (st, e) in used)
            if ok:
                used.append((pos, pos + len(m)))
                for j, ch in enumerate(m):
                    s[pos + j] = ch
                break
    return "".join(s)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for _ in range(N):
        f.write(gen_one()); f.write("\n")
print(f"Wrote {N} sequences to {out}")
