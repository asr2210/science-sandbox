# 018_ccre_gc_filtered

cCREs filtered to per-sequence GC in [40%, 55%].

## Result
eval_01: 0.4594 — DROP from 0.684 baseline.
eval_07: 0.6628 — DROP from 0.741.

## Key learning: VARIANCE MATTERS
Restricting GC variance crashed the score. Confirms that per-sequence
variance in (probably) GC content (or correlated features) drives the
correlation coefficient up.

This means: WIDER GC variance in the library may push higher than the
cCRE-all 0.684. Real DNA has natural GC variance (some sequences 25% GC,
others 65% GC); restricting to 40-55% removes this signal.

## Next
Try a library that maximizes biologically meaningful variance: real DNA from
sources with very different GC profiles (CpG islands + heterochromatin).
