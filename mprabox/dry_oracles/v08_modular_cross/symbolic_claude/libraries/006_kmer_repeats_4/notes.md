# 006 kmer_repeats_4

50,000 sequences, each = random 4-mer (one of 256) repeated 50 times → length 200.

## Result
eval_01 = -0.0010 (near baseline).
**eval_10 jumped to +0.0069 (highest single eval so far).**
condition_a is small positive (0.0021) for eval_01, condition_b is negative (-0.0043).

## Interpretation
- 4-mer identity systematically influences some evals (eval_10) but not eval_01.
- Low-complexity sequences hurt condition_b (which seems to reward sequence complexity).
- Different evals reward different features.

## Pattern observed across exps for eval_01:
| Exp | condition_a | condition_b | condition_c | mean |
|---|---|---|---|---|
| 001 random | -0.0003 | 0.0067 | -0.0025 | 0.0013 |
| 005 dirichlet | 0.0003 | 0.0070 | 0.0016 | 0.0030 |
| 006 4-mer rpt | 0.0021 | -0.0043 | -0.0007 | -0.0010 |
| 003 grad_3 | -0.0127 | 0.0057 | -0.0078 | -0.0049 |

condition_b loves diversity/complexity; condition_a is small for everything.
