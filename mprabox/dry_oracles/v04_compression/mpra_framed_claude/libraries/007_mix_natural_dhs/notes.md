# 007_mix_natural_dhs — notes

## Design
25K natural genomic + 25K DHS summit-centered 200bp windows. DHS from
Meuleman 2020 index (3.6M sites across 438 biosamples), sampled uniformly
at random.

## Result (29s training, 61s wall)
- eval_01: 0.4898 (vs 0.4937 with cCRE mix; essentially tied)
- Pattern almost identical to 004 (natural+cCRE)
- eval_08 = 0.0955 (slightly higher than 004's 0.0906, but in noise)

## Interpretation
DHS index covers many more cell types than cCRE focus, but the
information added is essentially the same. The boost over pure natural is
similar regardless of whether the "regulatory enrichment" half comes from
cCRE or DHS.

This is mildly disappointing for the cross-cell-type hypothesis: I expected
DHS (multi-cell-type) to outperform cCRE (more focused) for cross-cell-type
generalization specifically. It doesn't.

## Implication
The marginal value of "regulatory elements" beyond a natural-DNA baseline
saturates quickly. Adding more sources of regulatory elements has limited
return.

What does add value is **diversity of activity range** (positive +
negative examples). Both cCRE and DHS provide regulatory positives;
natural DNA provides composition negatives. The combination wins.

## Next test
Either: (a) try 3-way mix (test if more sources help), or (b) try a new
axis like augmentation or scrambled controls. The 3-way mix is the
cheaper test.
