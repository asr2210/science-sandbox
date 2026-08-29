# 029 — Exp 020 composition with SEED=2 (3rd noise sample)

**Purpose:** Third seed replication of best library (exp 020 composition)
to bound true mean and noise band.

**Results:**

| seed | mean | eval_01 | eval_07 | eval_08 | eval_13 |
|------|------|---------|---------|---------|---------|
| 0    | 0.5468 | 0.5787 | 0.6168 | 0.1743 | 0.5968 |
| 1    | 0.5456 | 0.5777 | 0.6180 | 0.1691 | 0.5975 |
| 2    | 0.5465 | 0.5780 | 0.6128 | 0.1806 | 0.5926 |
| mean | **0.5463** | 0.5781 | 0.6159 | 0.1747 | 0.5956 |

**Noise band:** range = 0.0012, std ≈ 0.0006. Single-seed noise
~±0.0006 around the true mean. Most per-eval noise is ±0.001-0.005.

**Conclusion:** The exp 020 composition has a robust true mean of
0.5463 ± 0.001. Seed=0 happens to be on the high end (0.5468) which
is well within seed noise of the true value.

**Plan exp 030:** Final swing — try scaling cCRE further (6k unique
× 5 = 30k cCRE) while KEEPING 5% synthetic counterweight. Tests
whether more cCRE diversity (with proper counterweight balance)
breaks past the 0.5463 plateau.
