# 001_random_baseline

## Setup
50,000 uniformly random 200bp DNA sequences (seed=1). No regulatory structure.

## Result
- eval_01=0.5131, eval_08=0.1624, eval_07=0.5790 (highest), eval_13=0.5594
- Mean of all 14 eval_r: ~0.49
- 31s training time

## Observations
1. Random sequences yield a *much* stronger baseline than expected. The model
   apparently learns sequence-composition features (GC, dinucleotide bias) that
   correlate with activity in real held-out eval sequences.
2. Several eval sets give identical r values:
   - eval_01=eval_02=eval_05=eval_14 (0.5131-0.5132)
   - eval_06=eval_11 (0.5123)
   - eval_03=eval_12 (0.5176)
   - eval_04=eval_09 (0.4175)
   So the 14 eval sets contain duplicates → effectively ~7 distinct evals.
3. eval_08 is a clear outlier (0.16). This is likely the hardest, most
   motif-dependent benchmark — improving it will be the strongest signal of
   learning real regulatory grammar.
4. SK-N-SH r is consistently the lowest of the three cell types across evals.

## Implication for theory
Random sequences leak ~0.5 r through composition features. We must do better
than 0.5 to claim any motif/grammar value. eval_08 is the canary for genuine
regulatory learning.
