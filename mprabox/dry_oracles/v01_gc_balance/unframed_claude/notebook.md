# Lab Notebook

## 2026-06-02 15:55 — Setup & initial theory

### Setup
- Black-box scoring across 14 eval sets, with eval_01 as primary metric.
- Per-eval returns mean_r, k562_r, hepg2_r, sknsh_r — suggests cell-type-specific regulatory activity prediction (MPRA-like).
- 50,000 sequences of 200bp from {A,C,G,T}.
- 30 experiments total.

### Initial theory (v1)
The scorer likely measures correlation (Pearson r) of predicted regulatory activity in K562, HepG2, SK-N-SH cell lines against some held-out reference set. The score probably reflects:
- (a) presence of cell-type-specific TF binding motifs
- (b) overall regulatory potential (promoter/enhancer-like signature)
- (c) maybe sequence composition / GC content

Plausible the "r" is correlation between predicted activity of *our* library and measured activity of a *held-out* library; in that case our scores reward having a *diverse* library that spans a range of activity levels, not just being uniformly high.

OR — more likely — the scorer trains/applies a model and reports correlation of predicted activity with some ground-truth-derived score per sequence. We probably want sequences that elicit *strong* predicted regulatory activity.

### Plan for experiment 001
Random baseline: uniform sampling from {A,C,G,T}. This anchors the score scale and tells us how far random sits.

Predicts: low mean_r, since random sequences have no enrichment of regulatory elements.

## 2026-06-02 15:58 — Experiment 001 result

Random baseline: eval_01 mean_r = 0.4637. Surprisingly high.

### Observations
- 14 evals but only ~8 unique due to duplicates: eval_01==14, 02==05, 03==12, 04==09, 06==11.
- eval_08 is an outlier (0.15), seemingly hardest.
- Across cell lines: HepG2 typically highest, SKNSH lowest.
- Scoring takes ~10s — fast, can iterate.

### Theory update (v2)
Random ≠ near-zero score. The scorer probably computes Pearson r between (a) a hidden "ground truth" derived from each sequence and (b) a hidden "prediction" applied to each sequence — both derived from sequence-internal features. For random sequences both pick up basic dinucleotide/GC patterns and agree at r≈0.46.

Implication: to improve, sequences need to be more *informative* — span a wider range of regulatory activity, and ideally exhibit features that one or both models pick up strongly. The score may reward libraries that include real regulatory elements (e.g., promoters with strong TF motifs) because the predictor model is presumably trained on real DNA and will give confident, discriminative outputs on real-like sequences.

### Plan for experiment 002
GC-rich biased random sequences (60% GC). Promoter/enhancer regions are GC-richer than genomic average. Tests whether GC alone shifts the score, separate from motif content.

Predicts: small positive shift if GC matters, larger if it doesn't reach the level of motif-level patterns.

## 2026-06-02 16:02 — Experiment 002 result: HUGE signal

GC-rich (60% GC) → eval_01 = -0.2388 (FROM +0.4637). eval_07: -0.59 (from +0.51).

This is a big finding. The scoring function is highly sensitive to GC content.
Going from 50% GC to 60% GC flipped the sign of correlation on most evals.

### Theory update (v3)
The hidden target/prediction relationship strongly involves GC content.

Hypothesis: For each sequence the scorer computes (target, prediction). The
correlation across the 50k library is the metric. There must be SOMETHING the
scorer's target rewards that anti-correlates with high GC for the prediction.

But the sign FLIP (not just decrease) means the relationship is not just
"high-GC is bad" — it's that the ordering reversed. This suggests the within-
library variance in *something else* (NOT mean GC) is what's being measured,
and shifting the mean GC shifted the relative ordering / disagreement between
predictor and target.

Or perhaps simpler: across libraries, the score depends on average sequence
features. Real promoters/enhancers have specific GC distributions, and 60% GC
is outside the natural distribution, causing model disagreement.

