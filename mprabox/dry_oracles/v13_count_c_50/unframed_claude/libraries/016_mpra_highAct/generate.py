"""Experiment 16: MPRA training sequences with high activity magnitude.

Hypothesis: opposite of exp 015 — sequences whose measured log2FC has high
magnitude (in any cell line) carry strong, confidently-predicted signal, so
both models should score them with high consistency. Higher variance in
ground truth + same in predictor -> higher Pearson r.

Take sequences with max(|K562|, |HepG2|, |SKNSH| log2FC) above the upper
quartile, then sample 50K.
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=16)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

print("Reading MPRA dataset...")
seqs = []
acts = []
with open(src) as f:
    h = f.readline().rstrip("\n").split("\t")
    si, ki, hi, ni = h.index("sequence"), h.index("K562_log2FC"), h.index("HepG2_log2FC"), h.index("SKNSH_log2FC")
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) <= si:
            continue
        s = p[si].upper()
        if len(s) != L or set(s) - set("ACGT"):
            continue
        try:
            k = float(p[ki]); hv = float(p[hi]); nv = float(p[ni])
        except ValueError:
            continue
        seqs.append(s)
        acts.append((k, hv, nv))
seqs = np.array(seqs)
acts = np.array(acts)
max_abs = np.abs(acts).max(axis=1)
print(f"Loaded {len(seqs):,} sequences. max|log2FC|: median={np.median(max_abs):.3f}, "
      f"q75={np.quantile(max_abs, 0.75):.3f}, q90={np.quantile(max_abs, 0.90):.3f}")

# Keep top quartile by magnitude
q75 = np.quantile(max_abs, 0.75)
keep = np.where(max_abs >= q75)[0]
print(f"Kept {len(keep):,} sequences with max|log2FC| >= q75={q75:.3f}")

chosen = rng.choice(keep, size=N, replace=False)
out = seqs[chosen].tolist()
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} high-activity MPRA training sequences")

# Stats on what we kept
chosen_acts = acts[chosen]
for name, col in zip(["K562", "HepG2", "SKNSH"], range(3)):
    print(f"  {name}: mean={chosen_acts[:, col].mean():.3f}, std={chosen_acts[:, col].std():.3f}, "
          f"range=[{chosen_acts[:, col].min():.2f}, {chosen_acts[:, col].max():.2f}]")
