# 025 — Planted TF consensus motifs in random backgrounds (10%)

**Hypothesis:** Motif-dense without cCRE redundancy → lifts eval_07/13
while providing light OOD without crowding cCRE diversity. Planted
1-4 motifs from 35 curated TF consensus k-mers into random ACGT 200bp.

**Design:** 17.5k genomic + 20k cCRE 5-window + 5k CpGi 5-window
+ 5k planted-motif synthetic + 1.25k uniform + 1.25k shuffled.

**Results vs exp 020 (best, 0.5468):**

| eval | exp 020 | exp 025 | Δ      |
|------|---------|---------|--------|
| 01   | 0.5778  | 0.5686  | -0.009 |
| 04/09| 0.5660  | 0.5698  | +0.004 |
| 07   | 0.6166  | 0.5919  | -0.025 |
| 08   | 0.1751  | 0.2253  | +0.050 |
| 10   | 0.5142  | 0.5009  | -0.013 |
| 13   | 0.5963  | 0.5693  | -0.027 |
| mean | 0.5468  | **0.5398** | **-0.0070** |

**Findings — eval_08 BIG lift (+0.050) but mean hurt badly:**

eval_08 jumped from 0.1751 to 0.2253 — the biggest single-eval lift
seen, exceeding TF ChIP CRM (+0.038). But the cost is large:
eval_07 (-0.025), eval_13 (-0.027), eval_01 (-0.009).

**Why it failed:** Motifs planted in pure random ACGT teach the model
that "motif in noise" is a signal pattern. Real motifs occur in
genomic flanking context with co-occurring elements. The model
learned a synthetic-bg pattern that doesn't transfer to genomic
test sequences (drops eval_07/13).

The eval_08 lift is misleading — it likely means eval_08 contains
some synthetic-bg-like sequences. The other evals are clearly
genomic-grounded.

**Theory v7.0:** When introducing motif content, the BACKGROUND must
match the distribution. Plant motifs in genomic backgrounds, not
random ACGT. Also: 10% may be too much. Try 2.5%.

**Plan exp 026:** Plant motifs in GENOMIC backgrounds at 2.5% dose
(1250 sequences) — test whether the source can help when properly
contextualized.
