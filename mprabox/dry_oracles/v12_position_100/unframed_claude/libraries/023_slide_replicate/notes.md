# 023 slide_replicate

**Design:** Exact replicate of 020 with SEED=211 (vs 97 in 020). Top-12.5k cCREs by TFBS-density × 4 sliding windows.

**Result:** eval_01 = 0.0766 (vs 020: 0.0764). Confirms the slide-window-on-TFBS-hub recipe is the new genuine plateau (~0.0765), measurably above 011 (0.0760) — though the lift is small.

**Note:** because top-by-TFBS selection is mostly deterministic (only tiebreak jitter varies with seed), 020 and 023 share most of the same 12.5k cCREs. The two seeds confirm low variance for THIS recipe.

**Next:** try a weighted selection (TFBS × DHS-signal) and a wider slide offsets variant.