### Plan for experiment 003
Test the opposite: AT-rich (40% GC, P(A)=P(T)=0.30). If symmetric, we should
see a similar sign flip. If asymmetric, only one direction matters.

## 2026-06-02 16:07 — Experiments 003, 004, 005 results

| exp | description | eval_01 | eval_07 | eval_13 | eval_04 | eval_08 |
|---|---|---|---|---|---|---|
| 001 | random 50% GC | 0.464 | 0.507 | 0.490 | 0.402 | 0.151 |
| 002 | 60% GC | -0.239 | -0.588 | -0.557 | 0.144 | 0.057 |
| 003 | 40% GC | 0.466 | 0.712 | 0.690 | 0.089 | 0.041 |
| 004 | 30% GC | 0.498 | 0.697 | 0.674 | 0.149 | 0.069 |
| 005 | chr22 real DNA | 0.678 | 0.746 | 0.743 | 0.581 | 0.123 |

### Findings
- GC content matters but the bigger lever is real-DNA-likeness.
- eval_04 (and dup 09) PREFERS natural variance (penalized by all biased composition, but real DNA recovers).
- eval_08 is special: stays stubbornly low even with real DNA. Likely measures something orthogonal (sequence diversity / k-mer coverage?).

### Theory update (v4)
The scorer's "ground truth" appears to be some predictive model of regulatory activity (likely an MPRA-trained sequence-to-activity model for K562, HepG2, SK-N-SH). The Pearson r is computed across the 50k library between predicted activity (by the eval model) and target activity (by a hidden reference model). When sequences are biologically realistic (real DNA), both models give meaningful, agreeing outputs → high r. When sequences are random or compositionally weird, the predictor's outputs are not informative → r drops.

Implication: optimal strategy is sequences that look as much like real regulatory DNA as possible, with maximum diversity in regulatory activity (so the correlation has variance to measure).

### Plan for experiment 006
Target highly regulatory regions specifically: ENCODE cCREs (candidate cis-regulatory elements for hg38). These are pre-curated regions enriched for promoter/enhancer activity. Predict eval_01 > 0.75.

## 2026-06-02 16:25 — Experiments 006-008 results

| exp | description | eval_01 | eval_07 | eval_13 | eval_04 |
|---|---|---|---|---|---|
| 005 | chr22 random | 0.678 | 0.746 | 0.743 | 0.581 |
| 006 | cCRE all categories | 0.684 | 0.741 | 0.724 | 0.609 |
| 007 | whole genome random | 0.615 | 0.760 | 0.756 | 0.384 |
| 008 | PLS (promoter) only | 0.088 | -0.097 | -0.079 | 0.359 |

### Key findings
- cCRE-all barely beats chr22-random. Regulatory enrichment alone is not the lever.
- chr22 (gene-rich) > whole genome on eval_01 → eval_01 rewards gene-rich regions but is not just about being "real DNA."
- PLS catastrophe → promoter regions are too GC-rich (CpG islands). Same composition trap as exp 002.

### Theory update (v5)
The scoring function is sensitive to the COMPOSITIONAL DISTRIBUTION of the library.
- Composition matching natural genome (~41% GC) helps eval_07/13.
- Composition matching gene-rich regions (~48% GC, more CG/CGI features) helps eval_01.
- Extreme high GC (CpG-island-like, >60%) tanks everything.

Saturation near 0.68 for eval_01 with broad "real DNA" libraries suggests we need:
(a) sequences with high regulatory activity that *aren't* GC-island promoters
(b) maybe MPRA-tested sequences with known activity
(c) MAYBE diversity of composition WITHIN the library matters — variance helps
    correlation

### Plan
- 009: dELS (distal enhancers, less GC-rich) only — should match cCRE all
- 010: dinucleotide-shuffled chr22 — test motif vs k=2 composition
- 011: download MPRA-tested sequences if accessible (DREAM challenge / ENCODE)
- 012+: mix winning sources, design with motif insertion

## 2026-06-02 16:50 — Mid-run summary (experiments 9-16)

