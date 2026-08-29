# 014_gc_normal_sigma07

## Hypothesis
Per-seq GC drawn from N(0.5, 0.075), clipped to [0.20, 0.80]. Empirical per-seq GC std ≈ 0.082 (~2.3× random uniform's binomial std of 0.035). Mean GC = 0.5.

If T5 (more per-seq variance helps): r > 0.398.
If T3 (binomial spread is sweet spot, wider hurts smoothly): r ~ 0.390-0.395.
If a plateau exists in this range: r ~ 0.398.

## Result
- **eval_01 mean_r = 0.3989** (K562=0.6188, HepG2=0.4358, SKNSH=0.1421)
- This is **statistically indistinguishable from random uniform (0.3981)** — within the 0.001 noise floor measured in 009.

## Interpretation
Widening per-seq GC std from 0.035 (binomial) to 0.082 (~2.3×) has **zero effect on the score**. This is a *major* finding that refines T3/T5:

**Theory T6**: The score has a wide flat plateau on the per-seq GC axis between roughly [0.035, ~0.10]. Random uniform is NOT at a peak — it's sitting on a broad plateau. Penalty only kicks in for wider variance (005 at σ=0.23 dropped 0.033; 004 at σ=0.30 dropped 0.058).

T3 is REVISED: the penalty curve isn't smooth across all σ — there's a flat region near random uniform, then quadratic-or-worse decline for σ > 0.10.

Combined with 012's catastrophe at σ=0:
- σ = 0: r ≈ 0.024 (12)
- σ = 0.010 (015, pending): ?
- σ = 0.035: r ≈ 0.398 (001 random uniform)
- σ = 0.082: r ≈ 0.399 (014)
- σ = 0.10 estimate: r ≈ 0.395?
- σ = 0.23: r ≈ 0.365 (005)
- σ = 0.30: r ≈ 0.340 (004)

## Next
- 015 (already prepped): σ_GC = 0.010 (tight) — does the plateau extend below binomial, or do we start sliding toward 012's collapse?
- 016 onward: depending on 015, refine the variance frontier or explore orthogonal levers.
