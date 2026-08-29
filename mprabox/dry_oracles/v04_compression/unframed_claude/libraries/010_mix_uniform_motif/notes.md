# Experiment 010 — 50/50 mix of uniform + motif-loaded

## Result
eval_01: 0.305. WORSE than both pure uniform (0.331) and pure motif-loaded (0.328).
eval_07: 0.398 (vs 0.447 in pure motif-loaded) — also worse.

## Interpretation
Mixing two distributions HURTS. The library becomes bimodal in feature space (some seqs have a motif boost, some don't), and that heterogeneity decorrelates whatever the scorer is correlating. This rejects the "activity-space variance" hypothesis.

T6 confirmed: scorer rewards HOMOGENEOUS libraries close to its training distribution. Uniform random is the homogeneous winner. Mixed libraries cluster and decorrelate.

## Theory T7 (working theory)
The scorer was likely trained on synthetic uniform-random oligo MPRA libraries (e.g., Tewhey/Inoue style — random 200bp lentiMPRA). The Pearson r is computed between two model predictions over our library. Random uniform is exactly the training distribution → models agree most → highest r.

To exceed 0.331, would need: subtle homogeneous perturbation that still looks like the training distribution but adds a tiny bit of consistent signal. Hard.

## Next
Continue exploring homogeneous diverse-motif strategies. Exp 011 = 32-motif pool to test if more diversity = closer to "natural random" = ≥ 0.328.
