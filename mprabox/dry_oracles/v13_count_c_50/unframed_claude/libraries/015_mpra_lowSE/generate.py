"""Experiment 15: MPRA training sequences filtered by low measurement error.

Hypothesis: sequences with low lfcSE in all three cell lines are
high-confidence measurements -> both ground-truth and eval models likely
agree most on them -> higher Pearson r.

Take sequences whose mean(K562_lfcSE, HepG2_lfcSE, SKNSH_lfcSE) is in the
lowest quartile, then sample 50K.
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=15)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

print("Reading MPRA dataset...")
seqs = []
ses = []
with open(src) as f:
    header = f.readline().rstrip("\n").split("\t")
    si = header.index("sequence")
    kse = header.index("K562_lfcSE")
    hse = header.index("HepG2_lfcSE")
    sse = header.index("SKNSH_lfcSE")
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) <= si:
            continue
        s = p[si].upper()
        if len(s) != L or set(s) - set("ACGT"):
            continue
        try:
            a = float(p[kse]); b = float(p[hse]); c = float(p[sse])
        except ValueError:
            continue
        seqs.append(s)
        ses.append((a, b, c))
seqs = np.array(seqs)
ses = np.array(ses)
mean_se = ses.mean(axis=1)
print(f"Loaded {len(seqs):,} sequences with valid lfcSE values")
print(f"lfcSE per-cell stats: mean={ses.mean(0)}, median={np.median(ses, 0)}")
print(f"mean_se: median={np.median(mean_se):.4f}, q25={np.quantile(mean_se, 0.25):.4f}, "
      f"q75={np.quantile(mean_se, 0.75):.4f}")

# Filter to lowest quartile (most confident)
q25 = np.quantile(mean_se, 0.25)
keep = np.where(mean_se <= q25)[0]
print(f"Kept {len(keep):,} sequences with mean_se <= q25={q25:.4f}")

if len(keep) >= N:
    chosen = rng.choice(keep, size=N, replace=False)
else:
    # Fallback - take next quartile too
    chosen = keep
    q50 = np.quantile(mean_se, 0.50)
    extra = np.where((mean_se > q25) & (mean_se <= q50))[0]
    need = N - len(chosen)
    if len(extra) >= need:
        chosen = np.concatenate([chosen, rng.choice(extra, size=need, replace=False)])
    else:
        chosen = np.concatenate([chosen, extra])
        print(f"WARNING only {len(chosen)} available")

out = seqs[chosen].tolist()
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} low-SE MPRA training sequences")
