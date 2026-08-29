# 011 — dELS distal enhancers + random genomic null

## Method
25k active: random dELS (distal enhancer-like) cCREs, 200bp midpoint-centered.
25k null: random 200bp genomic windows from autosomes.

## Results (eval_01)
mean_r=-0.0010, K562=-0.0058, HepG2=+0.0059, SKNSH=-0.0032

## Lessons
- Even DISTAL enhancers (exclude promoters) gave NEGATIVE K562 r.
- HepG2 stayed positive (HepG2 model likes real-looking sequences).
- SKNSH neutral.

## Updated theory
The scorer is correlating two predictors. For SYNTHETIC dense-motif
libraries, both predictors AGREE on which sequences are active → r > 0.
For REAL biological sequences, the two predictors DISAGREE (different
models capture different facets of biology) → r ≈ 0 or negative.

Implication: maximum r comes from sequences where the two models can
**unambiguously agree**. Strong, dense, clean motif libraries fit that.
Real genomic complexity hurts because models disagree on the details.

## Results trend so far (eval_01 mean_r)
| exp | mean_r | best K562 | comment |
|-----|--------|-----------|---------|
| 001 random         | -0.003 | 0.001 | noise floor |
| 002 GC sweep       |  0.003 | 0.002 | tiny lift |
| 003 mixed motifs+null | 0.001 | 0.014 | K562 lift, others offset |
| 004 4-bank         |  0.000 | 0.002 | dilution killed signal |
| 005 K562 motifs    |  0.004 | 0.008 | best synthetic-motif mean |
| 006 HepG2 motifs   | -0.003 | -0.004 | hurt other cells |
| 007 SKNSH motifs   |  0.003 | 0.003 | all-three positive |
| 008 saturated univ |  0.004 | 0.005 | similar to 005 |
| 009 cCRE vs shuf   |  0.002 | -0.002 | real OK but not great |
| 010 cell-DHS top   | -0.004 | -0.012 | K562 NEGATIVE |
| 011 dELS+genomic   | -0.001 | -0.006 | K562 NEGATIVE |

## Next
Exp 012: doubly-down on the WORKS direction. Universal-motif library
with VERY DENSE tiling of 4-5 strongest universal motifs (AP-1, SP1,
NF-Y, CREB, E-box), 15-20 motifs per sequence, matched-GC null. Should
beat exp 005 / 008 if my "two-model agreement" theory is right.
