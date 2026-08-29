# 011_duplicate_half

## Hypothesis
25,000 unique random-uniform sequences, each duplicated to fill 50,000. Library-level marginal stats identical to 001 (random uniform 50k unique). Tests whether the eval cares about *number of distinct sequences* or only marginal sequence statistics.

## Method
Generate 25k random uniform 200bp sequences (seed 42), write them twice each (total 50k lines, 25k unique). Library mean GC ≈ 50%.

## Result
- **eval_01 mean_r = 0.3921** (K562=0.6169, HepG2=0.4315, SKNSH=0.1280)
- Drop of 0.006 vs random uniform (0.3981). Tiny — probably driven by slightly noisier library statistics with half the unique samples.

## Interpretation
Library uniqueness barely matters. The eval is largely insensitive to whether you submit 50k distinct sequences or 25k duplicated. The drop (~0.006) is consistent with the slight increase in marginal-stats noise from a smaller effective unique pool.

So: it's the marginal sequence distribution that matters, not per-sequence diversity. Random uniform marginals beat everything else.

## Next
- 012: every sequence has exactly 50 A's, 50 C's, 50 G's, 50 T's. Tightest possible per-seq base balance.
- Test whether tightening per-sequence base counts squeezes out any additional gain over random uniform.
