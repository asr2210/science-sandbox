# 010_four_axis_gradient

## Setup
4 independent per-char gradients, same direction. Char 0: 2→98 (+96), char 1:
100→10 (-90), char 2: 78→12 (-66), char 3: 20→80 (+60). Sum 200 per row.

## Results
eval_01: 0.5871 (009 was 0.6010, -0.014)
eval_07: 0.6496 (009 was 0.6685, -0.019)
eval_04/09: 0.4740 (009 was 0.5091, -0.035)
eval_08: 0.1271

## Interpretation
Splitting per-pair characters HURT. The (0+3) vs (1+2) PAIRED axis is the
real signal direction; chars 0 and 3 act symmetrically as do chars 1 and 2.
By making chars 0/3 grow at different rates, we reduced the per-pair
gradient sharpness → r dropped.

## Implication
Don't sub-divide the (0,3) and (1,2) pairs. Treat them as the same chemical
class. Focus optimization energy on other levers.
