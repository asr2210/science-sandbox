# Exp 003: GC=70% biased random

**Hypothesis**: High-GC composition (CpG-island-like) would *raise* mean_r.

**Method**: 50k random sequences with p(A)=p(T)=0.15, p(C)=p(G)=0.35.

**Results**:
- eval_01 mean=0.3567 (vs 0.4203 random) → **-0.064**
- K562: 0.5048 (vs 0.5847) → -0.080
- HepG2: 0.5231 (vs 0.6175) → -0.094
- SKNSH: 0.0421 (vs 0.0587) → -0.017

**Interpretation**: STRONG signal in the OPPOSITE direction from my hypothesis.
High GC hurts. Composition matters a lot more than motif content.

Two possible explanations:
1. The metric rewards libraries with high dynamic range, and skewed
   composition reduces variance in predicted activity.
2. The model prefers natural-like compositions (~42% GC). Random 50% may
   already be slightly off-optimum.

**Implications**: Next test GC=30% to see if symmetric, or natural-like.
