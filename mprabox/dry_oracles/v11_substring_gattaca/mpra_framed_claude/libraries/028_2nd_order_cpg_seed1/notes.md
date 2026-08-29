# 028 Reseed 025 (seed=1)

Same design as 025. Realized GC=0.66, CpG=0.23 (matches 025).

## Result
mean_r=0.874, eval_01=0.889. Below 025 by -0.005.

## Takeaway
**Seed variance at 2nd-order chain is ~0.005.** Larger than iid noise
floor (0.003 from exp 001 vs 008). The 2nd-order chain has more
between-seed variance because clustered positions amplify variance.

Best 025 result (0.879) is partly seed luck. Robust expected: 0.876±0.003.

## Implications for final
Either 025 design (best seen, 0.879) or 021 design (1st-order, robust 0.874).
The expected 025 value (0.876) edges 021 (0.874) by +0.002 on mean,
+0.005 on eval_01. 025 still wins in expectation.

## Next
- Exp 029: Try recalibrating 1st-order base for 025-style chain to land
  at realized GC=0.62 (instead of 0.66). Tests if the GC drift hurt.
- Exp 030: Final library = best design.
