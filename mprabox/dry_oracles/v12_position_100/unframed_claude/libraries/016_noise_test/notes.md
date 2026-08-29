# 016 noise_test

**Design:** EXACT REPLICATE of exp 011's recipe (4-mer K-Means(50) on 250k cCRE subsample, 1000/cluster, with-replacement fill) with seed=911 instead of 41.

**Result:** eval_01 = 0.0734. Compare:
- 011 (seed 41) = 0.0760
- 016 (seed 911) = 0.0734
- Delta = 0.0026

**Lesson — BIG:** the noise floor between same-recipe runs is ~0.003 on eval_01. This means:
- 011 vs 014 (0.0760 vs 0.0739, delta 0.0021) was WITHIN NOISE
- 011 vs 003 (0.0760 vs 0.0752, delta 0.0008) was almost certainly noise
- The whole "topic clustering helps" story may be largely noise too — only the random→cCRE gap (0.0648→0.073-0.076, +0.010) is clearly real

**Implication:** Tuning the cCRE recipe further is hopeless — I'm chasing noise. To make eval_01 jump meaningfully (>+0.005), I need a CATEGORICALLY different substrate, not a better sampler.

**Next theory (T4):** All my cCRE-based libraries are at the same ceiling. The 50k training budget is the bottleneck — each cCRE contributes a small amount and 50k of any reasonable cCRE-like substrate gives the same model. To break through I need:
- (a) Sequences with HIGHER information per token (TFBS hub regions, multi-modal regulatory)
- (b) Sequences spanning the activity dynamic range explicitly via real-MPRA (Tewhey/Sharpr)
- (c) An entirely different domain — e.g., Alu/LINE/repeat-rich for the genomic-distribution prior
