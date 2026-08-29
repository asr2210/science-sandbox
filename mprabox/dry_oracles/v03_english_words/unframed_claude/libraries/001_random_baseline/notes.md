# Exp 001: random baseline

**Hypothesis**: Uniform random gives baseline mean_r near zero or unknown direction.

**Method**: 50,000 sequences, each 200bp, uniform i.i.d. from {A,C,G,T} with seed=0.

**Results** (from result.json):
- eval_01 mean=0.4203, K562=0.5847, HepG2=0.6175, SKNSH=0.0587
- range of mean_r across 14 evals: 0.3809 (eval_08, anomalous low) to 0.4250
- K562 always ~0.58, HepG2 always ~0.62, SKNSH always ~0.06

**Surprises**:
1. RANDOM gets POSITIVE correlation 0.42 on average. So the metric is not "predicted vs measured activity" in the naive sense — random sequences happen to be predictive of *something*. Possible: noise-resistant metric, or correlation between two model predictions, or the library is matched against natural-sequence baseline.
2. Many evals look identical (01=02=05=14 at 0.4203; 04=09 at 0.4250; 06=11 at 0.4201; 03=12 at 0.4169). Looks like there are maybe ~6–8 unique eval sets with duplication.
3. eval_08 is anomalously low (0.3809) — possibly stricter/different test.
4. SKNSH cell type is far harder than K562/HepG2 — only 0.06 on random.

**Implications**: 
- Direction unknown. Need next exp to perturb baseline and see which way scores move.
- Need to maximize each of K562, HepG2, SKNSH. SKNSH has most headroom but probably needs cell-type-specific design.
- For now, eval_01 is primary metric. Random baseline = 0.4203.
