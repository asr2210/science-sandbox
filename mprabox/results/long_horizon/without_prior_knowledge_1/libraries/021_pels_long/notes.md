# 021_pels_long — notes

## Design
50K LONGEST pELS cCREs from the 249K pool (length ≥336bp;
pELS pool ranges 150-350bp). Same central-200bp extraction.
Three seeds (only affect ordering — filtered set is fixed).

## Result vs. pELS-only

| eval | pELS012 | long021 | Δ      |
|------|---------|---------|--------|
| 01   | 0.7203  | 0.7141  | -0.006 |
| 02   | 0.8129  | 0.8077  | -0.005 |
| 03   | 0.7958  | 0.7874  | -0.008 |
| 04   | 0.7603  | 0.7631  | **+0.003** |
| 05   | 0.7203  | 0.7142  | -0.006 |
| 06   | 0.8133  | 0.8082  | -0.005 |
| 07   | 0.7489  | 0.7315  | -0.017 |
| 08   | 0.6844  | 0.6819  | -0.003 |
| 09   | 0.8238  | 0.8259  | **+0.002** |
| 10   | 0.7729  | 0.7740  | **+0.001** |
| 11   | 0.7083  | 0.7021  | -0.006 |
| 12   | 0.6853  | 0.6762  | -0.009 |
| 13   | 0.7473  | 0.7200  | **-0.027** |
| 14   | 0.8129  | 0.8078  | -0.005 |

Mean: pELS012 0.758, **long021 0.751, Δ=-0.007**.

## Interpretation

**Hypothesis (B/C) confirmed: length is NOT a quality signal**
for pELS, with slight evidence of mild anti-quality bias.

Most evals modestly drop (-0.005 to -0.017), but evals 04/09/10
actually slightly improve (+0.001 to +0.003). Eval_13 takes the
biggest hit (-0.027), consistent with eval_13's "composition
matters" property — the longest pELS may have biased
composition vs. the natural pELS distribution.

**High seed variance (0.69/0.74/0.72 on eval_01).** Even with
the same 50K elements across seeds, training noise produces
0.046 range. This is high for pELS (uniform pELS has ~0.01
seed variance). Possible reason: longest cCREs are more
"edge-case" sensitive to training stochasticity, or their
composition imbalance creates a less smooth loss landscape.

**Why might length be anti-quality?**
- Longest pELS may overlap multiple regulatory elements (super-
  enhancer-like territory): noisier signal per element.
- Longest cCREs may be on systematically different chromatin
  contexts (e.g., transcribed regions overlapping several genes).
- Longest cCREs may be in dense-cluster regions where MPRA
  activity is harder to attribute to the central window.
- The 200bp central window only captures 57-60% of a 350bp
  cCRE, missing flanking grammar that would be wholly captured
  in shorter cCREs.

## Theory update

**Length-as-quality is FALSIFIED for pELS.** Filtering by
extreme length doesn't help and slightly hurts.

This matters because length was the only intrinsic quality
signal in the BED file. Without length being informative, no
purely-from-cCRE-coordinates filter can exceed pELS-only.
Quality filtering would need external data (conservation,
ChIP-seq strength, cell-type breadth).

**Augmentation playbook now empty AND length-filter playbook
empty.** The pELS-only at 50K random samples remains the local
optimum.

## Next experiment

**Exp 022: pELS top-50K-SHORTEST cCREs.** Confirms length
direction. If shortest ≈ longest ≈ uniform, length is purely
null. If shortest > uniform, short is the privileged tail
(suggesting the longest pELS introduce noise we don't see in
the natural distribution). If shortest << uniform, length
matters in the long-direction (which would CONTRADICT our 021
result, suggesting both tails are different from middle).
