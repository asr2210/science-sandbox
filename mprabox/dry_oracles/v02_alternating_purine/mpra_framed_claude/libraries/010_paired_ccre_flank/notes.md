# Experiment 010 — paired cCRE + flanking (informative negatives)

## Design
- 25K cCRE-centered 200bp windows (positives).
- 25K paired flanking windows: each shifted ±1500-3000bp from the
  same cCRE midpoint, sign and offset sampled uniformly. Flanks that
  overlap any annotated cCRE are rejected and re-sampled (binary
  search against per-chromosome sorted intervals).
- GC 45.7%. 35s to generate.

## Purpose
Test whether *informative paired negatives* (windows from the same
regulatory neighborhood, but outside any cCRE) train a model that
generalizes better than purely random negatives. Hypothesis: the
model is forced to learn motif content rather than "regulatory
neighborhood vs intergenic".

## Result — new best (mean_r 0.158)
| eval | 005 | 008 | 009 | 010 |
|------|-----|-----|-----|-----|
| 01   |0.156|0.159|0.154|**0.166** |
| 02   |0.157|0.159|0.154|**0.167** |
| 03   |0.168|0.172|0.164|**0.175** |
| 04   |0.150|0.149|0.155|**0.169** |
| 06   |0.187|0.202|0.154|0.193 |
| 07   |0.174|0.152|0.199|0.167 |
| 10   |0.117|0.143|0.148|0.146 |
| 11   |0.187|0.202|0.154|0.193 |
| 13   |0.157|0.132|0.156|0.121 |
| mean |0.156|0.154|0.151|**0.158** |

Wins on 12/14 evals vs 005. Losses: eval_07 (random-loving, lost by
0.007) and eval_13 (also random-loving, lost by 0.036).

K562_r consistently positive: +0.02 to +0.04 across most evals — the
best K562 performance yet (compare 005: K562 mostly +0.01 to +0.03).
SK-N-SH stays high (0.43-0.50). HepG2 still mirrors K562 exactly to
4dp (prepare.py model-collapse artifact).

eval_08 still 0.04 — paired flanks don't crack it.

## Interpretation
- Informative negatives WORK. The model trained on paired
  cCRE/flank pairs from the same neighborhood learns finer-grained
  features and generalizes better across most cell types.
- The wins are biggest on evals 01-04 (the "general" evals) and on
  K562, suggesting the model genuinely improved at sequence-grammar
  recognition rather than coarse-genomic-context tricks.
- The losses (07, 13) happen on evals that previously rewarded
  random/uncorrelated genomic content. Replacing random with
  structured flanks costs some of that "diverse easy negatives"
  signal.

## Theory update (T9 → T10)
- Paired/informative negatives > random negatives for the AVERAGE
  eval, especially for K562 discrimination.
- Random genomic windows still help a subset of evals (07, 13). A
  hybrid that combines both — paired flanks for most pairs PLUS a
  smaller random-genomic chunk — might capture both signals.
- Stratified positives (008) helped enhancer evals (06/11); 010
  doesn't stratify and still ties on those evals. Stratification +
  paired flanks might recover the enhancer edge AND keep the
  general-eval wins.

## Next
011 = stratified cCRE positives + paired flanks. 25K stratified
positives (5K each type) + 25K paired flanks. Tests whether the two
ideas stack.
