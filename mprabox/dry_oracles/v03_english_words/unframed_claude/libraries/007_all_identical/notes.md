DIAGNOSTIC: all 50k sequences identical.
Result: NaN across all evals.
This confirms the score is Pearson-r-style: needs variance across library.
Implication: to maximize r, we need a library that produces WIDE VARIANCE
in predicted activities (some high, some low), AND the predictor must
RANK them correctly.
Strategy from here: design libraries with deliberate activity gradients,
e.g. bimodal (motif-rich + random) or graded (varying motif density).
