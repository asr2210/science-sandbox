# 004_mix_natural_ccre — notes

## Design
50/50 mix: 25K natural genomic windows + 25K cCRE-centered.

## Result (53s training, 87s wall)
- eval_01 = 0.4937 (vs 0.4798 pure natural, +0.014; vs 0.3446 pure cCRE, +0.149)
- Mix beats both pure libraries on every eval **except eval_08** (still ~0.09)
- Gain over pure natural is small (~3% relative) but consistent
- Gain over pure cCRE is large

## Implication
- cCRE adds *some* signal when balanced with broad natural coverage.
- Diversity > purity for library design.
- The natural-DNA backbone provides activity-range coverage; cCRE
  enriches the motif content seen within that backbone.
- eval_08 is unaffected by either — it tests something else entirely.

## Saturation question
Mix gain over natural is only ~3%. Either:
- The marginal value of cCRE is small once natural is present
- The 50/50 ratio is wrong; 90/10 or 75/25 might be better
- Other diversity sources (motif synthetic, scrambled controls) would
  add more

Next: test if pure synthetic motif library can complement natural
similarly or in a different direction (especially for eval_08).
