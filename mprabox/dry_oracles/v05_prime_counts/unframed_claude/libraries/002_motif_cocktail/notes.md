# Experiment 002 — Motif cocktail

## Hypothesis
If the oracle is a sequence-to-activity predictor, inserting ~10
strong canonical regulatory motifs (SP1, NFY, TATA, CRE, AP-1,
E-box, GATA, HNF, NeuroD…) per 200bp sequence should beat random.

## Method
Per sequence: uniform random background. Insert 10 non-overlapping
motifs at random positions and 50% reverse complement. Motifs drawn
uniformly from a list of 18 canonical activators.

## Results
- eval_01: 0.0386 (random was 0.0420)  → slightly DOWN
- eval_08: 0.1083 (random was 0.1237)  → DOWN
- Average across 14 sets: ~0.044 (random was ~0.046) → slightly DOWN

## Interpretation
Insertion of canonical TF motifs did NOT increase scores; if anything,
slightly decreased them. This is a meaningful negative result.

Possibilities:
- The oracle ignores TF motifs at this density / orientation.
- Inserting motifs reduces diversity → if oracle rewards diversity,
  this hurts.
- 200bp may be too short to express grammar the oracle wants.
- The motifs I chose may not be the active ones.

## Theory update
T1 (mean predicted activity rewards regulatory motifs) is weakened.
We need a sharper test of WHAT the oracle rewards.

## Next
Run a "zero diversity" experiment — 50K identical copies of one
densely-packed motif sequence. This separates:
  - If per-seq metric: score should be HIGH (this seq has many motifs)
  - If library-level metric (diversity): score should be near zero
