# Score is Pearson r

## Discovery
Submitting all identical "0"*200 sequences triggered:
`eval/harness.py:111: ConstantInputWarning: An input array is constant;
the correlation coefficient is not defined.`

All eval scores were NaN. This confirms **mean_r = Pearson correlation
coefficient r**, averaged or aggregated somehow over the library.

## Implications for generation
- NEVER submit truly constant inputs (will get NaN).
- Each string should have intra-string variation.
- Likely needs cross-string variation too (TBD).
- Score is calibrated: 0.5 ≈ random; 1.0 = perfect correlation; <0 = anti.
- To improve score: produce sequences that the underlying model deems
  "high activity" (assuming MPRA context).

## Context
Parent dir is `MPRAgent_adversarial` → strong hint this is MPRA (Massively
Parallel Reporter Assay) DNA sequence design. Alphabet {0,1,2,3} likely =
nucleotides {A,C,G,T}. Mapping unknown.
