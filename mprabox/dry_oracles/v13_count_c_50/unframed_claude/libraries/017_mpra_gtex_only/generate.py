"""Experiment 17: MPRA training sequences, GTEx eQTL subset only.

GTEx-derived MPRA sequences = paired ref/alt variants on eQTL loci, the
largest single project (445K sequences). Hypothesis: this is the most
consistent class — both models well-trained on it -> highest agreement.
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=17)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

print("Reading MPRA dataset...")
seqs = []
with open(src) as f:
    h = f.readline().rstrip("\n").split("\t")
    si, pi = h.index("sequence"), h.index("data_project")
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) <= si or p[pi] != "GTEX":
            continue
        s = p[si].upper()
        if len(s) != L or set(s) - set("ACGT"):
            continue
        seqs.append(s)
print(f"Loaded {len(seqs):,} GTEx-only MPRA sequences")

idx = rng.choice(len(seqs), size=N, replace=False)
out = [seqs[i] for i in idx]
rng.shuffle(out)
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} GTEx-only sequences")
