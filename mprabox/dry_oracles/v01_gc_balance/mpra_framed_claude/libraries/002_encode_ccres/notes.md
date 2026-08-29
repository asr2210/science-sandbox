# 002_encode_ccres

## Setup
50,000 200bp windows centered on ENCODE GRCh38 cCREs (release v4, all biosamples).
Stratified across cCRE types:
- PLS:        6,000  (proximal promoter-like)
- pELS:       7,000  (proximal enhancer-like)
- dELS:      10,000  (distal enhancer-like)
- TF:         6,000  (TF-bound non-DNase)
- CA:         6,000  (chromatin-accessible only)
- CA-CTCF:    6,000
- CA-H3K4me3: 5,000
- CA-TF:      4,000
Sampled with seed=2 from chr1..22, X, Y. N-containing windows skipped.

## Result
- eval_01=0.6921 (+0.18 vs random 0.5131)
- eval_07=0.7562 (+0.18), eval_13=0.7466 (+0.19), eval_10=0.6673 (+0.15)
- eval_04/09=0.5977 (+0.18)
- **eval_08=0.1248 (−0.04, WORSE than random)**
- Mean across 14 evals: ~0.62 (vs random ~0.49)

## Interpretation
Real regulatory elements dramatically improve every "normal" eval. But eval_08
gets *worse* — moving away from random sequence composition hurts whatever
eval_08 measures. Hypotheses for eval_08:
1. It tests on sequences with uniform-random composition (e.g., shuffled), so a
   cCRE-trained model is out-of-distribution there.
2. It tests on synthetic designed sequences with specific motif compositions
   not well represented in cCRE distribution.
3. It tests on a narrow target (e.g., very low expression / baseline) where the
   cCRE-trained model is overconfident.

Either way, the data say: cCREs are the strong signal for ~13/14 evals, but
something orthogonal is needed for eval_08. Mixing in random sequences (or
synthetic) should help.

SKNSH consistently lowest, gap to HepG2/K562 widens with cCREs — possibly
because cCREs are over-enriched for K562/HepG2-active elements vs neural ones.
