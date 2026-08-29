# 019 CpG=0.65 at GC=0.58 (joint optimization)

50k Markov chain. T[C→G]=0.65 (same as 015), but π=(0.21, 0.29, 0.29, 0.21)
i.e. stationary GC=0.58. Realized GC=0.579, CpG rate=0.188.

## Result
- **mean_r = 0.873** — NEW BEST (prev 0.868 at 015)
- **eval_01 = 0.888** — NEW BEST (prev 0.884 at 015)

vs 015 (CpG=0.65, GC=0.55): +0.005 mean, +0.004 eval_01

## Cell breakdown (easy evals avg)
| cell  | 015  | 019  | Δ     |
|-------|------|------|-------|
| K562  | 0.83 | 0.84 | +0.01 |
| HepG2 | 0.90 | 0.89 | -0.01 |
| SKNSH | 0.92 | 0.93 | +0.01 |

SKNSH gained the most (consistent with its high-GC preference). K562 also
slight up. HepG2 only slight down.

## Takeaway
**The GC peak shifts with CpG enrichment.** Without CpG, peak was 0.55-0.60.
With CpG=0.65, peak shifts to ~0.58. This is consistent with:
- More C bases → more CpG dinucleotides per sequence (composition × bias)
- High GC + CpG → CpG-island-like structure → tracks for all 3 cells

## Next
Push GC further. Try GC=0.60 with CpG=0.65. If 0.60 keeps improving,
go to 0.62. Otherwise 0.58 is the new peak.
