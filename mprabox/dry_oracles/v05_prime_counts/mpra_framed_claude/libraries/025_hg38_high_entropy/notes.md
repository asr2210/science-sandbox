# Exp 025 — High-entropy hg38 windows (top 50K of 150K by 4-mer entropy)

## Design
Filter for top-tier sequence complexity. Excludes low-complexity / repeat
regions. Library GC=0.443; CpG=0.0127.

## Result
**eval_01 = 0.0472; mean across evals = 0.044.** Signal redistributed:

| metric | 013 | 025 high-entropy |
|--------|-----|------------------|
| K562 mean | 0.038 | 0.043 |
| HepG2 mean | 0.053 | 0.038 |
| SKNSH mean | 0.046 | 0.051 |
| eval_01 K562 | 0.037 | 0.041 |
| eval_01 HepG2 | 0.057 | 0.044 |
| eval_01 SKNSH | 0.052 | 0.057 |

## Interpretation
Filtering for high entropy enriches for active accessible regions
(CpG-rich, high-information). These lift K562/SKNSH transfer (since K562
is dominant in cCRE definition) but actively HURT HepG2 — HepG2 may rely
on lower-entropy / repeat-context features that get filtered out.

## Theory update
- **Per-cell-type signal can be traded**, but the eval_01 mean stays
  pinned to ~0.05. This is more evidence the eval_01 ceiling is
  structural (model capacity / eval distribution), not library design.

## Next step
Try the opposite filter (low-entropy / repeat-rich) to confirm the
trade-off is real. If 026 produces inverse rebalancing (HepG2 up,
K562/SKNSH down), the trade-off mechanism is clear.

## Time
40s wall, 10s evaluator.
