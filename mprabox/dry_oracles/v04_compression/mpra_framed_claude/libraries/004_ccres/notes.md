# 004_ccres

50,000 cCREs from ENCODE SCREEN catalog (V3, GRCh38), restricted to
chrs {1, 11, 19, 20, 21, 22}. 200bp centered on cCRE midpoint.

## Result
mean across 14 evals: 0.396 (worse than 002 0.524, worse than 003 0.463)
eval_01: 0.386 (vs 002: 0.497)

## Per-eval delta vs 002 (genomic random windows)
- eval_01: -0.110
- eval_03: -0.124
- eval_04: +0.039 !  (only eval where cCRE helps over random genomic)
- eval_06: -0.129
- eval_07: -0.258  (HUGE drop)
- eval_08: -0.011
- eval_10: -0.079
- eval_13: -0.204

## Surprise
Curated regulatory elements are SUBSTANTIALLY WORSE than random
genomic windows for almost every eval set. Eval_07 dropped from
0.599 to 0.341.

The only eval where cCREs help is eval_04. Notable: eval_04 saw the
biggest lift from 001→002 also. So eval_04 may care about regulatory
elements specifically.

## Interpretation
Diversity > curation. A model trained on cCREs only sees regulatory
sequences with a particular composition and motif density. When
evaluated on the broader test distribution (probably mostly non-cCRE
sequences from the genome), it doesn't know what those look like and
fails.

Random genomic windows include the full diversity: regulatory regions
(by chance — they're ~5-10% of the genome), repeats, introns,
intergenic, UTRs, CDS. The model learns the FULL sequence-to-activity
mapping across this diversity and generalizes.

## Implication
For a held-out eval set whose composition we don't know, **train on
the broadest sequence distribution possible**, not a curated subset.
Curation hurts unless the eval is also curated to match.
