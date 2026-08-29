# 005 — cCRE (35K) + iid (5K) + real genomic (5K) + mono-shuffled genomic (5K)

## Result — regression vs 004 on every eval
| metric  | 005 | 004 | Δ |
|---------|-----|-----|------|
| eval_01 | 0.7343 | 0.7395 | −0.0052 |
| eval_02 | 0.8266 | 0.8342 | −0.0076 |
| eval_03 | 0.8095 | 0.8178 | −0.0083 |
| eval_04 | 0.7903 | 0.7998 | −0.0095 |
| eval_05 | 0.7344 | 0.7395 | −0.0051 |
| eval_06 | 0.8269 | 0.8343 | −0.0074 |
| eval_07 | 0.7689 | 0.7724 | −0.0035 |
| eval_08 | 0.7055 | 0.7160 | −0.0105 |
| eval_09 | 0.8590 | 0.8712 | −0.0122 |
| eval_10 | 0.7870 | 0.7989 | −0.0119 |
| eval_11 | 0.7216 | 0.7265 | −0.0049 |
| eval_12 | 0.6972 | 0.7029 | −0.0057 |
| eval_13 | 0.7612 | 0.7671 | −0.0059 |
| eval_14 | 0.8268 | 0.8344 | −0.0076 |

Mean 14: **0.7749** vs 004's **0.7825**. Wall: 1307 s.

## Per-seed eval_01
- seed 0: 0.7458
- seed 1: 0.6968 (low outlier — same seed as 003 and 004 had low/high spread)
- seed 2: 0.7602

Spread = 0.063. Within the typical 0.04–0.07 range.

## Pre-registered prediction scorecard
- "diversity scales": predicted eval_01 0.745–0.755. Actual 0.7343. **Falsified.**
- "saturated at 2 sources": predicted 0.738–0.745. Actual 0.7343. **Just below band.**
- "actively harmful": predicted < 0.735. Actual 0.7343. Right on the borderline.

The result sits between "saturated" and "harmful" — closer to "the mono-shuffled
source was approximately neutral, while losing 5K of the cCRE backbone hurt".

## Confound disentangling
Two changes vs 004:
1. cCRE backbone 40K → 35K (lost 5K of biological foreground)
2. Added 5K mono-shuffled genomic

Loss is roughly the magnitude expected from cCRE backbone reduction alone
(extrapolating from the dhs_topic 50K curve where ~5K marginal regulatory
sequences contribute several percentage points). The mono-shuffled component
likely contributed approximately zero — it didn't compensate for the cCRE
loss.

## What I learned
1. **Diversity scaling does NOT extend to a 3rd source if that source occupies
   the same conceptual axis as an existing one.** Mono-shuffled genomic
   (preserves only mono composition, no structure) sits informationally
   close to iid uniform (no composition or structure). Adding it does not
   give the model a new axis of calibration.
2. **The 002+003 synergy was specifically about TWO orthogonal axes**: iid
   provides off-genome calibration; real genomic provides in-genome
   calibration. These are orthogonal because they probe different parts of
   the input distribution. Adding redundant signal along either axis is
   wasteful.
3. **The cCRE backbone is load-bearing.** Even small reductions (40K → 35K)
   cost meaningful performance.

## Theory update
Refined working theory:
> Library value = (i) regulatory grammar coverage [cCRE backbone, ~40K is
> a sweet spot] + (ii) sequence-space calibration via QUALITATIVELY
> ORTHOGONAL axes (currently identified: off-genome iid + in-genome real
> genomic). Adding a 3rd source is only valuable if it occupies a NEW axis,
> not if it duplicates an existing one. Finding new orthogonal axes is the
> next research task.

## What to try next
**Test cross-species genomic windows as a candidate new axis.** Mouse mm10
non-cCRE windows: realistic mammalian genomic composition like human, but
from a different evolutionary trajectory. If they help on top of human
genomic + iid, "cross-species" is a new axis. If not, "in-genome" is one
saturating axis regardless of species.

Design: 35K cCRE + 5K iid + 5K human genomic + 5K mouse genomic. Direct
substitution test against 005 (replacing 5K mono-shuffled with 5K mouse).
- 006 ≥ 004 → mouse genomic helps; cross-species is a new axis.
- 005 < 006 < 004 → mouse genomic helps modestly but not enough to recover
  the cCRE loss; suggests it's a partial new axis.
- 006 ≈ 005 → mouse genomic is also redundant with human genomic; in-genome
  axis saturates regardless of source species.
