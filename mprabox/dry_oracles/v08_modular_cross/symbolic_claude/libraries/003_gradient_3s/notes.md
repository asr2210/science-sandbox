# 003 gradient_3s

50,000 sequences. Sequence i has fraction("3") = i/49999, rest uniform over {0,1,2}.
A monotone gradient: 0% threes at index 0, 100% at index 49999.

## Result
eval_01 = -0.0049 (vs 001 baseline 0.0013) — slight drop of ~0.006.
Other evals mixed: 03/12 went up to +0.0022, 13 went up to +0.0006,
04/09 down to -0.0052, 02/05 down to -0.0053.

## Interpretation
Confound: this experiment changed BOTH the order AND the average composition
(50% "3" instead of 25%). Cannot conclude whether order or composition drove the shift.

## Next
Run a control: SAME 50k sequences shuffled randomly. Compare to disambiguate.
