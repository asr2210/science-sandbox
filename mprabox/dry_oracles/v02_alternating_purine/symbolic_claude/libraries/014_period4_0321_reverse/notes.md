# Exp 014 — reverse period-4 (0,3,2,1) at p=0.7

## Result
eval_01 mean_r = 0.1536, condition_c = 0.396.
Nearly identical to (0,1,2,3) at 0.1550 — ascending and descending
score equivalently.

## Interpretation
The scorer has cyclic + reflection symmetry — both monotonic orderings
work equally well. Non-monotonic (0,2,1,3) failed (0.095). So the
lever isn't "ascending" specifically; it's "monotonic in mod-4 cycle"
i.e., consecutive bases in the natural order.

## Next
Test the "alternating purine" hint from sibling project paths:
period-2 template (0,2) at p=0.7. Each position alternates between
bases 0 and 2 (preferred). Bases 1 and 3 still present (0.1 noise).
If this beats period-4, period-2 with these two bases is the lever.
