# 011 within-library GC mix (25k @ 0.5 + 25k @ 0.6)

## Result
- mean_r = 0.756 (eval_01 = 0.770)
- Much worse than either component alone (-0.10 from GC=0.6)

## Takeaway
Even a NARROW within-library GC mix (only 0.10 spread) catastrophically
hurts. Confirms unimodal-labels-required hypothesis from exp 005. The MPRA
activity distributions for GC=0.5 vs GC=0.6 are different enough that
mixing them within a single library breaks the model's ability to fit.

Single fixed GC is the only viable strategy.
