"""Experiment 14: MPRA training sequences stratified by measured activity.

Source: Tewhey/Gosai MPRA training data with measured K562_log2FC, HepG2_log2FC,
SKNSH_log2FC per sequence. Stratify so the library spans the full activity
range uniformly in each cell line.

Strategy: combine three cell-type activity scores into a 3D activity vector,
project to principal-axis-or-mean, and bin. Or simpler: stratify each cell
type independently and union.

We'll use a 3D grid: 6 bins per cell line × 6 × 6 = 216 cells, ~232/cell.
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=14)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

print("Reading MPRA dataset...")
records = []
with open(src) as f:
    header = f.readline().rstrip("\n").split("\t")
    seq_i = header.index("sequence")
    k_i = header.index("K562_log2FC")
    h_i = header.index("HepG2_log2FC")
    s_i = header.index("SKNSH_log2FC")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= seq_i:
            continue
        s = parts[seq_i].upper()
        if len(s) != L or set(s) - set("ACGT"):
            continue
        try:
            k = float(parts[k_i]); h = float(parts[h_i]); n = float(parts[s_i])
        except ValueError:
            continue
        records.append((s, k, h, n))
print(f"Loaded {len(records):,} valid records with activity labels")

seqs_arr = np.array([r[0] for r in records])
acts = np.array([(r[1], r[2], r[3]) for r in records], dtype=np.float64)
print(f"Activity stats:")
for name, col in zip(["K562", "HepG2", "SKNSH"], range(3)):
    print(f"  {name}: mean={acts[:, col].mean():.3f}, std={acts[:, col].std():.3f}, "
          f"range=[{acts[:, col].min():.2f}, {acts[:, col].max():.2f}]")

# 3D stratification with 6 bins per axis (quantile-based, equal-count bins)
n_per_axis = 6
total_cells = n_per_axis ** 3   # 216
per_cell = N // total_cells     # 231

# Compute quantile boundaries per axis
boundaries = []
for col in range(3):
    q = np.quantile(acts[:, col], np.linspace(0, 1, n_per_axis + 1))
    # Slightly expand edges so all samples bin
    q[0] -= 1e-6
    q[-1] += 1e-6
    boundaries.append(q)

def bin_3d(act):
    ix = []
    for c in range(3):
        b = np.searchsorted(boundaries[c], act[c], side="right") - 1
        b = min(max(b, 0), n_per_axis - 1)
        ix.append(b)
    return tuple(ix)

# Group records by cell
print(f"Grouping into {total_cells} 3D cells...")
cells = {}
for i, a in enumerate(acts):
    key = bin_3d(a)
    cells.setdefault(key, []).append(i)
populated = len(cells)
print(f"  {populated}/{total_cells} cells populated")

# Sample per_cell from each populated cell
out_idx = []
for key, members in cells.items():
    take = min(per_cell, len(members))
    chosen = rng.choice(members, size=take, replace=False)
    out_idx.extend(chosen)

print(f"  collected {len(out_idx)} from stratified sample")

# Top up to N with uniform-random from full set
if len(out_idx) < N:
    remaining_idx = list(set(range(len(records))) - set(out_idx))
    pad_n = N - len(out_idx)
    pad = rng.choice(remaining_idx, size=pad_n, replace=False)
    out_idx.extend(pad.tolist())
elif len(out_idx) > N:
    # Trim
    rng.shuffle(out_idx)
    out_idx = out_idx[:N]

rng.shuffle(out_idx)
out_seqs = [records[i][0] for i in out_idx]
assert len(out_seqs) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out_seqs) + "\n")
print(f"Wrote {len(out_seqs)} activity-stratified sequences")

# Realized activity stats
out_acts = np.array([acts[i] for i in out_idx])
for name, col in zip(["K562", "HepG2", "SKNSH"], range(3)):
    print(f"  {name} realized: mean={out_acts[:, col].mean():.3f}, std={out_acts[:, col].std():.3f}")
