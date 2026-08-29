# 017_motif_rich_natural — notes

## Design
20K natural windows curated by JASPAR motif score (top 20K from 100K
candidates, scored by sum of max log-odds for 19 diverse TF PWMs) +
15K cCRE off-center + 10K DHS + 5K mouse.

## Result
- eval_01 = 0.4866 (vs exp 011 = 0.5012, Δ = -0.0146)
- This is **outside noise** (>3σ below plateau). Real regression.
- eval_07/13 also down ~0.03 from 011
- Time: 30s

## Interpretation
Curating natural windows for motif richness actively HURTS. The natural
20K component is doing the job of representing the diversity of genomic
context — silencers, neutral background, intergenic spacers, repeat
regions. Curating to "motif-rich" creates a biased subset enriched for
the same 19 TFs the scorer used, which:
1. Reduces sequence diversity (over-represents one TF family)
2. Overlaps with what cCRE/DHS already provide
3. Loses the "neutral baseline" function of random natural

## Implication
**The natural 20K must remain random/unbiased.** Diversity of context,
not motif density, is its job. Regulatory atlases supply density.
Curation criteria within natural that match cCRE's bias are net-harmful.

## Lesson for future curation
If I want a curated natural component, the criterion must be ORTHOGONAL
to what cCRE captures — e.g., conservation (functional importance with
selection criterion outside chromatin), or anti-correlation with cCRE
(deserts / regulatory-poor regions as cleaner negatives).

## Next test
Conserved sequences (phastCons elements). Conservation is an orthogonal
selection criterion (purifying selection, multi-species sequence
divergence) vs chromatin accessibility (one-cell-type measurement).