| exp | description | eval_01 | eval_07 | eval_04 |
|---|---|---|---|---|
| 009 | dELS only | 0.671 | 0.750 | 0.547 |
| 010 | chr22 shuffled | 0.571 | 0.686 | 0.358 |
| 011 | chr22+wholegenome mix | 0.657 | 0.760 | 0.501 |
| 012 | FANTOM5 enhancers | 0.656 | 0.736 | 0.522 |
| 013 | chr22 + motif insertions | 0.662 | 0.740 | 0.543 |
| 014 | K562+HepG2+SKNSH accessible | 0.393 | 0.431 | 0.491 |
| 015 | chr19 random | 0.674 | 0.732 | 0.611 |
| 016 | cCREs excl PLS | 0.682 | 0.742 | 0.597 |

### Critical observation
**chr22 random sampling remains the best for eval_01 (0.6780).**
All elaborate strategies (cCREs, FANTOM5, motif insertion, gene-dense chr19,
cell-type accessible) match or slightly underperform.

### Theory update (v6)
The scoring function rewards:
1. Real-DNA-like sequence character (HUGE signal — pushed from 0.46 → 0.68)
2. Moderate GC content centered around 45-50% (chr22-like)
3. Some unidentified property that gene-dense chromosomes have

But NOT:
- Cell-type-specific accessibility (drops score, due to GC enrichment)
- Synthetic motif insertion (no benefit)
- Pure enhancer/promoter regions (PLS catastrophe)
- Mere diversity (mixing sources doesn't help past chr22 alone)

The ceiling at 0.68 likely reflects the inherent agreement between the predictor
and ground-truth functions on broad real-DNA libraries. To go higher we'd need
sequences from the predictor's actual training distribution (likely MPRA-tested
sequences with known measured activity).

### Plan for next experiments
- 017: chr17 + chr19 + chr20 + chr22 mix (multi gene-dense)
- 018: GENCODE gene-overlapping regions
- 019: phastCons highly conserved regions
- 020: ENCODE rDHS (representative DHS)
- 021-024: try to find/use MPRA-trained model predictions for selection
- 025-030: final combinations & optimization

## 2026-06-02 17:30 — Experiment 018-019: VARIANCE BREAKTHROUGH

| exp | description | eval_01 | eval_07 | eval_13 |
|---|---|---|---|---|
| 018 | cCRE filtered GC 40-55% | 0.4594 | 0.6628 | 0.6439 |
| 019 | 5-source max-variance mix | **0.6895** | **0.7615** | **0.7549** |

Exp 018 deliberately *narrowed* per-seq GC variance → score collapsed
from 0.68 → 0.46. Exp 019 deliberately *widened* it (5 sources spanning
30-65% GC) → score jumped to 0.6895, new best on eval_01, eval_07, eval_13.

### Theory update (v7) — VARIANCE HYPOTHESIS CONFIRMED
The metric is Pearson r — explicitly bounded by within-library *variance*
of whatever features the scorer measures. Restricting variance destroys
the score; expanding variance with real-DNA-realistic sequences raises it.

This reframes everything:
- Past plateau at 0.68 wasn't a hard ceiling; it was the variance of a
  single biological source.
- PLS catastrophe (exp 008) was high-GC outside the natural distribution.
  But PLS as 1/5 of a mixed library (exp 019) contributes useful variance.
- Composition extremes are information when mixed with their opposites.

### Plan for experiments 020-030
- 020: push variance further — add chrY heterochromatin + CpG island cores
  (most extreme GC poles) to the 5-source mix
- 021: bimodal pure — 50% very-AT (chrY/satellite-like) + 50% very-GC (CpG island cores)
- 022: ENCODE rDHS (representative DHS) as additional source
- 023: optimal mix — combine 019's mix with extra extreme-GC sources
- 024-027: search optimal source weights
- 028-030: final combinations

## 2026-06-02 18:30 — Experiments 020-027: ratio search

