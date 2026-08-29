# 007 narrow_constrained — first improvement!

Each sequence: uniform random rejected unless every char count ∈ [45,55].

Result: eval_01 mean_r = **0.8597** (NEW BEST, +0.007 over uniform random).
- condition_a: 0.849 → 0.865 (UP)
- condition_b: 0.875 → 0.919 (UP)
- condition_c: 0.834 → 0.796 (DOWN slightly)

Net positive. The "composition std vs r" curve:
- std≈0 (exact balance):     mean=0.8185
- std≈3 (constrained [45,55]):mean=0.8597 ← best
- std≈6.1 (uniform random):  mean=0.8526
- std large (Dirichlet):     mean=0.6545

So compositional std should be small but nonzero. Optimal seems ~3.
Next: try even tighter constraint [48,52] (std≈1.4).
