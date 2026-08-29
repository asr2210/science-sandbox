# 003 — ENCODE v4 cCREs, 200bp centered, stratified by type

## Design
50,000 sequences, 6,250 from each of the 8 ENCODE cCRE annotation classes:
dELS, pELS, CA, CA-CTCF, TF, CA-H3K4me3, PLS, CA-TF. 200bp centered on each cCRE midpoint, drawn from hg38 autosomes only, rejecting any with 'N'.

## Result
- eval_01 mean_r = **0.4963** (vs 0.5177 random uniform, 0.4861 random genomic)
- K562 r ≈ 0.928 (between 0.99 and 0.89 — narrower composition than uniform, broader than pure-random-genomic because of stratification)
- HepG2 r ≈ 0.562 (unchanged from baselines)
- SK-N-SH r ≈ 0 (STILL zero — even concentrated regulatory regions failed to teach the model anything SK-N-SH-related)

## Reading
- cCRE enrichment did NOT unlock SK-N-SH. The hypothesis that "real regulatory sequences contain motifs that lift SK-N-SH" is contradicted.
- Either (a) SK-N-SH activity in the eval sets requires motifs/contexts not abundant in cCREs, (b) the model has limited capacity to learn SK-N-SH-specific features from this dataset, or (c) SK-N-SH activity in the eval simulator is dominated by noise/unpredictable factors.
- Composition coverage drove the rank order: random uniform (broadest comp) > stratified cCREs > random genomic. Composition diversity is a stronger lever than motif content.

## Big-picture implication
The "natural sequences are more informative" intuition is wrong for this benchmark. So far, the simpler the sequences (closest to random uniform), the better mean_r. The next test should isolate **composition** as the primary lever: explicitly vary per-sequence composition outside what binomial random gives, to see if K562 can be pushed further or if it's saturated.
