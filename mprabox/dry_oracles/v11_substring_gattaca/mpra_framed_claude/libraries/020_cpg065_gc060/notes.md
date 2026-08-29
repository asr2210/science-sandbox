# 020 CpG=0.65, GC=0.60

50k Markov. Realized GC=0.60, CpG=0.195.

## Result
- mean_r = 0.873, eval_01 = 0.888 — TIED with 019 (both new best)

GC sweep with CpG=0.65:
| GC | mean_r | eval_01 |
| 0.55 (015) | 0.868 | 0.884 |
| 0.58 (019) | 0.873 | 0.888 |
| 0.60 (020) | 0.873 | 0.888 |

Flat plateau from GC=0.58 to 0.60 with CpG=0.65.

SKNSH still creeping up (0.94 vs 0.93 at GC=0.58). HepG2 same. K562 same.

## Next
- Push GC to 0.62 (021)
- After GC peak is mapped, try simultaneously refining CpG at the new GC
