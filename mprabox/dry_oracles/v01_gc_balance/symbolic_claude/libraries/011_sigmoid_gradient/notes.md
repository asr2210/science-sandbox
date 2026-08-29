# 011_sigmoid_gradient

## Setup
Sigmoid composition gradient with k=10. Endpoints (2,98,98,2) ↔ (98,2,2,98)
same as 009 but rows concentrated near extremes (few in middle).

## Results
eval_01: 0.5986 (009 was 0.6010, within noise — basically same)
eval_07: 0.6646 (009: 0.6685, slightly down)

## Interpretation
Target is approximately LINEAR in row index. Sigmoid bunching at extremes
doesn't help. Likely target = approximately linear (continuous activity).

## Implication
Composition gradient axis is fully saturated. r ~ 0.60 is the cap for this
single axis. To break through, need to add an ORTHOGONAL row-correlated
signal that the model picks up on.