| exp | description | eval_01 |
|---|---|---|
| 020 | 7 src + chrY + chromHMM Het/Quies | 0.6822 |
| 021 | 7 src euchromatic (no chrY/Het) | 0.6908 |
| 022 | 30% high-GC cCRE + 5 src | **0.6930** |
| 023 | 50% high-GC cCRE (overshoot) | 0.6865 |
| 024 | 022 + split cCRE_all into subcategories | 0.6916 |
| 025 | 022 minus whole_genome | 0.6901 |
| 026 | 022 + explicit chr1/11/16 instead of WG | 0.6924 |
| 027 | 022 with different seed | 0.6934 |

### Theory update (v8) — VARIANCE-WITHIN-TRAINING-DISTRIBUTION
exp 020 confirmed: chrY satellites and chromHMM Het/Quies move outside
the predictor's training distribution. Wide GC variance from these
sources does NOT help — adds noise.

Variance helps ONLY among sequences the predictor can score meaningfully
(euchromatic real DNA, including regulatory elements). Within that
constraint, the optimal mix uses:
- ~50% chr-derived (gene-dense + WG) for low-mid GC variance
- ~20% cCRE_all for natural cCRE distribution
- ~30% TSS-proximal high-GC (PLS+DNase-H3K4me3) for the high-GC pole

The 30% high-GC sweet spot was found by ratio sweep (014→022→023).
Seed-variation (027) showed 0.693 is stable; noise floor ±0.0004.

## 2026-06-02 19:00 — Experiments 028-030: refinement

| exp | description | eval_01 |
|---|---|---|
| 028 | 022 + pELS in high-GC pool | **0.6940** |
| 029 | 028 with more cCRE_all, less chr | 0.6935 |
| 030 | 028 + dELS,CTCF-bound compound | 0.6940 (tied) |

### Final summary — what works
**Best score: 0.6940 (exp 028 and 030 tied)**

Started from random baseline 0.4637. Total improvement: +0.230.

Recipe (028, winning):
- 5,000 × chr22 + 5,000 × chr19 + 5,000 × chr17 + 5,000 × chr20 (gene-dense)
- 5,000 × whole_genome (length-weighted random)
- 10,000 × cCRE_all (natural cCRE mix)
- 15,000 × cCRE PLS|DNase-H3K4me3|pELS (TSS-proximal high-GC)
Total: 50,000. GC mean ≈ 0.48, std ≈ 0.11.

### Final theory (v9)
The scorer computes Pearson r between two sequence→activity models
(predictor and ground truth). r is bounded by within-library variance of
features both models read. Maximizing r requires:

1. **Real-DNA-likeness** — sequences within predictor's training
   distribution. Random/satellite DNA gives flat predictions → low r.
   This was the dominant lever (random 0.46 → real DNA 0.68).
2. **Composition variance** — wide per-sequence GC distribution within
   the euchromatic real-DNA manifold. Restricting variance (exp 018)
   crashed the score; widening with high-GC TSS-proximal regulatory
   elements (exp 022, 028) lifted it.
3. **TSS-proximal regulatory enrichment** — promoter-like (PLS) and
   DNase-H3K4me3 and pELS regions contribute high-GC signal AND
   regulatory information density. At ~30% of library, gain is maximal;
   beyond that, the library loses its low-GC end and drops.

### Things that did NOT help
- Synthetic motif insertion (exp 013, no gain over chr22)
- Cell-type-specific accessibility (exp 014, crashed)
- Heterochromatin / chrY / satellite repeats (exp 020, hurt)
- Splitting cCRE_all into subcategories (exp 024, neutral)
- Removing whole_genome (exp 025, dropped slightly)
- Adding dELS,CTCF-bound compound regulatory (exp 030, neutral)

### Ceiling
0.694 likely reflects the inherent agreement floor between the scorer's
two models on broad real-DNA libraries. To push higher would likely
require sequences from the predictor's actual MPRA training distribution
(the model's "easy" examples, not the manifold's interior).





