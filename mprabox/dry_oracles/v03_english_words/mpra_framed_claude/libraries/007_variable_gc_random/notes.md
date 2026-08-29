# 007 — Variable-GC random

**Design.** 50K random 200bp; each sequence's GC content drawn uniformly from [0.25, 0.75]; bases sampled per-position based on that target GC.

**Result.** eval_01 = **0.3706**. K562 = 0.521, HepG2 = 0.540, SK-N-SH = 0.051. WORSE than uniform-50%-GC random on every cell type.

| | K562 | HepG2 | SK-N-SH | mean |
|---|---|---|---|---|
| 001 uniform 50% GC | 0.590 | 0.623 | 0.045 | 0.419 |
| 007 variable GC | 0.521 | 0.540 | 0.051 | 0.371 |

**Interpretation.** The eval distribution is *composition-narrow* — concentrated around 50% GC, uniform-random-like. Any broadening of the training composition (variable GC) reduces K562/HepG2 r dramatically. This is a clean signal that the eval sets contain (mostly) random-like, 50%-GC sequences for the K562/HepG2 axis.

**Theory v7.** The K562/HepG2 r ceiling under uniform random training (~0.6) appears to be set by training-eval composition match. The eval sequences likely include synthetic-random sequences themselves, and the optimal training composition is uniform-50%-GC random. Any perturbation that shifts overall composition (variable GC, real cCREs, shuffled cCREs) hurts K562/HepG2 r.

**Implication.** To improve beyond random baseline, I need a library that:
1. Preserves uniform-50%-GC composition overall (don't shift k-mer distributions).
2. Adds biological signal in a way that doesn't disrupt composition.

This rules out: variable GC, real CREs, shuffled CREs, and mixes of these.
This allows: small embedded biology (a 20bp real motif in 180bp random background changes overall composition only slightly).

**Next.** Test random backgrounds with single short real-CRE fragments embedded. If a 20bp real-CRE chunk in 180bp random gives K562/HepG2 ≈ 0.58 + SK-N-SH > 0.045, that's a strict improvement on random. If it kills K562/HepG2 too, then even small biology insertions are too disruptive — and there may be no way to improve on random.
