# 002 homopolymers_stratified

12,500 each of "0...0", "1...1", "2...2", "3...3" — length 200.

## Result
mean_r = NaN for ALL evals (because condition_a is NaN).
condition_b and condition_c are defined and small (mostly negative for b).

## Key insight (HUGE)
Scoring uses `scipy.stats.pearsonr` (per the warning), computed across the 50k
sequences. Condition_a became constant across the 4 homopolymer values — meaning
the underlying model gave identical output for all 4 homopolymers in that condition.
This means we need WITHIN-SUBMISSION DIVERSITY to get a defined score at all.

condition_b/c still defined — they vary across the 4 homopolymers, so the underlying
model captures *some* feature (composition?) that differs across homopolymers.

## Implication
- Scorer evaluates model_k(sequence_i) for each i and condition
- Computes Pearson r between predictions and a hidden per-sequence target
- mean_r = mean of 3 conditions
- To get positive r: model outputs must correlate with the hidden target
