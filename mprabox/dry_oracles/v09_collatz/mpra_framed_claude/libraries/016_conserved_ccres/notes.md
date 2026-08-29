# 016_conserved_ccres

## Design
Top 5,000 cCREs by phastCons-conserved-base count within their
200bp core × 10 random-offset tiles = 50K. Conservation source =
phastConsElements100way (UCSC, 100-vertebrate alignment).

Top-scored cCREs had nearly all 200 bases inside conserved
elements (top score 200, 5000th score 198) — these are the most
deeply selection-preserved cCREs.

## Hypothesis (T11)
Conservation-filtered cCREs concentrate functional regulatory bases.
A model trained on these should learn higher-information-per-base
grammar that generalizes across cell types.

## Result vs 014 (5K x 10 same allocation)
                eval_01  K562    HepG2   SKNSH
014 5K x 10:    0.3181   0.144   0.188   0.623
016 conserved:  0.3057   0.139   0.174   0.604

DOWN by 0.012. SKNSH took the biggest hit (-0.019).

## Interpretation — top-conservation falls into the same trap
Same lesson as 009 (top DHS) and 011 (top STARR): top-filtering
along any axis NARROWS the training distribution. Deeply
conserved cCREs are enriched for:
- Coding-region-proximal regulatory elements (5'UTRs, splice
  regions, miRNA targets)
- Universally-essential promoters
- Ultra-conserved noncoding elements (often developmental, lineage-
  specific)

These are LESS cell-type-variable than typical enhancers. SKNSH
suffers most because SKNSH's hardest evals likely require breadth
across the full enhancer landscape, not the conservation tip.

Filtering rule confirmed across THREE assays: any filter that
selects the top-N by a single quality score (signal, function,
conservation) collapses variance and hurts cross-cell-type
prediction. The lesson generalizes: **breadth beats peak quality
within the natural-genomic family.**

## Falsified hypotheses (running list)
- Cell-type-bias for K562 (003): refuted
- Motif/composition separation (004): refuted
- Synthetic motif sufficiency (006): refuted
- Promoter universality (007): refuted
- Compositional spread additivity (008): refuted
- Peak signal strength (009): refuted
- Differential activity (010): refuted
- STARR-seq MPRA-likeness (011): refuted
- RC strand augmentation (012): null
- Paired wt/mut training (013): refuted
- Intra-region density at saturation (014): null
- Motif-amplified additive (015): null
- Conservation top-filter (016): refuted

## Confirmed findings
1. Saturation at ~5K cCREs × 5 tiles (confirmed 3 ways: 005/012/014)
2. Per-cell-type ceilings: K562 ~0.146, HepG2 ~0.19, SKNSH ~0.625
3. Top-anything filtering collapses variance, hurts
4. Distributionally close fillers add noise, slightly hurt
5. eval_08 is anti-cCRE (likes random/synthetic); rest are
   cCRE-positive
6. eval_07 / eval_13 are most grammar-sensitive

## Next
Experiment 017: cCRE CLASS-BALANCED design. 1K cCREs from EACH of
{PLS, pELS, dELS, CTCF-only, DNase-H3K4me3} × 10 tiles each = 50K.
Tests "regulatory class diversity" axis: dELS dominates the cCRE
file (74% of cCREs), so random cCRE sampling is heavily
distal-enhancer-biased. Class-balanced may give the model better
coverage of regulatory archetypes.

Generalization justification: cCRE classes are 5 different
regulatory archetypes. A model trained on equal representation of
each learns the full archetypal vocabulary, which transfers to
any cell type's regulatory landscape.
