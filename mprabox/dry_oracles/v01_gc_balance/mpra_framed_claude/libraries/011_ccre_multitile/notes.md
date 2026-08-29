# 011_ccre_multitile

## Setup
25k unique cCREs × 2 windows each (offsets −50, +50) = 50k sequences.
Stratification quotas halved from exp 002. Tests if multi-view per element
beats more unique elements.

## Result vs exp 002
- eval_01: 0.6916 vs 0.6921 (−0.001, identical)
- eval_04: 0.5941 vs 0.5977 (−0.004, identical)
- eval_07: 0.7570 vs 0.7562 (+0.001)
- eval_08: 0.1225 vs 0.1248 (−0.002, in noise)
- eval_10: 0.6674 vs 0.6673 (~tied)

## Interpretation
Halving unique elements but doubling windows = no change. Two near-identical
views (offsets ±50bp) of the same element don't add training signal beyond
what one centered view provides. Half as many elements gives the same eval_01.

Hypothesis ruled out: multi-view per element is NOT what limits the model.
The cCRE ceiling is about the *information content per element*, not the
number of views per element.

## Takeaway
This is the 5th library at ~0.69 eval_01 (002, 005, 006, 010, 011). The
ceiling is robust. Need to break out of the cCRE distribution entirely or
find an entirely orthogonal signal. Next: try real measured MPRA training
data (Malinois dataset, 798k oligos in the actual target cell types).
