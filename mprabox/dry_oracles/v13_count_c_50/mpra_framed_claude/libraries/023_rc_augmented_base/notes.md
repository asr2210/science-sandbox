# Experiment 023 — RC augmentation in the base

## Result vs 013
| eval | 013 | 023 (RC base) | Δ | within noise? |
|------|-----|---------------|---|---------------|
| 01 ★ | 0.5765 | 0.5757 | -0.001 | yes |
| 04 | 0.5774 | 0.5781 | +0.001 | yes |
| 07 | 0.6037 | 0.6024 | -0.001 | yes |
| 08 | 0.1730 | 0.1817 | +0.009 | real (~8×noise) |
| 10 | 0.5087 | 0.5081 | -0.001 | yes |
| 13 | 0.5865 | 0.5856 | -0.001 | yes |
| mean8 | 0.5705 | 0.5710 | +0.001 | tiny |

## Verdict: RC augmentation is essentially neutral
On 5/6 unique evals, RC augmentation is within seed noise. eval_08 shows
a small real gain (+0.009), but eval_01 is unchanged.

## Why
Two factors:
1. The model likely learns RC-invariance from the cCRE supplement and the
   diversity of natural sequences already. Adding RC pairs explicitly
   doesn't add new information at the model level.
2. RC of a sequence has the SAME GC content but DIFFERENT dinucleotide
   composition (AC → GT, etc.). This subtly enriches the dinuc histogram
   of the base, which is why eval_08 (composition-sensitive) gains.

So RC augmentation provides a tiny dinucleotide-level enrichment but
nothing motif-grammar-wise. Composition ceiling still holds.

## Implication
Cannot break the 0.5765 ceiling via simple symmetry hints. Must directly
manipulate the composition signal further. Next: dinucleotide matching
(CpG specifically) — the suspected remaining cCRE-specific feature.
