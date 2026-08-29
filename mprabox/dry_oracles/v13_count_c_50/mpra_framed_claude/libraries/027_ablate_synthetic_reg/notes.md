# 027 — Ablate synthetic regularizers (uniform + shuffled)

**Hypothesis:** Test whether the 2.5% uniform + 2.5% shuffled
synthetic regularization in exp 020 is load-bearing, or inert noise.

**Design:** Remove both synthetic sources. Scale cCRE 4k→5k unique
and CpGi 1k→1.5k unique (still 5-window each).
- 17,500 genomic + 25,000 cCRE + 7,500 CpGi = 50,000

**Results vs exp 020 (best, 0.5468):**

| eval | exp 020 | exp 027 | Δ      |
|------|---------|---------|--------|
| 01   | 0.5778  | 0.5723  | -0.006 |
| 04/09| 0.5660  | 0.5763  | +0.010 |
| 07   | 0.6166  | 0.5990  | -0.018 |
| 08   | 0.1751  | 0.2115  | +0.036 |
| 10   | 0.5142  | 0.5019  | -0.012 |
| 13   | 0.5963  | 0.5759  | -0.020 |
| mean | 0.5468  | **0.5431** | **-0.0037** |

**Findings — synthetic regularizers are load-bearing:**

Removing them hurt mean by 0.0037 (outside seed noise). But notice
the PATTERN of damage matches TF ChIP CRM exactly: eval_08 +0.036
(big lift), eval_04/09 +0.010, eval_07 -0.018, eval_13 -0.020.

This is the **same tradeoff** as exp 023. Mechanism: removing the
"anti-cCRE" synthetic noise + scaling up cCRE/CpGi → model becomes
more cCRE-biased → lifts OOD/composition (which has cCRE-like
queries) but hurts motif specificity (which needs grammar-level
discrimination).

**Theory v7.1:** Synthetic regularizers (uniform + mono-shuffled cCRE)
are not just noise — they're **structural counterweights** that
prevent the model from over-fitting to cCRE chromatin signatures.
They preserve motif-grounded performance by ensuring the model
distinguishes "motif" from "cCRE-region prior".

**Plan exp 028:** Push synthetic regularization HIGHER (5% uniform
+ 5% shuffled = 10% total). Test if more counterweight further
tilts toward motif-grounded evals.
