# 008 motif-inserted random

## Design
50,000 unique random seqs, each with 4 random 6-mer motifs inserted.

## Result
DISASTER. Eval_01 = -0.0141. Many evals NEGATIVE.
- eval_07 = -0.21, eval_13 = -0.18 (worst).
- eval_04/09 = 0.25 (smaller drop but still much worse than baseline 0.44).
- eval_08 went slightly up (0.13 → 0.11).

## Interpretation
Inserting "synthetic" motifs into random seqs pushes f and g in OPPOSITE
directions for most evals. This is strong evidence that:
- f and g are NOT identical functions; their disagreement is structured.
- For uniform random seqs, f and g happen to agree (mid-positive r).
- For "designed" seqs with non-natural motif patterns, f and g
  systematically anti-correlate.

So sequence "complexity" alone doesn't help; the COMPOSITION must match
the predictors' shared training distribution to align f and g.

## Strategy update
1. AVOID inserting arbitrary motifs.
2. The successful path is: diverse random + constant anchors that
   happen to sit at extremes of the f-g line.
3. Next: probe anchor-fraction sensitivity. Exp 005 had 62.5% anchor
   weight. Try lower (20%) and see if random-heavy beats anchor-heavy.
