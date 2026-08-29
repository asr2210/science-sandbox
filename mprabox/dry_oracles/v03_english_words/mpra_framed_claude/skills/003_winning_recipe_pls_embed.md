# Skill: PLS-fragment-embedded random library (winning recipe so far)

## Recipe (exp 012)
1. Generate 50K uniform random 200bp sequences.
2. For each sequence, pick one random 25bp fragment from any ENCODE V4 PLS (promoter-like cCRE; ~47K available).
   - Sample a PLS, take a 200bp window centered on its midpoint, then take a random 25bp substring.
3. Embed each fragment at a random position in its corresponding random sequence.
4. Submit to prepare.py.

## Why this beats pure random
- 175/200 bases per sequence are uniform random → preserves random's K562/HepG2 advantage (avg GC ≈ 0.498-0.500).
- 25bp PLS fragment carries CORE PROMOTER motifs (Inr, TATA, NFY, SP1) which drive activity in ALMOST ALL cell types → lifts SK-N-SH r from 0.045 → 0.065 and gives K562/HepG2 a tiny lift too.
- PLS specifically (not mixed cCREs): promoters are more universally active than distal enhancers (dELS), so they teach the model UNIVERSAL grammar that generalizes across cell types.

## Numbers (exp 012)
- eval_01 mean_r: **0.4248** (vs pure random 0.4192, Δ+0.0056)
- K562_r: 0.591 (slightly above random 0.590)
- HepG2_r: 0.619 (slightly below random 0.623)
- SK-N-SH_r: 0.065 (+44% over random 0.045)

## What was tried that didn't beat random
| Variant | Δ vs random | Notes |
|---|---|---|
| Pure random (baseline) | 0 | eval_01 = 0.4192 |
| Planted consensus motifs (002) | -0.007 | Short consensuses too weak |
| Real cCREs full (003) | -0.025 | Composition shift hurts K562/HepG2 |
| 50/50 mix random+cCRE (004) | -0.024 | Mixing hurts |
| 90/10 mix (005) | -0.012 | Small mix still hurts |
| Shuffled cCRE (006) | -0.051 | Wrong composition + no motifs |
| Variable GC random (007) | -0.049 | Eval is composition-narrow at 50% GC |
| 1x25bp mixed cCRE embed (008) | -0.002 | Closest mixed but still slight loss |
| 1x15bp embed (009) | -0.002 | Smaller fragment, smaller lift |
| 1x50bp embed (010) | -0.008 | Too big, more disruption |
| 3x10bp distributed embed (011) | -0.001 | Distributed preserves comp, smaller lift |

## What PLS gives that mixed doesn't
PLS (47K elements) is the SMALLEST and most enriched class in the registry. dELS (1.47M) is the largest. By restricting to PLS, the fragments have higher density of:
- Core promoter motifs (universally active)
- CpG content (promoter-associated)
- High MPRA activity baseline

## Open directions to try
- 013: 3x10bp distributed PLS-only (combine distribution + PLS) — possibly better
- 014: Active learning style — multiple seeds, identify which fragments add most value
- 015: PLS fragments centered on TSS (more enriched)
- 016: Vary fragment length within PLS (mixed 15/20/25/30bp)
