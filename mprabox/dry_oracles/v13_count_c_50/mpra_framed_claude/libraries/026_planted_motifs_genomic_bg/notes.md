# 026 — Planted TF motifs in GENOMIC backgrounds, 2.5% dose

**Hypothesis (theory v7.0):** Exp 025 failed because random ACGT
backgrounds break motif transfer. Plant the same motifs into
genomic 200bp at lower dose (2.5%) → should not hurt mean.

**Design:** 21.25k genomic + 20k cCRE 5-window + 5k CpGi 5-window
+ 1.25k planted-motif (genomic bg, 1-3 motifs) + 1.25k uniform
+ 1.25k shuffled.

**Results vs exp 020 (best, 0.5468) and exp 025 (random bg, 0.5398):**

| eval | exp 020 | exp 025 | exp 026 | Δ vs 020 |
|------|---------|---------|---------|----------|
| 01   | 0.5778  | 0.5686  | 0.5774  | -0.000   |
| 04/09| 0.5660  | 0.5698  | 0.5643  | -0.002   |
| 07   | 0.6166  | 0.5919  | 0.6161  | -0.001   |
| 08   | 0.1751  | 0.2253  | 0.1741  | -0.001   |
| 10   | 0.5142  | 0.5009  | 0.5138  | -0.000   |
| 13   | 0.5963  | 0.5693  | 0.5954  | -0.001   |
| mean | 0.5468  | 0.5398  | **0.5456** | -0.0012 (within noise) |

**Findings — theory v7.0 confirmed:**

Genomic backgrounds eliminate the motif-transfer damage. At 2.5%
dose with proper bg, planted motifs are NEUTRAL: mean matches
exp 020 within seed noise. The exp 025 eval_08 jump was entirely
a random-bg artifact, not signal — eval_08 here = baseline 0.1741.

**Implication:** Planting synthetic motifs doesn't ADD signal once
cCRE multi-window is present. The model already learns motifs from
real genomic context; reintroducing them artificially in genomic
bg is redundant. The signal saturates at exp 020-style composition.

**Remaining strategy:** I have 4 experiments left and a clear ceiling
~0.5468 across multiple variants. Next moves:
- exp 027: Test whether synthetic regularizers (uniform + shuffled,
  5% total) are actually needed. Drop them, scale cCRE+CpGi up.
- exp 028: Try denser cCRE multi-window offsets [-100,-50,0,50,100]
  (focused on cCRE core) vs current [-200,-100,0,100,200].
- exp 029: Confirm best library at seed=2.
- exp 030: Final selection.
