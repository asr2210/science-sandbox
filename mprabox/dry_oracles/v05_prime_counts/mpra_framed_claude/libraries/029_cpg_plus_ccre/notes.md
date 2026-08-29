# Exp 029 — Stack CpG + cCRE + random (20K + 15K + 15K)

## Design
20K random hg38 + 15K cCRE-centered + 15K CpG-enriched (top 15K of 100K
candidates by CpG count). Library GC=0.464; CpG=0.0196.

## Result
**eval_01 = 0.0490; mean = 0.0468; HepG2 = 0.0560.**

| metric | 013 (0% CpG-enr) | 029 (30% CpG-enr) | 028 (100% CpG-enr) |
|--------|------------------|-------------------|---------------------|
| eval_01 mean | 0.0488 | 0.0490 | **0.0524** |
| HepG2 | 0.0535 | 0.0560 | **0.0610** |
| GC | 0.45 | 0.46 | 0.49 |
| CpG | 0.013 | 0.020 | 0.027 |

Adding cCRE-centered + random DILUTES the CpG signal. 029 is barely
above 013 baseline — the CpG-enriched 30% subset alone doesn't carry the
lift seen in 028.

## Interpretation
- The 028 lift is **DOSE-DEPENDENT** on CpG content. Diluting from 100%
  CpG-top to 30% CpG-top loses most of the gain.
- This is consistent with two readings:
  (a) The lift is from the CpG-rich windows themselves (their TF motifs,
      GC composition, promoter content). 30% isn't enough mass to dominate.
  (b) Adding random/cCRE windows pulls GC and CpG back toward genomic
      mean — the lift required the library-level composition shift, not
      just inclusion of CpG-rich examples.
- Either way: **don't dilute the CpG axis** if you want the lift.

## Theory update
- CpG enrichment lifts, but the lift is monotone in CpG-fraction.
- 028 design (pure top-50K) is robust; 029 (mixed) regresses.
- Final question for 030: can we push CpG even harder?

## Next step
Exp 030: top 50K of 500K candidates (top 10%), the most CpG-extreme
filter. If 030 ≥ 028, CpG axis hasn't saturated. If 030 < 028, 028 was
near-optimal.

## Time
58s wall, 27s evaluator.
