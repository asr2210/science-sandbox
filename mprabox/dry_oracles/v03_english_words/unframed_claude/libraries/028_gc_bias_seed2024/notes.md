# Exp 028 — GC-bias 0.23/0.27/0.27/0.23, seed=2024

**Hypothesis**: Maybe model prefers slightly GC-enriched random
(GC=54%) — between flat random and CpG-island-like.

**Result**: eval_01 = 0.4213.

vs seed=2024 pure random (0.4278): -0.0065 (worse).

**Interpretation**: Slight GC bias HURTS. Consistent with the earlier
finding that GC>50% drives K562/HepG2 down — the cliff is sharp.
AT-bias (Exp 027) was neutral; GC-bias is bad. The metric prefers
GC ∈ [0.46, 0.50].

**Takeaway**: Composition perturbations don't help. The flat-prior
random seed lottery is the only lever that moves the needle.
