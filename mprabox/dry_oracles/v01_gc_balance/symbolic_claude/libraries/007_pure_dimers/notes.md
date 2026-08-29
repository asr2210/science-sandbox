# 007 pure dimer-repeats

## Design
16 distinct dimer-repeat templates × 3125 copies = 50,000.

## Result
mean_r = NaN (because SKNSH is NaN for every eval).
K562: 0.026 — 0.112 across evals (tiny but non-zero).
HepG2: 0.015 — 0.072.
SKNSH: NaN for all evals.

## Interpretation
1. SKNSH's f or g is constant across the 16 dimer-repeat templates →
   the SKNSH model is INVARIANT to dimer composition. Big surprise.
2. K562 and HepG2 see SOMETHING differentiating dimer-repeats but very
   weakly correlated (r < 0.12).
3. Dimer-repeat anchors do NOT form a coherent line in (f, g) space.

## Theory v4 (refined)
The 3 cell-line predictors have very different sensitivities:
- SKNSH: depends on higher-order structure (k≥3?). Constant on dimers.
- K562, HepG2: weakly sensitive to dimer composition.
On varied seqs all three give strong signals.

So:
- f and g are likely shared "real DNA" predictors (e.g., CNNs).
- The predictors saturate / are invariant for "trivial" inputs (single
  letters, dimers).
- For interesting score, we need seqs with sufficient k-mer COMPLEXITY
  (k≥3 motifs, varied content).

## Strategy update
- Pure repetitive seqs are useless.
- Best path = diverse "natural-looking" random seqs.
- Anchor-style additions (in exp 005) helped only because the anchors
  contributed extreme f values while the bulk-random seqs contributed
  g variance.
