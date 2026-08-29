# 001_random_uniform

Uniform random 200bp from {A,C,G,T}, seed 0, 50,000 sequences.

## Result
- eval_01: mean=0.1357 (K562=0.256, HepG2=0.032, SKNSH=0.119)
- eval_04 / eval_09: mean=0.3956 (identical — duplicate evals)
- eval_08: mean=0.5787 (K562=0.176, HepG2=0.764, SKNSH=0.796)
- eval_07 / eval_13: mean ≈ -0.137 (mostly negative)
- eval_05 = eval_02 (duplicates)
- eval_06 = eval_11 (duplicates)
- eval_14 = eval_01 (duplicates)
- eval_03 = eval_12 (duplicates)

Distinct eval groups (by score signature):
- A: {01, 14}
- B: {02, 05}
- C: {03, 12}
- D: {04, 09}
- E: {06, 11}
- F: {07}
- G: {08}
- H: {10}
- I: {13}

→ Only ~9 distinct evals. Many are duplicates / identical scoring.

## Observations
- K562_r is positive across all 14 evals (0.18–0.34): K562 model gives random sequences a positive correlation/score consistently. Either K562 is "easy" or random is informative for K562.
- HepG2 swings from -0.33 (eval_07) to +0.76 (eval_08). Highly eval-dependent.
- SKNSH similar pattern to HepG2.
- Negative scores on eval_07, eval_13 suggest the metric isn't just |score| — direction matters. Random anti-correlates with whatever eval_07/13 reward.

## Hypotheses to update
- The metric "_r" is most likely Pearson correlation between something on my side and something on the eval side. With zero per-sequence ground-truth from me, it's probably between paired sequences. **Most likely:** prepare.py treats my 50K sequences as paired with their fixed reference set of 50K labeled sequences (perhaps by row index), and computes Pearson between predicted activity of mine vs measured activity of theirs. Random sequences would average to mean activity ≈ population mean, giving low |r| with high noise.
- Alternative: r is correlation between two predictors applied to my library (model A vs model B). Random sequences would naturally give moderate-to-high agreement.

## Runtime
~23s wallclock for prepare.py.
