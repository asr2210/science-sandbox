# Exp 028 — chr22 + chr19 + chr1 (40/40/20)

50k 200bp windows: 20k chr22 + 20k chr19 + 10k chr1.

## Result

| metric  | chr22+chr19 (027) | + chr1 20% (028) |
|---------|------------------:|-----------------:|
| eval_01 | **0.3215**        | 0.3197           |
| k562    | 0.1446            | 0.1447           |
| hepg2   | 0.2004            | 0.2013           |
| sknsh   | 0.6196            | 0.6132           |

Adding 20% chr1 lifted HepG2 (+0.001) but dropped SKNSH (-0.006).
Net loss -0.0018.

Confirms: chr22+chr19 50/50 = local optimum. chr1's 42% GC drags
SKNSH down more than its HepG2 benefit.

**Plan for exp 029**: chr22+chr19+chr1 with only 5-10% chr1 (lighter
dose to minimize SKNSH cost while keeping diversity).
