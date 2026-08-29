# 019_ca_h3k4me3_only — notes

## Design
50K from 79K CA-H3K4me3 cCREs (no replacement), central-200bp.
CA-H3K4me3 = chromatin-accessible region with H3K4me3 mark
(active promoter chromatin, evidenced by accessibility +
canonical promoter histone mark).

## Result vs. other single-class libraries

| eval | rand   | PLS006 | CA011  | CA-H3K4me3019 | pELS012 |
|------|--------|--------|--------|---------------|---------|
| 01   | 0.6954 | 0.5903 | 0.6775 | **0.7095**    | 0.7203  |
| 02   | 0.7848 | 0.6657 | 0.7667 | **0.8009**    | 0.8129  |
| 03   | 0.7612 | 0.6278 | 0.7579 | **0.7884**    | 0.7958  |
| 04   | 0.7494 | 0.7022 | 0.7048 | **0.7496**    | 0.7603  |
| 05   | 0.6951 | 0.5901 | 0.6777 | **0.7095**    | 0.7203  |
| 06   | 0.7853 | 0.6655 | 0.7671 | **0.8012**    | 0.8133  |
| 07   | 0.6684 | 0.5091 | 0.7386 | **0.7563**    | 0.7489  |
| 08   | 0.7841 | 0.4774 | 0.6193 | **0.6512**    | 0.6844  |
| 09   | 0.8115 | 0.7543 | 0.7638 | **0.8125**    | 0.8238  |
| 10   | 0.7564 | 0.5925 | 0.7437 | **0.7721**    | 0.7729  |
| 11   | 0.6833 | 0.5789 | 0.6668 | **0.6974**    | 0.7083  |
| 12   | 0.6553 | 0.5372 | 0.6509 | **0.6772**    | 0.6853  |
| 13   | 0.6584 | 0.4912 | 0.7441 | **0.7540**    | 0.7473  |
| 14   | 0.7851 | 0.6661 | 0.7665 | **0.8009**    | 0.8129  |

Mean: PLS 0.604, CA 0.718, **CA-H3K4me3 0.749**, pELS 0.758.

## Interpretation

**MAJOR SURPRISE: hypothesis (A) "promoter is promoter" is
FALSIFIED.** CA-H3K4me3 (active-promoter chromatin) scores
0.749, dramatically beating PLS (0.604) by **+0.145 mean**,
despite both targeting active promoter biology.

CA-H3K4me3 ranks **4th overall**, slotting between cCRE
class-balanced (0.748) and natural-prop cCRE (0.752). Beats
CA-only (0.718), CA-CTCF (0.710), and approaches the top
single-class enhancer libraries (pELS 0.758, dELS 0.756).

**Two mechanism hypotheses for the PLS / CA-H3K4me3 gap:**
1. **Annotation evidence quality.** PLS is annotated by
   TSS-proximal LOCATION (location evidence). CA-H3K4me3 is
   annotated by direct chromatin signal (DNase + histone mark
   = functional evidence). Functional evidence selects active
   elements; location evidence captures both active and silent
   promoters → noisy training labels.
2. **Element selection breadth.** PLS pool may include
   primarily housekeeping/canonical TSS regions (~47K = roughly
   1 per gene). CA-H3K4me3 pool (~79K) includes broader chromatin
   contexts: alternative TSSs, bidirectional promoters, even
   enhancer regions with H3K4me3 marks (which is increasingly
   recognized as overlapping enhancer biology).

**Eval_07 highlight:** CA-H3K4me3 = 0.756 actually BEATS pELS
(0.749) on this eval, the best single-class score on eval_07
yet. eval_07 was the "purely motif-rewarding" eval — perhaps
H3K4me3 marks select for sites with more canonical TF motifs.

**Eval_13 highlight:** CA-H3K4me3 = 0.754 also beats pELS
(0.747) on eval_13, the only "composition-helping" eval.

**High seed variance flag:** eval_01 = 0.6762 / 0.7191 / 0.7333
(range 0.057). Same pattern as CA-CTCF. Suggests the
"chromatin + secondary mark" cCRE classes have heterogeneous
samples; different 50K draws produce variable models. Possibly
the secondary mark spans multiple chromatin contexts.

## Theory update

**New principle: annotation evidence type matters more than
biological category.** Two libraries targeting the "same"
biology (active promoters) can differ by 0.145 mean depending
on whether the annotation is functional (chromatin-direct) or
positional (TSS-proximal).

This generalizes: when choosing cCREs for training, prefer
classes annotated by direct functional evidence (chromatin +
histone mark) over classes annotated by genomic location.

**Updated single-class hierarchy:**
| class       | pool   | mean   | evidence type           |
|-------------|--------|--------|-------------------------|
| pELS        | 249K   | 0.758  | DNase + chromatin marks |
| dELS        | 1.47M  | 0.756  | DNase + chromatin marks |
| CA-H3K4me3  | 79K    | 0.749  | DNase + H3K4me3         |
| CA          | 246K   | 0.718  | DNase only              |
| CA-CTCF     | 126K   | 0.710  | DNase + CTCF (narrow)   |
| TF          | 105K   | 0.683  | TF-bound only           |
| PLS         | 47K    | 0.604  | TSS-proximal (location) |

Pattern: chromatin-evidence top. Single chromatin signal
(CA = DNase only) middle. Single mark with strong narrow
binding (CTCF, TF) lower. Pure location-based (PLS) bottom.

**Implication for top-tier strategies:**
1. CA-H3K4me3 punches above its pool weight. Suggests
   chromatin-mark-confirmed active sites are intrinsically
   high-quality training data per element.
2. The PLS class label is broken-as-training-data; consider it
   as evidence that location-only annotation should be avoided.
3. If we cannot mix (010-013-015 confirmed), the best path is
   to identify the SINGLE best class, which is pELS by a
   small margin.

## Next experiment

**Exp 020: CA-TF only.** 26K pool — smallest of all SCREEN
classes; will require sampling with replacement (~2x per
element). Completes the single-class matrix. Expected to land
between TF (0.683) and CA (0.718) if "+TF binding" adds
discriminative signal to accessibility, or below TF if pool
size penalizes. Result also tests whether the high-variance
pattern of CA-CTCF / CA-H3K4me3 generalizes to all "CA-X"
sub-classes.
