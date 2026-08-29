# 024 — Random + 1x30bp PLS

eval_01 = **0.4173**. K562 0.583 / HepG2 0.609 / SK-N-SH 0.060.

Slightly longer than 25bp. K562/HepG2 dropped without SK-N-SH gain. Net loses to 012.

**Length sweep summary (PLS-only, single fragment, random offset):**
| Length | eval_01 | K562 | HepG2 | SK-N-SH |
|---|---|---|---|---|
| 15bp (022) | 0.4211 | 0.585 | 0.614 | 0.064 |
| 18bp (023) | 0.4217 | 0.590 | 0.616 | 0.059 |
| **25bp (012)** | **0.4248** | **0.591** | **0.619** | **0.065** |
| 30bp (024) | 0.4173 | 0.583 | 0.609 | 0.060 |

25bp is a clear local optimum. The peak is sharp; shorter and longer both drop.
