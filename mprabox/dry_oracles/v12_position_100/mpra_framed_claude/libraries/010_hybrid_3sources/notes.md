# Experiment 010: 3-source hybrid (cCRE + DNase + H3K27ac + random)

## Design
50K sequences:
- 15K cCREs (6K dELS + 4K pELS + 2.5K PLS + 1.5K CA_TF + 1K CA-CTCF)
- 5K each K562/HepG2/SKNSH DNase peaks (15K total)
- 5K each K562/HepG2/SKNSH H3K27ac peaks (15K total)
- 5K random non-cCRE/non-peak autosomal background
Seed=10.

## Results — REGRESSION vs 009
| eval | 009 hybrid | **010 3-source** | Δ |
|---|---|---|---|
| 01 | **0.0772** | 0.0753 | **-0.0019** |
| 02 | **0.0755** | 0.0737 | -0.0018 |
| 03 | **0.0955** | 0.0911 | -0.0044 |
| 04 | **0.0913** | 0.0896 | -0.0017 |
| 06 | **0.0765** | 0.0748 | -0.0017 |
| 07 | **0.1437** | 0.1429 | -0.0008 |
| 08 | 0.0639 | **0.0648** | +0.0009 |
| 10 | **0.1286** | 0.1281 | -0.0005 |
| 13 | **0.1409** | 0.1374 | -0.0035 |
Time: 110s (slower — more file IO)

010 loses on 8/9 distinct eval sets. Only eval_08 improved trivially.

## Per-cell eval_01
- K562: 0.0783 (vs 009 0.0799, -0.0016)
- HepG2: 0.0789 (vs 009 0.0812, -0.0023)
- SKNSH: 0.0688 (vs 009 0.0705, -0.0017)
All three cells got worse.

## What I learned
**H3K27ac is REDUNDANT with DNase, not orthogonal.** The "more orthogonal
sources = better" hypothesis is WRONG. H3K27ac peaks live almost entirely
within DNase peaks (active enhancers are accessible), so adding them
duplicates information already present. The penalty: less cCRE share
(15K vs 20K) and less DNase share (15K vs 25K) for no information gain.

The cCRE→DNase jump in 009 worked because DNase added a NEW signal type
(cell-type-specific accessibility) that cCREs lacked. H3K27ac adds nothing
DNase didn't already provide on these cells.

## Theory update
- "Orthogonal sources stack" only holds if sources are TRULY orthogonal
- Within a cell type, DNase and H3K27ac are highly correlated (both mark
  active regulatory regions). Sequence content of their peaks heavily overlaps
- Adding redundant sources DILUTES the more informative ones (cCREs, DNase)
- The 009 composition (20K cCRE + 25K DNase + 5K random) was likely near
  optimal for this mix of sources

## Next: optimize 009's composition (no new sources)
009 is the new ceiling. Try variations on its proportions:
- Exp 011: tilt MORE toward DNase (15K cCRE + 30K DNase + 5K random)
  — tests whether the cell-type-specific signal scales further
- If 011 < 009: composition already optimal; try qualitatively different
  signal sources (e.g., ATAC-seq from other cells, evolutionarily
  conserved regions, eQTL-overlapping sequences)
