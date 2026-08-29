# 015 4 buckets EXACT composition (170/10/10/10 shuffled per seq)

NaN across all evals + ConstantInputWarning x42.
Lesson: scorer requires VARIANCE in per-seq feature it extracts.
Exact compositions per seq create zero variance somewhere → NaN.

CONSTRAINT: must have variance in per-seq composition (use iid draws, not exact).
