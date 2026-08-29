# Experiment 003 — 2-3 TF motifs per random background

## What I did
50,000 random 200bp sequences, each with 2-3 motifs inserted at random
non-overlapping positions. Pool: 12 motifs (K562/HepG2/SKNSH/general TFs).

## Result (eval_01)
- mean_r = **0.5114**  (baseline 0.5187, −0.007)
- k562_r = 0.9758 (was 0.9947, −0.02)
- hepg2_r = 0.5646 (was 0.5669, ~same)
- sknsh_r = -0.0061 (was -0.0054, ~same)

## Interpretation
Light motif insertion **doesn't help anything**. K562 takes a tiny hit
(probably from broken k-mer uniformity); HepG2/SKNSH are unchanged.

This is informative: it means the per-cell-type scores aren't simply
"sum activity of motifs present" — otherwise inserting strong motifs
would lift HepG2/SKNSH. Either the score is correlation-with-reference
(and our reference isn't right) or it needs much denser motif loading.

## Next
Try dense motif library (8+ motifs per 200bp sequence). If HepG2/SKNSH
lift significantly while K562 stays above 0.9, that's a win for mean.
