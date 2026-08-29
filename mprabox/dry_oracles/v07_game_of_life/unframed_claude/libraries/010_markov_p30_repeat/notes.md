# 010_markov_p30_repeat

## Hypothesis
A first-order Markov chain with mild self-repeat bias (P(next=prev)=0.30) generates sequences with slightly longer mean runs and shifted dinucleotide composition. Tests whether random uniform i.i.d. is at a local optimum on the dinuc-structure axis, or whether mild "naturalness" can push above 0.398.

## Method
- 4×4 transition matrix: 0.30 on diagonal, 0.70/3 off-diagonal.
- 50,000 sequences sampled. Seed 42.
- Result: mean max-run = 5.10 (vs ~6 for random uniform), GC ≈ 50% (binomial spread same as iid).

## Result
- **eval_01 mean_r = 0.3892** (K562=0.6084, HepG2=0.4262, SKNSH=0.1328)
- Drop of ~0.009 vs random uniform (0.3981).

## Interpretation
Mild repeat bias *hurts*. Combined with prior result for 007 (anti-repeat hurts -0.023), the dinucleotide axis has a clear local optimum at random uniform i.i.d. — repeats at the random-uniform-implied rate.

Pattern:
- 007 (P(repeat)=0, no runs > 3): -0.023
- 001 (P(repeat)=0.25, uniform): 0
- 010 (P(repeat)=0.30): -0.009

Strong evidence T4 holds. Random uniform is a local maximum.

## Next
- 011: duplicates test — does library uniqueness matter?
- 012: 90/10 mix of random uniform + real DNA — does small biological "contamination" hurt linearly?
