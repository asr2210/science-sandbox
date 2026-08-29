# 004 — broad-GC random sequences

## Design
50,000 random sequences of length 200; per-sequence GC ~ Uniform(0.10, 0.90); each base drawn iid from that per-sequence multinomial.

## Result
- eval_01 mean_r = **0.4466** — WORSE than random uniform (0.5177) by 0.07
- K562 r ≈ 0.81 (vs 0.99) — dropped a lot
- HepG2 r ≈ 0.54 (vs 0.57) — slightly down
- SK-N-SH r ≈ 0 — still flat

## Reading
**Major finding.** The eval set composition is NOT broad — it's concentrated near GC≈0.5 (matching random uniform's binomial distribution). Extending training composition to [0.10, 0.90] put most training mass OUTSIDE the eval distribution, hurting prediction.

This **localizes the eval composition** very precisely: the eval set sequences look like random-uniform DNA, GC tightly around 0.5. Random uniform is the COMPOSITION SWEET SPOT for this benchmark.

## Implication
- Composition tuning is exhausted. Random uniform is the right base.
- To beat 0.5177, the lift must come from **motifs or other regulatory features** that random uniform doesn't have, WITHOUT changing the composition distribution.
- Next: random uniform base + implanted TF motifs.
