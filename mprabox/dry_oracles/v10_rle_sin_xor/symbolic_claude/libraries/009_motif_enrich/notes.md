# Experiment 009: Motif Enrichment

## Setup
- All 50000 random sequences with "01230123" inserted twice per sequence
- Motif is balanced (2 of each base)

## Results
- eval_01: mean=0.5184, a=0.9936, b=0.5664, c=-0.0049
- vs random baseline: mean=0.5174, a=0.9945, b=0.5643, c=-0.0065
- Tiny gain in b (+0.002), tiny loss in a, c unchanged
- All within noise

## Interpretation
- Adding balanced motifs doesn't significantly help any condition
- c is robust to motif content — needs something else (or is fundamentally near 0)
