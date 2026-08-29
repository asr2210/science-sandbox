"""Experiment 30: Ensemble of best recipes — sample from winning libraries.

Take 10K from each of the top 5 libraries seen (018, 020, 025, 028, 029)
to form a 50K mixture. Tests whether averaging across already-good
distributions can edge above any single one (around 0.574 plateau).
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=30)
N = 50000
N_EACH = 10000

ROOT = Path(__file__).resolve().parents[1]
sources = [
    "018_mpra_plus_natural",
    "020_mpra_plus_gc_strat",
    "025_mpra_balanced_proj",
    "028_mpra_plus_eqchrom_nat",
    "029_mpra_cre_heavy",
]

out = []
for src in sources:
    seqs = (ROOT / src / "sequences_0.txt").read_text().strip().split("\n")
    print(f"{src}: {len(seqs)} seqs")
    idx = rng.choice(len(seqs), size=N_EACH, replace=False)
    out.extend(seqs[i] for i in idx)

rng.shuffle(out)
assert len(out) == N
# Final dedupe: keep 50000 unique (in case of overlap)
unique_out = list(dict.fromkeys(out))
print(f"Unique after dedupe: {len(unique_out)}")
if len(unique_out) < N:
    # Pad with extras from first source
    seqs = (ROOT / sources[0] / "sequences_0.txt").read_text().strip().split("\n")
    rng.shuffle(seqs)
    for s in seqs:
        if len(unique_out) >= N:
            break
        if s not in set(unique_out):
            unique_out.append(s)
out = unique_out[:N]
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} (ensemble of top 5)")
