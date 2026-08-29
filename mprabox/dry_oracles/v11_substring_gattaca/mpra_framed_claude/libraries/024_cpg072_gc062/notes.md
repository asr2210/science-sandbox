# 024 CpG=T[C→G]=0.72, GC=0.62

mean_r=0.872, eval_01=0.888. Slightly down from 021 (0.874, 0.890).

## CpG-GC joint surface map
| GC \ T[C→G] | 0.275 | 0.55 | 0.65 | 0.70 | 0.72 | 0.80 |
| 0.49 (014)  |      |      | -    |      |      |      | 0.858 |
| 0.55 (012/015/018/016) | 0.857 |      | 0.868 | 0.864 |      | 0.857 |
| 0.58 (019)  |      |      | 0.873 |      |      |      |
| 0.60 (020)  |      |      | 0.873 |      |      |      |
| 0.62 (021/023/024) |   | 0.868 | 0.874  |      | 0.872 |      |
| 0.65 (022)  |      |      | 0.869 |      |      |      |

Peak: (GC=0.62, T[C→G]=0.65) = 0.874. Smooth flat-top peak.

## Takeaway
The 1st-order Markov design is fully mapped. Joint (GC, CpG) peak is at
(0.62, 0.65 transition). Going off in any direction loses 0.005-0.020.

## Next
Move to 2nd-order Markov to add trinucleotide structure (CpG-island core
patterns like CGCG runs). Tests if higher-order context adds signal.
