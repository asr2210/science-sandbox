# Skill: 3D joint activity stratification for MPRA libraries

## Setting
You need to choose N sequences (typically 50,000) from a labeled MPRA
dataset like Gosai/Malinois (200bp DNA sequences with K562_log2FC,
HepG2_log2FC, SKNSH_log2FC). The selected set is used to train an
oracle/scoring model, and that model is evaluated against held-out
test data. Optimization target: Pearson r between predictions and
held-out labels per cell line.

## Best-performing recipe
**3D quantile stratification on (K562, HepG2, SKNSH) with a 4×4×4 grid.**

1. Read all (K562_lfc, HepG2_lfc, SKNSH_lfc, sequence) tuples.
2. Compute quantile edges separately for each cell line:
   `edges_K = [Q(K562, i/4) for i in 1..3]` (3 cutpoints).
3. Bin every sequence by its (K562_bin, HepG2_bin, SKNSH_bin) triple
   → 4×4×4 = 64 cells.
4. From each cell, randomly sample `ceil(50000/64) = 782` sequences
   (without replacement; with replacement only if a cell is sparse).
5. Shuffle and truncate to exactly 50,000.

## Why it works
- **Coverage of the joint activity space** trains the downstream
  oracle to predict any (K, H, S) combination rather than just the
  bulk diagonal where K, H, S are correlated (r ≈ 0.8 in Malinois).
- **64 cells** is a sweet spot: enough resolution to span activity
  gradient, but each cell still holds ~800 sequences, giving the
  oracle within-bin sequence diversity to learn from.
- Coarser (3×3×3, 27 cells): too few activity gradations → -0.01.
- Finer (5×5×5 or 6×6×6): some cells get only a few real sequences →
  noisier training → -0.005 to -0.015.

## What NOT to do (tested, ranked worst → near-best)
- Composition-only bias (GC content): hurts
- Random TF motif insertion in random backbones: hurts vs random
- Top-K by |log2FC| (max-magnitude): overweights one cell, K562 lift small
- Filter by lfcSE (low SE): narrows distribution, hurts
- Highest-z (cleanest) sequences within each bin: hurts vs random within bin
- Adding curated CRE class on top: neutral / slightly worse
- PCA-decorrelating the 3D axes before stratifying: neutral
- Seed unions / averaging multiple stratified samples: neutral

## Expected score (Malinois → eval_01.mean_r)
- Uniformly random 200bp: 0.131
- Random Malinois 50k: 0.152
- Single-cell extremes: 0.170
- 1D quantile stratification (10 bins): 0.174
- 3D joint stratification 4×4×4: **0.191** (plateau / noise floor 0.19)

## Notes
- K562 and HepG2 oracle outputs in this setup are **identical** to 4
  decimals. They are not informative as separate signals. Treat as one
  cell line for design purposes; you can stratify on average(K562,
  HepG2) without losing information.
- SKNSH oracle saturates around r ≈ 0.46-0.51 on Malinois data; the
  K562/HepG2 component is the lever that moves between strategies.
- To push above 0.19, would need to score candidate sequences with a
  trained model (e.g., download/train Malinois CNN, predict on full
  pool, select by predicted variance × activity).
