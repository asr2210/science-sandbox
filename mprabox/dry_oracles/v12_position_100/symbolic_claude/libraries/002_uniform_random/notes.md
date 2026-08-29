# Exp 002: Uniform random

## Setup
50K sequences, each length 200, drawn iid uniform from {0,1,2,3}.

## Results
Scores per eval (mean_r):
- eval_01=0.0648  eval_14=0.0648
- eval_02=0.0634  eval_05=0.0634
- eval_03=0.0782  eval_12=0.0782
- eval_04=0.0813  eval_09=0.0813
- eval_06=0.0653  eval_11=0.0653
- eval_07=0.1310  eval_08=0.0563
- eval_10=0.1194  eval_13=0.1186

## Observations
- All POSITIVE. With 50K samples, std of corr is ~0.004 → these are highly significant.
- Eval pairs match EXACTLY: (01,14), (02,05), (03,12), (04,09), (06,11). Five duplicate pairs + four uniques → 9 distinct evals.
- ~30s of work; ~22s of measurement.

## Theory implication
Mean(|pearson r|) of two length-200 random vectors ≈ sqrt(2/π)/sqrt(199) ≈ 0.057. Very close to most evals' values (0.05-0.08). The high ones (0.13) might use length-50 fragments (gives ~0.11).

**Refined hypothesis: per-sequence pearson correlation** between my_seq (as int vector) and a hidden target sequence per eval, then aggregated (mean or mean of |r|).
