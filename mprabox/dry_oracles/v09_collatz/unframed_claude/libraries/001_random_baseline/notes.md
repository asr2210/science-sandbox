# Exp 001 — Random 50% GC baseline

50,000 sequences, 200bp, iid uniform from {A,C,G,T}, seed 42.

## Result

| eval | mean_r | k562_r | hepg2_r | sknsh_r |
|------|-------:|-------:|--------:|--------:|
| 01   | 0.2307 | 0.1361 | -0.0742 | 0.6302  |
| 02   | 0.2311 | 0.1373 | -0.0741 | 0.6300  |
| 03   | 0.2334 | 0.1287 | -0.0736 | 0.6450  |
| 04   | 0.2251 | 0.1093 | -0.0384 | 0.6044  |
| 05   | 0.2311 | 0.1373 | -0.0741 | 0.6300  |
| 06   | 0.2313 | 0.1357 | -0.0721 | 0.6303  |
| 07   | 0.2141 | 0.1154 | -0.1272 | 0.6542  |
| 08   | 0.0864 | 0.0848 | -0.0004 | 0.1749  |
| 09   | 0.2251 | 0.1093 | -0.0384 | 0.6044  |
| 10   | 0.2312 | 0.1211 | -0.0610 | 0.6335  |
| 11   | 0.2313 | 0.1357 | -0.0721 | 0.6303  |
| 12   | 0.2334 | 0.1287 | -0.0736 | 0.6450  |
| 13   | 0.2087 | 0.1048 | -0.1211 | 0.6425  |
| 14   | 0.2307 | 0.1361 | -0.0742 | 0.6302  |

Total scoring time: 44s (well under 30 exp budget).

## Observations

1. `mean_r = mean(k562_r, hepg2_r, sknsh_r)` exactly (eval_01: 0.2307 == (0.1361-0.0742+0.6302)/3).
2. SK-N-SH is much higher than the other two for random sequences (0.63).
3. HepG2 is *negative* for random — random sequences "anti-correlate" or score below baseline for HepG2.
4. eval_08 is anomalously low across the board (mean=0.086). Some evals duplicate each other (02==05, 04==09, 11==06).
5. Random gives non-trivial r — so "r" is unlikely to be a Pearson correlation that requires library variance. More likely it's average predicted activity per cell type from a held-out scoring model.

## Implication for strategy

If `_r` is mean predicted activity, the task is: design sequences that score high on all three cell-type models. Strong activating TF motifs should boost score (if hypothesis is right). Test in exp 002.
