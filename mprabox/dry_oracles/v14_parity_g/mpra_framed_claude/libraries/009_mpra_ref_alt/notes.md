# 009 — Ref+alt allele pairs from K562+SK-N-SH MPRA TSVs

25,000 unique variant locations × 2 alleles (ref + alt) = 50,000 lines, all 200bp. Window centered on variant. Chr7/13 excluded. HepG2 TSV skipped (~all NA chr).

**Result:** mean_r = -0.0006. eval_07 K562 = 0.0118 (highest seen for eval_07!), eval_08 HepG2 = 0.0068. But eval_13 K562 dropped to 0.0004 (was 0.0143 in 008) and eval_10 SK-N-SH = -0.0134.

**Interpretation:** Pairing ref+alt didn't help broadly. Hypothesis: the simulator's eval is robust to single-bp paired contrasts but the cost was halving unique location diversity (25k locations vs 008's 50k). Lost the K562/eval_13 signal that 008 picked up.

**Lesson:** Diversity of locations > paired contrasts at this scale. To pair, you need many more locations to start with.
