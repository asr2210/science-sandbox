# 003 — ENCODE Registry V4 cCRE library

**Design.** 50,000 cCREs from ENCODE Registry V4 (GRCh38), sampled across element types: 25K dELS, 10K pELS, 7K PLS, 3K TF, 2K CA-CTCF, 3K CA. 200bp window centered on each element's midpoint, extracted from hg38 (uppercased; <5 N tolerated and replaced with random base).

**Result.** eval_01 = **0.3942** (Δ-0.025 vs random 001). Per cell: K562 = 0.546 (Δ-0.044), HepG2 = 0.558 (Δ-0.065), **SK-N-SH = 0.079 (Δ+0.034 — nearly doubled)**. eval_08 dropped sharply (0.319, vs 0.385 random).

**Interpretation — informative trade-off, not a uniform win.**
- Real biology HURT K562 and HepG2 performance substantially (~7% relative drop each).
- Real biology HELPED SK-N-SH (~75% relative increase, but still very low absolute 0.079).
- eval_08 is most punished (drop of 0.066 vs 001). Other eval sets dropped uniformly ~0.02-0.03.
- Net effect on mean_r is negative because K562/HepG2 dominate the absolute scale.

**Why?** Real cCREs are a *narrower* sequence distribution than random — GC-biased, selection-shaped, often promoter/enhancer-like. The model trained on cCREs sees less compositional diversity and so under-generalizes to whatever compositional spectrum the eval sets contain. But for SK-N-SH, the eval sequences' activity actually depends on biological grammar (TF motifs, regulatory architecture) which only real CREs provide.

**Theory update (v2 → v3).**
- *Compositional diversity (training distribution entropy)* drives K562/HepG2 generalization.
- *Biological grammar (real regulatory sequences)* is what unlocks SK-N-SH at all.
- These are **independent and complementary**. A library should provide both — random sequences for compositional coverage + real CREs for biological grammar.

**Next.** Test a 50/50 mix of random + real cCREs. Prediction: K562/HepG2 should land between 001 and 003 (perhaps ~0.57/0.59), SK-N-SH should land between (~0.06-0.08). If the mix is genuinely additive, mean_r should be similar to random (~0.42) but with non-zero SK-N-SH signal.
