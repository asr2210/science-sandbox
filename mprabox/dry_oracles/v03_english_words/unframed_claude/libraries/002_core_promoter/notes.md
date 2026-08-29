# 002 — Core Promoter Motif Scaffolds

## Hypothesis
Embedding canonical regulatory elements (SP1 GC-box, TATA box, Inr) at fixed
positions in each sequence will make the library more in-distribution for both
scoring models and raise their agreement (mean_r).

## Method
50,000 random scaffolds with these fixed-position inserts:
- pos 50:  SP1 / GC-box `GGGGCGGGGC`
- pos 100: TATA box `TATAAAAG`
- pos 125: Inr `TCAGTTT`
All other positions uniform random.

## Result
- eval_01 mean_r = **0.4127** (vs 0.4200 random baseline — slightly worse)
- K562: 0.5693 (−0.019), HepG2: 0.6066 (−0.012), SKNSH: 0.0621 (+0.009)
- The same eval_08 dip we saw before (0.368) — eval_08 is consistently the
  hardest set.

## Interpretation
Adding fixed motifs to every sequence DECREASED K562/HepG2 r.
This is informative: the scoring system isn't simply rewarding "regulatory-looking"
sequences. The leading theory becomes:

**Pearson r is being driven by VARIANCE in model predictions across the library,
plus AGREEMENT between two scoring methods.** Embedding the same motifs in every
sequence shifts the mean but doesn't help the variance, and may even reduce
useful variance by making sequences more uniform.

SKNSH improved slightly, suggesting low-baseline (~0.05) noise can be lifted by
adding any consistent signal — but the gains there are tiny.

## Next
Test the variance hypothesis: build a library with *spread* in a known
sequence-level property (GC content). If r climbs, variance is the lever.
