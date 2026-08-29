# 004 — DIAGNOSTIC: single sequence repeated 50k times

## What
1 random Gosai sequence × 50,000 copies.

## Result
All scores: **NaN**. With warning:
`ConstantInputWarning: An input array is constant; the correlation coefficient is not defined.`
From `eval/harness.py:111`.

## Critical findings
1. **Pearson r is computed PER SEQUENCE** between two length-50,000 vectors.
2. prepare.py constructs two vectors from our sequences and correlates them.
3. With all sequences identical, both vectors are constant → r undefined.
4. **Variance in our library is REQUIRED** for r to be defined.

## Theory update
prepare.py computes f(seq_i) and g(seq_i) per sequence, where f and g are
two different scorers (oracle + target / model A + model B). r is the
correlation across our 50k positions. To maximize r:
- Sequences where f and g AGREE strongly contribute
- Sequences where f and g DISAGREE pull r down

For random seqs: r=0.117 because oracle outputs and target outputs weakly agree
on noise. For real biological sequences: r=0.144 because both signals more
consistently predict activity from sequence content.

## Next steps
- Hypothesis: scorer pair is (Malinois, ground-truth-MPRA) where ground-truth
  comes from the Gosai dataset. Sequences from the dataset have both available.
- Optimize: select sequences where predicted activity ≈ measured activity
  (high Malinois accuracy = high r contribution).
- But: we'd need Malinois to compute this. Try installing torch or finding
  cached predictions.
