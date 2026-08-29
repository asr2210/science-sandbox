# 021 CpG=0.65, GC=0.62

50k Markov. Realized GC=0.62, CpG=0.20.

## Result
- mean_r = 0.874 (eval_01 = 0.890) — NEW BEST (prev 0.873/0.888)
- Improvement is at noise floor (+0.001 mean), but eval_01 +0.002

GC sweep with CpG=0.65:
| GC   | mean_r | eval_01 | K562 | HepG2 | SKNSH |
| 0.55 | 0.868 | 0.884 | 0.83 | 0.90 | 0.92 |
| 0.58 | 0.873 | 0.888 | 0.84 | 0.89 | 0.93 |
| 0.60 | 0.873 | 0.888 | 0.84 | 0.89 | 0.94 |
| 0.62 | 0.874 | 0.890 | 0.84 | 0.89 | 0.95 |

SKNSH keeps climbing. K562 plateaued. HepG2 slowly slipping.

## Next
- Try GC=0.65 (022) — does SKNSH gain still outpace HepG2 loss?
- If yes, push further. If no, GC peak is at ~0.62.
