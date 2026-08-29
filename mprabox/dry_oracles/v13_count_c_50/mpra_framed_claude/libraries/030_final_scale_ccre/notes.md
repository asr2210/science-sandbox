# 030 — Scale cCRE to 6k×5 with synthetic counterweight (FINAL)

**Hypothesis:** Exp 027 hurt mean by removing synthetic AND scaling
cCRE. Was the scaling part actually bad? Test: scale to 6k×5 cCRE
WITH synthetic counterweight preserved (5%).

**Design:** 12.5k genomic + 30k cCRE (6k × 5) + 5k CpGi + 1.25k uniform
+ 1.25k shuffled.

**Results vs exp 020 (best, 0.5468) and exp 027 (0% synth, scaled cCRE):**

| eval | exp 020 | exp 027 | exp 030 | Δ vs 020 |
|------|---------|---------|---------|----------|
| 01   | 0.5778  | 0.5723  | 0.5716  | -0.006   |
| 04/09| 0.5660  | 0.5763  | 0.5770  | +0.011   |
| 07   | 0.6166  | 0.5990  | 0.5948  | -0.022   |
| 08   | 0.1751  | 0.2115  | 0.2250  | +0.050   |
| 10   | 0.5142  | 0.5019  | 0.5041  | -0.010   |
| 13   | 0.5963  | 0.5759  | 0.5712  | -0.025   |
| mean | 0.5468  | 0.5431  | **0.5431** | -0.0037 |

**Findings — cCRE scaling itself is bad:**

Exp 030 (with synthetic) matches exp 027 (no synthetic) mean exactly.
The 5% synthetic counterweight CANNOT compensate for the cCRE overload
when cCRE goes from 4k to 6k unique. The cCRE-bias wins:
- eval_08 lifted even more (+0.050, biggest in entire study)
- eval_07/13 hurt as much as exp 027

**Conclusion:** Exp 020's 4k unique × 5 windows cCRE = 20k is at
the sweet spot. More cCRE diversity adds OOD signal but at greater
cost to motif-grounded performance than the synthetic counterweight
can fix.

**Final library = exp 020 composition with seed=0** (3-seed verified
mean = 0.5463 ± 0.001, single-seed best 0.5468). See final summary
in notebook.md.
