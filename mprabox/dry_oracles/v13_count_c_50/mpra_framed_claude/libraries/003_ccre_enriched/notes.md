# 003 — ENCODE cCRE-Enriched Library

**Hypothesis:** Regulatory-enriched sequences have denser motif content
and should improve all evals, especially eval_07/13 (most
motif-dependent). Predicted mean_r 0.55–0.65.

**Design:** Sample 50,000 cCREs (V3 ENCODE Combined, 926k elements,
primary chroms only). For each, take 200bp centered on the cCRE
midpoint. 50% strand-flip for balance. Seed 0.

**Results (mean_r per eval, Δ vs exp 002 random genomic):**
- eval_01: 0.5147 (+0.011 marginal)
- eval_02/05: 0.5148 (+0.010)
- eval_03/12: 0.4976 (-0.022)
- eval_04/09: **0.5528 (+0.166 BIG WIN)**
- eval_06/11: 0.5091 (+0.004)
- eval_07: **0.4811 (-0.156 LOSS)**
- eval_08: **0.3053 (+0.442 PARTIAL RECOVERY)**
- eval_10: 0.4674 (+0.012)
- eval_13: **0.4661 (-0.155 LOSS)**
- eval_14: 0.5147
- Mean across 14: **0.493** (vs 0.458)
- Time: 104 s (longer training — wider activity range?)

**Per-cell-type for the affected evals:**
- eval_07: K562 stayed at 0.69 (unchanged), HepG2 0.61→0.42, SKNSH 0.61→0.33
- eval_13: K562 0.69→0.67, HepG2 0.58→0.40, SKNSH 0.59→0.32

So cCRE training **does not help K562** (already saturated there) and
**actively hurts HepG2 and SK-N-SH** on eval_07/13.

**What this tells me — major theory update:**

cCRE enrichment is NOT a strict improvement over random genomic. It
trades:
- Wins on eval_04/09 (+0.17), eval_08 (+0.44 partial)
- Losses on eval_07/13 (-0.16 each)
- Wash on eval_01

Why? Two hypotheses to test:

**H1: distributional diversity hypothesis.** Random genomic gives the
model broad exposure to many sequence regimes (regulatory and
non-regulatory). cCRE concentrates training in a narrower regulatory
manifold. The model becomes excellent at predicting cCRE-like
sequences but worse at predicting *anything else*. If eval_07/13
contain non-cCRE-like test sequences (e.g., random genomic, intronic
enhancers, low-grade regulatory regions), cCRE training systematically
mispredicts them.

**H2: cell-type bias hypothesis.** cCREs are discovered using
chromatin marks pooled across ENCODE cell types — but the discovery is
biased toward well-characterized cell types (K562 leads ENCODE
sequencing). HepG2 and SK-N-SH-specific elements may be relatively
under-represented in cCRE catalogs. So cCRE-trained models do well on
K562 (the dominant signal in the catalog) but worse on HepG2/SK-N-SH.

H2 is more consistent with the per-cell-type drop pattern (K562
stayed high, HepG2/SKNSH dropped). But H1 may also contribute.

**Counter-intuitive lesson:** "More regulatory enrichment" is NOT
always better. The OPTIMAL library probably mixes:
- Background genomic (for breadth + cell-type-agnostic generalization)
- Regulatory enriched (for motif density)
- And possibly more

**Theory v3:**

(a) Compositional coverage: random gives ~0.15 floor
(b) Motif density: genomic adds ~0.30; cCRE adds another marginal
    amount BUT introduces bias
(c) **Distributional breadth**: genomic > cCRE on this axis. A
    narrow training distribution underperforms even when the
    distribution is "richer per sequence."
(d) **Cell-type label balance**: a library that over-represents one
    cell type's regulatory elements will train a model biased to that
    cell type, hurting predictions on others — even at the same
    architecture / training budget. This is critical for
    generalization to unseen cell types.

**Next experiment:** Mixed library (50% random genomic + 50% cCRE).
Predictions:
- eval_07/13 should recover toward 0.62 (broad context restored)
- eval_04/09 should partially keep the +0.17 (some cCRE preserved)
- eval_08 should keep partial recovery
- eval_01 should land around 0.55

If mixing works, theory v3 is supported and the next move is to add
cell-type-diverse regulatory data (DHS peaks from many tissues, not
just cCRE) to address (d).
