# 010 diverse random, no anchors

## Design
4 diverse random strata × 12500 each, no constant anchors:
uniform, GC-rich, AT-rich, no-homopolymer.

## Result
eval_01 = 0.5579. Lower than exp 009 (0.5689, with 20% anchors) by 0.011.
Higher than exp 003 pure uniform random (0.5299) by 0.028.

## Conclusion
Both contribute independently:
- Random-stratum diversity gives ~+0.028 over uniform random.
- Adding 20% letter anchors on top gives an extra ~+0.011.

For best score, combine BOTH: diverse random + modest anchor fraction.

## Next plan
Try even MORE diverse compositional strata + anchors.
