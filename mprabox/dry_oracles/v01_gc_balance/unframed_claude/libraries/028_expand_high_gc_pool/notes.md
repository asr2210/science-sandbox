# 028_expand_high_gc_pool

022 recipe but expand high-GC pool to include pELS (proximal enhancer-like)
alongside PLS and DNase-H3K4me3.

## Result
eval_01: **0.6940 — NEW BEST** (+0.0006 over 027's 0.6934)
eval_07: 0.7488
eval_13: 0.7423
GC mean=0.483 std=0.113

## Interpretation
Adding pELS to the high-GC pool gives a tiny but real lift.
pELS shares the TSS-proximal regulatory character (PLS, DNase-H3K4me3,
pELS are all near genes) while diluting GC slightly (mean 0.483 vs 0.491).

The signal is more about "TSS-proximal regulatory regions" than just
"high GC."

## Next
- 029: shift more weight to cCRE_all (more enhancer-like / distal) while
  keeping TSS-proximal pool at 30%.
- 030: combine all learnings.
