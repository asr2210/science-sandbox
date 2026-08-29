# 002 — random 200bp windows from hg38 autosomes

## Design
Sampled 50,000 200bp windows uniformly at random across autosomes 1–22 (proportional to chromosome length). Rejected any window containing 'N'. Seed=0. Sampling kept ~96% of attempts.

## Result
- eval_01 mean_r = **0.4861** (vs 0.5177 for random uniform — WORSE by ~0.03)
- K562 r ≈ 0.895 (vs 0.99) — dropped significantly
- HepG2 r ≈ 0.558 (vs 0.567) — basically unchanged
- SK-N-SH r ≈ 0.005 (vs −0.009) — essentially still zero

## Reading
- Random genomic DNA has a **narrower composition distribution** than uniform random (e.g., GC ~41% with biological variance vs binomial variance around 50%). That narrower composition coverage HURT K562 prediction more than the increased "naturalness" helped — strong evidence that K562 activity in eval sets is composition-driven and the model needs broad composition exposure.
- HepG2 unchanged — the natural-genomic motifs present aren't more useful than the random-uniform features the model already learned.
- SK-N-SH still ≈ 0 — random genomic windows do NOT contain SK-N-SH-active regulatory features at meaningful density. Most genomic DNA is non-regulatory.

## Implication
Throwing real DNA at the problem without enrichment for regulatory function buys nothing — and costs composition coverage. The path forward is sequences that BOTH (a) keep composition broad and (b) inject regulatory information densely.
