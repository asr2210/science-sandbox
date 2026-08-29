# Exp 027 — Chimeric 100bp cCRE + 100bp random (within-sequence)

## Design
50K sequences, each = 100bp cCRE-centered + 100bp random hg38; side
randomized 50/50. GC=0.452; CpG=0.0152.

## Result
**eval_01 = 0.0400; mean = 0.0385; K562=0.034, HepG2=0.037, SKNSH=0.045.**
This is the **worst natural-DNA library so far** (excluding 5-gram Markov
which was negative). Regression of ~0.009 from the 013 baseline (0.049).

## Interpretation
Within-sequence chimerics actively HURT. Hypothesis: the model sees a
discontinuity at position 100 (boundary between cCRE motif context and
random flank) that doesn't appear in either eval distribution or in
training-data analogues. The boundary creates fake junction features that
don't generalize.

Alternative reading: by forcing cCRE content into a 100bp sub-region, we
lose the natural cCRE flanking context (real cCREs are embedded in their
own genomic context, not in random flank). The "synthetic cassette"
hypothesis fails — eval distribution is NOT cassette-like.

## Theory update
- **Natural genomic context matters** more than just having cCRE content.
  Slicing cCREs out of their natural flank costs ~0.009.
- The eval distribution looks like natural genomic windows, not synthetic
  cassettes.
- This narrows the design space: keep cCREs in their natural context,
  don't synthetically rearrange.

## Next step
Try the opposite: 50K random hg38 with strict CpG-island enrichment
(filter for high CpG density), to see if natural-context CpG-rich windows
lift over random sampling. CpG islands are a key promoter feature; the
013 design pulls some CpG-rich content via cCREs but not specifically.

## Time
43s wall, 13s evaluator.
