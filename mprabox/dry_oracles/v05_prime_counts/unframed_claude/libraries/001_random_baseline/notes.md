# Experiment 001 — Random baseline

## Hypothesis
Uniformly random sequences anchor the baseline. Predicted: low mean_r
on all eval sets if the oracle rewards regulatory grammar.

## Method
50K x 200bp sequences sampled iid from uniform(A,C,G,T), seed=0.

## Results (eval_01..eval_14 mean_r)
```
eval_01: 0.0420
eval_02: 0.0422
eval_03: 0.0413
eval_04: 0.0489
eval_05: 0.0422
eval_06: 0.0418
eval_07: 0.0254
eval_08: 0.1237  <-- much higher
eval_09: 0.0489
eval_10: 0.0320
eval_11: 0.0418
eval_12: 0.0533
eval_13: 0.0203
eval_14: 0.0420
```
Average mean_r over 14 sets: ~0.046

## Observations
- Most eval sets land 0.02-0.05 (essentially zero — confirms random).
- eval_08 is ~3x higher (0.124). Interesting — either eval_08 baseline
  is naturally higher, or random uniform DNA already contains motifs
  it likes.
- Some eval sets appear paired (identical values: 01=14, 02=05,
  03=12, 04=09, 06=11). So likely only 9 distinct evaluators with
  some duplicated, OR cell-type tasks reuse outputs.
- HepG2 is consistently the strongest of the 3 cell types on random.

## Theory update
T1 (mean predicted activity) still consistent. ~0.04 = essentially
chance level. Big runway to improve.

## Next
Try GC-rich content. Many enhancers/promoters are GC-rich; CpG
islands are ~60-70% GC.
